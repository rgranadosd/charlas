import json
import os
import re
import sys
import time as _time
from pathlib import PurePosixPath

from app.agents.context_builder import build_agent_extra_context
from app.services.c_codegen_service import (
    detect_c_generation_issues,
    render_c_array_decl,
    render_c_const_array,
    render_c_function_decl,
    render_c_function_def,
    render_c_include,
)
from app.services.contract_validation_service import normalize_asset_token
from app.services.llm_service import json_call

MAIN_C_PATH = "src/main.c"
GAME_H_PATH = "src/game.h"
GAME_C_PATH = "src/game.c"
HUD_H_PATH = "src/systems/hud.h"
HUD_C_PATH = "src/systems/hud.c"
PLAYER_H_PATH = "src/entities/player.h"
ENEMY_H_PATH = "src/entities/enemy.h"
ENEMY_C_PATH = "src/entities/enemy.c"
PROJECTILE_H_PATH = "src/entities/projectile.h"
PROJECTILE_C_PATH = "src/entities/projectile.c"
LEVEL1_H_PATH = "src/data/level1.h"
LEVEL1_C_PATH = "src/data/level1.c"
TILESET_BASE_H_PATH = "src/data/tileset/base.h"
TILESET_BASE_C_PATH = "src/data/tileset/base.c"
PLAYERKNIGHT_H_PATH = "src/data/sprites/playerknight.h"
PLAYERKNIGHT_C_PATH = "src/data/sprites/playerknight.c"
HEALTHBAR_H_PATH = "src/data/hud/healthbar.h"
HEALTHBAR_C_PATH = "src/data/hud/healthbar.c"
INPUT_H_PATH = "src/systems/input.h"
INPUT_C_PATH = "src/systems/input.c"
COLLISION_H_PATH = "src/systems/collision.h"
COLLISION_C_PATH = "src/systems/collision.c"
TILEMAP_H_PATH = "src/systems/tilemap.h"
TILEMAP_C_PATH = "src/systems/tilemap.c"
PLAYER_C_PATH = "src/entities/player.c"

PLAYABLE_RUNTIME_PROFILES = {"playable_slice", "vertical_slice"}

MANDATORY_RUNTIME_MODULES = {
    PLAYER_C_PATH,
    INPUT_C_PATH,
    COLLISION_C_PATH,
    TILEMAP_C_PATH,
}


# ---------------------------------------------------------------------------
# Video mode + palette resolution.
# Values come from the upstream agents (cpctelera_tech_agent.video_mode and
# art_agent.palette_strategy / palette_hw). Stubs MUST use these helpers so
# the generated code is internally consistent (mode N <-> palette size N
# <-> byte fill macros for mode N).
# ---------------------------------------------------------------------------

PALETTE_SIZE_BY_MODE = {0: 16, 1: 4, 2: 2}

# Firmware palette index (0..26) -> hardware ink byte accepted by Gate Array.
# Source used across the project: cpctelera/cpct_firmware2hw_colour_table.s
FIRMWARE_TO_HW_INK = [
    0x54, 0x44, 0x55, 0x5C, 0x58, 0x5D, 0x4C, 0x45, 0x4D,
    0x56, 0x46, 0x57, 0x5E, 0x40, 0x5F, 0x4E, 0x47, 0x4F,
    0x52, 0x42, 0x53, 0x5A, 0x59, 0x5B, 0x4A, 0x43, 0x4B,
]

# CPCtelera hardware palette values (Gate Array inks).
# These are bytes accepted by cpct_setPalette, not firmware indexes 0..26.
DEFAULT_PALETTE_HW_BY_MODE: dict[int, list[int]] = {
    # pen 0 = Black (bg), pen 6 = Bright White (player) — contrast guaranteed on black bg.
    # Original was pen0=0x17 (BrightWhite bg) + pen6=0x00 (White player) → both white → player invisible.
    0: [0x48, 0x54, 0x4E, 0x4C, 0x4B, 0x4A, 0x57, 0x46, 0x55, 0x52, 0x5E, 0x56, 0x47, 0x5A, 0x5C, 0x5F],
    # Reuse a known-good Mode 1 palette from working CPCtelera sample code.
    1: [0x54, 0x40, 0x4B, 0x44],
    2: [0x54, 0x4B],
}

# Semantic pen roles -> in-palette pen index per mode.
# Mode 1 only has 4 pens, so several roles collapse onto the same pen.
_PEN_TABLE: dict[int, dict[str, int]] = {
    0: {
        "bg": 0, "ground": 1, "platform": 2, "decor": 3, "goal": 5,
        "player": 6, "enemy": 4, "pickup": 7,
        "victory_bg": 8, "victory_fg": 5, "gameover_bg": 1, "gameover_fg": 6,
        "checkpoint": 9, "boss_bar_bg": 1, "boss_bar_fg": 5,
        "enemy_kind0": 4, "enemy_kind1": 14, "enemy_kind2": 10, "enemy_kind3": 12,
        "projectile_basic": 15, "projectile_upgraded": 11, "projectile_special": 5,
    },
    1: {
        "bg": 0, "ground": 1, "platform": 1, "decor": 1, "goal": 2,
        "player": 2, "enemy": 3, "pickup": 2,
        "victory_bg": 2, "victory_fg": 3, "gameover_bg": 3, "gameover_fg": 2,
        "checkpoint": 2, "boss_bar_bg": 3, "boss_bar_fg": 2,
        "enemy_kind0": 3, "enemy_kind1": 3, "enemy_kind2": 3, "enemy_kind3": 3,
        "projectile_basic": 3, "projectile_upgraded": 2, "projectile_special": 3,
    },
    2: {
        "bg": 0, "ground": 1, "platform": 1, "decor": 1, "goal": 1,
        "player": 1, "enemy": 1, "pickup": 1,
        "victory_bg": 1, "victory_fg": 1, "gameover_bg": 1, "gameover_fg": 1,
        "checkpoint": 1, "boss_bar_bg": 1, "boss_bar_fg": 1,
        "enemy_kind0": 1, "enemy_kind1": 1, "enemy_kind2": 1, "enemy_kind3": 1,
        "projectile_basic": 1, "projectile_upgraded": 1, "projectile_special": 1,
    },
}


def _resolve_video_mode(tech_output: dict | None) -> int:
    """Map tech_output.video_mode (string) to integer 0/1/2. Default 1.

    Accepts: "0", "Mode 0", "MODE_0", "mode-0", "mode0", "M0", etc.
    """
    if not tech_output:
        return 1
    raw = str(tech_output.get("video_mode", "")).strip().lower()
    if not raw:
        return 1
    # Normalise: strip everything except digits and the word 'mode'.
    digits = "".join(ch for ch in raw if ch.isdigit())
    if digits in {"0"}:
        requested_mode = 0
    elif digits in {"2"}:
        requested_mode = 2
    elif digits in {"1"}:
        requested_mode = 1
    else:
        requested_mode = None
    # Fallback: look for substrings.
    if requested_mode is None:
        if "mode 0" in raw or "mode_0" in raw or "mode-0" in raw or "mode0" in raw:
            requested_mode = 0
        elif "mode 2" in raw or "mode_2" in raw or "mode-2" in raw or "mode2" in raw:
            requested_mode = 2
        else:
            requested_mode = 1

    # Keep runtime defaults in Mode 1 for reliable visibility with current
    # generated renderer. Set CPC_ALLOW_MODE0=1 to permit Mode 0.
    if requested_mode == 0 and os.getenv("CPC_ALLOW_MODE0", "0").strip() != "1":
        return 1
    return requested_mode

def _resolve_palette_hw(art_output: dict | None, mode: int) -> list[int]:
    """Return palette as CPC hardware ink bytes, sized per mode.

    Accepts either firmware indexes (0..26) or hardware bytes (0x40..0x5F).
    """
    size = PALETTE_SIZE_BY_MODE.get(mode, 4)
    palette: list[int] = []
    if art_output:
        raw = art_output.get("palette_hw")
        if isinstance(raw, list):
            for value in raw:
                try:
                    pen = int(value)
                except (TypeError, ValueError):
                    continue
                if 0 <= pen <= 26:
                    palette.append(FIRMWARE_TO_HW_INK[pen])
                elif 0x40 <= pen <= 0x5F:
                    palette.append(pen)
    if not palette:
        palette = list(DEFAULT_PALETTE_HW_BY_MODE.get(mode, DEFAULT_PALETTE_HW_BY_MODE[1]))
    if len(palette) < size:
        palette = (palette + DEFAULT_PALETTE_HW_BY_MODE.get(mode, []))[:size]
    return palette[:size]


def _pen(role: str, mode: int) -> int:
    """Resolve a semantic pen role to the in-palette pen index for the mode."""
    table = _PEN_TABLE.get(mode, _PEN_TABLE[1])
    return table.get(role, 1)


def _fill_byte_expr(pen: int, mode: int) -> str:
    """Return a C expression evaluating to a screen byte fully filled with `pen`.

    Uses CPCtelera macros so the value is computed by the C preprocessor at
    compile time; this avoids hardcoded 0xXX literals that only happen to be
    correct for one specific mode."""
    if mode == 0:
        return f"cpct_px2byteM0({pen}, {pen})"
    if mode == 2:
        return f"cpct_px2byteM2({pen}, {pen}, {pen}, {pen}, {pen}, {pen}, {pen}, {pen})"
    return f"cpct_px2byteM1({pen}, {pen}, {pen}, {pen})"


def _fill_for(role: str, mode: int) -> str:
    return _fill_byte_expr(_pen(role, mode), mode)


def _render_u8_const_array(
    name: str,
    values: list[str],
    qualifiers: tuple[str, ...] = ("static", "const"),
) -> str:
    declaration = " ".join([*qualifiers, "u8", f"{name}[]"]) + " = {"
    lines = [declaration]
    for index in range(0, len(values), 8):
        chunk = values[index:index + 8]
        lines.append("    " + ", ".join(chunk) + ",")
    lines.append("};")
    return "\n".join(lines)


_MODE0_PIXEL_TABLE = [0x00, 0x40, 0x04, 0x44, 0x10, 0x50, 0x14, 0x54, 0x01, 0x41, 0x05, 0x45, 0x11, 0x51, 0x15, 0x55]


def _encode_mode0_byte(px0: int, px1: int) -> str:
    value = ((_MODE0_PIXEL_TABLE[px0 & 0x0F] << 1) & 0xFF) | _MODE0_PIXEL_TABLE[px1 & 0x0F]
    return f"0x{value:02X}"


def _encode_mode0_rows(rows: list[list[int]]) -> list[str]:
    encoded: list[str] = []
    for row in rows:
        if len(row) % 2 != 0:
            row = [*row, row[-1] if row else 0]
        for index in range(0, len(row), 2):
            encoded.append(_encode_mode0_byte(row[index], row[index + 1]))
    return encoded


def _build_box_sprite_values(width: int, height: int, fill: int, accent: int, variant: int = 0) -> list[str]:
    width_px = width * 2
    rows: list[list[int]] = []
    for y in range(height):
        row: list[int] = []
        for x in range(width_px):
            is_border = y == 0 or y == height - 1 or x == 0 or x == width_px - 1
            is_center_line = x == ((variant % max(1, width_px - 2)) + 1) if width_px > 2 else False
            is_mid_band = height > 2 and y == (height // 2)
            row.append(accent if is_border or is_center_line or is_mid_band else fill)
        rows.append(row)
    return _encode_mode0_rows(rows)


def _digit_sprite_values(digit: int, bg: int, fg: int) -> list[str]:
    segment_map = {
        0: "abcfed",
        1: "bc",
        2: "abdeg",
        3: "abcdg",
        4: "fgbc",
        5: "afgcd",
        6: "afgcde",
        7: "abc",
        8: "abcdefg",
        9: "abcfgd",
    }
    active = set(segment_map.get(digit, ""))
    rows: list[list[int]] = []

    for y in range(8):
        row: list[int] = []
        for x in range(8):
            on = False
            if "a" in active and y == 0 and 1 <= x <= 6:
                on = True
            elif "g" in active and y == 3 and 1 <= x <= 6:
                on = True
            elif "d" in active and y == 7 and 1 <= x <= 6:
                on = True
            elif "f" in active and x == 0 and 1 <= y <= 2:
                on = True
            elif "b" in active and x == 7 and 1 <= y <= 2:
                on = True
            elif "e" in active and x == 0 and 4 <= y <= 6:
                on = True
            elif "c" in active and x == 7 and 4 <= y <= 6:
                on = True
            row.append(fg if on else bg)
        rows.append(row)

    return _encode_mode0_rows(rows)


def _build_visible_asset_values(symbol: str) -> list[str]:
    """
    RENDERING RULE (CPCtelera Mode 0):
    cpct_drawSprite has NO transparency.  Pen 0 = background colour.
    Any sprite pixel encoded as pen 0 will be painted in the background
    colour → the interior becomes invisible against the background.
    Always use pen 6 (black) or another opaque pen as the fill for
    character / enemy sprites.  Use pen 0 ONLY for HUD digits where
    the game area is already cleared to pen 0 (acts as pseudo-transparency).
    """
    token = symbol.lower()
    bg = 0        # pen 0: background — valid only for HUD digit gaps
    opaque = 6    # pen 6: bright white — opaque fill for character sprites (contrasts with black bg)
    if "hud" in token or "health" in token:
        return _digit_sprite_values(8, bg, 15)
    if "player" in token or "knight" in token:
        return _build_box_sprite_values(8, 24, opaque, 15, variant=1)
    if "tile" in token:
        return _build_box_sprite_values(4, 8, 1, 14, variant=2)
    return _build_box_sprite_values(4, 8, opaque, 10, variant=3)


def _build_game_h_stub() -> str:
    return "\n".join(
        [
            "#ifndef GAME_H",
            "#define GAME_H",
            "",
            "void game_init(void);",
            "void game_update(void);",
            "void game_render(void);",
            "",
            "#endif",
            "",
        ]
    )


def _build_game_c_stub(mode: int = 1) -> str:
    safe_mode = 1 if mode != 0 else 0
    bg_fill = _fill_for("bg", safe_mode)
    ground_fill = _fill_for("ground", safe_mode)
    player_fill = _fill_for("player", safe_mode)
    pickup_fill = _fill_for("pickup", safe_mode)

    if safe_mode == 0:
        palette_decl = "static const u8 game_palette[16] = {0x54, 0x4B, 0x58, 0x5D, 0x4A, 0x43, 0x53, 0x4F, 0x46, 0x45, 0x4C, 0x5C, 0x40, 0x57, 0x5E, 0x47};"
        palette_apply = "cpct_setPalette((u8*)game_palette, 16);"
    else:
        palette_decl = "static const u8 game_palette[4] = {0x54, 0x4B, 0x58, 0x5D};"
        palette_apply = "cpct_setPalette((u8*)game_palette, 4);"

    return "\n".join(
        [
            render_c_include("game.h"),
            render_c_include("<cpctelera.h>"),
            "",
            palette_decl,
            "",
            "void game_init(void) {",
            "    cpct_disableFirmware();",
            f"    cpct_setVideoMode({safe_mode});",
            "    cpct_setBorder(game_palette[0]);",
            f"    {palette_apply}",
            f"    cpct_clearScreen({bg_fill});",
            "}",
            "",
            "void game_update(void) {",
            "}",
            "",
            "void game_render(void) {",
            "    u8* pvmem;",
            f"    cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 0, 184), {ground_fill}, 40, 16);",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 160);",
            f"    cpct_drawSolidBox(pvmem, {player_fill}, 4, 16);",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 26, 152);",
            f"    cpct_drawSolidBox(pvmem, {pickup_fill}, 3, 10);",
            "}",
            "",
        ]
    )


def _build_player_render_function(mode: int) -> str:
    bg_fill = _fill_for("bg", mode)
    player_fill = _fill_for("player", mode)
    flicker_fill = _fill_for("pickup", mode)
    return "\n".join(
        [
            "void player_render(void) {",
            "    u8 color;",
            "",
            "    // Erase previous",
            f"    cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, player.prev_x, player.prev_y), {bg_fill}, player.w, player.h);",
            "    // Draw player (solid box as placeholder)",
            f"    color = (player.invulnerable_timer & 2) ? {flicker_fill} : {player_fill};",
            "    cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, player.x, player.y), color, player.w, player.h);",
            "}",
        ]
    )


def _build_projectile_render_function(mode: int) -> str:
    bg_fill = _fill_for("bg", mode)
    proj_fill = _fill_for("projectile_basic", mode)
    return "\n".join(
        [
            "void projectile_render(void) {",
            "    for (u8 i = 0; i < MAX_PROJECTILES; ++i) {",
            "        Projectile* p = &projectiles[i];",
            "        if (!p->active) continue;",
            "        // Erase previous",
            f"        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, p->prev_x, p->prev_y), {bg_fill}, p->w, p->h);",
            "        // Draw projectile (solid box as placeholder)",
            f"        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, p->x, p->y), {proj_fill}, p->w, p->h);",
            "    }",
            "}",
        ]
    )


def _replace_function_block(source: str, func_name: str, replacement: str) -> str:
    pattern = rf"void\\s+{re.escape(func_name)}\\s*\\(\\s*void\\s*\\)\\s*\\{{.*?\\n\\}}"
    return re.sub(pattern, replacement, source, count=1, flags=re.DOTALL)


def _sanitize_entity_render_source_files(
    files: dict[str, str],
    allowed_files: set[str],
    tech_output: dict | None,
) -> tuple[dict[str, str], list[str]]:
    normalized = dict(files)
    sanitized: list[str] = []
    mode = _resolve_video_mode(tech_output)

    if _is_allowed(PLAYER_C_PATH, allowed_files):
        player_c = str(normalized.get(PLAYER_C_PATH, ""))
        if player_c and "void player_render(void)" in player_c:
            suspicious = bool(re.search(r"void\\s+player_render\\s*\\(\\s*void\\s*\\)\\s*\\{.*0x[0-9A-Fa-f]{1,2}", player_c, flags=re.DOTALL))
            if suspicious:
                replaced = _replace_function_block(player_c, "player_render", _build_player_render_function(mode))
                if replaced != player_c:
                    normalized[PLAYER_C_PATH] = replaced
                    sanitized.append(PLAYER_C_PATH)

    if _is_allowed(PROJECTILE_C_PATH, allowed_files):
        projectile_c = str(normalized.get(PROJECTILE_C_PATH, ""))
        if projectile_c and "void projectile_render(void)" in projectile_c:
            suspicious = bool(re.search(r"void\\s+projectile_render\\s*\\(\\s*void\\s*\\)\\s*\\{.*0x[0-9A-Fa-f]{1,2}", projectile_c, flags=re.DOTALL))
            if suspicious:
                replaced = _replace_function_block(projectile_c, "projectile_render", _build_projectile_render_function(mode))
                if replaced != projectile_c:
                    normalized[PROJECTILE_C_PATH] = replaced
                    sanitized.append(PROJECTILE_C_PATH)

        # Some generated legacy projectiles use C89-incompatible declarations
        # inside projectile_render_all/projectile_erase_all loops (e.g. "u8* s"
        # after a "continue"). Normalize those blocks to keep SDCC happy.
        projectile_c = str(normalized.get(PROJECTILE_C_PATH, ""))
        if projectile_c and "void projectile_render_all(void)" in projectile_c:
            replaced = projectile_c
            replaced = re.sub(
                r"if \(!p->active\) continue;\s*\n\s*u8\* s = cpct_getScreenPtr\(CPCT_VMEM_START, p->x, p->y\);",
                "u8* s;\n        if (!p->active) continue;\n        s = cpct_getScreenPtr(CPCT_VMEM_START, p->x, p->y);",
                replaced,
                count=1,
            )
            replaced = re.sub(
                r"if \(!p->active\) continue;\s*\n\s*u8\* s = cpct_getScreenPtr\(CPCT_VMEM_START, p->prev_x, p->prev_y\);",
                "u8* s;\n        if (!p->active) continue;\n        s = cpct_getScreenPtr(CPCT_VMEM_START, p->prev_x, p->prev_y);",
                replaced,
                count=1,
            )
            if replaced != projectile_c:
                normalized[PROJECTILE_C_PATH] = replaced
                sanitized.append(PROJECTILE_C_PATH)

    return normalized, sorted(set(sanitized))


def _build_player_c_compat_stub(mode: int = 1) -> str:
    bg_fill = _fill_for("bg", mode)
    player_fill = _fill_for("player", mode)
    return "\n".join(
        [
            render_c_include("entities/player.h"),
            render_c_include("systems/input.h"),
            render_c_include("systems/tilemap.h"),
            render_c_include("<cpctelera.h>"),
            "",
            "Player player;",
            "",
            "#define PLAYER_W 8",
            "#define PLAYER_H 24",
            "#define PLAYER_SPEED 2",
            "#define PLAYER_JUMP_VY -6",
            "#define PLAYER_GRAVITY 1",
            "#define PLAYER_MAX_FALL 4",
            "",
            "void player_init(void) {",
            "    player.x = 16;",
            "    player.y = (u8)(tilemap_ground_y() - PLAYER_H);",
            "    player.w = PLAYER_W;",
            "    player.h = PLAYER_H;",
            "    player.vx = 0;",
            "    player.vy = 0;",
            "    player.state = PLAYER_STATE_IDLE;",
            "    player.lives = 3;",
            "    player.score = 0;",
            "    player.invulnerable = 0;",
            "    player.prev_x = player.x;",
            "    player.prev_y = player.y;",
            "    player.active = 1;",
            "    player.jump_timer = 0;",
            "    player.can_shoot = 1;",
            "}",
            "",
            "void player_update(void) {",
            "    i16 nextx;",
            "    i16 nexty;",
            "",
            "    if (!player.active || player.state == PLAYER_STATE_DEAD) return;",
            "",
            "    player.prev_x = player.x;",
            "    player.prev_y = player.y;",
            "",
            "    player.vx = 0;",
            "    if (input_left && !input_right) player.vx = -PLAYER_SPEED;",
            "    else if (input_right && !input_left) player.vx = PLAYER_SPEED;",
            "",
            "    nextx = (i16)player.x + (i16)player.vx;",
            "    if (nextx < 0) nextx = 0;",
            "    if (nextx > (80 - (i16)player.w)) nextx = (80 - (i16)player.w);",
            "    player.x = (u8)nextx;",
            "",
            "    if (input_jump && player.vy == 0 && (i16)player.y + (i16)player.h >= (i16)tilemap_ground_y()) {",
            "        player.vy = PLAYER_JUMP_VY;",
            "        player.state = PLAYER_STATE_JUMP;",
            "    }",
            "",
            "    player.vy = (i8)(player.vy + PLAYER_GRAVITY);",
            "    if (player.vy > PLAYER_MAX_FALL) player.vy = PLAYER_MAX_FALL;",
            "",
            "    nexty = (i16)player.y + (i16)player.vy;",
            "    if (nexty + (i16)player.h >= (i16)tilemap_ground_y()) {",
            "        nexty = (i16)tilemap_ground_y() - (i16)player.h;",
            "        player.vy = 0;",
            "        if (input_down) player.state = PLAYER_STATE_CROUCH;",
            "        else if (player.vx) player.state = PLAYER_STATE_RUN;",
            "        else player.state = PLAYER_STATE_IDLE;",
            "    }",
            "    if (nexty < 0) nexty = 0;",
            "    player.y = (u8)nexty;",
            "",
            "    if (player.invulnerable > 0) player.invulnerable--;",
            "}",
            "",
            "void player_render(void) {",
            "    cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, player.x, player.y), " + player_fill + ", player.w, player.h);",
            "}",
            "",
            "void player_erase(void) {",
            "    cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, player.prev_x, player.prev_y), " + bg_fill + ", player.w, player.h);",
            "}",
            "",
            "void player_save_prev_pos(void) {",
            "    player.prev_x = player.x;",
            "    player.prev_y = player.y;",
            "}",
            "",
        ]
    )


def _sanitize_player_source_files(
    files: dict[str, str],
    allowed_files: set[str],
    tech_output: dict | None,
) -> tuple[dict[str, str], list[str]]:
    normalized = dict(files)
    sanitized: list[str] = []

    if not _is_allowed(PLAYER_C_PATH, allowed_files):
        return normalized, sanitized

    player_c = str(normalized.get(PLAYER_C_PATH, ""))
    if not player_c:
        return normalized, sanitized

    # Generated legacy player implementations frequently mix C99 declarations
    # with C89 SDCC and call tilemap/projectile APIs in incompatible ways.
    has_c89_risk = bool(re.search(r"return\s*;\s*\n\s*i8\s+[A-Za-z_][A-Za-z0-9_]*\s*=", player_c))
    has_inline_extern_projectile = bool(
        re.search(r"\n\s*extern\s+void\s+projectile_spawn\s*\(", player_c)
    )
    has_late_local_declarations = bool(
        re.search(r"\n\s*u8\s+ground_y\s*=", player_c)
        or re.search(r"\n\s*u8\s*\*\s*[A-Za-z_][A-Za-z0-9_]*\s*=\s*cpct_getScreenPtr\s*\(", player_c)
    )
    uses_missing_tilemap_api = "tilemap_is_solid(" in player_c
    uses_legacy_projectile_hook = "player_shoot_projectile(" in player_c

    player_h = str(normalized.get(PLAYER_H_PATH, ""))
    uses_undefined_state_enum = bool(
        re.search(r"\bPLAYER_STATE_", player_c)
        and not re.search(r"#define\s+PLAYER_STATE_IDLE", player_h)
    )
    uses_undefined_player_fields = bool(
        re.search(r"player\.(invulnerable|jump_timer|can_shoot)\b", player_c)
        and not re.search(r"\binvulnerable\b", player_h)
    )

    needs_stub = (
        has_c89_risk
        or has_inline_extern_projectile
        or has_late_local_declarations
        or uses_missing_tilemap_api
        or uses_legacy_projectile_hook
        or uses_undefined_state_enum
        or uses_undefined_player_fields
    )

    if needs_stub:
        mode = _resolve_video_mode(tech_output)
        replacement = _build_player_c_compat_stub(mode)
        if replacement != player_c:
            normalized[PLAYER_C_PATH] = replacement
            sanitized.append(PLAYER_C_PATH)
        # Also replace player.h with the matching stub so fields/enums are consistent
        if _is_allowed(PLAYER_H_PATH, allowed_files):
            h_stub = _build_player_h_stub()
            if normalized.get(PLAYER_H_PATH) != h_stub:
                normalized[PLAYER_H_PATH] = h_stub
                sanitized.append(PLAYER_H_PATH)

    return normalized, sorted(set(sanitized))


def _sanitize_projectile_source_files(
    files: dict[str, str],
    allowed_files: set[str],
) -> tuple[dict[str, str], list[str]]:
    """Patch projectile.h struct when projectile.c uses fields not declared in it."""
    normalized = dict(files)
    sanitized: list[str] = []

    if not _is_allowed(PROJECTILE_H_PATH, allowed_files):
        return normalized, sanitized

    projectile_h = str(normalized.get(PROJECTILE_H_PATH, ""))
    projectile_c = str(normalized.get(PROJECTILE_C_PATH, ""))
    if not projectile_h or not projectile_c:
        return normalized, sanitized

    # prev_active used in .c but missing from struct in .h
    if (
        re.search(r"\bprev_active\b", projectile_c)
        and not re.search(r"\bprev_active\b", projectile_h)
    ):
        patched = re.sub(
            r"(\bprev_h\s*,\s*active)\s*;",
            r"\1, prev_active;",
            projectile_h,
        )
        if patched == projectile_h:
            # Fallback: add before closing brace of Projectile typedef
            patched = re.sub(
                r"(\bactive\b[^;]*;)(\s*\}[^;]*Projectile\s*;)",
                r"\1\n    u8 prev_active;\2",
                projectile_h,
            )
        if patched != projectile_h:
            normalized[PROJECTILE_H_PATH] = patched
            sanitized.append(PROJECTILE_H_PATH)

    return normalized, sorted(set(sanitized))


def _sanitize_main_source_files(
    files: dict[str, str],
    allowed_files: set[str],
) -> tuple[dict[str, str], list[str]]:
    normalized = dict(files)
    sanitized: list[str] = []

    if not _is_allowed(MAIN_C_PATH, allowed_files):
        return normalized, sanitized

    main_c = str(normalized.get(MAIN_C_PATH, ""))
    if not main_c:
        return normalized, sanitized

    if "jp cpc_run_address" in main_c and "cpc_run_address::" not in main_c:
        replacement = main_c.replace("        .globl cpc_run_address\n", "")
        replacement = replacement.replace("        jp cpc_run_address", "        jp _main")
        if replacement != main_c:
            normalized[MAIN_C_PATH] = replacement
            sanitized.append(MAIN_C_PATH)

    return normalized, sorted(set(sanitized))

    return "\n".join(
        [
            render_c_include("game.h"),
            render_c_include("<cpctelera.h>"),
            render_c_include("systems/tilemap.h"),
            render_c_include("systems/input.h"),
            render_c_include("systems/collision.h"),
            render_c_include("entities/player.h"),
            render_c_include("entities/enemy.h"),
            render_c_include("entities/projectile.h"),
            render_c_include("systems/hud.h"),
            render_c_include("data/level1.h"),
            "",
            "#define MAX_ENEMIES 6",
            "#define MAX_PROJECTILES 6",
            "#define TOTAL_WAVES 3",
            "",
            "static Player g_player;",
            "static Enemy g_enemies[MAX_ENEMIES];",
            "static Projectile g_projectiles[MAX_PROJECTILES];",
            "",
            "static u8 g_lives;",
            "static u16 g_score;",
            "static u8 g_timeleft;",
            "static u8 g_weapondisplay;",
            "static u8 g_currentwave;",
            "static u8 g_aliveenemies;",
            "static u8 g_wavecooldown;",
            "static u8 g_damagecooldown;",
            "static u8 g_shootcooldown;",
            "static u8 g_victory;",
            "static u8 g_gameover;",
            "static u16 g_framecounter;",
            "static u8 g_checkpointx;",
            "static u8 g_checkpointy;",
            "static u8 g_checkpointactive;",
            "static Enemy g_boss;",
            "static u8 g_bossactive;",
            "static u8 g_bossphase;",
            "static u8 g_weaponlevel;",
            "static u8 g_pickuptaken;",
            "",
            "static void reset_player_to_checkpoint(void) {",
            "    g_player.x = g_checkpointx;",
            "    g_player.y = g_checkpointy;",
            "    g_player.vx = 0;",
            "    g_player.vy = 0;",
            "}",
            "",
            "static u8 rect_overlap(i16 ax, i16 ay, u8 aw, u8 ah, i16 bx, i16 by, u8 bw, u8 bh) {",
            "    if (ax + aw <= bx) return 0;",
            "    if (bx + bw <= ax) return 0;",
            "    if (ay + ah <= by) return 0;",
            "    if (by + bh <= ay) return 0;",
            "    return 1;",
            "}",
            "",
            "static void spawn_wave(u8 wave) {",
            "    u8 i;",
            "    u8 count;",
            "",
            "    for (i = 0; i < MAX_ENEMIES; ++i) {",
            "        enemyinit(&g_enemies[i]);",
            "    }",
            "",
            "    if (wave == 0) count = 2;",
            "    else if (wave == 1) count = 3;",
            "    else count = 4;",
            "",
            "    if (count > MAX_ENEMIES) count = MAX_ENEMIES;",
            "",
            "    for (i = 0; i < count; ++i) {",
            "        u8 type;",
            "        u8 spawn_y;",
            "        if (wave == 0) type = 0;",
            "        else if (wave == 1) type = (u8)((i == 0) ? 1 : 0);",
            "        else type = (u8)((i == 0 || i == 3) ? 2 : 1);",
            "",
            "        spawn_y = (type == 2) ? 84 : 112;",
            "        enemyspawn(&g_enemies[i], (u8)(46 + (i * 8)), spawn_y, type, (u8)((i & 1) ? 1 : 0));",
            "    }",
            "",
            "    g_aliveenemies = count;",
            "}",
            "",
            "static void spawn_boss(void) {",
            "    enemyinit(&g_boss);",
            "    enemyspawn(&g_boss, 68, 112, 1, 0);",
            "    g_boss.w = 10;",
            "    g_boss.h = 18;",
            "    g_boss.health = 10;",
            "    g_boss.reward = 1500;",
            "    g_boss.kind = 3;",
            "    g_boss.vx = -1;",
            "    g_bossactive = 1;",
            "    g_bossphase = 0;",
            "}",
            "",
            "static void try_fire_projectile(void) {",
            "    u8 i;",
            "    i8 dir;",
            "",
            "    if (!input_is_shoot_just_pressed()) return;",
            "    if (g_shootcooldown) return;",
            "",
            "    dir = g_player.facing_left ? -3 : 3;",
            "",
            "    for (i = 0; i < MAX_PROJECTILES; ++i) {",
            "        if (!g_projectiles[i].active) {",
            "            /* weapon_upgrade_active: pickup permanente que mejora el disparo */",
            "            projectilefire(&g_projectiles[i], (u8)(g_player.x + 2), (u8)(g_player.y + 6), dir, g_weaponlevel > 0 ? 1 : 0);",
            "            g_shootcooldown = g_weaponlevel > 0 ? 4 : 8;",
            "            break;",
            "        }",
            "    }",
            "}",
            "",
            "static void register_player_hit(void) {",
            "    if (g_lives) {",
            "        g_lives--;",
            "    }",
            "    if (g_lives == 0) {",
            "        g_gameover = 1;",
            "        return;",
            "    }",
            "",
            "    reset_player_to_checkpoint();",
            "    g_damagecooldown = 40;",
            "}",
            "",
            "void game_init(void) {",
            "    u8 i;",
            "",
            "    cpct_disableFirmware();",
            f"    cpct_setVideoMode({mode});",
            "    cpct_setPalette((u8*)gpalette, GPALETTE_SIZE);",
            "    cpct_setBorder(gpalette[0]);",
            "    cpct_clearScreen(0x00);",
            "    tilemap_init();",
            "    collision_init();",
            "    playerinit(&g_player);",
            "    hudinit();",
            "",
            "    for (i = 0; i < MAX_PROJECTILES; ++i) {",
            "        projectileinit(&g_projectiles[i]);",
            "    }",
            "",
            "    g_lives = 3;",
            "    g_score = 0;",
            "    g_timeleft = 99;",
            "    g_weapondisplay = 1;",
            "    g_currentwave = 0;",
            "    g_wavecooldown = 1;",
            "    g_damagecooldown = 0;",
            "    g_shootcooldown = 0;",
            "    g_victory = 0;",
            "    g_gameover = 0;",
            "    g_framecounter = 0;",
            "    g_checkpointx = 20;",
            "    g_checkpointy = 120;",
            "    g_checkpointactive = 0;",
            "    g_bossactive = 0;",
            "    g_weaponlevel = 0;",
            "    g_pickuptaken = 0;",
            "    enemyinit(&g_boss);",
            "}",
            "",
            "void game_update(void) {",
            "    u8 i;",
            "    u8 j;",
            "",
            "    input_update();",
            "",
            "    if (g_gameover || g_victory) {",
            "        hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);",
            "        return;",
            "    }",
            "",
            "    playerupdate(&g_player);",
            "    try_fire_projectile();",
            "",
            "    if (g_shootcooldown) g_shootcooldown--;",
            "    if (g_damagecooldown) g_damagecooldown--;",
            "",
            "    for (i = 0; i < MAX_PROJECTILES; ++i) {",
            "        projectileupdate(&g_projectiles[i]);",
            "    }",
            "",
            "    for (i = 0; i < MAX_ENEMIES; ++i) {",
            "        enemyupdate(&g_enemies[i]);",
            "    }",
            "",
            "    if (g_bossactive) {",
            "        if (g_boss.health > 4) g_bossphase = 0;",
            "        else g_bossphase = 1;",
            "",
            "        g_boss.vx = (i8)(g_player.x + 2 < g_boss.x ? -(g_bossphase ? 2 : 1) : (g_bossphase ? 2 : 1));",
            "        enemyupdate(&g_boss);",
            "    }",
            "",
            "    for (i = 0; i < MAX_PROJECTILES; ++i) {",
            "        if (!g_projectiles[i].active) continue;",
            "        for (j = 0; j < MAX_ENEMIES; ++j) {",
            "            if (!g_enemies[j].active) continue;",
            "            if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,",
            "                             (i16)g_enemies[j].x, (i16)g_enemies[j].y, g_enemies[j].w, g_enemies[j].h)) continue;",
            "            if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {",
            "                g_score = (u16)(g_score + g_enemies[j].reward);",
            "                if (g_aliveenemies) g_aliveenemies--;",
            "            }",
            "            g_projectiles[i].active = 0;",
            "            break;",
            "        }",
            "",
            "        if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,",
            "                (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {",
            "            g_projectiles[i].active = 0;",
            "            if (enemydamage(&g_boss, g_projectiles[i].damage)) {",
            "                g_bossactive = 0;",
            "                g_score = (u16)(g_score + g_boss.reward);",
            "                g_victory = 1;",
            "            }",
            "        }",
            "    }",
            "",
            "    if (!g_damagecooldown) {",
            "        for (i = 0; i < MAX_ENEMIES; ++i) {",
            "            if (!g_enemies[i].active) continue;",
            "            if (rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,",
            "                             (i16)g_enemies[i].x, (i16)g_enemies[i].y, g_enemies[i].w, g_enemies[i].h)) {",
            "                register_player_hit();",
            "                break;",
            "            }",
            "        }",
            "",
            "        if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,",
            "                (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {",
            "            register_player_hit();",
            "        }",
            "",
            "        if (!g_damagecooldown && collision_is_on_trap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h)) {",
            "            register_player_hit();",
            "        }",
            "    }",
            "",
            "    if (!g_checkpointactive && g_player.x >= 44) {",
            "        g_checkpointactive = 1;",
            "        g_checkpointx = 52;",
            "        g_checkpointy = (u8)(tilemap_ground_y() - g_player.h);",
            "    }",
            "",
            "    if (!g_pickuptaken && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h, (i16)36, (i16)(tilemap_ground_y() - 8), 4, 4)) {",
            "        g_pickuptaken = 1;",
            "        g_weaponlevel = 1;",
            "        g_score = (u16)(g_score + 100);",
            "    }",
            "",
            "    g_weapondisplay = (u8)(g_weaponlevel + 1);",
            "",
            "    if (!g_bossactive && g_aliveenemies == 0 && !g_gameover) {",
            "        if (g_currentwave < TOTAL_WAVES) {",
            "            if (g_wavecooldown == 0) {",
            "                spawn_wave(g_currentwave);",
            "                g_currentwave++;",
            "                g_wavecooldown = 90;",
            "            } else {",
            "                g_wavecooldown--;",
            "            }",
            "        } else if (g_player.x >= (u8)(tilemap_goal_x() - 2)) {",
            "            spawn_boss();",
            "        }",
            "    }",
            "",
            "    g_framecounter++;",
            "    if ((g_framecounter % 50) == 0 && g_timeleft > 0) {",
            "        g_timeleft--;",
            "    }",
            "    if (g_timeleft == 0 && !g_victory) {",
            "        g_gameover = 1;",
            "    }",
            "",
            "    hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);",
            "}",
            "",
            "void game_render(void) {",
            "    u8 i;",
            "",
            f"    cpct_clearScreen({_fill_for('bg', mode)});",
            "    tilemap_render();",
            f"    cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 60, 18), {_fill_for('victory_fg', mode)}, 6, 10);",
            f"    cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 58, 20), {_fill_for('victory_bg', mode)}, 2, 6);",
            "",
            "    for (i = 0; i < MAX_PROJECTILES; ++i) {",
            "        if (g_projectiles[i].active) {",
            f"            cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, g_projectiles[i].x, g_projectiles[i].y), {_fill_for('projectile_upgraded', mode)}, g_projectiles[i].w, g_projectiles[i].h);",
            "        }",
            "    }",
            "",
            "    for (i = 0; i < MAX_ENEMIES; ++i) {",
            "        if (g_enemies[i].active) {",
            f"            cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, g_enemies[i].x, g_enemies[i].y), {_fill_for('enemy', mode)}, g_enemies[i].w, g_enemies[i].h);",
            "        }",
            "    }",
            "",
            "    if (g_bossactive) {",
            f"        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, g_boss.x, g_boss.y), {_fill_for('enemy', mode)}, g_boss.w, g_boss.h);",
            f"        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), {_fill_for('boss_bar_bg', mode)}, 32, 2);",
            f"        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), {_fill_for('boss_bar_fg', mode)}, (u8)(g_boss.health * 3), 2);",
            "    }",
            "",
            "    if (!g_pickuptaken) {",
            f"        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 36, (u8)(tilemap_ground_y() - 8)), {_fill_for('pickup', mode)}, 4, 4);",
            "    }",
            f"    cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, g_player.x, g_player.y), {_fill_for('player', mode)}, g_player.w, g_player.h);",
            "    hudrender();",
            "",
            "    if (g_victory) {",
            f"        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), {_fill_for('victory_bg', mode)}, 32, 12);",
            f"        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), {_fill_for('victory_fg', mode)}, 24, 8);",
            "    } else if (g_gameover) {",
            f"        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), {_fill_for('gameover_bg', mode)}, 32, 12);",
            f"        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), {_fill_for('gameover_fg', mode)}, 24, 8);",
            "    } else if (g_checkpointactive) {",
            f"        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, g_checkpointx, (u8)(g_checkpointy - 8)), {_fill_for('checkpoint', mode)}, 2, 8);",
            "    }",
            "}",
            "",
        ]
    )


def _build_main_c_stub() -> str:
    return "\n".join(
        [
            render_c_include("<cpctelera.h>"),
            render_c_include("game.h"),
            "",
            "void cpc_entry_wrapper(void) __naked {",
            "    __asm",
            "        .globl cpc_run_address",
            "        .globl s__INITIALIZER",
            "        .globl s__INITIALIZED",
            "        .globl l__INITIALIZER",
            "    cpc_run_address::",
            "        di",
            "        ld sp, #0xBFF0",
            "        ld bc, #l__INITIALIZER",
            "        ld a, b",
            "        or c",
            "        jr z, 00001$",
            "        ld de, #s__INITIALIZED",
            "        ld hl, #s__INITIALIZER",
            "        ldir",
            "00001$:",
            "        call _main",
            "        ret",
            "    __endasm;",
            "}",
            "",
            "void main(void) {",
            "    /* Force a known-good stack pointer below firmware RAM (--no-std-crt0). */",
            "    __asm",
            "        di",
            "        ld sp, #0xBFF0",
            "    __endasm;",
            "",
            "    game_init();",
            "    while (1) {",
            "        game_update();",
            "        game_render();",
            "        cpct_waitVSYNC();",
            "    }",
            "}",
            "",
        ]
    )


def _build_player_h_stub() -> str:
    return "\n".join(
        [
            "#ifndef ENTITIES_PLAYER_H",
            "#define ENTITIES_PLAYER_H",
            "",
            render_c_include("<cpctelera.h>"),
            "",
            "#define PLAYER_STATE_IDLE   0",
            "#define PLAYER_STATE_RUN    1",
            "#define PLAYER_STATE_JUMP   2",
            "#define PLAYER_STATE_CROUCH 3",
            "#define PLAYER_STATE_DEAD   4",
            "",
            "typedef struct {",
            "    u8 x;",
            "    u8 y;",
            "    i8 vx;",
            "    i8 vy;",
            "    u8 w;",
            "    u8 h;",
            "    u8 prev_x;",
            "    u8 prev_y;",
            "    u8 state;",
            "    u8 lives;",
            "    u16 score;",
            "    u8 invulnerable;",
            "    u8 jump_timer;",
            "    u8 can_shoot;",
            "    u8 active;",
            "} Player;",
            "",
            "extern Player player;",
            "",
            "void player_init(void);",
            "void player_update(void);",
            "void player_render(void);",
            "void player_erase(void);",
            "void player_store_prev(void);",
            "void player_kill(void);",
            "",
            "#endif",
            "",
        ]
    )


def _build_enemy_h_stub() -> str:
    return "\n".join(
        [
            "#ifndef ENTITIES_ENEMY_H",
            "#define ENTITIES_ENEMY_H",
            "",
            render_c_include("<cpctelera.h>"),
            "",
            "typedef struct {",
            "    u8 x;",
            "    u8 y;",
            "    i8 vx;",
            "    i8 vy;",
            "    u8 w;",
            "    u8 h;",
            "    u8 active;",
            "    u8 health;",
            "    u8 reward;",
            "    u8 kind;",
            "} Enemy;",
            "",
            "void enemyinit(Enemy* enemy);",
            "void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right);",
            "void enemyupdate(Enemy* enemy);",
            "void enemyrender(const Enemy* enemy);",
            "u8 enemydamage(Enemy* enemy, u8 damage);",
            "",
            "#endif",
            "",
        ]
    )


def _build_projectile_h_stub() -> str:
    return "\n".join(
        [
            "#ifndef ENTITIES_PROJECTILE_H",
            "#define ENTITIES_PROJECTILE_H",
            "",
            render_c_include("<cpctelera.h>"),
            "",
            "typedef struct {",
            "    u8 x;",
            "    u8 y;",
            "    i8 vx;",
            "    i8 vy;",
            "    u8 w;",
            "    u8 h;",
            "    u8 active;",
            "    u8 damage;",
            "    u8 lifetime;",
            "    u8 weapon;",
            "} Projectile;",
            "",
            "void projectileinit(Projectile* projectile);",
            "void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon);",
            "void projectileupdate(Projectile* projectile);",
            "void projectilerender(const Projectile* projectile);",
            "",
            "#endif",
            "",
        ]
    )


def _build_enemy_c_stub(mode: int = 1) -> str:
    enemy0 = _pen('enemy_kind0', mode)
    enemy1 = _pen('enemy_kind1', mode)
    enemy2 = _pen('enemy_kind2', mode)
    enemy3 = _pen('enemy_kind3', mode)
    bg = _pen('bg', mode)
    enemy0_sprite = _render_u8_const_array("enemy_kind0_sprite", _build_box_sprite_values(4, 16, bg, enemy0, variant=0))
    enemy1_sprite = _render_u8_const_array("enemy_kind1_sprite", _build_box_sprite_values(5, 14, bg, enemy1, variant=1))
    enemy2_sprite = _render_u8_const_array("enemy_kind2_sprite", _build_box_sprite_values(6, 10, bg, enemy2, variant=2))
    enemy3_sprite = _render_u8_const_array("enemy_kind3_sprite", _build_box_sprite_values(10, 18, bg, enemy3, variant=3))
    return "\n".join(
        [
            render_c_include("entities/enemy.h"),
            render_c_include("systems/collision.h"),
            render_c_include("<cpctelera.h>"),
            "",
            enemy0_sprite,
            "",
            enemy1_sprite,
            "",
            enemy2_sprite,
            "",
            enemy3_sprite,
            "",
            "void enemyinit(Enemy* enemy) {",
            "    if (!enemy) {",
            "        return;",
            "    }",
            "",
            "    enemy->x = 0;",
            "    enemy->y = 0;",
            "    enemy->vx = 0;",
            "    enemy->vy = 0;",
            "    enemy->w = 4;",
            "    enemy->h = 16;",
            "    enemy->active = 0;",
            "    enemy->health = 1;",
            "    enemy->reward = 100;",
            "    enemy->kind = 0;",
            "}",
            "",
            "void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {",
            "    if (!enemy) {",
            "        return;",
            "    }",
            "",
            "    enemy->x = x;",
            "    enemy->y = y;",
            "    enemy->vx = move_right ? 1 : -1;",
            "    enemy->vy = 0;",
            "    enemy->active = 1;",
            "    enemy->kind = kind;",
            "",
            "    if (kind == 1) {",
            "        enemy->w = 5;",
            "        enemy->h = 14;",
            "        enemy->health = 2;",
            "        enemy->reward = 180;",
            "        enemy->vx = move_right ? 2 : -2;",
            "    } else if (kind == 2) {",
            "        enemy->w = 6;",
            "        enemy->h = 10;",
            "        enemy->health = 1;",
            "        enemy->reward = 150;",
            "        enemy->vy = move_right ? 1 : -1;",
            "        enemy->vx = 1;",
            "    } else if (kind == 3) {",
            "        enemy->w = 10;",
            "        enemy->h = 18;",
            "        enemy->health = 8;",
            "        enemy->reward = 800;",
            "        enemy->vx = move_right ? 1 : -1;",
            "    } else {",
            "        enemy->w = 4;",
            "        enemy->h = 16;",
            "        enemy->health = 1;",
            "        enemy->reward = 100;",
            "    }",
            "}",
            "",
            "void enemyupdate(Enemy* enemy) {",
            "    i16 nextx;",
            "    i16 nexty;",
            "",
            "    if (!enemy || !enemy->active) {",
            "        return;",
            "    }",
            "",
            "    if (enemy->kind == 2) {",
            "        nextx = (i16)enemy->x + (i16)enemy->vx;",
            "        nexty = (i16)enemy->y + (i16)enemy->vy;",
            "",
            "        if (nextx < 8 || nextx > 72) {",
            "            enemy->vx = (i8)(-enemy->vx);",
            "            nextx = (i16)enemy->x + (i16)enemy->vx;",
            "        }",
            "        if (nexty < 56 || nexty > 120) {",
            "            enemy->vy = (i8)(-enemy->vy);",
            "            nexty = (i16)enemy->y + (i16)enemy->vy;",
            "        }",
            "",
            "        enemy->x = (u8)nextx;",
            "        enemy->y = (u8)nexty;",
            "        return;",
            "    }",
            "",
            "    nextx = (i16)enemy->x + (i16)enemy->vx;",
            "    if (nextx < 2) {",
            "        nextx = 2;",
            "        enemy->vx = 1;",
            "    }",
            "    {",
            "        i16 maxx = (i16)(80 - (i16)enemy->w);",
            "        if (nextx > maxx) {",
            "            nextx = maxx;",
            "            enemy->vx = -1;",
            "        }",
            "    }",
            "    enemy->x = (u8)nextx;",
            "",
            "    enemy->vy = (i8)(enemy->vy + 1);",
            "    if (enemy->vy > 3) enemy->vy = 3;",
            "    nexty = (i16)enemy->y + (i16)enemy->vy;",
            "    nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);",
            "    enemy->y = (u8)nexty;",
            "    if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {",
            "        enemy->vy = 0;",
            "    }",
            "}",
            "",
            "void enemyrender(const Enemy* enemy) {",
            "    u8* pvmem;",
            "    const u8* sprite;",
            "",
            "    if (!enemy || !enemy->active) {",
            "        return;",
            "    }",
            "",
            "    if (enemy->kind == 3) sprite = enemy_kind3_sprite;",
            "    else if (enemy->kind == 2) sprite = enemy_kind2_sprite;",
            "    else if (enemy->kind == 1) sprite = enemy_kind1_sprite;",
            "    else sprite = enemy_kind0_sprite;",
            "",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);",
            "    cpct_drawSprite((u8*)sprite, pvmem, enemy->w, enemy->h);",
            "}",
            "",
            "u8 enemydamage(Enemy* enemy, u8 damage) {",
            "    if (!enemy || !enemy->active) {",
            "        return 0;",
            "    }",
            "",
            "    if (damage >= enemy->health) {",
            "        enemy->health = 0;",
            "        enemy->active = 0;",
            "        return 1;",
            "    }",
            "",
            "    enemy->health = (u8)(enemy->health - damage);",
            "    return 0;",
            "}",
            "",
        ]
    )


def _build_projectile_c_stub(mode: int = 1) -> str:
    proj_basic = _pen('projectile_basic', mode)
    proj_up = _pen('projectile_upgraded', mode)
    proj_special = _pen('projectile_special', mode)
    bg = _pen('bg', mode)
    # Minimum 4x4 bytes for basic projectile -- 3x2 is too small to see at runtime.
    # Projectile sprites have no interior pixels (all border), so bg pen is unused.
    projectile_basic_sprite = _render_u8_const_array("projectile_basic_sprite", _build_box_sprite_values(4, 4, bg, proj_basic, variant=0))
    projectile_up_sprite = _render_u8_const_array("projectile_up_sprite", _build_box_sprite_values(3, 4, bg, proj_up, variant=1))
    projectile_special_sprite = _render_u8_const_array("projectile_special_sprite", _build_box_sprite_values(4, 4, bg, proj_special, variant=2))
    return "\n".join(
        [
            render_c_include("entities/projectile.h"),
            render_c_include("<cpctelera.h>"),
            "",
            projectile_basic_sprite,
            "",
            projectile_up_sprite,
            "",
            projectile_special_sprite,
            "",
            "void projectileinit(Projectile* projectile) {",
            "    if (!projectile) {",
            "        return;",
            "    }",
            "",
            "    projectile->x = 0;",
            "    projectile->y = 0;",
            "    projectile->vx = 0;",
            "    projectile->vy = 0;",
            "    projectile->w = 2;",
            "    projectile->h = 2;",
            "    projectile->active = 0;",
            "    projectile->damage = 1;",
            "    projectile->lifetime = 0;",
            "    projectile->weapon = 0;",
            "}",
            "",
            "void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {",
            "    if (!projectile) {",
            "        return;",
            "    }",
            "",
            "    projectile->x = x;",
            "    projectile->y = y;",
            "    projectile->vx = dir;",
            "    projectile->vy = 0;",
            "    projectile->weapon = weapon;",
            "    projectile->active = 1;",
            "",
            "    if (weapon == 0) {",
            "        projectile->w = 4;",
            "        projectile->h = 4;",
            "        projectile->damage = 1;",
            "        projectile->lifetime = 45;",
            "    } else if (weapon == 1) {",
            "        projectile->w = 2;",
            "        projectile->h = 3;",
            "        projectile->damage = 2;",
            "        projectile->lifetime = 28;",
            "    } else {",
            "        projectile->w = 4;",
            "        projectile->h = 3;",
            "        projectile->damage = 3;",
            "        projectile->lifetime = 56;",
            "        projectile->vx = (i8)(dir > 0 ? 4 : -4);",
            "    }",
            "}",
            "",
            "void projectileupdate(Projectile* projectile) {",
            "    if (!projectile || !projectile->active) {",
            "        return;",
            "    }",
            "",
            "    projectile->x = (u8)(projectile->x + projectile->vx);",
            "    projectile->y = (u8)(projectile->y + projectile->vy);",
            "",
            "    if (projectile->lifetime) {",
            "        projectile->lifetime--;",
            "    }",
            "",
            "    if (projectile->x > 78 || projectile->lifetime == 0) {",
            "        projectile->active = 0;",
            "    }",
            "}",
            "",
            "void projectilerender(const Projectile* projectile) {",
            "    u8* pvmem;",
            "    const u8* sprite;",
            "",
            "    if (!projectile || !projectile->active) {",
            "        return;",
            "    }",
            "",
            "    if (projectile->weapon == 0) sprite = projectile_basic_sprite;",
            "    else if (projectile->weapon == 1) sprite = projectile_up_sprite;",
            "    else sprite = projectile_special_sprite;",
            "",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);",
            "    cpct_drawSprite((u8*)sprite, pvmem, projectile->w, projectile->h);",
            "}",
            "",
        ]
    )


def _build_player_c_stub(mode: int = 1) -> str:
    hflip_fn = "cpct_hflipSpriteM0" if mode == 0 else ("cpct_hflipSpriteM2" if mode == 2 else "cpct_hflipSpriteM1")

    return "\n".join(
        [
            render_c_include("entities/player.h"),
            render_c_include("systems/input.h"),
            render_c_include("systems/collision.h"),
            render_c_include("data/sprites/playerknight.h"),
            render_c_include("<cpctelera.h>"),
            "",
            "/* Use #define instead of `static const i8` so values are inlined as immediates.",
            "   With --no-std-crt0 there is no GSINIT phase that copies INITIALIZER -> DATA. */",
            "#define kplayermovespeed     3",
            "#define kplayeracceleration  1",
            "#define kplayerdeceleration  1",
            "#define kplayergravity       1",
            "#define kplayermaxfall       4",
            "#define kplayerjumpvelocity  (-6)",
            "#define kplayerjumpboost     (-1)",
            "#define kplayerspritebytes   192",
            "",
            "static u8 gplayersprite[kplayerspritebytes];",
            "static u8 gplayerspritefacingleft;",
            "",
            "void playerinit(Player* player) {",
            "    u8 index;",
            "    if (!player) {",
            "        return;",
            "    }",
            "",
            "    player->x = 20;",
            "    player->y = 120;",
            "    player->vx = 0;",
            "    player->vy = 0;",
            "    player->w = 8;",
            "    player->h = 24;",
            "    player->health = 3;",
            "    player->weapon = 0;",
            "    player->facing_left = 0;",
            "    player->jump_hold = 0;",
            "    for (index = 0; index < kplayerspritebytes; ++index) {",
            "        gplayersprite[index] = sprplayerknight_data[index];",
            "    }",
            "    gplayerspritefacingleft = 0;",
            "}",
            "",
            "void playerupdate(Player* player) {",
            "    i16 nextx;",
            "    i16 nexty;",
            "",
            "    if (!player) {",
            "        return;",
            "    }",
            "",
            "    if (input_is_left_pressed()) {",
            "        player->vx = (i8)(player->vx - kplayeracceleration);",
            "        player->facing_left = 1;",
            "    } else if (input_is_right_pressed()) {",
            "        player->vx = (i8)(player->vx + kplayeracceleration);",
            "        player->facing_left = 0;",
            "    } else if (player->vx > 0) {",
            "        player->vx = (i8)(player->vx - kplayerdeceleration);",
            "        if (player->vx < 0) player->vx = 0;",
            "    } else if (player->vx < 0) {",
            "        player->vx = (i8)(player->vx + kplayerdeceleration);",
            "        if (player->vx > 0) player->vx = 0;",
            "    }",
            "",
            "    if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;",
            "    if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;",
            "",
            "    if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {",
            "        player->vy = kplayerjumpvelocity;",
            "        player->jump_hold = 5;",
            "    }",
            "",
            "    if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {",
            "        player->vy = (i8)(player->vy + kplayerjumpboost);",
            "        player->jump_hold--;",
            "    } else {",
            "        player->jump_hold = 0;",
            "    }",
            "",
            "    player->vy = (i8)(player->vy + kplayergravity);",
            "    if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;",
            "",
            "    nextx = (i16)player->x + (i16)player->vx;",
            "    if (nextx < 0) {",
            "        nextx = 0;",
            "    }",
            "    if (nextx > 72) {",
            "        nextx = 72;",
            "    }",
            "    player->x = (u8)nextx;",
            "",
            "    nexty = (i16)player->y + (i16)player->vy;",
            "    nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);",
            "    if (nexty < 0) {",
            "        nexty = 0;",
            "    }",
            "    player->y = (u8)nexty;",
            "",
            "    if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {",
            "        player->vy = 0;",
            "    }",
            "}",
            "",
            "void playerrender(const Player* player) {",
            "    u8* pvmem;",
            "",
            "    if (!player) {",
            "        return;",
            "    }",
            "",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);",
            "    if (player->facing_left != gplayerspritefacingleft) {",
            f"        {hflip_fn}(player->w, player->h, gplayersprite);",
            "        gplayerspritefacingleft = player->facing_left;",
            "    }",
            "    cpct_drawSprite(gplayersprite, pvmem, player->w, player->h);",
            "}",
            "",
            "u8 player_get_ammo(const Player* player) {",
            "    (void)player;",
            "    return 3;",
            "}",
            "",
            "u8 player_get_health(const Player* player) {",
            "    return player ? player->health : 0;",
            "}",
            "",
            "u8 player_get_weapon(const Player* player) {",
            "    return player ? player->weapon : 0;",
            "}",
            "",
        ]
    )


def _build_input_h_stub() -> str:
    return "\n".join(
        [
            "#ifndef SYSTEMS_INPUT_H",
            "#define SYSTEMS_INPUT_H",
            "",
            render_c_include("<cpctelera.h>"),
            "",
            "void input_update(void);",
            "u8 input_is_left_pressed(void);",
            "u8 input_is_right_pressed(void);",
            "u8 input_is_up_pressed(void);",
            "u8 input_is_down_pressed(void);",
            "u8 input_is_jump_pressed(void);",
            "u8 input_is_jump_just_pressed(void);",
            "u8 input_is_shoot_pressed(void);",
            "u8 input_is_shoot_just_pressed(void);",
            "",
            "#endif",
            "",
        ]
    )


def _build_input_c_stub() -> str:
    return "\n".join(
        [
            render_c_include("systems/input.h"),
            "",
            "static u8 ginputleft;",
            "static u8 ginputright;",
            "static u8 ginputup;",
            "static u8 ginputdown;",
            "static u8 ginputshoot;",
            "static u8 gprevjump;",
            "static u8 gprevshoot;",
            "",
            "void input_update(void) {",
            "    gprevjump = ginputup;",
            "    gprevshoot = ginputshoot;",
            "    cpct_scanKeyboard();",
            "    ginputleft = (u8)(cpct_isKeyPressed(Key_CursorLeft) || cpct_isKeyPressed(Key_A));",
            "    ginputright = (u8)(cpct_isKeyPressed(Key_CursorRight) || cpct_isKeyPressed(Key_D));",
            "    ginputup = (u8)(cpct_isKeyPressed(Key_CursorUp) || cpct_isKeyPressed(Key_W) || cpct_isKeyPressed(Key_Z));",
            "    ginputdown = (u8)(cpct_isKeyPressed(Key_CursorDown) || cpct_isKeyPressed(Key_S) || cpct_isKeyPressed(Key_X));",
            "    ginputshoot = (u8)(cpct_isKeyPressed(Key_Space) || cpct_isKeyPressed(Key_X) || cpct_isKeyPressed(Key_CursorDown));",
            "}",
            "",
            "u8 input_is_left_pressed(void) {",
            "    return ginputleft;",
            "}",
            "",
            "u8 input_is_right_pressed(void) {",
            "    return ginputright;",
            "}",
            "",
            "u8 input_is_up_pressed(void) {",
            "    return ginputup;",
            "}",
            "",
            "u8 input_is_down_pressed(void) {",
            "    return ginputdown;",
            "}",
            "",
            "u8 input_is_jump_pressed(void) {",
            "    return ginputup;",
            "}",
            "",
            "u8 input_is_jump_just_pressed(void) {",
            "    return (u8)(ginputup && !gprevjump);",
            "}",
            "",
            "u8 input_is_shoot_pressed(void) {",
            "    return ginputshoot;",
            "}",
            "",
            "u8 input_is_shoot_just_pressed(void) {",
            "    return (u8)(ginputshoot && !gprevshoot);",
            "}",
            "",
        ]
    )


def _build_collision_h_stub() -> str:
    return "\n".join(
        [
            "#ifndef SYSTEMS_COLLISION_H",
            "#define SYSTEMS_COLLISION_H",
            "",
            render_c_include("<cpctelera.h>"),
            "",
            "void collision_init(void);",
            "u8 collision_is_on_ground(i16 y, u8 h);",
            "u8 collision_is_on_ground_at(i16 x, i16 y, u8 h);",
            "i16 collision_clamp_y_to_ground(i16 y, u8 h);",
            "i16 collision_clamp_y_at(i16 x, i16 y, u8 h);",
            "u8 collision_is_on_trap(i16 x, i16 y, u8 w, u8 h);",
            "u8 collision_is_on_ladder(i16 x, i16 y, u8 w, u8 h);",
            "",
            "#endif",
            "",
        ]
    )


def _build_collision_c_stub() -> str:
    return "\n".join(
        [
            render_c_include("systems/collision.h"),
            render_c_include("systems/tilemap.h"),
            "",
            "static i16 ggroundy = 160;",
            "",
            "void collision_init(void) {",
            "    ggroundy = (i16)tilemap_ground_y();",
            "}",
            "",
            "u8 collision_is_on_ground(i16 y, u8 h) {",
            "    return collision_is_on_ground_at(0, y, h);",
            "}",
            "",
            "u8 collision_is_on_ground_at(i16 x, i16 y, u8 h) {",
            "    i16 feet;",
            "    i16 support;",
            "",
            "    (void)x;",
            "    support = (i16)tilemap_ground_y();",
            "    feet = y + (i16)h;",
            "    return (u8)(feet >= support);",
            "}",
            "",
            "i16 collision_clamp_y_to_ground(i16 y, u8 h) {",
            "    return collision_clamp_y_at(0, y, h);",
            "}",
            "",
            "i16 collision_clamp_y_at(i16 x, i16 y, u8 h) {",
            "    i16 maxy;",
            "",
            "    (void)x;",
            "    ggroundy = (i16)tilemap_ground_y();",
            "    maxy = ggroundy - (i16)h;",
            "    if (y > maxy) {",
            "        return maxy;",
            "    }",
            "    return y;",
            "}",
            "",
            "u8 collision_is_on_trap(i16 x, i16 y, u8 w, u8 h) {",
            "    (void)x;",
            "    (void)y;",
            "    (void)w;",
            "    (void)h;",
            "    return 0;",
            "}",
            "",
            "u8 collision_is_on_ladder(i16 x, i16 y, u8 w, u8 h) {",
            "    (void)x;",
            "    (void)y;",
            "    (void)w;",
            "    (void)h;",
            "    return 0;",
            "}",
            "",
        ]
    )


def _build_tilemap_h_stub() -> str:
    return "\n".join(
        [
            "#ifndef SYSTEMS_TILEMAP_H",
            "#define SYSTEMS_TILEMAP_H",
            "",
            render_c_include("<cpctelera.h>"),
            "",
            "void tilemap_init(void);",
            "void tilemap_render(void);",
            "u8 tilemap_ground_y(void);",
            "u8 tilemap_is_solid(u8 x, u8 y, u8 w, u8 h);",
            "u8 tilemap_is_on_ground(u8 x, u8 y);",
            "u8 tilemap_platform_y_at(i16 x);",
            "u8 get_tile_at(i16 x, i16 y);",
            "u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h);",
            "u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h);",
            "u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h);",
            "u8 tilemap_goal_x(void);",
            "",
            "#endif",
            "",
        ]
    )


def _build_tilemap_c_stub(mode: int = 1) -> str:
    return "\n".join(
        [
            render_c_include("systems/tilemap.h"),
            render_c_include("<cpctelera.h>"),
            "",
            "static u8 gtilegroundy = 136;",
            "static u8 gtileplatformy = 96;",
            "static u8 ggoalx = 72;",
            "",
            "void tilemap_init(void) {",
            "    gtilegroundy = 136;",
            "    if (gtilegroundy > 152) gtilegroundy = 152;",
            "    gtileplatformy = (u8)(gtilegroundy - 40);",
            "    ggoalx = 72;",
            "}",
            "",
            "void tilemap_render(void) {",
            "    u8* pvmem;",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, 24);",
            f"    cpct_drawSolidBox(pvmem, {_fill_for('decor', mode)}, 80, 88);",
            "",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);",
            f"    cpct_drawSolidBox(pvmem, {_fill_for('ground', mode)}, 80, 16);",
            "",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);",
            f"    cpct_drawSolidBox(pvmem, {_fill_for('platform', mode)}, 20, 6);",
            "",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 50, gtileplatformy + 18);",
            f"    cpct_drawSolidBox(pvmem, {_fill_for('platform', mode)}, 18, 6);",
            "",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);",
            f"    cpct_drawSolidBox(pvmem, {_fill_for('decor', mode)}, 16, 2);",
            "",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);",
            f"    cpct_drawSolidBox(pvmem, {_fill_for('goal', mode)}, 2, 16);",
            "}",
            "",
            "u8 tilemap_ground_y(void) {",
            "    return gtilegroundy;",
            "}",
            "",
            "u8 tilemap_is_solid(u8 x, u8 y, u8 w, u8 h) {",
            "    i16 left;",
            "    i16 right;",
            "    i16 top;",
            "    i16 bottom;",
            "",
            "    left = (i16)x;",
            "    right = left + (i16)w - 1;",
            "    top = (i16)y;",
            "    bottom = top + (i16)h - 1;",
            "",
            "    if (bottom >= (i16)gtilegroundy - 1) {",
            "        return 1;",
            "    }",
            "    if (bottom >= (i16)gtileplatformy - 1 && bottom <= (i16)gtileplatformy + 2 && right >= 24 && left <= 56) {",
            "        return 1;",
            "    }",
            "    return 0;",
            "}",
            "",
            "u8 tilemap_is_on_ground(u8 x, u8 y) {",
            "    return tilemap_is_solid(x, (u8)(y + 1), 1, 1);",
            "}",
            "",
            "u8 tilemap_platform_y_at(i16 x) {",
            "    if (x >= 24 && x <= 56) {",
            "        return gtileplatformy;",
            "    }",
            "    return 255;",
            "}",
            "",
            "u8 get_tile_at(i16 x, i16 y) {",
            "    if (y >= (i16)gtilegroundy - 8) {",
            "        return 1;",
            "    }",
            "    if (y >= (i16)gtileplatformy - 4 && y < (i16)gtileplatformy + 4 && x >= 24 && x <= 56) {",
            "        return 2;",
            "    }",
            "    return 0;",
            "}",
            "",
            "u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {",
            "    i16 left;",
            "    i16 right;",
            "    i16 feet;",
            "",
            "    left = x;",
            "    right = x + (i16)w;",
            "    feet = y + (i16)h;",
            "",
            "    if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {",
            "        return 1;",
            "    }",
            "    return 0;",
            "}",
            "",
            "u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {",
            "    (void)x;",
            "    (void)y;",
            "    (void)w;",
            "    (void)h;",
            "    return 0;",
            "}",
            "",
            "u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {",
            "    (void)x;",
            "    (void)y;",
            "    (void)w;",
            "    (void)h;",
            "    return 0;",
            "}",
            "",
            "u8 tilemap_goal_x(void) {",
            "    return ggoalx;",
            "}",
            "",
        ]
    )


def _build_level1_h_stub(mode: int = 1) -> str:
    palette_size = PALETTE_SIZE_BY_MODE.get(mode, 4)
    return "\n".join(
        [
            "#ifndef DATA_LEVEL1_H",
            "#define DATA_LEVEL1_H",
            "",
            render_c_include("<cpctelera.h>"),
            "",
            f"#define GPALETTE_SIZE {palette_size}",
            "",
            "extern const u8 level1tilemap[];",
            "extern const u8 level1tileproperties[];",
            "extern const u8 gpalette[GPALETTE_SIZE];",
            "extern const u16 level1tilemapwidth;",
            "extern const u16 level1tilemapheight;",
            "",
            "#endif",
            "",
        ]
    )


def _build_level1_c_stub(mode: int = 1, palette_hw: list[int] | None = None) -> str:
    if palette_hw is None:
        palette_hw = _resolve_palette_hw(None, mode)
    palette_size = PALETTE_SIZE_BY_MODE.get(mode, 4)
    palette_hw = list(palette_hw)[:palette_size]
    if len(palette_hw) < palette_size:
        palette_hw = (palette_hw + DEFAULT_PALETTE_HW_BY_MODE.get(mode, []))[:palette_size]
    palette_lines = ["    " + ", ".join(str(v) for v in palette_hw)]
    return "\n".join(
        [
            '#include "data/level1.h"',
            "",
            "const u16 level1tilemapwidth = 20;",
            "const u16 level1tilemapheight = 18;",
            "",
            "const u8 level1tilemap[] = {",
            "    1, 1, 1, 1, 1, 1, 1, 1, 1, 1,",
            "    1, 0, 0, 0, 0, 0, 0, 0, 0, 1,",
            "    1, 1, 1, 1, 1, 1, 1, 1, 1, 1",
            "};",
            "",
            "const u8 level1tileproperties[] = { 0, 1 };",
            "",
            "const u8 gpalette[GPALETTE_SIZE] = {",
            *palette_lines,
            "};",
            "",
        ]
    )


def _build_fixed_asset_header(path: str, symbol: str) -> str:
    guard = _header_guard(path)
    return "\n".join(
        [
            f"#ifndef {guard}",
            f"#define {guard}",
            "",
            render_c_include("<cpctelera.h>"),
            "",
            f"extern const u8 {symbol}[];",
            "",
            "#endif",
            "",
        ]
    )


def _build_fixed_asset_source(header_path: str, symbol: str) -> str:
    array_decl = render_c_const_array("u8", symbol, _build_visible_asset_values(symbol))
    return "\n".join(
        [
            render_c_include(header_path),
            "",
            array_decl,
            "",
        ]
    )


def _build_hud_h_stub() -> str:
    return "\n".join(
        [
            "#ifndef SYSTEMS_HUD_H",
            "#define SYSTEMS_HUD_H",
            "",
            render_c_include("<cpctelera.h>"),
            "",
            render_c_function_decl("void", "hudinit", []),
            render_c_function_decl(
                "void",
                "hudupdate",
                [("u8", "lives"), ("u16", "score"), ("u8", "time"), ("u8", "weapon")],
            ),
            render_c_function_decl("void", "hudrender", []),
            "",
            "#endif",
            "",
        ]
    )


def _build_hud_c_stub(mode: int = 1) -> str:
    bg = _pen('bg', mode)
    health = _pen('player', mode)
    lives = _pen('enemy', mode)
    digits = [_render_u8_const_array(f"huddigit_{digit}", _digit_sprite_values(digit, bg, health)) for digit in range(10)]
    lives_sprite = _render_u8_const_array("hudlives", _build_box_sprite_values(4, 8, bg, lives, variant=2))
    return "\n".join(
        [
            '#include "systems/hud.h"',
            '#include "data/hud/healthbar.h"',
            "",
            "static u8  currenthealth;",
            "static u16 currentscore;",
            "static u8  currenttime;",
            "static u8  currentlives;",
            "static u8  currentweapon;",
            "",
            lives_sprite,
            "",
            *digits,
            "",
            "/* GSINIT-safe digit lookup: a function avoids initialised pointer arrays",
            "   (those require the INITIALIZER -> DATA copy that --no-std-crt0 skips). */",
            "static const u8* hud_get_number_sprite(u8 digit) {",
            "    switch (digit % 10) {",
            "    case 0: return huddigit_0;",
            "    case 1: return huddigit_1;",
            "    case 2: return huddigit_2;",
            "    case 3: return huddigit_3;",
            "    case 4: return huddigit_4;",
            "    case 5: return huddigit_5;",
            "    case 6: return huddigit_6;",
            "    case 7: return huddigit_7;",
            "    case 8: return huddigit_8;",
            "    default: return huddigit_9;",
            "    }",
            "}",
            "",
            "static void hud_draw_digits(u16 value, u8 digits, u8 startx, u8 y) {",
            "    u8 i;",
            "    u8 digit;",
            "    u16 divisor;",
            "    u8* pvmem;",
            "",
            "    divisor = 1;",
            "    for (i = 1; i < digits; ++i) {",
            "        divisor *= 10;",
            "    }",
            "",
            "    for (i = 0; i < digits; ++i) {",
            "        digit = (u8)(value / divisor);",
            "        value = (u16)(value % divisor);",
            "",
            "        pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 4), y);",
            "        cpct_drawSprite((u8*)hud_get_number_sprite(digit), pvmem, 4, 8);",
            "",
            "        if (divisor > 1) {",
            "            divisor /= 10;",
            "        }",
            "    }",
            "}",
            "",
            "void hudinit(void) {",
            "    currenthealth = 3;",
            "    currentscore  = 0;",
            "    currenttime   = 90;",
            "    currentlives  = 3;",
            "    currentweapon = 0;",
            "}",
            "",
            "void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {",
            "    currenthealth = lives;",
            "    currentscore  = score;",
            "    currenttime   = time;",
            "    currentlives  = lives;",
            "    currentweapon = weapon;",
            "}",
            "",
            "void hudrender(void) {",
            "    u8 i;",
            "    u8* pvmem;",
            "    u16 scoretemp;",
            "    u8 timetemp;",
            "",
            "    for (i = 0; i < currenthealth; ++i) {",
            "        pvmem = cpct_getScreenPtr(CPCT_VMEM_START, (i * 8), 2);",
            "        cpct_drawSprite((u8*)hudhealthbar_data, pvmem, 4, 8);",
            "    }",
            "",
            "    scoretemp = currentscore;",
            "    hud_draw_digits(scoretemp, 4, 24, 2);",
            "",
            "    timetemp = currenttime;",
            "    hud_draw_digits((u16)timetemp, 3, 56, 2);",
            "",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);",
            "    cpct_drawSprite((u8*)hudlives, pvmem, 4, 8);",
            "",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);",
            "    cpct_drawSprite((u8*)hud_get_number_sprite(currentlives % 10), pvmem, 4, 8);",
            "",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 70, 180);",
            "    cpct_drawSprite((u8*)hud_get_number_sprite(currentweapon % 10), pvmem, 4, 8);",
            "}",
            "",
        ]
    )


def _build_hud_c_safe_stub(mode: int = 1) -> str:
    bg = _pen('bg', mode)
    hud = _pen('hud', mode)
    return "\n".join(
        [
            '#include "systems/hud.h"',
            '#include <cpctelera.h>',
            "",
            "void hud_init(void) {}",
            "void hud_update(void) {}",
            "",
            "void hud_render(void) {",
            "    u8* pvmem;",
            "    cpct_drawSolidBox(CPCT_VMEM_START, " + str(bg) + ", 40, 8);",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 1);",
            "    cpct_drawSolidBox(pvmem, " + str(hud) + ", 3, 6);",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 8, 1);",
            "    cpct_drawSolidBox(pvmem, " + str(hud) + ", 3, 6);",
            "}",
            "",
        ]
    )


def _header_guard(path: str) -> str:
    token = re.sub(r"[^A-Za-z0-9]", "_", str(path).upper())
    return token or "ASSET_HEADER_H"


def _asset_token(value: str) -> str:
    normalized = normalize_asset_token(str(value))
    if normalized:
        return normalized
    fallback = "".join(ch for ch in str(value).lower() if ch.isalnum() or ch == "_")
    return fallback


def _asset_symbol_name(asset_name: str, target_path: str) -> str:
    token = _asset_token(asset_name)
    if not token:
        token = "".join(ch for ch in PurePosixPath(target_path).stem.lower() if ch.isalnum() or ch == "_")
    if not token:
        token = "asset"
    if not (token[0].isalpha() or token[0] == "_"):
        token = f"asset_{token}"
    return f"{token}_data"


def _build_asset_header_stub_with_symbol(path: str, symbol: str) -> str:
    guard = _header_guard(path)
    return "\n".join(
        [
            f"#ifndef {guard}",
            f"#define {guard}",
            "",
            render_c_include("<cpctelera.h>"),
            "",
            render_c_array_decl("u8", symbol, None, qualifiers=["extern", "const"]),
            "",
            "#endif",
            "",
        ]
    )


def _build_asset_header_stub(path: str, asset_name: str) -> str:
    symbol = _asset_symbol_name(asset_name, path)
    return _build_asset_header_stub_with_symbol(path, symbol)


def _extract_declared_asset_symbol(content: str) -> str:
    match = re.search(r"extern\s+const\s+u8\s+([A-Za-z_][A-Za-z0-9_]*)\s*\[\s*\]\s*;", content)
    if not match:
        return ""
    return match.group(1)


def _sanitize_asset_headers(
    files: dict[str, str],
    allowed_files: set[str],
) -> tuple[dict[str, str], list[str]]:
    normalized = dict(files)
    sanitized: list[str] = []

    for path, content in list(normalized.items()):
        if not path.startswith("src/data/assets/") or not path.endswith(".h"):
            continue
        if not _is_allowed(path, allowed_files):
            continue

        text = str(content)
        lowered = text.lower()
        if "typedef struct" not in lowered and "typedef enum" not in lowered:
            continue

        symbol = _extract_declared_asset_symbol(text)
        if not symbol:
            symbol = _asset_symbol_name(PurePosixPath(path).stem, path)

        replacement = _build_asset_header_stub_with_symbol(path, symbol)
        if replacement != text:
            normalized[path] = replacement
            sanitized.append(path)

    return normalized, sorted(set(sanitized))


def _sanitize_enemy_source_files(
    files: dict[str, str],
    allowed_files: set[str],
) -> tuple[dict[str, str], list[str]]:
    normalized = dict(files)
    sanitized: list[str] = []

    if not _is_allowed(ENEMY_C_PATH, allowed_files):
        return normalized, sanitized

    current = normalized.get(ENEMY_C_PATH)
    if not current:
        return normalized, sanitized

    enemy_c = str(current)
    enemy_h = str(normalized.get(ENEMY_H_PATH, ""))

    has_local_enemy_typedef = bool(
        re.search(r"typedef\s+struct\s*\{[\s\S]*?\}\s*Enemy\s*;", enemy_c)
    )
    uses_enemy_type = "EnemyType" in enemy_c
    header_declares_enemy_type = bool(
        re.search(r"typedef\s+enum[\s\S]*?EnemyType\s*;", enemy_h)
    )

    required_api_patterns = (
        r"\bvoid\s+enemyinit\s*\(\s*Enemy\s*\*\s*[A-Za-z_][A-Za-z0-9_]*\s*\)",
        r"\bvoid\s+enemyupdate\s*\(\s*Enemy\s*\*\s*[A-Za-z_][A-Za-z0-9_]*\s*\)",
        r"\bvoid\s+enemyrender\s*\(\s*const\s+Enemy\s*\*\s*[A-Za-z_][A-Za-z0-9_]*\s*\)",
    )
    has_required_api = all(re.search(pattern, enemy_c) for pattern in required_api_patterns)

    struct_match = re.search(r"typedef\s+struct\s*\{(?P<body>[\s\S]*?)\}\s*Enemy\s*;", enemy_h)
    declared_fields: set[str] = set()
    if struct_match:
        for line in struct_match.group("body").splitlines():
            cleaned = line.split("//", 1)[0].strip()
            if not cleaned:
                continue
            field_match = re.search(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*(?:\[[^\]]*\])?\s*;\s*$", cleaned)
            if field_match:
                declared_fields.add(field_match.group(1))

    accessed_fields = set(re.findall(r"(?:->|\.)\s*([A-Za-z_][A-Za-z0-9_]*)", enemy_c))
    unknown_fields = sorted(name for name in accessed_fields if declared_fields and name not in declared_fields)

    should_replace = (
        has_local_enemy_typedef
        or (uses_enemy_type and not header_declares_enemy_type)
        or (not has_required_api)
        or bool(unknown_fields)
    )

    if should_replace:
        if _is_allowed(ENEMY_H_PATH, allowed_files):
            replacement_h = _build_enemy_h_stub()
            if replacement_h != enemy_h:
                normalized[ENEMY_H_PATH] = replacement_h
                sanitized.append(ENEMY_H_PATH)

        replacement = _build_enemy_c_stub()
        if replacement != enemy_c:
            normalized[ENEMY_C_PATH] = replacement
            sanitized.append(ENEMY_C_PATH)

    # Keep collision API coherent with enemy runtime stubs when enemy logic
    # depends on helper functions not present in a minimal collision header.
    collision_h = str(normalized.get(COLLISION_H_PATH, ""))
    enemy_uses_collision_runtime_api = (
        "collision_clamp_y_at(" in enemy_c
        or "collision_is_on_ground_at(" in enemy_c
    )
    collision_h_has_runtime_api = bool(
        re.search(r"\bi16\s+collision_clamp_y_at\s*\(", collision_h)
    ) and bool(
        re.search(r"\bu8\s+collision_is_on_ground_at\s*\(", collision_h)
    )

    if enemy_uses_collision_runtime_api and not collision_h_has_runtime_api:
        if _is_allowed(COLLISION_H_PATH, allowed_files):
            replacement_collision_h = _build_collision_h_stub()
            if replacement_collision_h != collision_h:
                normalized[COLLISION_H_PATH] = replacement_collision_h
                sanitized.append(COLLISION_H_PATH)

        if _is_allowed(COLLISION_C_PATH, allowed_files):
            collision_c = str(normalized.get(COLLISION_C_PATH, ""))
            collision_c_has_runtime_api = (
                "collision_clamp_y_at(" in collision_c
                and "collision_is_on_ground_at(" in collision_c
            )
            if not collision_c_has_runtime_api:
                replacement_collision_c = _build_collision_c_stub()
                if replacement_collision_c != collision_c:
                    normalized[COLLISION_C_PATH] = replacement_collision_c
                    sanitized.append(COLLISION_C_PATH)

    # Some generations wire collision.c against a different enemy runtime
    # contract (ENEMY_MAX|MAX_ENEMIES, enemies[]|g_enemies[],
    # ENEMY_STATE_*|ENEMY_DEAD) while enemy.h provides
    # only enemyinit/enemyspawn style APIs. Replace collision with a coherent
    # generic stub in that case.
    collision_h_current = str(normalized.get(COLLISION_H_PATH, ""))
    collision_c_current = str(normalized.get(COLLISION_C_PATH, ""))
    enemy_h_current = str(normalized.get(ENEMY_H_PATH, ""))

    collision_uses_enemy_globals = bool(
        re.search(r"\bENEMY_MAX\b", collision_c_current)
        or re.search(r"\bMAX_ENEMIES\b", collision_c_current)
        or re.search(r"\benemies\s*\[", collision_c_current)
        or re.search(r"\bg_enemies\s*\[", collision_c_current)
        or re.search(r"\bENEMY_STATE_[A-Z0-9_]+\b", collision_c_current)
        or re.search(r"\bENEMY_DEAD\b", collision_c_current)
    )
    enemy_header_supports_enemy_globals = bool(
        (re.search(r"\bENEMY_MAX\b", enemy_h_current) or re.search(r"\bMAX_ENEMIES\b", enemy_h_current))
        and (
            re.search(r"\bextern\s+Enemy\s+enemies\s*\[", enemy_h_current)
            or re.search(r"\bextern\s+Enemy\s+g_enemies\s*\[", enemy_h_current)
        )
        and (
            re.search(r"\bENEMY_STATE_[A-Z0-9_]+\b", enemy_h_current)
            or re.search(r"\bENEMY_DEAD\b", enemy_h_current)
        )
    )

    if collision_uses_enemy_globals and not enemy_header_supports_enemy_globals:
        if _is_allowed(COLLISION_H_PATH, allowed_files):
            replacement_collision_h = _build_collision_h_stub()
            if replacement_collision_h != collision_h_current:
                normalized[COLLISION_H_PATH] = replacement_collision_h
                sanitized.append(COLLISION_H_PATH)

        if _is_allowed(COLLISION_C_PATH, allowed_files):
            replacement_collision_c = _build_collision_c_stub()
            if replacement_collision_c != collision_c_current:
                normalized[COLLISION_C_PATH] = replacement_collision_c
                sanitized.append(COLLISION_C_PATH)

    projectile_c_current = str(normalized.get(PROJECTILE_C_PATH, ""))
    projectile_uses_enemy_globals = bool(
        re.search(r"\bENEMY_MAX\b", projectile_c_current)
        or re.search(r"\benemies\s*\[", projectile_c_current)
        or re.search(r"\bENEMY_STATE_[A-Z0-9_]+\b", projectile_c_current)
    )

    if projectile_uses_enemy_globals and not enemy_header_supports_enemy_globals:
        if _is_allowed(PROJECTILE_C_PATH, allowed_files):
            replacement_projectile_c = re.sub(
                r"for\s*\(\s*u8\s+j\s*=\s*0\s*;\s*j\s*<\s*ENEMY_MAX\s*;\s*\+\+j\s*\)\s*\{[\s\S]*?\n\s*\}",
                "/* enemy collision disabled: incompatible ENEMY_MAX/enemies contract */",
                projectile_c_current,
                count=1,
            )
            replacement_projectile_c = replacement_projectile_c.replace("#include \"entities/enemy.h\"\n", "")
            if replacement_projectile_c != projectile_c_current:
                normalized[PROJECTILE_C_PATH] = replacement_projectile_c
                sanitized.append(PROJECTILE_C_PATH)

    return normalized, sorted(set(sanitized))


def _sanitize_input_source_files(
    files: dict[str, str],
    allowed_files: set[str],
) -> tuple[dict[str, str], list[str]]:
    normalized = dict(files)
    sanitized: list[str] = []

    for path, content in list(normalized.items()):
        if not path.endswith("/input.c"):
            continue
        if not _is_allowed(path, allowed_files):
            continue

        text = str(content)
        if "cpct_scanKeyboard_f(" not in text:
            continue

        replacement = text.replace("cpct_scanKeyboard_f(", "cpct_scanKeyboard(")
        if replacement != text:
            normalized[path] = replacement
            sanitized.append(path)

    return normalized, sorted(set(sanitized))


def _sanitize_tilemap_source_files(
    files: dict[str, str],
    allowed_files: set[str],
    tech_output: dict | None,
) -> tuple[dict[str, str], list[str]]:
    normalized = dict(files)
    sanitized: list[str] = []

    if not (_is_allowed(TILEMAP_H_PATH, allowed_files) and _is_allowed(TILEMAP_C_PATH, allowed_files)):
        return normalized, sanitized

    tilemap_h = str(normalized.get(TILEMAP_H_PATH, ""))
    tilemap_c = str(normalized.get(TILEMAP_C_PATH, ""))
    if not tilemap_h or not tilemap_c:
        return normalized, sanitized

    mode = _resolve_video_mode(tech_output)
    tile_w_match = re.search(r"#define\s+TILE_W\s+(\d+)", tilemap_h)
    tile_w = int(tile_w_match.group(1)) if tile_w_match else 0

    # cpct_getScreenPtr X and cpct_drawSolidBox width are byte units.
    # If a generated tilemap uses TILE_W as pixel-size (e.g. 16 in Mode 1),
    # rendering goes mostly off-screen/garbled.
    suspicious_byte_units = bool(
        re.search(r"cpct_getScreenPtr\s*\(\s*CPCT_VMEM_START\s*,\s*[^,]*\*[^,]*TILE_W", tilemap_c)
    ) and tile_w >= 8
    suspicious_fill_bytes = mode == 1 and bool(
        re.search(r"cpct_drawSolidBox\s*\([^,]+,\s*0x[0-9A-Fa-f]{1,2}\s*,", tilemap_c)
    )
    uses_undefined_player_dims = bool(
        re.search(r"\bPLAYER_(?:W|H)\b", tilemap_c)
        and not re.search(r"#define\s+PLAYER_(?:W|H)\b", tilemap_c)
    )
    # SDCC is C89: variable declarations inside for(...) are not allowed.
    # e.g.  for (u8 ty = 0; ...) is invalid and causes "syntax error: token -> 'u8'"
    uses_c99_for_decl = bool(
        re.search(r"for\s*\(\s*(u8|u16|u32|i8|i16|i32|int|char|unsigned)\s+\w+\s*=", tilemap_c)
    )

    if suspicious_byte_units or suspicious_fill_bytes or uses_undefined_player_dims or uses_c99_for_decl:
        normalized[TILEMAP_H_PATH] = _build_tilemap_h_stub()
        normalized[TILEMAP_C_PATH] = _build_tilemap_c_stub(mode)
        sanitized.extend([TILEMAP_H_PATH, TILEMAP_C_PATH])

    return normalized, sorted(set(sanitized))


def _sanitize_game_source_files(
    files: dict[str, str],
    allowed_files: set[str],
    tech_output: dict | None,
) -> tuple[dict[str, str], list[str]]:
    normalized = dict(files)
    sanitized: list[str] = []

    if not _is_allowed(GAME_C_PATH, allowed_files):
        return normalized, sanitized

    game_c = str(normalized.get(GAME_C_PATH, ""))
    if not game_c:
        return normalized, sanitized

    mode = _resolve_video_mode(tech_output)
    replacement = game_c
    suspicious_palette_as_fill = bool(
        re.search(r"cpct_clearScreen\s*\(\s*game_palette\s*\[", replacement)
        or re.search(r"cpct_drawSolidBox\s*\([^\)]*game_palette\s*\[", replacement)
    )

    if re.search(
        r"\b(enemy_update_all|projectile_update_all|tilemap_render_dirty|player_save_prev|enemy_save_prev_all|projectile_save_prev_all|enemy_update\s*\(|projectile_update\s*\(|enemy_render_all\s*\(|projectile_render_all\s*\()",
        replacement,
    ):
        replacement = _build_game_c_stub(mode)
    elif suspicious_palette_as_fill:
        replacement = _build_game_c_stub(mode)
    elif mode == 1:
        replacement = replacement.replace("cpct_setVideoMode(0)", "cpct_setVideoMode(1)")

    if replacement != game_c:
        normalized[GAME_C_PATH] = replacement
        sanitized.append(GAME_C_PATH)

    return normalized, sorted(set(sanitized))


def _sanitize_integer_aliases(
    files: dict[str, str],
    allowed_files: set[str],
) -> tuple[dict[str, str], list[str]]:
    normalized = dict(files)
    sanitized: list[str] = []

    for path, content in list(normalized.items()):
        if not _is_allowed(path, allowed_files):
            continue
        if not (path.endswith(".c") or path.endswith(".h")):
            continue

        text = str(content)
        replacement = text
        replacement = re.sub(r"\bs8\b", "i8", replacement)
        replacement = re.sub(r"\bs16\b", "i16", replacement)
        replacement = re.sub(r"\bs32\b", "i32", replacement)

        if replacement != text:
            normalized[path] = replacement
            sanitized.append(path)

    return normalized, sorted(set(sanitized))


# SDCC compiles as C89: variables must be declared at the top of a block,
# not inside a for(...) initialiser.  This sanitizer hoists the loop variable
# declaration to just before the for statement so the code compiles cleanly.
_C99_FOR_TYPES = r"u8|u16|u32|i8|i16|i32|int|char|unsigned\s+char|unsigned\s+int"
_C99_FOR_RE = re.compile(
    r"(\n([ \t]*)for\s*\(\s*(" + _C99_FOR_TYPES + r")\s+(\w+)\s*=\s*([^;]+);)",
    re.MULTILINE,
)


def _hoist_for_decl(m: re.Match) -> str:  # type: ignore[type-arg]
    _full, indent, typ, varname, init = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
    return f"\n{indent}{typ} {varname};\n{indent}for ({varname} = {init};"


def _sanitize_c89_for_loops(
    files: dict[str, str],
    allowed_files: set[str],
) -> tuple[dict[str, str], list[str]]:
    """Replace C99-style 'for (TYPE var = ...)' with C89-compatible hoisted declarations."""
    normalized = dict(files)
    sanitized: list[str] = []

    for path, content in list(normalized.items()):
        if not _is_allowed(path, allowed_files):
            continue
        if not path.endswith(".c"):
            continue

        text = str(content)
        replacement = _C99_FOR_RE.sub(_hoist_for_decl, text)
        if replacement != text:
            normalized[path] = replacement
            sanitized.append(path)

    return normalized, sorted(set(sanitized))


def _sanitize_hud_source_files(
    files: dict[str, str],
    allowed_files: set[str],
    tech_output: dict | None,
) -> tuple[dict[str, str], list[str]]:
    normalized = dict(files)
    sanitized: list[str] = []

    if not _is_allowed(HUD_C_PATH, allowed_files):
        return normalized, sanitized

    hud_c = str(normalized.get(HUD_C_PATH, ""))
    if not hud_c:
        return normalized, sanitized

    mode = _resolve_video_mode(tech_output)
    replacement = _build_hud_c_safe_stub(mode)

    if replacement != hud_c:
        normalized[HUD_C_PATH] = replacement
        sanitized.append(HUD_C_PATH)

    return normalized, sorted(set(sanitized))


def _build_asset_source_stub(path: str, header_path: str, asset_name: str) -> str:
    symbol = _asset_symbol_name(asset_name, path)

    if "level1tileproperties" in _asset_token(asset_name):
        array_decl = render_c_const_array("u8", "level1tileproperties", ["0x00", "0x01", "0x01", "0x00"])
    else:
        array_decl = render_c_const_array("u8", symbol, _build_visible_asset_values(symbol))

    return "\n".join(
        [
            render_c_include(header_path),
            "",
            array_decl,
            "",
        ]
    )


def _as_list(value) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [str(value).strip()]


def _as_dict(value) -> dict:
    return value if isinstance(value, dict) else {}


def _normalize_compile_profile(value: str) -> str:
    token = "".join(ch for ch in str(value).strip().lower() if ch.isalpha())
    profile_map = {
        "prototype": "prototype",
        "verticalslice": "vertical_slice",
        "playableslice": "playable_slice",
    }
    return profile_map.get(token, "playable_slice")


def _runtime_contract(tech_output: dict | None) -> dict:
    payload = _as_dict(tech_output)
    return _as_dict(payload.get("runtime_contract"))


def _runtime_compile_profile(tech_output: dict | None) -> str:
    runtime = _runtime_contract(tech_output)
    return _normalize_compile_profile(runtime.get("compile_profile", "playable_slice"))


def _normalize_src_path(path: str) -> str:
    candidate = str(path).strip().replace("\\", "/")
    if not candidate:
        return ""
    if candidate.startswith("./"):
        candidate = candidate[2:]
    if not candidate.startswith("src/"):
        return ""
    return PurePosixPath(candidate).as_posix()


def _runtime_critical_modules(tech_output: dict | None) -> set[str]:
    runtime = _runtime_contract(tech_output)
    critical: set[str] = set()

    for path in _as_list(runtime.get("critical_modules")):
        normalized = _normalize_src_path(path)
        if normalized and normalized.endswith(".c"):
            critical.add(normalized)

    return critical


def _runtime_modules_to_preserve(tech_output: dict | None) -> set[str]:
    preserved = set(MANDATORY_RUNTIME_MODULES)
    preserved.update(_runtime_critical_modules(tech_output))
    return {path for path in preserved if path.endswith(".c")}


def _preview_paths(paths: list[str], max_items: int = 8) -> str:
    if not paths:
        return ""
    ordered = sorted(paths)
    preview = ", ".join(ordered[:max_items])
    return preview + (", ..." if len(ordered) > max_items else "")


def _has_enriched_contract(tech_output: dict | None) -> bool:
    if not isinstance(tech_output, dict):
        return False
    return isinstance(tech_output.get("integration_blueprint"), dict) or isinstance(
        tech_output.get("module_contracts"), list
    )


def _collect_raw_src_files(payload: dict) -> list[str]:
    raw_files = payload.get("files")
    if not isinstance(raw_files, dict):
        return []

    result: list[str] = []
    for path in raw_files.keys():
        if not isinstance(path, str):
            continue
        normalized = _normalize_src_path(path)
        if normalized:
            result.append(normalized)
    return sorted(set(result))


def _extract_scaffold_allowed_files(tech_output: dict | None) -> set[str]:
    scaffold = _as_dict(_as_dict(tech_output).get("scaffold"))
    return {
        normalized
        for path in _as_list(scaffold.get("allowed_files"))
        for normalized in [_normalize_src_path(path)]
        if normalized
    }


def _extract_contract_owned_files(tech_output: dict | None) -> set[str]:
    payload = _as_dict(tech_output)
    owned: set[str] = set()

    integration_blueprint = _as_dict(payload.get("integration_blueprint"))
    owned.update(_as_list(integration_blueprint.get("owned_files")))
    owned.update(_as_list(integration_blueprint.get("planned_files")))
    owned.update(_as_list(integration_blueprint.get("integrated_modules")))

    raw_contract_files = integration_blueprint.get("files")
    if isinstance(raw_contract_files, dict):
        owned.update(str(path).strip() for path in raw_contract_files.keys())

    raw_module_contracts = payload.get("module_contracts")
    if isinstance(raw_module_contracts, list):
        for item in raw_module_contracts:
            data = _as_dict(item)
            owned.update(_as_list(data.get("owned_files")))
            owned.add(str(data.get("module", "")).strip())
            owned.add(str(data.get("header", "")).strip())

    normalized_owned = {
        normalized
        for path in owned
        for normalized in [_normalize_src_path(path)]
        if normalized and normalized != "src/scene_game.c"
    }

    return normalized_owned


def _extract_asset_file_map(tech_output: dict | None) -> dict[str, list[str]]:
    payload = _as_dict(tech_output)
    blueprint = _as_dict(payload.get("integration_blueprint"))
    raw_map = blueprint.get("asset_file_map")
    if not isinstance(raw_map, dict):
        return {}

    mapping: dict[str, list[str]] = {}
    for asset_name, files in raw_map.items():
        token = _asset_token(str(asset_name))
        if not token:
            continue
        normalized_files = [
            normalized
            for path in _as_list(files)
            for normalized in [_normalize_src_path(path)]
            if normalized
        ]
        if normalized_files:
            mapping[token] = sorted(set(normalized_files))

    return mapping


def _required_assets_for_integration(tech_output: dict | None) -> list[str]:
    payload = _as_dict(tech_output)
    runtime = _as_dict(payload.get("runtime_contract"))
    raw_module_contracts = payload.get("module_contracts")

    tracked_modules = set(_as_list(runtime.get("integrated_modules")))
    tracked_modules.update(_as_list(runtime.get("critical_modules")))

    required_assets: list[str] = []
    asset_contract = _as_dict(payload.get("asset_contract"))
    required_assets.extend(_as_list(asset_contract.get("required_assets")))

    if isinstance(raw_module_contracts, list):
        for item in raw_module_contracts:
            data = _as_dict(item)
            module_path = _normalize_src_path(str(data.get("module", "")))
            if not module_path:
                continue

            if data.get("integrated", True) or data.get("critical", False):
                tracked_modules.add(module_path)

        for item in raw_module_contracts:
            data = _as_dict(item)
            module_path = _normalize_src_path(str(data.get("module", "")))
            if module_path and module_path in tracked_modules:
                required_assets.extend(_as_list(data.get("required_assets")))

    cleaned: list[str] = []
    for asset in required_assets:
        token = _asset_token(asset)
        if token:
            cleaned.append(token)
    return list(dict.fromkeys(cleaned))


def ensure_required_asset_files(
    files: dict[str, str],
    tech_output: dict | None,
    allowed_files: set[str],
) -> dict[str, str]:
    normalized = dict(files)
    asset_file_map = _extract_asset_file_map(tech_output)
    required_assets = _required_assets_for_integration(tech_output)

    for asset in required_assets:
        for path in asset_file_map.get(asset, []):
            if not _is_allowed(path, allowed_files):
                continue

            if path.endswith(".c"):
                header_path = str(PurePosixPath(path).with_suffix(".h"))
                if _is_allowed(header_path, allowed_files) and header_path not in normalized:
                    normalized[header_path] = _build_asset_header_stub(header_path, asset)

            if path in normalized:
                continue

            if path.endswith(".h"):
                normalized[path] = _build_asset_header_stub(path, asset)
            elif path.endswith(".c"):
                header_path = str(PurePosixPath(path).with_suffix(".h"))
                normalized[path] = _build_asset_source_stub(path, header_path, asset)

    return normalized


def normalize_files_payload(payload: dict, allowed_files: set[str]) -> dict[str, str]:
    raw_files = payload.get("files")
    if not isinstance(raw_files, dict):
        return {}

    normalized: dict[str, str] = {}
    for path, content in raw_files.items():
        if not isinstance(path, str):
            continue
        rel_path = _normalize_src_path(path)
        if not rel_path:
            continue
        if allowed_files and rel_path not in allowed_files:
            continue
        normalized[rel_path] = str(content)

    return normalized


def _normalize_files(payload: dict, allowed_files: set[str]) -> dict[str, str]:
    # Backward-compatible alias.
    return normalize_files_payload(payload, allowed_files)


def _is_allowed(path: str, allowed_files: set[str]) -> bool:
    return not allowed_files or path in allowed_files


def ensure_core_game_module(
    files: dict[str, str],
    allowed_files: set[str],
    tech_output: dict | None = None,
    art_output: dict | None = None,
) -> dict[str, str]:
    normalized = dict(files)
    mode = _resolve_video_mode(tech_output)
    palette_hw = _resolve_palette_hw(art_output, mode)

    def _ensure(path: str, content: str) -> None:
        if path in normalized and str(normalized.get(path, "")).strip():
            return
        normalized[path] = content

    if _is_allowed(GAME_H_PATH, allowed_files):
        _ensure(GAME_H_PATH, _build_game_h_stub())

    if _is_allowed(GAME_C_PATH, allowed_files):
        _ensure(GAME_C_PATH, _build_game_c_stub(mode))

    if _is_allowed(MAIN_C_PATH, allowed_files):
        _ensure(MAIN_C_PATH, _build_main_c_stub())

    if _is_allowed(PLAYER_H_PATH, allowed_files):
        _ensure(PLAYER_H_PATH, _build_player_h_stub())

    if _is_allowed(PLAYER_C_PATH, allowed_files):
        _ensure(PLAYER_C_PATH, _build_player_c_stub(mode))

    # Ensure gameplay dependencies exist, but preserve generated implementations.
    _ensure(ENEMY_H_PATH, _build_enemy_h_stub())
    _ensure(ENEMY_C_PATH, _build_enemy_c_stub(mode))
    _ensure(PROJECTILE_H_PATH, _build_projectile_h_stub())
    _ensure(PROJECTILE_C_PATH, _build_projectile_c_stub(mode))

    if _is_allowed(LEVEL1_H_PATH, allowed_files):
        _ensure(LEVEL1_H_PATH, _build_level1_h_stub(mode))

    if _is_allowed(LEVEL1_C_PATH, allowed_files):
        _ensure(LEVEL1_C_PATH, _build_level1_c_stub(mode, palette_hw))

    if _is_allowed(TILESET_BASE_H_PATH, allowed_files):
        _ensure(TILESET_BASE_H_PATH, _build_fixed_asset_header(TILESET_BASE_H_PATH, "tilesetbase_data"))

    if _is_allowed(TILESET_BASE_C_PATH, allowed_files):
        _ensure(TILESET_BASE_C_PATH, _build_fixed_asset_source("data/tileset/base.h", "tilesetbase_data"))

    if _is_allowed(PLAYERKNIGHT_H_PATH, allowed_files):
        _ensure(PLAYERKNIGHT_H_PATH, _build_fixed_asset_header(PLAYERKNIGHT_H_PATH, "sprplayerknight_data"))

    if _is_allowed(PLAYERKNIGHT_C_PATH, allowed_files):
        _ensure(
            PLAYERKNIGHT_C_PATH,
            _build_fixed_asset_source("data/sprites/playerknight.h", "sprplayerknight_data"),
        )

    if _is_allowed(HEALTHBAR_H_PATH, allowed_files):
        _ensure(HEALTHBAR_H_PATH, _build_fixed_asset_header(HEALTHBAR_H_PATH, "hudhealthbar_data"))

    if _is_allowed(HEALTHBAR_C_PATH, allowed_files):
        _ensure(HEALTHBAR_C_PATH, _build_fixed_asset_source("data/hud/healthbar.h", "hudhealthbar_data"))

    if _is_allowed(HUD_H_PATH, allowed_files):
        _ensure(HUD_H_PATH, _build_hud_h_stub())

    if _is_allowed(HUD_C_PATH, allowed_files):
        _ensure(HUD_C_PATH, _build_hud_c_stub(mode))

    if _is_allowed(INPUT_H_PATH, allowed_files):
        _ensure(INPUT_H_PATH, _build_input_h_stub())

    if _is_allowed(INPUT_C_PATH, allowed_files):
        _ensure(INPUT_C_PATH, _build_input_c_stub())

    if _is_allowed(COLLISION_H_PATH, allowed_files):
        _ensure(COLLISION_H_PATH, _build_collision_h_stub())

    if _is_allowed(COLLISION_C_PATH, allowed_files):
        _ensure(COLLISION_C_PATH, _build_collision_c_stub())

    if _is_allowed(TILEMAP_H_PATH, allowed_files):
        _ensure(TILEMAP_H_PATH, _build_tilemap_h_stub())

    if _is_allowed(TILEMAP_C_PATH, allowed_files):
        _ensure(TILEMAP_C_PATH, _build_tilemap_c_stub(mode))

    # scene_game is no longer the central game loop module.
    normalized.pop("src/scene_game.c", None)

    return normalized


def _ensure_core_game_module(
    files: dict[str, str],
    allowed_files: set[str],
    tech_output: dict | None = None,
    art_output: dict | None = None,
) -> dict[str, str]:
    # Backward-compatible alias.
    return ensure_core_game_module(files, allowed_files, tech_output, art_output)


def _enforce_compile_safe_c_files(
    files: dict[str, str],
    allowed_files: set[str],
    tech_output: dict | None,
) -> tuple[dict[str, str], list[str]]:
    compile_profile = _runtime_compile_profile(tech_output)
    if compile_profile in PLAYABLE_RUNTIME_PROFILES:
        # In playable/vertical slices we keep runtime gameplay modules instead of
        # collapsing to a compile-only core slice.
        return dict(files), []

    compile_safe_c = {
        MAIN_C_PATH,
        GAME_C_PATH,
        LEVEL1_C_PATH,
        TILESET_BASE_C_PATH,
        PLAYERKNIGHT_C_PATH,
        HEALTHBAR_C_PATH,
    }
    compile_safe_c.update(_runtime_modules_to_preserve(tech_output))

    if _is_allowed(HUD_C_PATH, allowed_files):
        compile_safe_c.add(HUD_C_PATH)

    normalized = dict(files)
    dropped: list[str] = []

    for path in sorted(list(normalized.keys())):
        if not path.endswith(".c"):
            continue
        if path in compile_safe_c:
            continue
        dropped.append(path)
        normalized.pop(path, None)

    return normalized, dropped


def _extract_issue_paths(issues: list[str]) -> list[str]:
    paths: set[str] = set()
    for issue in issues:
        candidate = str(issue).split(":", 1)[0].strip()
        normalized = _normalize_src_path(candidate)
        if normalized:
            paths.add(normalized)
        # For signature mismatch issues ("between X.h and X.c"), also repair the .h
        between_match = re.search(r"between\s+(\S+\.h)\s+and\s+(\S+\.c)\b", str(issue))
        if between_match:
            for p in (between_match.group(1), between_match.group(2)):
                norm = _normalize_src_path(p)
                if norm:
                    paths.add(norm)
    return sorted(paths)


def _build_generic_header_stub(path: str) -> str:
    guard = _header_guard(path)
    return "\n".join(
        [
            f"#ifndef {guard}",
            f"#define {guard}",
            "",
            render_c_include("<cpctelera.h>"),
            "",
            "#endif",
            "",
        ]
    )


def _build_generic_source_stub(path: str, files: dict[str, str]) -> str:
    header_path = str(PurePosixPath(path).with_suffix(".h"))
    lines = []
    if header_path in files:
        lines.append(render_c_include(header_path))
    else:
        lines.append(render_c_include("<cpctelera.h>"))
    lines.extend(["", f"/* compile-safe fallback stub for {PurePosixPath(path).name} */", ""])
    return "\n".join(lines)


def _fallback_stub_for_path(
    path: str,
    files: dict[str, str],
    mode: int = 1,
    palette_hw: list[int] | None = None,
) -> str:
    stub_builders: dict[str, callable] = {
        MAIN_C_PATH: _build_main_c_stub,
        GAME_H_PATH: _build_game_h_stub,
        GAME_C_PATH: lambda: _build_game_c_stub(mode),
        PLAYER_H_PATH: _build_player_h_stub,
        PLAYER_C_PATH: lambda: _build_player_c_stub(mode),
        ENEMY_H_PATH: _build_enemy_h_stub,
        ENEMY_C_PATH: lambda: _build_enemy_c_stub(mode),
        PROJECTILE_H_PATH: _build_projectile_h_stub,
        PROJECTILE_C_PATH: lambda: _build_projectile_c_stub(mode),
        INPUT_H_PATH: _build_input_h_stub,
        INPUT_C_PATH: _build_input_c_stub,
        COLLISION_H_PATH: _build_collision_h_stub,
        COLLISION_C_PATH: _build_collision_c_stub,
        TILEMAP_H_PATH: _build_tilemap_h_stub,
        TILEMAP_C_PATH: lambda: _build_tilemap_c_stub(mode),
        LEVEL1_H_PATH: lambda: _build_level1_h_stub(mode),
        LEVEL1_C_PATH: lambda: _build_level1_c_stub(mode, palette_hw),
        TILESET_BASE_H_PATH: lambda: _build_fixed_asset_header(TILESET_BASE_H_PATH, "tilesetbase_data"),
        TILESET_BASE_C_PATH: lambda: _build_fixed_asset_source("data/tileset/base.h", "tilesetbase_data"),
        PLAYERKNIGHT_H_PATH: lambda: _build_fixed_asset_header(PLAYERKNIGHT_H_PATH, "sprplayerknight_data"),
        PLAYERKNIGHT_C_PATH: lambda: _build_fixed_asset_source("data/sprites/playerknight.h", "sprplayerknight_data"),
        HEALTHBAR_H_PATH: lambda: _build_fixed_asset_header(HEALTHBAR_H_PATH, "hudhealthbar_data"),
        HEALTHBAR_C_PATH: lambda: _build_fixed_asset_source("data/hud/healthbar.h", "hudhealthbar_data"),
        HUD_H_PATH: _build_hud_h_stub,
        HUD_C_PATH: _build_hud_c_stub,
    }

    builder = stub_builders.get(path)
    if builder:
        return builder()

    if path.endswith(".h"):
        return _build_generic_header_stub(path)
    if path.endswith(".c"):
        return _build_generic_source_stub(path, files)
    return ""


def _repair_invalid_generated_files(
    files: dict[str, str],
    allowed_files: set[str],
    tech_output: dict | None = None,
    art_output: dict | None = None,
) -> tuple[dict[str, str], list[str], list[str]]:
    repaired = dict(files)
    repaired_paths: list[str] = []
    remaining_issues = detect_c_generation_issues(repaired)
    mode = _resolve_video_mode(tech_output)
    palette_hw = _resolve_palette_hw(art_output, mode)

    for _ in range(2):
        if not remaining_issues:
            break

        issue_paths = _extract_issue_paths(remaining_issues)
        changed = False

        for path in issue_paths:
            if not _is_allowed(path, allowed_files):
                continue

            replacement = _fallback_stub_for_path(path, repaired, mode, palette_hw)
            if not replacement:
                continue

            if repaired.get(path) == replacement:
                continue

            repaired[path] = replacement
            repaired_paths.append(path)
            changed = True

        if not changed:
            break

        remaining_issues = detect_c_generation_issues(repaired)

    return repaired, sorted(set(repaired_paths)), remaining_issues


def run(
    user_request: str,
    orchestrator_output: dict | None = None,
    narrative_output: dict | None = None,
    design_output: dict | None = None,
    art_output: dict | None = None,
    tech_output: dict | None = None,
) -> dict:
    _ci_t0 = _time.time()
    print("[INFO] [code_integrator] construyendo contexto RAG...", file=sys.stderr)

    payload = json_call(
        "code_integrator",
        user_request,
        build_agent_extra_context(
            "code_integrator_agent",
            user_request,
            upstream_payloads={
                "orchestrator": orchestrator_output or {},
                "narrative": narrative_output or {},
                "design": design_output or {},
                "art": art_output or {},
                "tech": tech_output or {},
            },
            retrieval_limit=6,
        ),
    )
    print(f"[INFO] [code_integrator] LLM respondió en {_time.time() - _ci_t0:.1f}s; normalizando ficheros...", file=sys.stderr)
    assumptions = _as_list(payload.get("assumptions"))
    manual_followups = _as_list(payload.get("manual_followups"))

    contract_mode = _has_enriched_contract(tech_output)
    scaffold_allowed_files = _extract_scaffold_allowed_files(tech_output)
    contract_owned_files = _extract_contract_owned_files(tech_output) if contract_mode else set()

    if contract_mode and contract_owned_files:
        allowed_files = set(contract_owned_files)
        if scaffold_allowed_files:
            allowed_files = allowed_files.intersection(scaffold_allowed_files)
    else:
        allowed_files = set(scaffold_allowed_files)

    raw_src_files = _collect_raw_src_files(payload)
    compile_profile = _runtime_compile_profile(tech_output)
    print(f"[INFO] [code_integrator] perfil={compile_profile} allowed={len(allowed_files)} raw_src={len(raw_src_files)}", file=sys.stderr)

    files = normalize_files_payload(payload, allowed_files)
    files_before_core = dict(files)
    files = ensure_core_game_module(files, allowed_files, tech_output, art_output)
    files = ensure_required_asset_files(files, tech_output, allowed_files)
    files, sanitized_integer_aliases = _sanitize_integer_aliases(files, allowed_files)
    files, sanitized_c89_for = _sanitize_c89_for_loops(files, allowed_files)
    files, sanitized_asset_headers = _sanitize_asset_headers(files, allowed_files)
    files, sanitized_game_sources = _sanitize_game_source_files(files, allowed_files, tech_output)
    files, sanitized_enemy_sources = _sanitize_enemy_source_files(files, allowed_files)
    files, sanitized_player_sources = _sanitize_player_source_files(files, allowed_files, tech_output)
    files, sanitized_projectile_sources = _sanitize_projectile_source_files(files, allowed_files)
    files, sanitized_input_sources = _sanitize_input_source_files(files, allowed_files)
    files, sanitized_hud_sources = _sanitize_hud_source_files(files, allowed_files, tech_output)
    files, sanitized_tilemap_sources = _sanitize_tilemap_source_files(files, allowed_files, tech_output)
    files, sanitized_entity_render_sources = _sanitize_entity_render_source_files(files, allowed_files, tech_output)
    files, sanitized_main_sources = _sanitize_main_source_files(files, allowed_files)
    files, dropped_unsafe_c = _enforce_compile_safe_c_files(files, allowed_files, tech_output)
    files, repaired_invalid_files, prebuild_validation_errors = _repair_invalid_generated_files(files, allowed_files, tech_output, art_output)

    if not files:
        if contract_mode and contract_owned_files:
            expected_preview = _preview_paths(sorted(contract_owned_files))
            notes = [
                "CodeIntegratorAgent returned no valid contract-owned files. "
                f"Expected owned files: {expected_preview}."
            ]
        elif contract_mode:
            notes = [
                "CodeIntegratorAgent returned no valid files. "
                "Contract metadata exists but owned_files are missing; scaffold fallback also produced no files."
            ]
        else:
            notes = ["CodeIntegratorAgent returned no valid scaffold files."]

        return {
            "files": {},
            "assumptions": assumptions,
            "integration_notes": notes,
            "manual_followups": manual_followups,
            "prebuild_validation_errors": [],
        }

    notes_parts: list[str] = []
    if contract_mode:
        notes_parts.append(
            f"Contract mode enabled. Accepted {len(files_before_core)} of {len(raw_src_files)} generated files."
        )

        if contract_owned_files:
            outside_contract = sorted(path for path in raw_src_files if path not in contract_owned_files)
            if outside_contract:
                notes_parts.append(
                    "Rejected "
                    f"{len(outside_contract)} files outside owned contract files: "
                    f"{_preview_paths(outside_contract)}."
                )

            expected_contract_files = sorted(
                path for path in contract_owned_files if path.endswith(".c") or path.endswith(".h")
            )
            missing_expected = sorted(path for path in expected_contract_files if path not in files)
            if missing_expected:
                notes_parts.append(
                    "Missing "
                    f"{len(missing_expected)} expected contract files: "
                    f"{_preview_paths(missing_expected)}."
                )
        else:
            notes_parts.append(
                "Contract metadata exists but owned_files are empty; fallback to scaffold.allowed_files was used."
            )

        injected = len(files) - len(files_before_core)
        if injected > 0:
            notes_parts.append(
                f"Injected {injected} core files allowed by contract/scaffold policy."
            )

        if dropped_unsafe_c:
            notes_parts.append(
                "Omitted "
                f"{len(dropped_unsafe_c)} non-core C file(s) to keep compile-only slice stable: "
                f"{_preview_paths(dropped_unsafe_c)}."
            )
            if compile_profile in PLAYABLE_RUNTIME_PROFILES:
                notes_parts.append(
                    "Runtime compile profile is playable/vertical, so C-file pruning was skipped."
                )
    else:
        notes_parts.append(f"Generated {len(files)} valid source files.")

    if repaired_invalid_files:
        notes_parts.append(
            "Repaired "
            f"{len(repaired_invalid_files)} file(s) with deterministic compile-safe stubs: "
            f"{_preview_paths(repaired_invalid_files)}."
        )

    if sanitized_asset_headers:
        notes_parts.append(
            "Sanitized "
            f"{len(sanitized_asset_headers)} asset header(s) to data-only declarations: "
            f"{_preview_paths(sanitized_asset_headers)}."
        )

    if sanitized_integer_aliases:
        notes_parts.append(
            "Sanitized "
            f"{len(sanitized_integer_aliases)} source/header file(s) to normalize SDCC integer aliases: "
            f"{_preview_paths(sanitized_integer_aliases)}."
        )

    if sanitized_enemy_sources:
        notes_parts.append(
            "Sanitized "
            f"{len(sanitized_enemy_sources)} enemy source file(s) to remove invalid type coupling: "
            f"{_preview_paths(sanitized_enemy_sources)}."
        )

    if sanitized_player_sources:
        notes_parts.append(
            "Sanitized "
            f"{len(sanitized_player_sources)} player source file(s) to enforce C89-safe movement/collision logic: "
            f"{_preview_paths(sanitized_player_sources)}."
        )

    if sanitized_game_sources:
        notes_parts.append(
            "Sanitized "
            f"{len(sanitized_game_sources)} game source file(s) for runtime mode compatibility: "
            f"{_preview_paths(sanitized_game_sources)}."
        )

    if sanitized_input_sources:
        notes_parts.append(
            "Sanitized "
            f"{len(sanitized_input_sources)} input source file(s) to force hardware keyboard polling: "
            f"{_preview_paths(sanitized_input_sources)}."
        )

    if sanitized_hud_sources:
        notes_parts.append(
            "Sanitized "
            f"{len(sanitized_hud_sources)} HUD source file(s) for SDCC/CPC text rendering compatibility: "
            f"{_preview_paths(sanitized_hud_sources)}."
        )

    if sanitized_tilemap_sources:
        notes_parts.append(
            "Sanitized "
            f"{len(sanitized_tilemap_sources)} tilemap file(s) due to byte-unit rendering mismatch "
            f"in cpct_getScreenPtr/cpct_drawSolidBox: {_preview_paths(sanitized_tilemap_sources)}."
        )

    if sanitized_entity_render_sources:
        notes_parts.append(
            "Sanitized "
            f"{len(sanitized_entity_render_sources)} entity render file(s) to replace raw fill-byte literals "
            f"with mode-aware CPCtelera expressions: {_preview_paths(sanitized_entity_render_sources)}."
        )

    if sanitized_main_sources:
        notes_parts.append(
            "Sanitized "
            f"{len(sanitized_main_sources)} main source file(s) to avoid unresolved cpc_run_address entrypoint symbols: "
            f"{_preview_paths(sanitized_main_sources)}."
        )

    if prebuild_validation_errors:
        preview = " | ".join(prebuild_validation_errors[:3])
        notes_parts.append(
            "Pre-build C validation failed with "
            f"{len(prebuild_validation_errors)} issue(s): {preview}"
            f"{' | ...' if len(prebuild_validation_errors) > 3 else ''}."
        )

    integration_notes = [part for part in notes_parts if part]

    return {
        "files": files,
        "assumptions": assumptions,
        "integration_notes": integration_notes,
        "manual_followups": manual_followups,
        "prebuild_validation_errors": prebuild_validation_errors,
    }
