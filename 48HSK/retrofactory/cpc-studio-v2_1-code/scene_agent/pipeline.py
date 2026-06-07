"""End-to-end pipeline: prompt → orchestrator → developer agent → compile → emulator.

Flow:
  1. orchestrate(prompt)          → OrchestratorContract  (WHAT)
  2. topological_sort(tasks)      → ordered list
  3. for each task → _dispatch_graph (LangGraph):
       route → developer_node | audio_node → DevelopmentOutput
       write files_to_write → run_dir/src/main.c …
       pass current code as ctx  → next task sees accumulated state
  4. _fix_graph (LangGraph cycle):
       compile → (errors?) → fix_agent → compile → … → OK
  5. _launch_emulator(dsk)        → Caprice32

Usage:
    python -m scene_agent.pipeline "breakout WSO2 with score and lives"
    python -m scene_agent.pipeline "hud_only add score and lives counters" --no-emu
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, TypedDict

from langgraph.graph import StateGraph, END

from .build_and_run import _launch_emulator, _new_run_dir, _scaffold, _CPCTELERA_ROOT
from .code_guard import auto_fix as _guard_auto_fix, check as _guard_check
from .contracts import DevelopmentInput, DevelopmentOutput, OrchestratorContract, TaskDef
from .developer_agent import run_task, input_from_taskdef
from .audio_agent import run_audio_task
from .orchestrator_agent import orchestrate

logger = logging.getLogger(__name__)

_G   = "\033[32m"
_Y   = "\033[33m"
_R   = "\033[31m"
_B   = "\033[36m"
_W   = "\033[1m"
_DIM = "\033[2m"
_RS  = "\033[0m"


_MAX_FIX_ATTEMPTS = 3


def _shorten(text: str, limit: int = 1200) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[:limit] + "\n...[truncated]"


def _format_llm_exception(exc: Exception) -> str:
    """Extract useful provider diagnostics from nested exception objects."""
    lines: list[str] = []
    seen: set[int] = set()
    cur: BaseException | None = exc
    level = 0

    while cur is not None and id(cur) not in seen and level < 4:
        seen.add(id(cur))
        prefix = f"cause[{level}]"
        lines.append(f"{prefix}: {cur.__class__.__name__}: {cur}")

        # Common OpenAI/httpx/requests style payloads
        status_code = getattr(cur, "status_code", None)
        body = getattr(cur, "body", None)
        response = getattr(cur, "response", None)

        if status_code is not None:
            lines.append(f"{prefix}.status_code: {status_code}")

        if body:
            try:
                body_text = body if isinstance(body, str) else json.dumps(body, ensure_ascii=False)
                lines.append(f"{prefix}.body:\n{_shorten(body_text)}")
            except Exception:
                lines.append(f"{prefix}.body: {body}")

        if response is not None:
            resp_status = getattr(response, "status_code", None)
            if resp_status is not None:
                lines.append(f"{prefix}.response.status_code: {resp_status}")

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
                        resp_text = json.dumps(resp_json, ensure_ascii=False)
                except Exception:
                    resp_text = None

            if resp_text:
                lines.append(f"{prefix}.response.body:\n{_shorten(resp_text)}")

        nxt = cur.__cause__ or cur.__context__
        if nxt is cur:
            break
        cur = nxt
        level += 1

    return "\n".join(lines)


def _print_llm_failure(stage: str, exc: Exception) -> None:
    print(f"\n{_R}{_W}════════════════ LLM FAILURE [{stage}] ════════════════{_RS}")
    print(f"{_R}{_format_llm_exception(exc)}{_RS}")
    print(f"{_R}{_W}══════════════════════════════════════════════════════{_RS}")


# ---------------------------------------------------------------------------
# Compile with error capture
# ---------------------------------------------------------------------------

def _compile_with_errors(run_dir: Path) -> tuple[bool, str]:
    """Run make and return (success, error_text)."""
    cpct_path = str(_CPCTELERA_ROOT.resolve())
    env = {**os.environ, "CPCT_PATH": cpct_path}
    print(f"\n{_G}{_W}══════════════════════════════════════════════════════════{_RS}")
    print(f"{_G}{_W}  BUILD  make -C {run_dir.name}{_RS}")
    print(f"{_G}{_W}══════════════════════════════════════════════════════════{_RS}")
    result = subprocess.run(
        ["make", "-C", str(run_dir.resolve())],
        capture_output=True, text=True, env=env, timeout=120,
    )
    if result.returncode == 0:
        print(f"{_G}  ✓ compilación OK{_RS}")
        for dsk in run_dir.glob("*.dsk"):
            print(f"{_G}  ✓ DSK: {dsk.name}{_RS}")
        return True, ""
    errors = (result.stderr + result.stdout)[:1200]
    print(f"{_R}  ✗ FAILED (rc={result.returncode})\n{errors}{_RS}")
    return False, errors


# ---------------------------------------------------------------------------
# Audio scaffold — fixed templates, no LLM needed
# ---------------------------------------------------------------------------

_AUDIO_H = """\
#ifndef AUDIO_H
#define AUDIO_H
#include <cpctelera.h>

#define SFX_WALL_HIT       0
#define SFX_PADDLE_HIT     1
#define SFX_BRICK_HIT      2
#define SFX_LIFE_LOST      3
#define SFX_GAME_OVER      4
#define SFX_LEVEL_COMPLETE 4

void audio_init(void);
void audio_update(void);
void audio_play_sfx(u8 sfx_id);

#endif /* AUDIO_H */
"""

_AUDIO_C = """\
/* audio.c — Phase 2: direct AY-3-8912 access via Z80 inline assembly.
   CPC AY ports: BC=0xF400 to latch register, BC=0xF600 to write value.
   __sfr __at(0xFx) is WRONG (generates OUT (N),A using A as port high byte).
   Correct approach: OUT (c),A with BC=16-bit port address. */
#include "audio.h"

/* Global relay vars — avoids SDCC Z80 calling-convention issues in inline asm */
static u8 g_ay_reg;
static u8 g_ay_dat;
static u8 g_sfx_timer;

static void ay_write_hw(void) {
    __asm
        ; Phase 1 — latch register address: BDIR=1, BC1=1
        ld  a, (_g_ay_reg)
        ld  bc, #0xF4FF     ; PPI Port A (AY data bus)
        out (c), a           ; put register number on bus
        ld  b, #0xF6
        ld  a, #0xC0         ; BDIR=1 (bit7), BC1=1 (bit6) = LATCH ADDRESS
        out (c), a
        ld  a, #0x40         ; BDIR=0 = inactive
        out (c), a
        ; Phase 2 — write data: BDIR=1, BC1=0
        ld  a, (_g_ay_dat)
        ld  bc, #0xF4FF     ; PPI Port A
        out (c), a           ; put data value on bus
        ld  b, #0xF6
        ld  a, #0x80         ; BDIR=1 (bit7), BC1=0 (bit6) = WRITE DATA
        out (c), a
        ld  a, #0x40         ; BDIR=0 = inactive
        out (c), a
    __endasm;
}

#define AY(r, v) do { g_ay_reg = (r); g_ay_dat = (v); ay_write_hw(); } while(0)

void audio_init(void) {
    g_sfx_timer = 0;
    AY(7,  0x3F);  /* mixer: silence all */
    AY(8,  0);     /* channel A volume = 0 */
    AY(9,  0);     /* channel B volume = 0 */
    AY(10, 0);     /* channel C volume = 0 */
}

void audio_update(void) {
    if (g_sfx_timer > 0) {
        g_sfx_timer--;
        if (g_sfx_timer == 0) {
            AY(8, 0);       /* silence channel A */
            AY(7, 0x3F);    /* mixer off */
        }
    }
}

void audio_play_sfx(u8 sfx_id) {
    u8 period_lo, duration;
    switch (sfx_id) {
        case SFX_WALL_HIT:   period_lo = 0x23; duration = 4;  break;
        case SFX_PADDLE_HIT: period_lo = 0x47; duration = 6;  break;
        case SFX_BRICK_HIT:  period_lo = 0x8E; duration = 5;  break;
        case SFX_LIFE_LOST:  period_lo = 0xFF; duration = 20; break;
        case SFX_GAME_OVER:  period_lo = 0xCC; duration = 40; break;
        default: return;
    }
    AY(0, period_lo);  /* tone period channel A low */
    AY(1, 0);          /* tone period channel A high */
    AY(7, 0x3E);       /* enable tone on channel A */
    AY(8, 12);         /* channel A volume */
    g_sfx_timer = duration;
}
"""


def _scaffold_audio(run_dir: Path) -> None:
    """Write fixed audio.h and audio.c templates — no LLM needed."""
    (run_dir / "src" / "audio.h").write_text(_AUDIO_H, encoding="utf-8")
    (run_dir / "src" / "audio.c").write_text(_AUDIO_C, encoding="utf-8")
    print(f"{_G}  ✓ audio scaffold → src/audio.h + src/audio.c{_RS}")


# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# File writing
# ---------------------------------------------------------------------------

def _write_patch(run_dir: Path, path: str, content: str, mode: str) -> None:
    target = run_dir / path
    target.parent.mkdir(parents=True, exist_ok=True)
    if mode == "append" and target.exists():
        target.write_text(target.read_text(encoding="utf-8") + "\n" + content, encoding="utf-8")
    else:
        target.write_text(content, encoding="utf-8")



# ---------------------------------------------------------------------------
# Task routing — LangGraph conditional dispatch: developer | audio
# ---------------------------------------------------------------------------

class _DispatchState(TypedDict):
    task:      TaskDef
    dev_input: DevelopmentInput
    settings:  Any
    output:    DevelopmentOutput | None


def _route_task(state: _DispatchState) -> str:
    return "audio" if getattr(state["task"], "agent_type", "") == "audio_c_agent" else "developer"


def _developer_node(state: _DispatchState) -> dict:
    return {"output": run_task(state["dev_input"], state["settings"])}


def _audio_node(state: _DispatchState) -> dict:
    print(f"  {_G}✓ audio scaffold already applied — skipping LLM for audio task{_RS}")
    return {"output": DevelopmentOutput(
        task_id=state["dev_input"].task_id,
        status="done",
        summary="Audio handled by scaffold (audio.h + audio.c already written).",
        files_to_write=[],
    )}


def _build_dispatch_graph():
    g = StateGraph(_DispatchState)
    g.add_node("developer", _developer_node)
    g.add_node("audio",     _audio_node)
    g.set_entry_point("developer")  # overridden by conditional below
    g.add_conditional_edges("__start__", _route_task, {"developer": "developer", "audio": "audio"})
    g.add_edge("developer", END)
    g.add_edge("audio", END)
    return g.compile()


_dispatch_graph = _build_dispatch_graph()


def _dispatch_task(task: TaskDef, dev_input: DevelopmentInput, settings: Any) -> DevelopmentOutput:
    return _dispatch_graph.invoke(
        {"task": task, "dev_input": dev_input, "settings": settings, "output": None}
    )["output"]


# ---------------------------------------------------------------------------
# Task ordering
# ---------------------------------------------------------------------------

def _topological_sort(tasks: list[TaskDef]) -> list[TaskDef]:
    completed: set[str] = set()
    ordered:   list[TaskDef] = []
    remaining  = list(tasks)
    for _ in range(len(tasks) ** 2 + 1):
        if not remaining:
            break
        for task in remaining[:]:
            if all(dep in completed for dep in task.depends_on):
                ordered.append(task)
                completed.add(task.task_id)
                remaining.remove(task)
    for task in remaining:
        logger.warning("[PIPE] %s has unresolvable deps %s — appending last", task.task_id, task.depends_on)
        ordered.append(task)
    return ordered


# ---------------------------------------------------------------------------
# Fix loop — LangGraph cycle: compile → (errors?) → fix → compile → …
# ---------------------------------------------------------------------------

class _FixState(TypedDict):
    run_dir:      Path
    project_name: str
    settings:     Any
    current_code: dict[str, str]
    compile_ok:   bool
    errors:       str
    guard_errors: list[str]
    fix_attempt:  int


def _compile_node(state: _FixState) -> _FixState:
    main_c = state["current_code"].get("src/main.c", "")
    guard_result = _guard_check(main_c) if main_c else None
    guard_errors = guard_result.errors if guard_result and not guard_result.ok else []
    if guard_errors:
        print(f"{_Y}  ⚠  CODE GUARD: {len(guard_errors)} error(es) semántico(s) detectado(s){_RS}")
        for _ge in guard_errors:
            print(f"     {_R}✗{_RS} {_ge[:120]}")
    compile_ok, errors = _compile_with_errors(state["run_dir"])
    return {**state, "compile_ok": compile_ok, "errors": errors, "guard_errors": guard_errors}


def _fix_node(state: _FixState) -> _FixState:
    fix_attempt  = state["fix_attempt"] + 1
    fix_id       = f"FIX_{fix_attempt:02d}"
    current_code = dict(state["current_code"])
    errors       = state["errors"]
    guard_errors = state["guard_errors"]

    print(f"\n{_Y}{_W}  ── Corrección {fix_attempt}/{_MAX_FIX_ATTEMPTS} [{fix_id}] ──────────────────────────{_RS}")
    fix_input = DevelopmentInput(
        task_id=fix_id,
        project_name=state["project_name"],
        goal="Corregir todos los errores de compilación en src/main.c",
        context=[
            f"ESTADO ACTUAL src/main.c (DEBES incluir todo y solo corregir los errores):\n"
            f"{current_code.get('src/main.c', '')}",
            f"ERRORES DEL COMPILADOR SDCC:\n{errors}" if errors else "Sin errores de compilador.",
            *([
                f"ERRORES SEMÁNTICOS (code guard — deben corregirse aunque compile):\n"
                + "\n".join(guard_errors)
            ] if guard_errors else []),
        ],
        acceptance_criteria=["make termina con rc=0 sin errores"],
        constraints=[
            "C89/SDCC — declara TODAS las variables antes de cualquier sentencia",
            "No stdio.h, stdlib.h, printf, puts",
            "Solo CPCtelera API — <cpctelera.h>",
            "No uses funciones que no existan en CPCtelera (ej: cpct_setPaletteFromGIMP no existe)",
            "Mode 0 pen bytes (ambos píxeles = pen N): pen0=0x00 pen1=0xC0 pen2=0x0C pen3=0xCC. JAMÁS uses 0x03 (=pen 8) ni 0x0F (=pen 10) con paleta de 4 entradas — se renderizan INVISIBLES.",
            "Entrega el archivo src/main.c COMPLETO y corregido",
        ],
        target_files=["src/main.c"],
    )
    try:
        fix_output = run_task(fix_input, state["settings"])
    except Exception as exc:
        _print_llm_failure(f"FIX_WORKER:{fix_id}", exc)
        # Force exit on exception — set attempt to max
        return {**state, "fix_attempt": _MAX_FIX_ATTEMPTS}

    if fix_output.status == "done" and fix_output.files_to_write:
        for fp in fix_output.files_to_write:
            content = _guard_auto_fix(fp.content) if fp.path.endswith(".c") else fp.content
            lines = content.count("\n") + 1
            if lines < 20:
                print(f"  {_Y}  ⚠ [{fix_id}] output sospechoso ({lines} líneas) — descartando{_RS}")
                continue
            _write_patch(state["run_dir"], fp.path, content, fp.mode)
            current_code[fp.path] = content
            print(f"  {_G}✎  {fp.path}{_RS}  ({lines} líneas corregidas)")
    else:
        print(f"  {_R}  fix agent devolvió {fix_output.status} — abortando{_RS}")
        # Force exit — no point retrying if agent can't produce output
        return {**state, "fix_attempt": _MAX_FIX_ATTEMPTS, "current_code": current_code}

    return {**state, "fix_attempt": fix_attempt, "current_code": current_code}


def _route_after_compile(state: _FixState) -> str:
    if state["compile_ok"] and not state["guard_errors"]:
        return "end"
    if state["fix_attempt"] >= _MAX_FIX_ATTEMPTS:
        print(f"{_R}  ✗ máximo de intentos de corrección alcanzado ({_MAX_FIX_ATTEMPTS}){_RS}")
        return "end"
    return "fix"


def _build_fix_graph():
    g = StateGraph(_FixState)
    g.add_node("compile", _compile_node)
    g.add_node("fix", _fix_node)
    g.set_entry_point("compile")
    g.add_conditional_edges("compile", _route_after_compile, {"end": END, "fix": "fix"})
    g.add_edge("fix", "compile")
    return g.compile()


_fix_graph = _build_fix_graph()


def _run_fix_loop(
    run_dir:      Path,
    project_name: str,
    settings:     Any,
    current_code: dict[str, str],
) -> tuple[bool, dict[str, str]]:
    """Execute the compile→fix cycle via LangGraph. Returns (compile_ok, updated_code)."""
    final = _fix_graph.invoke({
        "run_dir":      run_dir,
        "project_name": project_name,
        "settings":     settings,
        "current_code": current_code,
        "compile_ok":   False,
        "errors":       "",
        "guard_errors": [],
        "fix_attempt":  0,
    })
    return final["compile_ok"], final["current_code"]


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run_pipeline(
    prompt:       str,
    project_name: str,
    settings,
    no_emu:       bool = False,
    dry_run:      bool = False,
) -> tuple[Path, bool]:
    """Execute full pipeline. Returns (run_dir, compile_ok)."""

    print(f"\n{_B}{_W}{'═'*62}{_RS}")
    print(f"{_B}{_W}  PIPELINE  {project_name}{_RS}")
    print(f"{_B}{_W}{'═'*62}{_RS}")

    # 1. Orchestrate ────────────────────────────────────────────────
    try:
        contract: OrchestratorContract = orchestrate(prompt, project_name, settings)
    except Exception as exc:
        _print_llm_failure("ORCHESTRATOR", exc)
        raise

    # 2. Scaffold run directory ─────────────────────────────────────
    run_dir = _new_run_dir()
    _scaffold(run_dir)
    _scaffold_audio(run_dir)  # write fixed audio.h + audio.c before any task runs
    print(f"\n{_DIM}  run_dir : {run_dir}{_RS}")

    # Save contract for debugging
    (run_dir / "orchestrator_contract.json").write_text(
        contract.model_dump_json(indent=2), encoding="utf-8"
    )

    if dry_run:
        print(f"{_Y}  [DRY-RUN] stopping before developer agent{_RS}")
        return run_dir, False

    # 3. Execute tasks ──────────────────────────────────────────────
    ordered = _topological_sort(contract.tasks)
    completed:    dict[str, object] = {}
    current_code: dict[str, str]   = {}

    print(f"\n{_W}  Tareas a ejecutar: {len(ordered)}{_RS}")
    for t in ordered:
        deps = f"  deps={t.depends_on}" if t.depends_on else ""
        print(f"  {_B}[{t.task_id}]{_RS} p{t.priority}  {t.title[:55]}{deps}")
    print()

    total_tasks = len(ordered)
    for task_idx, task in enumerate(ordered, start=1):
        print(f"\n{_B}{_W}── Etapa {task_idx}/{total_tasks}: [{task.task_id}] {task.title[:50]} ──{_RS}")

        unmet = [d for d in task.depends_on if d not in completed]
        if unmet:
            print(f"{_Y}  ⏭  [{task.task_id}] saltado — deps sin completar: {unmet}{_RS}")
            continue

        dev_input: DevelopmentInput = input_from_taskdef(task, project_name)
        if current_code.get("src/main.c"):
            dev_input = dev_input.model_copy(update={
                "context": dev_input.context + [
                    f"ESTADO ACTUAL src/main.c (DEBES incluir todo esto y añadir tu funcionalidad):\n"
                    f"{current_code['src/main.c']}"
                ]
            })

        try:
            dev_output = _dispatch_task(task, dev_input, settings)
        except Exception as exc:
            _print_llm_failure(f"DEV_WORKER:{task.task_id}", exc)
            raise

        (run_dir / f"{task.task_id}_output.json").write_text(
            dev_output.model_dump_json(indent=2), encoding="utf-8"
        )

        if dev_output.status == "done":
            for fp in dev_output.files_to_write:
                content = _guard_auto_fix(fp.content) if fp.path.endswith(".c") else fp.content
                _write_patch(run_dir, fp.path, content, fp.mode)
                current_code[fp.path] = content
                print(f"  {_G}✎  {fp.path}{_RS}  ({fp.mode}, {content.count(chr(10))+1} líneas)")
            completed[task.task_id] = dev_output
        elif dev_output.status == "needs_clarification":
            print(f"  {_Y}⚠  [{task.task_id}] needs_clarification — continuando sin bloquear{_RS}")
            for q in dev_output.follow_up_questions:
                print(f"     ? {q[:80]}")
            completed[task.task_id] = dev_output
        else:
            print(f"  {_R}✗  [{task.task_id}] blocked — {dev_output.summary[:80]}{_RS}")
            for r in dev_output.risks:
                print(f"     ⚠ {r[:80]}")

    # 4. Summary ────────────────────────────────────────────────────
    done_count    = sum(1 for v in completed.values() if hasattr(v, "status") and v.status == "done")
    skipped_count = len(ordered) - len(completed)
    print(f"\n{_W}  Tareas completadas: {_G}{done_count}/{len(ordered)}{_RS}  "
          f"saltadas: {_Y}{skipped_count}{_RS}")

    if not current_code:
        print(f"{_R}  ✗ ningún archivo generado — abortando compilación{_RS}")
        return run_dir, False

    # 5. Compile + fix loop (LangGraph cycle) ──────────────────────────
    compile_ok, current_code = _run_fix_loop(run_dir, project_name, settings, current_code)

    # 6. Emulator ───────────────────────────────────────────────────
    if compile_ok and not no_emu:
        dsk = next(run_dir.glob("*.dsk"), None)
        if dsk:
            _launch_emulator(dsk)

    return run_dir, compile_ok


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    parser = argparse.ArgumentParser(description="Pipeline orquestador → developer → compile")
    parser.add_argument("prompt", help="Descripción del juego a generar")
    parser.add_argument("--project", default="scene_project", help="Nombre del proyecto")
    parser.add_argument("--no-emu", action="store_true", help="No lanzar el emulador")
    parser.add_argument("--dry-run", action="store_true", help="Solo orquestar, sin generar código")
    args = parser.parse_args()

    from .settings import AppSettings
    try:
        run_dir, ok = run_pipeline(
            prompt=args.prompt,
            project_name=args.project,
            settings=AppSettings(),
            no_emu=args.no_emu,
            dry_run=args.dry_run,
        )
        print(f"\n  run_dir : {run_dir}")
        sys.exit(0 if ok else 1)
    except Exception as exc:
        print(f"\n{_R}{_W}Pipeline aborted due to error:{_RS} {_R}{exc}{_RS}")
        # Avoid silent failures in CLI mode while keeping the provider response visible.
        print(f"{_R}{_format_llm_exception(exc)}{_RS}")
        sys.exit(1)
