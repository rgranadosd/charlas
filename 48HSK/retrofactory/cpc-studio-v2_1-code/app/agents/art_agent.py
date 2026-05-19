import json
import os
import sys

from app.agents.context_builder import build_agent_extra_context
from app.services.llm_service import json_call


def _as_list(value) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [str(value).strip()]


def _log(tag: str, message: str) -> None:
    sys.stderr.write(f"[{tag}] {message}\n")
    sys.stderr.flush()


def _as_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _art_runtime_config() -> dict[str, object]:
    return {
        "direction_text_model": os.getenv("ART_DIRECTION_TEXT_MODEL", "moonshotai/kimi-k2.6").strip(),
        "assets_text_model": os.getenv("ART_ASSETS_TEXT_MODEL", "moonshotai/kimi-k2.6").strip(),
        "assets_image_model": os.getenv("ART_ASSETS_IMAGE_MODEL", "black-forest-labs/flux.2-klein-4b").strip(),
        "assets_image_enabled": _as_bool(os.getenv("ART_ASSETS_IMAGE_ENABLED"), True),
        "constraints_text_model": os.getenv("ART_CONSTRAINTS_TEXT_MODEL", "moonshotai/kimi-k2.6").strip(),
    }


def _art_retrieval_limit() -> int:
    raw = os.getenv("ART_RETRIEVAL_LIMIT", "4").strip()
    try:
        return max(0, int(raw))
    except ValueError:
        return 4


def _phase_payload(label: str, payload: dict) -> str:
    return json.dumps({label: payload}, ensure_ascii=False, indent=2)


def _base_upstream_payloads(
    orchestrator_output: dict | None,
    narrative_output: dict | None,
    design_output: dict | None,
) -> dict[str, dict]:
    return {
        "orchestrator": orchestrator_output or {},
        "narrative": narrative_output or {},
        "design": design_output or {},
    }


def _art_direction_context(upstream_payloads: dict[str, dict], runtime_cfg: dict[str, object]) -> str:
    return "\n\n".join(
        [
            _phase_payload("upstream_payloads", upstream_payloads),
            _phase_payload(
                "art_phase",
                {
                    "name": "art_direction",
                    "text_model": runtime_cfg["direction_text_model"],
                    "focus": ["visual style", "palette strategy", "readability", "global coherence"],
                    "technical_retrieval": False,
                },
            ),
        ]
    )


def _art_assets_context(user_request: str, upstream_payloads: dict[str, dict], direction_output: dict, runtime_cfg: dict[str, object]) -> str:
    blocks = [
        build_agent_extra_context("art_agent", user_request, upstream_payloads, retrieval_limit=_art_retrieval_limit()),
        _phase_payload("art_direction", direction_output),
        _phase_payload(
            "art_phase",
            {
                "name": "art_assets",
                "text_model": runtime_cfg["assets_text_model"],
                "image_model": runtime_cfg["assets_image_model"],
                "image_enabled": runtime_cfg["assets_image_enabled"],
                "focus": ["tileset", "sprites", "hud", "asset inventory", "visual references"],
                "technical_retrieval": True,
            },
        ),
    ]
    return "\n\n".join(block for block in blocks if block)


def _art_constraints_context(
    user_request: str,
    upstream_payloads: dict[str, dict],
    direction_output: dict,
    assets_output: dict,
    visual_refs: dict,
    runtime_cfg: dict[str, object],
) -> str:
    blocks = [
        build_agent_extra_context("art_agent", user_request, upstream_payloads, retrieval_limit=_art_retrieval_limit()),
        _phase_payload("art_direction", direction_output),
        _phase_payload("art_assets", assets_output),
        _phase_payload("visual_refs", visual_refs),
        _phase_payload(
            "art_phase",
            {
                "name": "art_constraints",
                "text_model": runtime_cfg["constraints_text_model"],
                "focus": [
                    "CPC palette",
                    "sprite and tile sizes",
                    "transparency and masking",
                    "export and conversion hints",
                    "integration compatibility",
                ],
                "technical_retrieval": True,
            },
        ),
    ]
    return "\n\n".join(block for block in blocks if block)


def generate_visual_refs_for_assets(user_request: str, direction_output: dict, assets_output: dict, runtime_cfg: dict[str, object]) -> dict:
    asset_names = _as_list(assets_output.get("asset_list"))
    visual_prompts = _as_list(assets_output.get("visual_ref_prompts"))
    enabled = bool(runtime_cfg["assets_image_enabled"])
    image_model = str(runtime_cfg["assets_image_model"])

    references = []
    if enabled:
        prompt_bank = visual_prompts or [
            (
                f"Create a CPC reference concept for {asset}. "
                f"Style: {direction_output.get('palette_strategy', '')}. "
                f"Target video mode: {direction_output.get('video_mode_recommendation', '')}. "
                f"Gameplay request: {user_request}"
            ).strip()
            for asset in asset_names[:8]
        ]
        for index, prompt in enumerate(prompt_bank, start=1):
            asset = asset_names[index - 1] if index - 1 < len(asset_names) else f"visual_ref_{index}"
            references.append(
                {
                    "asset": asset,
                    "image_model": image_model,
                    "status": "stubbed",
                    "reference_prompt": prompt,
                    "backend": "not_configured",
                }
            )

    return {
        "image_enabled": enabled,
        "image_model": image_model,
        "status": "stubbed" if enabled else "disabled",
        "references": references,
    }


def _merge_outputs(direction_output: dict, assets_output: dict, constraints_output: dict) -> dict:
    return {
        "video_mode_recommendation": str(direction_output.get("video_mode_recommendation", "")).strip(),
        "palette_strategy": str(direction_output.get("palette_strategy", "")).strip(),
        "tileset_plan": _as_list(assets_output.get("tileset_plan")),
        "sprite_plan": _as_list(assets_output.get("sprite_plan")),
        "hud_plan": _as_list(assets_output.get("hud_plan")),
        "asset_list": _as_list(assets_output.get("asset_list")),
        "conversion_hints": _as_list(constraints_output.get("conversion_hints")),
    }


def run(
    user_request: str,
    orchestrator_output: dict | None = None,
    narrative_output: dict | None = None,
    design_output: dict | None = None,
) -> dict:
    upstream_payloads = _base_upstream_payloads(orchestrator_output, narrative_output, design_output)
    runtime_cfg = _art_runtime_config()

    _log(
        "ART",
        (
            "Modelos activos "
            f"dir={runtime_cfg['direction_text_model']} "
            f"assets_text={runtime_cfg['assets_text_model']} "
            f"assets_image={runtime_cfg['assets_image_model']} "
            f"constraints={runtime_cfg['constraints_text_model']}"
        ),
    )

    _log("ART_DIR", "Calculando dirección visual global")
    direction_output = json_call(
        "art_direction",
        user_request,
        _art_direction_context(upstream_payloads, runtime_cfg),
    )

    _log("ART_ASSETS", "Planificando assets y referencias visuales")
    assets_output = json_call(
        "art_assets",
        user_request,
        _art_assets_context(user_request, upstream_payloads, direction_output, runtime_cfg),
    )
    visual_refs = generate_visual_refs_for_assets(user_request, direction_output, assets_output, runtime_cfg)
    _log(
        "ART_ASSETS",
        f"Referencias visuales {visual_refs.get('status', 'unknown')} con modelo {runtime_cfg['assets_image_model']}",
    )

    _log("ART_CONSTRAINTS", "Traduciendo assets a restricciones técnicas CPC/CPCtelera")
    constraints_output = json_call(
        "art_constraints",
        user_request,
        _art_constraints_context(
            user_request,
            upstream_payloads,
            direction_output,
            assets_output,
            visual_refs,
            runtime_cfg,
        ),
    )

    final_output = _merge_outputs(direction_output, assets_output, constraints_output)
    _log("ART", "Plan de arte consolidado y compatible con ArtOutput")
    return final_output
