import json
import os
import subprocess
import sys
import time
from pathlib import Path

from langgraph.graph import END, START, StateGraph

from app.agents.art_agent import run as run_art
from app.agents.build_agent import (
    CPCTELERA_HOME,
    CPCT_MKPROJECT,
    run as run_build,
    sanitize_project_name,
)
from app.agents.build_validation_agent import run as run_build_validation
from app.agents.code_integrator_agent import run as run_integrator
from app.agents.cpctelera_tech_agent import run as run_tech
from app.agents.design_agent import run as run_design
from app.agents.narrative_agent import run as run_narrative
from app.agents.orchestrator_agent import run as run_orchestrator
from app.agents.qa_agent import run as run_qa
from app.schemas.outputs import (
    ArtOutput,
    BuildOutput,
    BuildValidationOutput,
    ComposeOutput,
    ContractValidationOutput,
    DesignOutput,
    IntegrationOutput,
    NarrativeOutput,
    OrchestratorOutput,
    QAOutput,
    TechOutputV2,
)
from app.services.contract_validation_service import adapttechoutput, validatecontract
from app.services.project_service import generateproject
from app.state.studio_state import StudioState

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GENERATED_PROJECTS_DIR = PROJECT_ROOT / "generated_projects"

WORKFLOW_STEP_TO_NODE = {
    "narrative": "narrative_node",
    "design": "design_node",
    "art": "art_node",
    "tech": "tech_node",
    "contract_validation": "contractvalidationnode",
    "integration": "integration_node",
    "build": "build_node",
    "build_validation": "build_validation_node",
    "qa": "qa_node",
    "compose": "compose_node",
}

DEFAULT_WORKFLOW_PLAN = [
    "narrative",
    "design",
    "art",
    "tech",
    "contract_validation",
    "integration",
    "build",
    "build_validation",
    "qa",
    "compose",
]


def _mock_payload_for_step(state: StudioState, step_name: str) -> dict:
    replay = state.get("mock_replay") or {}
    if not isinstance(replay, dict):
        return {}
    payload = replay.get(step_name)
    if isinstance(payload, dict):
        print(f"[INFO] [mock-replay] usando payload cacheado para step='{step_name}'", file=sys.stderr)
        return payload
    return {}


def _to_dict(payload) -> dict:
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    if hasattr(payload, "model_dump"):
        return payload.model_dump()
    return {}


def _build_failure_payload(stderr: str, build_notes: str, project_path: str = "") -> dict:
    return {
        "success": False,
        "return_code": -1,
        "stdout": "",
        "stderr": stderr,
        "artifacts": [],
        "project_path": project_path,
        "build_notes": build_notes,
    }


def _cpct_env() -> dict[str, str]:
    env = os.environ.copy()
    scripts_dir = str(CPCT_MKPROJECT.parent)
    env["CPCT_PATH"] = str(CPCTELERA_HOME)
    env["PATH"] = f"{scripts_dir}:{env.get('PATH', '')}" if env.get("PATH") else scripts_dir
    return env


def _is_valid_cpct_scaffold(project_dir: Path) -> bool:
    return (
        project_dir.exists()
        and project_dir.is_dir()
        and (project_dir / "src").is_dir()
        and (project_dir / "src" / "main.c").is_file()
        and (project_dir / "cfg").is_dir()
        and (project_dir / "cfg" / "build_config.mk").is_file()
        and (project_dir / "Makefile").is_file()
    )


def _is_build_path_compatible(project_dir: Path) -> bool:
    expected = (GENERATED_PROJECTS_DIR / sanitize_project_name(project_dir.name)).resolve()
    return project_dir.resolve() == expected


def _next_default_run_project_dir() -> Path:
    seed = int(time.time() * 1000)
    for offset in range(1000):
        suffix = f"{(seed + offset) % 100000:05d}"
        project_name = f"run{suffix}"
        candidate = (GENERATED_PROJECTS_DIR / project_name).resolve()
        if not candidate.exists():
            return candidate

    raise RuntimeError("Could not find a free generated_projects/runXXXXX directory.")


def _scaffold_path_set(scaffold: dict, key: str) -> set[str]:
    values = scaffold.get(key, []) if isinstance(scaffold, dict) else []
    if not isinstance(values, list):
        return set()

    normalized: set[str] = set()
    for value in values:
        if not isinstance(value, str):
            continue
        path = value.strip().replace("\\", "/")
        if path:
            normalized.add(path)
    return normalized


def _filter_writable_integration_files(
    files: dict[str, str],
    project_dir: Path,
    scaffold: dict,
) -> tuple[dict[str, str], list[str]]:
    allowed_files = _scaffold_path_set(scaffold, "allowed_files")
    overwrite_files = _scaffold_path_set(scaffold, "overwrite_files")
    create_if_missing = _scaffold_path_set(scaffold, "create_if_missing")

    filtered: dict[str, str] = {}
    dropped: list[str] = []

    for rel_path, content in files.items():
        if rel_path not in allowed_files:
            dropped.append(rel_path)
            continue

        target = project_dir / rel_path
        if target.exists():
            if rel_path in overwrite_files:
                filtered[rel_path] = content
            else:
                dropped.append(rel_path)
            continue

        if rel_path in create_if_missing:
            filtered[rel_path] = content
        else:
            dropped.append(rel_path)

    return filtered, dropped


def _create_cpct_project(project_dir: Path) -> Path:
    if project_dir.exists():
        raise ValueError(f"Project directory already exists: {project_dir}")
    if not CPCT_MKPROJECT.exists():
        raise FileNotFoundError(f"cpct_mkproject not found at {CPCT_MKPROJECT}")

    parent_dir = project_dir.parent
    parent_dir.mkdir(parents=True, exist_ok=True)

    project_name = sanitize_project_name(project_dir.name)

    try:
        subprocess.run(
            [str(CPCT_MKPROJECT), project_name],
            cwd=str(parent_dir),
            capture_output=True,
            text=True,
            timeout=120,
            env=_cpct_env(),
            check=True,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            f"cpct_mkproject timed out while creating {project_name} in {parent_dir}"
        ) from exc
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "")[-3000:]
        stdout = (exc.stdout or "")[-3000:]
        raise RuntimeError(
            f"cpct_mkproject failed for {project_name} in {parent_dir}."
            f"\nstdout:\n{stdout}\nstderr:\n{stderr}"
        ) from exc

    created_project_dir = (parent_dir / project_name).resolve()
    if not _is_valid_cpct_scaffold(created_project_dir):
        raise RuntimeError(
            f"Created directory is not a valid CPCtelera scaffold: {created_project_dir}"
        )
    if not _is_build_path_compatible(created_project_dir):
        raise ValueError(
            "Generated project path is not compatible with build agent path resolution: "
            f"{created_project_dir}"
        )

    return created_project_dir


def _resolve_integration_project_path(state: StudioState) -> Path:
    raw_path = state.get("generated_project_path")
    candidate = Path(raw_path).expanduser().resolve() if raw_path else _next_default_run_project_dir()

    if candidate.exists():
        if not _is_valid_cpct_scaffold(candidate):
            raise ValueError(
                "Refusing to integrate into a directory without valid CPCtelera scaffold: "
                f"{candidate}"
            )
        if not _is_build_path_compatible(candidate):
            raise ValueError(
                "Existing generated_project_path is not compatible with build path resolution: "
                f"{candidate}"
            )
        return candidate

    return _create_cpct_project(candidate)


def _build_workflow_plan(_: OrchestratorOutput) -> list[str]:
    return list(DEFAULT_WORKFLOW_PLAN)


def _merge_agent_payloads(state: StudioState, payload_updates: dict[str, object] | None = None) -> dict[str, dict]:
    merged = dict(state.get("agent_payloads") or {})
    for key, value in (payload_updates or {}).items():
        merged[key] = _to_dict(value)
    return merged


def _node_result(
    state: StudioState,
    step_name: str,
    payload_key: str | None = None,
    payload=None,
    **updates,
) -> dict:
    completed_steps = list(state.get("completed_steps") or [])
    if step_name not in completed_steps:
        completed_steps.append(step_name)

    payload_updates = {payload_key: payload} if payload_key and payload is not None else {}
    result = {
        "completed_steps": completed_steps,
        "current_step": step_name,
        "agent_payloads": _merge_agent_payloads(state, payload_updates),
        **updates,
    }
    if payload_key and payload is not None:
        result[payload_key] = payload
    return result


def _next_workflow_step(state: StudioState) -> str:
    workflow_plan = state.get("workflow_plan") or list(DEFAULT_WORKFLOW_PLAN)
    completed_steps = set(state.get("completed_steps") or [])

    if "contract_validation" in completed_steps:
        validation_payload = state.get("contract_validation") or state.get("contractvalidation")
        validation = _to_dict(validation_payload)
        if validation and validation.get("status") == "fail":
            # Only abort on hard blockers: missing required files or missing critical symbols.
            # Duplicate-symbol false positives (ghost entries in provided_symbols) are non-fatal.
            missing_files = validation.get("missing_required_files") or []
            missing_symbols = validation.get("missing_symbols") or []
            if missing_files or missing_symbols:
                return "compose"
            # Otherwise: warnings/duplicates → log and proceed to integration
            import logging as _logging
            _logging.getLogger(__name__).warning(
                "[contract_validation] status=fail but no missing files/symbols — "
                "likely duplicate symbol entries in contract (non-fatal). "
                "issues=%s", validation.get("issues") or validation.get("errors") or []
            )

    for step in workflow_plan:
        if step not in completed_steps:
            return step

    return "compose"


def _route_next_step(state: StudioState):
    next_step = _next_workflow_step(state)
    route = WORKFLOW_STEP_TO_NODE.get(next_step, "compose_node")
    print(f"-> route_next_step => {route}", file=sys.stderr)
    return route


def orchestrator_node(state: StudioState):
    print("-> orchestrator_node", file=sys.stderr)
    mock_payload = _mock_payload_for_step(state, "orchestrator")
    if mock_payload:
        orchestrator = OrchestratorOutput.model_validate(mock_payload)
    else:
        orchestrator = OrchestratorOutput.model_validate(run_orchestrator(state["user_request"]))
    workflow_plan = _build_workflow_plan(orchestrator)
    return _node_result(
        state,
        "orchestrator",
        payload_key="orchestrator",
        payload=orchestrator,
        workflow_plan=workflow_plan,
    )


def narrative_node(state: StudioState):
    print("-> narrative_node", file=sys.stderr)
    mock_payload = _mock_payload_for_step(state, "narrative")
    if mock_payload:
        narrative = NarrativeOutput.model_validate(mock_payload)
    else:
        narrative = NarrativeOutput.model_validate(
            run_narrative(
                state["user_request"],
                _to_dict(state.get("orchestrator")) or None,
            )
        )
    return _node_result(state, "narrative", payload_key="narrative", payload=narrative)


def design_node(state: StudioState):
    print("-> design_node", file=sys.stderr)
    mock_payload = _mock_payload_for_step(state, "design")
    if mock_payload:
        design = DesignOutput.model_validate(mock_payload)
    else:
        design = DesignOutput.model_validate(
            run_design(
                state["user_request"],
                _to_dict(state.get("orchestrator")) or None,
                _to_dict(state.get("narrative")) or None,
            )
        )
    return _node_result(state, "design", payload_key="design", payload=design)


def art_node(state: StudioState):
    print("-> art_node", file=sys.stderr)
    mock_payload = _mock_payload_for_step(state, "art")
    if mock_payload:
        art = ArtOutput.model_validate(mock_payload)
    else:
        art = ArtOutput.model_validate(
            run_art(
                state["user_request"],
                _to_dict(state.get("orchestrator")) or None,
                _to_dict(state.get("narrative")) or None,
                _to_dict(state.get("design")) or None,
            )
        )
    return _node_result(state, "art", payload_key="art", payload=art)


def tech_node(state: StudioState):
    print("-> tech_node", file=sys.stderr)
    mock_payload = _mock_payload_for_step(state, "tech")
    if mock_payload:
        tech = adapttechoutput(TechOutputV2.model_validate(mock_payload))
    else:
        tech = adapttechoutput(
            TechOutputV2.model_validate(
                run_tech(
                    state["user_request"],
                    _to_dict(state.get("orchestrator")) or None,
                    _to_dict(state.get("narrative")) or None,
                    _to_dict(state.get("design")) or None,
                    _to_dict(state.get("art")) or None,
                )
            )
        )
    return _node_result(state, "tech", payload_key="tech", payload=tech)


def contractvalidationnode(state: StudioState):
    print("-> contractvalidationnode", file=sys.stderr)
    mock_payload = _mock_payload_for_step(state, "contract_validation")
    if mock_payload:
        validation = ContractValidationOutput.model_validate(mock_payload)
    else:
        validation = ContractValidationOutput.model_validate(validatecontract(_to_dict(state.get("tech"))))
    result = _node_result(
        state,
        "contract_validation",
        payload_key="contract_validation",
        payload=validation,
        contractvalidation=validation,
    )
    result["contract_validation"] = validation
    return result


def integration_node(state: StudioState):
    print("-> integration_node", file=sys.stderr)
    strict_mocks = bool(state.get("strict_mocks"))
    mock_payload = _mock_payload_for_step(state, "integration")
    if mock_payload:
        integration = IntegrationOutput.model_validate(mock_payload)
        project_path = (
            str(state.get("generated_project_path") or "").strip()
            or str(state.get("mock_generated_project_path") or "").strip()
        )
        if project_path and Path(project_path).exists():
            return _node_result(
                state,
                "integration",
                payload_key="integration",
                payload=integration,
                generated_project_path=project_path,
            )
        if strict_mocks:
            raise RuntimeError(
                "strict mock mode: integration requiere generated_project_path valido en la traza"
            )
        print(
            "[WARN] [mock-replay] integration mock sin generated_project_path válido; ejecutando integración real.",
            file=sys.stderr,
        )

    integration_project_dir = _resolve_integration_project_path(state)

    print("[INFO] [integration] llamando a code_integrator_agent (LLM + post-proceso)...", file=sys.stderr)
    _t0 = time.time()
    integration = IntegrationOutput.model_validate(
        run_integrator(
            state["user_request"],
            _to_dict(state.get("orchestrator")) or None,
            _to_dict(state.get("narrative")) or None,
            _to_dict(state.get("design")) or None,
            _to_dict(state.get("art")) or None,
            _to_dict(state.get("tech")) or None,
        )
    )
    print(f"[INFO] [integration] code_integrator_agent completado en {time.time() - _t0:.1f}s", file=sys.stderr)

    print("[INFO] [integration] filtrando ficheros y materializando proyecto...", file=sys.stderr)
    tech = _to_dict(state.get("tech"))
    scaffold = tech.get("scaffold", {}) if isinstance(tech, dict) else {}

    writable_files, dropped_files = _filter_writable_integration_files(
        integration.files,
        integration_project_dir,
        scaffold,
    )

    print(f"[INFO] [integration] generando proyecto en {integration_project_dir} ({len(writable_files)} fichero(s))...", file=sys.stderr)
    path = generateproject(
        str(integration_project_dir),
        {
            "files": writable_files,
            "scaffold": scaffold,
        },
    )
    print(f"[INFO] [integration] proyecto materializado en {path}", file=sys.stderr)

    integration_notes = list(integration.integration_notes or [])
    manual_followups = list(integration.manual_followups or [])
    if not integration_notes:
        integration_notes.append(f"Accepted {len(writable_files)} scaffold-valid file(s) for project materialization.")
    if dropped_files:
        manual_followups.append(
            "Skipped non-writable files: "
            + ", ".join(sorted(dropped_files)[:10])
            + (", ..." if len(dropped_files) > 10 else "")
        )
    if not writable_files:
        manual_followups.append("No writable files were applied to the generated CPCtelera scaffold.")

    integration = integration.model_copy(
        update={
            "files": writable_files,
            "integration_notes": integration_notes,
            "manual_followups": manual_followups,
        }
    )

    return _node_result(
        state,
        "integration",
        payload_key="integration",
        payload=integration,
        generated_project_path=path,
    )


def build_node(state: StudioState):
    print("-> build_node", file=sys.stderr)
    mock_payload = _mock_payload_for_step(state, "build")
    if mock_payload:
        build_output = BuildOutput.model_validate(mock_payload)
        return _node_result(
            state,
            "build",
            payload_key="build_output",
            payload=build_output,
            generated_project_path=str(
                state.get("generated_project_path")
                or state.get("mock_generated_project_path")
                or build_output.project_path
                or ""
            ),
        )

    integration = state.get("integration")
    prebuild_errors = []
    integration_is_mocked = "integration" in (state.get("mock_replay") or {})
    if integration is not None and not integration_is_mocked:
        prebuild_errors = [
            str(item).strip()
            for item in getattr(integration, "prebuild_validation_errors", [])
            if str(item).strip()
        ]

    if prebuild_errors:
        project_path = str(state.get("generated_project_path") or "")
        build_output = BuildOutput.model_validate(
            _build_failure_payload(
                "Pre-build C validation failed before compilation:\n"
                + "\n".join(f"- {issue}" for issue in prebuild_errors[:20]),
                "Build skipped due to malformed generated C includes/prototypes.",
                project_path,
            )
        )
        return _node_result(
            state,
            "build",
            payload_key="build_output",
            payload=build_output,
            generated_project_path=project_path,
        )

    project_path = state.get("generated_project_path")
    if not project_path:
        build_output = BuildOutput.model_validate(
            _build_failure_payload(
                "generated_project_path is missing before build_node.",
                "Build skipped because integration did not provide a project path.",
                "",
            )
        )
        return _node_result(state, "build", payload_key="build_output", payload=build_output)

    requested_project_path = Path(project_path).resolve()

    if not _is_valid_cpct_scaffold(requested_project_path):
        build_output = BuildOutput.model_validate(
            _build_failure_payload(
                f"Invalid CPCtelera scaffold: {requested_project_path}",
                "Build skipped because the integration path is not a valid CPCtelera project.",
                str(requested_project_path),
            )
        )
        return _node_result(
            state,
            "build",
            payload_key="build_output",
            payload=build_output,
            generated_project_path=str(requested_project_path),
        )

    if not _is_build_path_compatible(requested_project_path):
        build_output = BuildOutput.model_validate(
            _build_failure_payload(
                f"Build path mismatch risk for: {requested_project_path}",
                "Build skipped to avoid compiling a different directory than integration_node used.",
                str(requested_project_path),
            )
        )
        return _node_result(
            state,
            "build",
            payload_key="build_output",
            payload=build_output,
            generated_project_path=str(requested_project_path),
        )

    build_raw, resolved_project_path = run_build(str(requested_project_path))
    if Path(resolved_project_path).resolve() != requested_project_path:
        build_output = BuildOutput.model_validate(
            _build_failure_payload(
                (
                    "Build agent resolved a different project path than integration_node used. "
                    f"requested={requested_project_path} resolved={resolved_project_path}"
                ),
                "Build aborted to preserve integration/build path consistency.",
                str(requested_project_path),
            )
        )
        return _node_result(
            state,
            "build",
            payload_key="build_output",
            payload=build_output,
            generated_project_path=str(requested_project_path),
        )

    build_output = BuildOutput.model_validate(build_raw).model_copy(
        update={"project_path": str(requested_project_path)}
    )

    return _node_result(
        state,
        "build",
        payload_key="build_output",
        payload=build_output,
        generated_project_path=str(requested_project_path),
    )


def build_validation_node(state: StudioState):
    print("-> build_validation_node", file=sys.stderr)
    mock_payload = _mock_payload_for_step(state, "build_validation")
    if mock_payload:
        build_validation = BuildValidationOutput.model_validate(mock_payload)
    else:
        build_validation = BuildValidationOutput.model_validate(
            run_build_validation(
                state["user_request"],
                state.get("generated_project_path"),
                _to_dict(state.get("build_output")),
            )
        )
    return _node_result(
        state,
        "build_validation",
        payload_key="build_validation",
        payload=build_validation,
    )


def qa_node(state: StudioState):
    print("-> qa_node", file=sys.stderr)
    mock_payload = _mock_payload_for_step(state, "qa")
    if mock_payload:
        qa = QAOutput.model_validate(mock_payload)
    else:
        qa = QAOutput.model_validate(
            run_qa(
                state["user_request"],
                _to_dict(state.get("orchestrator")) or None,
                _to_dict(state.get("design")) or None,
                _to_dict(state.get("art")) or None,
                _to_dict(state.get("tech")) or None,
                _to_dict(state.get("integration")) or None,
                _to_dict(state.get("build_validation")) or None,
                _to_dict(state.get("build_output")) or None,
            )
        )
    return _node_result(state, "qa", payload_key="qa", payload=qa)


def compose_node(state: StudioState):
    print("-> compose_node", file=sys.stderr)
    completed_steps = list(state.get("completed_steps") or [])
    if "compose" not in completed_steps:
        completed_steps.append("compose")

    contract_validation = state.get("contract_validation") or state.get("contractvalidation")
    final_payload = ComposeOutput.model_validate(
        {
            "target_platform": state.get("target_platform", ""),
            "framework": state.get("framework", ""),
            "workflow_plan": state.get("workflow_plan") or list(DEFAULT_WORKFLOW_PLAN),
            "completed_steps": completed_steps,
            "generated_project_path": str(state.get("generated_project_path") or ""),
            "orchestrator": _to_dict(state.get("orchestrator")),
            "narrative": _to_dict(state.get("narrative")),
            "design": _to_dict(state.get("design")),
            "art": _to_dict(state.get("art")),
            "tech": _to_dict(state.get("tech")),
            "contract_validation": _to_dict(contract_validation),
            "integration": _to_dict(state.get("integration")),
            "build_output": _to_dict(state.get("build_output")),
            "build_validation": _to_dict(state.get("build_validation")),
            "qa": _to_dict(state.get("qa")),
        }
    )

    return {
        "completed_steps": completed_steps,
        "current_step": "compose",
        "final_payload": final_payload,
        "final_output": json.dumps(final_payload.model_dump(), ensure_ascii=False, indent=2),
    }


builder = StateGraph(StudioState)
builder.add_node("orchestrator_node", orchestrator_node)
builder.add_node("narrative_node", narrative_node)
builder.add_node("design_node", design_node)
builder.add_node("art_node", art_node)
builder.add_node("tech_node", tech_node)
builder.add_node("contractvalidationnode", contractvalidationnode)
builder.add_node("integration_node", integration_node)
builder.add_node("build_node", build_node)
builder.add_node("build_validation_node", build_validation_node)
builder.add_node("qa_node", qa_node)
builder.add_node("compose_node", compose_node)

builder.add_edge(START, "orchestrator_node")
route_map = {node_name: node_name for node_name in WORKFLOW_STEP_TO_NODE.values()}
builder.add_conditional_edges("orchestrator_node", _route_next_step, route_map)
builder.add_conditional_edges("narrative_node", _route_next_step, route_map)
builder.add_conditional_edges("design_node", _route_next_step, route_map)
builder.add_conditional_edges("art_node", _route_next_step, route_map)
builder.add_conditional_edges("tech_node", _route_next_step, route_map)
builder.add_conditional_edges("contractvalidationnode", _route_next_step, route_map)
builder.add_conditional_edges("integration_node", _route_next_step, route_map)
builder.add_conditional_edges("build_node", _route_next_step, route_map)
builder.add_conditional_edges("build_validation_node", _route_next_step, route_map)
builder.add_conditional_edges("qa_node", _route_next_step, route_map)
builder.add_edge("compose_node", END)

graph = builder.compile()


def run_studio(
    user_request: str,
    mock_replay: dict[str, dict] | None = None,
    mock_generated_project_path: str | None = None,
    strict_mocks: bool = False,
):
    initial_state = {
        "user_request": user_request,
        "target_platform": "Amstrad CPC 6128",
        "framework": "CPCtelera",
        "agent_payloads": {},
        "completed_steps": [],
        "workflow_plan": list(DEFAULT_WORKFLOW_PLAN),
        "mock_replay": mock_replay or {},
        "strict_mocks": strict_mocks,
    }
    if mock_generated_project_path:
        initial_state["mock_generated_project_path"] = str(mock_generated_project_path)
        initial_state["generated_project_path"] = str(mock_generated_project_path)

    return graph.invoke(initial_state)
