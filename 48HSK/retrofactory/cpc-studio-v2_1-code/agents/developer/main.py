"""Developer Agent — FastAPI server wrapping run_task().

Endpoint: POST /run
  body:    DevelopmentInput (task definition from orchestrator)
  returns: DevelopmentOutput (generated files + status)
"""
from __future__ import annotations

import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException
from scene_agent.contracts import DevelopmentInput, DevelopmentOutput
from scene_agent.developer_agent import run_task
from scene_agent.settings import AppSettings

app = FastAPI(title="CPC Studio — Developer Agent")


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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
