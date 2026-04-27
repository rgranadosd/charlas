"""Authentication facade for shared use between CLI and service modes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Set

from oauth_session import OAuthCallbackHandler, OAuthClient, TokenStore


@dataclass
class SessionInfo:
    access_token: Optional[str]
    scopes: Optional[str]
    user_permissions: Set[str]


def ensure_user_session(force_auth: bool = False) -> OAuthClient:
    return OAuthClient(force_auth=force_auth)


def get_access_token(force_auth: bool = False) -> Optional[str]:
    client = ensure_user_session(force_auth=force_auth)
    return client.ensure_token()


def get_session_info(force_auth: bool = False) -> SessionInfo:
    token = get_access_token(force_auth=force_auth)
    scopes = getattr(OAuthCallbackHandler, "scopes", None)
    permissions = set(getattr(OAuthCallbackHandler, "user_permissions", set()) or set())
    return SessionInfo(access_token=token, scopes=scopes, user_permissions=permissions)


__all__ = [
    "TokenStore",
    "OAuthCallbackHandler",
    "OAuthClient",
    "SessionInfo",
    "ensure_user_session",
    "get_access_token",
    "get_session_info",
]
