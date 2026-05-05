from __future__ import annotations

from typing import Any

import httpx
from fastapi import APIRouter, Header, HTTPException

from app.config import get_settings
from app.models.schemas import ProtectedAccessRequest
from app.state.session_store import session_store

router = APIRouter(tags=["tests"])


def _require_session_id(session_id: str | None) -> str:
    if not session_id:
        raise HTTPException(status_code=400, detail="X-Demo-Session-Id header is required")
    return session_id


async def _call_resource_api(
    *,
    token: str,
    label: str,
    session_id: str,
    payload: ProtectedAccessRequest,
) -> dict[str, Any]:
    settings = get_settings()
    url = f"{settings.resource_api_base_url}{payload.resource_path}"
    method = payload.method.upper()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(timeout=settings.resource_api_timeout_seconds, verify=False) as client:
        response = await client.request(method, url, json=payload.payload, headers=headers)
    try:
        response_body: Any = response.json()
    except ValueError:
        response_body = response.text

    security_explanation = (
        response_body.get("token_analysis", {}).get("security_explanation")
        if isinstance(response_body, dict)
        else "Resource API returned a non-JSON response"
    )
    request_payload = {
        "method": method,
        "url": url,
        "headers": {"Authorization": f"Bearer {token[:18]}..."},
        "json": payload.payload,
    }
    response_payload = {"status_code": response.status_code, "body": response_body}
    session_store.set_last_api_interaction(
        session_id,
        request_payload=request_payload,
        response_payload=response_payload,
        security_explanation=security_explanation,
    )
    session_store.append_trace(
        session_id,
        {
            "action": label,
            "endpoint": url,
            "method": method,
            "request_parameters": request_payload,
            "response_status": response.status_code,
            "response_body": response_body,
            "functional_interpretation": "La demo llamo a la API protegida para contrastar token autonomo frente a token delegado.",
            "security_interpretation": security_explanation,
        },
    )
    return session_store.serialize_session(session_id, settings.debug_show_full_tokens)


@router.post("/api/agent-token")
async def agent_token(x_demo_session_id: str | None = Header(default=None)) -> dict:
    from app.services.agent_token_service import agent_token_service

    session_id = _require_session_id(x_demo_session_id)
    return await agent_token_service.fetch_and_store(session_id)


@router.post("/api/test/agent-access")
async def test_agent_access(
    payload: ProtectedAccessRequest,
    x_demo_session_id: str | None = Header(default=None),
) -> dict:
    session_id = _require_session_id(x_demo_session_id)
    current = session_store.get_or_create(session_id)
    artifact = current.get("agent_token")
    if not artifact or not artifact.get("token"):
        raise HTTPException(status_code=400, detail="AGENT_TOKEN is missing")
    return await _call_resource_api(
        token=artifact["token"],
        label="Probar acceso con AGENT_TOKEN",
        session_id=session_id,
        payload=payload,
    )


@router.post("/api/test/obo-access")
async def test_obo_access(
    payload: ProtectedAccessRequest,
    x_demo_session_id: str | None = Header(default=None),
) -> dict:
    session_id = _require_session_id(x_demo_session_id)
    current = session_store.get_or_create(session_id)
    artifact = current.get("obo_token")
    if not artifact or not artifact.get("token"):
        raise HTTPException(status_code=400, detail="OBO_TOKEN is missing")
    return await _call_resource_api(
        token=artifact["token"],
        label="Leer mis ficheros con OBO_TOKEN",
        session_id=session_id,
        payload=payload,
    )
