"""Audio Agent — FastAPI server wrapping run_audio_task().

Generates the CPCtelera AY-3-8912 audio subsystem (src/audio.h + src/audio.c)
with an LLM, specialised for the SFX the game described in the task needs.

Endpoint: POST /run
  body:    DevelopmentInput (audio task from the orchestrator)
  returns: DevelopmentOutput (files_to_write = audio.h + audio.c)

Endpoint: POST /chat  (WSO2 Agent Manager "Try it out" adapter)
  body:    { "session_id": str, "message": str }
  returns: { "response": str, "status": str, ...tokens }
"""
from __future__ import annotations

import asyncio
import re

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from scene_agent.contracts import DevelopmentInput, DevelopmentOutput
from scene_agent.audio_agent import run_audio_task
from scene_agent.settings import AppSettings

app = FastAPI(title="CPC Studio — Audio Agent")


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
    status: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None


def _project_name(session_id: str) -> str:
    slug = re.sub(r"[^a-z0-9]", "_", (session_id or "")[:24].lower()).strip("_")
    return slug or "chat"


def _render_output(out: DevelopmentOutput) -> str:
    lines = [f"**status:** {out.status}", "", out.summary or ""]
    if out.files_to_write:
        lines.append("")
        lines.append("**Generated audio files:**")
        for f in out.files_to_write:
            head = "\n".join((f.content or "").strip().splitlines()[:40])
            lines.append(f"\n`{f.path}` ({f.mode}):\n```c\n{head}\n```")
    for note in out.notes:
        lines.append(f"\n- note: {note}")
    return "\n".join(lines).strip()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/run", response_model=DevelopmentOutput)
async def run(dev_input: DevelopmentInput) -> DevelopmentOutput:
    settings = AppSettings()
    try:
        return await asyncio.to_thread(run_audio_task, dev_input, settings)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    message = (req.message or "").strip()
    if not message:
        return ChatResponse(response="Describe the sound effects / music the game needs.", status="needs_clarification")
    dev_input = DevelopmentInput(
        task_id=f"chat-{_project_name(req.session_id)}",
        project_name=_project_name(req.session_id),
        goal=message,
    )
    settings = AppSettings()
    try:
        out = await asyncio.to_thread(run_audio_task, dev_input, settings)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return ChatResponse(
        response=_render_output(out),
        status=out.status,
        input_tokens=out.input_tokens,
        output_tokens=out.output_tokens,
        total_tokens=out.total_tokens,
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
