from __future__ import annotations

from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel

from app.config import settings
from app.demo_files_repository import DemoFilesUnavailableError
from app.security import bearer, enforce_user_resource, require_token
from app.state import demo_files_debug_state, list_public_files, list_user_files, share_user_file, upload_user_file


class UploadRequest(BaseModel):
    file_name: str


class ShareRequest(BaseModel):
    target: str


app = FastAPI(title=settings.app_name, version="0.1.0")


def _require_user_subject(context: Any) -> str:
    if context.subject:
        return context.subject
    raise HTTPException(
        status_code=403,
        detail={
            "message": "User subject required",
            "reason": "The token is valid but does not carry a user subject suitable for /files/me ownership.",
        },
    )


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "issuer": settings.wso2_issuer,
        "jwks": settings.wso2_jwks_endpoint,
        "introspection": settings.wso2_introspection_endpoint,
    }


@app.get("/files/public")
async def public_files(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> dict[str, Any]:
    token_analysis = None
    if credentials is not None:
        context = require_token(credentials)
        token_analysis = context.analysis(
            authorization_result="allowed",
            security_explanation="El recurso publico puede mostrarse con o sin token; si viene un token, la API igualmente lo inspecciona.",
        )

    return {
        "items": list_public_files(),
        "token_analysis": token_analysis,
    }


@app.get("/files/me")
async def my_files(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)) -> dict[str, Any]:
    context = enforce_user_resource(require_token(credentials))
    subject = _require_user_subject(context)
    explanation = (
        "La API acepta el token porque existe un sub de usuario. El ownership de /files/me se resuelve solo con ese sub; si ademas existe act, queda demostrada la delegacion OBO."
    )
    return {
        "items": list_user_files(subject),
        "token_analysis": context.analysis("allowed", explanation),
    }


@app.post("/files/upload")
async def upload_file(
    payload: UploadRequest,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> dict[str, Any]:
    context = enforce_user_resource(
        require_token(credentials),
        required_scopes=["files.write"],
        delegated_only=True,
    )
    subject = _require_user_subject(context)
    try:
        created = upload_user_file(subject, payload.file_name)
    except DemoFilesUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    explanation = "La carga exige scope files.write y delegacion explicita; un AGENT_TOKEN aislado no basta."
    return {
        "item": created,
        "token_analysis": context.analysis("allowed", explanation),
    }


@app.post("/files/{file_id}/share")
async def share_file(
    file_id: str,
    payload: ShareRequest,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> dict[str, Any]:
    context = enforce_user_resource(
        require_token(credentials),
        required_scopes=["files.share"],
        delegated_only=True,
    )
    subject = _require_user_subject(context)
    try:
        shared = share_user_file(subject, file_id, payload.target)
    except DemoFilesUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="File not found") from exc
    explanation = "Compartir un fichero es una accion sensible del usuario; por eso la demo exige OBO_TOKEN y scope files.share."
    return {
        "item": shared,
        "token_analysis": context.analysis("allowed", explanation),
    }


if settings.is_local_or_dev:

    @app.get("/debug/demo-files")
    async def debug_demo_files() -> dict[str, Any]:
        return demo_files_debug_state()
