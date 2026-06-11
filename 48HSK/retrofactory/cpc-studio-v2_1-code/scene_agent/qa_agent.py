"""QA Agent — semantic review of the generated game against the ORIGINAL prompt.

Game-agnostic by design: the success criteria ARE the user's prompt, not a
fixed rule set. Runs inside the fix loop after compilation; the violations it
returns feed the fix agent exactly like compiler errors do.

Contract:
  Input : original user prompt + final src/main.c
  Output: list[str] of violated requirements (empty = code honours the prompt)
"""
from __future__ import annotations

import logging

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from .developer_agent import _build_worker_llm, _parse_output, _read_env

logger = logging.getLogger(__name__)

_G   = "\033[32m"
_Y   = "\033[33m"
_R   = "\033[31m"
_B   = "\033[36m"
_W   = "\033[1m"
_DIM = "\033[2m"
_RS  = "\033[0m"

_MAX_VIOLATIONS = 5

QA_SYSTEM_PROMPT = """Eres un revisor QA de juegos CPCtelera (Amstrad CPC, C89/SDCC).
Recibes el PROMPT ORIGINAL del usuario (la especificación) y el src/main.c final.
Tu trabajo: detectar requisitos EXPLÍCITOS del prompt que el código INCUMPLE.

Reglas:
- Solo violaciones verificables leyendo el código (estructura, llamadas, orden de
  ejecución). Nada de estilo, micro-optimizaciones ni mejoras opcionales.
- Presta especial atención a:
  * qué se dibuja en init vs. en el bucle principal (el decorado estático y las
    etiquetas/valores iniciales del HUD deben pintarse UNA vez en init);
  * redibujados completos de escena dentro del bucle (matan el rendimiento en un
    Z80 a 4MHz — solo las entidades móviles usan erase/draw por frame);
  * mandatos del prompt marcados como EXACTLY / MUST / NEVER / ONCE.
- Máximo 5 violaciones, las más graves primero.
- Cada violación: UNA frase concreta y accionable citando la función afectada,
  para que un programador pueda corregirla sin más contexto.

Devuelve SOLO JSON válido (sin markdown):
{"violations": ["..."]}
Lista vacía si el código cumple el prompt.
"""


def run_qa(user_prompt: str, main_c: str, settings) -> list[str]:
    """Review main_c against user_prompt. Returns violated requirements.

    Never raises: on any LLM/parse failure returns [] so the pipeline is not
    blocked by the QA stage itself.
    """
    if not user_prompt.strip() or not main_c.strip():
        return []

    env = _read_env()
    try:
        llm, label = _build_worker_llm(env)
    except RuntimeError as exc:
        logger.warning("[QA] no LLM configured (%s) — skipping QA", exc)
        return []

    print(f"\n{_B}{_W}╔══ QA REVIEW ═════════════════════════════════════════════════╗{_RS}")
    print(f"{_B}{_W}║  contrastando src/main.c contra el prompt original{_RS}")
    print(f"{_B}{_W}╚══════════════════════════════════════════════════════════════╝{_RS}")
    print(f"{_Y}  [QA] [{label}]  revisando …{_RS}")

    sys_esc = QA_SYSTEM_PROMPT.replace("{", "{{").replace("}", "}}")
    prompt = ChatPromptTemplate.from_messages([
        ("system", sys_esc),
        ("user", "=== PROMPT ORIGINAL DEL USUARIO ===\n{user_prompt}\n\n"
                 "=== src/main.c FINAL ===\n{code}"),
    ])
    chain = prompt | llm | StrOutputParser() | _parse_output

    try:
        raw = chain.invoke({"user_prompt": user_prompt, "code": main_c})
    except Exception as exc:
        logger.warning("[QA] review failed (%s) — skipping QA", exc)
        print(f"{_Y}  [QA] no disponible ({exc.__class__.__name__}) — continuando sin QA{_RS}")
        return []

    violations = raw.get("violations") if isinstance(raw, dict) else None
    if not isinstance(violations, list):
        return []
    cleaned = [str(v).strip() for v in violations if str(v).strip()][:_MAX_VIOLATIONS]

    if cleaned:
        print(f"{_Y}{_W}  [QA] {len(cleaned)} requisito(s) del prompt incumplido(s):{_RS}")
        for v in cleaned:
            print(f"     {_R}✗{_RS} {v[:110]}")
    else:
        print(f"{_G}{_W}  [QA] ✓ el código cumple el prompt{_RS}")
    return cleaned
