"""Emit JSON artifacts for a validated scene."""
from __future__ import annotations

import json
from pathlib import Path

from .schemas import RenderPlan, SceneSpec, ValidationReport


def emit(
    scene: SceneSpec,
    render_plan: RenderPlan,
    report: ValidationReport,
    output_dir: str = "scene_agent/outputs",
) -> dict[str, str]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    paths: dict[str, str] = {}
    files = {
        "scene_spec.json": scene.model_dump(),
        "render_plan.json": render_plan.model_dump(),
        "validation_report.json": report.model_dump(),
    }
    for filename, data in files.items():
        p = out / filename
        p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        paths[filename] = str(p)

    return paths
