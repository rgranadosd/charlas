import re
from pathlib import PurePosixPath
from typing import Any

from app.schemas.outputs import (
    AssetContract,
    BuildContract,
    ContractValidationIssue,
    ContractValidationOutput,
    ModuleContract,
    TechOutput,
    TechOutputV2,
    TechScaffold,
)

_LOCAL_INCLUDE_RE = re.compile(r'^\s*#\s*include\s+"([^"]+)"', re.MULTILINE)
_FUNCTION_DEF_RE = re.compile(r'\b([A-Za-z_][A-Za-z0-9_]*)\s*\([^;{}]*\)\s*\{')
_FUNCTION_DECL_RE = re.compile(r'\b([A-Za-z_][A-Za-z0-9_]*)\s*\([^;{}]*\)\s*;')
_EMPTY_WHILE_RE = re.compile(r'while\s*\([^)]*\)\s*\{\s*\}', re.DOTALL)

_SRC_PATH_RE = re.compile(r'^src/[A-Za-z0-9_./-]+\.(?:c|h)$')
_SRC_PATH_EXTRACT_RE = re.compile(r'src/[A-Za-z0-9_./-]+\.(?:c|h)')
_C_IDENT_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
_SIMPLE_ASSET_RE = re.compile(r'^[A-Za-z0-9_][A-Za-z0-9_.-]{0,127}$')
_INCLUDE_TOKEN_RE = re.compile(r'^[A-Za-z0-9_./-]+\.h$')


def _issue(
    code: str,
    message: str,
    *,
    file: str = "",
    related_items: list[str] | None = None,
    severity: str = "error",
    symbol: str = "",
    asset: str = "",
) -> ContractValidationIssue:
    return ContractValidationIssue(
        code=code,
        message=message,
        file=file,
        related_items=related_items or [],
        severity="warning" if severity == "warning" else "error",
        symbol=symbol,
        asset=asset,
    )


def _warn_dropped(kind: str, value: Any, *, context: str = "") -> ContractValidationIssue:
    raw = str(value).strip()
    suffix = f" ({context})" if context else ""
    return _issue(
        f"NORMALIZATION_DROPPED_{kind.upper()}_TOKEN",
        f"Dropped unsafe {kind} token{suffix}: {raw}",
        severity="warning",
        related_items=[raw] if raw else [],
    )


def _dedupe_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def _strip_wrappers(value: str) -> str:
    text = value.strip().replace("\\", "/")
    while text and text[0] in '"\'`([{<':
        text = text[1:].strip()
    while text and text[-1] in '"\'`)]}>,;:':
        text = text[:-1].strip()
    return text


def normalize_src_path_token(value: str) -> str | None:
    raw = _strip_wrappers(str(value))
    if not raw:
        return None

    if raw.startswith("./"):
        raw = raw[2:]

    if _SRC_PATH_RE.fullmatch(raw):
        path = PurePosixPath(raw).as_posix()
        if ".." in PurePosixPath(path).parts:
            return None
        return path

    matches = list(_SRC_PATH_EXTRACT_RE.finditer(raw))
    if len(matches) != 1:
        return None

    match = matches[0]
    candidate = match.group(0)
    remainder = (raw[: match.start()] + raw[match.end() :]).strip()
    if remainder and any(ch.isalnum() for ch in remainder):
        return None

    if not _SRC_PATH_RE.fullmatch(candidate):
        return None

    path = PurePosixPath(candidate).as_posix()
    if ".." in PurePosixPath(path).parts:
        return None
    return path


def normalize_symbol_token(value: str) -> str | None:
    raw = _strip_wrappers(str(value))
    if not raw:
        return None

    if _C_IDENT_RE.fullmatch(raw):
        return raw

    if "." in raw or " " in raw and "(" not in raw:
        return None

    match = re.match(r'^(?:[A-Za-z_][A-Za-z0-9_\s\*]*\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*\(', raw)
    if match:
        symbol = match.group(1)
        if _C_IDENT_RE.fullmatch(symbol):
            return symbol

    return None


def normalize_asset_token(value: str) -> str | None:
    raw = _strip_wrappers(str(value))
    if not raw:
        return None

    if _SIMPLE_ASSET_RE.fullmatch(raw):
        return raw

    return None


def _normalize_include_token(value: str) -> str | None:
    raw = _strip_wrappers(str(value))
    if not raw:
        return None

    if raw.startswith("src/"):
        src_path = normalize_src_path_token(raw)
        if src_path and src_path.endswith(".h"):
            return src_path

    if _INCLUDE_TOKEN_RE.fullmatch(raw):
        if ".." in raw.split("/"):
            return None
        return raw

    matches = list(re.finditer(r'[A-Za-z0-9_./-]+\.h', raw))
    if len(matches) != 1:
        return None

    match = matches[0]
    candidate = match.group(0)
    remainder = (raw[: match.start()] + raw[match.end() :]).strip()
    if remainder and any(ch.isalnum() for ch in remainder):
        return None

    if candidate.startswith("src/"):
        src_path = normalize_src_path_token(candidate)
        if src_path and src_path.endswith(".h"):
            return src_path

    if _INCLUDE_TOKEN_RE.fullmatch(candidate):
        if ".." in candidate.split("/"):
            return None
        return candidate

    return None


def _normalize_src_list(values: list[Any], *, context: str) -> tuple[list[str], list[ContractValidationIssue]]:
    normalized: list[str] = []
    warnings: list[ContractValidationIssue] = []

    for value in values:
        token = normalize_src_path_token(str(value))
        if token is None:
            if str(value).strip():
                warnings.append(_warn_dropped("src", value, context=context))
            continue
        normalized.append(token)

    return _dedupe_keep_order(normalized), warnings


def _normalize_symbol_list(values: list[Any], *, context: str) -> tuple[list[str], list[ContractValidationIssue]]:
    normalized: list[str] = []
    warnings: list[ContractValidationIssue] = []

    for value in values:
        token = normalize_symbol_token(str(value))
        if token is None:
            if str(value).strip():
                warnings.append(_warn_dropped("symbol", value, context=context))
            continue
        normalized.append(token)

    return _dedupe_keep_order(normalized), warnings


def _normalize_asset_list(values: list[Any], *, context: str) -> tuple[list[str], list[ContractValidationIssue]]:
    normalized: list[str] = []
    warnings: list[ContractValidationIssue] = []

    for value in values:
        token = normalize_asset_token(str(value))
        if token is None:
            if str(value).strip():
                warnings.append(_warn_dropped("asset", value, context=context))
            continue
        normalized.append(token)

    return _dedupe_keep_order(normalized), warnings


def _normalize_include_list(values: list[Any], *, context: str) -> tuple[list[str], list[ContractValidationIssue]]:
    normalized: list[str] = []
    warnings: list[ContractValidationIssue] = []

    for value in values:
        token = _normalize_include_token(str(value))
        if token is None:
            if str(value).strip():
                warnings.append(_warn_dropped("include", value, context=context))
            continue
        normalized.append(token)

    return _dedupe_keep_order(normalized), warnings


def _normalize_module_hint_to_src_c(value: str) -> str | None:
    raw = _strip_wrappers(str(value))
    if not raw:
        return None

    if raw.startswith("src/"):
        candidate = raw
    else:
        candidate = f"src/{raw.lstrip('/')}"

    if candidate.endswith(".h"):
        candidate = candidate[:-2] + ".c"
    elif not candidate.endswith(".c"):
        candidate = candidate + ".c"

    return normalize_src_path_token(candidate)


def canonicalize_scaffold(scaffold: TechScaffold | dict) -> tuple[TechScaffold, list[ContractValidationIssue]]:
    model = scaffold if isinstance(scaffold, TechScaffold) else TechScaffold.model_validate(scaffold or {})
    warnings: list[ContractValidationIssue] = []

    required_files, w = _normalize_src_list(list(model.required_files), context="scaffold.required_files")
    warnings.extend(w)

    base_scaffold_files, w = _normalize_src_list(
        list(model.base_scaffold_files),
        context="scaffold.base_scaffold_files",
    )
    warnings.extend(w)

    optional_files, w = _normalize_src_list(list(model.optional_files), context="scaffold.optional_files")
    warnings.extend(w)

    allowed_files, w = _normalize_src_list(list(model.allowed_files), context="scaffold.allowed_files")
    warnings.extend(w)

    if not allowed_files:
        allowed_files = _dedupe_keep_order(required_files + base_scaffold_files + optional_files)

    overwrite_files, w = _normalize_src_list(list(model.overwrite_files), context="scaffold.overwrite_files")
    warnings.extend(w)

    create_if_missing, w = _normalize_src_list(
        list(model.create_if_missing),
        context="scaffold.create_if_missing",
    )
    warnings.extend(w)

    overwrite_files = [path for path in overwrite_files if path in allowed_files]
    create_if_missing = [path for path in create_if_missing if path in allowed_files]

    return (
        TechScaffold(
            required_files=required_files,
            base_scaffold_files=base_scaffold_files,
            optional_files=optional_files,
            allowed_files=allowed_files,
            overwrite_files=overwrite_files,
            create_if_missing=create_if_missing,
        ),
        warnings,
    )


def canonicalize_module_contracts(
    module_contracts: list[ModuleContract] | list[dict] | None,
    modules: list[str] | None,
    scaffold: TechScaffold,
) -> tuple[list[ModuleContract], list[ContractValidationIssue]]:
    warnings: list[ContractValidationIssue] = []
    normalized_modules: dict[str, ModuleContract] = {}

    items = module_contracts if isinstance(module_contracts, list) else []
    for item in items:
        model = item if isinstance(item, ModuleContract) else ModuleContract.model_validate(item or {})

        module_path = normalize_src_path_token(model.module)
        if module_path is None:
            fallback = _normalize_module_hint_to_src_c(model.module)
            module_path = fallback

        if module_path is None:
            if str(model.module).strip():
                warnings.append(_warn_dropped("src", model.module, context="module_contract.module"))
            continue

        header = ""
        if model.header:
            header = normalize_src_path_token(model.header) or ""
            if not header:
                warnings.append(_warn_dropped("src", model.header, context=f"module_contract[{module_path}].header"))

        local_includes, w = _normalize_include_list(
            list(model.local_includes),
            context=f"module_contract[{module_path}].local_includes",
        )
        warnings.extend(w)

        declared_symbols, w = _normalize_symbol_list(
            list(model.declared_symbols),
            context=f"module_contract[{module_path}].declared_symbols",
        )
        warnings.extend(w)

        defined_symbol_candidates = list(model.defined_symbols) if model.defined_symbols else list(model.exports)
        defined_symbols, w = _normalize_symbol_list(
            defined_symbol_candidates,
            context=f"module_contract[{module_path}].defined_symbols",
        )
        warnings.extend(w)

        required_symbols, w = _normalize_symbol_list(
            list(model.required_symbols),
            context=f"module_contract[{module_path}].required_symbols",
        )
        warnings.extend(w)

        required_assets, w = _normalize_asset_list(
            list(model.required_assets),
            context=f"module_contract[{module_path}].required_assets",
        )
        warnings.extend(w)

        candidate = ModuleContract(
            module=module_path,
            header=header,
            local_includes=local_includes,
            declared_symbols=declared_symbols,
            defined_symbols=defined_symbols,
            exports=defined_symbols,
            required_symbols=required_symbols,
            required_assets=required_assets,
            critical=bool(model.critical),
            integrated=bool(model.integrated),
            allows_stub=bool(model.allows_stub),
        )

        current = normalized_modules.get(module_path)
        if not current:
            normalized_modules[module_path] = candidate
            continue

        merged_defined = _dedupe_keep_order(current.defined_symbols + candidate.defined_symbols)

        normalized_modules[module_path] = ModuleContract(
            module=module_path,
            header=current.header or candidate.header,
            local_includes=_dedupe_keep_order(current.local_includes + candidate.local_includes),
            declared_symbols=_dedupe_keep_order(current.declared_symbols + candidate.declared_symbols),
            defined_symbols=merged_defined,
            exports=merged_defined,
            required_symbols=_dedupe_keep_order(current.required_symbols + candidate.required_symbols),
            required_assets=_dedupe_keep_order(current.required_assets + candidate.required_assets),
            critical=current.critical or candidate.critical,
            integrated=current.integrated and candidate.integrated,
            allows_stub=current.allows_stub or candidate.allows_stub,
        )

    if not normalized_modules:
        for module_hint in modules or []:
            module_path = _normalize_module_hint_to_src_c(module_hint)
            if module_path is None:
                if str(module_hint).strip():
                    warnings.append(_warn_dropped("src", module_hint, context="tech.modules"))
                continue
            if module_path in normalized_modules:
                continue
            normalized_modules[module_path] = ModuleContract(module=module_path)

    ordered = [normalized_modules[key] for key in sorted(normalized_modules.keys())]
    return ordered, warnings


def canonicalize_asset_contract(
    asset_contract: AssetContract | dict | None,
    module_contracts: list[ModuleContract],
) -> tuple[AssetContract, list[ContractValidationIssue]]:
    warnings: list[ContractValidationIssue] = []
    model = (
        asset_contract
        if isinstance(asset_contract, AssetContract)
        else AssetContract.model_validate(asset_contract or {})
    )

    required_assets, w = _normalize_asset_list(list(model.required_assets), context="asset_contract.required_assets")
    warnings.extend(w)

    for contract in module_contracts:
        normalized_required, w = _normalize_asset_list(
            list(contract.required_assets),
            context=f"module_contract[{contract.module}].required_assets",
        )
        warnings.extend(w)
        required_assets.extend(normalized_required)

    required_assets = _dedupe_keep_order(required_assets)

    declared_assets, w = _normalize_asset_list(list(model.declared_assets), context="asset_contract.declared_assets")
    warnings.extend(w)

    defined_assets, w = _normalize_asset_list(list(model.defined_assets), context="asset_contract.defined_assets")
    warnings.extend(w)

    return (
        AssetContract(
            required_assets=required_assets,
            declared_assets=declared_assets,
            defined_assets=defined_assets,
        ),
        warnings,
    )


def _canonicalize_symbol_map(
    mapping: dict[str, Any],
    *,
    context: str,
) -> tuple[dict[str, list[str]], list[ContractValidationIssue]]:
    normalized: dict[str, list[str]] = {}
    warnings: list[ContractValidationIssue] = []

    for owner, symbols in mapping.items():
        owner_path = normalize_src_path_token(str(owner))
        if owner_path is None:
            warnings.append(_warn_dropped("src", owner, context=f"{context}.owner"))
            continue

        if not isinstance(symbols, list):
            continue

        normalized_symbols, w = _normalize_symbol_list(
            list(symbols),
            context=f"{context}[{owner_path}]",
        )
        warnings.extend(w)
        if normalized_symbols:
            normalized[owner_path] = _dedupe_keep_order(normalized.get(owner_path, []) + normalized_symbols)

    return normalized, warnings


def _canonicalize_include_map(
    mapping: dict[str, Any],
    *,
    context: str,
) -> tuple[dict[str, list[str]], list[ContractValidationIssue]]:
    normalized: dict[str, list[str]] = {}
    warnings: list[ContractValidationIssue] = []

    for owner, includes in mapping.items():
        owner_path = normalize_src_path_token(str(owner))
        if owner_path is None:
            warnings.append(_warn_dropped("src", owner, context=f"{context}.owner"))
            continue

        if not isinstance(includes, list):
            continue

        normalized_includes, w = _normalize_include_list(
            list(includes),
            context=f"{context}[{owner_path}]",
        )
        warnings.extend(w)
        if normalized_includes:
            normalized[owner_path] = _dedupe_keep_order(normalized.get(owner_path, []) + normalized_includes)

    return normalized, warnings


def _canonicalize_asset_file_map(
    mapping: dict[str, Any],
    *,
    context: str,
) -> tuple[dict[str, list[str]], list[ContractValidationIssue]]:
    normalized: dict[str, list[str]] = {}
    warnings: list[ContractValidationIssue] = []

    for asset_name, raw_files in mapping.items():
        asset_token = normalize_asset_token(str(asset_name))
        if asset_token is None:
            if str(asset_name).strip():
                warnings.append(_warn_dropped("asset", asset_name, context=f"{context}.asset"))
            continue

        if not isinstance(raw_files, list):
            continue

        normalized_files, w = _normalize_src_list(
            list(raw_files),
            context=f"{context}[{asset_token}]",
        )
        warnings.extend(w)

        if normalized_files:
            normalized[asset_token] = _dedupe_keep_order(normalized.get(asset_token, []) + normalized_files)

    return normalized, warnings


def canonicalize_runtime_contract(
    runtime_contract: BuildContract | dict | None,
) -> tuple[BuildContract, list[ContractValidationIssue]]:
    warnings: list[ContractValidationIssue] = []
    model = (
        runtime_contract
        if isinstance(runtime_contract, BuildContract)
        else BuildContract.model_validate(runtime_contract or {})
    )

    compile_profile = model.compile_profile
    if compile_profile not in {"prototype", "vertical_slice", "playable_slice"}:
        compile_profile = "playable_slice"

    critical_modules, w = _normalize_src_list(list(model.critical_modules), context="runtime_contract.critical_modules")
    warnings.extend(w)

    integrated_modules, w = _normalize_src_list(
        list(model.integrated_modules),
        context="runtime_contract.integrated_modules",
    )
    warnings.extend(w)

    required_entrypoints, w = _normalize_symbol_list(
        list(model.required_entrypoints),
        context="runtime_contract.required_entrypoints",
    )
    warnings.extend(w)

    main_loop_file = normalize_src_path_token(model.main_loop_file)
    if main_loop_file is None:
        if str(model.main_loop_file).strip():
            warnings.append(_warn_dropped("src", model.main_loop_file, context="runtime_contract.main_loop_file"))
        main_loop_file = "src/main.c"

    return (
        BuildContract(
            compile_profile=compile_profile,
            critical_modules=critical_modules,
            integrated_modules=integrated_modules,
            required_entrypoints=required_entrypoints,
            main_loop_file=main_loop_file,
            reject_empty_main_loop=bool(model.reject_empty_main_loop),
        ),
        warnings,
    )


def canonicalize_integration_blueprint(
    integration_blueprint: dict[str, Any] | None,
) -> tuple[dict[str, Any], list[ContractValidationIssue]]:
    payload = integration_blueprint if isinstance(integration_blueprint, dict) else {}
    warnings: list[ContractValidationIssue] = []

    planned_files_raw = payload.get("planned_files", [])
    planned_files, w = _normalize_src_list(
        list(planned_files_raw) if isinstance(planned_files_raw, list) else [],
        context="integration_blueprint.planned_files",
    )
    warnings.extend(w)

    integrated_modules_raw = payload.get("integrated_modules", [])
    integrated_modules, w = _normalize_src_list(
        list(integrated_modules_raw) if isinstance(integrated_modules_raw, list) else [],
        context="integration_blueprint.integrated_modules",
    )
    warnings.extend(w)

    owned_files_raw = payload.get("owned_files", [])
    owned_files, w = _normalize_src_list(
        list(owned_files_raw) if isinstance(owned_files_raw, list) else [],
        context="integration_blueprint.owned_files",
    )
    warnings.extend(w)

    files_raw = payload.get("files", {})
    files: dict[str, str] = {}
    if isinstance(files_raw, dict):
        for key, content in files_raw.items():
            key_path = normalize_src_path_token(str(key))
            if key_path is None:
                warnings.append(_warn_dropped("src", key, context="integration_blueprint.files.key"))
                continue
            files[key_path] = str(content)

    file_headers_raw = payload.get("file_headers", {})
    file_headers, w = _canonicalize_include_map(
        file_headers_raw if isinstance(file_headers_raw, dict) else {},
        context="integration_blueprint.file_headers",
    )
    warnings.extend(w)

    provided_symbols_raw = payload.get("provided_symbols", {})
    provided_symbols, w = _canonicalize_symbol_map(
        provided_symbols_raw if isinstance(provided_symbols_raw, dict) else {},
        context="integration_blueprint.provided_symbols",
    )
    warnings.extend(w)

    required_symbols_raw = payload.get("required_symbols", {})
    required_symbols, w = _canonicalize_symbol_map(
        required_symbols_raw if isinstance(required_symbols_raw, dict) else {},
        context="integration_blueprint.required_symbols",
    )
    warnings.extend(w)

    asset_file_map_raw = payload.get("asset_file_map", {})
    asset_file_map, w = _canonicalize_asset_file_map(
        asset_file_map_raw if isinstance(asset_file_map_raw, dict) else {},
        context="integration_blueprint.asset_file_map",
    )
    warnings.extend(w)

    return (
        {
            "planned_files": _dedupe_keep_order(planned_files),
            "files": files,
            "file_headers": file_headers,
            "provided_symbols": provided_symbols,
            "required_symbols": required_symbols,
            "integrated_modules": _dedupe_keep_order(integrated_modules),
            "owned_files": _dedupe_keep_order(owned_files),
            "asset_file_map": asset_file_map,
        },
        warnings,
    )


def _input_had_runtime_contract(raw: TechOutput | TechOutputV2 | dict) -> bool:
    if isinstance(raw, dict):
        return raw.get("runtime_contract") is not None
    return raw.runtime_contract is not None


def _canonicalize_tech_output(
    tech_output: TechOutput | TechOutputV2 | dict,
) -> tuple[TechOutput, list[ContractValidationIssue], bool]:
    had_runtime_contract = _input_had_runtime_contract(tech_output)
    tech = tech_output if isinstance(tech_output, TechOutput) else TechOutput.model_validate(tech_output or {})

    warnings: list[ContractValidationIssue] = []

    scaffold, w = canonicalize_scaffold(tech.scaffold)
    warnings.extend(w)

    module_contracts, w = canonicalize_module_contracts(tech.module_contracts, tech.modules, scaffold)
    warnings.extend(w)

    runtime_contract, w = canonicalize_runtime_contract(tech.runtime_contract)
    warnings.extend(w)

    asset_contract, w = canonicalize_asset_contract(tech.asset_contract, module_contracts)
    warnings.extend(w)

    integration_blueprint, w = canonicalize_integration_blueprint(tech.integration_blueprint)
    warnings.extend(w)

    canonical = tech.model_copy(
        update={
            "scaffold": scaffold,
            "module_contracts": module_contracts,
            "runtime_contract": runtime_contract,
            "asset_contract": asset_contract,
            "integration_blueprint": integration_blueprint,
        }
    )

    return canonical, warnings, had_runtime_contract


def adapt_tech_output(tech_output: TechOutput | TechOutputV2 | dict) -> TechOutput:
    """Returns a normalized and canonicalized TechOutput without touching filesystem."""
    canonical, _, _ = _canonicalize_tech_output(tech_output)
    return canonical


def _generated_files(tech: TechOutput) -> set[str]:
    blueprint = tech.integration_blueprint if isinstance(tech.integration_blueprint, dict) else {}
    planned = blueprint.get("planned_files", [])
    files_map = blueprint.get("files", {})

    generated: list[str] = []
    if isinstance(planned, list):
        generated.extend(path for path in planned if isinstance(path, str))
    if isinstance(files_map, dict):
        generated.extend(str(path) for path in files_map.keys())

    if not generated and tech.module_contracts:
        for contract in tech.module_contracts:
            if contract.module:
                generated.append(contract.module)
            if contract.header:
                generated.append(contract.header)

    return {path for path in generated if isinstance(path, str) and path}


def _extract_includes_from_content(content: str) -> list[str]:
    return [match.group(1).strip() for match in _LOCAL_INCLUDE_RE.finditer(content or "")]


def _resolve_include(owner_file: str, include_path: str, universe: set[str]) -> str:
    include = _normalize_include_token(include_path)
    if not include:
        return ""

    direct_src = normalize_src_path_token(include)
    if direct_src and direct_src in universe:
        return direct_src

    if include in universe:
        return include

    owner_dir = PurePosixPath(owner_file).parent.as_posix() if owner_file else ""
    if owner_dir and owner_dir != ".":
        joined = normalize_src_path_token(str(PurePosixPath(owner_dir) / include))
        if joined and joined in universe:
            return joined

    basename = PurePosixPath(include).name
    matches = [path for path in universe if PurePosixPath(path).name == basename]
    if len(matches) == 1:
        return matches[0]

    return ""


def _module_symbol_maps_from_blueprint(tech: TechOutput) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    blueprint = tech.integration_blueprint if isinstance(tech.integration_blueprint, dict) else {}
    provided = blueprint.get("provided_symbols", {})
    files_map = blueprint.get("files", {})

    defined_symbols: dict[str, set[str]] = {}
    declared_symbols: dict[str, set[str]] = {}

    def add(owner_file: str, symbol_list: list[str], bucket: dict[str, set[str]]) -> None:
        if not owner_file:
            return
        owner_bucket = bucket.setdefault(owner_file, set())
        for symbol in symbol_list:
            token = normalize_symbol_token(symbol)
            if token:
                owner_bucket.add(token)

    for contract in tech.module_contracts:
        if contract.module:
            source_defined = list(contract.defined_symbols) if contract.defined_symbols else list(contract.exports)
            if source_defined:
                add(contract.module, source_defined, defined_symbols)
        if contract.header and contract.declared_symbols:
            add(contract.header, contract.declared_symbols, declared_symbols)

    if isinstance(provided, dict):
        for owner_file, symbol_list in provided.items():
            if isinstance(symbol_list, list):
                owner = str(owner_file)
                normalized = [str(symbol) for symbol in symbol_list]
                if owner.endswith(".c"):
                    add(owner, normalized, defined_symbols)
                elif owner.endswith(".h"):
                    add(owner, normalized, declared_symbols)

    if isinstance(files_map, dict):
        for owner_file, content in files_map.items():
            owner = str(owner_file)
            if owner.endswith(".c"):
                parsed = [m.group(1) for m in _FUNCTION_DEF_RE.finditer(str(content))]
                add(owner, parsed, defined_symbols)
            elif owner.endswith(".h"):
                parsed = [m.group(1) for m in _FUNCTION_DECL_RE.finditer(str(content))]
                add(owner, parsed, declared_symbols)

    return defined_symbols, declared_symbols


def _required_symbols(tech: TechOutput, include_runtime_symbols: bool) -> set[str]:
    required: list[str] = []

    for contract in tech.module_contracts:
        required.extend(contract.required_symbols)

    blueprint = tech.integration_blueprint if isinstance(tech.integration_blueprint, dict) else {}
    required_map = blueprint.get("required_symbols", {})
    if isinstance(required_map, dict):
        for values in required_map.values():
            if isinstance(values, list):
                required.extend(str(symbol) for symbol in values)

    if include_runtime_symbols and tech.runtime_contract:
        required.extend(tech.runtime_contract.required_entrypoints)

    normalized = [token for token in (normalize_symbol_token(value) for value in required) if token]
    return set(_dedupe_keep_order(normalized))


def _content_looks_stub(content: str) -> bool:
    text = str(content or "")
    if not text.strip():
        return True
    lowered = text.lower()
    if "todo" in lowered or "stub" in lowered:
        return True
    if _EMPTY_WHILE_RE.search(text):
        return True
    return False


def _validate_file_closure_canonical(tech: TechOutput) -> list[ContractValidationIssue]:
    generated = _generated_files(tech)
    allowed = set(tech.scaffold.allowed_files)

    issues: list[ContractValidationIssue] = []
    for path in sorted(generated):
        if path in allowed:
            continue
        issues.append(
            _issue(
                "FILE_NOT_ALLOWED",
                f"Generated file is outside scaffold.allowed_files: {path}",
                file=path,
                related_items=[path],
            )
        )
    return issues


def _validate_header_closure_canonical(tech: TechOutput) -> list[ContractValidationIssue]:
    generated = _generated_files(tech)
    base_scaffold = set(tech.scaffold.base_scaffold_files)
    universe = generated | base_scaffold

    blueprint = tech.integration_blueprint if isinstance(tech.integration_blueprint, dict) else {}
    file_headers = blueprint.get("file_headers", {})
    files_map = blueprint.get("files", {})

    checks: list[tuple[str, str]] = []

    for contract in tech.module_contracts:
        owner = contract.module
        if not owner:
            continue
        for include in contract.local_includes:
            checks.append((owner, str(include)))

    if isinstance(file_headers, dict):
        for owner, includes in file_headers.items():
            if not isinstance(includes, list):
                continue
            for include in includes:
                checks.append((str(owner), str(include)))

    if isinstance(files_map, dict):
        for owner, content in files_map.items():
            owner_path = str(owner)
            for include in _extract_includes_from_content(str(content)):
                checks.append((owner_path, include))

    issues: list[ContractValidationIssue] = []
    seen: set[tuple[str, str]] = set()

    for owner, include in checks:
        include_token = _normalize_include_token(include)
        if not include_token:
            continue

        key = (owner, include_token)
        if key in seen:
            continue
        seen.add(key)

        if _resolve_include(owner, include_token, universe):
            continue

        issues.append(
            _issue(
                "MISSING_LOCAL_INCLUDE",
                f'Local include "{include_token}" referenced by {owner} is not covered by generated files or base_scaffold_files.',
                file=owner,
                related_items=[include_token],
            )
        )

    return issues


def _validate_symbol_closure_canonical(
    tech: TechOutput,
    *,
    include_runtime_symbols: bool,
) -> list[ContractValidationIssue]:
    required = _required_symbols(tech, include_runtime_symbols=include_runtime_symbols)
    defined_by_module, declared_by_header = _module_symbol_maps_from_blueprint(tech)

    declared_by_symbol: dict[str, set[str]] = {}
    for header, symbols in declared_by_header.items():
        for symbol in symbols:
            declared_by_symbol.setdefault(symbol, set()).add(header)

    tracked_symbols = set(required) | set(declared_by_symbol.keys())
    if not tracked_symbols:
        return []

    definition_count: dict[str, int] = {}

    for symbols in defined_by_module.values():
        for symbol in symbols:
            definition_count[symbol] = definition_count.get(symbol, 0) + 1

    issues: list[ContractValidationIssue] = []

    for symbol in sorted(tracked_symbols):
        count = definition_count.get(symbol, 0)
        is_required = symbol in required

        if count == 0:
            if is_required:
                issues.append(
                    _issue(
                        "MISSING_REQUIRED_SYMBOL",
                        f"Required symbol is not defined in any .c file: {symbol}",
                        related_items=[symbol],
                        symbol=symbol,
                    )
                )
            else:
                declaration_sources = sorted(declared_by_symbol.get(symbol, set()))
                issues.append(
                    _issue(
                        "DECLARED_SYMBOL_NOT_DEFINED",
                        f"Declared symbol is not defined in any .c file: {symbol}",
                        related_items=declaration_sources or [symbol],
                        symbol=symbol,
                    )
                )
        elif count > 1:
            modules = sorted(module for module, symbols in defined_by_module.items() if symbol in symbols)
            issues.append(
                _issue(
                    "DUPLICATE_REQUIRED_SYMBOL" if is_required else "MULTIPLE_SYMBOL_DEFINITION",
                    f"Symbol is defined in multiple .c files: {symbol}",
                    related_items=modules,
                    symbol=symbol,
                )
            )

    return issues


def _validate_asset_closure_canonical(tech: TechOutput) -> list[ContractValidationIssue]:
    required_assets = set(tech.asset_contract.required_assets if tech.asset_contract else [])
    for contract in tech.module_contracts:
        required_assets.update(contract.required_assets)

    declared_assets = set(tech.asset_contract.declared_assets if tech.asset_contract else [])
    defined_assets = set(tech.asset_contract.defined_assets if tech.asset_contract else [])

    issues: list[ContractValidationIssue] = []

    for asset in sorted(required_assets):
        if asset not in declared_assets:
            issues.append(
                _issue(
                    "ASSET_NOT_DECLARED",
                    f"Required asset is not declared in asset_contract: {asset}",
                    related_items=[asset],
                    asset=asset,
                )
            )
        if asset not in defined_assets:
            issues.append(
                _issue(
                    "ASSET_NOT_DEFINED",
                    f"Required asset is not defined in asset_contract: {asset}",
                    related_items=[asset],
                    asset=asset,
                )
            )

    return issues


def _tracked_contract_modules(tech: TechOutput) -> set[str]:
    runtime = tech.runtime_contract or BuildContract()
    tracked = set(runtime.integrated_modules)
    tracked.update(runtime.critical_modules)

    for contract in tech.module_contracts:
        if contract.integrated or contract.critical:
            tracked.add(contract.module)

    return {path for path in tracked if path}


def _required_assets_for_file_mapping(tech: TechOutput) -> list[str]:
    required: list[str] = []

    if tech.asset_contract:
        required.extend(tech.asset_contract.required_assets)

    tracked_modules = _tracked_contract_modules(tech)
    for contract in tech.module_contracts:
        if contract.module and contract.module in tracked_modules:
            required.extend(contract.required_assets)

    normalized = [token for token in (normalize_asset_token(item) for item in required) if token]
    return _dedupe_keep_order(normalized)


def _validate_asset_file_mapping_canonical(tech: TechOutput) -> list[ContractValidationIssue]:
    blueprint = tech.integration_blueprint if isinstance(tech.integration_blueprint, dict) else {}
    raw_map = blueprint.get("asset_file_map", {})
    asset_file_map = raw_map if isinstance(raw_map, dict) else {}
    planned_files_raw = blueprint.get("planned_files", [])
    planned_files = set(planned_files_raw) if isinstance(planned_files_raw, list) else set()

    owned_files_raw = blueprint.get("owned_files", [])
    owned_files = set(owned_files_raw) if isinstance(owned_files_raw, list) else set()

    writable_files = set(tech.scaffold.base_scaffold_files)
    writable_files.update(tech.scaffold.allowed_files)
    writable_files.update(tech.scaffold.create_if_missing)

    required_assets = _required_assets_for_file_mapping(tech)
    issues: list[ContractValidationIssue] = []

    for asset in required_assets:
        raw_mapped = asset_file_map.get(asset, [])
        mapped_items = raw_mapped if isinstance(raw_mapped, list) else []
        mapped_files = [
            path
            for path in mapped_items
            if normalize_src_path_token(path)
        ]

        if not mapped_files:
            issues.append(
                _issue(
                    "REQUIRED_ASSET_NO_WRITABLE_MAPPING",
                    f"Required asset {asset} has no writable owned file mapping",
                    related_items=[asset],
                    asset=asset,
                )
            )
            continue

        missing_planned = sorted(path for path in mapped_files if path not in planned_files)
        if missing_planned:
            issues.append(
                _issue(
                    "REQUIRED_ASSET_MISSING_PLANNED_FILE",
                    f"Required asset {asset} is missing planned files: {', '.join(missing_planned)}",
                    related_items=missing_planned,
                    asset=asset,
                )
            )

        missing_owned = sorted(path for path in mapped_files if path not in owned_files)
        if missing_owned:
            issues.append(
                _issue(
                    "REQUIRED_ASSET_PLANNED_NOT_OWNED",
                    f"Required asset {asset} has planned files not owned: {', '.join(missing_owned)}",
                    related_items=missing_owned,
                    asset=asset,
                )
            )

        non_writable = sorted(path for path in mapped_files if path not in writable_files)
        if non_writable:
            issues.append(
                _issue(
                    "REQUIRED_ASSET_OWNED_NOT_WRITABLE",
                    f"Required asset {asset} has owned files outside writable scaffold: {', '.join(non_writable)}",
                    related_items=non_writable,
                    asset=asset,
                )
            )

        writable_owned = [
            path
            for path in mapped_files
            if path in planned_files and path in owned_files and path in writable_files
        ]
        if not writable_owned:
            issues.append(
                _issue(
                    "REQUIRED_ASSET_NO_WRITABLE_MAPPING",
                    f"Required asset {asset} has no writable owned file mapping",
                    related_items=mapped_files,
                    asset=asset,
                )
            )

    return issues


def _validate_scaffold_coverage_canonical(tech: TechOutput) -> list[ContractValidationIssue]:
    generated = _generated_files(tech)
    base_scaffold = set(tech.scaffold.base_scaffold_files)
    covered = generated | base_scaffold

    issues: list[ContractValidationIssue] = []
    for required in sorted(set(tech.scaffold.required_files)):
        if required in covered:
            continue
        issues.append(
            _issue(
                "REQUIRED_FILE_NOT_COVERED",
                f"Required file is not covered by generated files or base_scaffold_files: {required}",
                file=required,
                related_items=[required],
            )
        )

    return issues


def _validate_build_profile_canonical(
    tech: TechOutput,
    *,
    had_runtime_contract: bool,
) -> list[ContractValidationIssue]:
    if not had_runtime_contract:
        return []

    runtime = tech.runtime_contract or BuildContract()
    if runtime.compile_profile != "playable_slice":
        return []

    issues: list[ContractValidationIssue] = []

    blueprint = tech.integration_blueprint if isinstance(tech.integration_blueprint, dict) else {}
    files_map = blueprint.get("files", {}) if isinstance(blueprint.get("files", {}), dict) else {}

    for contract in tech.module_contracts:
        module_path = contract.module
        if module_path in {"src/main.c", "src/game.c"} and contract.allows_stub:
            issues.append(
                _issue(
                    "PLAYABLE_SLICE_STUB_NOT_ALLOWED",
                    f"playable_slice does not allow stubs for critical module: {module_path}",
                    file=module_path,
                    related_items=[module_path],
                )
            )

    for module_path in ("src/main.c", "src/game.c"):
        content = files_map.get(module_path)
        if content is None:
            continue
        if _content_looks_stub(str(content)):
            issues.append(
                _issue(
                    "PLAYABLE_SLICE_EMPTY_STUB",
                    f"playable_slice detected empty/stub-like content in {module_path}",
                    file=module_path,
                    related_items=[module_path],
                )
            )

    main_content = str(files_map.get(runtime.main_loop_file, ""))
    if main_content:
        for entrypoint in runtime.required_entrypoints:
            if entrypoint and entrypoint not in main_content:
                issues.append(
                    _issue(
                        "PLAYABLE_SLICE_MAIN_MISSING_ENTRYPOINT",
                        f"Main loop file {runtime.main_loop_file} does not reference required symbol: {entrypoint}",
                        file=runtime.main_loop_file,
                        related_items=[entrypoint],
                        symbol=entrypoint,
                    )
                )

    return issues


def validate_file_closure(tech_output: TechOutput | TechOutputV2 | dict) -> list[ContractValidationIssue]:
    tech, _, _ = _canonicalize_tech_output(tech_output)
    return _validate_file_closure_canonical(tech)


def validate_header_closure(tech_output: TechOutput | TechOutputV2 | dict) -> list[ContractValidationIssue]:
    tech, _, _ = _canonicalize_tech_output(tech_output)
    return _validate_header_closure_canonical(tech)


def validate_symbol_closure(tech_output: TechOutput | TechOutputV2 | dict) -> list[ContractValidationIssue]:
    tech, _, had_runtime = _canonicalize_tech_output(tech_output)
    return _validate_symbol_closure_canonical(tech, include_runtime_symbols=had_runtime)


def validate_asset_closure(tech_output: TechOutput | TechOutputV2 | dict) -> list[ContractValidationIssue]:
    tech, _, _ = _canonicalize_tech_output(tech_output)
    return _validate_asset_closure_canonical(tech)


def validate_asset_file_mapping(tech_output: TechOutput | TechOutputV2 | dict) -> list[ContractValidationIssue]:
    tech, _, _ = _canonicalize_tech_output(tech_output)
    return _validate_asset_file_mapping_canonical(tech)


def validate_scaffold_coverage(tech_output: TechOutput | TechOutputV2 | dict) -> list[ContractValidationIssue]:
    tech, _, _ = _canonicalize_tech_output(tech_output)
    return _validate_scaffold_coverage_canonical(tech)


def validate_build_profile(tech_output: TechOutput | TechOutputV2 | dict) -> list[ContractValidationIssue]:
    tech, _, had_runtime = _canonicalize_tech_output(tech_output)
    return _validate_build_profile_canonical(tech, had_runtime_contract=had_runtime)


def validate_contract(tech_output: TechOutput | TechOutputV2 | dict) -> ContractValidationOutput:
    tech, normalization_warnings, had_runtime = _canonicalize_tech_output(tech_output)

    file_issues = _validate_file_closure_canonical(tech)
    header_issues = _validate_header_closure_canonical(tech)
    symbol_issues = _validate_symbol_closure_canonical(tech, include_runtime_symbols=had_runtime)
    asset_issues = _validate_asset_closure_canonical(tech)
    asset_mapping_issues = _validate_asset_file_mapping_canonical(tech)
    coverage_issues = _validate_scaffold_coverage_canonical(tech)
    build_profile_issues = _validate_build_profile_canonical(tech, had_runtime_contract=had_runtime)

    validation_issues = (
        file_issues
        + header_issues
        + symbol_issues
        + asset_issues
        + asset_mapping_issues
        + coverage_issues
        + build_profile_issues
    )
    all_issues = normalization_warnings + validation_issues

    checks = {
        "file_closure": len(file_issues) == 0,
        "header_closure": len(header_issues) == 0,
        "symbol_closure": len(symbol_issues) == 0,
        "asset_closure": len(asset_issues) == 0,
        "asset_file_mapping": len(asset_mapping_issues) == 0,
        "scaffold_coverage": len(coverage_issues) == 0,
        "build_profile": len(build_profile_issues) == 0,
    }

    errors = [issue.message for issue in all_issues if issue.severity == "error"]
    warnings = [issue.message for issue in all_issues if issue.severity == "warning"]

    return ContractValidationOutput(
        status="pass" if not errors else "fail",
        issues=all_issues,
        checks=checks,
        errors=errors,
        warnings=warnings,
        out_of_scaffold_files=[issue.file for issue in file_issues if issue.file],
        missing_includes=[issue.message for issue in header_issues],
        missing_symbols=_dedupe_keep_order(
            [
                issue.symbol
                for issue in symbol_issues
                if issue.code in {"MISSING_REQUIRED_SYMBOL", "DECLARED_SYMBOL_NOT_DEFINED"} and issue.symbol
            ]
        ),
        duplicate_symbols=_dedupe_keep_order(
            [
                issue.symbol
                for issue in symbol_issues
                if issue.code in {"DUPLICATE_REQUIRED_SYMBOL", "MULTIPLE_SYMBOL_DEFINITION"} and issue.symbol
            ]
        ),
        missing_assets=_dedupe_keep_order(
            [issue.asset for issue in asset_issues + asset_mapping_issues if issue.asset]
        ),
        missing_required_files=_dedupe_keep_order([issue.file for issue in coverage_issues if issue.file]),
        build_profile_issues=[issue.message for issue in build_profile_issues],
    )
