"""Scene harness — three categories of tests:

1. CONTRACT  — JSON round-trip and schema conformance
2. BEHAVIOR  — multiple distinct prompts all produce valid scenes
3. EDIT      — SceneSpec mutations preserve contract integrity
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from scene_agent import editor
from scene_agent.main import run_pipeline
from scene_agent.planner import build_render_plan, plan_scene
from scene_agent.schemas import (
    AgentOutput,
    ControlSpec,
    EntitySpec,
    Position,
    PromptInput,
    RenderPlan,
    SceneSpec,
    ValidationReport,
)
from scene_agent.validator import validate

# ---------------------------------------------------------------------------
# 1 · CONTRACT TESTS
# ---------------------------------------------------------------------------

class TestContract:

    def test_scene_spec_round_trips_via_json(self, tmp_path):
        out = run_pipeline("fondo rojo, pala, pelota, marcador", output_dir=str(tmp_path))
        dumped = out.scene_spec.model_dump()
        restored = SceneSpec.model_validate(dumped)
        assert restored == out.scene_spec

    def test_render_plan_round_trips_via_json(self, tmp_path):
        out = run_pipeline("fondo negro, pala, pelota, marcador de puntos", output_dir=str(tmp_path))
        dumped = out.render_plan.model_dump()
        restored = RenderPlan.model_validate(dumped)
        assert restored == out.render_plan

    def test_validation_report_round_trips_via_json(self, tmp_path):
        out = run_pipeline("fondo azul, pala, pelota, marcador", output_dir=str(tmp_path))
        dumped = out.validation_report.model_dump()
        restored = ValidationReport.model_validate(dumped)
        assert restored == out.validation_report

    def test_artifact_json_files_are_valid_json(self, tmp_path):
        out = run_pipeline("pala, pelota, marcador", output_dir=str(tmp_path))
        for name, path in out.artifacts.items():
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            assert isinstance(data, dict), f"{name} is not a JSON object"

    def test_artifact_scene_spec_matches_schema(self, tmp_path):
        out = run_pipeline("pala, pelota, marcador", output_dir=str(tmp_path))
        raw = json.loads(Path(out.artifacts["scene_spec.json"]).read_text())
        scene = SceneSpec.model_validate(raw)
        assert scene.id == out.scene_spec.id

    def test_all_layer_entity_ids_exist_in_entities(self, tmp_path):
        out = run_pipeline("fondo verde, pala, pelota, marcador, ladrillo", output_dir=str(tmp_path))
        entity_ids = {e.id for e in out.scene_spec.entities}
        for layer in out.scene_spec.layers:
            for eid in layer.entities:
                assert eid in entity_ids, f"Layer '{layer.name}' references missing entity '{eid}'"

    def test_render_steps_reference_valid_entities(self, tmp_path):
        out = run_pipeline("pala, pelota, marcador", output_dir=str(tmp_path))
        entity_ids = {e.id for e in out.scene_spec.entities}
        for step in out.render_plan.steps:
            if step.entity_id:
                assert step.entity_id in entity_ids


# ---------------------------------------------------------------------------
# 2 · BEHAVIOR TESTS — prompt variations
# ---------------------------------------------------------------------------

PROMPT_CASES = [
    pytest.param(
        "Una pantalla estilo Arkanoid con fondo azul, letras wso2 formadas por bloques, "
        "marcador en la esquina superior derecha, pala y pelota con control horizontal.",
        {"paddle", "ball", "score", "blocks_letters"},
        {"background", "playfield", "entities", "hud"},
        id="arkanoid",
    ),
    pytest.param(
        "Space shooter: fondo negro estrellado, nave del jugador abajo, naves enemigas, "
        "marcador de vidas y puntos en la esquina superior izquierda.",
        {"player", "enemy", "score"},   # nave del jugador → player, not paddle
        {"background", "entities", "hud"},
        id="space_shooter",
    ),
    pytest.param(
        "Juego de plataformas: fondo azul, personaje en la parte izquierda, "
        "marcador de puntos arriba.",
        {"score"},
        {"background", "entities", "hud"},
        id="platformer_minimal",
    ),
    pytest.param(
        "Pantalla de menú principal: fondo negro, marcador de puntuación máxima.",
        {"score"},
        {"background", "hud"},
        id="menu_screen",
    ),
    pytest.param(
        "Puzzle game: fondo gris, piezas como bloques en el campo, "
        "marcador de movimientos en la esquina superior derecha.",
        {"score"},
        {"background", "playfield", "hud"},
        id="puzzle_game",
    ),
]


@pytest.mark.parametrize("prompt,expected_entity_ids,expected_layer_names", PROMPT_CASES)
def test_prompt_produces_valid_scene(prompt, expected_entity_ids, expected_layer_names, tmp_path):
    out = run_pipeline(prompt, output_dir=str(tmp_path))
    assert out.validation_report.ok, (
        f"Validation failed: {[i.message for i in out.validation_report.issues if i.level == 'error']}"
    )
    actual_ids = {e.id for e in out.scene_spec.entities}
    actual_layers = {l.name for l in out.scene_spec.layers}
    assert expected_entity_ids <= actual_ids, f"Missing entities: {expected_entity_ids - actual_ids}"
    assert expected_layer_names <= actual_layers, f"Missing layers: {expected_layer_names - actual_layers}"


@pytest.mark.parametrize("prompt,_ei,_el", PROMPT_CASES)
def test_hud_always_last_when_present(prompt, _ei, _el, tmp_path):
    out = run_pipeline(prompt, output_dir=str(tmp_path))
    layer_orders = {l.name: l.order for l in out.scene_spec.layers}
    if "hud" in layer_orders and "entities" in layer_orders:
        assert layer_orders["hud"] > layer_orders["entities"], (
            "HUD layer must always have higher draw order than entities"
        )


@pytest.mark.parametrize("prompt,_ei,_el", PROMPT_CASES)
def test_hypotheses_always_populated(prompt, _ei, _el, tmp_path):
    out = run_pipeline(prompt, output_dir=str(tmp_path))
    assert out.scene_spec.hypotheses, "Every scene must record at least one planning hypothesis"


def test_unknown_prompt_does_not_crash(tmp_path):
    """Graceful handling of a vague or nonsense prompt."""
    out = run_pipeline("algo con colores", output_dir=str(tmp_path))
    assert out.scene_spec is not None
    assert out.render_plan is not None


# ---------------------------------------------------------------------------
# 3 · EDIT TESTS — mutations preserve contract
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def arkanoid_scene():
    prompt = PromptInput(text=(
        "Arkanoid: fondo azul, letras wso2 en bloques, marcador superior derecha, pala, pelota."
    ))
    return plan_scene(prompt)


class TestEdit:

    def test_add_entity_updates_layer(self, arkanoid_scene):
        new_entity = EntitySpec(id="lives", type="text", layer="hud",
                                position=Position(x="left", y=0),
                                properties={"initial_value": "3", "label": "Lives:"})
        updated = editor.add_entity(arkanoid_scene, new_entity)
        assert any(e.id == "lives" for e in updated.entities)
        hud_layer = next(l for l in updated.layers if l.name == "hud")
        assert "lives" in hud_layer.entities

    def test_add_entity_does_not_mutate_original(self, arkanoid_scene):
        new_entity = EntitySpec(id="power_up", type="sprite", layer="entities")
        editor.add_entity(arkanoid_scene, new_entity)
        assert not any(e.id == "power_up" for e in arkanoid_scene.entities)

    def test_remove_entity_cleans_layer(self, arkanoid_scene):
        updated = editor.remove_entity(arkanoid_scene, "ball")
        assert not any(e.id == "ball" for e in updated.entities)
        for layer in updated.layers:
            assert "ball" not in layer.entities

    def test_update_entity_changes_field(self, arkanoid_scene):
        updated = editor.update_entity(arkanoid_scene, "score",
                                        position=Position(x="left", y=0))
        score = next(e for e in updated.entities if e.id == "score")
        assert score.position.x == "left"

    def test_update_entity_leaves_others_intact(self, arkanoid_scene):
        original_paddle = next(e for e in arkanoid_scene.entities if e.id == "paddle")
        updated = editor.update_entity(arkanoid_scene, "score",
                                        position=Position(x="left", y=0))
        paddle_after = next(e for e in updated.entities if e.id == "paddle")
        assert paddle_after == original_paddle

    def test_add_control_appended(self, arkanoid_scene):
        ctrl = ControlSpec(entity_id="paddle", action="fire", key="Key_Space")
        updated = editor.add_control(arkanoid_scene, ctrl)
        keys = {c.key for c in updated.controls}
        assert "Key_Space" in keys

    def test_change_background_color(self, arkanoid_scene):
        updated = editor.set_background_color(arkanoid_scene, "red")
        assert updated.background_color == "red"
        bg_entity = next((e for e in updated.entities if e.type == "background"), None)
        if bg_entity:
            assert bg_entity.color == "red"

    def test_edited_scene_still_validates(self, arkanoid_scene):
        new_entity = EntitySpec(id="lives", type="text", layer="hud",
                                position=Position(x="left", y=0),
                                properties={"initial_value": "3"})
        ctrl = ControlSpec(entity_id="paddle", action="fire", key="Key_Space")
        updated = editor.add_entity(arkanoid_scene, new_entity)
        updated = editor.add_control(updated, ctrl)
        render_plan = build_render_plan(updated)
        report = validate(updated, render_plan)
        assert report.ok, [i.message for i in report.issues if i.level == "error"]

    def test_removing_score_then_validator_warns(self, arkanoid_scene):
        stripped = editor.remove_entity(arkanoid_scene, "score")
        render_plan = build_render_plan(stripped)
        report = validate(stripped, render_plan)
        codes = {i.code for i in report.issues}
        assert "MISSING_SCORE_ENTITY" in codes
