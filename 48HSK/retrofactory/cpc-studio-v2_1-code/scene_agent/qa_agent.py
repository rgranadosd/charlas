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
  * mandatos del prompt marcados como EXACTLY / MUST / NEVER / ONCE;
  * ELEMENTOS INVENTADOS: cualquier elemento visual (etiquetas, textos, contadores,
    decoración) que el prompt NO pide dibujar es una violación — aunque parezca
    una mejora;
  * SOLAPAMIENTOS de coordenadas: en Mode 0 cada carácter ocupa 4 bytes de x, así
    que un string de N caracteres en x ocupa de x a x+4N-1. Dos draws en la misma
    fila cuyos rangos se crucen se pisan en pantalla — violación.
- ANCLAJE OBLIGATORIO: cada violación debe terminar citando entre comillas el
  fragmento del prompt que se incumple, o la marca [NO SOLICITADO] si es un
  elemento inventado, o [SOLAPAMIENTO x=A..B vs x=C..D] si es colisión de
  coordenadas. Si no puedes anclarla a ninguna de las tres, NO la reportes.
- Máximo 5 violaciones, las más graves primero.
- Cada violación: UNA frase concreta y accionable citando la función afectada,
  para que un programador pueda corregirla sin más contexto.

Devuelve SOLO JSON válido (sin markdown):
{"violations": ["..."]}
Lista vacía si el código cumple el prompt.
"""


QA_VERIFIER_PROMPT = """Eres un verificador ESCÉPTICO de hallazgos de QA.
Recibes el PROMPT ORIGINAL (la especificación) y una lista numerada de supuestas
violaciones, cada una con su ancla (cita del prompt, [NO SOLICITADO] o
[SOLAPAMIENTO]).

Para cada una decide si es REAL:
- Si el ancla es una cita: ¿esa frase del prompt realmente exige lo que la
  violación afirma? Una cita que habla de OTRA cosa (otro elemento, otra
  función) NO sostiene la violación → descártala.
- Si es [NO SOLICITADO]: ¿de verdad el prompt no pide ese elemento en ninguna
  parte? Si el prompt lo menciona como algo a mostrar, descártala.
- Si es [SOLAPAMIENTO]: ¿los rangos de x calculados (4 bytes por carácter en
  Mode 0) realmente se cruzan en la misma fila?
- En caso de duda, DESCARTA: un falso positivo provoca correcciones que rompen
  código correcto, que es peor que dejar pasar un hallazgo dudoso.

Devuelve SOLO JSON válido (sin markdown), razonando ANTES de decidir cada una:
{"verdicts": [{"i": 0, "ancla_dice": "qué exige realmente la frase citada",
               "violacion_afirma": "qué reclama la violación", "real": true}]}
"real" es true SOLO si lo que el ancla exige coincide con lo que la violación
afirma sobre EL MISMO elemento. Cita sobre la bola usada para quejarse de los
ladrillos → real: false.
"""


def _build_verifier_llm(env: dict[str, str]):
    """A stronger reasoner than the finder: judging citations needs judgment."""
    from langchain_openai import ChatOpenAI
    key = env.get("MISTRAL_ORCHESTRATOR_API_KEY") or env.get("MISTRAL_API_KEY") \
        or env.get("MISTRAL_WORKER_API_KEY", "")
    if not key:
        return None
    return ChatOpenAI(
        model=env.get("MISTRAL_ORCHESTRATOR_MODEL", "mistral-large-latest"),
        temperature=0,
        openai_api_base=env.get("MISTRAL_BASE_URL", "https://api.mistral.ai/v1"),
        openai_api_key=key,
        timeout=90,
        max_retries=0,
    )


def _verify_violations(env: dict[str, str], user_prompt: str, violations: list[str]) -> list[str]:
    """Second adversarial pass: drop findings whose anchor doesn't hold up."""
    llm = _build_verifier_llm(env)
    if llm is None:
        return violations
    numbered = "\n".join(f"[{i}] {v}" for i, v in enumerate(violations))
    sys_esc = QA_VERIFIER_PROMPT.replace("{", "{{").replace("}", "}}")
    prompt = ChatPromptTemplate.from_messages([
        ("system", sys_esc),
        ("user", "=== PROMPT ORIGINAL ===\n{user_prompt}\n\n=== VIOLACIONES ===\n{violations}"),
    ])
    chain = prompt | llm | StrOutputParser() | _parse_output
    try:
        raw = chain.invoke({"user_prompt": user_prompt, "violations": numbered})
        verdicts = raw.get("verdicts") if isinstance(raw, dict) else None
        if not isinstance(verdicts, list):
            return violations
        keep_idx = {int(v["i"]) for v in verdicts
                    if isinstance(v, dict) and v.get("real") is True and str(v.get("i", "")).isdigit()}
        kept = [violations[i] for i in sorted(keep_idx) if i < len(violations)]
        dropped = len(violations) - len(kept)
        if dropped:
            print(f"{_DIM}  [QA verify] descartadas {dropped} violación(es) sin ancla válida{_RS}")
        return kept
    except Exception as exc:
        logger.warning("[QA] verifier failed (%s) — keeping unverified findings", exc)
        return violations


def run_qa(user_prompt: str, main_c: str, settings) -> list[str]:
    """Review main_c against user_prompt. Returns violated requirements.

    Two passes: a finder (against the prompt) and a skeptical verifier that
    drops findings whose prompt anchor doesn't actually support them.
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
        cleaned = _verify_violations(env, user_prompt, cleaned)

    if cleaned:
        print(f"{_Y}{_W}  [QA] {len(cleaned)} requisito(s) del prompt incumplido(s):{_RS}")
        for v in cleaned:
            print(f"     {_R}✗{_RS} {v[:110]}")
    else:
        print(f"{_G}{_W}  [QA] ✓ el código cumple el prompt{_RS}")
    return cleaned
