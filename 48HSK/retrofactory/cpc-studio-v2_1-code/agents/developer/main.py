"""Developer Agent — FastAPI server wrapping run_task().

Endpoint: POST /run
  body:    DevelopmentInput (task definition from orchestrator)
  returns: DevelopmentOutput (generated files + status)

Endpoint: POST /chat  (WSO2 Agent Manager "Try it out" adapter)
  body:    { "session_id": str, "message": str }
  returns: { "response": str, "status": str, ...tokens }
  The free-text message becomes the task goal; the structured output is
  rendered as a human-readable summary so the chat widget can display it.
"""
from __future__ import annotations

import asyncio
import re
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scene_agent.contracts import DevelopmentInput, DevelopmentOutput
from scene_agent.developer_agent import run_task
from scene_agent.settings import AppSettings

app = FastAPI(title="CPC Studio — Developer Agent")


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
    status: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None


_IDENTITY = (
    "Soy el **Developer Agent** de CPC Studio.\n\n"
    "Genero código C89 para juegos en CPCtelera (Amstrad CPC): gameplay, HUD, "
    "colisiones, render de sprites y cualquier lógica de juego.\n\n"
    "Dime qué implementar, por ejemplo:\n"
    "- *'implementa el movimiento del paddle y la colisión con la bola'*\n"
    "- *'añade el sistema de puntuación y vidas al HUD'*\n\n"
    "Te devuelvo un `src/main.c` completo y compilable."
)

_CONVERSATIONAL = re.compile(
    r"^\s*(?:"
    r"qui[eé]n?\s+eres|who\s+are\s+you|what\s+are\s+you"
    r"|hola|hello|hi|hey|help|ayuda|qu[eé]\s+haces|what\s+do\s+you\s+do"
    r"|buenas?|saludos?|cpc.?developer"
    r")\s*\??$",
    re.IGNORECASE,
)

_TASK_HINT = re.compile(
    r"\b(?:implement[ae]?|a[ñn]ade?|add|crea?(?:te)?|genera?(?:te)?|fix|escribe?|write"
    r"|src/main|main\.c|hud|score|lives|paddle|ball|brick|ghost|maze|player|sprite"
    r"|colisi[oó]n|collision|movimiento|movement|render|draw|init|loop|game"
    r"|cpct_|cpctelera|sdcc)\b",
    re.IGNORECASE,
)


def _is_task(message: str) -> bool:
    if _CONVERSATIONAL.match(message):
        return False
    if _TASK_HINT.search(message):
        return True
    return len(message.split()) > 8


def _project_name(session_id: str) -> str:
    slug = re.sub(r"[^a-z0-9]", "_", (session_id or "")[:24].lower()).strip("_")
    return slug or "chat"


def _render_output(out: DevelopmentOutput) -> str:
    """Render a DevelopmentOutput as a chat-friendly text summary."""
    lines = [f"**status:** {out.status}", "", out.summary or ""]
    if out.files_to_write:
        lines.append("")
        lines.append("**Generated files:**")
        for f in out.files_to_write:
            preview = (f.content or "").strip().splitlines()
            head = "\n".join(preview[:40])
            lines.append(f"\n`{f.path}` ({f.mode}):\n```c\n{head}\n```")
    for note in out.notes:
        lines.append(f"\n- note: {note}")
    for q in out.follow_up_questions:
        lines.append(f"\n- ❓ {q}")
    return "\n".join(lines).strip()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/run", response_model=DevelopmentOutput)
async def run(dev_input: DevelopmentInput) -> DevelopmentOutput:
    settings = AppSettings()
    try:
        return await asyncio.to_thread(run_task, dev_input, settings)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    message = (req.message or "").strip()
    if not message or not _is_task(message):
        return ChatResponse(response=_IDENTITY, status="ready")
    dev_input = DevelopmentInput(
        task_id=f"chat-{_project_name(req.session_id)}",
        project_name=_project_name(req.session_id),
        goal=message,
    )
    settings = AppSettings()
    try:
        out = await asyncio.to_thread(run_task, dev_input, settings)
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
