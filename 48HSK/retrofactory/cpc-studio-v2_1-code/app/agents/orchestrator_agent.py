from app.services.llm_service import json_call


def _as_list(value) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [str(value).strip()]


def run(user_request: str) -> dict:
    payload = json_call("orchestrator", user_request)

    scope = payload.get("scope") if isinstance(payload.get("scope"), dict) else {}
    constraints = payload.get("constraints") if isinstance(payload.get("constraints"), dict) else {}

    return {
        "game_concept": str(payload.get("game_concept", "")).strip(),
        "genre_hint": str(payload.get("genre_hint", "")).strip(),
        "reference_games": _as_list(payload.get("reference_games")),
        "player_fantasy": str(payload.get("player_fantasy", "")).strip(),
        "must_have_features": _as_list(payload.get("must_have_features")),
        "nice_to_have_features": _as_list(payload.get("nice_to_have_features")),
        "scope": {
            "target": str(scope.get("target", "vertical_slice")).strip() or "vertical_slice",
            "complexity": str(scope.get("complexity", "small")).strip() or "small",
        },
        "constraints": {
            "target_platform": str(constraints.get("target_platform", "Amstrad CPC")).strip() or "Amstrad CPC",
            "engine": str(constraints.get("engine", "CPCtelera")).strip() or "CPCtelera",
        },
    }
