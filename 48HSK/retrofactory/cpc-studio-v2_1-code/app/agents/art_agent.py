import json

from app.services.llm_service import json_call
from app.services.resource_service import format_resources_for_prompt


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
    design_output: dict | None = None,
) -> dict:
    blocks = []
    if orchestrator_output:
        blocks.append("Orchestrator JSON:\n" + json.dumps(orchestrator_output, ensure_ascii=False, indent=2))
    if narrative_output:
        blocks.append("Narrative JSON:\n" + json.dumps(narrative_output, ensure_ascii=False, indent=2))
    if design_output:
        blocks.append("Design JSON:\n" + json.dumps(design_output, ensure_ascii=False, indent=2))

    resource_context = format_resources_for_prompt("graphics_agent", user_request, limit=5)
    if resource_context:
        blocks.append(resource_context)

    payload = json_call("art", user_request, "\n\n".join(blocks))
    return {
        "video_mode_recommendation": str(payload.get("video_mode_recommendation", "")).strip(),
        "palette_strategy": str(payload.get("palette_strategy", "")).strip(),
        "tileset_plan": _as_list(payload.get("tileset_plan")),
        "sprite_plan": _as_list(payload.get("sprite_plan")),
        "hud_plan": _as_list(payload.get("hud_plan")),
        "asset_list": _as_list(payload.get("asset_list")),
        "conversion_hints": _as_list(payload.get("conversion_hints")),
    }
