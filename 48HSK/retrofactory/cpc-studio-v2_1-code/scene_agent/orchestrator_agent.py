"""Orchestrator Agent — LangChain LCEL.

Interprets the user prompt, extracts intent, decomposes it into tasks, and
decides routing. Does NOT generate code. Returns an OrchestratorContract.

Chain:  ChatPromptTemplate | ChatOpenAI | PydanticOutputParser
"""
from __future__ import annotations

import logging
import time
import uuid
from pathlib import Path

import json as _json
import langchain
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Enable LangChain verbose traces in INFO logs
langchain.verbose = True
langchain.debug = False   # set True for full token-level traces

from .contracts import OrchestratorContract
from .rag_store import RagStore

logger = logging.getLogger(__name__)

_G   = "\033[32m"
_Y   = "\033[33m"
_B   = "\033[36m"
_W   = "\033[1m"
_DIM = "\033[2m"
_RS  = "\033[0m"

_REPO_ROOT_ENV = Path(__file__).parents[1] / ".env"

_orch_rag: RagStore | None = None


def _get_orch_rag() -> RagStore:
    global _orch_rag
    if _orch_rag is None:
        _orch_rag = RagStore.load_or_build_orchestrator()
    return _orch_rag


# ---------------------------------------------------------------------------
# Prompts — loaded from prompts/
# ---------------------------------------------------------------------------

_PROMPTS_DIR = Path(__file__).parent / "prompts"

def _load_prompt(filename: str) -> str:
    return (_PROMPTS_DIR / filename).read_text(encoding="utf-8")

# Escape braces so LangChain doesn't interpret JSON examples as template variables
_SYSTEM = _load_prompt("orchestrator_system_prompt.md").replace("{", "{{").replace("}", "}}")
_HUMAN  = _load_prompt("orchestrator_human_prompt.md")


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


_R = "\033[31m"


_NVIDIA_MAX_RETRIES = 3
_NVIDIA_RETRY_BASE  = 1.0   # seconds; doubles each retry: 1 → 2 → 4
_NVIDIA_TIMEOUT     = 240


def _build_llm(env: dict[str, str], timeout: int = _NVIDIA_TIMEOUT):
    """Return (llm, label).

    Priority:
      1. Mistral API direct (MISTRAL_ORCHESTRATOR_API_KEY or MISTRAL_API_KEY)
      2. NVIDIA NIM       (NVIDIA_ORCHESTRATOR_API_KEY)
    """
    # 1. Mistral direct API — better JSON schema compliance, faster for orchestration
    mistral_key   = env.get("MISTRAL_ORCHESTRATOR_API_KEY") or env.get("MISTRAL_API_KEY", "")
    mistral_model = env.get("MISTRAL_ORCHESTRATOR_MODEL", "mistral-large-latest")
    mistral_url   = env.get("MISTRAL_BASE_URL", "https://api.mistral.ai/v1")
    if mistral_key:
        llm = ChatOpenAI(
            model=mistral_model, temperature=0,
            openai_api_base=mistral_url,
            openai_api_key=mistral_key,
            # AMP LLM proxy authenticates via the "API-Key" header (ChatOpenAI
            # only sends Authorization: Bearer by default → 401). Harmless for
            # direct api.mistral.ai calls.
            default_headers={"API-Key": mistral_key},
            timeout=timeout,
            max_retries=0,
        )
        logger.info("[ORCH] primary LLM: Mistral — %s (timeout=%ds)", mistral_model, timeout)
        return llm, f"MISTRAL/{mistral_model}"

    # 2. NVIDIA NIM
    nvidia_key   = env.get("NVIDIA_ORCHESTRATOR_API_KEY", "")
    nvidia_model = env.get("NVIDIA_ORCHESTRATOR_MODEL", "nvidia/llama-3.3-nemotron-super-49b-v1.5")
    nvidia_url   = env.get("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
    if nvidia_key:
        llm = ChatOpenAI(
            model=nvidia_model, temperature=0,
            openai_api_base=nvidia_url,
            openai_api_key=nvidia_key,
            timeout=timeout,
        )
        logger.info("[ORCH] primary LLM: NVIDIA NIM — %s (timeout=%ds)", nvidia_model, timeout)
        return llm, f"NVIDIA/{nvidia_model}"

    raise RuntimeError(
        "No orchestrator LLM configured. Set MISTRAL_ORCHESTRATOR_API_KEY/MISTRAL_API_KEY "
        "or NVIDIA_ORCHESTRATOR_API_KEY. Local fallback is disabled."
    )


def _tolerant_validate_contract(raw: dict, user_prompt: str) -> "OrchestratorContract":
    """Validate raw dict → OrchestratorContract; coerce bad literal values before final raise."""
    # The LLM occasionally returns a bare `null`/list instead of a JSON object;
    # JsonOutputParser passes it straight through. Coerce to {} so the schema
    # repair below can rebuild a minimal valid contract instead of crashing.
    if not isinstance(raw, dict):
        logger.warning("[ORCH] LLM returned non-object (%s) — coercing to empty contract", type(raw).__name__)
        raw = {}
    try:
        return OrchestratorContract.model_validate(raw)
    except Exception as exc:
        logger.warning("[ORCH] strict validation failed (%s) — coercing schema", exc)

    intent = raw.get("intent") or {}
    if isinstance(intent, dict):
        valid_cats = {"gameplay", "runtime", "hud", "assets", "build", "qa", "refactor", "unknown"}
        if intent.get("category") not in valid_cats:
            intent["category"] = "unknown"
        for fld in ("summary", "goal"):
            if not intent.get(fld):
                intent[fld] = user_prompt[:80]
        raw["intent"] = intent

    routing = raw.get("routing") or {}
    if not isinstance(routing, dict) or routing.get("mode") not in ("single", "sequential", "parallel"):
        raw["routing"] = {"mode": "sequential", "reason": "coerced from invalid response"}
    elif not routing.get("reason"):
        routing["reason"] = "coerced"

    if not isinstance(raw.get("tasks"), list):
        raw["tasks"] = []
    if not raw.get("request_id"):
        raw["request_id"] = str(uuid.uuid4())[:8]
    if not raw.get("project_name"):
        raw["project_name"] = "testproject"
    if not raw.get("user_prompt"):
        raw["user_prompt"] = user_prompt

    return OrchestratorContract.model_validate(raw)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def orchestrate(
    user_prompt: str,
    project_name: str,
    settings,
) -> OrchestratorContract:
    """Run the orchestrator chain.

    Prints:
      → ORCH  when calling the LLM
      ← ORCH  when returning, with task summary
    """
    print(f"\n{_B}{_W}╔══ ORCHESTRATOR ══════════════════════════════════════════════╗{_RS}")
    print(f"{_B}{_W}║  → ANALIZANDO INTENCIÓN DEL PROMPT{_RS}")
    print(f"{_DIM}║  project : {project_name}{_RS}")
    print(f"{_DIM}║  prompt  : {user_prompt[:80]}{_RS}")

    env = _read_env()
    nvidia_timeout = int(env.get("NVIDIA_TIMEOUT", str(_NVIDIA_TIMEOUT)))
    llm, llm_label = _build_llm(env, timeout=nvidia_timeout)
    print(f"{_W}║  modelo  : {llm_label}{_RS}")
    print(f"{_B}{_W}╚══════════════════════════════════════════════════════════════╝{_RS}")

    parser = JsonOutputParser()
    prompt = ChatPromptTemplate.from_messages([
        ("system", _SYSTEM),
        ("human", _HUMAN),
    ])
    chain = prompt | llm | parser

    max_retries  = int(env.get("NVIDIA_MAX_RETRIES", str(_NVIDIA_MAX_RETRIES)))
    retry_base   = float(env.get("NVIDIA_RETRY_BASE", str(_NVIDIA_RETRY_BASE)))
    # RAG: retrieve architecture/design context from doc/ root files
    rag_context = ""
    try:
        orch_rag = _get_orch_rag()
        chunks = orch_rag.retrieve(
            f"{user_prompt} agent architecture decomposition", top_k=3
        )
        rag_context = "\n".join(
            f"[{i}] {c.source}:\n{c.text[:300]}" for i, c in enumerate(chunks, 1)
        )
    except Exception as rag_exc:
        logger.warning("[ORCH] RAG unavailable: %s", rag_exc)

    invoke_input  = {"project_name": project_name, "user_prompt": user_prompt, "rag_context": rag_context}
    raw: dict | None = None

    if "NVIDIA" in llm_label:
        for attempt in range(1, max_retries + 1):
            try:
                print(f"\n{_Y}  [{attempt}/{max_retries}] intentando {llm_label} …{_RS}")
                logger.info("[ORCH] NVIDIA attempt %d/%d", attempt, max_retries)
                raw = chain.invoke(invoke_input)
                if not isinstance(raw, dict):
                    raise ValueError(f"respuesta no-objeto del LLM: {type(raw).__name__}")
                print(f"{_G}  [{attempt}/{max_retries}] {llm_label} → OK{_RS}")
                break
            except Exception as exc:
                delay = retry_base * (2 ** (attempt - 1))
                print(f"{_R}  [{attempt}/{max_retries}] {llm_label} → fallo: {type(exc).__name__}{_RS}")
                logger.warning("[ORCH] NVIDIA attempt %d/%d failed: %s", attempt, max_retries, exc)
                if attempt < max_retries:
                    print(f"{_Y}  reintentando en {delay:.0f}s …{_RS}")
                    time.sleep(delay)

        if raw is None:
            raise RuntimeError(
                f"{llm_label} agotado tras {max_retries} intentos y local fallback deshabilitado"
            )
    else:
        for attempt in range(1, 3):
            try:
                print(f"\n{_Y}  [{attempt}/2] intentando {llm_label} …{_RS}")
                logger.info("[ORCH] primary attempt %d/2", attempt)
                raw = chain.invoke(invoke_input)
                if not isinstance(raw, dict):
                    raise ValueError(f"respuesta no-objeto del LLM: {type(raw).__name__}")
                print(f"{_G}  [{attempt}/2] {llm_label} → OK{_RS}")
                break
            except Exception as exc:
                logger.warning("[ORCH] primary attempt %d/2 failed: %s", attempt, exc)
                if attempt < 2:
                    print(f"{_Y}  [{attempt}/2] {llm_label} → fallo, reintentando en 2s …{_RS}")
                    time.sleep(2.0)
                else:
                    raise

    # Tolerant validation — coerces wrong literal values before raising
    contract = _tolerant_validate_contract(raw, user_prompt)

    # Ensure a request_id is present (LLM might omit it)
    if not contract.request_id:
        contract = contract.model_copy(
            update={"request_id": str(uuid.uuid4())[:8]}
        )

    # Patch user_prompt in case the LLM left it empty
    if not contract.user_prompt:
        contract = contract.model_copy(update={"user_prompt": user_prompt})

    print(f"\n{_G}{_W}  ✓ [{llm_label}]  orquestación completa{_RS}")
    print(f"{_DIM}    intención : [{contract.intent.category}] {contract.intent.summary[:75]}{_RS}")
    print(f"{_DIM}    routing   : {contract.routing.mode} — {contract.routing.reason[:60]}{_RS}")
    print(f"{_DIM}    tareas    : {len(contract.tasks)}{_RS}")
    for task in sorted(contract.tasks, key=lambda t: t.priority):
        print(
            f"    {_B}[{task.task_id}]{_RS} [{task.subagent:20s}]"
            f" p{task.priority}  {task.title[:55]}"
        )
    if contract.risks:
        for r in contract.risks:
            col = _Y if r.level in ("low", "medium") else "\033[31m"
            print(f"    {col}⚠ [{r.level}] {r.message[:70]}{_RS}")

    logger.info(
        "[ORCH] done: %d tasks, routing=%s, intent=%s",
        len(contract.tasks),
        contract.routing.mode,
        contract.intent.category,
    )
    return contract


if __name__ == "__main__":
    import json, sys, logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    if len(sys.argv) < 3:
        print("Usage: python -m scene_agent.orchestrator_agent <project_name> <prompt>")
        sys.exit(1)
    project = sys.argv[1]
    prompt  = " ".join(sys.argv[2:])
    from .settings import AppSettings
    contract = orchestrate(prompt, project, AppSettings())
    print(json.dumps(contract.model_dump(), indent=2, ensure_ascii=False))
