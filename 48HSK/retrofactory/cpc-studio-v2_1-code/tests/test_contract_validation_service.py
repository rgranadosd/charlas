import unittest

from app.services.contract_validation_service import validate_contract


MAIN_C_CONTENT = """#include \"game.h\"

int main(void) {
    game_init();
    while (1) {
        game_update();
        game_render();
    }
    return 0;
}
"""

GAME_H_CONTENT = """#ifndef GAME_H
#define GAME_H

void game_init(void);
void game_update(void);
void game_render(void);

#endif
"""

GAME_C_CONTENT = """#include \"game.h\"

void game_init(void) { }
void game_update(void) { }
void game_render(void) { }
"""


def _valid_payload() -> dict:
    return {
        "archetype": "action_platformer_run_and_gun",
        "video_mode": "Mode 1",
        "level_structure": "single_room",
        "camera": "locked",
        "modules": ["main", "game"],
        "input_model": {},
        "entity_model": {},
        "collision_model": {},
        "rendering_model": {},
        "data_model": {},
        "update_order": ["input", "logic", "render"],
        "runtime_contract": {
            "compile_profile": "playable_slice",
            "critical_modules": ["src/main.c", "src/game.c"],
            "integrated_modules": ["src/main.c", "src/game.c"],
            "required_entrypoints": ["game_init", "game_update", "game_render"],
            "main_loop_file": "src/main.c",
            "reject_empty_main_loop": True,
        },
        "module_contracts": [
            {
                "module": "src/main.c",
                "header": "",
                "local_includes": ["game.h"],
                "exports": [],
                "required_symbols": ["game_init", "game_update", "game_render"],
                "required_assets": [],
                "critical": True,
                "integrated": True,
                "allows_stub": False,
            },
            {
                "module": "src/game.c",
                "header": "src/game.h",
                "local_includes": ["game.h"],
                "exports": ["game_init", "game_update", "game_render"],
                "required_symbols": [],
                "required_assets": [],
                "critical": True,
                "integrated": True,
                "allows_stub": False,
            },
        ],
        "asset_contract": {
            "required_assets": ["tileset_main"],
            "declared_assets": ["tileset_main"],
            "defined_assets": ["tileset_main"],
        },
        "integration_blueprint": {
            "planned_files": ["src/main.c", "src/game.c", "src/game.h"],
            "provided_symbols": {
                "src/game.c": ["game_init", "game_update", "game_render"],
            },
            "required_symbols": {
                "src/main.c": ["game_init", "game_update", "game_render"],
            },
            "file_headers": {
                "src/main.c": ["game.h"],
                "src/game.c": ["game.h"],
            },
            "integrated_modules": ["src/main.c", "src/game.c"],
            "files": {
                "src/main.c": MAIN_C_CONTENT,
                "src/game.h": GAME_H_CONTENT,
                "src/game.c": GAME_C_CONTENT,
            },
        },
        "scaffold": {
            "required_files": ["src/main.c", "src/game.h", "src/game.c"],
            "base_scaffold_files": ["src/main.c"],
            "optional_files": [],
            "allowed_files": ["src/main.c", "src/game.h", "src/game.c"],
            "overwrite_files": ["src/main.c", "src/game.h", "src/game.c"],
            "create_if_missing": ["src/game.h", "src/game.c"],
        },
    }


class ContractValidationServiceTests(unittest.TestCase):
    def test_include_faltante(self):
        payload = _valid_payload()
        payload["module_contracts"].append(
            {
                "module": "src/systems/hud.c",
                "header": "src/systems/hud.h",
                "local_includes": ["hud_assets.h"],
                "exports": ["hud_render"],
                "required_symbols": [],
                "required_assets": [],
                "critical": False,
                "integrated": True,
                "allows_stub": False,
            }
        )
        payload["integration_blueprint"]["planned_files"].append("src/systems/hud.c")
        payload["scaffold"]["allowed_files"].extend(["src/systems/hud.c", "src/systems/hud.h"])

        result = validate_contract(payload)

        self.assertEqual(result.status, "fail")
        self.assertTrue(any("hud_assets.h" in item for item in result.missing_includes))

    def test_simbolo_duplicado(self):
        payload = _valid_payload()
        payload["module_contracts"].append(
            {
                "module": "src/entities/player.c",
                "header": "",
                "local_includes": [],
                "exports": ["game_update"],
                "required_symbols": [],
                "required_assets": [],
                "critical": False,
                "integrated": True,
                "allows_stub": False,
            }
        )
        payload["integration_blueprint"]["planned_files"].append("src/entities/player.c")
        payload["scaffold"]["allowed_files"].append("src/entities/player.c")

        result = validate_contract(payload)

        self.assertEqual(result.status, "fail")
        self.assertIn("game_update", result.duplicate_symbols)

    def test_asset_faltante(self):
        payload = _valid_payload()
        payload["asset_contract"] = {
            "required_assets": ["tileset_main", "hud_tiles"],
            "declared_assets": ["tileset_main"],
            "defined_assets": ["tileset_main"],
        }

        result = validate_contract(payload)

        self.assertEqual(result.status, "fail")
        self.assertIn("hud_tiles", result.missing_assets)

    def test_archivo_fuera_de_scaffold(self):
        payload = _valid_payload()
        payload["integration_blueprint"]["planned_files"].append("src/rogue/forbidden.c")

        result = validate_contract(payload)

        self.assertEqual(result.status, "fail")
        self.assertIn("src/rogue/forbidden.c", result.out_of_scaffold_files)

    def test_required_file_no_cubierto(self):
        payload = _valid_payload()
        payload["scaffold"]["required_files"].append("src/systems/collision.c")
        payload["scaffold"]["allowed_files"].append("src/systems/collision.c")

        result = validate_contract(payload)

        self.assertEqual(result.status, "fail")
        self.assertIn("src/systems/collision.c", result.missing_required_files)

    def test_caso_valido_completo(self):
        payload = _valid_payload()

        result = validate_contract(payload)

        self.assertEqual(result.status, "pass")
        self.assertEqual(result.errors, [])


if __name__ == "__main__":
    unittest.main()
