"""Audio Agent — FastAPI server wrapping run_audio_task().

Generates the CPCtelera AY-3-8912 audio subsystem (src/audio.h + src/audio.c)
with an LLM, specialised for the SFX the game described in the task needs.

Endpoint: POST /run
  body:    DevelopmentInput (audio task from the orchestrator)
  returns: DevelopmentOutput (files_to_write = audio.h + audio.c)
"""
from __future__ import annotations

import asyncio

import uvicorn
from fastapi import FastAPI, HTTPException

from scene_agent.contracts import DevelopmentInput, DevelopmentOutput
from scene_agent.audio_agent import run_audio_task
from scene_agent.settings import AppSettings

app = FastAPI(title="CPC Studio — Audio Agent")


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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
