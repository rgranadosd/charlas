import json

from app.services.llm_service import json_call


def _as_list(value) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [str(value).strip()]


def run(user_request: str, orchestrator_output: dict | None = None) -> dict:
    extra_context = ""
    if orchestrator_output:
        extra_context = "Orchestrator JSON:\n" + json.dumps(orchestrator_output, ensure_ascii=False, indent=2)

    payload = json_call("narrative", user_request, extra_context)
    return {
        "theme": str(payload.get("theme", "")).strip(),
        "tone": str(payload.get("tone", "")).strip(),
        "setting": str(payload.get("setting", "")).strip(),
        "player_role": str(payload.get("player_role", "")).strip(),
        "goal_fiction": str(payload.get("goal_fiction", "")).strip(),
        "enemy_fantasy": _as_list(payload.get("enemy_fantasy")),
        "world_keywords": _as_list(payload.get("world_keywords")),
        "hud_text_style": str(payload.get("hud_text_style", "")).strip(),
    }
