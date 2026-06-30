"""Audio Worker Agent — specialised for CPCtelera AY-3-8912 sound generation.

Produces compilable C audio code without requiring external .aks Arkos assets.
Default backend: direct AY register writes (beep backend).
Future backend: Arkos Tracker (swap implementation when .aks files are available).

Worker contract (same as developer_agent):
  Input : DevelopmentInput
  Output: DevelopmentOutput (files_to_write with audio functions added to src/main.c)
"""
from __future__ import annotations

import logging
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from json_repair import repair_json
import json as _json
import re as _re
import time as _time

from common.contracts import DevelopmentInput, DevelopmentOutput
from common.rag_store import RagStore

_audio_rag_instance = None

def _get_audio_rag() -> RagStore:
    global _audio_rag_instance
    if _audio_rag_instance is None:
        _audio_rag_instance = RagStore.load_or_build_audio()
        logger.info("Audio RAG store ready: %d chunks", _audio_rag_instance.chunk_count)
    return _audio_rag_instance

logger = logging.getLogger(__name__)

_G   = "\033[32m"
_Y   = "\033[33m"
_R   = "\033[31m"
_B   = "\033[36m"
_W   = "\033[1m"
_DIM = "\033[2m"
_RS  = "\033[0m"

_REPO_ROOT_ENV = Path(__file__).parents[2] / ".env"

# ---------------------------------------------------------------------------
# Prompt — loaded from prompts/
# ---------------------------------------------------------------------------

_PROMPTS_DIR = Path(__file__).parent / "prompts"
AUDIO_SYSTEM_PROMPT = (_PROMPTS_DIR / "audio_system_prompt.md").read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Build audio LLM chain
# ---------------------------------------------------------------------------

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
    """Resolve AMP's governed LLM gateway from the binding env vars, or None.

    AMP injects ``<PREFIX>_<N>_URL`` + ``<PREFIX>_<N>_API_KEY`` when an LLM
    provider is attached. That URL is external; we keep its context path, swap
    the authority for the in-cluster gateway service, append ``/v1`` and
    surface the original hostname as the ``Host`` header for routing.
    Explicit ``AMP_LLM_URL`` + ``AMP_LLM_API_KEY`` win over auto-detection.
    """
    import re
    from urllib.parse import urlsplit

    binding_re = re.compile(r"^(?P<prefix>.+)_(?P<idx>\d+)_URL$")
    url = env.get("AMP_LLM_URL", "").strip()
    key = env.get("AMP_LLM_API_KEY", "").strip()
    if not url:
        for name, value in env.items():
            match = binding_re.match(name)
            if not match or not value.strip().startswith("http"):
                continue
            sibling = f"{match.group('prefix')}_{match.group('idx')}_API_KEY"
            if env.get(sibling, "").strip():
                url, key = value.strip(), env[sibling].strip()
                break
    if not url or not key:
        return None

    parts = urlsplit(url)
    authority = env.get("AMP_LLM_GATEWAY_AUTHORITY", "gateway-default.openchoreo-data-plane:19080").strip()
    scheme = env.get("AMP_LLM_GATEWAY_SCHEME", "http").strip() or "http"
    base_url = f"{scheme}://{authority}{parts.path.rstrip('/')}".rstrip("/")
    if not base_url.endswith("/v1"):
        base_url = f"{base_url}/v1"
    return {"base_url": base_url, "api_key": key, "host": parts.hostname or ""}


def _audio_model(env: dict[str, str]) -> str:
    """Model for the audio worker. Set ``AUDIO_MODEL`` in the agent's env vars;
    falls back to ``AMP_GENAI_MODEL`` and finally a sensible default."""
    model = env.get("AUDIO_MODEL", "").strip() or env.get("AMP_GENAI_MODEL", "").strip() or "codestral-latest"
    if "/" in model:
        model = model.split("/", 1)[1]
    return model


def _parse_output(text: str) -> dict:
    try:
        return _json.loads(text)
    except _json.JSONDecodeError:
        pass
    stripped = _re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=_re.MULTILINE)
    stripped = _re.sub(r"\s*```$", "", stripped.strip(), flags=_re.MULTILINE)
    try:
        return _json.loads(stripped)
    except _json.JSONDecodeError:
        pass
    repaired = repair_json(stripped, return_objects=True)
    if isinstance(repaired, dict):
        return repaired
    raise ValueError(f"Could not parse audio agent output:\n{text[:300]}")


def build_audio_agent(settings) -> tuple:
    env = _read_env()
    model = _audio_model(env)
    timeout = int(env.get("AUDIO_TIMEOUT_SECONDS", "180"))

    # 1. AMP governed LLM gateway — normal path when a provider is attached.
    gateway = _resolve_amp_llm_gateway(env)
    if gateway:
        llm = ChatOpenAI(
            model=model, temperature=0,
            openai_api_base=gateway["base_url"],
            openai_api_key=gateway["api_key"],
            default_headers={"API-Key": gateway["api_key"], "Host": gateway["host"]},
            timeout=timeout,
            max_retries=0,
        )
        label = f"AUDIO/AMP-GATEWAY/{model}"
        logger.info("[AUDIO] LLM: AMP gateway — %s (timeout=%ds)", model, timeout)
    # 2. Mistral direct API — local-dev fallback.
    elif env.get("MISTRAL_WORKER_API_KEY") or env.get("MISTRAL_API_KEY", ""):
        mistral_key = env.get("MISTRAL_WORKER_API_KEY") or env.get("MISTRAL_API_KEY", "")
        mistral_url = env.get("MISTRAL_BASE_URL", "https://api.mistral.ai/v1")
        llm = ChatOpenAI(
            model=model, temperature=0,
            openai_api_base=mistral_url,
            openai_api_key=mistral_key,
            default_headers={"API-Key": mistral_key},
            timeout=timeout,
            max_retries=0,
        )
        label = f"AUDIO/MISTRAL/{model}"
        logger.info("[AUDIO] LLM: Mistral direct — %s (timeout=%ds)", model, timeout)
    else:
        raise RuntimeError(
            "No audio LLM configured. Attach an LLM provider in Agent Manager "
            "(or set AMP_LLM_URL/AMP_LLM_API_KEY), or set MISTRAL_API_KEY for local dev."
        )

    # Audio agent uses src/audio.c and src/audio.h — never src/main.c
    audio_schema = (
        "\nReturn ONLY valid JSON (no markdown):\n"
        '{{ "task_id": "string", "status": "done|blocked|needs_clarification", '
        '"summary": "string", "files_to_write": ['
        '{{"path": "src/audio.h", "content": "#ifndef AUDIO_H\\n#define AUDIO_H\\n...\\n#endif", "mode": "write"}}, '
        '{{"path": "src/audio.c", "content": "#include \\"audio.h\\"\\n...implementation...", "mode": "write"}}], '
        '"notes": [], "risks": [], "follow_up_questions": [] }}'
        "\nfiles_to_write MUST use path=src/audio.h and path=src/audio.c. NEVER path=src/main.c."
    )

    sys_esc = AUDIO_SYSTEM_PROMPT.replace("{", "{{").replace("}", "}}")
    prompt = ChatPromptTemplate.from_messages([
        ("system", sys_esc + audio_schema),
        ("user", "=== Audio/AY knowledge ===\n{rag_context}\n\n"
                 "TASK:\n{task_json}\n\n"
                 "PROJECT CONTEXT:\n{project_context}"),
    ])

    chain = prompt | llm | StrOutputParser() | _parse_output
    return chain, label


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def run_audio_task(task: DevelopmentInput, settings) -> DevelopmentOutput:
    """Execute one audio task and return a validated DevelopmentOutput."""
    from common.llm_utils import _normalize_development_output

    print(f"\n{_B}{_W}╔══ AUDIO WORKER [{task.task_id}] ═══════════════════════════╗{_RS}")
    print(f"{_B}{_W}║  tarea  : {task.goal[:65]}{_RS}")
    print(f"{_B}{_W}╚══════════════════════════════════════════════════════════════╝{_RS}")

    # RAG retrieval — audio-specific RAG (data/audio/ only)
    rag_context = ""
    try:
        rag = _get_audio_rag()
        query = f"CPCtelera AY-3-8912 audio SFX beep {task.goal[:60]}"
        chunks = rag.retrieve(query, top_k=3)
        print(f"{_DIM}         query (audio): {query[:80]}{_RS}")
        for i, c in enumerate(chunks, 1):
            print(f"{_DIM}         [{i}] {c.source}{_RS}")
        rag_context = "\n".join(f"[{i}] {c.source}:\n{c.text[:200]}" for i, c in enumerate(chunks, 1))
    except Exception as exc:
        print(f"{_Y}  [RAG] no disponible ({exc.__class__.__name__}) — continuando sin contexto{_RS}")

    project_context = (
        f"project: {task.project_name}\n"
        f"target_files: {task.target_files}\n"
        f"constraints:\n" + "\n".join(f"  - {c}" for c in task.constraints)
    )

    chain, label = build_audio_agent(settings)
    print(f"{_Y}  [2/3] [{label}]  generando código audio …{_RS}")

    invoke_input = {
        "task_json":       task.model_dump_json(indent=2),
        "project_context": project_context,
        "rag_context":     rag_context,
    }

    usage_data: dict[str, int] = {}

    try:
        try:
            from langchain_core.callbacks.base import BaseCallbackHandler

            class _UsageCapture(BaseCallbackHandler):
                def __init__(self):
                    self.usage: dict[str, int] = {}
                def on_llm_end(self, response, **kwargs):
                    try:
                        for gen_list in response.generations:
                            for gen in gen_list:
                                meta = getattr(getattr(gen, "message", None), "usage_metadata", None) or {}
                                if meta:
                                    self.usage = {
                                        "input_tokens": int(meta.get("input_tokens") or 0),
                                        "output_tokens": int(meta.get("output_tokens") or 0),
                                        "total_tokens": int(meta.get("total_tokens") or 0),
                                    }
                    except Exception:
                        pass

            cb = _UsageCapture()
            raw = chain.invoke(invoke_input, config={"callbacks": [cb]})
            if cb.usage:
                usage_data = cb.usage
        except Exception:
            raw = chain.invoke(invoke_input)
        normalized = _normalize_development_output(raw, task.task_id)
        output = DevelopmentOutput.model_validate(normalized)
    except Exception as exc:
        print(f"{_R}  ✗ [{label}] falló: {exc}{_RS}")
        output = DevelopmentOutput(
            task_id=task.task_id,
            status="blocked",
            summary=f"Audio agent error: {exc}",
            files_to_write=[],
            risks=[str(exc)],
        )

    if usage_data:
        output = output.model_copy(update={
            "input_tokens": usage_data.get("input_tokens"),
            "output_tokens": usage_data.get("output_tokens"),
            "total_tokens": usage_data.get("total_tokens"),
        })

    status_col = _G if output.status == "done" else _Y
    print(f"\n{status_col}{_W}  [3/3] [{label}]  [{task.task_id}] → {output.status}{_RS}")
    print(f"{_DIM}         {output.summary[:90]}{_RS}")
    for fp in output.files_to_write:
        lines = fp.content.count("\n") + 1
        print(f"         {_B}✎ {fp.path}{_RS}  ({fp.mode}, {lines} líneas)")

    return output
