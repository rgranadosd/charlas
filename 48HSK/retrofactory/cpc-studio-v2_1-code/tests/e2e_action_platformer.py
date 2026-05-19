"""
End-to-end test: action_platformer_run_and_gun pipeline
========================================================
Ejecuta el pipeline completo con `run_studio` y dumpa:
  - workflow_plan y completed_steps
  - payload resumido por agente (agent_payloads)
  - archivos generados en el scaffold (integration)
  - build_output
  - build_validation
  - final_output (compose)

Uso:
    cd /Users/rafagranados/Develop/charlas/48HSK/retrofactory/cpc-studio-v2_1-code
    source ../.venv/bin/activate
    python -m tests.e2e_action_platformer 2>&1 | tee /tmp/e2e_platformer.log
"""

import json
import sys
import traceback
from pathlib import Path

# Asegura que el proyecto esté en el path aunque se invoque como script directo
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from app.graph.main_graph import run_studio  # noqa: E402

GAME_REQUEST = (
    "Crea un action platformer run-and-gun para Amstrad CPC 6128 con CPCtelera. "
    "El jugador es un soldado que corre, salta y dispara en un scroll lateral. "
    "Prioridad: control suave, sprites grandes y fluidos, mapa de tiles. "
    "No usar rasterización compleja; mode 0 con paleta de 8 colores."
)


def _sep(title: str = "") -> None:
    line = "=" * 70
    if title:
        print(f"\n{line}\n  {title}\n{line}")
    else:
        print(line)


def _dump_agent_payloads(agent_payloads: dict) -> None:
    for step, payload in agent_payloads.items():
        _sep(f"AGENT PAYLOAD: {step}")
        if not payload:
            print("  (vacío)")
            continue
        # Imprime las claves top-level y sus tipos / valores cortos
        for k, v in payload.items():
            if isinstance(v, str) and len(v) > 200:
                print(f"  {k}: {v[:200]}…")
            elif isinstance(v, list) and len(v) > 8:
                print(f"  {k}: [{len(v)} items] → {json.dumps(v[:3], ensure_ascii=False)} …")
            elif isinstance(v, dict) and len(v) > 10:
                keys = list(v.keys())[:6]
                print(f"  {k}: {{… {len(v)} keys, first 6: {keys} …}}")
            else:
                print(f"  {k}: {json.dumps(v, ensure_ascii=False, default=str)}")


def _dump_integration_files(project_path: str | None) -> None:
    _sep("INTEGRATION — archivos en scaffold")
    if not project_path:
        print("  generated_project_path no definido")
        return
    base = Path(project_path)
    if not base.exists():
        print(f"  DIRECTORIO NO EXISTE: {project_path}")
        return
    files = sorted(base.rglob("*"))
    for f in files:
        if f.is_file():
            rel = f.relative_to(base)
            size = f.stat().st_size
            print(f"  {rel}  [{size} bytes]")


def _dump_build_output(build_output: dict) -> None:
    _sep("BUILD OUTPUT")
    if not build_output:
        print("  (vacío)")
        return
    keys = ["success", "return_code", "project_path", "build_notes", "artifacts"]
    for k in keys:
        if k in build_output:
            v = build_output[k]
            print(f"  {k}: {json.dumps(v, ensure_ascii=False, default=str)}")
    # stdout / stderr resumidos
    for stream in ("stdout", "stderr"):
        text = build_output.get(stream, "")
        if text:
            lines = text.strip().splitlines()
            tail = "\n    ".join(lines[-30:])
            print(f"  {stream} (últimas 30 líneas):\n    {tail}")


def _dump_build_validation(bv: dict) -> None:
    _sep("BUILD VALIDATION")
    if not bv:
        print("  (vacío)")
        return
    for k, v in bv.items():
        print(f"  {k}: {json.dumps(v, ensure_ascii=False, default=str)}")


def main() -> None:
    _sep("E2E TEST: action_platformer_run_and_gun")
    print(f"Request: {GAME_REQUEST}\n")

    try:
        state = run_studio(GAME_REQUEST)
    except Exception:
        _sep("PIPELINE EXCEPTION")
        traceback.print_exc()
        sys.exit(1)

    # ── workflow tracking ──────────────────────────────────────────────
    _sep("WORKFLOW PLAN")
    print(f"  plan:      {state.get('workflow_plan')}")
    print(f"  completed: {state.get('completed_steps')}")
    print(f"  project:   {state.get('generated_project_path')}")

    # ── per-agent payloads ─────────────────────────────────────────────
    agent_payloads: dict = state.get("agent_payloads") or {}
    _dump_agent_payloads(agent_payloads)

    # ── integration files ──────────────────────────────────────────────
    _dump_integration_files(state.get("generated_project_path"))

    # ── build ──────────────────────────────────────────────────────────
    bld = state.get("build_output")
    if hasattr(bld, "model_dump"):
        bld = bld.model_dump()
    elif not isinstance(bld, dict):
        bld = {}
    _dump_build_output(bld)

    # ── build validation ───────────────────────────────────────────────
    bv = state.get("build_validation")
    if hasattr(bv, "model_dump"):
        bv = bv.model_dump()
    elif not isinstance(bv, dict):
        bv = {}
    _dump_build_validation(bv)

    # ── final_output (compose) ─────────────────────────────────────────
    _sep("FINAL OUTPUT (compose)")
    final = state.get("final_output", "")
    if final:
        try:
            parsed = json.loads(final) if isinstance(final, str) else final
            print(json.dumps(parsed, ensure_ascii=False, indent=2, default=str)[:4000])
        except Exception:
            print(str(final)[:4000])
    else:
        print("  (vacío)")

    _sep("TEST COMPLETE")
    completed = state.get("completed_steps") or []
    plan = state.get("workflow_plan") or []
    missing = [s for s in plan if s not in completed]
    if missing:
        print(f"  ADVERTENCIA: pasos no completados: {missing}")
    else:
        print(f"  Todos los pasos completados: {completed}")

    bld_ok = bld.get("success", False) if bld else False
    bv_status = bv.get("status", "unknown") if bv else "unknown"
    print(f"  build.success       = {bld_ok}")
    print(f"  build_validation    = {bv_status}")


if __name__ == "__main__":
    main()
