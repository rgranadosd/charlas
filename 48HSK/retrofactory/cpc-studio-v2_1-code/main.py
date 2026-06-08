"""FastAPI wrapper — exposes CPC Studio pipeline as a Chat Agent for WSO2 Agent Manager.

Endpoint: POST /chat
  body:    { "session_id": str, "message": str }
  returns: { "response": str }

The `message` field is passed directly as the game generation prompt.
The pipeline runs synchronously in a thread to avoid blocking the event loop.
"""
from __future__ import annotations

import asyncio
import re
import uuid
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from scene_agent.pipeline import run_pipeline
from scene_agent.settings import AppSettings

app = FastAPI(title="CPC Studio Agent")


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    project: str
    message: str
    run_dir: str | None = None
    dsk_file: str | None = None


_jobs: dict[str, dict[str, str | None]] = {}


_CHAT_INTENT_PATTERNS = [
    r"\bquien\s+eres\b",
    r"\bqui[eé]n\s+eres\b",
    r"\bwhat\s+are\s+you\b",
    r"\bwho\s+are\s+you\b",
    r"\bhello\b",
    r"\bhi\b",
    r"\bhola\b",
    r"\bhelp\b",
    r"\bayuda\b",
]

_GAME_INTENT_PATTERNS = [
    r"\b(game|juego)\b",
    r"\b(build|crear|create|genera|generate)\b",
    r"\b(level|nivel|sprite|hud|score|lives|paddle|ball)\b",
    r"\b(cpc|cpctelera|amstrad|dsk)\b",
]


def _project_name(session_id: str) -> str:
    """Derive a filesystem-safe project name from the session ID."""
    slug = re.sub(r"[^a-z0-9]", "_", session_id[:24].lower()).strip("_")
    return slug or "game"


def _should_run_pipeline(message: str) -> bool:
    text = message.strip().lower()
    if not text:
        return False

    if any(re.search(p, text) for p in _CHAT_INTENT_PATTERNS):
        return any(re.search(p, text) for p in _GAME_INTENT_PATTERNS)

    return True


def _chat_only_response() -> str:
    return (
        "Soy CPC-PM, el Product Manager de juegos para Amstrad CPC. "
        "Puedo ayudarte a definir y generar un juego (escenas, HUD, reglas, assets y build). "
        "Si quieres que empiece a construir, dime el juego que quieres crear."
    )


async def _run_pipeline_job(job_id: str, prompt: str, project_name: str) -> None:
    settings = AppSettings()
    _jobs[job_id] = {
        "status": "running",
        "project": project_name,
        "message": "Procesando pipeline de generación...",
        "run_dir": None,
        "dsk_file": None,
    }

    try:
        run_dir, compile_ok = await asyncio.to_thread(
            run_pipeline,
            prompt,
            project_name,
            settings,
            True,   # no_emu — no emulator available in the container
            False,  # dry_run
        )

        run_dir_path = Path(run_dir)
        dsk_files = list(run_dir_path.glob("*.dsk"))
        dsk_name = dsk_files[0].name if dsk_files else None

        if compile_ok:
            _jobs[job_id] = {
                "status": "succeeded",
                "project": project_name,
                "message": "Juego generado correctamente.",
                "run_dir": run_dir_path.name,
                "dsk_file": dsk_name,
            }
        else:
            _jobs[job_id] = {
                "status": "failed",
                "project": project_name,
                "message": "El pipeline terminó pero la compilación no fue exitosa.",
                "run_dir": run_dir_path.name,
                "dsk_file": dsk_name,
            }
    except Exception as exc:
        _jobs[job_id] = {
            "status": "failed",
            "project": project_name,
            "message": f"Error ejecutando pipeline: {exc}",
            "run_dir": None,
            "dsk_file": None,
        }


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    if not _should_run_pipeline(req.message):
        return ChatResponse(response=_chat_only_response())

    project_name = _project_name(req.session_id)
    job_id = str(uuid.uuid4())
    _jobs[job_id] = {
        "status": "queued",
        "project": project_name,
        "message": "Trabajo en cola.",
        "run_dir": None,
        "dsk_file": None,
    }
    asyncio.create_task(_run_pipeline_job(job_id, req.message, project_name))

    return ChatResponse(
        response=(
            f"He iniciado la generación en segundo plano. "
            f"job_id={job_id}. "
            f"Consulta el estado en GET /jobs/{job_id}."
        )
    )


@app.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def job_status(job_id: str) -> JobStatusResponse:
    job = _jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job_id no encontrado")

    return JobStatusResponse(
        job_id=job_id,
        status=str(job.get("status") or "unknown"),
        project=str(job.get("project") or "unknown"),
        message=str(job.get("message") or ""),
        run_dir=job.get("run_dir"),
        dsk_file=job.get("dsk_file"),
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
