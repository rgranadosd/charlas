from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException

from app.config import get_settings
from app.models.schemas import UserTokenRequest
from app.services.jwt_debug_service import build_token_artifact
from app.state.session_store import session_store

router = APIRouter(tags=["session"])


def _require_session_id(session_id: str | None) -> str:
    if not session_id:
        raise HTTPException(status_code=400, detail="X-Demo-Session-Id header is required")
    return session_id


@router.get("/api/session")
async def get_session(x_demo_session_id: str | None = Header(default=None)) -> dict:
    settings = get_settings()
    session_id = _require_session_id(x_demo_session_id)
    return session_store.serialize_session(session_id, settings.debug_show_full_tokens)


@router.post("/api/session/user-token")
async def store_user_token(
    payload: UserTokenRequest,
    x_demo_session_id: str | None = Header(default=None),
) -> dict:
    settings = get_settings()
    session_id = _require_session_id(x_demo_session_id)
    artifact = build_token_artifact(
        payload.access_token,
        explanation="Emitido por WSO2 IS para la sesion del usuario en la SPA.",
        consumer="Frontend SPA y trazas didacticas",
        issuer_hint=settings.wso2_issuer,
    )
    if payload.user_profile:
        artifact["claims"] = {**artifact["claims"], "spa_profile": payload.user_profile}
        artifact["subject"] = artifact["claims"].get("sub") or payload.user_profile.get("username")
    session_store.set_user_token(session_id, artifact)
    session_store.append_trace(
        session_id,
        {
            "action": "Sincronizar USER_TOKEN",
            "endpoint": "/api/session/user-token",
            "method": "POST",
            "request_parameters": {
                "access_token_preview": artifact.get("token")[:18] if artifact.get("token") else None,
            },
            "response_status": 200,
            "response_body": {"subject": artifact.get("subject"), "scopes": artifact.get("scopes", [])},
            "functional_interpretation": "La SPA entrego su access token al backend para enriquecer la vista de artefactos de la demo.",
            "security_interpretation": "Este token autentica al usuario en la SPA, pero no sustituye al token del agente ni al OBO token.",
        },
    )
    return session_store.serialize_session(session_id, settings.debug_show_full_tokens)
