"""arkanoid_prompt_case — acceptance test for the scene agent pipeline."""
from __future__ import annotations

import pytest

from scene_agent.main import run_pipeline
from scene_agent.schemas import SceneSpec, RenderPlan, ValidationReport

ARKANOID_PROMPT = (
    "Créame una pantalla estilo Arkanoid con fondo azul, letras wso2 formadas por bloques, "
    "un marcador de puntos en la esquina superior derecha, una pala en la parte inferior "
    "y una pelota que rebote. La pala se controla horizontalmente con el teclado. "
    "El render debe dibujarse por capas para que el marcador y los objetos no se pisen."
)


@pytest.fixture(scope="module")
def output(tmp_path_factory):
    out_dir = str(tmp_path_factory.mktemp("outputs"))
    return run_pipeline(ARKANOID_PROMPT, output_dir=out_dir)


# ---------------------------------------------------------------------------
# SceneSpec
# ---------------------------------------------------------------------------

def test_scene_has_four_layers(output):
    layer_names = {l.name for l in output.scene_spec.layers}
    assert layer_names >= {"background", "playfield", "entities", "hud"}


def test_layers_have_unique_draw_order(output):
    orders = [l.order for l in output.scene_spec.layers]
    assert len(orders) == len(set(orders))


def test_hud_has_highest_draw_order(output):
    layers_by_name = {l.name: l.order for l in output.scene_spec.layers}
    assert layers_by_name["hud"] > layers_by_name["entities"]
    assert layers_by_name["hud"] > layers_by_name.get("playfield", -1)


def test_scene_has_required_entities(output):
    entity_ids = {e.id for e in output.scene_spec.entities}
    assert "paddle" in entity_ids
    assert "ball" in entity_ids
    assert "score" in entity_ids


def test_paddle_is_in_entities_layer(output):
    paddle = next(e for e in output.scene_spec.entities if e.id == "paddle")
    assert paddle.layer == "entities"


def test_score_is_in_hud_layer(output):
    score = next(e for e in output.scene_spec.entities if e.id == "score")
    assert score.layer == "hud"
    assert score.type == "text"


def test_blocks_letters_detected(output):
    entity_ids = {e.id for e in output.scene_spec.entities}
    assert "blocks_letters" in entity_ids


def test_background_is_blue(output):
    assert output.scene_spec.background_color == "blue"


def test_wso2_text_in_blocks_letters(output):
    blocks = next(e for e in output.scene_spec.entities if e.id == "blocks_letters")
    assert "WSO2" in blocks.properties.get("text", "")


def test_score_position_is_right(output):
    score = next(e for e in output.scene_spec.entities if e.id == "score")
    assert score.position is not None
    assert score.position.x == "right"


# ---------------------------------------------------------------------------
# Controls
# ---------------------------------------------------------------------------

def test_paddle_has_horizontal_controls(output):
    paddle_controls = [c for c in output.scene_spec.controls if c.entity_id == "paddle"]
    assert len(paddle_controls) >= 2
    axes = {c.axis for c in paddle_controls}
    assert "horizontal" in axes


def test_cursor_keys_assigned(output):
    keys = {c.key for c in output.scene_spec.controls}
    assert "Key_CursorLeft" in keys
    assert "Key_CursorRight" in keys


# ---------------------------------------------------------------------------
# RenderPlan
# ---------------------------------------------------------------------------

def test_render_plan_strategy_is_full_redraw(output):
    assert output.render_plan.strategy == "full_redraw_per_frame"


def test_hud_rendered_after_entities(output):
    steps = output.render_plan.steps
    layers_in_order = [s.layer for s in steps]
    assert "hud" in layers_in_order
    assert "entities" in layers_in_order
    assert layers_in_order.index("hud") > layers_in_order.index("entities"), (
        "HUD must be rendered after entities to prevent score being overwritten"
    )


def test_background_rendered_first(output):
    steps = output.render_plan.steps
    layers_in_order = [s.layer for s in steps]
    assert layers_in_order[0] == "background"


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def test_validation_passes(output):
    assert output.validation_report.ok is True


def test_no_validation_errors(output):
    errors = [i for i in output.validation_report.issues if i.level == "error"]
    assert errors == [], f"Unexpected errors: {[e.message for e in errors]}"


def test_validation_includes_hypotheses(output):
    infos = [i for i in output.validation_report.issues if i.level == "info"]
    assert len(infos) > 0, "Expected at least one hypothesis note in the report"


# ---------------------------------------------------------------------------
# Artifacts
# ---------------------------------------------------------------------------

def test_artifacts_produced(output):
    assert "scene_spec.json" in output.artifacts
    assert "render_plan.json" in output.artifacts
    assert "validation_report.json" in output.artifacts


def test_artifact_files_exist(output):
    from pathlib import Path
    for path in output.artifacts.values():
        assert Path(path).exists(), f"Missing artifact: {path}"


# ---------------------------------------------------------------------------
# Simulation
# ---------------------------------------------------------------------------

def test_simulation_ok(output):
    assert output.simulation["status"] == "ok"


def test_simulation_frame_log_covers_all_layers(output):
    log = " ".join(output.simulation["frame_log"])
    for layer in ("background", "playfield", "entities", "hud"):
        assert f"[{layer}]" in log, f"Layer '{layer}' missing from simulation frame log"


# ---------------------------------------------------------------------------
# Generic reuse guarantee
# ---------------------------------------------------------------------------

def test_schema_accepts_different_prompt(tmp_path):
    """SceneSpec is generic: a space-shooter prompt must also produce a valid scene."""
    from scene_agent.main import run_pipeline as rp
    shooter_prompt = (
        "Una pantalla de space shooter con fondo negro, naves enemigas, "
        "una nave del jugador en la parte inferior y un marcador de vidas y puntos en la esquina superior izquierda."
    )
    out = rp(shooter_prompt, output_dir=str(tmp_path))
    assert out.validation_report.ok
    layer_names = {l.name for l in out.scene_spec.layers}
    assert "entities" in layer_names
    assert "hud" in layer_names
