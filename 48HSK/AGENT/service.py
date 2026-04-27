"""HTTP service mode for WSO2 Agent Manager integration."""

from __future__ import annotations

import os
import uuid
from typing import Any, Dict, Literal, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

from agent_core import RafaAgent
from observability import bootstrap_fastapi_observability, get_current_trace_id
from request_identity import CallerIdentity, use_caller_identity


APP_DESCRIPTION = (
    "Stable HTTP contract for the Rafa agent service. "
    "Service mode is always non-interactive: it accepts a caller bearer token, "
    "or falls back to configured service credentials when SERVICE_AUTH_MODE allows it."
)


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"


class ReadyResponse(BaseModel):
    status: Literal["ready", "initializing"]


class ErrorResponse(BaseModel):
    detail: str


class InvokeRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Prompt or command to send to the agent.")
    session_id: Optional[str] = Field(default=None, description="Opaque caller session identifier.")
    user_id: Optional[str] = Field(
        default=None,
        description="Caller user identifier used as a fallback when resolving WSO2 permissions.",
    )
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Opaque caller metadata propagated internally.")
    allow_interactive_auth: bool = Field(
        default=False,
        description="Deprecated. Interactive auth is ignored in service mode and never opens a browser.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "lista productos",
                "session_id": "session-123",
                "user_id": "Rafa",
                "metadata": {"channel": "agent-manager"},
            }
        }
    }


class InvokeResponse(BaseModel):
    answer: str
    session_id: str
    model: str
    trace_id: Optional[str] = None
    status: Literal["ok"]

    model_config = {
        "json_schema_extra": {
            "example": {
                "answer": "He encontrado 5 productos.",
                "session_id": "session-123",
                "model": "gpt-4o-mini",
                "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
                "status": "ok",
            }
        }
    }


app = FastAPI(title="Rafa Agent Service", version="0.2.0", description=APP_DESCRIPTION)
bootstrap_fastapi_observability(app, service_name=os.getenv("OTEL_SERVICE_NAME", "rafa-agent-service"))

agent = RafaAgent(
    force_auth=False,
    debug_mode=os.getenv("DEBUG", "false").lower() in {"1", "true", "yes", "on"},
    env_profile=os.getenv("AGENT_ENV_PROFILE", "service"),
    model_id=os.getenv("AGENT_MODEL_ID", "gpt-4o-mini"),
)


def _service_auth_mode() -> str:
    raw_mode = (os.getenv("SERVICE_AUTH_MODE") or "caller-token").strip().lower()
    aliases = {
        "incoming-token": "caller-token",
        "incoming": "caller-token",
        "caller": "caller-token",
        "prefer-incoming-token": "prefer-caller-token",
        "prefer-caller": "prefer-caller-token",
        "service": "service-token",
    }
    mode = aliases.get(raw_mode, raw_mode)
    if mode not in {"caller-token", "prefer-caller-token", "service-token"}:
        raise RuntimeError(f"Invalid SERVICE_AUTH_MODE: {raw_mode}")
    return mode


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


def _extract_service_access_token() -> Optional[str]:
    env_token = (os.getenv("WSO2_SERVICE_ACCESS_TOKEN") or "").strip()
    if env_token:
        return env_token

    token_file = (os.getenv("WSO2_SERVICE_ACCESS_TOKEN_FILE") or "").strip()
    if not token_file:
        return None

    try:
        with open(token_file, "r", encoding="utf-8") as handle:
            token = handle.read().strip()
    except OSError as exc:
        raise RuntimeError(f"Unable to read WSO2 service access token file: {exc}") from exc

    return token or None


def _build_request_identity(payload: InvokeRequest, request: Request) -> CallerIdentity:
    mode = _service_auth_mode()
    caller_access_token = _extract_caller_access_token(request)
    service_access_token = _extract_service_access_token()
    metadata = dict(payload.metadata or {})

    if mode == "service-token":
        if not service_access_token:
            raise HTTPException(
                status_code=401,
                detail="Missing configured service access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        metadata.setdefault("auth_source", "service_token")
        return CallerIdentity(
            access_token=service_access_token,
            user_id=payload.user_id or os.getenv("WSO2_SERVICE_USER_ID"),
            metadata=metadata,
        )

    if caller_access_token:
        metadata.setdefault("auth_source", "caller_token")
        return CallerIdentity(
            access_token=caller_access_token,
            user_id=payload.user_id,
            metadata=metadata,
        )

    if mode == "prefer-caller-token" and service_access_token:
        metadata.setdefault("auth_source", "service_token")
        return CallerIdentity(
            access_token=service_access_token,
            user_id=payload.user_id or os.getenv("WSO2_SERVICE_USER_ID"),
            metadata=metadata,
        )

    detail = "Missing caller bearer token"
    if mode == "prefer-caller-token":
        detail = "Missing caller bearer token or configured service access token"

    raise HTTPException(
        status_code=401,
        detail=detail,
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


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Liveness probe for the service process.",
)
async def health() -> HealthResponse:
    return HealthResponse()


@app.get(
    "/ready",
    response_model=ReadyResponse,
    summary="Readiness check",
    description="Readiness probe that reflects whether the agent runtime finished initialization.",
)
async def ready() -> ReadyResponse:
    return ReadyResponse(status="ready" if agent.is_ready else "initializing")


@app.post(
    "/invoke",
    response_model=InvokeResponse,
    summary="Invoke the agent",
    description=(
        "Stable invocation endpoint for Agent Manager or external callers. "
        "Service mode never opens a browser and always uses a caller token or configured backend credentials."
    ),
    responses={
        401: {"model": ErrorResponse, "description": "Missing caller bearer token or service credentials."},
        500: {"model": ErrorResponse, "description": "Agent invocation failed."},
    },
)
async def invoke(payload: InvokeRequest, request: Request) -> InvokeResponse:
    caller_identity = _build_request_identity(payload, request)

    try:
        with use_caller_identity(caller_identity):
            answer = await agent.ask(
                payload.message,
                silent=True,
                allow_interactive_auth=False,
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
    uvicorn.run(app, host=host, port=port, reload=False)


if __name__ == "__main__":
    run()
