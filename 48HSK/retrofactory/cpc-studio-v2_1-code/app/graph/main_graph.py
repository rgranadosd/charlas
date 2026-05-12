import json
import os
import subprocess
import sys
import time
from pathlib import Path

from langgraph.graph import StateGraph, START, END

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
    ContractValidationOutput,
    DesignOutput,
    IntegrationOutput,
    NarrativeOutput,
    OrchestratorOutput,
    QAOutput,
    TechOutputV2,
)
from app.services.contract_validation_service import adapt_tech_output, validate_contract
from app.services.project_service import generate_project
from app.state.studio_state import StudioState

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GENERATED_PROJECTS_DIR = PROJECT_ROOT / "generated_projects"


def _to_dict(payload) -> dict:
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    if hasattr(payload, "model_dump"):
        return payload.model_dump()
    return {}


def _json_block(title: str, payload) -> str:
    data = _to_dict(payload)
    if not data:
        return ""
    return f"{title}:\n" + json.dumps(data, ensure_ascii=False, indent=2)


def _build_failure_payload(stderr: str, build_notes: str) -> dict:
    return {
        "success": False,
        "return_code": -1,
        "stdout": "",
        "stderr": stderr,
        "artifacts": [],
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
    # Keep names <= 8 chars and alphanumeric so build_agent resolves the same path.
    # Format: runXXXXX (timestamp-derived suffix).
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


def orchestrator_node(state: StudioState):
    print("-> orchestrator_node", file=sys.stderr)
    raw = run_orchestrator(state["user_request"])
    return {"orchestrator": OrchestratorOutput.model_validate(raw)}


def narrative_node(state: StudioState):
    print("-> narrative_node", file=sys.stderr)
    raw = run_narrative(
        state["user_request"],
        _to_dict(state.get("orchestrator")) or None,
    )
    return {
        "narrative": NarrativeOutput.model_validate(raw)
    }


def design_node(state: StudioState):
    print("-> design_node", file=sys.stderr)
    raw = run_design(
        state["user_request"],
        _to_dict(state.get("orchestrator")) or None,
        _to_dict(state.get("narrative")) or None,
    )
    return {
        "design": DesignOutput.model_validate(raw)
    }


def art_node(state: StudioState):
    print("-> art_node", file=sys.stderr)
    raw = run_art(
        state["user_request"],
        _to_dict(state.get("orchestrator")) or None,
        _to_dict(state.get("narrative")) or None,
        _to_dict(state.get("design")) or None,
    )
    return {
        "art": ArtOutput.model_validate(raw)
    }


def tech_node(state: StudioState):
    print("-> tech_node", file=sys.stderr)
    raw = run_tech(
        state["user_request"],
        _to_dict(state.get("orchestrator")) or None,
        _to_dict(state.get("narrative")) or None,
        _to_dict(state.get("design")) or None,
        _to_dict(state.get("art")) or None,
    )
    tech = adapt_tech_output(TechOutputV2.model_validate(raw))
    return {
        "tech": tech
    }


def contractvalidationnode(state: StudioState):
    print("-> contractvalidationnode", file=sys.stderr)
    validation = validate_contract(_to_dict(state.get("tech")))
    return {
        "contractvalidation": validation,
        "contract_validation": validation,
    }


def _route_after_contractvalidation(state: StudioState):
    raw = state.get("contractvalidation") or state.get("contract_validation")
    payload = _to_dict(raw)

    try:
        validation = ContractValidationOutput.model_validate(payload)
    except Exception:
        return "compose_node"

    return "integration_node" if validation.status == "pass" else "compose_node"


def integration_node(state: StudioState):
    print("-> integration_node", file=sys.stderr)
    integration_project_dir = _resolve_integration_project_path(state)

    raw = run_integrator(
        state["user_request"],
        _to_dict(state.get("orchestrator")) or None,
        _to_dict(state.get("narrative")) or None,
        _to_dict(state.get("design")) or None,
        _to_dict(state.get("art")) or None,
        _to_dict(state.get("tech")) or None,
    )
    integration = IntegrationOutput.model_validate(raw)

    tech = _to_dict(state.get("tech"))
    scaffold = tech.get("scaffold", {}) if isinstance(tech, dict) else {}

    writable_files, dropped_files = _filter_writable_integration_files(
        integration.files,
        integration_project_dir,
        scaffold,
    )

    payload = {
        "files": writable_files,
        "scaffold": scaffold,
    }

    path = generate_project(str(integration_project_dir), payload)

    notes = integration.integration_notes or (
        f"Generated {len(integration.files)} valid source files."
    )
    if dropped_files:
        dropped_preview = ", ".join(sorted(dropped_files)[:10])
        notes += (
            f" Skipped {len(dropped_files)} files not writable by scaffold/project state"
            f": {dropped_preview}{', ...' if len(dropped_files) > 10 else ''}."
        )
    if not writable_files:
        notes += " No files were applied."

    integration = integration.model_copy(
        update={
            "files": writable_files,
            "integration_notes": notes,
        }
    )

    return {
        "integration": integration,
        "generated_project_path": path,
    }

def build_node(state: StudioState):
    print("-> build_node", file=sys.stderr)

    integration = state.get("integration")
    prebuild_errors = []
    if integration is not None:
        prebuild_errors = [
            str(item).strip()
            for item in getattr(integration, "prebuild_validation_errors", [])
            if str(item).strip()
        ]

    if prebuild_errors:
        stderr = "Pre-build C validation failed before compilation:\n" + "\n".join(
            f"- {issue}" for issue in prebuild_errors[:20]
        )
        build_output = BuildOutput.model_validate(
            _build_failure_payload(
                stderr,
                "Build skipped due to malformed generated C includes/prototypes.",
            )
        )
        project_path = state.get("generated_project_path")
        return {
            "build_output": build_output,
            "generated_project_path": str(Path(project_path).resolve()) if project_path else "",
        }

    project_path = state.get("generated_project_path")
    if not project_path:
        build_output = BuildOutput.model_validate(
            _build_failure_payload(
                "generated_project_path is missing before build_node.",
                "Build skipped because integration did not provide a project path.",
            )
        )
        return {
            "build_output": build_output,
            "generated_project_path": "",
        }

    requested_project_path = Path(project_path).resolve()

    if not _is_valid_cpct_scaffold(requested_project_path):
        build_output = BuildOutput.model_validate(
            _build_failure_payload(
                f"Invalid CPCtelera scaffold: {requested_project_path}",
                "Build skipped because the integration path is not a valid CPCtelera project.",
            )
        )
        return {
            "build_output": build_output,
            "generated_project_path": str(requested_project_path),
        }

    if not _is_build_path_compatible(requested_project_path):
        build_output = BuildOutput.model_validate(
            _build_failure_payload(
                f"Build path mismatch risk for: {requested_project_path}",
                "Build skipped to avoid compiling a different directory than integration_node used.",
            )
        )
        return {
            "build_output": build_output,
            "generated_project_path": str(requested_project_path),
        }

    build_raw, resolved_project_path = run_build(str(requested_project_path))
    if Path(resolved_project_path).resolve() != requested_project_path:
        build_output = BuildOutput.model_validate(
            _build_failure_payload(
                (
                    "Build agent resolved a different project path than integration_node used. "
                    f"requested={requested_project_path} resolved={resolved_project_path}"
                ),
                "Build aborted to preserve integration/build path consistency.",
            )
        )
        return {
            "build_output": build_output,
            "generated_project_path": str(requested_project_path),
        }

    build_output = BuildOutput.model_validate(build_raw)

    return {
        "build_output": build_output,
        "generated_project_path": str(requested_project_path),
    }


def build_validation_node(state: StudioState):
    print("-> build_validation_node", file=sys.stderr)
    raw = run_build_validation(
        state["user_request"],
        state.get("generated_project_path"),
        _to_dict(state.get("build_output")),
    )

    return {
        "build_validation": BuildValidationOutput.model_validate(raw)
    }


def qa_node(state: StudioState):
    print("-> qa_node", file=sys.stderr)
    raw = run_qa(
        state["user_request"],
        _to_dict(state.get("orchestrator")) or None,
        _to_dict(state.get("design")) or None,
        _to_dict(state.get("art")) or None,
        _to_dict(state.get("tech")) or None,
        _to_dict(state.get("integration")) or None,
        _to_dict(state.get("build_validation")) or None,
        _to_dict(state.get("build_output")) or None,
    )

    return {
        "qa": QAOutput.model_validate(raw)
    }


def compose_node(state: StudioState):
    parts = ["# CPC Studio Output", ""]
    if state.get("orchestrator"):
        parts += ["## Orchestrator", _json_block("spec", state["orchestrator"]), ""]
    if state.get("narrative"):
        parts += ["## Narrative", _json_block("narrative", state["narrative"]), ""]
    if state.get("design"):
        parts += ["## Design", _json_block("design", state["design"]), ""]
    if state.get("art"):
        parts += ["## Art", _json_block("art", state["art"]), ""]
    if state.get("tech"):
        parts += ["## Tech", _json_block("tech", state["tech"]), ""]
    contract_validation = state.get("contractvalidation") or state.get("contract_validation")
    if contract_validation:
        parts += [
            "## Contract Validation",
            _json_block("contract_validation", contract_validation),
            "",
        ]
    if state.get("integration"):
        parts += ["## Integration", state["integration"].integration_notes, ""]
        prebuild_errors = state["integration"].prebuild_validation_errors
        if prebuild_errors:
            parts += ["Pre-build Validation Errors:", "\n".join(prebuild_errors[:20]), ""]
    if state.get("build_output"):
        bo = state["build_output"]
        status = "OK" if bo.success else f"FAILED (exit {bo.return_code})"
        parts += ["## Build", f"Status: {status}", bo.build_notes, ""]
        if bo.artifacts:
            parts += ["Artifacts: " + ", ".join(bo.artifacts), ""]
        if not bo.success and bo.stderr:
            parts += ["Errors:", bo.stderr[:2000], ""]
    if state.get("build_validation"):
        parts += ["## Build Validation", _json_block("build_validation", state["build_validation"]), ""]
    if state.get("qa"):
        parts += ["## QA", _json_block("qa", state["qa"]), ""]

    return {"final_output": "\n".join(parts).strip()}


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
builder.add_edge("orchestrator_node", "narrative_node")
builder.add_edge("narrative_node", "design_node")
builder.add_edge("design_node", "art_node")
builder.add_edge("art_node", "tech_node")
builder.add_edge("tech_node", "contractvalidationnode")
builder.add_conditional_edges(
    "contractvalidationnode",
    _route_after_contractvalidation,
    {
        "integration_node": "integration_node",
        "compose_node": "compose_node",
    },
)
builder.add_edge("integration_node", "build_node")
builder.add_edge("build_node", "build_validation_node")
builder.add_edge("build_validation_node", "qa_node")
builder.add_edge("qa_node", "compose_node")
builder.add_edge("compose_node", END)

graph = builder.compile()


def run_studio(user_request: str):
    return graph.invoke({
        "user_request": user_request,
        "target_platform": "Amstrad CPC 6128",
        "framework": "CPCtelera",
    })
