from __future__ import annotations

from fastapi import APIRouter

from app.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/api/health")
async def health() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "issuer": settings.wso2_issuer,
        "token_endpoint": settings.wso2_token_endpoint,
        "jwks_endpoint": settings.wso2_jwks_endpoint,
    }
