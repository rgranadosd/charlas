from pathlib import Path
from app.services.file_service import write_text


def generate_project(base_dir: str, payload: dict) -> str:
    base = Path(base_dir)
    video_mode = payload.get("video_mode", "Mode 1")
    gameplay = payload.get("gameplay_spec", "")
    art_spec = payload.get("art_spec", "")
    tech_plan = payload.get("implementation_plan", "")

    write_text(base / "src" / "game.h", """#ifndef GAME_H
#define GAME_H

void game_init(void);
void game_update(void);
void game_render(void);

#endif
""")

    write_text(base / "src" / "systems" / "input.h", """#ifndef INPUT_H
#define INPUT_H

void input_update(void);

#endif
""")

    write_text(base / "src" / "entities" / "player.h", """#ifndef PLAYER_H
#define PLAYER_H

void player_init(void);
void player_update(void);
void player_render(void);

#endif
""")

    write_text(base / "src" / "main.c", """#include <cpctelera.h>
#include "game.h"

void main(void) {
    game_init();

    while (1) {
        game_update();
        game_render();
        cpct_waitVSYNC();
    }
}
""")

    write_text(base / "src" / "systems" / "input.c", """#include <cpctelera.h>
#include "input.h"

void input_update(void) {
    cpct_scanKeyboard_f();
}
""")

    write_text(base / "src" / "entities" / "player.c", """#include <cpctelera.h>
#include "player.h"

static u8 px;
static u8 py;

void player_init(void) {
    px = 20;
    py = 80;
}

void player_update(void) {
    if (cpct_isKeyPressed(Key_CursorLeft) && px > 0)
        px -= 2;

    if (cpct_isKeyPressed(Key_CursorRight) && px < 70)
        px += 2;
}

void player_render(void) {
    u8* pvmem;

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, py);
    cpct_drawSolidBox(pvmem, 0x00, 80, 8);

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, px, py);
    cpct_drawSolidBox(pvmem, 0xF0, 4, 8);
}
""")

    scene = f"""#include <cpctelera.h>
#include "game.h"
#include "systems/input.h"
#include "entities/player.h"

/* Auto-generated notes
Video mode: {video_mode}

Gameplay:
{gameplay}

Art:
{art_spec}

Tech:
{tech_plan}
*/

void game_init(void) {{
    cpct_disableFirmware();
    cpct_setVideoMode(1);
    cpct_clearScreen(0x00);
    player_init();
}}

void game_update(void) {{
    input_update();
    player_update();
}}

void game_render(void) {{
    player_render();
}}
"""
    write_text(base / "src" / "scene_game.c", scene)

    write_text(base / "README.md", f"""# Generated Project

Recommended video mode: {video_mode}
""")

    return str(base)
