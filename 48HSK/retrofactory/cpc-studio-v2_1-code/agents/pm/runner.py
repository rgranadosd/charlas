"""Mock runner — simulates frame rendering without compiling CPCtelera code."""
from __future__ import annotations

from .schemas import RenderPlan, SceneSpec


def run(scene: SceneSpec, render_plan: RenderPlan) -> dict:
    frame_log: list[str] = []
    entity_by_id = {e.id: e for e in scene.entities}

    for step in render_plan.steps:
        if step.operation == "clear":
            frame_log.append(f"[{step.layer}] CLEAR layer")
        elif step.operation == "fill_rect":
            color = step.params.get("color", "?")
            frame_log.append(f"[{step.layer}] FILL_RECT color={color}")
        elif step.operation == "draw_sprite":
            eid = step.entity_id or "?"
            entity = entity_by_id.get(eid)
            pos = entity.position if entity else None
            frame_log.append(
                f"[{step.layer}] DRAW_SPRITE id={eid} "
                f"pos=({pos.x},{pos.y})" if pos else f"[{step.layer}] DRAW_SPRITE id={eid}"
            )
        elif step.operation == "draw_string":
            eid = step.entity_id or "?"
            value = step.params.get("value", "?")
            entity = entity_by_id.get(eid)
            pos = entity.position if entity else None
            frame_log.append(
                f"[{step.layer}] DRAW_STRING id={eid} value='{value}' "
                f"pos=({pos.x},{pos.y})" if pos else f"[{step.layer}] DRAW_STRING id={eid}"
            )
        else:
            frame_log.append(f"[{step.layer}] {step.operation.upper()}")

    return {
        "mode": "mock",
        "scene_id": scene.id,
        "frames_simulated": 1,
        "frame_log": frame_log,
        "status": "ok",
    }
