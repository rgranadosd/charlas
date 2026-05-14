import argparse
import json
import os
import sys
import traceback
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from app.graph.main_graph import graph, run_studio

BASE = Path(__file__).resolve().parents[1]
TARGET_PLATFORM = "Amstrad CPC 6128"
FRAMEWORK = "CPCtelera"

load_dotenv(BASE / ".env")


def ensure_env() -> None:
    provider = os.getenv("LLM_PROVIDER", "openai").lower()

    if provider == "mistral":
        if not os.getenv("MISTRAL_API_KEY"):
            raise RuntimeError(
                "No se ha encontrado MISTRAL_API_KEY en el archivo .env de la raíz del proyecto."
            )
        return

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "No se ha encontrado OPENAI_API_KEY en el archivo .env de la raíz del proyecto."
        )


def _to_dict(payload: Any) -> Any:
    if payload is None:
        return None
    if isinstance(payload, dict):
        return payload
    if hasattr(payload, "model_dump"):
        return payload.model_dump()
    return payload


def _find_artifacts(project_path: str | None, build_output: dict[str, Any]) -> tuple[list[str], list[str]]:
    if not project_path:
        return [], []

    project_dir = Path(project_path)
    if not project_dir.exists() or not project_dir.is_dir():
        return [], []

    dsk_paths: set[str] = set()
    cdt_paths: set[str] = set()

    for artifact in build_output.get("artifacts", []):
        candidate = project_dir / artifact
        if not candidate.exists() or not candidate.is_file():
            continue
        suffix = candidate.suffix.lower()
        if suffix == ".dsk":
            dsk_paths.add(str(candidate))
        elif suffix == ".cdt":
            cdt_paths.add(str(candidate))

    for candidate in project_dir.rglob("*.dsk"):
        if candidate.is_file():
            dsk_paths.add(str(candidate))
    for candidate in project_dir.rglob("*.cdt"):
        if candidate.is_file():
            cdt_paths.add(str(candidate))

    return sorted(dsk_paths), sorted(cdt_paths)


def run_full_studio_pipeline(game_request: str) -> dict[str, Any]:
    initial_state = {
        "user_request": game_request,
        "target_platform": TARGET_PLATFORM,
        "framework": FRAMEWORK,
    }

    state = graph.invoke(initial_state)

    project_path = state.get("generated_project_path")
    build_output = _to_dict(state.get("build_output")) or {}
    dsk_paths, cdt_paths = _find_artifacts(project_path, build_output)

    agent_outputs = {
        "orchestrator": _to_dict(state.get("orchestrator")) or {},
        "narrative": _to_dict(state.get("narrative")) or {},
        "design": _to_dict(state.get("design")) or {},
        "art": _to_dict(state.get("art")) or {},
        "tech": _to_dict(state.get("tech")) or {},
        "contract_validation": _to_dict(
            state.get("contract_validation") or state.get("contractvalidation")
        )
        or {},
        "integration": _to_dict(state.get("integration")) or {},
        "build": build_output,
        "build_validation": _to_dict(state.get("build_validation")) or {},
        "qa": _to_dict(state.get("qa")) or {},
    }

    return {
        "request": game_request,
        "project_path": project_path,
        "dsk_paths": dsk_paths,
        "cdt_paths": cdt_paths,
        "qa_status": agent_outputs["qa"].get("status", "unknown"),
        "agent_outputs": agent_outputs,
        "final_output": state.get("final_output", ""),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the full CPC Studio pipeline.")
    parser.add_argument(
        "request",
        nargs="*",
        help="Game request in natural language.",
    )
    parser.add_argument(
        "--request",
        dest="request_flag",
        default="",
        help="Game request in natural language.",
    )
    args = parser.parse_args()

    request = args.request_flag.strip() or " ".join(args.request).strip()
    if not request:
        request = (
            "Crea una base de shooter lateral para Amstrad CPC 6128 con control suave, "
            "scroll contenido y gran legibilidad visual."
        )

    try:
        ensure_env()
        result = run_studio(request)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    except Exception:
        traceback.print_exc(file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
