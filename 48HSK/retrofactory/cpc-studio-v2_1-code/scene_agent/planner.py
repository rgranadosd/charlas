"""Mock planner: converts a natural-language prompt into a SceneSpec + RenderPlan."""
from __future__ import annotations

import re

from .schemas import (
    ControlSpec,
    EntitySpec,
    LayerSpec,
    Position,
    PromptInput,
    RenderPlan,
    RenderStep,
    SceneSpec,
    Size,
)

# ---------------------------------------------------------------------------
# Keyword tables
# ---------------------------------------------------------------------------

_BACKGROUND_COLORS = {
    "azul": "blue", "rojo": "red", "verde": "green",
    "negro": "black", "blanco": "white", "gris": "gray",
}

# Order matters: more specific patterns first.
# Each tuple: (regex on lowercased text, entity_type)
_ENTITY_PATTERNS: list[tuple[str, str]] = [
    # WSO2 blocks — must come before generic "letras" catch
    (r"\bwso2\b", "blocks_letters"),
    # Paddle / player paddle
    (r"pala\b|paddle|barra.*inferior|plataforma", "paddle"),
    # Player (ship, character — distinct from paddle in some genres)
    (r"nave.*jugador|jugador.*nave|personaje|jugador\b|player\b", "player"),
    # Ball
    (r"pelota|bola\b|ball\b", "ball"),
    # Generic letter-blocks (after WSO2 so WSO2 doesn't also match this)
    (r"letras.*bloques|bloques.*letras", "blocks_letters"),
    # HUD elements
    (r"marcador|puntuaci|score|hud|contador|vidas", "score"),
    # Background
    (r"fondo\b|background", "background_fill"),
    # Brick fields
    (r"ladrillo|brick|pieza.*bloque|bloque.*campo|piezas.*campo", "bricks"),
    # Enemies
    (r"enemigo|enemy|nave.*enemi|enemi.*nave", "enemy"),
]

_LAYER_OF: dict[str, str] = {
    "background_fill": "background",
    "blocks_letters":  "playfield",
    "bricks":          "playfield",
    "paddle":          "entities",
    "player":          "entities",
    "ball":            "entities",
    "enemy":           "entities",
    "score":           "hud",
}

_CONTROL_AXIS_PATTERNS = [
    (r"horizontalmente|horizontal|izquierda.*derecha|cursor", "horizontal"),
    (r"verticalmente|vertical|arriba.*abajo", "vertical"),
]

_STANDARD_LAYER_ORDER = ["background", "playfield", "entities", "hud"]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _detect_background_color(text: str) -> str | None:
    for word, color in _BACKGROUND_COLORS.items():
        if word in text:
            return color
    return None


def _detect_entities(text: str) -> list[str]:
    """Return list of detected entity types, no duplicates, order preserved."""
    found: list[str] = []
    seen: set[str] = set()
    for pattern, entity_type in _ENTITY_PATTERNS:
        if entity_type not in seen and re.search(pattern, text):
            found.append(entity_type)
            seen.add(entity_type)
    return found


def _detect_control_axis(text: str) -> str | None:
    for pattern, axis in _CONTROL_AXIS_PATTERNS:
        if re.search(pattern, text):
            return axis
    return None


def _extract_blocks_text(text: str, original_text: str) -> str:
    """Extract the brand/acronym to show in blocks_letters.

    Priority:
      1. Explicit \bwso2\b anywhere in text → 'WSO2'
      2. Word immediately after 'letras' in lowercase text
      3. Any ALLCAPS token in the original text
    """
    if re.search(r"\bwso2\b", text):
        return "WSO2"
    near = re.search(r"letras\s+(\w+)", text)
    if near:
        candidate = near.group(1).upper()
        if re.fullmatch(r"[A-Z0-9]{2,6}", candidate):
            return candidate
    caps = re.search(r"\b([A-Z][A-Z0-9]{1,5})\b", original_text)
    return caps.group(1) if caps else "TEXT"


def _make_entity(entity_type: str, text: str, original_text: str = "") -> EntitySpec:
    layer = _LAYER_OF.get(entity_type, "entities")

    if entity_type == "paddle":
        return EntitySpec(
            id="paddle", type="paddle", layer=layer,
            position=Position(x="center", y=190),
            size=Size(w=10, h=2),
            visual_pen=1,          # white — max contrast on black background
            render_hint="solid_box",
        )
    if entity_type == "player":
        return EntitySpec(
            id="player", type="player", layer=layer,
            position=Position(x="center", y=170),
            size=Size(w=4, h=4),
            visual_pen=1,
            render_hint="solid_box",
        )
    if entity_type == "ball":
        # Detect "small ball" / "1x1" / "square" / "single pixel" hints
        small = bool(re.search(
            r"cuadrado\s*peque|1\s*x\s*1|un\s*pixel|pixel\s*unico|pelota\s*peque|bola\s*peque",
            text
        ))
        # Detect "no floor bounce" = "pierde vida" / "no rebotar en suelo"
        no_floor = bool(re.search(
            r"no\s*rebotar.*suelo|pierde.*vida|suelo.*vida|sin\s*rebotar.*suelo|"
            r"vida.*suelo|si.*suelo.*vida|cae.*vida|ball.*floor.*life",
            text
        ))
        w, h = (1, 2) if small else (2, 2)   # 1×2 = 2×2 px square in mode0; 2×2 = 4×2 px
        return EntitySpec(
            id="ball", type="ball", layer=layer,
            position=Position(x=36, y=80),
            size=Size(w=w, h=h),
            visual_pen=3,
            render_hint="solid_box",
            properties={
                "velocity_x": 1, "velocity_y": 1,
                "bounce_floor": not no_floor,   # False → losing the ball costs a life
            },
        )
    if entity_type == "blocks_letters":
        text_value = _extract_blocks_text(text, original_text)
        char_count = len(text_value)
        # width in bytes = chars × 4 (mode-0 font: 4 bytes/char)
        sprite_w = char_count * 4
        return EntitySpec(
            id="blocks_letters", type="blocks_group", layer=layer,
            position=Position(x=max(0, (_SCREEN_W_BYTES - sprite_w) // 2), y=40),
            size=Size(w=sprite_w, h=8),
            properties={"text": text_value},
        )
    if entity_type == "score":
        right = "superior derecha" in text or "esquina derecha" in text
        return EntitySpec(
            id="score", type="text", layer=layer,
            position=Position(x="right" if right else "left", y=0),
            properties={"initial_value": "00000", "label": "Score:"},
        )
    if entity_type == "background_fill":
        color = _detect_background_color(text)
        return EntitySpec(
            id="background_fill", type="background", layer=layer,
            color=color or "black",
        )
    if entity_type in ("bricks", "enemy"):
        return EntitySpec(
            id=entity_type, type=entity_type, layer=layer,
            position=Position(x=10, y=20),
            size=Size(w=4, h=4),
        )
    return EntitySpec(id=entity_type, type=entity_type, layer=layer)


_SCREEN_W_BYTES = 80


def _build_layers(entity_types: list[str]) -> list[LayerSpec]:
    needed: set[str] = {_LAYER_OF.get(et, "entities") for et in entity_types}
    layers = []
    for i, name in enumerate(_STANDARD_LAYER_ORDER):
        if name in needed:
            ids = [et for et in entity_types if _LAYER_OF.get(et) == name]
            layers.append(LayerSpec(
                name=name, order=i, entities=ids,
                clear_on_frame=(name != "background"),
            ))
    return layers


def _build_controls(entity_types: list[str], text: str) -> list[ControlSpec]:
    controls: list[ControlSpec] = []
    for controlled in ("paddle", "player"):
        if controlled not in entity_types:
            continue
        axis = _detect_control_axis(text) or "horizontal"
        controls.append(ControlSpec(entity_id=controlled, action="move_left",
                                    key="Key_CursorLeft", axis="horizontal"))
        controls.append(ControlSpec(entity_id=controlled, action="move_right",
                                    key="Key_CursorRight", axis="horizontal"))
        if axis == "vertical":
            controls.append(ControlSpec(entity_id=controlled, action="move_up",
                                        key="Key_CursorUp", axis="vertical"))
            controls.append(ControlSpec(entity_id=controlled, action="move_down",
                                        key="Key_CursorDown", axis="vertical"))
    return controls


def _build_hypotheses(entity_types: list[str], color: str | None) -> list[str]:
    h = [
        "Modo de vídeo 0 (160×200, 16 colores) asumido por defecto.",
        "Estrategia de render: erase/draw por entidad — sin clear total por frame.",
    ]
    if "ball" in entity_types:
        h.append("Pelota: velocidad 1 byte cada 4 frames (~12 px/s visible).")
    if "blocks_letters" in entity_types:
        h.append("Letras formadas con font bitmap 4 bytes/char × 8 rows en modo 0.")
    if color:
        h.append(f"Color de fondo '{color}' → pen 0 de la paleta CPCtelera.")
    if "score" in entity_types:
        h.append("Marcador inicial: 00000. Posición derecha calculada en bytes de modo 0.")
    return h


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def _detect_lives(text: str) -> int:
    """Extract number of lives from text. Returns 0 if not mentioned."""
    m = re.search(r"(\d+)\s*vida|vida.*?(\d+)|(\d+)\s*live|live.*?(\d+)", text)
    if m:
        val = next(g for g in m.groups() if g is not None)
        return int(val)
    if re.search(r"\bvidas?\b|\blives?\b", text):
        return 3   # default if "vidas" mentioned without a number
    return 0


def plan_scene(prompt: PromptInput) -> SceneSpec:
    text = prompt.text.lower()
    entity_types = _detect_entities(text)
    bg_color = _detect_background_color(text)
    lives = _detect_lives(text)
    scoring = bool(re.search(r"puntos|score|marcador|scoring", text))

    if not entity_types:
        entity_types = ["background_fill"]

    entities = [_make_entity(et, text, prompt.text) for et in entity_types]
    layers = _build_layers(entity_types)
    controls = _build_controls(entity_types, text)
    hypotheses = _build_hypotheses(entity_types, bg_color)
    if lives:
        hypotheses.append(f"Vidas: {lives}. Si la pelota cae sin tocar la pala se pierde una vida.")
    if scoring:
        hypotheses.append("Score incrementa cuando la pelota toca el área de bloques.")

    return SceneSpec(
        id="scene_001",
        title="Generated scene",
        description=prompt.text[:120],
        video_mode=0,
        background_color=bg_color,
        layers=layers,
        entities=entities,
        controls=controls,
        hypotheses=hypotheses,
        lives=lives,
        scoring=scoring,
    )


def build_render_plan(scene: SceneSpec) -> RenderPlan:
    steps: list[RenderStep] = []
    entity_by_id = {e.id: e for e in scene.entities}

    # Render in layer order
    for layer in sorted(scene.layers, key=lambda l: l.order):
        if layer.name == "background":
            bg = entity_by_id.get("background_fill")
            steps.append(RenderStep(
                layer=layer.name, entity_id="background_fill",
                operation="fill_rect",
                params={"color": bg.color if bg else "black",
                        "x": 0, "y": 0, "w": 80, "h": 200},
            ))
        else:
            steps.append(RenderStep(
                layer=layer.name, entity_id=None,
                operation="clear", params={"color": 0},
            ))

        for eid in layer.entities:
            entity = entity_by_id.get(eid)
            if entity is None or entity.type == "background":
                continue
            if entity.type in ("paddle", "ball", "player", "blocks_group",
                               "bricks", "enemy"):
                steps.append(RenderStep(
                    layer=layer.name, entity_id=eid,
                    operation="draw_sprite", params={"entity_id": eid},
                ))
            elif entity.type == "text":
                steps.append(RenderStep(
                    layer=layer.name, entity_id=eid,
                    operation="draw_string",
                    params={
                        "cpctelera_api": "cpct_drawStringM0",
                        "screen_ptr_args": {
                            "screen_start": "CPCT_VMEM_START",
                            "x_bytes": entity.position.x if entity.position else 0,
                            "y_pixels": entity.position.y if entity.position else 0,
                        },
                        "string": entity.properties.get("initial_value", "0"),
                        "fg_pen": 1,
                        "bg_pen": 0,
                    },
                ))

    return RenderPlan(
        scene_id=scene.id,
        strategy="full_redraw_per_frame",
        steps=steps,
        notes=[
            "HUD rendered last — score never overwritten by entities.",
            "Erase/draw per-entity: no full-screen clear per frame.",
        ],
    )
