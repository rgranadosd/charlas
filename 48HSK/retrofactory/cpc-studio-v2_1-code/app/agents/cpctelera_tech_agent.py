import json
from pathlib import PurePosixPath

from app.services.contract_validation_service import (
    normalize_asset_token,
    normalize_src_path_token,
    normalize_symbol_token,
)
from app.services.llm_service import json_call
from app.services.resource_service import format_resources_for_prompt

CORE_GAME_H = "src/game.h"
CORE_GAME_C = "src/game.c"
CORE_MAIN_C = "src/main.c"
LEGACY_SCENE_GAME_C = "src/scene_game.c"

RUNTIME_CRITICAL_MODULES = [
    "src/entities/player.c",
    "src/systems/input.c",
    "src/systems/collision.c",
    "src/systems/tilemap.c",
]

RUNTIME_SUPPORT_FILES = [
    "src/entities/player.h",
    "src/entities/player.c",
    "src/systems/input.h",
    "src/systems/input.c",
    "src/systems/collision.h",
    "src/systems/collision.c",
    "src/systems/tilemap.h",
    "src/systems/tilemap.c",
    "src/data/level1.h",
    "src/data/level1.c",
    "src/data/tileset/base.h",
    "src/data/tileset/base.c",
    "src/data/sprites/playerknight.h",
    "src/data/sprites/playerknight.c",
    "src/data/hud/healthbar.h",
    "src/data/hud/healthbar.c",
]

ASSET_FILE_OVERRIDES = {
    "sprplayerknight": ["src/data/sprites/playerknight.h", "src/data/sprites/playerknight.c"],
    "hudhealthbar": ["src/data/hud/healthbar.h", "src/data/hud/healthbar.c"],
    "tilesetbase": ["src/data/tileset/base.h", "src/data/tileset/base.c"],
}

SYSTEM_HEADER_TOKENS = {
    "cpctelera.h",
}


def _token_slug(value: str) -> str:
    return "".join(ch for ch in str(value).lower() if ch.isalnum())


def _as_list(value) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [str(value).strip()]


def _as_dict(value) -> dict:
    return value if isinstance(value, dict) else {}


def _as_bool(value, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value in (None, ""):
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _src_path(value: str) -> str:
    token = normalize_src_path_token(str(value))
    if token:
        return token

    candidate = str(value).strip().replace("\\", "/")
    if not candidate:
        return ""
    if candidate.startswith("./"):
        candidate = candidate[2:]
    if not candidate.startswith("src/"):
        candidate = f"src/{candidate.lstrip('/')}"

    normalized = PurePosixPath(candidate).as_posix()
    return normalize_src_path_token(normalized) or ""


def _clean_symbols(values) -> list[str]:
    cleaned: list[str] = []
    for value in _as_list(values):
        token = normalize_symbol_token(value)
        if token:
            cleaned.append(token)
    return _unique(cleaned)


def _clean_assets(values) -> list[str]:
    cleaned: list[str] = []
    for value in _as_list(values):
        token = normalize_asset_token(value)
        if token:
            cleaned.append(token)
    return _unique(cleaned)


def _clean_local_includes(values) -> list[str]:
    cleaned: list[str] = []

    for value in _as_list(values):
        token = str(value).strip()
        if not token:
            continue

        if token.startswith("#include"):
            token = token.replace("#include", "", 1).strip()

        # Local include closure should only track quote includes.
        if token.startswith("<") and token.endswith(">"):
            continue

        token = token.strip('"').strip("'").replace("\\", "/")
        if token.startswith("./"):
            token = token[2:]
        if token.startswith("src/"):
            token = token[4:]

        if not token or not token.endswith(".h"):
            continue

        normalized = PurePosixPath(token).as_posix()
        if ".." in PurePosixPath(normalized).parts:
            continue
        if normalized in SYSTEM_HEADER_TOKENS:
            continue

        cleaned.append(normalized)

    return _unique(cleaned)


def _asset_key(value: str) -> str:
    return "".join(ch for ch in str(value).lower() if ch.isalnum())


def _asset_file_paths(asset: str) -> list[str]:
    token = _asset_key(asset)
    if not token:
        return []

    if token in ASSET_FILE_OVERRIDES:
        return [path for path in (_src_path(item) for item in ASSET_FILE_OVERRIDES[token]) if path]

    stem = token
    folder = "assets"

    if stem.startswith("spr"):
        folder = "sprites"
        stem = stem[3:] or token
    elif "hud" in stem:
        folder = "hud"
        stem = stem.replace("hud", "", 1) or token
    elif "tile" in stem:
        folder = "tileset"

    return [
        _src_path(f"src/data/{folder}/{stem}.h"),
        _src_path(f"src/data/{folder}/{stem}.c"),
    ]


def _asset_alias_paths(asset: str, paths: list[str]) -> list[str]:
    # Preserve explicit separators from asset names (e.g. font_gothic)
    # when the computed file stem was compacted (e.g. fontgothic).
    asset_token = normalize_asset_token(asset) or ""
    if "_" not in asset_token:
        return []

    alias_stem_raw = "".join(ch if (ch.isalnum() or ch == "_") else "_" for ch in asset_token.lower())
    alias_stem = "_".join(part for part in alias_stem_raw.split("_") if part)
    if not alias_stem:
        return []

    alias_slug = _token_slug(alias_stem)
    aliases: list[str] = []
    for path in paths:
        suffix = PurePosixPath(path).suffix.lower()
        # Emit alias headers only. Mirroring .c files would duplicate
        # asset data definitions and break linker symbol uniqueness.
        if suffix != ".h":
            continue

        stem_slug = _token_slug(PurePosixPath(path).stem)
        if stem_slug != alias_slug:
            continue

        parent = PurePosixPath(path).parent.as_posix()
        alias_path = _src_path(f"{parent}/{alias_stem}{suffix}")
        if alias_path and alias_path != path:
            aliases.append(alias_path)

    return _unique(aliases)


def _build_asset_file_map(asset_contract: dict, module_contracts: list[dict], runtime: dict) -> dict[str, list[str]]:
    modules_by_path = {
        str(module.get("module", "")).strip(): module
        for module in module_contracts
        if str(module.get("module", "")).strip()
    }

    targeted_modules = {
        path for path in _as_list(runtime.get("critical_modules")) + _as_list(runtime.get("integrated_modules")) if path
    }
    for module in module_contracts:
        module_path = str(module.get("module", "")).strip()
        if not module_path:
            continue
        if module.get("critical") or module.get("integrated", True):
            targeted_modules.add(module_path)

    required_assets: list[str] = _as_list(asset_contract.get("required_assets"))
    for module_path in sorted(targeted_modules):
        contract = modules_by_path.get(module_path)
        if not contract:
            continue
        required_assets.extend(_as_list(contract.get("required_assets")))

    if _module_has_hint(module_contracts, "player"):
        required_assets.append("sprplayerknight")
    if _module_has_hint(module_contracts, "hud"):
        required_assets.append("hudhealthbar")
    if _module_has_hint(module_contracts, "tile"):
        required_assets.append("tilesetbase")

    result: dict[str, list[str]] = {}
    for asset in _clean_assets(required_assets):
        files = [path for path in _asset_file_paths(asset) if path]
        files = _unique(files + _asset_alias_paths(asset, files))
        if files:
            result[asset] = _unique(files)

    return result


def _ensure_asset_scaffold_entries(scaffold: dict, asset_file_map: dict[str, list[str]]) -> dict:
    updated = {
        "required_files": _as_list(scaffold.get("required_files")),
        "base_scaffold_files": _as_list(scaffold.get("base_scaffold_files")),
        "optional_files": _as_list(scaffold.get("optional_files")),
        "allowed_files": _as_list(scaffold.get("allowed_files")),
        "overwrite_files": _as_list(scaffold.get("overwrite_files")),
        "create_if_missing": _as_list(scaffold.get("create_if_missing")),
    }

    for paths in asset_file_map.values():
        for path in _as_list(paths):
            normalized = _src_path(path)
            if not normalized:
                continue
            updated["allowed_files"].append(normalized)
            updated["create_if_missing"].append(normalized)
            if normalized.endswith(".h"):
                updated["optional_files"].append(normalized)

    for key in ("required_files", "base_scaffold_files", "optional_files", "allowed_files", "overwrite_files", "create_if_missing"):
        updated[key] = _unique(path for path in (_src_path(item) for item in updated[key]) if path)

    updated["create_if_missing"] = [
        path for path in updated["create_if_missing"] if path in updated["allowed_files"]
    ]

    return updated


def _ensure_core_scaffold(scaffold: dict) -> dict:
    required_files = [_src_path(path) for path in _as_list(scaffold.get("required_files"))]
    base_scaffold_files = [_src_path(path) for path in _as_list(scaffold.get("base_scaffold_files"))]
    optional_files = [_src_path(path) for path in _as_list(scaffold.get("optional_files"))]
    allowed_files = _as_list(scaffold.get("allowed_files"))
    overwrite_files = _as_list(scaffold.get("overwrite_files"))
    create_if_missing = _as_list(scaffold.get("create_if_missing"))

    allowed_files = [_src_path(path) for path in allowed_files]
    overwrite_files = [_src_path(path) for path in overwrite_files]
    create_if_missing = [_src_path(path) for path in create_if_missing]

    # game.c is now the main loop module. Keep scene_game optional, not central.
    required_files = [path for path in required_files if path != LEGACY_SCENE_GAME_C]
    base_scaffold_files = [path for path in base_scaffold_files if path != LEGACY_SCENE_GAME_C]
    optional_files = [path for path in optional_files if path != LEGACY_SCENE_GAME_C]
    allowed_files = [path for path in allowed_files if path != LEGACY_SCENE_GAME_C]
    overwrite_files = [path for path in overwrite_files if path != LEGACY_SCENE_GAME_C]
    create_if_missing = [path for path in create_if_missing if path != LEGACY_SCENE_GAME_C]

    required_files.extend([CORE_MAIN_C, CORE_GAME_H, CORE_GAME_C])
    required_files.extend(RUNTIME_CRITICAL_MODULES)
    base_scaffold_files.append(CORE_MAIN_C)

    writable_runtime_files = [CORE_MAIN_C, CORE_GAME_H, CORE_GAME_C]
    writable_runtime_files.extend(RUNTIME_SUPPORT_FILES)

    for core_path in writable_runtime_files:
        allowed_files.append(core_path)
        overwrite_files.append(core_path)
        create_if_missing.append(core_path)

    allowed_files.extend(required_files)
    allowed_files.extend(base_scaffold_files)
    allowed_files.extend(optional_files)
    overwrite_files.append(CORE_MAIN_C)

    allowed_files = _unique(path for path in allowed_files if path)
    overwrite_files = [path for path in _unique(path for path in overwrite_files if path) if path in allowed_files]
    create_if_missing = [
        path for path in _unique(path for path in create_if_missing if path) if path in allowed_files
    ]
    required_files = [path for path in _unique(path for path in required_files if path) if path in allowed_files]
    base_scaffold_files = [
        path for path in _unique(path for path in base_scaffold_files if path) if path in allowed_files
    ]
    optional_files = [path for path in _unique(path for path in optional_files if path) if path in allowed_files]

    return {
        "required_files": required_files,
        "base_scaffold_files": base_scaffold_files,
        "optional_files": optional_files,
        "allowed_files": allowed_files,
        "overwrite_files": overwrite_files,
        "create_if_missing": create_if_missing,
    }


def _normalize_module_contracts(payload: dict, modules: list[str], scaffold: dict) -> list[dict]:
    raw_contracts = payload.get("module_contracts", [])
    known_scaffold_paths = set(_as_list(scaffold.get("required_files")))
    known_scaffold_paths.update(_as_list(scaffold.get("base_scaffold_files")))
    known_scaffold_paths.update(_as_list(scaffold.get("optional_files")))
    known_scaffold_paths.update(_as_list(scaffold.get("allowed_files")))
    known_scaffold_paths = {_src_path(path) for path in known_scaffold_paths if _src_path(path)}

    def _module_path(raw_module: str) -> str:
        normalized = _src_path(raw_module)
        if not normalized:
            return ""

        if normalized == LEGACY_SCENE_GAME_C:
            return ""

        if normalized.endswith(".h"):
            normalized = _src_path(normalized[:-2] + ".c")
        elif not normalized.endswith(".c"):
            normalized = _src_path(f"{normalized}.c")

        if normalized == LEGACY_SCENE_GAME_C:
            return ""

        return normalized

    def _header_for_module(module_path: str) -> str:
        if module_path == CORE_GAME_C:
            return CORE_GAME_H
        candidate = _src_path(module_path[:-2] + ".h") if module_path.endswith(".c") else ""
        if candidate and candidate in known_scaffold_paths:
            return candidate
        return ""

    contracts_by_module: dict[str, dict] = {}

    if isinstance(raw_contracts, list):
        for item in raw_contracts:
            data = _as_dict(item)
            module = _module_path(data.get("module", ""))
            if not module:
                continue

            header = _src_path(data.get("header", "")) if data.get("header") else ""
            if not header:
                header = _header_for_module(module)

            declared_symbols = _clean_symbols(data.get("declared_symbols"))
            defined_symbols = _clean_symbols(data.get("defined_symbols"))
            if not defined_symbols:
                defined_symbols = _clean_symbols(data.get("exports"))
            required_symbols = _clean_symbols(data.get("required_symbols"))

            # Keep module contracts focused on callable symbols.
            # LLM output may inject type names (e.g. enums/struct aliases)
            # into declared_symbols; those are not part of symbol closure.
            symbol_closure_targets = set(defined_symbols + required_symbols)
            if symbol_closure_targets:
                declared_symbols = [symbol for symbol in declared_symbols if symbol in symbol_closure_targets]
            else:
                declared_symbols = []
            declared_symbols = _unique(declared_symbols + defined_symbols)

            contracts_by_module[module] = {
                "module": module,
                "header": header,
                "local_includes": _clean_local_includes(data.get("local_includes")),
                "declared_symbols": declared_symbols,
                "defined_symbols": defined_symbols,
                "exports": defined_symbols,
                "required_symbols": required_symbols,
                "required_assets": _clean_assets(data.get("required_assets")),
                "critical": _as_bool(data.get("critical"), default=False),
                "integrated": _as_bool(data.get("integrated"), default=True),
                "allows_stub": _as_bool(data.get("allows_stub"), default=False),
            }

    module_candidates = [CORE_MAIN_C, CORE_GAME_C]
    module_candidates.extend(_module_path(module_name) for module_name in modules)

    for path in sorted(known_scaffold_paths):
        if path.endswith(".c"):
            module_candidates.append(path)

    module_candidates = [module for module in _unique(module_candidates) if module]

    for module in module_candidates:
        if module in contracts_by_module:
            continue

        contracts_by_module[module] = {
            "module": module,
            "header": _header_for_module(module),
            "local_includes": [],
            "declared_symbols": [],
            "defined_symbols": [],
            "exports": [],
            "required_symbols": [],
            "required_assets": [],
            "critical": False,
            "integrated": True,
            "allows_stub": False,
        }

    main_contract = contracts_by_module.get(CORE_MAIN_C)
    if main_contract:
        main_contract["header"] = ""
        main_contract["local_includes"] = _unique(main_contract["local_includes"] + ["game.h"])
        main_contract["required_symbols"] = _clean_symbols(
            main_contract["required_symbols"] + ["game_init", "game_update", "game_render"]
        )
        main_contract["critical"] = True
        main_contract["integrated"] = True
        main_contract["allows_stub"] = False

    game_contract = contracts_by_module.get(CORE_GAME_C)
    if game_contract:
        entrypoints = _clean_symbols(["game_init", "game_update", "game_render"])
        game_contract["header"] = CORE_GAME_H
        game_contract["local_includes"] = _unique(game_contract["local_includes"] + ["game.h"])
        game_contract["declared_symbols"] = _clean_symbols(
            game_contract.get("declared_symbols", []) + entrypoints
        )
        game_contract["defined_symbols"] = _clean_symbols(
            game_contract.get("defined_symbols", []) + entrypoints
        )
        game_contract["exports"] = list(game_contract["defined_symbols"])
        game_contract["critical"] = True
        game_contract["integrated"] = True
        game_contract["allows_stub"] = False

    contracts: list[dict] = [
        contracts_by_module[module]
        for module in _unique([CORE_MAIN_C, CORE_GAME_C] + sorted(contracts_by_module.keys()))
        if module in contracts_by_module
    ]

    for contract in contracts:
        if not contract.get("header"):
            contract["header"] = _header_for_module(contract["module"])

    return contracts


def _module_has_hint(module_contracts: list[dict], hint: str) -> bool:
    needle = hint.lower()
    for module in module_contracts:
        module_name = str(module.get("module", "")).lower()
        header_name = str(module.get("header", "")).lower()
        if needle in module_name or needle in header_name:
            return True
    return False


def _assets_from_art_for_hud(art_output: dict | None) -> list[str]:
    if not art_output:
        return []

    hud_assets = _as_list(art_output.get("hud_plan"))
    for asset in _as_list(art_output.get("asset_list")):
        lowered = asset.lower()
        if "hud" in lowered or "score" in lowered or "life" in lowered:
            hud_assets.append(asset)
    return _unique(hud_assets)


def _assets_from_art_for_tilemap(art_output: dict | None) -> list[str]:
    if not art_output:
        return []

    tile_assets = _as_list(art_output.get("tileset_plan"))
    for asset in _as_list(art_output.get("asset_list")):
        lowered = asset.lower()
        if "tile" in lowered or "tileset" in lowered or "tilemap" in lowered or "level" in lowered:
            tile_assets.append(asset)
    return _unique(tile_assets)


def _build_contract_main_c(required_entrypoints: list[str]) -> str:
    entrypoints = _clean_symbols(required_entrypoints) or ["game_init", "game_update", "game_render"]

    init_symbol = entrypoints[0]
    update_symbol = entrypoints[1] if len(entrypoints) > 1 else entrypoints[0]
    render_symbol = entrypoints[2] if len(entrypoints) > 2 else entrypoints[-1]

    body_lines = [
        f"{init_symbol}();",
        "",
        "while (1) {",
        f"    {update_symbol}();",
        f"    {render_symbol}();",
        "    cpct_waitVSYNC();",
        "}",
    ]

    for symbol in entrypoints:
        body_lines.append(f"/* required entrypoint: {symbol} */")

    return "\n".join(
        [
            '#include <cpctelera.h>',
            '#include "game.h"',
            "",
            "void main(void) {",
            *(f"    {line}" if line else "" for line in body_lines),
            "}",
            "",
        ]
    )


def _build_contract_game_c() -> str:
    return "\n".join(
        [
            '#include "game.h"',
            '#include <cpctelera.h>',
            "",
            "void game_init(void) {",
            "    cpct_disableFirmware();",
            "    cpct_setVideoMode(1);",
            "    cpct_clearScreen(0x00);",
            "}",
            "",
            "void game_update(void) {",
            "}",
            "",
            "void game_render(void) {",
            "}",
            "",
        ]
    )


def _normalize_runtime_contract(payload: dict, module_contracts: list[dict]) -> dict:
    raw = _as_dict(payload.get("runtime_contract"))
    raw_profile = str(raw.get("compile_profile", "playable_slice")).strip()
    profile_token = "".join(ch for ch in raw_profile.lower() if ch.isalpha())
    profile_map = {
        "prototype": "prototype",
        "verticalslice": "vertical_slice",
        "playableslice": "playable_slice",
    }
    compile_profile = profile_map.get(profile_token, "playable_slice")
    if compile_profile not in {"prototype", "vertical_slice", "playable_slice"}:
        compile_profile = "playable_slice"

    critical_modules = _unique(path for path in (_src_path(path) for path in _as_list(raw.get("critical_modules"))) if path)
    integrated_modules = _unique(path for path in (_src_path(path) for path in _as_list(raw.get("integrated_modules"))) if path)

    for module in module_contracts:
        module_path = module.get("module", "")
        if module.get("critical") and module_path:
            critical_modules.append(module_path)
        if module.get("integrated", True) and module_path:
            integrated_modules.append(module_path)

    critical_modules.extend(RUNTIME_CRITICAL_MODULES)
    integrated_modules.extend(RUNTIME_CRITICAL_MODULES)

    return {
        "compile_profile": compile_profile,
        "critical_modules": _unique(path for path in critical_modules if path),
        "integrated_modules": _unique(path for path in integrated_modules if path),
        "required_entrypoints": _clean_symbols(raw.get("required_entrypoints"))
        or ["game_init", "game_update", "game_render"],
        "main_loop_file": _src_path(str(raw.get("main_loop_file", "src/main.c"))),
        "reject_empty_main_loop": _as_bool(raw.get("reject_empty_main_loop"), default=True),
    }


def _normalize_asset_contract(payload: dict, art_output: dict | None, module_contracts: list[dict]) -> dict:
    raw = _as_dict(payload.get("asset_contract"))
    required_assets = _clean_assets(raw.get("required_assets"))

    if art_output:
        required_assets.extend(_clean_assets(art_output.get("asset_list")))

    if _module_has_hint(module_contracts, "hud"):
        required_assets.extend(_assets_from_art_for_hud(art_output))

    if _module_has_hint(module_contracts, "tilemap"):
        required_assets.extend(_assets_from_art_for_tilemap(art_output))

    if _module_has_hint(module_contracts, "player"):
        required_assets.append("sprplayerknight")
    if _module_has_hint(module_contracts, "hud"):
        required_assets.append("hudhealthbar")
    if _module_has_hint(module_contracts, "tile"):
        required_assets.append("tilesetbase")

    for module in module_contracts:
        required_assets.extend(_clean_assets(module.get("required_assets")))

    required_assets = _unique(required_assets)
    declared_assets = _unique(_clean_assets(raw.get("declared_assets")) + required_assets)
    defined_assets = _unique(_clean_assets(raw.get("defined_assets")) + required_assets)

    return {
        "required_assets": required_assets,
        "declared_assets": declared_assets,
        "defined_assets": defined_assets,
    }


def _normalize_integration_blueprint(
    payload: dict,
    scaffold: dict,
    module_contracts: list[dict],
    runtime: dict,
    asset_file_map: dict[str, list[str]],
) -> dict:
    raw = _as_dict(payload.get("integration_blueprint"))

    planned_files = _as_list(raw.get("planned_files"))
    planned_files.extend(scaffold.get("required_files", []))
    planned_files.extend(scaffold.get("create_if_missing", []))
    for files_for_asset in asset_file_map.values():
        planned_files.extend(_as_list(files_for_asset))

    for module in module_contracts:
        planned_files.append(module.get("module", ""))
        planned_files.append(module.get("header", ""))

    provided_symbols: dict[str, list[str]] = {}
    required_symbols: dict[str, list[str]] = {}
    file_headers: dict[str, list[str]] = {}

    raw_provided = raw.get("provided_symbols", {})
    if isinstance(raw_provided, dict):
        for module, symbols in raw_provided.items():
            module_path = _src_path(module)
            if not module_path:
                continue
            provided_symbols[module_path] = _clean_symbols(symbols)

    raw_required = raw.get("required_symbols", {})
    if isinstance(raw_required, dict):
        for module, symbols in raw_required.items():
            module_path = _src_path(module)
            if not module_path:
                continue
            required_symbols[module_path] = _clean_symbols(symbols)

    raw_headers = raw.get("file_headers", {})
    if isinstance(raw_headers, dict):
        for module, includes in raw_headers.items():
            module_path = _src_path(module)
            if not module_path:
                continue
            file_headers[module_path] = _clean_local_includes(includes)

    for module in module_contracts:
        module_path = module.get("module", "")
        if not module_path:
            continue

        module_defined_symbols = _clean_symbols(module.get("defined_symbols") or module.get("exports"))
        if module_defined_symbols:
            provided_symbols[module_path] = _unique(
                provided_symbols.get(module_path, []) + module_defined_symbols
            )

        if module.get("required_symbols"):
            required_symbols[module_path] = _unique(
                required_symbols.get(module_path, []) + _clean_symbols(module.get("required_symbols"))
            )

        if module.get("local_includes"):
            file_headers[module_path] = _unique(
                file_headers.get(module_path, []) + _clean_local_includes(module.get("local_includes"))
            )

    files = {}
    raw_files = raw.get("files", {})
    if isinstance(raw_files, dict):
        for file_path, content in raw_files.items():
            normalized_path = _src_path(file_path)
            if not normalized_path:
                continue
            files[normalized_path] = str(content)

    # Force non-empty playable-slice templates for core loop files so contract
    # validation does not depend on minimal LLM placeholders.
    files[CORE_MAIN_C] = _build_contract_main_c(_as_list(runtime.get("required_entrypoints")))
    files[CORE_GAME_C] = _build_contract_game_c()

    integrated_modules = _unique(
        _src_path(path)
        for path in (_as_list(raw.get("integrated_modules")) + _as_list(runtime.get("integrated_modules")))
    )

    raw_owned = _as_list(raw.get("owned_files"))
    owned_files = list(raw_owned)
    owned_files.extend(_as_list(raw.get("planned_files")))
    for files_for_asset in asset_file_map.values():
        owned_files.extend(_as_list(files_for_asset))

    normalized_asset_file_map: dict[str, list[str]] = {}
    for asset, mapped_files in asset_file_map.items():
        clean_asset = normalize_asset_token(asset)
        if not clean_asset:
            continue
        clean_files = _unique(path for path in (_src_path(item) for item in _as_list(mapped_files)) if path)
        if clean_files:
            normalized_asset_file_map[clean_asset] = clean_files

    return {
        "planned_files": _unique(_src_path(path) for path in planned_files if path),
        "provided_symbols": provided_symbols,
        "required_symbols": required_symbols,
        "file_headers": file_headers,
        "integrated_modules": [path for path in integrated_modules if path],
        "owned_files": _unique(_src_path(path) for path in owned_files if path),
        "asset_file_map": normalized_asset_file_map,
        "files": files,
    }


def _resolve_include_reference(owner_file: str, include: str, known_headers: set[str]) -> str:
    normalized_includes = _clean_local_includes([include])
    if not normalized_includes:
        return ""

    token = normalized_includes[0]

    if token.startswith("src/"):
        direct_src = _src_path(token)
        if direct_src and direct_src in known_headers:
            return direct_src

    if token in known_headers:
        return token

    owner_path = _src_path(owner_file)
    owner_dir = PurePosixPath(owner_path).parent.as_posix() if owner_path else ""
    if owner_dir and owner_dir != ".":
        joined = _src_path(f"{owner_dir}/{token}")
        if joined and joined in known_headers:
            return joined

    basename = PurePosixPath(token).name
    basename_matches = [path for path in known_headers if PurePosixPath(path).name == basename]
    if len(basename_matches) == 1:
        return basename_matches[0]

    basename_slug = _token_slug(basename)
    if basename_slug:
        slug_matches = [
            path
            for path in known_headers
            if _token_slug(PurePosixPath(path).name) == basename_slug
        ]
        if len(slug_matches) == 1:
            return slug_matches[0]

    return token


def _normalize_contract_include_references(
    module_contracts: list[dict],
    integration_blueprint: dict,
    scaffold: dict,
    asset_file_map: dict[str, list[str]],
) -> tuple[list[dict], dict]:
    header_universe: set[str] = set()

    for key in (
        "required_files",
        "base_scaffold_files",
        "optional_files",
        "allowed_files",
        "overwrite_files",
        "create_if_missing",
    ):
        for path in _as_list(scaffold.get(key)):
            normalized = _src_path(path)
            if normalized and normalized.endswith(".h"):
                header_universe.add(normalized)

    for mapped_files in asset_file_map.values():
        for path in _as_list(mapped_files):
            normalized = _src_path(path)
            if normalized and normalized.endswith(".h"):
                header_universe.add(normalized)

    for path in _as_list(integration_blueprint.get("planned_files")):
        normalized = _src_path(path)
        if normalized and normalized.endswith(".h"):
            header_universe.add(normalized)

    normalized_contracts: list[dict] = []
    for contract in module_contracts:
        contract_copy = dict(contract)
        owner = str(contract_copy.get("module", ""))
        includes = _clean_local_includes(contract_copy.get("local_includes"))

        resolved: list[str] = []
        for include in includes:
            include_token = _resolve_include_reference(owner, include, header_universe)
            if include_token:
                resolved.append(include_token)

        contract_copy["local_includes"] = _unique(resolved)
        normalized_contracts.append(contract_copy)

    blueprint = dict(integration_blueprint)
    raw_file_headers = _as_dict(blueprint.get("file_headers"))
    normalized_file_headers: dict[str, list[str]] = {}
    for owner, includes in raw_file_headers.items():
        owner_path = _src_path(owner)
        if not owner_path:
            continue

        resolved: list[str] = []
        for include in _clean_local_includes(includes):
            include_token = _resolve_include_reference(owner_path, include, header_universe)
            if include_token:
                resolved.append(include_token)

        if resolved:
            normalized_file_headers[owner_path] = _unique(resolved)

    blueprint["file_headers"] = normalized_file_headers
    return normalized_contracts, blueprint


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
    modules = _as_list(payload.get("modules"))
    scaffold = _ensure_core_scaffold(_as_dict(payload.get("scaffold")))
    module_contracts = _normalize_module_contracts(payload, modules, scaffold)
    runtime_contract = _normalize_runtime_contract(payload, module_contracts)
    asset_contract = _normalize_asset_contract(payload, art_output, module_contracts)
    asset_file_map = _build_asset_file_map(asset_contract, module_contracts, runtime_contract)
    scaffold = _ensure_asset_scaffold_entries(scaffold, asset_file_map)
    integration_blueprint = _normalize_integration_blueprint(
        payload,
        scaffold,
        module_contracts,
        runtime_contract,
        asset_file_map,
    )
    module_contracts, integration_blueprint = _normalize_contract_include_references(
        module_contracts,
        integration_blueprint,
        scaffold,
        asset_file_map,
    )

    return {
        "archetype": str(payload.get("archetype", "")).strip(),
        "video_mode": str(payload.get("video_mode", "Mode 1")).strip() or "Mode 1",
        "level_structure": str(payload.get("level_structure", "")).strip(),
        "camera": str(payload.get("camera", "")).strip(),
        "modules": modules,
        "input_model": _as_dict(payload.get("input_model")),
        "entity_model": _as_dict(payload.get("entity_model")),
        "collision_model": _as_dict(payload.get("collision_model")),
        "rendering_model": _as_dict(payload.get("rendering_model")),
        "data_model": _as_dict(payload.get("data_model")),
        "update_order": _as_list(payload.get("update_order")),
        "scaffold": scaffold,
        "runtime_contract": runtime_contract,
        "module_contracts": module_contracts,
        "asset_contract": asset_contract,
        "integration_blueprint": integration_blueprint,
    }
