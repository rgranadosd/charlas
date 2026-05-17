import json
import re
from pathlib import Path

from app.services.llm_service import json_call


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


def _project_snapshot(project_path: str | None) -> dict:
    if not project_path:
        return {"exists": False, "files": []}

    base = Path(project_path)
    if not base.exists():
        return {"exists": False, "files": []}

    files = []
    for path in sorted(base.rglob("*")):
        if not path.is_file():
            continue
        rel = str(path.relative_to(base)).replace("\\", "/")
        if rel.startswith("obj/"):
            continue
        files.append(rel)

    return {"exists": True, "files": files[:400]}


def _has_bootable_artifacts(project_path: str | None) -> bool:
    if not project_path:
        return False

    base = Path(project_path)
    if not base.exists() or not base.is_dir():
        return False

    dsk_exists = any(base.glob("*.dsk")) or any(base.glob("*.cdt"))
    required_obj = [
        base / "obj" / "binaryAddresses.log",
        *base.glob("obj/*.bin"),
        *base.glob("obj/*.map"),
        *base.glob("obj/*.noi"),
    ]

    has_binary_addresses = (base / "obj" / "binaryAddresses.log").exists()
    has_bin = any(base.glob("obj/*.bin"))
    has_map = any(base.glob("obj/*.map"))
    has_noi = any(base.glob("obj/*.noi"))

    return dsk_exists and has_binary_addresses and has_bin and has_map and has_noi


def _detect_runtime_placeholder_issues(project_path: str | None) -> tuple[list[str], list[str]]:
    if not project_path:
        return [], []

    base = Path(project_path)
    if not base.exists() or not base.is_dir():
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
            "Reject builds that ship generated asset arrays with only { 0x00 } placeholder data."
        )

    render_targets = [
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
            "Require sprite-backed rendering for player, enemies, projectiles, and HUD before marking build_validation as pass."
        )

    hud_path = base / "src" / "systems" / "hud.c"
    if hud_path.exists():
        hud_text = hud_path.read_text(encoding="utf-8", errors="ignore")
        if "_hud_dummy_sprite" in hud_text or "return _hud_dummy_sprite;" in hud_text:
            findings.append("HUD dummy sprite fallback detected in src/systems/hud.c")
            recommendations.append(
                "Reject HUD implementations that keep dummy digit/health sprites instead of real assets."
            )

    return findings, recommendations


def run(user_request: str, project_path: str | None, build_output=None) -> dict:
    build_payload = _build_output_dict(build_output)
    snapshot = _project_snapshot(project_path)

    extra_context = "\n\n".join(
        [
            "Project snapshot JSON:\n" + json.dumps(snapshot, ensure_ascii=False, indent=2),
            "Build output JSON:\n" + json.dumps(build_payload, ensure_ascii=False, indent=2),
        ]
    )

    validation_request = user_request or "Validate generated CPCtelera project coherence."
    payload = json_call("build_validation", validation_request, extra_context)

    status = str(payload.get("status", "fail")).strip().lower()
    if status not in {"pass", "fail"}:
        status = "fail"

    suspected_compile_errors = _as_list(payload.get("suspected_compile_errors"))
    fix_recommendations = _as_list(payload.get("fix_recommendations"))

    placeholder_findings, placeholder_fixes = _detect_runtime_placeholder_issues(project_path)
    if placeholder_findings:
        status = "fail"
        suspected_compile_errors.extend(placeholder_findings)
        fix_recommendations.extend(placeholder_fixes)
    elif _has_bootable_artifacts(project_path):
        status = "pass"

    return {
        "status": status,
        "missing_files": _as_list(payload.get("missing_files")),
        "invalid_paths": _as_list(payload.get("invalid_paths")),
        "header_source_mismatches": _as_list(payload.get("header_source_mismatches")),
        "suspected_compile_errors": suspected_compile_errors,
        "fix_recommendations": fix_recommendations,
    }
