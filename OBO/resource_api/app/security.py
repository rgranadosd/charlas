from __future__ import annotations

import os
from base64 import b64encode
from dataclasses import dataclass
from typing import Any

import httpx
import jwt
from jwt import PyJWK
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


def _extract_scopes(claims: dict[str, Any]) -> list[str]:
    scope = claims.get("scope") or claims.get("scp") or []
    if isinstance(scope, str):
        return [item for item in scope.split() if item]
    if isinstance(scope, list):
        return [str(item) for item in scope]
    return []


def _extract_actor(claims: dict[str, Any]) -> str | None:
    actor = claims.get("act")
    if isinstance(actor, dict):
        return actor.get("sub") or actor.get("client_id") or str(actor)
    if isinstance(actor, str):
        return actor
    return None


def _extract_subject(claims: dict[str, Any]) -> str | None:
    subject = claims.get("sub") or claims.get("username") or claims.get("preferred_username") or claims.get("email")
    if subject is None:
        return None
    return str(subject)


def _extract_token_authentication_type(claims: dict[str, Any]) -> str | None:
    auth_type = claims.get("aut") or claims.get("token_authentication_type")
    if auth_type is None:
        return None
    return str(auth_type)


def _truncate(token: str) -> str:
    if len(token) <= 32:
        return token
    return f"{token[:20]}...{token[-12:]}"


class SecuritySettings:
    def __init__(self) -> None:
        self.app_name = os.getenv("APP_NAME", "WSO2 OBO Resource API")
        self.resource_api_host = os.getenv("RESOURCE_API_HOST", "0.0.0.0")
        self.resource_api_port = int(os.getenv("RESOURCE_API_PORT", "8001"))
        self.wso2_issuer = os.getenv("WSO2_ISSUER", "https://localhost:9443/oauth2/token")
        self.wso2_jwks_endpoint = os.getenv("WSO2_JWKS_ENDPOINT", "https://localhost:9443/oauth2/jwks")
        self.wso2_introspection_endpoint = os.getenv(
            "WSO2_INTROSPECTION_ENDPOINT", "https://localhost:9443/oauth2/introspect"
        )
        self.introspection_client_id = os.getenv("INTROSPECTION_CLIENT_ID", "admin")
        self.introspection_client_secret = os.getenv("INTROSPECTION_CLIENT_SECRET", "admin")
        self.expected_audience = os.getenv("EXPECTED_AUDIENCE", "")


settings = SecuritySettings()
bearer = HTTPBearer(auto_error=False)


@dataclass
class TokenContext:
    raw_token: str
    claims: dict[str, Any]
    scopes: list[str]
    subject: str | None
    actor: str | None
    oauth_client_id: str | None
    token_authentication_type: str | None
    token_format: str
    is_obo: bool
    is_machine_token: bool

    def analysis(self, authorization_result: str, security_explanation: str) -> dict[str, Any]:
        return {
            "subject": self.subject,
            "actor": self.actor,
            "oauth_client_id": self.oauth_client_id,
            "token_authentication_type": self.token_authentication_type,
            "token_format": self.token_format,
            "scopes": self.scopes,
            "is_obo": self.is_obo,
            "is_machine_token": self.is_machine_token,
            "authorization_result": authorization_result,
            "issuer": self.claims.get("iss"),
            "audience": self.claims.get("aud"),
            "expires_at": self.claims.get("exp"),
            "token_preview": _truncate(self.raw_token),
            "security_explanation": security_explanation,
        }


def _introspect_token(token: str) -> dict[str, Any]:
    basic_auth = b64encode(
        f"{settings.introspection_client_id}:{settings.introspection_client_secret}".encode("utf-8")
    ).decode("ascii")
    headers = {
        "Authorization": f"Basic {basic_auth}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    with httpx.Client(verify=False, timeout=15.0) as client:
        response = client.post(settings.wso2_introspection_endpoint, data={"token": token}, headers=headers)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict) or not payload.get("active"):
        raise HTTPException(status_code=401, detail="Bearer token rejected: inactive introspection response")
    return payload


def _decode_jwt(token: str) -> tuple[dict[str, Any], str]:
    try:
        header = jwt.get_unverified_header(token)
    except jwt.PyJWTError as exc:
        raise exc

    key_id = header.get("kid")
    if not key_id:
        raise jwt.PyJWTError("JWT header does not contain kid")

    with httpx.Client(verify=False, timeout=15.0) as client:
        jwks_response = client.get(settings.wso2_jwks_endpoint)
    jwks_response.raise_for_status()
    jwks = jwks_response.json()
    keys = jwks.get("keys", []) if isinstance(jwks, dict) else []
    signing_key = None
    for candidate in keys:
        if isinstance(candidate, dict) and candidate.get("kid") == key_id:
            signing_key = PyJWK.from_dict(candidate).key
            break
    if signing_key is None:
        raise jwt.PyJWTError("Unable to find signing key for JWT")

    kwargs: dict[str, Any] = {
        "algorithms": ["RS256", "PS256", "ES256"],
        "issuer": settings.wso2_issuer,
        "options": {"verify_aud": bool(settings.expected_audience)},
    }
    if settings.expected_audience:
        kwargs["audience"] = settings.expected_audience
    claims = jwt.decode(token, signing_key, **kwargs)
    return claims, "jwt"


def authenticate(credentials: HTTPAuthorizationCredentials | None) -> TokenContext:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token required")

    token = credentials.credentials
    try:
        claims, token_format = _decode_jwt(token)
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(status_code=401, detail="Bearer token expired") from exc
    except jwt.PyJWTError as exc:
        try:
            claims = _introspect_token(token)
            token_format = "opaque"
        except httpx.HTTPStatusError as http_exc:
            raise HTTPException(status_code=401, detail="Bearer token rejected by introspection") from http_exc
        except HTTPException:
            raise
        except Exception as introspection_exc:
            raise HTTPException(status_code=401, detail=f"Bearer token rejected: {exc}") from introspection_exc

    scopes = _extract_scopes(claims)
    actor = _extract_actor(claims)
    token_authentication_type = _extract_token_authentication_type(claims)
    subject = _extract_subject(claims)
    human_subject = subject is not None and token_authentication_type != "APPLICATION"
    is_obo = actor is not None or token_authentication_type == "APPLICATION_USER"
    is_machine_token = not human_subject and not is_obo
    return TokenContext(
        raw_token=token,
        claims=claims,
        scopes=scopes,
        subject=subject,
        actor=actor,
        oauth_client_id=claims.get("client_id"),
        token_authentication_type=token_authentication_type,
        token_format=token_format,
        is_obo=is_obo,
        is_machine_token=is_machine_token,
    )


def require_token(credentials: HTTPAuthorizationCredentials | None) -> TokenContext:
    return authenticate(credentials)


def enforce_user_resource(
    context: TokenContext,
    *,
    required_scopes: list[str] | None = None,
    delegated_only: bool = False,
) -> TokenContext:
    missing_scopes = [scope for scope in required_scopes or [] if scope not in context.scopes]
    if missing_scopes:
        raise HTTPException(
            status_code=403,
            detail={
                "message": "Missing required scopes",
                "required_scopes": required_scopes,
                "granted_scopes": context.scopes,
            },
        )

    if context.is_machine_token:
        raise HTTPException(
            status_code=403,
            detail={
                "message": "Agent token alone has no user resource context",
                "reason": "The token authenticates the agent, but the resource belongs to a user.",
            },
        )

    if delegated_only and not context.is_obo:
        raise HTTPException(
            status_code=403,
            detail={
                "message": "Delegated user context required",
                "reason": "This operation is reserved for OBO tokens carrying user delegation.",
            },
        )

    return context
