import json
import re
from pathlib import PurePosixPath

from app.services.c_codegen_service import (
    detect_c_generation_issues,
    render_c_array_decl,
    render_c_const_array,
    render_c_function_decl,
    render_c_function_def,
    render_c_include,
    render_c_struct,
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
PROJECTILE_H_PATH = "src/entities/projectile.h"
LEVEL1_H_PATH = "src/data/level1.h"
LEVEL1_C_PATH = "src/data/level1.c"
TILESET_BASE_H_PATH = "src/data/tileset/base.h"
TILESET_BASE_C_PATH = "src/data/tileset/base.c"
PLAYERKNIGHT_H_PATH = "src/data/sprites/playerknight.h"
PLAYERKNIGHT_C_PATH = "src/data/sprites/playerknight.c"
HEALTHBAR_H_PATH = "src/data/hud/healthbar.h"
HEALTHBAR_C_PATH = "src/data/hud/healthbar.c"


def _build_game_h_stub() -> str:
    return "\n".join(
        [
            "#ifndef GAME_H",
            "#define GAME_H",
            "",
            "void gameinit(void);",
            "void gameupdate(void);",
            "void gamerender(void);",
            "",
            "#endif",
            "",
        ]
    )


def _build_game_c_stub() -> str:
    return "\n".join(
        [
            render_c_include("game.h"),
            render_c_include("<cpctelera.h>"),
            "",
            "void gameinit(void) {",
            "    cpct_disableFirmware();",
            "    cpct_setVideoMode(0);",
            "    cpct_setBorder(HW_BLACK);",
            "}",
            "",
            "void gameupdate(void) {",
            "}",
            "",
            "void gamerender(void) {",
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
            "int main(void) {",
            "    gameinit();",
            "    while (1) {",
            "        gameupdate();",
            "        gamerender();",
            "        cpct_waitVSYNC();",
            "    }",
            "    return 0;",
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
            "typedef struct {",
            "    u8 x;",
            "    u8 y;",
            "    i8 vx;",
            "    i8 vy;",
            "    u8 w;",
            "    u8 h;",
            "} Player;",
            "",
            "void playerinit(Player* player);",
            "void playerupdate(Player* player);",
            "void playerrender(const Player* player);",
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
            "} Enemy;",
            "",
            "void enemyinit(Enemy* enemy);",
            "void enemyupdate(Enemy* enemy);",
            "void enemyrender(const Enemy* enemy);",
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
            "} Projectile;",
            "",
            "void projectileinit(Projectile* projectile);",
            "void projectileupdate(Projectile* projectile);",
            "void projectilerender(const Projectile* projectile);",
            "",
            "#endif",
            "",
        ]
    )


def _build_level1_h_stub() -> str:
    return "\n".join(
        [
            "#ifndef DATA_LEVEL1_H",
            "#define DATA_LEVEL1_H",
            "",
            render_c_include("<cpctelera.h>"),
            "",
            "extern const u8 level1tilemap[];",
            "extern const u8 level1tileproperties[];",
            "extern const u8 gpalette16[16];",
            "extern const u16 level1tilemapwidth;",
            "extern const u16 level1tilemapheight;",
            "",
            "#endif",
            "",
        ]
    )


def _build_level1_c_stub() -> str:
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
            "const u8 gpalette16[16] = {",
            "    0x54, 0x44, 0x55, 0x5C,",
            "    0x58, 0x5D, 0x4C, 0x45,",
            "    0x4D, 0x56, 0x46, 0x57,",
            "    0x5E, 0x40, 0x5F, 0x4E",
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
    return "\n".join(
        [
            render_c_include(header_path),
            "",
            f"const u8 {symbol}[] = {{ 0x00 }};",
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
                [("u8", "health"), ("u16", "score"), ("u8", "time"), ("u8", "lives")],
            ),
            render_c_function_decl("void", "hudrender", []),
            "",
            "#endif",
            "",
        ]
    )


def _build_hud_c_stub() -> str:
    return "\n".join(
        [
            '#include "systems/hud.h"',
            '#include "data/hud/elements.h"   /* Si tu arbol usa otro nombre, ajusta solo este include */',
            "",
            "static u8  currenthealth;",
            "static u16 currentscore;",
            "static u8  currenttime;",
            "static u8  currentlives;",
            "",
            "/* Fallback compile-clean sprites while real HUD assets are wired. */",
            "static const u8 _hud_dummy_sprite[64] = {0};",
            "static const u8* hudnumbers[10] = {",
            "    _hud_dummy_sprite, _hud_dummy_sprite, _hud_dummy_sprite, _hud_dummy_sprite, _hud_dummy_sprite,",
            "    _hud_dummy_sprite, _hud_dummy_sprite, _hud_dummy_sprite, _hud_dummy_sprite, _hud_dummy_sprite",
            "};",
            "static const u8 hudhealth[64] = {0};",
            "static const u8 hudlives[64] = {0};",
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
            "        pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 8), y);",
            "        cpct_drawSprite((u8*)hudnumbers[digit], pvmem, 8, 8);",
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
            "}",
            "",
            "void hudupdate(u8 health, u16 score, u8 time, u8 lives) {",
            "    currenthealth = health;",
            "    currentscore  = score;",
            "    currenttime   = time;",
            "    currentlives  = lives;",
            "}",
            "",
            "void hudrender(void) {",
            "    u8 i;",
            "    u8* pvmem;",
            "    u16 scoretemp;",
            "    u8 timetemp;",
            "",
            "    for (i = 0; i < currenthealth; ++i) {",
            "        pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2 + (i * 8), 2);",
            "        cpct_drawSprite((u8*)hudhealth, pvmem, 8, 8);",
            "    }",
            "",
            "    scoretemp = currentscore;",
            "    hud_draw_digits(scoretemp, 5, 88, 2);",
            "",
            "    timetemp = currenttime;",
            "    hud_draw_digits((u16)timetemp, 3, 56, 2);",
            "",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);",
            "    cpct_drawSprite((u8*)hudlives, pvmem, 8, 8);",
            "",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);",
            "    cpct_drawSprite((u8*)hudnumbers[currentlives % 10], pvmem, 8, 8);",
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


def _entity_struct_block() -> str:
    return "\n\n".join(
        [
            render_c_struct("Player", [("u8", "x"), ("u8", "y"), ("u8", "health")]),
            render_c_struct("Enemy", [("u8", "x"), ("u8", "y"), ("u8", "health")]),
            render_c_struct("Projectile", [("u8", "x"), ("u8", "y"), ("u8", "speed")]),
        ]
    )


def _build_asset_header_stub(path: str, asset_name: str) -> str:
    guard = _header_guard(path)
    symbol = _asset_symbol_name(asset_name, path)

    lines = [
        f"#ifndef {guard}",
        f"#define {guard}",
        "",
        render_c_include("<cpctelera.h>"),
        "",
    ]

    if any(tag in _asset_token(asset_name) for tag in ("player", "enemy", "projectile")):
        lines.extend([_entity_struct_block(), ""])

    lines.extend(
        [
            render_c_array_decl("u8", symbol, None, qualifiers=["extern", "const"]),
            "",
            "#endif",
            "",
        ]
    )

    return "\n".join(lines)


def _build_asset_source_stub(path: str, header_path: str, asset_name: str) -> str:
    symbol = _asset_symbol_name(asset_name, path)

    if "level1tileproperties" in _asset_token(asset_name):
        array_decl = render_c_const_array("u8", "level1tileproperties", ["0x00", "0x01", "0x01", "0x00"])
    else:
        array_decl = render_c_const_array("u8", symbol, ["0x00"])

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


def _normalize_src_path(path: str) -> str:
    candidate = str(path).strip().replace("\\", "/")
    if not candidate:
        return ""
    if candidate.startswith("./"):
        candidate = candidate[2:]
    if not candidate.startswith("src/"):
        return ""
    return PurePosixPath(candidate).as_posix()


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


def ensure_core_game_module(files: dict[str, str], allowed_files: set[str]) -> dict[str, str]:
    normalized = dict(files)

    if _is_allowed(GAME_H_PATH, allowed_files):
        normalized[GAME_H_PATH] = _build_game_h_stub()

    if _is_allowed(GAME_C_PATH, allowed_files):
        normalized[GAME_C_PATH] = _build_game_c_stub()

    if _is_allowed(MAIN_C_PATH, allowed_files):
        normalized[MAIN_C_PATH] = _build_main_c_stub()

    if _is_allowed(PLAYER_H_PATH, allowed_files):
        normalized[PLAYER_H_PATH] = _build_player_h_stub()

    if _is_allowed(ENEMY_H_PATH, allowed_files):
        normalized[ENEMY_H_PATH] = _build_enemy_h_stub()

    if _is_allowed(PROJECTILE_H_PATH, allowed_files):
        normalized[PROJECTILE_H_PATH] = _build_projectile_h_stub()

    if _is_allowed(LEVEL1_H_PATH, allowed_files):
        normalized[LEVEL1_H_PATH] = _build_level1_h_stub()

    if _is_allowed(LEVEL1_C_PATH, allowed_files):
        normalized[LEVEL1_C_PATH] = _build_level1_c_stub()

    if _is_allowed(TILESET_BASE_H_PATH, allowed_files):
        normalized[TILESET_BASE_H_PATH] = _build_fixed_asset_header(TILESET_BASE_H_PATH, "tilesetbase_data")

    if _is_allowed(TILESET_BASE_C_PATH, allowed_files):
        normalized[TILESET_BASE_C_PATH] = _build_fixed_asset_source("data/tileset/base.h", "tilesetbase_data")

    if _is_allowed(PLAYERKNIGHT_H_PATH, allowed_files):
        normalized[PLAYERKNIGHT_H_PATH] = _build_fixed_asset_header(PLAYERKNIGHT_H_PATH, "sprplayerknight_data")

    if _is_allowed(PLAYERKNIGHT_C_PATH, allowed_files):
        normalized[PLAYERKNIGHT_C_PATH] = _build_fixed_asset_source(
            "data/sprites/playerknight.h", "sprplayerknight_data"
        )

    if _is_allowed(HEALTHBAR_H_PATH, allowed_files):
        normalized[HEALTHBAR_H_PATH] = _build_fixed_asset_header(HEALTHBAR_H_PATH, "hudhealthbar_data")

    if _is_allowed(HEALTHBAR_C_PATH, allowed_files):
        normalized[HEALTHBAR_C_PATH] = _build_fixed_asset_source("data/hud/healthbar.h", "hudhealthbar_data")

    if _is_allowed(HUD_H_PATH, allowed_files):
        normalized[HUD_H_PATH] = _build_hud_h_stub()

    if _is_allowed(HUD_C_PATH, allowed_files):
        normalized[HUD_C_PATH] = _build_hud_c_stub()

    # scene_game is no longer the central game loop module.
    normalized.pop("src/scene_game.c", None)

    return normalized


def _ensure_core_game_module(files: dict[str, str], allowed_files: set[str]) -> dict[str, str]:
    # Backward-compatible alias.
    return ensure_core_game_module(files, allowed_files)


def _enforce_compile_safe_c_files(files: dict[str, str], allowed_files: set[str]) -> tuple[dict[str, str], list[str]]:
    compile_safe_c = {
        MAIN_C_PATH,
        GAME_C_PATH,
        LEVEL1_C_PATH,
        TILESET_BASE_C_PATH,
        PLAYERKNIGHT_C_PATH,
        HEALTHBAR_C_PATH,
    }
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


def run(
    user_request: str,
    orchestrator_output: dict | None = None,
    narrative_output: dict | None = None,
    design_output: dict | None = None,
    art_output: dict | None = None,
    tech_output: dict | None = None,
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
    if tech_output:
        blocks.append("Tech JSON:\n" + json.dumps(tech_output, ensure_ascii=False, indent=2))

    payload = json_call("code_integrator", user_request, "\n\n".join(blocks))

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

    files = normalize_files_payload(payload, allowed_files)
    files_before_core = dict(files)
    files = ensure_core_game_module(files, allowed_files)
    files = ensure_required_asset_files(files, tech_output, allowed_files)
    files, dropped_unsafe_c = _enforce_compile_safe_c_files(files, allowed_files)

    if not files:
        if contract_mode and contract_owned_files:
            expected_preview = _preview_paths(sorted(contract_owned_files))
            notes = (
                "CodeIntegratorAgent returned no valid contract-owned files. "
                f"Expected owned files: {expected_preview}."
            )
        elif contract_mode:
            notes = (
                "CodeIntegratorAgent returned no valid files. "
                "Contract metadata exists but owned_files are missing; scaffold fallback also produced no files."
            )
        else:
            notes = "CodeIntegratorAgent returned no valid scaffold files."

        return {
            "files": {},
            "integration_notes": notes,
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
    else:
        notes_parts.append(f"Generated {len(files)} valid source files.")

    prebuild_validation_errors = detect_c_generation_issues(files)
    if prebuild_validation_errors:
        preview = " | ".join(prebuild_validation_errors[:3])
        notes_parts.append(
            "Pre-build C validation failed with "
            f"{len(prebuild_validation_errors)} issue(s): {preview}"
            f"{' | ...' if len(prebuild_validation_errors) > 3 else ''}."
        )

    integration_notes = " ".join(part for part in notes_parts if part).strip()

    return {
        "files": files,
        "integration_notes": integration_notes,
        "prebuild_validation_errors": prebuild_validation_errors,
    }
