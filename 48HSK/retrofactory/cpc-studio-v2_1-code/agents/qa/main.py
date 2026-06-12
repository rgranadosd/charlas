"""QA Agent — FastAPI server wrapping run_qa().

Endpoint: POST /run
  body:    { "user_prompt": str, "main_c": str }
  returns: { "violations": [str] }   (empty list = code honours the prompt)

Game-agnostic: the review criteria ARE the user's original prompt.
"""
from __future__ import annotations

import asyncio

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from scene_agent.qa_agent import run_qa
from scene_agent.settings import AppSettings

app = FastAPI(title="CPC Studio — QA Agent")


class QAInput(BaseModel):
    user_prompt: str
    main_c: str


class QAOutput(BaseModel):
    violations: list[str]


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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
