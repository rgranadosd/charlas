from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException

from app.config import get_settings
from app.state.session_store import session_store

router = APIRouter(tags=["debug"])


@router.get("/api/debug/artifacts")
async def debug_artifacts(x_demo_session_id: str | None = Header(default=None)) -> dict:
    if not x_demo_session_id:
        raise HTTPException(status_code=400, detail="X-Demo-Session-Id header is required")
    settings = get_settings()
    return session_store.serialize_session(x_demo_session_id, settings.debug_show_full_tokens)
