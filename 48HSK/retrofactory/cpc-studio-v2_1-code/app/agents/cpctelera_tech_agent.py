import json

from app.services.llm_service import json_call
from app.services.resource_service import format_resources_for_prompt

CORE_GAME_H = "src/game.h"
CORE_GAME_C = "src/game.c"
LEGACY_SCENE_GAME_C = "src/scene_game.c"


def _as_list(value) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [str(value).strip()]


def _as_dict(value) -> dict:
    return value if isinstance(value, dict) else {}


def _unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _ensure_core_scaffold(scaffold: dict) -> dict:
    allowed_files = _as_list(scaffold.get("allowed_files"))
    overwrite_files = _as_list(scaffold.get("overwrite_files"))
    create_if_missing = _as_list(scaffold.get("create_if_missing"))

    # game.c is now the main loop module. Keep scene_game optional, not central.
    allowed_files = [path for path in allowed_files if path != LEGACY_SCENE_GAME_C]
    overwrite_files = [path for path in overwrite_files if path != LEGACY_SCENE_GAME_C]
    create_if_missing = [path for path in create_if_missing if path != LEGACY_SCENE_GAME_C]

    for core_path in (CORE_GAME_H, CORE_GAME_C):
        allowed_files.append(core_path)
        overwrite_files.append(core_path)
        create_if_missing.append(core_path)

    return {
        "allowed_files": _unique(allowed_files),
        "overwrite_files": _unique(overwrite_files),
        "create_if_missing": _unique(create_if_missing),
    }


def run(
    user_request: str,
    orchestrator_output: dict | None = None,
    narrative_output: dict | None = None,
    design_output: dict | None = None,
    art_output: dict | None = None,
) -> dict:
    blocks = []
    if orchestrator_output:
        blocks.append("Orchestrator JSON:\n" + json.dumps(orchestrator_output, ensure_ascii=False, indent=2))
    if narrative_output:
        blocks.append("Narrative JSON:\n" + json.dumps(narrative_output, ensure_ascii=False, indent=2))
    if design_output:
        blocks.append("Design JSON:\n" + json.dumps(design_output, ensure_ascii=False, indent=2))
    if art_output:
        blocks.append("Art JSON:\n" + json.dumps(art_output, ensure_ascii=False, indent=2))

    resource_context = format_resources_for_prompt("cpctelera_tech_agent", user_request, limit=6)
    if resource_context:
        blocks.append(resource_context)

    payload = json_call("cpctelera_tech", user_request, "\n\n".join(blocks))
    scaffold = _ensure_core_scaffold(_as_dict(payload.get("scaffold")))

    return {
        "archetype": str(payload.get("archetype", "")).strip(),
        "video_mode": str(payload.get("video_mode", "Mode 1")).strip() or "Mode 1",
        "level_structure": str(payload.get("level_structure", "")).strip(),
        "camera": str(payload.get("camera", "")).strip(),
        "modules": _as_list(payload.get("modules")),
        "input_model": _as_dict(payload.get("input_model")),
        "entity_model": _as_dict(payload.get("entity_model")),
        "collision_model": _as_dict(payload.get("collision_model")),
        "rendering_model": _as_dict(payload.get("rendering_model")),
        "data_model": _as_dict(payload.get("data_model")),
        "update_order": _as_list(payload.get("update_order")),
        "scaffold": scaffold,
    }
