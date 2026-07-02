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
import re

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from common.llm_utils import _parse_output, _read_env, _resolve_amp_llm_gateway, build_amp_gateway_chat

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

Método (en este orden):
1. PRIMERO: localiza cada bloque del prompt marcado MANDATORY / EXACTLY /
   "follow exactly" y compáralo LÍNEA A LÍNEA con su implementación. Reporta
   tanto pasos omitidos como pasos AÑADIDOS que el prompt no especifica
   (reposiciones de coordenadas tras colisión, ajustes, efectos extra).
2. Después aplica el resto de criterios de atención.

Reglas:
- Solo violaciones verificables leyendo el código (estructura, llamadas, orden de
  ejecución). Nada de estilo, micro-optimizaciones ni mejoras opcionales.
- Antes de afirmar que algo FALTA en el código, búscalo en TODO el fichero: una
  queja sobre código inexistente que sí existe invalida toda tu revisión.
- Presta especial atención a:
  * qué se dibuja en init vs. en el bucle principal (el decorado estático y las
    etiquetas/valores iniciales del HUD deben pintarse UNA vez en init);
  * redibujados completos de escena dentro del bucle (matan el rendimiento en un
    Z80 a 4MHz — solo las entidades móviles usan erase/draw por frame);
  * mandatos del prompt marcados como EXACTLY / MUST / NEVER / ONCE;
  * ELEMENTOS INVENTADOS: cualquier elemento visual (etiquetas, textos, contadores,
    decoración) que el prompt NO pide dibujar es una violación — aunque parezca
    una mejora;
  * COMPORTAMIENTO INVENTADO: cuando el prompt define una operación como secuencia
    exacta (MANDATORY / EXACTLY / "follow exactly"), el código no debe AÑADIR pasos
    extra (reposiciones de coordenadas, ajustes, efectos colaterales) ni omitir los
    especificados. Un paso añadido a una secuencia mandatoria es violación
    [NO SOLICITADO] aunque parezca razonable — las reposiciones de posición tras una
    colisión son el caso típico y causan túneles y reacciones en cadena;
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

Recibes también el CÓDIGO revisado. Para cada violación decide si es REAL con
DOS comprobaciones obligatorias:
A. ¿Es CIERTA sobre el código? Busca en el código: si la violación dice que
   falta algo que SÍ está (un goto, una llamada, una condición) o que existe
   algo que NO está, es falsa → descártala.
B. ¿El ancla la sostiene?
   - Cita del prompt: ¿esa frase realmente exige lo que la violación afirma?
     Una cita que habla de OTRA cosa (otro elemento, otra función) NO la
     sostiene → descártala.
   - [NO SOLICITADO]: ¿de verdad el prompt no pide ese elemento o paso en
     ninguna parte? Si el prompt lo menciona, descártala.
   - [SOLAPAMIENTO]: ¿los rangos de x calculados (4 bytes por carácter en
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


# Strong requirement markers — game-agnostic: they're a writing convention in
# the prompt, not domain rules. A line carrying one of these is a checkable item.
_MARK_RE = re.compile(
    r"\b(MANDATORY|EXACTLY|MUST|NEVER|ONCE|FORBIDDEN|AT MOST|follow exactly)\b",
    re.IGNORECASE,
)
_SECTION_RE = re.compile(r"^\s*\d+\.\s")          # "3. PHYSICS ..."  section header
_MAX_CHECKLIST = 20


def _extract_checkable_items(user_prompt: str) -> list[str]:
    """Mechanically pull the prompt's checkable requirements — game-agnostic.

    Two sources, both convention-based (no game knowledge):
      (a) every bullet under an INVARIANTS section (the user's distilled,
          code-checkable assertions);
      (b) any other bullet/line carrying a strong marker (MANDATORY/MUST/
          NEVER/EXACTLY/ONCE/FORBIDDEN/AT MOST).
    Section headers themselves are skipped (the bullets under them are the rules).
    """
    lines = user_prompt.splitlines()
    items: list[str] = []

    in_invariants = False
    for ln in lines:
        if _SECTION_RE.match(ln):
            in_invariants = bool(re.search(r"INVARIANT", ln, re.IGNORECASE))
            continue
        if in_invariants:
            s = ln.strip().lstrip("-•").strip()
            if len(s) > 12:
                items.append(s)

    for ln in lines:
        if _SECTION_RE.match(ln):
            continue
        s = ln.strip()
        if _MARK_RE.search(s):
            s = s.lstrip("-•").strip()
            if len(s) > 12:
                items.append(s)

    seen: set[str] = set()
    unique: list[str] = []
    for it in items:
        key = it[:90]
        if key not in seen:
            seen.add(key)
            unique.append(it)
    return unique[:_MAX_CHECKLIST]


QA_CHECKLIST_PROMPT = """Eres un auditor de conformidad de código CPCtelera.
Recibes (1) una CHECKLIST NUMERADA de requisitos extraídos del prompt del
usuario y (2) el src/main.c final.

Tu tarea: para CADA ítem de la checklist —sin saltarte NINGUNO— determina si el
código lo CUMPLE o lo INCUMPLE, leyendo el código.

Reglas de juicio:
- Decide leyendo el código real: estructura, llamadas, orden, condiciones.
- Antes de decir que algo FALTA, búscalo en TODO el fichero.
- Si el ítem prohíbe algo ("NEVER", "FORBIDDEN", "ADD NOTHING ELSE"), incumple
  si el código LO HACE.
- Si el ítem exige algo ("MUST", "ONCE", "AT MOST ONE", "EXACTLY"), incumple si
  el código NO lo hace o lo hace de más.
- En caso de duda razonable, marca cumple=true (no inventes fallos).

DEBES devolver un veredicto por CADA índice de la checklist. SOLO JSON válido:
{"verdicts": [{"i": 0, "cumple": true, "motivo": "una frase con la evidencia en el código"}]}
"""


def _checklist_audit(env: dict[str, str], user_prompt: str, main_c: str) -> list[str]:
    """Closed-checklist conformance pass.

    Instead of an open 'find violations' question (which skips items), we extract
    every marked requirement and force a verdict per item. Coverage is guaranteed
    by enumerating the checklist, not by any per-game rule.
    """
    items = _extract_checkable_items(user_prompt)
    if not items:
        return []
    llm = _build_verifier_llm(env)  # meticulous reasoner
    if llm is None:
        return []

    numbered = "\n".join(f"[{i}] {it}" for i, it in enumerate(items))
    sys_esc = QA_CHECKLIST_PROMPT.replace("{", "{{").replace("}", "}}")
    prompt = ChatPromptTemplate.from_messages([
        ("system", sys_esc),
        ("user", "=== CHECKLIST ({n} ítems — responde a TODOS) ===\n{checklist}\n\n"
                 "=== src/main.c ===\n{code}"),
    ])
    chain = prompt | llm | StrOutputParser() | _parse_output
    print(f"{_DIM}  [QA checklist] {len(items)} requisitos marcados extraídos del prompt{_RS}")
    try:
        raw = chain.invoke({"n": len(items), "checklist": numbered, "code": main_c})
    except Exception as exc:
        logger.warning("[QA] checklist audit failed (%s) — skipping", exc)
        return []

    verdicts = raw.get("verdicts") if isinstance(raw, dict) else None
    if not isinstance(verdicts, list):
        return []

    failed: list[str] = []
    judged: set[int] = set()
    for v in verdicts:
        if not isinstance(v, dict):
            continue
        try:
            idx = int(v.get("i"))
        except (TypeError, ValueError):
            continue
        judged.add(idx)
        if v.get("cumple") is False and 0 <= idx < len(items):
            motivo = str(v.get("motivo", "")).strip()
            failed.append(f"INCUMPLE: {items[idx]}" + (f" — {motivo}" if motivo else ""))

    # Items the auditor silently skipped are coverage gaps — surface them.
    missed = [i for i in range(len(items)) if i not in judged]
    if missed:
        logger.warning("[QA] checklist: %d ítem(s) sin veredicto", len(missed))
    return failed


def _build_verifier_llm(env: dict[str, str]):
    """A stronger reasoner than the finder: judging citations needs judgment.

    Priority: AMP gateway → Mistral direct → None (QA verifier is skipped).
    Model: QA_MODEL → AMP_GENAI_MODEL → mistral-large-latest.
    """
    from langchain_openai import ChatOpenAI
    model = env.get("QA_MODEL", "").strip() or env.get("AMP_GENAI_MODEL", "").strip() or "mistral-large-latest"
    if "/" in model:
        model = model.split("/", 1)[1]

    gateway = _resolve_amp_llm_gateway(env)
    if gateway:
        return build_amp_gateway_chat(gateway, model=model, env=env, timeout=90)

    key = env.get("MISTRAL_ORCHESTRATOR_API_KEY") or env.get("MISTRAL_API_KEY") \
        or env.get("MISTRAL_WORKER_API_KEY", "")
    if not key:
        return None
    return ChatOpenAI(
        model=model, temperature=0,
        openai_api_base=env.get("MISTRAL_BASE_URL", "https://api.mistral.ai/v1"),
        openai_api_key=key,
        default_headers={"API-Key": key},
        timeout=90,
        max_retries=0,
    )


def _build_qa_llm(env: dict[str, str]) -> tuple:
    """Build the primary QA LLM (finder pass). Returns (llm, label).

    Priority: AMP gateway → Mistral direct → RuntimeError.
    Model: QA_MODEL → AMP_GENAI_MODEL → codestral-latest.
    """
    from langchain_openai import ChatOpenAI
    model = env.get("QA_MODEL", "").strip() or env.get("AMP_GENAI_MODEL", "").strip() or "codestral-latest"
    if "/" in model:
        model = model.split("/", 1)[1]

    gateway = _resolve_amp_llm_gateway(env)
    if gateway:
        llm = build_amp_gateway_chat(gateway, model=model, env=env, timeout=90)
        return llm, f"AMP-GATEWAY/{model}"

    key = env.get("MISTRAL_ORCHESTRATOR_API_KEY") or env.get("MISTRAL_API_KEY") \
        or env.get("MISTRAL_WORKER_API_KEY", "")
    if key:
        llm = ChatOpenAI(
            model=model, temperature=0,
            openai_api_base=env.get("MISTRAL_BASE_URL", "https://api.mistral.ai/v1"),
            openai_api_key=key,
            default_headers={"API-Key": key},
            timeout=90,
            max_retries=0,
        )
        return llm, f"MISTRAL/{model}"

    raise RuntimeError(
        "No QA LLM configured. Attach an LLM provider in Agent Manager "
        "(or set AMP_LLM_URL/AMP_LLM_API_KEY), or set MISTRAL_API_KEY for local dev."
    )


def _verify_violations(env: dict[str, str], user_prompt: str, main_c: str, violations: list[str]) -> list[str]:
    """Second adversarial pass: drop findings whose anchor doesn't hold up
    against the prompt OR whose claim is factually false about the code."""
    llm = _build_verifier_llm(env)
    if llm is None:
        return violations
    numbered = "\n".join(f"[{i}] {v}" for i, v in enumerate(violations))
    sys_esc = QA_VERIFIER_PROMPT.replace("{", "{{").replace("}", "}}")
    prompt = ChatPromptTemplate.from_messages([
        ("system", sys_esc),
        ("user", "=== PROMPT ORIGINAL ===\n{user_prompt}\n\n"
                 "=== CÓDIGO REVISADO ===\n{code}\n\n"
                 "=== VIOLACIONES ===\n{violations}"),
    ])
    chain = prompt | llm | StrOutputParser() | _parse_output
    try:
        raw = chain.invoke({"user_prompt": user_prompt, "code": main_c, "violations": numbered})
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
        llm, label = _build_qa_llm(env)
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
    # Closed-checklist conformance audit: enumerate every marked requirement in
    # the prompt and force a verdict per item, so nothing gets silently skipped.
    checklist_fails = _checklist_audit(env, user_prompt, main_c)
    # Checklist failures are anchored by construction (they ARE prompt items), so
    # only the open-ended finder's hits go through the skeptical verifier.
    if cleaned:
        cleaned = _verify_violations(env, user_prompt, main_c, cleaned)
    # Checklist items first — they're the user-marked critical requirements.
    cleaned = (checklist_fails + cleaned)[:_MAX_VIOLATIONS]

    if cleaned:
        print(f"{_Y}{_W}  [QA] {len(cleaned)} requisito(s) del prompt incumplido(s):{_RS}")
        for v in cleaned:
            print(f"     {_R}✗{_RS} {v[:110]}")
    else:
        print(f"{_G}{_W}  [QA] ✓ el código cumple el prompt{_RS}")
    return cleaned
