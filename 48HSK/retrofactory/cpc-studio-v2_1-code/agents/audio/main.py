"""Audio Agent — FastAPI server returning fixed audio scaffold.

The audio for Amstrad CPC is generated from fixed templates (no LLM needed).
The orchestrator calls this agent for audio tasks; it returns the pre-written
audio.h and audio.c via the DevelopmentOutput contract.

Endpoint: POST /run
  body:    DevelopmentInput
  returns: DevelopmentOutput with files_to_write = []
           (files are written by the orchestrator via _scaffold_audio before tasks run)
"""
from __future__ import annotations

import uvicorn
from fastapi import FastAPI
from scene_agent.contracts import DevelopmentInput, DevelopmentOutput

app = FastAPI(title="CPC Studio — Audio Agent")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/run", response_model=DevelopmentOutput)
def run(dev_input: DevelopmentInput) -> DevelopmentOutput:
    return DevelopmentOutput(
        task_id=dev_input.task_id,
        status="done",
        summary="Audio handled by scaffold (audio.h + audio.c already written by orchestrator).",
        files_to_write=[],
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
