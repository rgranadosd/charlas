import json

from app.services.llm_service import json_call

MAIN_C_PATH = "src/main.c"
GAME_H_PATH = "src/game.h"
GAME_C_PATH = "src/game.c"

GAME_H_STUB = """#ifndef GAME_H
#define GAME_H

void game_init(void);
void game_update(void);
void game_render(void);

#endif
"""

GAME_C_STUB = """#include "game.h"
#include <cpctelera.h>

void game_init(void) {
    cpct_disableFirmware();
    cpct_setVideoMode(1);
    cpct_clearScreen(0x00);
}

void game_update(void) {
}

void game_render(void) {
}
"""

MAIN_C_STUB = """#include <cpctelera.h>
#include "game.h"

int main(void) {
    game_init();

    while (1) {
        game_update();
        game_render();
        cpct_waitVSYNC();
    }

    return 0;
}
"""


def _normalize_files(payload: dict, allowed_files: set[str]) -> dict[str, str]:
    raw_files = payload.get("files")
    if not isinstance(raw_files, dict):
        return {}

    normalized: dict[str, str] = {}
    for path, content in raw_files.items():
        if not isinstance(path, str):
            continue
        rel_path = path.strip().replace("\\", "/")
        if not rel_path.startswith("src/"):
            continue
        if allowed_files and rel_path not in allowed_files:
            continue
        normalized[rel_path] = str(content)

    return normalized


def _is_allowed(path: str, allowed_files: set[str]) -> bool:
    return not allowed_files or path in allowed_files


def _ensure_core_game_module(files: dict[str, str], allowed_files: set[str]) -> dict[str, str]:
    normalized = dict(files)

    if _is_allowed(GAME_H_PATH, allowed_files):
        normalized[GAME_H_PATH] = GAME_H_STUB

    if _is_allowed(GAME_C_PATH, allowed_files):
        normalized[GAME_C_PATH] = GAME_C_STUB

    if _is_allowed(MAIN_C_PATH, allowed_files):
        normalized[MAIN_C_PATH] = MAIN_C_STUB

    # scene_game is no longer the central game loop module.
    normalized.pop("src/scene_game.c", None)

    return normalized


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

    scaffold = tech_output.get("scaffold", {}) if isinstance(tech_output, dict) else {}
    allowed_files = set(scaffold.get("allowed_files", [])) if isinstance(scaffold, dict) else set()
    files = _normalize_files(payload, allowed_files)
    files = _ensure_core_game_module(files, allowed_files)

    if not files:
        return {
            "files": {},
            "integration_notes": "CodeIntegratorAgent returned no valid scaffold files.",
        }

    return {
        "files": files,
        "integration_notes": f"Generated {len(files)} valid source files.",
    }
