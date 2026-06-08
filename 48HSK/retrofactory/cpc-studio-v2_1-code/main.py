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


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    if not _should_run_pipeline(req.message):
        return ChatResponse(response=_chat_only_response())

    settings = AppSettings()
    project_name = _project_name(req.session_id)

    try:
        run_dir, compile_ok = await asyncio.to_thread(
            run_pipeline,
            req.message,
            project_name,
            settings,
            True,   # no_emu — no emulator available in the container
            False,  # dry_run
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

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

    return ChatResponse(response=response)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
