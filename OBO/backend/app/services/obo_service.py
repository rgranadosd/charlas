from __future__ import annotations

import base64
import hashlib
import secrets
from typing import Any

from fastapi import HTTPException

from app.config import get_settings
from app.services.jwt_debug_service import (
    build_token_artifact,
    extract_actor,
    extract_delegated_agent_id,
    extract_scopes,
    extract_subject,
    iso_from_epoch,
    truncate_value,
    utcnow,
)
from app.services.oauth_service import oauth_service
from app.state.session_store import session_store


def _generate_state() -> str:
    return secrets.token_urlsafe(24)


def _generate_code_verifier() -> str:
    return secrets.token_urlsafe(64)


def _build_code_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


class OBOService:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def _enrich_opaque_token_artifact(self, artifact: dict[str, Any]) -> dict[str, Any]:
        token = artifact.get("token")
        if not token or artifact.get("claims"):
            return artifact

        introspection = await oauth_service.introspect_token(
            token=token,
            client_id=self.settings.introspection_client_id,
            client_secret=self.settings.introspection_client_secret,
        )
        if introspection["status_code"] >= 400 or not isinstance(introspection["body"], dict):
            return artifact

        claims = introspection["body"]
        exp_value = claims.get("exp")
        is_expired = False
        if exp_value is not None:
            try:
                is_expired = iso_from_epoch(exp_value) is not None and utcnow().timestamp() >= float(exp_value)
            except (TypeError, ValueError):
                is_expired = False

        artifact.update(
            {
                "claims": claims,
                "scopes": extract_scopes(claims),
                "expires_at": iso_from_epoch(exp_value),
                "subject": extract_subject(claims),
                "actor": extract_actor(claims),
                "issuer": claims.get("iss") or artifact.get("issuer"),
                "audience": claims.get("aud"),
                "issued_at": iso_from_epoch(claims.get("iat")),
                "status": "expired" if is_expired else artifact.get("status", "available"),
            }
        )
        return artifact

    def start(self, session_id: str) -> dict[str, Any]:
        current = session_store.get_or_create(session_id)
        agent = current.get("agent_token")
        if not agent:
            raise HTTPException(status_code=400, detail="AGENT_TOKEN is required before starting OBO")

        state = _generate_state()
        code_verifier = _generate_code_verifier()
        code_challenge = _build_code_challenge(code_verifier)
        scopes = [item for item in self.settings.obo_scope.split() if item]
        authorization_url = oauth_service.build_authorization_url(
            state=state,
            code_challenge=code_challenge,
            scopes=scopes,
        )
        session_store.start_delegation(
            session_id,
            authorization_url=authorization_url,
            state=state,
            code_verifier=code_verifier,
            code_challenge=code_challenge,
            scopes=scopes,
        )
        session_store.append_trace(
            session_id,
            {
                "action": "Iniciar delegacion OBO",
                "endpoint": self.settings.wso2_authorize_endpoint,
                "method": "GET",
                "request_parameters": {
                    "response_type": "code",
                    "client_id": self.settings.obo_client_id,
                    "redirect_uri": self.settings.obo_redirect_uri,
                    "scope": scopes,
                    "prompt": self.settings.obo_authorization_prompt,
                    "state": state,
                    "code_verifier_preview": truncate_value(code_verifier),
                    "code_challenge": code_challenge,
                },
                "response_status": 200,
                "response_body": {"authorization_url": authorization_url},
                "functional_interpretation": "El backend preparo el reto PKCE y la URL de consentimiento.",
                "security_interpretation": "El state mitiga CSRF y el code_verifier quedara reservado para el intercambio final del codigo.",
            },
        )
        return session_store.serialize_session(session_id, self.settings.debug_show_full_tokens)

    def complete_callback(self, state: str, code: str) -> str:
        session_id = session_store.complete_callback(state, code)
        if not session_id:
            raise HTTPException(status_code=400, detail="Unknown or expired OBO state")
        session_store.append_trace(
            session_id,
            {
                "action": "Recibir authorization_code",
                "endpoint": self.settings.obo_redirect_uri,
                "method": "GET",
                "request_parameters": {
                    "state": state,
                    "code_preview": truncate_value(code),
                },
                "response_status": 200,
                "response_body": {"state_validated": True},
                "functional_interpretation": "El backend recibio el codigo y valido el state contra la sesion pendiente.",
                "security_interpretation": "Solo ahora existe un authorization_code utilizable para el exchange OBO.",
            },
        )
        return session_id

    async def exchange(self, session_id: str) -> dict[str, Any]:
        current = session_store.get_or_create(session_id)
        authorization_code = current.get("authorization_code")
        agent = current.get("agent_token")
        code_verifier = current.get("code_verifier")
        if not authorization_code:
            raise HTTPException(status_code=400, detail="AUTHORIZATION_CODE is not available yet")
        if not agent:
            raise HTTPException(status_code=400, detail="AGENT_TOKEN is missing")
        if not code_verifier:
            raise HTTPException(status_code=400, detail="PKCE code_verifier is missing")

        result = await oauth_service.exchange_code_for_obo(
            code=authorization_code,
            code_verifier=code_verifier,
            agent_token=agent["token"],
        )
        if result["status_code"] >= 400:
            raise HTTPException(
                status_code=result["status_code"],
                detail={
                    "message": "WSO2 IS rejected the OBO token exchange",
                    "oauth_response": result["body"],
                    "request_payload": result["request_payload"],
                    "note": "Si tu despliegue de WSO2 IS 7.2 usa parametros distintos para OBO, ajusta backend/app/services/oauth_service.py.",
                },
            )

        access_token = result["body"].get("access_token")
        artifact = build_token_artifact(
            access_token,
            explanation="Emitido por WSO2 IS tras consentimiento y token exchange. En este token delegado el usuario debe verse en sub y el agente delegado en act.sub.",
            consumer="Agente para llamadas delegadas a la API de recursos",
            issuer_hint=self.settings.wso2_issuer,
        )
        artifact = await self._enrich_opaque_token_artifact(artifact)
        claims = artifact.get("claims", {})
        delegated_actor = extract_delegated_agent_id(claims)

        if self.settings.obo_require_act_claim and not delegated_actor:
            raise HTTPException(
                status_code=502,
                detail={
                    "message": "WSO2 emitted OBO_TOKEN without act.sub",
                    "oauth_response": result["body"],
                    "request_payload": result["request_payload"],
                    "token_subject": extract_subject(claims),
                    "token_actor": extract_actor(claims),
                    "note": "Configura WSO2 para emitir act.sub en el token delegado OBO. El backend no rellenara claims derivados.",
                },
            )

        session_store.set_obo_token(
            session_id,
            artifact=artifact,
            delegated_user_id=extract_subject(claims),
            delegated_agent_id=delegated_actor,
        )
        session_store.append_trace(
            session_id,
            {
                "action": "Intercambiar code por OBO_TOKEN",
                "endpoint": self.settings.wso2_token_endpoint,
                "method": "POST",
                "request_parameters": result["request_payload"],
                "response_status": result["status_code"],
                "response_body": result["body"],
                "functional_interpretation": "El backend canjeo el authorization_code junto con PKCE y el token del agente.",
                "security_interpretation": "Tras OBO, la trazabilidad correcta queda en el token delegado: sub identifica al usuario y act.sub identifica al agente que actua en su nombre.",
            },
        )
        return session_store.serialize_session(session_id, self.settings.debug_show_full_tokens)


obo_service = OBOService()
