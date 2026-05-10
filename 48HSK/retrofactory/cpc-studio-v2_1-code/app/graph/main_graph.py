from pathlib import Path
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
from app.services.project_service import generate_project

GENERATED_DIR = Path(__file__).resolve().parents[2] / "generated_projects" / "latest_project"


def router_node(state: StudioState):
    print("-> router_node")
    decision = run_orchestrator(state["user_request"])
    return {"route": decision.route}


def narrative_node(state: StudioState):
    print("-> narrative_node")
    return {"narrative": run_narrative(state["user_request"])}


def design_node(state: StudioState):
    print("-> design_node")
    extra = ""
    if state.get("narrative"):
        n = state["narrative"]
        extra = f"Premise: {n.premise}\nTone: {n.tone}\nCharacters: {', '.join(n.characters)}"
    return {"design": run_design(state["user_request"], extra)}


def art_node(state: StudioState):
    print("-> art_node")
    extra = state.get("design").gameplay_spec if state.get("design") else ""
    return {"art": run_art(state["user_request"], extra)}


def tech_node(state: StudioState):
    print("-> tech_node")
    parts = []
    if state.get("design"):
        parts.append(state["design"].gameplay_spec)
    if state.get("art"):
        parts.append(state["art"].art_spec)
    return {"tech": run_tech(state["user_request"], "\n".join(parts))}


def qa_node(state: StudioState):
    print("-> qa_node")
    extra = state.get("tech").implementation_plan if state.get("tech") else ""
    return {"qa": run_qa(state["user_request"], extra)}


def integration_node(state: StudioState):
    print("-> integration_node")
    integration = run_integrator()
    payload = {
        "video_mode": state.get("tech").recommended_video_mode if state.get("tech") else "Mode 1",
        "gameplay_spec": state.get("design").gameplay_spec if state.get("design") else "",
        "art_spec": state.get("art").art_spec if state.get("art") else "",
        "implementation_plan": state.get("tech").implementation_plan if state.get("tech") else "",
    }
    path = generate_project(str(GENERATED_DIR), payload)
    return {"integration": integration, "generated_project_path": path}


def build_validation_node(state: StudioState):
    print("-> build_validation_node")
    build_output = state.get("build_output")
    return {"build_validation": run_build_validation(build_output)}


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
    if state.get("design"):
        parts += ["## Design", state["design"].gameplay_spec, ""]
    if state.get("art"):
        parts += ["## Art", state["art"].art_spec, ""]
    if state.get("tech"):
        parts += ["## Tech", state["tech"].implementation_plan, ""]
    if state.get("qa"):
        parts += ["## QA", state["qa"].performance_check, ""]
    if state.get("integration"):
        parts += ["## Integration", state["integration"].integration_notes, ""]
    if state.get("build_validation"):
        parts += ["## Build Validation", state["build_validation"].validation_notes, ""]
    if state.get("build_output"):
        bo = state["build_output"]
        status = "OK" if bo.success else f"FAILED (exit {bo.return_code})"
        parts += ["## Build", f"Status: {status}", bo.build_notes, ""]
        if bo.artifacts:
            parts += ["Artifacts: " + ", ".join(bo.artifacts), ""]
        if not bo.success and bo.stderr:
            parts += ["Errors:", bo.stderr[:2000], ""]
    return {"final_output": "\n".join(parts).strip()}


def route_selector(state: StudioState):
    return "narrative_node" if state["route"] == "narrative_design_art_tech" else "design_node"


builder = StateGraph(StudioState)
builder.add_node("router_node", router_node)
builder.add_node("narrative_node", narrative_node)
builder.add_node("design_node", design_node)
builder.add_node("art_node", art_node)
builder.add_node("tech_node", tech_node)
builder.add_node("qa_node", qa_node)
builder.add_node("integration_node", integration_node)
builder.add_node("build_validation_node", build_validation_node)
builder.add_node("build_node", build_node)
builder.add_node("compose_node", compose_node)

builder.add_edge(START, "router_node")
builder.add_conditional_edges("router_node", route_selector, {"narrative_node": "narrative_node", "design_node": "design_node"})
builder.add_edge("narrative_node", "design_node")
builder.add_edge("design_node", "art_node")
builder.add_edge("art_node", "tech_node")
builder.add_edge("tech_node", "qa_node")
builder.add_edge("qa_node", "integration_node")
builder.add_edge("integration_node", "build_node")
builder.add_edge("build_node", "build_validation_node")
builder.add_edge("build_validation_node", "compose_node")
builder.add_edge("compose_node", END)

graph = builder.compile()


def run_studio(user_request: str):
    return graph.invoke({
        "user_request": user_request,
        "target_platform": "Amstrad CPC 6128",
        "framework": "CPCtelera",
    })
