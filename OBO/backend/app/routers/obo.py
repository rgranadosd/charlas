from __future__ import annotations

import html

from fastapi import APIRouter, Header, HTTPException, Query
from fastapi.responses import HTMLResponse

from app.config import get_settings
from app.services.obo_service import obo_service
from app.state.session_store import session_store

router = APIRouter(tags=["obo"])


def _require_session_id(session_id: str | None) -> str:
    if not session_id:
        raise HTTPException(status_code=400, detail="X-Demo-Session-Id header is required")
    return session_id


@router.post("/api/obo/start")
async def start_obo(x_demo_session_id: str | None = Header(default=None)) -> dict:
    session_id = _require_session_id(x_demo_session_id)
    return obo_service.start(session_id)


@router.get("/api/obo/callback", response_class=HTMLResponse)
async def obo_callback(code: str = Query(...), state: str = Query(...)) -> HTMLResponse:
    session_id = obo_service.complete_callback(state, code)
    safe_session_id = html.escape(session_id)
    safe_state = html.escape(state)
    return HTMLResponse(
        content=f"""
<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <title>OBO Callback Received</title>
    <style>
      body {{ font-family: ui-monospace, Menlo, monospace; background: #0d1117; color: #e6edf3; padding: 32px; }}
      code {{ color: #7ee787; }}
    </style>
  </head>
  <body>
    <h1>Authorization code received</h1>
    <p>Session: <code>{safe_session_id}</code></p>
    <p>State validated: <code>{safe_state}</code></p>
    <p>You can close this window and continue the exchange from the SPA.</p>
    <script>
      if (window.opener) {{
        window.opener.postMessage({{ type: "obo-callback-complete", sessionId: "{safe_session_id}" }}, "*");
        window.close();
      }}
    </script>
  </body>
</html>
"""
    )


@router.post("/api/obo/exchange")
async def exchange_obo(x_demo_session_id: str | None = Header(default=None)) -> dict:
    session_id = _require_session_id(x_demo_session_id)
    return await obo_service.exchange(session_id)
