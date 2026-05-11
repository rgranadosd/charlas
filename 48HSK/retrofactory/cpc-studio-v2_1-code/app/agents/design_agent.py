import json

from app.services.llm_service import json_call


def _as_list(value) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [str(value).strip()]


def run(
    user_request: str,
    orchestrator_output: dict | None = None,
    narrative_output: dict | None = None,
) -> dict:
    blocks = []
    if orchestrator_output:
        blocks.append("Orchestrator JSON:\n" + json.dumps(orchestrator_output, ensure_ascii=False, indent=2))
    if narrative_output:
        blocks.append("Narrative JSON:\n" + json.dumps(narrative_output, ensure_ascii=False, indent=2))

    payload = json_call("design", user_request, "\n\n".join(blocks))
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
