import os
import json
import sys
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

BASE = Path(__file__).resolve().parents[2]
ENV_FILE = BASE / ".env"
load_dotenv(ENV_FILE)

PROMPTS = BASE / "prompts"
DATA = BASE / "data"

_hw_ref_path = DATA / "amstrad_cpc_hardware_reference.md"
HW_REFERENCE = _hw_ref_path.read_text(encoding="utf-8") if _hw_ref_path.exists() else ""

_motor_path = DATA / "motor_grafico.md"
MOTOR_REFERENCE = _motor_path.read_text(encoding="utf-8") if _motor_path.exists() else ""

_tutorial_path = DATA / "tutorial_crear_video_juego.md"
TUTORIAL_REFERENCE = _tutorial_path.read_text(encoding="utf-8") if _tutorial_path.exists() else ""

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
LLM_REQUEST_TIMEOUT = float(os.getenv("LLM_REQUEST_TIMEOUT", "180"))

ANSI_YELLOW = "\033[33m"
ANSI_RESET = "\033[0m"
DEBUG_TAG = f"{ANSI_YELLOW}[Debug]{ANSI_RESET}"

PLATFORM_CONTEXT = """
Target platform: Amstrad CPC 6128
CPU: Z80A 4 MHz
RAM: 128 KB
Framework: CPCtelera
Toolchain: SDCC + make + cpct_mkproject
Absolute priorities:
1. Smooth controls
2. Smooth sprite motion
3. Maximum visual quality within realistic budget
Reject ideas that harm control feel or motion smoothness.
""".strip()


def build_model(model_override: str | None = None, provider: str | None = None, timeout: int | None = None) -> ChatOpenAI:
    """Build LLM client with optional provider override (nvidia, mistral, openai)."""
    provider = provider or LLM_PROVIDER
    effective_timeout = timeout if timeout is not None else LLM_REQUEST_TIMEOUT
    
    if provider == "nvidia":
        api_key = os.getenv("NVIDIA_API_KEY")
        model = model_override or os.getenv("NVIDIA_MODEL", "moonshotai/kimi-k2.6")
        base_url = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
        return ChatOpenAI(
            model=model,
            temperature=0.2,
            api_key=api_key,
            base_url=base_url,
            timeout=effective_timeout,
        )
    elif provider == "mistral":
        api_key = os.getenv("MISTRAL_API_KEY")
        model = model_override or os.getenv("MISTRAL_MODEL", "mistral-small-latest")
        base_url = os.getenv("MISTRAL_BASE_URL", "https://api.mistral.ai/v1")
        return ChatOpenAI(
            model=model,
            temperature=0.2,
            api_key=api_key,
            base_url=base_url,
            timeout=effective_timeout,
        )
    elif provider == "local":
        api_key = os.getenv("LOCAL_API_KEY", "local")
        model = model_override or os.getenv("LOCAL_MODEL", "gemma-4-e4b-uncensored-hauhaucs-agresive")
        base_url = os.getenv("LOCAL_BASE_URL", "http://192.168.1.175:12345/v1")
        return ChatOpenAI(
            model=model,
            temperature=0.2,
            api_key=api_key,
            base_url=base_url,
            timeout=effective_timeout,
        )
    else:  # openai
        api_key = os.getenv("OPENAI_API_KEY")
        model = model_override or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        return ChatOpenAI(
            model=model,
            temperature=0.2,
            api_key=api_key,
            timeout=effective_timeout,
        )


_YELLOW = "\033[33m"
_RESET  = "\033[0m"

def _stderr_print(message: str) -> None:
    sys.stderr.write(message + "\n")
    sys.stderr.flush()


# Agentes técnicos que reciben el motor_grafico como referencia primaria
_TECHNICAL_AGENTS = {
    "code_integrator",
    "art_direction",
    "art",
    "art_assets",
    "art_constraints",
    "design",
    "qa",
    "cpctelera_tech",
}


_SKIP_REFS = os.getenv("LLM_SKIP_REFS", "0").strip() == "1"


def load_prompt(name: str) -> str:
    base_prompt = (PROMPTS / f"{name}.txt").read_text(encoding="utf-8")
    if _SKIP_REFS:
        return base_prompt
    extras = []
    # Hardware reference → todos los agentes
    if HW_REFERENCE:
        extras.append(
            "## REFERENCIA HARDWARE AMSTRAD CPC "
            "(leer antes de generar cualquier sprite, código o asset)\n\n"
            + HW_REFERENCE
        )
    # Motor gráfico TFG → sólo agentes técnicos (su biblia)
    if MOTOR_REFERENCE and name in _TECHNICAL_AGENTS:
        extras.append(
            "## MOTOR GRÁFICO AMSTRAD CPC — REFERENCIA PRIMARIA "
            "(TFG: arquitectura, modos gráficos, VRAM, raycasting, optimizaciones Z80)\n"
            "Tratar como biblia técnica: todos los algoritmos y decisiones de diseño "
            "deben ser compatibles con las restricciones aquí descritas.\n\n"
            + MOTOR_REFERENCE
        )
    # Tutorial videojuegos retrocomputación → todos los agentes
    if TUTORIAL_REFERENCE:
        extras.append(
            "## TUTORIAL DE DESARROLLO DE VIDEOJUEGOS PARA SISTEMAS DE 8 BITS "
            "(conocimiento base obligatorio para todos los agentes)\n\n"
            + TUTORIAL_REFERENCE
        )
    if extras:
        return base_prompt + "\n\n---\n\n" + "\n\n---\n\n".join(extras)
    return base_prompt


def _retry_config() -> tuple[int, float, float]:
    retries = int(os.getenv("LLM_MAX_RETRIES", "12"))
    base_delay = float(os.getenv("LLM_RETRY_BASE_DELAY", "2"))
    max_delay = float(os.getenv("LLM_RETRY_MAX_DELAY", "120"))
    return max(retries, 1), max(base_delay, 0.1), max(max_delay, base_delay)


def _retry_after_seconds(error) -> float | None:
    response = getattr(error, "response", None)
    headers = getattr(response, "headers", None)
    if not headers:
        return None

    retry_after = headers.get("retry-after") or headers.get("Retry-After")
    if retry_after:
        token = str(retry_after).strip()
        try:
            return max(float(token), 0.0)
        except ValueError:
            try:
                retry_at = parsedate_to_datetime(token)
                if retry_at.tzinfo is None:
                    retry_at = retry_at.replace(tzinfo=timezone.utc)
                now = datetime.now(timezone.utc)
                return max((retry_at - now).total_seconds(), 0.0)
            except (TypeError, ValueError, OverflowError):
                pass

    retry_after_ms = headers.get("retry-after-ms") or headers.get("Retry-After-Ms")
    if retry_after_ms:
        try:
            return max(float(str(retry_after_ms).strip()) / 1000.0, 0.0)
        except ValueError:
            return None

    return None


def _retry_delay_for_error(error, attempt: int, base_delay: float, max_delay: float) -> float:
    hinted_delay = _retry_after_seconds(error)
    if hinted_delay is not None:
        return min(max(hinted_delay, base_delay), max_delay)
    return min(base_delay * (2 ** attempt), max_delay)


def _current_model_name(llm) -> str:
    return str(getattr(llm, "model_name", "") or getattr(llm, "model", "") or "").strip()


def _route_label(provider: str, llm) -> str:
    model = _current_model_name(llm) or "<provider-default>"
    return f"provider={provider} model={model}"


def _fallback_llm_for_error(llm, error, attempt: int, provider: str = "mistral"):
    """Return (llm, provider) fallback when a provider is rate limited."""
    if provider not in ("mistral", "nvidia"):
        return llm, provider

    text = str(error).lower()
    is_rate_limit = "rate limit" in text or "429" in text or "rate_limited" in text
    is_timeout = "timed out" in text or "timeout" in text or "read timeout" in text
    if not is_rate_limit and not is_timeout:
        return llm, provider

    if attempt < 2 and not is_timeout:
        return llm, provider

    if attempt < 1:
        return llm, provider

    if provider == "mistral":
        fallback_model = os.getenv("MISTRAL_FALLBACK_MODEL", "mistral-small-latest").strip()
    elif provider == "nvidia":
        fallback_model = os.getenv("NVIDIA_FALLBACK_MODEL", "").strip()
    else:
        return llm, provider

    current_model = _current_model_name(llm)
    if fallback_model and fallback_model != current_model:
        _stderr_print(f"[INFO] [retry] cambiando temporalmente a modelo fallback ({provider}): {fallback_model}")
        return build_model(model_override=fallback_model, provider=provider), provider

    if provider == "nvidia":
        mistral_api_key = os.getenv("MISTRAL_API_KEY", "").strip()
        if mistral_api_key:
            mistral_model = os.getenv("MISTRAL_FALLBACK_MODEL", os.getenv("MISTRAL_MODEL", "mistral-small-latest")).strip()
            if mistral_model:
                _stderr_print(f"[INFO] [retry] NVIDIA rate limited; failover temporal a Mistral: {mistral_model}")
                return build_model(model_override=mistral_model, provider="mistral"), "mistral"

    return llm, provider


def invoke_with_backoff(llm, messages, retries=None, base_delay=None, max_delay=None, provider: str = "mistral"):
    configured_retries, configured_base_delay, configured_max_delay = _retry_config()
    retries = configured_retries if retries is None else max(int(retries), 1)
    base_delay = configured_base_delay if base_delay is None else max(float(base_delay), 0.1)
    max_delay = configured_max_delay if max_delay is None else max(float(max_delay), base_delay)

    last_error = None
    recovery_context = None
    for attempt in range(retries):
        try:
            response = llm.invoke(messages)
            _rc = getattr(response, "content", None)
            if _rc and isinstance(_rc, str):
                _snippet = _rc.strip().replace("\n", " ")[:120]
                _model = _current_model_name(llm) or provider
                _stderr_print(f"[INFO] [llm] ({_model}) \u2190 {_YELLOW}{_snippet}{_RESET}")
            if recovery_context is not None:
                _stderr_print(
                    "[INFO] [retry] conexion restablecida tras error transitorio "
                    f"({recovery_context['attempt']}/{retries}); "
                    f"ruta activa {_YELLOW}{_route_label(provider, llm)}{_RESET}"
                )
            return response
        except Exception as e:
            last_error = e
            text = str(e).lower()
            context_exceeded = (
                "context size" in text
                or "context_length_exceeded" in text
                or "context window" in text
                or "maximum context" in text
            )
            retryable = (
                not context_exceeded
                and (
                    "rate limit" in text
                    or "429" in text
                    or "rate_limited" in text
                    or "connection error" in text
                    or "connecterror" in text
                    or "api connection error" in text
                    or "temporary failure" in text
                    or "name resolution" in text
                    or "nodename nor servname provided" in text
                    or "timed out" in text
                    or "timeout" in text
                )
            )
            if not retryable or attempt == retries - 1:
                raise
            previous_provider = provider
            previous_model = _current_model_name(llm)
            llm, provider = _fallback_llm_for_error(llm, e, attempt, provider=provider)
            current_model = _current_model_name(llm)
            delay = _retry_delay_for_error(e, attempt, base_delay, max_delay)
            error_snippet = str(e).strip()[:200]
            _stderr_print(
                f"[INFO] [retry] error transitorio detectado ({attempt + 1}/{retries}), "
                f"error: {error_snippet} | reintentando en {delay:.1f}s..."
            )
            if provider != previous_provider or current_model != previous_model:
                _stderr_print(
                    "[INFO] [retry] nueva ruta de reintento: "
                    f"provider={_YELLOW}{provider}{_RESET} model={_YELLOW}{current_model or '<provider-default>'}{_RESET}"
                )
            recovery_context = {
                "attempt": attempt + 1,
            }
            time.sleep(delay)
    raise last_error


def _is_debug_enabled() -> bool:
    value = os.getenv("LLM_DEBUG", "").strip().lower()
    return value in {"1", "true", "yes", "on"}


def _trace_llm_io(prompt_name: str, kind: str, content: str) -> None:
    if not _is_debug_enabled():
        return

    _stderr_print(f"{DEBUG_TAG} [llm][{prompt_name}] {kind}_START")
    _stderr_print(content)
    _stderr_print(f"{DEBUG_TAG} [llm][{prompt_name}] {kind}_END")


def _response_text(response) -> str:
    content = getattr(response, "content", response)

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                if "text" in item:
                    parts.append(str(item["text"]))
                elif "content" in item:
                    parts.append(str(item["content"]))
        return "\n".join(parts).strip()

    return str(content).strip()


def _extract_json_object(text: str) -> dict:
    raw = (text or "").strip()
    if not raw:
        raise ValueError("LLM returned empty content.")

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        parsed = json.loads(raw[start : end + 1])

    if not isinstance(parsed, dict):
        raise ValueError("Expected a JSON object at top level.")

    return parsed


_LOCAL_MODEL_DEFAULT = "gemma-4-e4b-uncensored-hauhaucs-aggressive"

_PROMPT_ROUTES: dict[str, dict[str, str]] = {
    "orchestrator": {
        "provider": "openai",
        "model_env": "OPENAI_MODEL",
        "default_model": "gpt-4.1",
    },
    "art": {
        "provider": "openai",
        "model_env": "OPENAI_MODEL",
        "default_model": "gpt-4.1",
    },
    "art_direction": {
        "provider": "openai",
        "model_env": "OPENAI_MODEL",
        "default_model": "gpt-4.1",
    },
    "art_assets": {
        "provider": "openai",
        "model_env": "OPENAI_MODEL",
        "default_model": "gpt-4.1",
    },
    "art_constraints": {
        "provider": "openai",
        "model_env": "OPENAI_MODEL",
        "default_model": "gpt-4.1",
    },
    "cpctelera_tech": {
        "provider": "openai",
        "model_env": "OPENAI_MODEL",
        "default_model": "gpt-4.1",
    },
    "code_integrator": {
        "provider": "openai",
        "model_env": "OPENAI_MODEL",
        "default_model": "gpt-4.1",
    },
    "design": {
        "provider": "openai",
        "model_env": "OPENAI_MODEL",
        "default_model": "gpt-4.1",
    },
    "narrative": {
        "provider": "openai",
        "model_env": "OPENAI_MODEL",
        "default_model": "gpt-4.1",
    },
    "qa": {
        "provider": "openai",
        "model_env": "OPENAI_MODEL",
        "default_model": "gpt-4.1",
    },
}


def _resolve_route_model(route: dict[str, str]) -> str | None:
    model_env = route.get("model_env", "")
    fallback_env = route.get("fallback_env", "")
    default_model = route.get("default_model", "")

    if model_env:
        model = os.getenv(model_env, "").strip()
        if model:
            return model
    if fallback_env:
        model = os.getenv(fallback_env, "").strip()
        if model:
            return model
    return default_model or None


def _resolve_provider_and_model(prompt_name: str, provider_override: str | None) -> tuple[str, str | None]:
    """Return (provider, model_override) for a given agent."""
    if provider_override is not None:
        return provider_override, None
    route = _PROMPT_ROUTES.get(prompt_name)
    if route is not None:
        return route.get("provider", LLM_PROVIDER), _resolve_route_model(route)
    return LLM_PROVIDER, None


def json_call(prompt_name: str, user_request: str, extra_context: str = "", retries: int = 3, provider: str | None = None) -> dict:
    """Call LLM and extract JSON response.

    Routing (configurable via .env):
    - orchestrator           → NVIDIA NVIDIA_MODEL_ORCHESTRATOR
    - art                    → NVIDIA NVIDIA_MODEL_ART / NVIDIA_MODEL
    - art_direction          → NVIDIA ART_DIRECTION_TEXT_MODEL
    - art_assets             → NVIDIA ART_ASSETS_TEXT_MODEL
    - art_constraints        → NVIDIA ART_CONSTRAINTS_TEXT_MODEL
    - cpctelera_tech         → NVIDIA NVIDIA_MODEL
    - code_integrator        → NVIDIA NVIDIA_MODEL
    - design                 → NVIDIA NVIDIA_MODEL
    - narrative              → NVIDIA NVIDIA_MODEL
    - qa                     → NVIDIA NVIDIA_MODEL
      - all others             → LLM_PROVIDER (mistral by default)
    """
    provider, model_override = _resolve_provider_and_model(prompt_name, provider)
    llm = build_model(model_override=model_override, provider=provider)
    system = load_prompt(prompt_name)

    context = PLATFORM_CONTEXT
    if extra_context:
        context += f"\n\nRetrieved project knowledge:\n{extra_context}"

    # RAG: inject relevant CPCtelera manual excerpts for technical agents
    if prompt_name in _TECHNICAL_AGENTS and not _SKIP_REFS:
        try:
            from app.services.rag_service import query_cpct_manual as _qcm
            _rag_query = user_request[:800].strip()
            if _rag_query:
                _rag_results = _qcm(_rag_query)
                if _rag_results:
                    context += (
                        "\n\n## CPCtelera Reference Manual — extractos relevantes\n"
                        "(Fragmentos del manual oficial CPCtelera. Usar como referencia "
                        "autoritativa para nombres de funciones, parámetros, macros y "
                        "restricciones de hardware. Tienen mayor prioridad que cualquier "
                        "conocimiento previo del modelo.)\n\n"
                        + _rag_results
                    )
        except Exception as _rag_err:
            _stderr_print(f"[RAG] injection skipped: {_rag_err}")

    messages = [
        {"role": "system", "content": system},
        {
            "role": "user",
            "content": (
                f"{context}\n\nUser request:\n{user_request}\n\n"
                "Devuelve SOLO un objeto JSON valido. Sin markdown, sin texto adicional."
            ),
        },
    ]

    last_error = None
    for _ in range(retries):
        request_trace = messages[-1].get("content", "") if isinstance(messages[-1], dict) else str(messages[-1])
        _trace_llm_io(prompt_name, "REQUEST", str(request_trace))

        response = invoke_with_backoff(llm, messages, provider=provider)
        text = _response_text(response)
        _trace_llm_io(prompt_name, "RESPONSE", text)

        try:
            return _extract_json_object(text)
        except Exception as exc:
            last_error = exc
            messages.extend(
                [
                    {"role": "assistant", "content": text},
                    {
                        "role": "user",
                        "content": (
                            "Tu respuesta anterior no fue JSON valido. "
                            "Repite SOLO el JSON valido, sin markdown ni explicaciones."
                        ),
                    },
                ]
            )

    raise ValueError(f"LLM JSON output could not be parsed after {retries} attempts: {last_error}")


def structured_call(prompt_name: str, schema, user_request: str, extra_context: str = "", provider: str | None = None):
    """Call LLM with structured output schema. Same routing as json_call."""
    provider, model_override = _resolve_provider_and_model(prompt_name, provider)
    llm = build_model(model_override=model_override, provider=provider).with_structured_output(schema)
    system = load_prompt(prompt_name)
    context = PLATFORM_CONTEXT
    if extra_context:
        context += f"\n\nRetrieved project knowledge:\n{extra_context}"
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": f"{context}\n\nUser request:\n{user_request}"},
    ]

    request_trace = messages[-1].get("content", "") if isinstance(messages[-1], dict) else str(messages[-1])
    _trace_llm_io(prompt_name, "REQUEST", str(request_trace))

    response = invoke_with_backoff(llm, messages, provider=provider)

    if hasattr(response, "model_dump"):
        response_text = json.dumps(response.model_dump(), ensure_ascii=False, indent=2)
    else:
        response_text = _response_text(response)
    _trace_llm_io(prompt_name, "RESPONSE", response_text)

    return response