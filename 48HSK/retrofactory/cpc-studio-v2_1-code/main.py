"""FastAPI wrapper — exposes CPC Studio pipeline as a Chat Agent for WSO2 Agent Manager.

Endpoint: POST /chat
  body:    { "session_id": str, "message": str }
  returns: { "response": str }

The `message` field is passed directly as the game generation prompt.
The pipeline runs synchronously in a thread to avoid blocking the event loop.
"""
from __future__ import annotations

import asyncio
import json
import os
import re
import uuid
from pathlib import Path
from threading import Lock
from time import time

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


class JobSummary(BaseModel):
    job_id: str
    session_id: str | None = None
    status: str
    created_at: float | None = None
    updated_at: float | None = None


class JobListResponse(BaseModel):
    jobs: list[JobSummary]


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
_JOBS_FILE = os.getenv("CPC_PM_JOBS_FILE", "/tmp/cpc_pm_jobs.json")


def _save_jobs_to_disk() -> None:
    tmp_path = f"{_JOBS_FILE}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(_PIPELINE_JOBS, f, ensure_ascii=False)
    os.replace(tmp_path, _JOBS_FILE)


def _load_jobs_from_disk() -> None:
    if not os.path.exists(_JOBS_FILE):
        return
    try:
        with open(_JOBS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                _PIPELINE_JOBS.update(data)
    except Exception:
        # Keep startup resilient even if jobs file is corrupt.
        return


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
        job = _PIPELINE_JOBS.get(job_id, {})
        job["status"] = "running"
        job["response"] = None
        job["error"] = None
        job["updated_at"] = time()
        _PIPELINE_JOBS[job_id] = job
        _save_jobs_to_disk()

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
            job = _PIPELINE_JOBS.get(job_id, {})
            job["status"] = "completed"
            job["response"] = response
            job["error"] = None
            job["updated_at"] = time()
            _PIPELINE_JOBS[job_id] = job
            _save_jobs_to_disk()
    except Exception as exc:
        with _PIPELINE_JOBS_LOCK:
            job = _PIPELINE_JOBS.get(job_id, {})
            job["status"] = "failed"
            job["response"] = None
            job["error"] = str(exc)
            job["updated_at"] = time()
            _PIPELINE_JOBS[job_id] = job
            _save_jobs_to_disk()


@app.on_event("startup")
async def startup_event() -> None:
    with _PIPELINE_JOBS_LOCK:
        _load_jobs_from_disk()


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    if not _should_run_pipeline(req.message):
        return ChatResponse(response=_chat_only_response(), status="completed")

    job_id = uuid.uuid4().hex
    project_name = _project_name(req.session_id)

    with _PIPELINE_JOBS_LOCK:
        _PIPELINE_JOBS[job_id] = {
            "status": "accepted",
            "response": None,
            "error": None,
            "session_id": req.session_id,
            "project_name": project_name,
            "created_at": time(),
            "updated_at": time(),
        }
        _save_jobs_to_disk()

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


@app.get("/jobs", response_model=JobListResponse)
async def list_jobs(session_id: str | None = None, limit: int = 20) -> JobListResponse:
    if limit < 1:
        limit = 1
    if limit > 200:
        limit = 200

    with _PIPELINE_JOBS_LOCK:
        items = list(_PIPELINE_JOBS.items())

    summaries: list[JobSummary] = []
    for job_id, job in items:
        sid = job.get("session_id")
        if session_id and sid != session_id:
            continue
        summaries.append(
            JobSummary(
                job_id=job_id,
                session_id=str(sid) if sid is not None else None,
                status=str(job.get("status") or "unknown"),
                created_at=float(job.get("created_at")) if job.get("created_at") is not None else None,
                updated_at=float(job.get("updated_at")) if job.get("updated_at") is not None else None,
            )
        )

    summaries.sort(key=lambda j: j.updated_at or 0.0, reverse=True)
    return JobListResponse(jobs=summaries[:limit])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
