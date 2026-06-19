"""Orchestrator: prompt → plan → validate → emit → (mock) run."""
from __future__ import annotations

import json
import sys

from . import emitter, planner, runner, validator
from .schemas import AgentOutput, PromptInput


def _default_output_dir() -> str:
    import time
    return f"scene_agent/outputs/{time.strftime('%Y%m%d_%H%M%S')}"


def run_pipeline(
    prompt_text: str,
    output_dir: str | None = None,
) -> AgentOutput:
    if output_dir is None:
        output_dir = _default_output_dir()
    prompt = PromptInput(text=prompt_text)

    scene = planner.plan_scene(prompt)
    render_plan = planner.build_render_plan(scene)
    report = validator.validate(scene, render_plan)
    artifacts = emitter.emit(scene, render_plan, report, output_dir)
    simulation = runner.run(scene, render_plan)

    return AgentOutput(
        prompt=prompt,
        scene_spec=scene,
        render_plan=render_plan,
        validation_report=report,
        artifacts=artifacts,
        simulation=simulation,
    )


def main() -> int:
    prompt_text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else (
        "Créame una pantalla estilo Arkanoid con fondo azul, letras wso2 formadas por bloques, "
        "un marcador de puntos en la esquina superior derecha, una pala en la parte inferior "
        "y una pelota que rebote. La pala se controla horizontalmente con el teclado."
    )
    output = run_pipeline(prompt_text)
    print(json.dumps(output.model_dump(), indent=2, ensure_ascii=False))
    return 0 if output.validation_report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
