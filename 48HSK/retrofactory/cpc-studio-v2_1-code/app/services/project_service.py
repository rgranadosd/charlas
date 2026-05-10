from pathlib import Path
from app.services.file_service import write_text


def generate_project(base_dir: str, payload: dict) -> str:
    base = Path(base_dir)
    video_mode = payload.get("video_mode", "Mode 1")
    gameplay = payload.get("gameplay_spec", "")
    art_spec = payload.get("art_spec", "")
    tech_plan = payload.get("implementation_plan", "")

    write_text(base / "src" / "game.h", "#ifndef GAME_H\n#define GAME_H\n\nvoid game_init(void);\nvoid game_update(void);\nvoid game_render(void);\n\n#endif\n")
    write_text(base / "src" / "systems" / "input.h", "#ifndef INPUT_H\n#define INPUT_H\n\nvoid input_update(void);\n\n#endif\n")
    write_text(base / "src" / "entities" / "player.h", "#ifndef PLAYER_H\n#define PLAYER_H\n\nvoid player_init(void);\nvoid player_update(void);\nvoid player_render(void);\n\n#endif\n")
    write_text(base / "src" / "main.c", '#include "game.h"\n\nvoid main(void) {\n    game_init();\n    while (1) {\n        game_update();\n        game_render();\n    }\n}\n')
    write_text(base / "src" / "systems" / "input.c", '#include "input.h"\n\nvoid input_update(void) {\n    /* TODO: cpct_scanKeyboard_f() / joystick polling */\n}\n')
    write_text(base / "src" / "entities" / "player.c", '#include "player.h"\n\nvoid player_init(void) {\n}\n\nvoid player_update(void) {\n    /* TODO: smooth movement, collisions, bounds */\n}\n\nvoid player_render(void) {\n    /* TODO: draw sprite */\n}\n')
    scene = f'''#include "game.h"\n#include "systems/input.h"\n#include "entities/player.h"\n\n/* Auto-generated notes\nVideo mode: {video_mode}\n\nGameplay:\n{gameplay}\n\nArt:\n{art_spec}\n\nTech:\n{tech_plan}\n*/\n\nvoid game_init(void) {{\n    player_init();\n}}\n\nvoid game_update(void) {{\n    input_update();\n    player_update();\n}}\n\nvoid game_render(void) {{\n    player_render();\n}}\n'''
    write_text(base / "src" / "scene_game.c", scene)
    write_text(base / "README.md", f'# Generated Project\n\nRecommended video mode: {video_mode}\n')
    return str(base)
