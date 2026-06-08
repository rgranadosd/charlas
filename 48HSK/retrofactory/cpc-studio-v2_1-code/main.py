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
from threading import Lock

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
    job_id: str | None = None
    status: str | None = None


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    response: str | None = None
    error: str | None = None


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


_PIPELINE_JOBS: dict[str, dict[str, str | None]] = {}
_PIPELINE_JOBS_LOCK = Lock()


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


def _run_pipeline_job(job_id: str, message: str, project_name: str) -> None:
    settings = AppSettings()
    with _PIPELINE_JOBS_LOCK:
        _PIPELINE_JOBS[job_id] = {
            "status": "running",
            "response": None,
            "error": None,
        }

    try:
        run_dir, compile_ok = run_pipeline(
            message,
            project_name,
            settings,
            True,   # no_emu — no emulator available in the container
            False,  # dry_run
        )

        run_dir_path = Path(run_dir)
        if compile_ok:
            dsk_files = list(run_dir_path.glob("*.dsk"))
            dsk_name = dsk_files[0].name if dsk_files else "sin .dsk"
            response = (
                f"Juego generado correctamente.\n"
                f"Proyecto: {project_name}\n"
                f"Directorio de salida: {run_dir_path.name}\n"
                f"Archivo DSK: {dsk_name}"
            )
        else:
            response = (
                f"El pipeline se ejecutó pero la compilación no fue exitosa.\n"
                f"Proyecto: {project_name}\n"
                f"Revisa los logs del agente para más detalles."
            )

        with _PIPELINE_JOBS_LOCK:
            _PIPELINE_JOBS[job_id] = {
                "status": "completed",
                "response": response,
                "error": None,
            }
    except Exception as exc:
        with _PIPELINE_JOBS_LOCK:
            _PIPELINE_JOBS[job_id] = {
                "status": "failed",
                "response": None,
                "error": str(exc),
            }


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    if not _should_run_pipeline(req.message):
        return ChatResponse(response=_chat_only_response(), status="completed")

    job_id = uuid.uuid4().hex
    project_name = _project_name(req.session_id)

    loop = asyncio.get_running_loop()
    loop.run_in_executor(None, _run_pipeline_job, job_id, req.message, project_name)

    return ChatResponse(
        response=(
            "Solicitud aceptada. El pipeline se está ejecutando en segundo plano. "
            f"Consulta GET /jobs/{job_id} para ver el estado y el resultado final."
        ),
        job_id=job_id,
        status="accepted",
    )


@app.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str) -> JobStatusResponse:
    with _PIPELINE_JOBS_LOCK:
        job = _PIPELINE_JOBS.get(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="job_id no encontrado")

    return JobStatusResponse(
        job_id=job_id,
        status=str(job.get("status") or "unknown"),
        response=job.get("response"),
        error=job.get("error"),
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
