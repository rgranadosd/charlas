import os

from app.agents.context_builder import build_agent_extra_context
from app.services.llm_service import json_call


def _as_list(value) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [str(value).strip()]


def _design_retrieval_limit() -> int:
    raw = os.getenv("DESIGN_RETRIEVAL_LIMIT", "4").strip()
    try:
        return max(0, int(raw))
    except ValueError:
        return 4


def run(
    user_request: str,
    orchestrator_output: dict | None = None,
    narrative_output: dict | None = None,
) -> dict:
    extra_context = build_agent_extra_context(
        "design_agent",
        user_request,
        {
            "orchestrator": orchestrator_output or {},
            "narrative": narrative_output or {},
        },
        retrieval_limit=_design_retrieval_limit(),
    )
    payload = json_call("design", user_request, extra_context)
    return {
        "core_loop": str(payload.get("core_loop", "")).strip(),
        "win_condition": str(payload.get("win_condition", "")).strip(),
        "lose_condition": str(payload.get("lose_condition", "")).strip(),
        "player_actions": _as_list(payload.get("player_actions")),
        "game_states": _as_list(payload.get("game_states")),
        "enemy_roles": _as_list(payload.get("enemy_roles")),
        "level_flow": _as_list(payload.get("level_flow")),
        "difficulty_curve": str(payload.get("difficulty_curve", "")).strip(),
        "score_model": str(payload.get("score_model", "")).strip(),
        "lives_model": str(payload.get("lives_model", "")).strip(),
    }
