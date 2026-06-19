"""End-to-end per-run pipeline: prompt → orchestrator → C code → compile → Caprice32.

Every invocation creates a fresh isolated run directory:
    scene_agent/outputs/<YYYYMMDD_HHMMSS>/
        orchestrator_contract.json  ← task decomposition
        src/main.c                  ← generated C
        cfg/ Makefile obj/
        scene.dsk                   ← compiled artifact

Usage:
    python -m scene_agent.build_and_run [--goal "..."] [--no-emu]
"""
from __future__ import annotations

import argparse
import logging
import os
import shutil
import subprocess
import time
from pathlib import Path

logger = logging.getLogger(__name__)

_G  = "\033[32m"
_Y  = "\033[33m"
_B  = "\033[1m"
_RS = "\033[0m"

_REPO_ROOT      = Path(__file__).parents[1]
_TESTPROJECT    = _REPO_ROOT / "pruebacpct"
_CPCTELERA_ROOT = _REPO_ROOT / "cpctelera" / "cpctelera"
_CAPRICE32_BIN  = _REPO_ROOT / "cpctelera" / "tools" / "caprice32" / "cap32"
_OUTPUTS_ROOT   = Path(os.environ.get("CPC_OUTPUTS_DIR", "/tmp/cpc_outputs"))





# ---------------------------------------------------------------------------
# Infra helpers
# ---------------------------------------------------------------------------

def _new_run_dir() -> Path:
    run_id = time.strftime("%Y%m%d_%H%M%S")
    run_dir = _OUTPUTS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def _scaffold(run_dir: Path) -> None:
    (run_dir / "src").mkdir(exist_ok=True)
    (run_dir / "obj").mkdir(exist_ok=True)
    shutil.copy(_TESTPROJECT / "Makefile", run_dir / "Makefile")
    cfg_dst = run_dir / "cfg"
    if cfg_dst.exists():
        shutil.rmtree(cfg_dst)
    shutil.copytree(_TESTPROJECT / "cfg", cfg_dst)

    # Use a fixed short project name — AMSDOS limits filenames to 8 chars.
    # All runs produce SCENE.BIN inside the DSK, autorun is always run"SCENE.BIN
    cfg_mk = cfg_dst / "build_config.mk"
    if cfg_mk.exists():
        import re as _re
        src = cfg_mk.read_text(encoding="utf-8")
        patched = _re.sub(
            r"^(PROJNAME\s*:=\s*)\S+",
            r"\1scene",
            src,
            flags=_re.MULTILINE,
        )
        cpct_path = str(_CPCTELERA_ROOT.resolve())
        patched = _re.sub(
            r"^(CPCT_PATH\s*:=\s*).*",
            rf"\1{cpct_path}",
            patched,
            flags=_re.MULTILINE,
        )
        cfg_mk.write_text(patched, encoding="utf-8")


def _compile(run_dir: Path) -> bool:
    cpct_path = str(_CPCTELERA_ROOT.resolve())
    env = {**os.environ, "CPCT_PATH": cpct_path}
    print(f"\n{_G}{_B}══════════════════════════════════════════════════════════{_RS}")
    print(f"{_G}{_B}  BUILD  make -C {run_dir.name}{_RS}")
    print(f"{_G}{_B}══════════════════════════════════════════════════════════{_RS}")
    result = subprocess.run(
        ["make", "-C", str(run_dir.resolve())],
        capture_output=True, text=True, env=env, timeout=120,
    )
    if result.returncode == 0:
        print(f"{_G}  ✓ compilation OK{_RS}")
        dsks = list(run_dir.glob("*.dsk"))
        if dsks:
            print(f"{_G}  ✓ DSK: {dsks[0].name}{_RS}")
        return True
    print(f"\033[31m  ✗ FAILED (rc={result.returncode})\n{result.stderr[:400]}\033[0m")
    return False


def _launch_emulator(dsk_path: Path) -> None:
    if not _CAPRICE32_BIN.exists():
        logger.warning("[EMU] cap32 not found at %s", _CAPRICE32_BIN)
        return
    binary_name = dsk_path.stem[:8].upper()
    autocmd = f'run"{binary_name}.BIN'
    print(f"\n{_G}{_B}══════════════════════════════════════════════════════════{_RS}")
    print(f"{_G}{_B}  EMULATOR  {dsk_path.name}  →  {autocmd}{_RS}")
    print(f"{_G}{_B}══════════════════════════════════════════════════════════{_RS}")
    subprocess.run([str(_CAPRICE32_BIN), str(dsk_path), "-a", autocmd])


# ---------------------------------------------------------------------------
# Main pipeline entry
# ---------------------------------------------------------------------------

def run(
    goal: str,
    dry_run: bool = False,
    no_emu: bool = False,
) -> Path:
    from .pipeline import run_pipeline
    from .settings import AppSettings
    settings = AppSettings()

    run_dir, _ = run_pipeline(
        prompt=goal,
        project_name="testproject",
        settings=settings,
        no_emu=no_emu,
        dry_run=dry_run,
    )
    return Path(run_dir)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _find_dsk(run_id: str | None) -> Path | None:
    """Return the DSK for a specific run_id, or the most recent one if None."""
    if not _OUTPUTS_ROOT.exists():
        return None
    if run_id:
        # Accept both with and without underscore: "20260601_165325" or "20260601165325"
        candidates = [_OUTPUTS_ROOT / run_id, _OUTPUTS_ROOT / run_id.replace("_", "")]
        for c in candidates:
            if c.exists():
                dsks = list(c.glob("*.dsk"))
                return dsks[0] if dsks else None
        return None
    for r in sorted(_OUTPUTS_ROOT.iterdir(), reverse=True):
        dsks = list(r.glob("*.dsk"))
        if dsks:
            return dsks[0]
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="RetroStudio scene pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Modes:
  (no args)          → launch the last generated DSK in Caprice32
  <run_id>           → launch a specific run (e.g. 20260601_165325)
  --build            → run full pipeline: orchestrate → develop → compile → launch
  --build --no-emu   → same but skip emulator
  --build --goal "…" → pipeline with a custom goal
""",
    )
    parser.add_argument("run_id", nargs="?", default=None,
                        help="Run ID to launch (default: last run)")
    parser.add_argument("--build",   action="store_true",
                        help="Run full pipeline")
    parser.add_argument("--goal",    default=None,
                        help="What to build (required with --build)")
    parser.add_argument("--no-emu",  action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    # --- launch mode (default) ---
    if not args.build:
        dsk = _find_dsk(args.run_id)
        if dsk:
            label = args.run_id or f"last ({dsk.parent.name})"
            print(f"{_G}Launching {label} → {dsk.name}{_RS}")
            _launch_emulator(dsk)
            return 0
        print(f"{_Y}No DSK found. Run with --build first.{_RS}")
        return 1

    # --- full pipeline mode ---
    if not args.goal:
        print(f"{_Y}Error: --build requires --goal \"describe what to build\"{_RS}")
        print(f"  Example: python -m scene_agent.build_and_run --build --goal \"Arkanoid con pala y pelota\"")
        return 1

    run_dir = run(args.goal, dry_run=args.dry_run, no_emu=args.no_emu)
    print(f"\n{_G}Run directory: {run_dir}{_RS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
