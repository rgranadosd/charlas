"""Scene editor — structured modifications to an existing SceneSpec.

Every function returns a NEW SceneSpec (immutable update pattern).
The caller is responsible for re-validating after edits.
"""
from __future__ import annotations

from .schemas import ControlSpec, EntitySpec, LayerSpec, SceneSpec


def add_entity(scene: SceneSpec, entity: EntitySpec) -> SceneSpec:
    """Add an entity and register it in the appropriate layer."""
    entities = list(scene.entities) + [entity]
    layers = []
    for layer in scene.layers:
        if layer.name == entity.layer:
            updated_ids = list(layer.entities) + [entity.id]
            layers.append(layer.model_copy(update={"entities": updated_ids}))
        else:
            layers.append(layer)
    # Create the layer if it didn't exist yet
    existing_names = {l.name for l in layers}
    if entity.layer not in existing_names:
        order = max((l.order for l in layers), default=-1) + 1
        layers.append(LayerSpec(name=entity.layer, order=order, entities=[entity.id]))
    return scene.model_copy(update={"entities": entities, "layers": layers})


def remove_entity(scene: SceneSpec, entity_id: str) -> SceneSpec:
    """Remove an entity and unregister it from its layer."""
    entities = [e for e in scene.entities if e.id != entity_id]
    layers = [
        layer.model_copy(update={"entities": [eid for eid in layer.entities if eid != entity_id]})
        for layer in scene.layers
    ]
    return scene.model_copy(update={"entities": entities, "layers": layers})


def update_entity(scene: SceneSpec, entity_id: str, **fields) -> SceneSpec:
    """Return a scene with one entity's fields updated."""
    entities = [
        e.model_copy(update=fields) if e.id == entity_id else e
        for e in scene.entities
    ]
    return scene.model_copy(update={"entities": entities})


def add_control(scene: SceneSpec, control: ControlSpec) -> SceneSpec:
    controls = list(scene.controls) + [control]
    return scene.model_copy(update={"controls": controls})


def set_background_color(scene: SceneSpec, color: str) -> SceneSpec:
    entities = [
        e.model_copy(update={"color": color}) if e.type == "background" else e
        for e in scene.entities
    ]
    return scene.model_copy(update={"background_color": color, "entities": entities})
