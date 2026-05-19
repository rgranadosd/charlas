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

WORKFLOW_STEPS = [
    "orchestrator",
    "narrative",
    "design",
    "art",
    "tech",
    "contract_validation",
    "integration",
    "build",
    "build_validation",
    "qa",
]
STRICT_REQUIRED_MOCK_STEPS = set(WORKFLOW_STEPS)

load_dotenv(BASE / ".env")


def ensure_env() -> None:
    provider = os.getenv("LLM_PROVIDER", "openai").lower()

    if provider == "local":
        if not os.getenv("LOCAL_BASE_URL"):
            raise RuntimeError(
                "No se ha encontrado LOCAL_BASE_URL en el archivo .env de la raíz del proyecto."
            )
        return

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


def _load_json_trace(trace_path: str) -> dict[str, Any]:
    path = Path(trace_path).expanduser().resolve()
    if not path.is_file():
        raise RuntimeError(f"mock trace no encontrada: {path}")

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - defensive path
        raise RuntimeError(f"no se pudo parsear la mock trace en {path}: {exc}") from exc


def _trace_payload_for_step(trace_payload: dict[str, Any], step_name: str) -> dict[str, Any]:
    if not isinstance(trace_payload, dict):
        return {}

    source = trace_payload.get("agent_outputs")
    source = source if isinstance(source, dict) else trace_payload

    if step_name == "build":
        payload = source.get("build") or source.get("build_output")
    elif step_name == "contract_validation":
        payload = source.get("contract_validation") or source.get("contractvalidation")
    else:
        payload = source.get(step_name)

    if isinstance(payload, dict):
        return payload
    return {}


def _step_payload_is_success(step_name: str, payload: dict[str, Any]) -> bool:
    if not payload:
        return False

    if step_name == "build":
        return bool(payload.get("success"))

    if step_name in {"contract_validation", "build_validation", "qa"}:
        return str(payload.get("status", "")).lower() == "pass"

    status = str(payload.get("status", "")).lower()
    if status == "fail":
        return False

    return True


def _parse_mock_steps(raw_steps: str, successful_steps: set[str]) -> set[str]:
    value = (raw_steps or "auto").strip().lower()
    if value in {"", "auto"}:
        return set(successful_steps)
    if value in {"none", "off", "false", "0"}:
        return set()
    if value == "all":
        return set(successful_steps)

    selected: set[str] = set()
    for token in raw_steps.split(","):
        item = token.strip().lower()
        if not item:
            continue
        if item in successful_steps:
            selected.add(item)
    return selected


def _build_mock_replay(trace_payload: dict[str, Any], mock_steps_raw: str) -> tuple[dict[str, dict[str, Any]], list[str]]:
    successful_steps: set[str] = set()
    payload_by_step: dict[str, dict[str, Any]] = {}

    for step in WORKFLOW_STEPS:
        payload = _trace_payload_for_step(trace_payload, step)
        if _step_payload_is_success(step, payload):
            successful_steps.add(step)
            payload_by_step[step] = payload

    selected_steps = _parse_mock_steps(mock_steps_raw, successful_steps)
    mock_replay = {step: payload_by_step[step] for step in selected_steps if step in payload_by_step}
    return mock_replay, sorted(selected_steps)


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


def _build_agent_outputs_from_state(state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
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
        "build": _to_dict(state.get("build_output")) or {},
        "build_validation": _to_dict(state.get("build_validation")) or {},
        "qa": _to_dict(state.get("qa")) or {},
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
    parser.add_argument(
        "--mock-trace",
        dest="mock_trace",
        default="",
        help="Ruta a un JSON de ejecución previa para reutilizar pasos exitosos.",
    )
    parser.add_argument(
        "--mock-steps",
        dest="mock_steps",
        default="auto",
        help="Lista CSV de pasos a mockear (solo si ya fueron exitosos). Usa 'auto', 'all' o 'none'.",
    )
    parser.add_argument(
        "--strict-mocks",
        dest="strict_mocks",
        action="store_true",
        help="Falla si falta algun paso mockeable exitoso en la traza o si hubiese fallback a real.",
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
        mock_replay: dict[str, dict[str, Any]] = {}
        mock_generated_project_path: str | None = None
        mock_replay_summary: dict[str, Any] = {
            "enabled": False,
            "selected_steps": [],
            "reason": "mock_trace_not_provided",
        }
        if args.mock_trace:
            trace_payload = _load_json_trace(args.mock_trace)
            mock_replay, selected_steps = _build_mock_replay(trace_payload, args.mock_steps)
            mock_generated_project_path = (
                trace_payload.get("generated_project_path")
                or trace_payload.get("project_path")
                or None
            )
            if args.strict_mocks:
                selected_set = set(selected_steps)
                missing_steps = sorted(STRICT_REQUIRED_MOCK_STEPS - selected_set)
                if missing_steps:
                    raise RuntimeError(
                        "strict mock mode: faltan pasos con traza real reutilizable: "
                        + ", ".join(missing_steps)
                    )
            if selected_steps:
                print(
                    f"[INFO] mock replay activo en {len(selected_steps)} paso(s): {', '.join(selected_steps)}",
                    file=sys.stderr,
                )
                mock_replay_summary = {
                    "enabled": True,
                    "selected_steps": selected_steps,
                    "reason": "trace_loaded",
                }
            else:
                print(
                    "[WARN] ciclo sin mocks: se proporciono --mock-trace pero no hay pasos exitosos reutilizables para la seleccion actual.",
                    file=sys.stderr,
                )
                mock_replay_summary = {
                    "enabled": False,
                    "selected_steps": [],
                    "reason": "no_reusable_steps_in_trace",
                }
        else:
            if args.strict_mocks:
                raise RuntimeError("strict mock mode requiere --mock-trace")
            print(
                "[WARN] ciclo sin mocks: no se proporciono --mock-trace.",
                file=sys.stderr,
            )

        result = run_studio(
            request,
            mock_replay=mock_replay,
            mock_generated_project_path=mock_generated_project_path,
            strict_mocks=args.strict_mocks,
        )
        if isinstance(result, dict):
            result.setdefault("project_path", result.get("generated_project_path") or "")
            result["agent_outputs"] = _build_agent_outputs_from_state(result)
            result["mock_replay"] = mock_replay_summary
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    except Exception:
        traceback.print_exc(file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
