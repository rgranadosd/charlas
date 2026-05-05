from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class UserTokenRequest(BaseModel):
    access_token: str = Field(..., description="Access token obtained by the SPA via @asgardeo/auth-react")
    user_profile: dict[str, Any] | None = None


class ProtectedAccessRequest(BaseModel):
    resource_path: str = "/files/me"
    method: str = "GET"
    payload: dict[str, Any] | None = None
