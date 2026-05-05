from __future__ import annotations

from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel

from app.security import bearer, enforce_user_resource, require_token, settings
from app.state import list_public_files, list_user_files, share_user_file, upload_user_file


class UploadRequest(BaseModel):
    file_name: str


class ShareRequest(BaseModel):
    target: str


app = FastAPI(title=settings.app_name, version="0.1.0")


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
    explanation = (
        "La API acepta el token porque existe contexto de usuario. Si ademas incluye act, queda demostrada la delegacion OBO."
    )
    return {
        "items": list_user_files(context.subject or "anonymous-user"),
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
    created = upload_user_file(context.subject or "anonymous-user", payload.file_name)
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
    try:
        shared = share_user_file(context.subject or "anonymous-user", file_id, payload.target)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="File not found") from exc
    explanation = "Compartir un fichero es una accion sensible del usuario; por eso la demo exige OBO_TOKEN y scope files.share."
    return {
        "item": shared,
        "token_analysis": context.analysis("allowed", explanation),
    }
