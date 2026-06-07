"""Development Worker Agent — LangChain with_structured_output().

Worker in the planner/executor pattern:
  - Input : DevelopmentInput  (one task, fully specified by the orchestrator)
  - Output: DevelopmentOutput (files_to_write ready to flush, status, risks)

Uses with_structured_output(DevelopmentOutput) — Pydantic validation automatic.
Can run standalone or as a node under a LangGraph Supervisor.
"""
from __future__ import annotations

import langchain
import logging
from pathlib import Path
from typing import Any

import json as _json
import re as _re
import time as _time
from json_repair import repair_json
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .contracts import DevelopmentInput, DevelopmentOutput, FilePatch
from .rag_store import RagStore

_rag_instance: RagStore | None = None


def _get_rag() -> RagStore:
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = RagStore.load_or_build()
        logger.info("RAG store ready: %d chunks", _rag_instance.chunk_count)
    return _rag_instance

langchain.verbose = True
logger = logging.getLogger(__name__)

_G   = "\033[32m"
_Y   = "\033[33m"
_R   = "\033[31m"
_B   = "\033[36m"
_W   = "\033[1m"
_DIM = "\033[2m"
_RS  = "\033[0m"

_REPO_ROOT_ENV = Path(__file__).parents[1] / ".env"
_LOG_DIR = Path(__file__).parent / "test_logs"

# ---------------------------------------------------------------------------
# System prompt — loaded from prompts/developer_system_prompt.md
# ---------------------------------------------------------------------------

_RULES_FILE   = Path(__file__).parent / "prompts" / "cpctelera_c89_rules.md"
_PROMPT_FILE  = Path(__file__).parent / "prompts" / "developer_system_prompt.md"


def _load_system_prompt() -> str:
    rules  = _RULES_FILE.read_text(encoding="utf-8") if _RULES_FILE.exists() else ""
    template = _PROMPT_FILE.read_text(encoding="utf-8")
    return template.replace("<<rules>>", rules)


SYSTEM_PROMPT = _load_system_prompt()

# ---------------------------------------------------------------------------
# Agent builder
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


def _write_failed_model_output(task_id: str, model_label: str, raw_text: str, reason: str) -> Path:
    _LOG_DIR.mkdir(parents=True, exist_ok=True)
    safe_model = _re.sub(r"[^A-Za-z0-9_.-]+", "_", model_label)
    timestamp = _time.strftime("%Y%m%d_%H%M%S")
    log_path = _LOG_DIR / f"llm_raw_{task_id}_{safe_model}_{timestamp}.log"
    log_path.write_text(
        f"task_id: {task_id}\nmodel: {model_label}\nreason: {reason}\n\n{raw_text}",
        encoding="utf-8",
    )
    return log_path


def _shorten_diag(text: str, limit: int = 1200) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[:limit] + "\n...[truncated]"


def _extract_llm_error_details(exc: Exception) -> str:
    """Extract nested provider diagnostics (status/body/response) from exceptions."""
    lines: list[str] = []
    seen: set[int] = set()
    cur: BaseException | None = exc
    level = 0

    while cur is not None and id(cur) not in seen and level < 4:
        seen.add(id(cur))
        pfx = f"cause[{level}]"
        lines.append(f"{pfx}: {cur.__class__.__name__}: {cur}")

        status_code = getattr(cur, "status_code", None)
        body = getattr(cur, "body", None)
        response = getattr(cur, "response", None)

        if status_code is not None:
            lines.append(f"{pfx}.status_code: {status_code}")

        if body:
            try:
                body_text = body if isinstance(body, str) else _json.dumps(body, ensure_ascii=False)
                lines.append(f"{pfx}.body:\n{_shorten_diag(body_text)}")
            except Exception:
                lines.append(f"{pfx}.body: {body}")

        if response is not None:
            resp_status = getattr(response, "status_code", None)
            if resp_status is not None:
                lines.append(f"{pfx}.response.status_code: {resp_status}")

            resp_text: str | None = None
            try:
                text_attr = getattr(response, "text", None)
                if callable(text_attr):
                    text_attr = text_attr()
                if isinstance(text_attr, str) and text_attr.strip():
                    resp_text = text_attr
            except Exception:
                resp_text = None

            if resp_text is None:
                try:
                    json_fn = getattr(response, "json", None)
                    if callable(json_fn):
                        resp_json = json_fn()
                        resp_text = _json.dumps(resp_json, ensure_ascii=False)
                except Exception:
                    resp_text = None

            if resp_text:
                lines.append(f"{pfx}.response.body:\n{_shorten_diag(resp_text)}")

        nxt = cur.__cause__ or cur.__context__
        if nxt is cur:
            break
        cur = nxt
        level += 1

    return "\n".join(lines)


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


def _normalize_development_output(raw: dict[str, Any], task_id: str) -> dict[str, Any]:
    """Repair common LLM schema drift before Pydantic validation."""
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

    normalized: dict[str, Any] = dict(raw)
    normalized["task_id"] = str(normalized.get("task_id") or task_id)
    normalized["status"] = normalized.get("status") or "blocked"
    normalized["summary"] = str(normalized.get("summary") or "LLM response normalized before validation.")
    normalized["notes"] = normalized.get("notes") or []
    normalized["risks"] = normalized.get("risks") or []
    normalized["follow_up_questions"] = normalized.get("follow_up_questions") or []

    raw_patches = normalized.get("files_to_write")
    if not isinstance(raw_patches, list):
        raw_patches = []

    cleaned_patches: list[dict[str, str]] = []
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


def _make_nvidia_llm(env: dict[str, str]):
    model = env.get("NVIDIA_WORKER_MODEL", "qwen/qwen3-coder-480b-a35b-instruct")
    llm = ChatOpenAI(
        model=model, temperature=0,
        openai_api_base=env.get("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1"),
        openai_api_key=env.get("NVIDIA_WORKER_API_KEY", ""),
        timeout=_env_int(env, "NVIDIA_WORKER_TIMEOUT_SECONDS", 45),
        max_retries=0,
    )
    return llm, f"NVIDIA/{model}"


def _make_local_llm(env: dict[str, str]):
    model = env.get("LOCAL_AI_MODEL", "gemma-4-e4b-uncensored-hauhaucs-aggressive")
    local_url = (
        env.get("LOCAL_AI_BASE_URL", "http://192.168.1.175:1234/v1/chat/completions")
        .replace("/chat/completions", "").rstrip("/")
    )
    llm = ChatOpenAI(
        model=model, temperature=0,
        openai_api_base=local_url,
        openai_api_key=env.get("LOCAL_AI_API_KEY", "lmstudio"),
        timeout=_env_int(env, "LOCAL_WORKER_TIMEOUT_SECONDS", 180),
        max_retries=0,
    )
    return llm, f"LOCAL/{model}"


def _build_worker_llm(env: dict[str, str]) -> tuple:
    """Devuelve (llm, label) — Mistral Codestral primero, NVIDIA segundo, local Gemma último recurso."""
    mistral_key   = env.get("MISTRAL_WORKER_API_KEY") or env.get("MISTRAL_API_KEY", "")
    mistral_model = env.get("MISTRAL_WORKER_MODEL", "codestral-latest")
    if mistral_key:
        llm = ChatOpenAI(
            model=mistral_model, temperature=0,
            openai_api_base=env.get("MISTRAL_BASE_URL", "https://api.mistral.ai/v1"),
            openai_api_key=mistral_key,
            timeout=_env_int(env, "MISTRAL_WORKER_TIMEOUT_SECONDS", 90),
            max_retries=0,
        )
        return llm, f"MISTRAL/{mistral_model}"
    if env.get("NVIDIA_WORKER_API_KEY", ""):
        return _make_nvidia_llm(env)
    return _make_local_llm(env)


def build_development_agent(settings) -> tuple:
    """Devuelve (chain, model_label)."""
    env = _read_env()
    llm, label = _build_worker_llm(env)

    schema_hint = (
        "\nReturn ONLY valid JSON (no markdown):\n"
        '{{ "task_id": "string", "status": "done|blocked|needs_clarification", '
        '"summary": "string", "files_to_write": '
        '[{{"path": "src/main.c", "content": "C source here", "mode": "write"}}], '
        '"notes": [], "risks": [], "follow_up_questions": [] }}'
        "\nEvery files_to_write item MUST include non-empty path, content, and mode. "
        "mode MUST be exactly one of: write, append, patch."
    )

    _sys_esc = SYSTEM_PROMPT.replace("{", "{{").replace("}", "}}")
    prompt = ChatPromptTemplate.from_messages([
        ("system", _sys_esc + schema_hint),
        ("user", "=== CPCtelera knowledge ===\n{rag_context}\n\n"
                 "TASK:\n{task_json}\n\n"
                 "PROJECT CONTEXT:\n{project_context}"),
    ])

    chain = prompt | llm | StrOutputParser() | _parse_output
    return chain, label


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def _rag_query(task: DevelopmentInput) -> str:
    """Build a RAG query relevant to the actual task — special-cased for FIX tasks."""
    if not task.task_id.startswith("FIX_"):
        return f"CPCtelera C89 {task.goal[:60]} mode0 erase draw pattern"

    # For fix tasks, extract the error type from the compiler output in context
    error_ctx = next(
        (c for c in task.context if c.startswith("ERRORES DEL COMPILADOR")), ""
    )
    if not error_ctx:
        return "CPCtelera C89 SDCC variable declaration function block scope"

    el = error_ctx.lower()
    # C89 declaration-after-statement (most common: "syntax error: token -> 'u8'")
    if "syntax error" in el and any(t in el for t in ("'u8'", "'i8'", "'u16'", "'char'", "'int'")):
        return (
            "CPCtelera C89 SDCC variable declaration before statement block function "
            "loop for nested scope all variables top"
        )
    # Undefined identifier — variable not declared
    if "undefined identifier" in el or "undeclared" in el:
        return "CPCtelera C89 SDCC undeclared variable loop for block scope declaration top"
    # Missing #define
    if "'rows'" in el or "'cols'" in el or "define" in el:
        return "CPCtelera C preprocessor #define macro constant ROWS COLS integer"
    # Implicit function declaration / prototype missing
    if "implicit function" in el or "prototype" in el:
        return "CPCtelera C89 function prototype forward declaration header"
    # Fallback: first 120 chars of errors as query context
    snippet = error_ctx[len("ERRORES DEL COMPILADOR SDCC:\n"):].strip()[:120]
    return f"CPCtelera SDCC C89 compile error fix: {snippet}"


def run_task(task: DevelopmentInput, settings) -> DevelopmentOutput:
    """Execute one development task and return a validated DevelopmentOutput."""
    env = _read_env()

    print(f"\n{_B}{_W}╔══ DEV WORKER [{task.task_id}] ══════════════════════════════════╗{_RS}")
    print(f"{_B}{_W}║  tarea  : {task.goal[:65]}{_RS}")
    print(f"{_B}{_W}╚══════════════════════════════════════════════════════════════╝{_RS}")

    # 1. RAG
    print(f"\n{_Y}  [1/3]  buscando contexto RAG …{_RS}")
    rag_context = ""
    try:
        rag = _get_rag()
        query  = _rag_query(task)
        top_k  = 5 if task.task_id.startswith("FIX_") else 3
        chunks = rag.retrieve(query, top_k=top_k)
        print(f"{_DIM}         query: {query[:90]}{_RS}")
        for i, c in enumerate(chunks, 1):
            is_ex = "cpctelera/examples" in c.source
            print(f"{_DIM}         [{i}] {'[EX] ' if is_ex else ''}{c.source}{_RS}")
        rag_context = "\n".join(f"[{i}] {c.source}:\n{c.text[:200]}" for i, c in enumerate(chunks, 1))
    except Exception as rag_exc:
        print(f"{_Y}  [1/3] RAG no disponible ({rag_exc.__class__.__name__}) — continuando sin contexto{_RS}")
    project_context = (
        f"project: {task.project_name}\n"
        f"target_files: {task.target_files}\n"
        f"constraints:\n" + "\n".join(f"  - {c}" for c in task.constraints)
    )

    # 2. LLM — generar código C
    chain, model_label = build_development_agent(settings)
    print(f"{_Y}  [2/3] [{model_label}]  generando código C …{_RS}")
    logger.info("[DEV] invoking %s for task %s …", model_label, task.task_id)

    invoke_input = {
        "task_json":       task.model_dump_json(indent=2),
        "project_context": project_context,
        "rag_context":     rag_context,
    }

    def _validate_for_task(raw: dict[str, Any]) -> DevelopmentOutput:
        normalized = _normalize_development_output(raw, task.task_id)
        return DevelopmentOutput.model_validate(normalized)

    # Primary LLM call with 429-retry before activating fallback chain
    _RETRY_DELAYS = _env_retry_delays(env, "NVIDIA_WORKER_RETRY_DELAYS", [5, 10])
    output = None
    last_exc: Exception | None = None
    last_exc_diag = ""
    for _attempt, _delay in enumerate([0] + _RETRY_DELAYS):
        if _delay:
            print(f"{_Y}  ↺  [{model_label}]  429 rate-limit — esperando {_delay}s …{_RS}")
            _time.sleep(_delay)
        try:
            output = _validate_for_task(chain.invoke(invoke_input))
            break
        except Exception as exc:
            last_exc = exc
            last_exc_diag = _extract_llm_error_details(exc)
            exc_text = str(exc)
            exc_text_lower = exc_text.lower()
            is_rate_limit = "429" in exc_text or "too many requests" in exc_text_lower
            is_timeout = (
                "timeout" in exc_text_lower
                or "timed out" in exc_text_lower
                or exc.__class__.__name__ in {"APITimeoutError", "ReadTimeout", "TimeoutError"}
            )
            if is_timeout and "LOCAL" not in model_label:
                print(f"{_Y}  ↩  [{model_label}] timeout — activando fallback sin más espera{_RS}")
                break
            if "LOCAL" in model_label or not is_rate_limit or _attempt == len(_RETRY_DELAYS):
                break
            # else: retry after delay

    if output is None:
        exc = last_exc
        # If we were already on local (last resort), no further fallback exists
        if "LOCAL" in model_label:
            raise exc
        print(f"\n{_R}  ✗ {model_label} falló (definitivo): {exc}{_RS}")
        if last_exc_diag:
            print(f"{_DIM}    detalle proveedor:\n{last_exc_diag}{_RS}")

        from langchain_core.output_parsers import StrOutputParser as _StrOut
        from langchain_core.prompts import ChatPromptTemplate as _CPT

        # JSON prompt — used by NVIDIA (handles structured output well)
        _schema = (
            "\nReturn ONLY valid JSON (no markdown):\n"
            '{{ "task_id": "string", "status": "done|blocked|needs_clarification", '
            '"summary": "string", "files_to_write": '
            '[{{"path": "src/main.c", "content": "C source here", "mode": "write"}}], '
            '"notes": [], "risks": [], "follow_up_questions": [] }}'
            "\nEvery files_to_write item MUST include non-empty path, content, and mode. "
            "mode MUST be exactly one of: write, append, patch."
        )
        _sys_esc2 = SYSTEM_PROMPT.replace("{", "{{").replace("}", "}}")
        _prompt_json = _CPT.from_messages([
            ("system", _sys_esc2 + _schema),
            ("user", "=== CPCtelera knowledge ===\n{rag_context}\n\n"
                     "TASK:\n{task_json}\n\nPROJECT CONTEXT:\n{project_context}"),
        ])

        # Lean input — reduced context for fallback models with smaller context windows
        is_fix_task = task.task_id.startswith("FIX_")
        def _trim_ctx(c: str) -> str | None:
            if c.startswith("ESTADO ACTUAL src/main.c"):
                return c[:3500] if is_fix_task else None
            if c.startswith("ERRORES DEL COMPILADOR"):
                return c[:800]
            return c
        lean_context = [r for c in task.context if (r := _trim_ctx(c)) is not None]
        lean_task = task.model_copy(update={"context": lean_context})
        lean_input = {
            "task_json":       lean_task.model_dump_json(indent=2),
            "project_context": project_context,
            "rag_context":     rag_context[:300],
        }

        # ── NVIDIA fallback (only when Mistral was primary) ───────────────────
        nvidia_exc: Exception | None = None
        nvidia_exc_diag = ""
        if "MISTRAL" in model_label:
            if env.get("NVIDIA_WORKER_API_KEY", ""):
                nvidia_llm, nvidia_label = _make_nvidia_llm(env)
                print(f"{_Y}  ↩  [{nvidia_label}]  segundo modelo …{_RS}")
                _NV_DELAYS = _env_retry_delays(env, "NVIDIA_WORKER_RETRY_DELAYS", [5, 10])
                for _att, _dly in enumerate([0] + _NV_DELAYS):
                    if _dly:
                        print(f"{_Y}  ↺  [{nvidia_label}]  429 — esperando {_dly}s …{_RS}")
                        _time.sleep(_dly)
                    try:
                        raw_nv = (_prompt_json | nvidia_llm | _StrOut()).invoke(lean_input)
                        output = _validate_for_task(_parse_output(raw_nv))
                        model_label = nvidia_label
                        break
                    except Exception as _nv_exc:
                        nvidia_exc = _nv_exc
                        nvidia_exc_diag = _extract_llm_error_details(_nv_exc)
                        _et = str(_nv_exc).lower()
                        if ("timeout" in _et or "timed out" in _et
                                or _nv_exc.__class__.__name__ in {"APITimeoutError", "ReadTimeout", "TimeoutError"}):
                            print(f"{_Y}  ↩  [{nvidia_label}] timeout — saltando a local …{_RS}")
                            break
                        if "429" not in str(_nv_exc) and "too many requests" not in _et:
                            break
                        if _att == len(_NV_DELAYS):
                            break

        # ── Local fallback (last resort — code-only prompt, no JSON) ─────────
        if output is None:
            fallback_llm, local_label = _make_local_llm(env)
            local_model = local_label.split("/", 1)[1]
            print(f"{_R}  ↩  Conectando al modelo local [{local_model}] …{_RS}")
            # Code-only prompt: avoids JSON parse failures on small/quantised models
            _local_prompt = _CPT.from_messages([
                ("system",
                 "Eres un experto en CPCtelera (Amstrad CPC, C89/SDCC). "
                 "Escribe SOLO el contenido completo y compilable del archivo src/main.c "
                 "para la tarea recibida. No uses bloques markdown. Solo código C válido."),
                ("user", "TAREA:\n{task_json}\n\nCONTEXTO DEL PROYECTO:\n{project_context}"),
            ])
            simple_input = {
                "task_json":       lean_task.model_dump_json(indent=2),
                "project_context": project_context,
            }
            model_label = f"LOCAL/{local_model}"
            print(f"{_Y}  [2/3] [{model_label}]  generando código C …{_RS}")
            try:
                raw_local_output = (_local_prompt | fallback_llm | _StrOut()).invoke(simple_input)
                raw_code = _re.sub(r'^```[a-zA-Z]*\n?', '', raw_local_output.strip())
                raw_code = _re.sub(r'\n?```\s*$', '', raw_code).strip()
                if not raw_code:
                    raise ValueError("Local model returned empty content")
                output = _validate_for_task({
                    "task_id": task.task_id,
                    "status": "done",
                    "summary": f"Código C generado por fallback local ({raw_code.count(chr(10)) + 1} líneas)",
                    "files_to_write": [{"path": "src/main.c", "content": raw_code, "mode": "write"}],
                    "notes": [],
                    "risks": ["Generado por modelo local sin validación JSON — revisar compilación"],
                    "follow_up_questions": [],
                })
            except Exception as local_exc:
                local_exc_diag = _extract_llm_error_details(local_exc)
                local_log = None
                if "raw_local_output" in locals() and isinstance(raw_local_output, str):
                    local_log = _write_failed_model_output(
                        task.task_id, model_label, raw_local_output,
                        f"{local_exc.__class__.__name__}: {local_exc}",
                    )
                print(f"{_R}  ✗ [{model_label}] también falló: {local_exc.__class__.__name__}: {local_exc}{_RS}")
                if local_exc_diag:
                    print(f"{_DIM}    detalle proveedor local:\n{local_exc_diag}{_RS}")
                if local_log is not None:
                    print(f"{_DIM}    raw local output guardado en {local_log}{_RS}")
                print(f"{_R}    Todos los modelos fallaron — marcando tarea como blocked{_RS}")
                failed = f"Primario: {exc}"
                if nvidia_exc is not None:
                    failed += f". NVIDIA: {nvidia_exc}"
                failed += f". Local: {local_exc}"
                diag_chunks = [
                    f"Primary diag:\n{last_exc_diag}" if last_exc_diag else "",
                    f"NVIDIA diag:\n{nvidia_exc_diag}" if nvidia_exc_diag else "",
                    f"Local diag:\n{local_exc_diag}" if local_exc_diag else "",
                ]
                diag_text = "\n\n".join(c for c in diag_chunks if c)
                output = DevelopmentOutput(
                    task_id=task.task_id,
                    status="blocked",
                    summary=f"Todos los LLMs fallaron. {failed}",
                    files_to_write=[],
                    risks=[
                        "Mistral/NVIDIA/local fallaron — reintenta más tarde",
                        *([_shorten_diag(diag_text, 1400)] if diag_text else []),
                        *([f"Raw local output: {local_log}"] if local_log is not None else []),
                    ],
                )

    # 3. Resultado
    status_col = _G if output.status == "done" else (_Y if output.status == "needs_clarification" else "\033[31m")
    print(f"\n{status_col}{_W}  [3/3] [{model_label}]  [{task.task_id}] → {output.status}{_RS}")
    print(f"{_DIM}         {output.summary[:90]}{_RS}")
    for fp in output.files_to_write:
        lines = fp.content.count("\n") + 1
        print(f"         {_B}✎ {fp.path}{_RS}  ({fp.mode}, {lines} líneas)")
    for r in output.risks:
        print(f"         {_Y}⚠ {r[:70]}{_RS}")
    for q in output.follow_up_questions:
        print(f"         {_Y}? {q[:70]}{_RS}")

    return output


def input_from_taskdef(taskdef, project_name: str = "testproject") -> DevelopmentInput:
    """Convert an IntentSpec TaskDef → DevelopmentInput for the worker."""
    return DevelopmentInput(
        task_id=taskdef.task_id,
        project_name=project_name,
        goal=taskdef.functional_instruction,
        context=list(taskdef.input_context),
        acceptance_criteria=list(taskdef.acceptance_checks),
        constraints=[
            "C89/SDCC — declare ALL variables before any statement",
            "No stdio.h, stdlib.h, printf, puts",
            "CPCtelera API only — <cpctelera.h>",
            "Colour bytes via cpct_px2byteM0(pen,pen) assigned in init_game() — NEVER hardcode 0xC0/0xCC/0x03/0x0F",
            "Key constants: Key_Space Key_CursorLeft Key_CursorRight Key_Return — NEVER KEY_Space or CPCT_KEY_*",
            "cpct_getScreenPtr: x in BYTES 0-79, y in pixels 0-199",
            "Strings in Mode 0: each char = 4 bytes. Max chars from x: x=0→20 x=20→15 x=40→10 x=60→5",
            "Ball y-movement: NEVER clamp ball_y at any maximum — no 'if (ball_y>=FLOOR_Y-BALL_H) ball_y=FLOOR_Y-BALL_H' and no 'if (ball_y>=200-BALL_H) ball_vy=-1'. Only the floor boundary check handles life loss.",
            "ball_vx and ball_vy are GLOBAL i8 variables. NEVER redeclare them as local variables inside update_game() or any function — a local 'i8 ball_vx=1' shadows the global and resets direction every frame, breaking all bouncing.",
            "Ceiling bounce: if (ball_vy < 0 && ball_y == 0) ball_vy = 1; — ONLY invert ball_vy, NEVER touch ball_vx.",
            "ball_bottom MUST be declared without initializer (u8 ball_bottom;) and computed AFTER moving ball_y (ball_bottom = ball_y + BALL_H - 1). Never initialize it at the start of update_game — stale value causes wrong floor/paddle collision timing.",
            "Audio API available via #include \"audio.h\" (already in src/): call audio_init() once in init_game(), audio_update() at end of main loop, audio_play_sfx(SFX_WALL_HIT/SFX_PADDLE_HIT/SFX_BRICK_HIT/SFX_LIFE_LOST/SFX_GAME_OVER) on events. Do NOT implement audio — just call the API.",
            getattr(taskdef, "implementation_hint", "") or "",
        ],
        target_files=["src/main.c"],
    )


if __name__ == "__main__":
    import json, sys, logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    if len(sys.argv) < 3:
        print("Usage: python -m scene_agent.developer_agent <task_id> <goal>")
        sys.exit(1)
    from .settings import AppSettings
    task = DevelopmentInput(
        task_id=sys.argv[1],
        project_name="testproject",
        goal=" ".join(sys.argv[2:]),
        acceptance_criteria=["Compiles with make", "Implements the described goal"],
        constraints=["C89/SDCC", "CPCtelera API only", "No stdio.h"],
        target_files=["src/main.c"],
    )
    result = run_task(task, AppSettings())
    print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))
