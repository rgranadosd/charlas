import re
from pathlib import Path


CRITICAL_SCAFFOLD_FILES = [
    "src/main.c",
    "cfg/build_config.mk",
    "Makefile",
]

EXPECTED_ARTIFACT_PATTERNS = [
    "*.dsk",
    "*.cdt",
    "obj/binaryAddresses.log",
    "obj/*.bin",
    "obj/*.map",
    "obj/*.noi",
]

# Valid CPC hardware ink byte values accepted by cpct_setPalette.
# Source: cpctelera/cpct_firmware2hw_colour_table.s (+ 0x40 hardware bitfield)
CPC_HW_COLOR_VALUES = {
    0x54, 0x44, 0x55, 0x5C, 0x58, 0x5D, 0x4C, 0x45, 0x4D,
    0x56, 0x46, 0x57, 0x5E, 0x40, 0x5F, 0x4E, 0x47, 0x4F,
    0x52, 0x42, 0x53, 0x5A, 0x59, 0x5B, 0x4A, 0x43, 0x4B,
}


def _as_list(value) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [str(value).strip()]


def _build_output_dict(build_output) -> dict:
    if build_output is None:
        return {}
    if isinstance(build_output, dict):
        return build_output
    if hasattr(build_output, "model_dump"):
        return build_output.model_dump()
    return {}


def _project_base(project_path: str | None, build_payload: dict) -> Path | None:
    raw_path = str(build_payload.get("project_path") or project_path or "").strip()
    if not raw_path:
        return None
    return Path(raw_path)


def _is_valid_cpct_scaffold(base: Path | None) -> bool:
    if base is None:
        return False
    return (
        base.exists()
        and base.is_dir()
        and (base / "src").is_dir()
        and (base / "src" / "main.c").is_file()
        and (base / "cfg").is_dir()
        and (base / "cfg" / "build_config.mk").is_file()
        and (base / "Makefile").is_file()
    )


def _missing_scaffold_files(base: Path | None) -> list[str]:
    if base is None:
        return list(CRITICAL_SCAFFOLD_FILES)
    missing = []
    for rel_path in CRITICAL_SCAFFOLD_FILES:
        if not (base / rel_path).exists():
            missing.append(rel_path)
    return missing


def _collect_found_artifacts(base: Path | None, build_payload: dict) -> list[str]:
    found = {
        path.replace("\\", "/")
        for path in _as_list(build_payload.get("artifacts"))
    }
    if base is None or not base.exists():
        return sorted(found)

    for pattern in EXPECTED_ARTIFACT_PATTERNS:
        for path in base.glob(pattern):
            if path.is_file():
                found.add(str(path.relative_to(base)).replace("\\", "/"))
    return sorted(found)


def _missing_expected_artifacts(found_artifacts: list[str]) -> list[str]:
    found_set = set(found_artifacts)
    missing: list[str] = []

    if not any(path.endswith(".dsk") for path in found_set):
        missing.append("*.dsk")
    if not any(path.endswith(".cdt") for path in found_set):
        missing.append("*.cdt")
    if "obj/binaryAddresses.log" not in found_set:
        missing.append("obj/binaryAddresses.log")
    if not any(path.startswith("obj/") and path.endswith(".bin") for path in found_set):
        missing.append("obj/*.bin")
    if not any(path.startswith("obj/") and path.endswith(".map") for path in found_set):
        missing.append("obj/*.map")
    if not any(path.startswith("obj/") and path.endswith(".noi") for path in found_set):
        missing.append("obj/*.noi")

    return missing


def _invalid_artifact_paths(base: Path | None, artifacts: list[str]) -> list[str]:
    invalid: list[str] = []
    for rel_path in artifacts:
        if rel_path.startswith("/") or rel_path.startswith("../") or "/../" in f"/{rel_path}/":
            invalid.append(rel_path)
            continue
        if base is None:
            continue
        candidate = (base / rel_path).resolve()
        base_resolved = base.resolve()
        if candidate != base_resolved and base_resolved not in candidate.parents:
            invalid.append(rel_path)
    return sorted(set(invalid))


def _header_source_mismatches(base: Path | None) -> list[str]:
    if base is None or not base.exists():
        return []

    mismatches: list[str] = []
    for header in sorted((base / "src").rglob("*.h")):
        rel_header = str(header.relative_to(base)).replace("\\", "/")
        source = header.with_suffix(".c")
        asm_source = header.with_suffix(".s")
        asm_upper = header.with_suffix(".asm")
        if source.exists() or asm_source.exists() or asm_upper.exists():
            continue
        if "/data/" in rel_header:
            continue
        mismatches.append(rel_header)
    return mismatches


def _detect_runtime_placeholder_issues(base: Path | None) -> tuple[list[str], list[str]]:
    if base is None or not base.exists() or not base.is_dir():
        return [], []

    findings: list[str] = []
    recommendations: list[str] = []

    placeholder_asset_re = re.compile(
        r"const\s+u8\s+[A-Za-z_][A-Za-z0-9_]*\s*\[\]\s*=\s*\{\s*0x00\s*\};"
    )
    solid_box_re = re.compile(r"cpct_drawSolidBox\s*\(")

    asset_roots = [
        base / "src" / "data" / "assets",
        base / "src" / "data" / "hud",
        base / "src" / "data" / "sprites",
        base / "src" / "data" / "tileset",
    ]

    placeholder_assets: list[str] = []
    for root in asset_roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.c")):
            text = path.read_text(encoding="utf-8", errors="ignore")
            if placeholder_asset_re.search(text):
                placeholder_assets.append(str(path.relative_to(base)).replace("\\", "/"))

    if placeholder_assets:
        preview = ", ".join(placeholder_assets[:6])
        findings.append(
            "Placeholder asset data detected in generated sources: "
            f"{preview}{' ...' if len(placeholder_assets) > 6 else ''}"
        )
        recommendations.append(
            "Replace placeholder asset arrays before accepting the build as valid."
        )

    render_targets = [
        (base / "src" / "game.c", "game_render"),
        (base / "src" / "entities" / "player.c", "playerrender"),
        (base / "src" / "entities" / "enemy.c", "enemyrender"),
        (base / "src" / "entities" / "projectile.c", "projectilerender"),
        (base / "src" / "systems" / "hud.c", "hudrender"),
    ]
    solid_box_renderers: list[str] = []
    for path, symbol in render_targets:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if symbol in text and solid_box_re.search(text):
            solid_box_renderers.append(str(path.relative_to(base)).replace("\\", "/"))

    if solid_box_renderers:
        preview = ", ".join(solid_box_renderers)
        findings.append(
            "Placeholder renderer detected using cpct_drawSolidBox in runtime render paths: "
            f"{preview}"
        )
        recommendations.append(
            "Replace placeholder solid-box renderers with sprite-backed rendering for gameplay entities and HUD."
        )

    game_path = base / "src" / "game.c"
    if game_path.exists():
        game_text = game_path.read_text(encoding="utf-8", errors="ignore")
        game_solid_boxes = len(re.findall(r"cpct_drawSolidBox\s*\(", game_text))
        game_sprite_calls = len(re.findall(r"cpct_drawSprite\s*\(", game_text))
        game_entity_render_calls = len(
            re.findall(r"\b(playerrender|enemyrender|projectilerender|tilemap_render)\s*\(", game_text)
        )
        # Heuristic: a gameplay loop that mostly paints debug/fallback boxes is not a playable visual slice.
        if game_solid_boxes >= 8 and game_sprite_calls == 0 and game_entity_render_calls <= 1:
            findings.append(
                "Runtime renderer in src/game.c appears to be placeholder-heavy "
                f"(solid_boxes={game_solid_boxes}, sprite_calls={game_sprite_calls}, entity_render_calls={game_entity_render_calls})."
            )
            recommendations.append(
                "Require sprite-backed rendering (direct cpct_drawSprite or entity render functions) before accepting validation pass."
            )

    level1_path = base / "src" / "data" / "level1.c"
    if level1_path.exists():
        level1_text = level1_path.read_text(encoding="utf-8", errors="ignore")
        tilemap_match = re.search(r"level1tilemap\s*\[\]\s*=\s*\{([^}]*)\}", level1_text, re.DOTALL)
        if tilemap_match:
            tokens = [tok.strip() for tok in tilemap_match.group(1).split(",") if tok.strip()]
            if len(tokens) <= 40:
                findings.append(
                    "level1 tilemap data is trivially small "
                    f"({len(tokens)} entries), suggesting placeholder layout rather than a visible scene."
                )
                recommendations.append(
                    "Generate a non-trivial tilemap (e.g., full 20x18 coverage) to ensure readable on-screen gameplay composition."
                )

    hud_path = base / "src" / "systems" / "hud.c"
    if hud_path.exists():
        hud_text = hud_path.read_text(encoding="utf-8", errors="ignore")
        if "_hud_dummy_sprite" in hud_text or "return _hud_dummy_sprite;" in hud_text:
            findings.append("HUD dummy sprite fallback detected in src/systems/hud.c")
            recommendations.append("Remove HUD dummy sprite fallbacks before marking validation as pass.")

    return findings, recommendations


def _detect_palette_sanity_issues(base: Path | None) -> tuple[list[str], list[str]]:
    if base is None or not base.exists() or not base.is_dir():
        return [], []

    findings: list[str] = []
    recommendations: list[str] = []

    palette_file = base / "src" / "data" / "level1.c"
    if not palette_file.exists():
        return findings, recommendations

    text = palette_file.read_text(encoding="utf-8", errors="ignore")
    palette_match = re.search(r"gpalette\s*\[[^\]]*\]\s*=\s*\{([^}]*)\}", text, re.DOTALL)
    if not palette_match:
        return findings, recommendations

    raw_values = [token.strip() for token in palette_match.group(1).split(",") if token.strip()]
    parsed_values: list[int] = []
    for token in raw_values:
        token = token.split("/")[0].strip()
        if not token:
            continue
        try:
            parsed_values.append(int(token, 0))
        except ValueError:
            continue

    invalid_values = [value for value in parsed_values if value not in CPC_HW_COLOR_VALUES]
    if invalid_values:
        findings.append(
            "Invalid CPC hardware palette values detected in src/data/level1.c: "
            + ", ".join(str(value) for value in sorted(set(invalid_values)))
            + "."
        )
        recommendations.append(
            "Remap gpalette values to valid CPC hardware ink codes before shipping the build."
        )

    return findings, recommendations


def _build_error_findings(build_payload: dict) -> list[str]:
    if build_payload.get("success"):
        return []

    stderr = str(build_payload.get("stderr") or "").strip()
    stdout = str(build_payload.get("stdout") or "").strip()
    findings: list[str] = []

    if stderr:
        findings.extend(line.strip() for line in stderr.splitlines()[-12:] if line.strip())
    elif stdout:
        findings.extend(line.strip() for line in stdout.splitlines()[-8:] if line.strip())
    else:
        findings.append("Build failed without stderr/stdout details.")

    return findings[:12]


def run(user_request: str, project_path: str | None, build_output=None) -> dict:
    del user_request

    build_payload = _build_output_dict(build_output)
    base = _project_base(project_path, build_payload)
    project_path_str = str(base.resolve()) if base and base.exists() else str(base or "")

    scaffold_valid = _is_valid_cpct_scaffold(base)
    missing_scaffold = _missing_scaffold_files(base)
    found_artifacts = _collect_found_artifacts(base, build_payload)
    missing_artifacts = _missing_expected_artifacts(found_artifacts)
    invalid_paths = _invalid_artifact_paths(base, found_artifacts)
    header_source_mismatches = _header_source_mismatches(base)
    placeholder_findings, placeholder_recommendations = _detect_runtime_placeholder_issues(base)
    palette_findings, palette_recommendations = _detect_palette_sanity_issues(base)
    build_error_findings = _build_error_findings(build_payload)

    suspected_compile_errors = build_error_findings + placeholder_findings + palette_findings
    fix_recommendations: list[str] = []
    validation_notes: list[str] = []

    build_succeeded = bool(build_payload.get("success"))
    if scaffold_valid:
        validation_notes.append("Valid CPCtelera scaffold detected.")
    else:
        validation_notes.append("Invalid or missing CPCtelera scaffold.")

    if build_succeeded:
        validation_notes.append("Build output reports success.")
    else:
        validation_notes.append(
            f"Build output reports failure with return_code={build_payload.get('return_code', -1)}."
        )

    if missing_scaffold:
        fix_recommendations.append(
            "Restore required CPCtelera scaffold files: " + ", ".join(missing_scaffold)
        )
    if missing_artifacts:
        fix_recommendations.append(
            "Produce expected build artifacts: " + ", ".join(missing_artifacts)
        )
    if invalid_paths:
        fix_recommendations.append(
            "Remove invalid artifact paths outside the generated project root."
        )
    if header_source_mismatches:
        fix_recommendations.append(
            "Align header/source pairs for gameplay modules before next build."
        )
    fix_recommendations.extend(placeholder_recommendations)
    fix_recommendations.extend(palette_recommendations)

    missing_files = missing_scaffold + missing_artifacts
    status = "pass"
    if (
        not scaffold_valid
        or not build_succeeded
        or missing_files
        or invalid_paths
        or header_source_mismatches
        or suspected_compile_errors
    ):
        status = "fail"

    return {
        "status": status,
        "scaffold_valid": scaffold_valid,
        "build_succeeded": build_succeeded,
        "project_path": project_path_str,
        "expected_artifacts": list(EXPECTED_ARTIFACT_PATTERNS),
        "found_artifacts": found_artifacts,
        "missing_files": missing_files,
        "invalid_paths": invalid_paths,
        "header_source_mismatches": header_source_mismatches,
        "suspected_compile_errors": suspected_compile_errors,
        "fix_recommendations": list(dict.fromkeys(fix_recommendations)),
        "validation_notes": validation_notes,
    }
