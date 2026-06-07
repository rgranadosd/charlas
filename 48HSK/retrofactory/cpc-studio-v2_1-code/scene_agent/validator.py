"""Scene + render-plan coherence validator."""
from __future__ import annotations

from .schemas import RenderPlan, SceneSpec, ValidationIssue, ValidationReport

_SCORE_WORDS = ("score", "marcador", "puntos", "hud", "contador")
_INTERACTIVE_ENTITY_TYPES = {"paddle", "player", "character"}


def _issue(level: str, code: str, message: str, entity_id: str | None = None) -> ValidationIssue:
    return ValidationIssue(level=level, code=code, message=message, entity_id=entity_id)


def validate(scene: SceneSpec, render_plan: RenderPlan) -> ValidationReport:
    issues: list[ValidationIssue] = []
    entity_ids = {e.id for e in scene.entities}
    layer_names = {l.name for l in scene.layers}
    entity_by_id = {e.id: e for e in scene.entities}

    # --- structural checks ---

    # Duplicate layer orders
    orders = [l.order for l in scene.layers]
    if len(orders) != len(set(orders)):
        issues.append(_issue("error", "DUPLICATE_LAYER_ORDER",
                             "Two or more layers share the same draw order."))

    # All entity_ids in layers must exist
    for layer in scene.layers:
        for eid in layer.entities:
            if eid not in entity_ids:
                issues.append(_issue("error", "MISSING_ENTITY_IN_LAYER",
                                     f"Layer '{layer.name}' references unknown entity '{eid}'.",
                                     entity_id=eid))

    # All entity_ids in render plan must exist
    for step in render_plan.steps:
        if step.entity_id and step.entity_id not in entity_ids:
            issues.append(_issue("error", "MISSING_ENTITY_IN_RENDER",
                                 f"RenderStep references unknown entity '{step.entity_id}'.",
                                 entity_id=step.entity_id))

    # --- semantic / domain checks ---

    # HUD must exist if scene description mentions a score/HUD
    desc_l = scene.description.lower()
    has_score_intent = any(w in desc_l for w in _SCORE_WORDS)
    has_hud_layer = "hud" in layer_names
    has_score_entity = any(e.type == "text" and e.layer == "hud" for e in scene.entities)

    if has_score_intent and not has_hud_layer:
        issues.append(_issue("error", "MISSING_HUD_LAYER",
                             "Prompt mentions a score/HUD but no 'hud' layer was defined."))
    if has_score_intent and not has_score_entity:
        issues.append(_issue("error", "MISSING_SCORE_ENTITY",
                             "Prompt mentions a score but no text entity in the 'hud' layer exists."))

    # At least one interactive entity (paddle/player)
    has_interactive = any(e.type in _INTERACTIVE_ENTITY_TYPES for e in scene.entities)
    if not has_interactive:
        issues.append(_issue("warning", "NO_INTERACTIVE_ENTITY",
                             "No interactive entity (paddle, player…) found. Add one if the prompt implies user input."))

    # Controls reference existing entities
    for ctrl in scene.controls:
        if ctrl.entity_id not in entity_ids:
            issues.append(_issue("error", "CONTROL_MISSING_ENTITY",
                                 f"Control '{ctrl.action}' references unknown entity '{ctrl.entity_id}'.",
                                 entity_id=ctrl.entity_id))

    # --- render order checks ---

    steps_with_layer = [(s.layer, i) for i, s in enumerate(render_plan.steps) if s.layer]
    layer_first_step: dict[str, int] = {}
    for layer_name, idx in steps_with_layer:
        if layer_name not in layer_first_step:
            layer_first_step[layer_name] = idx

    hud_start = layer_first_step.get("hud", -1)
    entities_start = layer_first_step.get("entities", -1)

    if hud_start != -1 and entities_start != -1 and hud_start < entities_start:
        issues.append(_issue("error", "HUD_RENDERED_BEFORE_ENTITIES",
                             "HUD layer is rendered before the entities layer. "
                             "This would cause entities to overwrite the score."))

    # --- informational ---

    if scene.hypotheses:
        for h in scene.hypotheses:
            issues.append(_issue("info", "HYPOTHESIS", h))

    ok = not any(i.level == "error" for i in issues)
    return ValidationReport(scene_id=scene.id, ok=ok, issues=issues)
