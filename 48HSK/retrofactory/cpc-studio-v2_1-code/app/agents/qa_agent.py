from app.agents.context_builder import build_agent_extra_context
from app.services.llm_service import json_call


def _as_list(value) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [str(value).strip()]


def _clip_text(value, limit: int = 1200) -> str:
    text = str(value or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n...[truncated]"


def _limit_list(values, limit: int = 12) -> list[str]:
    items = _as_list(values)
    if len(items) <= limit:
        return items
    return items[:limit] + [f"...[{len(items) - limit} more]"]


def _extract_snippet(text: str, anchors: list[str], limit: int = 500) -> str:
    source = str(text or "")
    if not source:
        return ""

    lower_source = source.lower()
    start = 0
    for anchor in anchors:
        pos = lower_source.find(anchor.lower())
        if pos != -1:
            start = pos
            break

    snippet = source[start:start + limit].strip()
    if start + limit < len(source):
        snippet += "\n...[truncated]"
    return snippet


def _build_gameplay_signals(files: dict) -> dict:
    files = files if isinstance(files, dict) else {}
    game_c = str(files.get("src/game.c", ""))
    main_c = str(files.get("src/main.c", ""))
    player_c = str(files.get("src/entities/player.c", ""))
    enemy_c = str(files.get("src/entities/enemy.c", ""))
    projectile_c = str(files.get("src/entities/projectile.c", ""))
    input_c = str(files.get("src/systems/input.c", ""))
    collision_c = str(files.get("src/systems/collision.c", ""))
    hud_c = str(files.get("src/systems/hud.c", ""))
    tilemap_c = str(files.get("src/systems/tilemap.c", ""))
    merged = "\n".join([game_c, main_c, player_c, enemy_c, projectile_c, input_c, collision_c, hud_c, tilemap_c]).lower()

    return {
        "game_loop_present": "while (1)" in main_c and "game_update" in main_c and "game_render" in main_c,
        "player_movement_present": "input_is_left_pressed" in player_c or "input_is_right_pressed" in player_c,
        "jump_present": "input_is_jump" in player_c,
        "shoot_present": "projectilefire" in game_c or "input_is_shoot" in game_c,
        "enemy_logic_present": "enemyspawn" in game_c and "enemyupdate" in game_c,
        "projectiles_present": "projectileupdate" in game_c or "projectilefire" in projectile_c,
        "collision_present": "collision_" in merged or "rect_overlap" in game_c,
        "tilemap_render_present": "tilemap_render" in game_c or "tilemap_render" in tilemap_c,
        "hud_present": "hudrender" in game_c or "hudrender" in hud_c,
        "win_loss_present": "g_victory" in game_c or "g_gameover" in game_c,
        "controls_mapping_present": "joy0_left" in input_c.lower() or "key_cursorleft" in input_c.lower(),
    }


def _build_key_file_snippets(files: dict) -> dict:
    files = files if isinstance(files, dict) else {}
    snippet_specs = {
        "src/main.c": ["while (1)", "game_init"],
        "src/game.c": ["void game_update", "void game_render", "spawn_wave", "g_victory"],
        "src/entities/player.c": ["void playerupdate", "input_is_jump", "input_is_left_pressed"],
        "src/entities/enemy.c": ["void enemyspawn", "void enemyupdate"],
        "src/entities/projectile.c": ["projectilefire", "projectileupdate"],
        "src/systems/input.c": ["void input_update", "joy0_left", "key_cursorleft"],
        "src/systems/collision.c": ["collision_"],
        "src/systems/hud.c": ["void hudrender", "void hudupdate"],
        "src/systems/tilemap.c": ["tilemap_render", "tilemap_goal_x", "tilemap_ground_y"],
    }

    snippets = {}
    for path, anchors in snippet_specs.items():
        content = files.get(path)
        if not content:
            continue
        snippet = _extract_snippet(str(content), anchors)
        if snippet:
            snippets[path] = snippet
    return snippets


def _summarize_integration_output(payload: dict | None) -> dict:
    payload = payload or {}
    files = payload.get("files") or {}
    file_names = []
    if isinstance(files, dict):
        file_names = sorted(str(path) for path in files.keys())

    return {
        "file_count": len(file_names),
        "file_names": file_names[:40] + ([f"...[{len(file_names) - 40} more]"] if len(file_names) > 40 else []),
        "gameplay_signals": _build_gameplay_signals(files),
        "key_file_snippets": _build_key_file_snippets(files),
        "assumptions": _limit_list(payload.get("assumptions"), limit=10),
        "integration_notes": _limit_list(payload.get("integration_notes"), limit=10),
        "manual_followups": _limit_list(payload.get("manual_followups"), limit=10),
        "prebuild_validation_errors": _limit_list(payload.get("prebuild_validation_errors"), limit=10),
    }


def _summarize_build_output(payload: dict | None) -> dict:
    payload = payload or {}
    return {
        "success": bool(payload.get("success")),
        "return_code": payload.get("return_code", -1),
        "artifacts": _limit_list(payload.get("artifacts"), limit=12),
        "project_path": str(payload.get("project_path", "") or ""),
        "build_notes": _clip_text(payload.get("build_notes", ""), limit=1200),
        "stderr_tail": _clip_text(payload.get("stderr", ""), limit=2000),
    }


def run(
    user_request: str,
    orchestrator_output: dict | None = None,
    design_output: dict | None = None,
    art_output: dict | None = None,
    tech_output: dict | None = None,
    integration_output: dict | None = None,
    build_validation_output: dict | None = None,
    build_output: dict | None = None,
) -> dict:
    if isinstance(build_validation_output, dict):
        validation_status = str(build_validation_output.get("status", "fail")).strip().lower()
        if validation_status == "fail":
            issues = _as_list(build_validation_output.get("suspected_compile_errors"))
            fixes = _as_list(build_validation_output.get("fix_recommendations"))
            return {
                "status": "fail",
                "playability_checks": [
                    "pipeline_gate: build_validation returned fail; QA approval short-circuited"
                ],
                "missing_gameplay_elements": issues,
                "usability_issues": issues,
                "next_iteration_goals": fixes,
            }

    extra_context = build_agent_extra_context(
        "qa_agent",
        user_request,
        {
            "orchestrator": orchestrator_output or {},
            "design": design_output or {},
            "art": art_output or {},
            "tech": tech_output or {},
            "integration": _summarize_integration_output(integration_output),
            "build_validation": build_validation_output or {},
            "build_output": _summarize_build_output(build_output),
        },
        retrieval_limit=6,
    )

    payload = json_call("qa", user_request, extra_context)
    status = str(payload.get("status", "fail")).strip().lower()
    if status not in {"pass", "fail"}:
        status = "fail"

    return {
        "status": status,
        "playability_checks": _as_list(payload.get("playability_checks")),
        "missing_gameplay_elements": _as_list(payload.get("missing_gameplay_elements")),
        "usability_issues": _as_list(payload.get("usability_issues")),
        "next_iteration_goals": _as_list(payload.get("next_iteration_goals")),
    }
