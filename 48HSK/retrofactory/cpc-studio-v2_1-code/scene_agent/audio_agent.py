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

from .contracts import DevelopmentInput, DevelopmentOutput
from .rag_store import RagStore

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

_REPO_ROOT_ENV = Path(__file__).parents[1] / ".env"

# ---------------------------------------------------------------------------
# Prompt — loaded from prompts/
# ---------------------------------------------------------------------------

_PROMPTS_DIR = Path(__file__).parent / "prompts"
AUDIO_SYSTEM_PROMPT = (_PROMPTS_DIR / "audio_system_prompt.md").read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Build audio LLM chain
# ---------------------------------------------------------------------------

def _read_env() -> dict[str, str]:
    env: dict[str, str] = {}
    if _REPO_ROOT_ENV.exists():
        for line in _REPO_ROOT_ENV.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip()
    return env


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

    # Prefer Mistral Codestral for code generation
    mistral_key   = env.get("MISTRAL_WORKER_API_KEY") or env.get("MISTRAL_API_KEY", "")
    mistral_model = env.get("MISTRAL_WORKER_MODEL", "codestral-latest")
    mistral_url   = env.get("MISTRAL_BASE_URL", "https://api.mistral.ai/v1")

    if mistral_key:
        llm = ChatOpenAI(
            model=mistral_model, temperature=0,
            openai_api_base=mistral_url,
            openai_api_key=mistral_key,
            timeout=int(env.get("MISTRAL_WORKER_TIMEOUT_SECONDS", "90")),
            max_retries=0,
        )
        label = f"AUDIO/MISTRAL/{mistral_model}"
    else:
        # Fallback to local
        local_url = env.get("LOCAL_AI_BASE_URL", "http://192.168.1.175:1234/v1")
        local_model = env.get("LOCAL_AI_MODEL", "gemma-4-e4b-uncensored-hauhaucs-aggressive")
        llm = ChatOpenAI(
            model=local_model, temperature=0,
            openai_api_base=local_url,
            openai_api_key=env.get("LOCAL_AI_API_KEY", "lmstudio"),
            timeout=int(env.get("LOCAL_WORKER_TIMEOUT_SECONDS", "180")),
            max_retries=0,
        )
        label = f"AUDIO/LOCAL/{local_model}"

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
    from .developer_agent import _normalize_development_output

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

    try:
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

    status_col = _G if output.status == "done" else _Y
    print(f"\n{status_col}{_W}  [3/3] [{label}]  [{task.task_id}] → {output.status}{_RS}")
    print(f"{_DIM}         {output.summary[:90]}{_RS}")
    for fp in output.files_to_write:
        lines = fp.content.count("\n") + 1
        print(f"         {_B}✎ {fp.path}{_RS}  ({fp.mode}, {lines} líneas)")

    return output
