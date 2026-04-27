"""HTTP service mode for WSO2 Agent Manager integration."""

from __future__ import annotations

import os
import uuid
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

from agent_core import RafaAgent


class InvokeRequest(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    auth_mode: Optional[str] = "service"


class InvokeResponse(BaseModel):
    answer: str
    session_id: str
    model: str
    trace_id: Optional[str] = None


app = FastAPI(title="Rafa Agent Service", version="0.1.0")
agent = RafaAgent(
    force_auth=False,
    debug_mode=os.getenv("DEBUG", "false").lower() in {"1", "true", "yes", "on"},
    env_profile=os.getenv("AGENT_ENV_PROFILE", "service"),
    model_id=os.getenv("AGENT_MODEL_ID", "gpt-4o-mini"),
)


@app.on_event("startup")
async def startup_event() -> None:
    # Lazy failures are still handled in /invoke, but startup warms config/kernel paths.
    try:
        agent.initialize()
    except Exception:
        # Keep service up for diagnostics; readiness endpoint will reflect status.
        pass


@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs", status_code=307)


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
async def ready() -> Dict[str, str]:
    return {"status": "ready" if agent.is_ready else "initializing"}


@app.post("/invoke", response_model=InvokeResponse)
async def invoke(payload: InvokeRequest, request: Request) -> InvokeResponse:
    try:
        allow_interactive_auth = str(payload.auth_mode or "service").strip().lower() in {
            "interactive",
            "user",
            "user-pkce",
        }
        answer = await agent.ask(
            payload.message,
            silent=True,
            allow_interactive_auth=allow_interactive_auth,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    trace_id = (
        request.headers.get("x-trace-id")
        or request.headers.get("x-correlation-id")
        or request.headers.get("traceparent")
    )
    session_id = payload.session_id or f"session-{uuid.uuid4().hex[:12]}"

    return InvokeResponse(
        answer=answer,
        session_id=session_id,
        model=agent.model_id,
        trace_id=trace_id,
    )


def run() -> None:
    import uvicorn

    host = os.getenv("SERVICE_HOST", "0.0.0.0")
    port = int(os.getenv("SERVICE_PORT", "8010"))
    uvicorn.run("service:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    run()
