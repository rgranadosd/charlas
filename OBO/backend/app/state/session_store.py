from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from threading import Lock
from typing import Any

from app.services.jwt_debug_service import serialize_secret, serialize_token_artifact


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class SessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, dict[str, Any]] = {}
        self._state_index: dict[str, str] = {}
        self._lock = Lock()

    def _build_session(self, session_id: str) -> dict[str, Any]:
        timestamp = utcnow_iso()
        return {
            "session_id": session_id,
            "created_at": timestamp,
            "updated_at": timestamp,
            "user_token": None,
            "user_claims": {},
            "configured_agent_id": None,
            "oauth_client_id": None,
            "agent_token": None,
            "agent_token_claims": {},
            "agent_token_authentication_type": None,
            "agent_token_subject": None,
            "obo_authorization_url": None,
            "obo_state": None,
            "code_verifier": None,
            "code_challenge": None,
            "delegation_scopes": [],
            "authorization_code": None,
            "authorization_code_received_at": None,
            "obo_token": None,
            "obo_token_claims": {},
            "delegated_user_id": None,
            "delegated_agent_id": None,
            "last_api_request": None,
            "last_api_response": None,
            "last_security_explanation": None,
            "traces": [],
            "timestamps": {
                "user_token_received_at": None,
                "agent_token_received_at": None,
                "delegation_started_at": None,
                "obo_token_received_at": None,
            },
        }

    def _touch(self, session: dict[str, Any]) -> None:
        session["updated_at"] = utcnow_iso()

    def get_or_create(self, session_id: str) -> dict[str, Any]:
        with self._lock:
            if session_id not in self._sessions:
                self._sessions[session_id] = self._build_session(session_id)
            return deepcopy(self._sessions[session_id])

    def set_user_token(self, session_id: str, artifact: dict[str, Any]) -> None:
        with self._lock:
            session = self._sessions.setdefault(session_id, self._build_session(session_id))
            session["user_token"] = artifact
            session["user_claims"] = artifact.get("claims", {})
            session["timestamps"]["user_token_received_at"] = utcnow_iso()
            self._touch(session)

    def set_agent_token(
        self,
        session_id: str,
        *,
        artifact: dict[str, Any],
        configured_agent_id: str,
        oauth_client_id: str | None,
        token_subject: str | None,
        token_authentication_type: str | None,
    ) -> None:
        with self._lock:
            session = self._sessions.setdefault(session_id, self._build_session(session_id))
            session["configured_agent_id"] = configured_agent_id
            session["oauth_client_id"] = oauth_client_id
            session["agent_token"] = artifact
            session["agent_token_claims"] = artifact.get("claims", {})
            session["agent_token_authentication_type"] = token_authentication_type
            session["agent_token_subject"] = token_subject
            session["timestamps"]["agent_token_received_at"] = utcnow_iso()
            self._touch(session)

    def start_delegation(
        self,
        session_id: str,
        *,
        authorization_url: str,
        state: str,
        code_verifier: str,
        code_challenge: str,
        scopes: list[str],
    ) -> None:
        with self._lock:
            session = self._sessions.setdefault(session_id, self._build_session(session_id))
            session["obo_authorization_url"] = authorization_url
            session["obo_state"] = state
            session["code_verifier"] = code_verifier
            session["code_challenge"] = code_challenge
            session["delegation_scopes"] = scopes
            session["authorization_code"] = None
            session["authorization_code_received_at"] = None
            session["obo_token"] = None
            session["obo_token_claims"] = {}
            session["delegated_user_id"] = None
            session["delegated_agent_id"] = None
            session["timestamps"]["delegation_started_at"] = utcnow_iso()
            self._state_index[state] = session_id
            self._touch(session)

    def complete_callback(self, state: str, code: str) -> str | None:
        with self._lock:
            session_id = self._state_index.get(state)
            if not session_id:
                return None
            session = self._sessions[session_id]
            session["authorization_code"] = code
            session["authorization_code_received_at"] = utcnow_iso()
            self._touch(session)
            return session_id

    def set_obo_token(
        self,
        session_id: str,
        *,
        artifact: dict[str, Any],
        delegated_user_id: str | None,
        delegated_agent_id: str | None,
    ) -> None:
        with self._lock:
            session = self._sessions.setdefault(session_id, self._build_session(session_id))
            session["obo_token"] = artifact
            session["obo_token_claims"] = artifact.get("claims", {})
            session["delegated_user_id"] = delegated_user_id
            session["delegated_agent_id"] = delegated_agent_id
            session["timestamps"]["obo_token_received_at"] = utcnow_iso()
            self._touch(session)

    def append_trace(self, session_id: str, entry: dict[str, Any]) -> None:
        with self._lock:
            session = self._sessions.setdefault(session_id, self._build_session(session_id))
            trace = {"timestamp": utcnow_iso(), **entry}
            session["traces"].insert(0, trace)
            session["traces"] = session["traces"][:60]
            self._touch(session)

    def set_last_api_interaction(
        self,
        session_id: str,
        *,
        request_payload: dict[str, Any],
        response_payload: dict[str, Any],
        security_explanation: str,
    ) -> None:
        with self._lock:
            session = self._sessions.setdefault(session_id, self._build_session(session_id))
            session["last_api_request"] = request_payload
            session["last_api_response"] = response_payload
            session["last_security_explanation"] = security_explanation
            self._touch(session)

    def serialize_session(self, session_id: str, show_full_tokens: bool) -> dict[str, Any]:
        session = self.get_or_create(session_id)
        artifacts = {
            "user": serialize_token_artifact(session.get("user_token"), show_full_tokens),
            "agent": serialize_token_artifact(session.get("agent_token"), show_full_tokens),
            "delegation": {
                "status": "available" if session.get("obo_state") else "not-started",
                "authorization_url": {
                    "available": bool(session.get("obo_authorization_url")),
                    "preview": session.get("obo_authorization_url"),
                    "raw": session.get("obo_authorization_url"),
                },
                "state": {
                    "available": bool(session.get("obo_state")),
                    "preview": session.get("obo_state"),
                    "raw": session.get("obo_state"),
                },
                "code_verifier": serialize_secret(session.get("code_verifier"), show_full_tokens),
                "code_challenge": {
                    "available": bool(session.get("code_challenge")),
                    "preview": session.get("code_challenge"),
                    "raw": session.get("code_challenge"),
                },
                "scopes": session.get("delegation_scopes", []),
                "configured_agent_id": session.get("configured_agent_id"),
                "oauth_client_id": session.get("oauth_client_id"),
                "started_at": session.get("timestamps", {}).get("delegation_started_at"),
            },
            "authorization_code": {
                "status": "available" if session.get("authorization_code") else "waiting-callback",
                "value": serialize_secret(session.get("authorization_code"), show_full_tokens),
                "state_validated": bool(session.get("authorization_code")),
                "received_at": session.get("authorization_code_received_at"),
            },
            "obo": serialize_token_artifact(session.get("obo_token"), show_full_tokens),
        }

        comparison_rows = [
            {
                "artifact": "USER_TOKEN",
                "issuer": artifacts["user"].get("issuer"),
                "subject": artifacts["user"].get("subject"),
                "actor": artifacts["user"].get("actor"),
                "use": "Sesion del usuario en la SPA",
                "status": artifacts["user"].get("status"),
            },
            {
                "artifact": "AGENT_TOKEN",
                "issuer": artifacts["agent"].get("issuer"),
                "subject": session.get("oauth_client_id") or artifacts["agent"].get("subject"),
                "actor": session.get("configured_agent_id"),
                "use": "Cliente OAuth del agente autenticado en WSO2",
                "status": artifacts["agent"].get("status"),
            },
            {
                "artifact": "AUTHORIZATION_CODE",
                "issuer": "WSO2 IS",
                "subject": "flujo temporal",
                "actor": session.get("user_claims", {}).get("sub"),
                "use": "Insumo de token exchange",
                "status": artifacts["authorization_code"].get("status"),
            },
            {
                "artifact": "OBO_TOKEN",
                "issuer": artifacts["obo"].get("issuer"),
                "subject": session.get("delegated_user_id") or artifacts["obo"].get("subject"),
                "actor": session.get("delegated_agent_id") or artifacts["obo"].get("actor"),
                "use": "Agente actuando en nombre del usuario",
                "status": artifacts["obo"].get("status"),
            },
        ]

        return {
            "session_id": session_id,
            "created_at": session.get("created_at"),
            "updated_at": session.get("updated_at"),
            "configured_agent_id": session.get("configured_agent_id"),
            "oauth_client_id": session.get("oauth_client_id"),
            "agent_token_subject": session.get("agent_token_subject"),
            "agent_token_authentication_type": session.get("agent_token_authentication_type"),
            "delegated_user_id": session.get("delegated_user_id"),
            "delegated_agent_id": session.get("delegated_agent_id"),
            "artifacts": artifacts,
            "comparison_rows": comparison_rows,
            "last_api_request": session.get("last_api_request"),
            "last_api_response": session.get("last_api_response"),
            "last_security_explanation": session.get("last_security_explanation"),
            "traces": session.get("traces", []),
            "snapshot": {
                "user_token": serialize_secret(session.get("user_token", {}).get("token") if session.get("user_token") else None, show_full_tokens),
                "user_claims": session.get("user_claims", {}),
                "configured_agent_id": session.get("configured_agent_id"),
                "oauth_client_id": session.get("oauth_client_id"),
                "agent_token": serialize_secret(session.get("agent_token", {}).get("token") if session.get("agent_token") else None, show_full_tokens),
                "agent_token_claims": session.get("agent_token_claims", {}),
                "agent_token_authentication_type": session.get("agent_token_authentication_type"),
                "agent_token_subject": session.get("agent_token_subject"),
                "obo_authorization_url": serialize_secret(session.get("obo_authorization_url"), show_full_tokens),
                "obo_state": serialize_secret(session.get("obo_state"), show_full_tokens),
                "code_verifier": serialize_secret(session.get("code_verifier"), show_full_tokens),
                "code_challenge": serialize_secret(session.get("code_challenge"), show_full_tokens),
                "authorization_code": serialize_secret(session.get("authorization_code"), show_full_tokens),
                "obo_token": serialize_secret(session.get("obo_token", {}).get("token") if session.get("obo_token") else None, show_full_tokens),
                "obo_token_claims": session.get("obo_token_claims", {}),
                "delegated_user_id": session.get("delegated_user_id"),
                "delegated_agent_id": session.get("delegated_agent_id"),
                "last_api_request": session.get("last_api_request"),
                "last_api_response": session.get("last_api_response"),
                "last_security_explanation": session.get("last_security_explanation"),
                "timestamps": session.get("timestamps", {}),
            },
        }


session_store = SessionStore()
