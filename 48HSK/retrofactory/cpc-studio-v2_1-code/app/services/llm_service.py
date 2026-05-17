import os
import json
import time
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


def build_model() -> ChatOpenAI:
    if LLM_PROVIDER == "mistral":
        api_key = os.getenv("MISTRAL_API_KEY")
        model = os.getenv("MISTRAL_MODEL", "mistral-large-latest")
        base_url = os.getenv("MISTRAL_BASE_URL", "https://api.mistral.ai/v1")
        return ChatOpenAI(
            model=model,
            temperature=0.2,
            api_key=api_key,
            base_url=base_url,
        )

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    return ChatOpenAI(
        model=model,
        temperature=0.2,
        api_key=api_key,
    )


# Agentes técnicos que reciben el motor_grafico como referencia primaria
_TECHNICAL_AGENTS = {"code_integrator", "art", "design", "cpctelera_tech"}


def load_prompt(name: str) -> str:
    base_prompt = (PROMPTS / f"{name}.txt").read_text(encoding="utf-8")
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


def invoke_with_backoff(llm, messages, retries=5, base_delay=2):
    last_error = None
    for attempt in range(retries):
        try:
            return llm.invoke(messages)
        except Exception as e:
            last_error = e
            text = str(e).lower()
            retryable = (
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
            if not retryable or attempt == retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            print(f"[retry] error transitorio detectado, reintentando en {delay}s...")
            time.sleep(delay)
    raise last_error


def _is_debug_enabled() -> bool:
    value = os.getenv("LLM_DEBUG", "").strip().lower()
    return value in {"1", "true", "yes", "on"}


def _trace_llm_io(prompt_name: str, kind: str, content: str) -> None:
    if not _is_debug_enabled():
        return

    print(f"{DEBUG_TAG} [llm][{prompt_name}] {kind}_START")
    print(content)
    print(f"{DEBUG_TAG} [llm][{prompt_name}] {kind}_END")


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


def json_call(prompt_name: str, user_request: str, extra_context: str = "", retries: int = 3) -> dict:
    llm = build_model()
    system = load_prompt(prompt_name)

    context = PLATFORM_CONTEXT
    if extra_context:
        context += f"\n\nRetrieved project knowledge:\n{extra_context}"

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

        response = invoke_with_backoff(llm, messages)
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


def structured_call(prompt_name: str, schema, user_request: str, extra_context: str = ""):
    llm = build_model().with_structured_output(schema)
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

    response = invoke_with_backoff(llm, messages)

    if hasattr(response, "model_dump"):
        response_text = json.dumps(response.model_dump(), ensure_ascii=False, indent=2)
    else:
        response_text = _response_text(response)
    _trace_llm_io(prompt_name, "RESPONSE", response_text)

    return response