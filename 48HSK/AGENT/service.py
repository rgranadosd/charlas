"""HTTP service mode for WSO2 Agent Manager integration."""

from __future__ import annotations

import os
import uuid
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

from agent_core import RafaAgent
from observability import bootstrap_fastapi_observability, get_current_trace_id
from request_identity import CallerIdentity, use_caller_identity


class InvokeRequest(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    allow_interactive_auth: bool = False


class InvokeResponse(BaseModel):
    answer: str
    session_id: str
    model: str
    trace_id: Optional[str] = None
    status: str


app = FastAPI(title="Rafa Agent Service", version="0.1.0")
bootstrap_fastapi_observability(app, service_name=os.getenv("OTEL_SERVICE_NAME", "rafa-agent-service"))

agent = RafaAgent(
    force_auth=False,
    debug_mode=os.getenv("DEBUG", "false").lower() in {"1", "true", "yes", "on"},
    env_profile=os.getenv("AGENT_ENV_PROFILE", "service"),
    model_id=os.getenv("AGENT_MODEL_ID", "gpt-4o-mini"),
)


def _extract_trace_id_from_request(request: Request) -> Optional[str]:
    current_trace_id = get_current_trace_id()
    if current_trace_id:
        return current_trace_id

    explicit_trace_id = request.headers.get("x-trace-id") or request.headers.get("x-correlation-id")
    if explicit_trace_id:
        return explicit_trace_id

    traceparent = request.headers.get("traceparent")
    if not traceparent:
        return None

    parts = traceparent.split("-")
    if len(parts) >= 4 and len(parts[1]) == 32:
        return parts[1]
    return traceparent


def _extract_caller_access_token(request: Request) -> Optional[str]:
    authorization = request.headers.get("authorization")
    if not authorization:
        return None

    scheme, _, credentials = authorization.partition(" ")
    if scheme.lower() != "bearer" or not credentials.strip():
        return None

    return credentials.strip()


def _require_caller_access_token(request: Request) -> str:
    access_token = _extract_caller_access_token(request)
    if access_token:
        return access_token

    raise HTTPException(
        status_code=401,
        detail="Missing caller bearer token",
        headers={"WWW-Authenticate": "Bearer"},
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
    caller_identity = CallerIdentity(
        access_token=_require_caller_access_token(request),
        user_id=payload.user_id,
        metadata=payload.metadata,
    )

    try:
        with use_caller_identity(caller_identity):
            answer = await agent.ask(
                payload.message,
                silent=True,
                allow_interactive_auth=payload.allow_interactive_auth,
            )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    trace_id = _extract_trace_id_from_request(request)
    session_id = payload.session_id or f"session-{uuid.uuid4().hex[:12]}"

    return InvokeResponse(
        answer=answer,
        session_id=session_id,
        model=agent.model_id,
        trace_id=trace_id,
        status="ok",
    )


def run() -> None:
    import uvicorn

    host = os.getenv("SERVICE_HOST", "0.0.0.0")
    port = int(os.getenv("SERVICE_PORT", "8010"))
    uvicorn.run("service:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    run()
