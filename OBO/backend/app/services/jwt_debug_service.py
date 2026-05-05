from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import jwt


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def iso_from_epoch(epoch: int | float | None) -> str | None:
    if epoch is None:
        return None
    return datetime.fromtimestamp(epoch, tz=timezone.utc).isoformat()


def truncate_value(value: str | None, head: int = 20, tail: int = 12) -> str | None:
    if not value:
        return None
    if len(value) <= head + tail + 3:
        return value
    return f"{value[:head]}...{value[-tail:]}"


def extract_scopes(claims: dict[str, Any]) -> list[str]:
    scope_value = claims.get("scope") or claims.get("scp") or []
    if isinstance(scope_value, str):
        return [item for item in scope_value.split() if item]
    if isinstance(scope_value, list):
        return [str(item) for item in scope_value]
    return []


def extract_actor(claims: dict[str, Any]) -> str | None:
    actor = claims.get("act")
    if isinstance(actor, dict):
        return actor.get("sub") or actor.get("client_id") or str(actor)
    if isinstance(actor, str):
        return actor

    alternate = claims.get("actor") or claims.get("may_act")
    if isinstance(alternate, dict):
        return alternate.get("sub") or alternate.get("client_id") or str(alternate)
    if alternate is not None:
        return str(alternate)

    return None


def extract_subject(claims: dict[str, Any]) -> str | None:
    subject = claims.get("sub") or claims.get("username")
    if subject is None:
        return None
    return str(subject)


def extract_oauth_client_id(claims: dict[str, Any]) -> str | None:
    client_id = claims.get("client_id") or claims.get("azp") or claims.get("clientId")
    if client_id is None:
        return None
    return str(client_id)


def extract_token_authentication_type(claims: dict[str, Any]) -> str | None:
    auth_type = claims.get("aut") or claims.get("token_authentication_type")
    if auth_type is None:
        return None
    return str(auth_type)


def extract_delegated_agent_id(claims: dict[str, Any]) -> str | None:
    actor = claims.get("act")
    if isinstance(actor, dict) and actor.get("sub") is not None:
        return str(actor.get("sub"))
    return None


def decode_token(token: str | None) -> dict[str, Any]:
    if not token:
        return {}
    try:
        return jwt.decode(
            token,
            options={
                "verify_signature": False,
                "verify_aud": False,
                "verify_exp": False,
                "verify_iss": False,
            },
            algorithms=["RS256", "HS256", "ES256"],
        )
    except jwt.PyJWTError:
        return {}


def build_token_artifact(
    token: str | None,
    *,
    explanation: str,
    consumer: str,
    issuer_hint: str | None = None,
) -> dict[str, Any]:
    claims = decode_token(token)
    expires_at = iso_from_epoch(claims.get("exp"))
    is_expired = bool(claims.get("exp")) and datetime.fromtimestamp(
        int(claims["exp"]), tz=timezone.utc
    ) <= utcnow()
    return {
        "token": token,
        "claims": claims,
        "scopes": extract_scopes(claims),
        "expires_at": expires_at,
        "subject": extract_subject(claims),
        "actor": extract_actor(claims),
        "issuer": claims.get("iss") or issuer_hint,
        "audience": claims.get("aud"),
        "status": "expired" if is_expired else ("available" if token else "missing"),
        "explanation": explanation,
        "consumer": consumer,
        "issued_at": iso_from_epoch(claims.get("iat")),
    }


def serialize_secret(value: str | None, show_full: bool) -> dict[str, Any]:
    return {
        "available": bool(value),
        "preview": truncate_value(value),
        "raw": value if show_full else None,
    }


def serialize_token_artifact(artifact: dict[str, Any] | None, show_full: bool) -> dict[str, Any]:
    if not artifact:
        return {
            "status": "not-started",
            "available": False,
            "preview": None,
            "raw": None,
            "claims": {},
            "scopes": [],
            "subject": None,
            "actor": None,
            "issuer": None,
            "audience": None,
            "expires_at": None,
            "explanation": None,
            "consumer": None,
            "issued_at": None,
        }

    return {
        "status": artifact.get("status", "available"),
        "available": bool(artifact.get("token")),
        "preview": truncate_value(artifact.get("token")),
        "raw": artifact.get("token") if show_full else None,
        "claims": artifact.get("claims", {}),
        "scopes": artifact.get("scopes", []),
        "subject": artifact.get("subject"),
        "actor": artifact.get("actor"),
        "issuer": artifact.get("issuer"),
        "audience": artifact.get("audience"),
        "expires_at": artifact.get("expires_at"),
        "explanation": artifact.get("explanation"),
        "consumer": artifact.get("consumer"),
        "issued_at": artifact.get("issued_at"),
    }
