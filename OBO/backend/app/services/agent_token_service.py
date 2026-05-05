from __future__ import annotations

from typing import Any

from fastapi import HTTPException

from app.config import get_settings
from app.services.jwt_debug_service import (
    build_token_artifact,
    extract_actor,
    extract_oauth_client_id,
    extract_scopes,
    extract_subject,
    extract_token_authentication_type,
    iso_from_epoch,
    utcnow,
)
from app.services.oauth_service import oauth_service
from app.state.session_store import session_store


class AgentTokenService:
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

    async def fetch_and_store(self, session_id: str) -> dict[str, Any]:
        if not self.settings.agent_client_id or not self.settings.agent_client_secret:
            raise HTTPException(status_code=400, detail="Agent client credentials are not configured")

        result = await oauth_service.request_client_credentials_token(
            client_id=self.settings.agent_client_id,
            client_secret=self.settings.agent_client_secret,
            scope=self.settings.agent_scope,
        )
        if result["status_code"] >= 400:
            raise HTTPException(
                status_code=result["status_code"],
                detail={
                    "message": "WSO2 IS rejected the agent token request",
                    "oauth_response": result["body"],
                },
            )

        access_token = result["body"].get("access_token")
        artifact = build_token_artifact(
            access_token,
            explanation="Emitido por WSO2 IS para autenticar al cliente OAuth asociado al agente. El agent_id logico proviene del registro/configuracion del agente y no debe inferirse desde sub ni client_id.",
            consumer="Backend OBO coordinator y llamadas autonomas del agente",
            issuer_hint=self.settings.wso2_issuer,
        )
        artifact = await self._enrich_opaque_token_artifact(artifact)
        claims = artifact.get("claims", {})
        oauth_client_id = extract_oauth_client_id(claims) or self.settings.agent_client_id or None
        token_sub = extract_subject(claims)
        token_authentication_type = extract_token_authentication_type(claims) or "APPLICATION"
        session_store.set_agent_token(
            session_id,
            artifact=artifact,
            configured_agent_id=self.settings.agent_id,
            oauth_client_id=oauth_client_id,
            token_sub=token_sub,
            token_authentication_type=token_authentication_type,
        )
        session_store.append_trace(
            session_id,
            {
                "action": "Obtener AGENT_TOKEN",
                "endpoint": self.settings.wso2_token_endpoint,
                "method": "POST",
                "request_parameters": {
                    "grant_type": "client_credentials",
                    "scope": self.settings.agent_scope,
                    "client_id": self.settings.agent_client_id,
                },
                "response_status": result["status_code"],
                "response_body": result["body"],
                "functional_interpretation": "El backend obtuvo un token propio del agente usando client credentials.",
                "security_interpretation": "Este token autentica al cliente OAuth del agente en WSO2. El agent_id logico sigue viniendo de AGENT_ID y no debe inferirse desde sub ni client_id del token.",
            },
        )
        return session_store.serialize_session(session_id, self.settings.debug_show_full_tokens)


agent_token_service = AgentTokenService()
