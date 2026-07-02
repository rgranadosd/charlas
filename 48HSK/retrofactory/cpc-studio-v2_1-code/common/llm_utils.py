"""Shared LLM utility helpers — extracted from developer_agent.py.

Used by agents that need to resolve the AMP LLM gateway, parse LLM output,
or read environment variables.
"""
from __future__ import annotations

import json as _json
import re as _re
from pathlib import Path

from json_repair import repair_json

_REPO_ROOT_ENV = Path(__file__).parents[1] / ".env"

_AMP_BINDING_RE = _re.compile(r"^(?P<prefix>.+)_(?P<idx>\d+)_URL$")
_AMP_BINDING_PLAIN_RE = _re.compile(r"^(?P<prefix>.+)_URL$")


def _read_env() -> dict[str, str]:
    import os
    env: dict[str, str] = dict(os.environ)
    if _REPO_ROOT_ENV.exists():
        for line in _REPO_ROOT_ENV.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, _, v = line.partition("=")
                env.setdefault(k.strip(), v.strip())
    return env


def _resolve_amp_llm_gateway(env: dict[str, str]) -> dict | None:
    """Resolve the connection details for AMP's governed LLM gateway, or None.

    When an LLM provider is attached to the agent, AMP injects a pair of env
    vars ``<PREFIX>_<N>_URL`` + ``<PREFIX>_<N>_API_KEY`` (e.g.
    ``CPC_STUDIO_PM_1_URL`` / ``CPC_STUDIO_PM_1_API_KEY``). That URL is the
    *external* invoke URL (``http://…gateway.localhost:19080/<context>``) which
    does NOT resolve from inside the cluster, and the gateway routes by ``Host``
    header. So we keep the provider *context path*, swap the authority for the
    in-cluster gateway service (``AMP_LLM_GATEWAY_AUTHORITY``), append the
    OpenAI-compatible ``/v1`` suffix, and surface the original hostname as the
    ``Host`` header for the caller to send.

    Precedence: explicit ``AMP_LLM_URL`` + ``AMP_LLM_API_KEY`` win over the
    auto-detected binding, so a deploy can pin stable names if it prefers.
    """
    url = env.get("AMP_LLM_URL", "").strip()
    key = env.get("AMP_LLM_API_KEY", "").strip()

    if not url:
        # Accept both indexed ("<PREFIX>_<N>_URL") and plain ("<PREFIX>_URL")
        # bindings — AMP names them differently depending on the provider setup
        # (e.g. CPC_STUDIO_PM_1_URL vs GEMINI_URL / MISTRALAI_URL).
        for regexp, sibling_fmt in (
            (_AMP_BINDING_RE, "{prefix}_{idx}_API_KEY"),
            (_AMP_BINDING_PLAIN_RE, "{prefix}_API_KEY"),
        ):
            for name, value in env.items():
                match = regexp.match(name)
                if not match or not value.strip().startswith("http"):
                    continue
                sibling = sibling_fmt.format(**match.groupdict())
                if sibling == name:            # don't pair a var with itself
                    continue
                if env.get(sibling, "").strip():
                    url = value.strip()
                    key = env[sibling].strip()
                    break
            if url:
                break

    if not url or not key:
        return None

    from urllib.parse import urlsplit

    parts = urlsplit(url)
    host_header = parts.hostname or ""
    context = parts.path.rstrip("/")
    authority = env.get(
        "AMP_LLM_GATEWAY_AUTHORITY", "gateway-default.openchoreo-data-plane:19080"
    ).strip()
    scheme = env.get("AMP_LLM_GATEWAY_SCHEME", "http").strip() or "http"

    # OpenAI-compatible path suffix. Most providers live under "/v1"; Google
    # Gemini's OpenAI surface is under "/v1beta/openai". The gateway forwards
    # everything after the context path verbatim, so this decides the upstream
    # path. Override with AMP_LLM_OPENAI_PATH.
    suffix = env.get("AMP_LLM_OPENAI_PATH", "").strip()
    if not suffix:
        model_hint = " ".join(
            env.get(k, "") for k in (
                "ORCHESTRATOR_MODEL", "DEVELOPER_MODEL", "AUDIO_MODEL",
                "QA_MODEL", "AMP_GENAI_MODEL",
            )
        ).lower()
        suffix = "/v1beta/openai" if "gemini" in model_hint else "/v1"

    base_url = f"{scheme}://{authority}{context}".rstrip("/")
    if not base_url.endswith(suffix):
        base_url = f"{base_url}{suffix}"

    return {"base_url": base_url, "api_key": key, "host": host_header}


def build_amp_gateway_chat(gateway: dict, *, model: str, env: dict[str, str],
                           temperature: float = 0, timeout: int = 240,
                           max_retries: int = 0):
    """Build a ChatOpenAI client for AMP's governed LLM gateway.

    AMP authenticates the *consumer* (agent -> gateway) via the subscription key
    in a dedicated header (default "X-API-Key"). The OpenAI SDK always injects
    "Authorization: Bearer <api_key>", which must NOT reach the provider: the
    gateway's endpoint-security owns the upstream Authorization (e.g. Bearer
    <provider key>). So we carry the subscription key in the consumer header and
    strip Authorization on the way out with an httpx request hook.
    """
    import httpx
    from langchain_openai import ChatOpenAI

    consumer_header = env.get("AMP_LLM_CONSUMER_HEADER", "X-API-Key").strip() or "X-API-Key"

    def _drop_authorization(request: "httpx.Request") -> None:
        request.headers.pop("authorization", None)

    async def _adrop_authorization(request: "httpx.Request") -> None:
        request.headers.pop("authorization", None)

    return ChatOpenAI(
        model=model, temperature=temperature,
        openai_api_base=gateway["base_url"],
        openai_api_key="amp-managed",   # placeholder; stripped before send
        default_headers={
            consumer_header: gateway["api_key"],
            "API-Key": gateway["api_key"],   # legacy fallback for older bindings
            "Host": gateway["host"],
        },
        http_client=httpx.Client(timeout=timeout, event_hooks={"request": [_drop_authorization]}),
        http_async_client=httpx.AsyncClient(timeout=timeout, event_hooks={"request": [_adrop_authorization]}),
        timeout=timeout,
        max_retries=max_retries,
    )


def _parse_output(text: str) -> dict:
    """Parse the LLM text response to a dict.

    LLM output often has unescaped double-quotes inside C code content strings
    (e.g. inside comments like  // buffer for "SCORE: 99" ).
    json_repair handles this case without an extra LLM round-trip.
    """
    try:
        return _json.loads(text)
    except _json.JSONDecodeError:
        pass
    # Strip markdown fences if present
    stripped = _re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=_re.MULTILINE)
    stripped = _re.sub(r"\s*```$", "", stripped.strip(), flags=_re.MULTILINE)
    try:
        return _json.loads(stripped)
    except _json.JSONDecodeError:
        pass
    # json_repair handles unescaped quotes and trailing commas — keeps LLM output
    repaired = repair_json(stripped, return_objects=True)
    if isinstance(repaired, dict):
        return repaired
    raise ValueError(f"Could not parse LLM output as JSON:\n{text[:300]}")


def _env_int(env: dict[str, str], key: str, default: int) -> int:
    value = env.get(key, "").strip()
    if not value:
        return default
    try:
        parsed = int(value)
    except ValueError:
        return default
    return parsed if parsed > 0 else default


def _env_retry_delays(env: dict[str, str], key: str, default: list[int]) -> list[int]:
    raw = env.get(key, "").strip()
    if not raw:
        return default
    values: list[int] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            delay = int(part)
        except ValueError:
            continue
        if delay > 0:
            values.append(delay)
    return values or default


def _normalize_development_output(raw: dict, task_id: str) -> dict:
    """Repair common LLM schema drift before Pydantic validation."""
    from typing import Any
    if not isinstance(raw, dict):
        return {
            "task_id": task_id,
            "status": "blocked",
            "summary": "LLM devolvio una respuesta no estructurada o no parseable.",
            "files_to_write": [],
            "notes": [],
            "risks": ["Respuesta del modelo fuera del esquema esperado"],
            "follow_up_questions": [],
        }

    normalized: dict = dict(raw)
    normalized["task_id"] = str(normalized.get("task_id") or task_id)
    normalized["status"] = normalized.get("status") or "blocked"
    normalized["summary"] = str(normalized.get("summary") or "LLM response normalized before validation.")
    normalized["notes"] = normalized.get("notes") or []
    normalized["risks"] = normalized.get("risks") or []
    normalized["follow_up_questions"] = normalized.get("follow_up_questions") or []

    raw_patches = normalized.get("files_to_write")
    if not isinstance(raw_patches, list):
        raw_patches = []

    cleaned_patches: list[dict] = []
    discarded = 0
    defaulted_mode = 0
    for item in raw_patches:
        if not isinstance(item, dict):
            discarded += 1
            continue

        path = str(item.get("path") or "").strip()
        content = item.get("content")
        mode = str(item.get("mode") or "").strip().lower()

        if not mode or mode not in {"write", "append", "patch"}:
            mode = "write"
            defaulted_mode += 1

        if not path or not isinstance(content, str) or not content.strip():
            discarded += 1
            continue

        cleaned_patches.append({
            "path": path,
            "content": content,
            "mode": mode,
        })

    normalized["files_to_write"] = cleaned_patches

    if defaulted_mode:
        normalized["notes"] = list(normalized["notes"])
        normalized["notes"].append(
            f"Normalizado files_to_write.mode por defecto a 'write' en {defaulted_mode} item(s)."
        )

    if discarded:
        normalized["risks"] = list(normalized["risks"])
        normalized["risks"].append(
            f"Se descartaron {discarded} patch(es) incompletos antes de validar la salida."
        )

    if normalized["status"] == "done" and not cleaned_patches:
        normalized["status"] = "needs_clarification"
        normalized["summary"] = (
            "LLM devolvio status=done pero sin archivos validos; se degrada a needs_clarification."
        )
        normalized["follow_up_questions"] = list(normalized["follow_up_questions"])
        normalized["follow_up_questions"].append(
            "Devuelve al menos un files_to_write valido con path, content y mode explicito."
        )

    return normalized
