from pathlib import Path
import json

from langgraph.graph import StateGraph, START, END
from app.state.studio_state import StudioState
from app.agents.orchestrator_agent import run as run_orchestrator
from app.agents.narrative_agent import run as run_narrative
from app.agents.design_agent import run as run_design
from app.agents.art_agent import run as run_art
from app.agents.cpctelera_tech_agent import run as run_tech
from app.agents.qa_agent import run as run_qa
from app.agents.code_integrator_agent import run as run_integrator
from app.agents.build_validation_agent import run as run_build_validation
from app.agents.build_agent import run as run_build
from app.services.file_service import write_text
from app.services.project_service import generate_project

GENERATED_DIR = Path(__file__).resolve().parents[2] / "generated_projects" / "latest_project"


def _json_block(title: str, payload: dict | None) -> str:
    if not payload:
        return ""
    return f"{title}:\n" + json.dumps(payload, ensure_ascii=False, indent=2)


def orchestrator_node(state: StudioState):
    print("-> orchestrator_node")
    return {"orchestrator": run_orchestrator(state["user_request"])}


def narrative_node(state: StudioState):
    print("-> narrative_node")
    return {
        "narrative": run_narrative(
            state["user_request"],
            state.get("orchestrator"),
        )
    }


def design_node(state: StudioState):
    print("-> design_node")
    return {
        "design": run_design(
            state["user_request"],
            state.get("orchestrator"),
            state.get("narrative"),
        )
    }


def art_node(state: StudioState):
    print("-> art_node")
    return {
        "art": run_art(
            state["user_request"],
            state.get("orchestrator"),
            state.get("narrative"),
            state.get("design"),
        )
    }


def tech_node(state: StudioState):
    print("-> tech_node")
    return {
        "tech": run_tech(
            state["user_request"],
            state.get("orchestrator"),
            state.get("narrative"),
            state.get("design"),
            state.get("art"),
        )
    }


def qa_node(state: StudioState):
    print("-> qa_node")
    return {
        "qa": run_qa(
            state["user_request"],
            state.get("orchestrator"),
            state.get("design"),
            state.get("art"),
            state.get("tech"),
            state.get("integration"),
            state.get("build_validation"),
            state.get("build_output"),
        )
    }


def integration_node(state: StudioState):
    print("-> integration_node")
    integration = run_integrator(
        state["user_request"],
        state.get("orchestrator"),
        state.get("narrative"),
        state.get("design"),
        state.get("art"),
        state.get("tech"),
    )

    design = state.get("design") or {}
    art = state.get("art") or {}
    tech = state.get("tech") or {}

    payload = {
        "video_mode": tech.get("video_mode", "Mode 1"),
        "gameplay_spec": json.dumps(design, ensure_ascii=False, indent=2),
        "art_spec": json.dumps(art, ensure_ascii=False, indent=2),
        "implementation_plan": json.dumps(tech, ensure_ascii=False, indent=2),
    }
    path = generate_project(str(GENERATED_DIR), payload)

    applied = 0
    generated_path = Path(path)
    for rel_path, content in (integration.get("files") or {}).items():
        normalized = str(rel_path).strip().replace("\\", "/")
        if not normalized.startswith("src/"):
            continue
        write_text(generated_path / normalized, str(content))
        applied += 1

    integration_result = dict(integration)
    integration_result["integration_notes"] = f"Applied {applied} source files from CodeIntegratorAgent."

    return {"integration": integration_result, "generated_project_path": path}


def build_validation_node(state: StudioState):
    print("-> build_validation_node")
    return {
        "build_validation": run_build_validation(
            state["user_request"],
            state.get("generated_project_path"),
            state.get("build_output"),
        )
    }


def build_node(state: StudioState):
    print("-> build_node")
    project_path = state.get("generated_project_path", "")
    build_output, resolved_project_path = run_build(project_path)
    return {
        "build_output": build_output,
        "generated_project_path": resolved_project_path,
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
    if state.get("qa"):
        parts += ["## QA", _json_block("qa", state["qa"]), ""]
    if state.get("integration"):
        parts += ["## Integration", state["integration"].get("integration_notes", ""), ""]
    if state.get("build_validation"):
        parts += ["## Build Validation", _json_block("build_validation", state["build_validation"]), ""]
    if state.get("build_output"):
        bo = state["build_output"]
        status = "OK" if bo.get("success") else f"FAILED (exit {bo.get('return_code')})"
        parts += ["## Build", f"Status: {status}", bo.get("build_notes", ""), ""]
        if bo.get("artifacts"):
            parts += ["Artifacts: " + ", ".join(bo.get("artifacts", [])), ""]
        if not bo.get("success") and bo.get("stderr"):
            parts += ["Errors:", bo.get("stderr", "")[:2000], ""]
    return {"final_output": "\n".join(parts).strip()}


builder = StateGraph(StudioState)
builder.add_node("orchestrator_node", orchestrator_node)
builder.add_node("narrative_node", narrative_node)
builder.add_node("design_node", design_node)
builder.add_node("art_node", art_node)
builder.add_node("tech_node", tech_node)
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
builder.add_edge("tech_node", "integration_node")
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
