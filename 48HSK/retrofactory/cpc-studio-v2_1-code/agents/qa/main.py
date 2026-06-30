"""QA Agent — FastAPI server wrapping run_qa().

Endpoint: POST /run
  body:    { "user_prompt": str, "main_c": str }
  returns: { "violations": [str] }   (empty list = code honours the prompt)

Game-agnostic: the review criteria ARE the user's original prompt.

Endpoint: POST /chat  (WSO2 Agent Manager "Try it out" adapter)
  body:    { "session_id": str, "message": str }
  The message must carry the C source to review inside a fenced ```code``` block;
  any text outside the block becomes the review prompt (the acceptance criteria).
"""
from __future__ import annotations

import asyncio
import re

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from qa_agent import run_qa
from common.settings import AppSettings

app = FastAPI(title="CPC Studio — QA Agent")


class QAInput(BaseModel):
    user_prompt: str
    main_c: str


class QAOutput(BaseModel):
    violations: list[str]


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
    status: str | None = None


_CODE_BLOCK = re.compile(r"```(?:[a-zA-Z0-9_+-]*)\n(.*?)```", re.DOTALL)


def _split_message(message: str) -> tuple[str, str]:
    """Return (user_prompt, main_c). Code goes in a fenced block; prose is the prompt."""
    blocks = _CODE_BLOCK.findall(message)
    main_c = "\n\n".join(b.strip() for b in blocks).strip()
    prompt = _CODE_BLOCK.sub("", message).strip()
    return prompt, main_c


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/run", response_model=QAOutput)
async def run(qa_in: QAInput) -> QAOutput:
    settings = AppSettings()
    try:
        violations = await asyncio.to_thread(run_qa, qa_in.user_prompt, qa_in.main_c, settings)
        return QAOutput(violations=violations)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    user_prompt, main_c = _split_message(req.message or "")
    if not main_c:
        return ChatResponse(
            response=(
                "I'm the QA agent: I check whether C code honours a prompt. "
                "Send the source to review inside a fenced code block, e.g.\n\n"
                "```\n#include <cpctelera.h>\nvoid main(void){...}\n```\n\n"
                "and (optionally) the requirements as plain text above it."
            ),
            status="needs_clarification",
        )
    settings = AppSettings()
    try:
        violations = await asyncio.to_thread(run_qa, user_prompt, main_c, settings)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    if not violations:
        return ChatResponse(response="✅ No violations — the code honours the prompt.", status="ok")
    body = "\n".join(f"- {v}" for v in violations)
    return ChatResponse(response=f"⚠️ Found {len(violations)} violation(s):\n{body}", status="needs_revision")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
