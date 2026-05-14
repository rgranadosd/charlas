import copy
import unittest

from app.services.contract_validation_service import validate_contract


def _valid_payload() -> dict:
    return {
        "scaffold": {
            "required_files": ["src/main.c", "src/game.c", "src/game.h"],
            "base_scaffold_files": ["src/game.h"],
            "allowed_files": [
                "src/main.c",
                "src/game.c",
                "src/game.h",
                "src/data/tileset/main.h",
            ],
            "create_if_missing": ["src/data/tileset/main.h"],
        },
        "runtime_contract": {
            "compile_profile": "playable_slice",
            "required_entrypoints": ["game_init", "game_update", "game_render"],
            "main_loop_file": "src/main.c",
            "reject_empty_main_loop": True,
        },
        "module_contracts": [
            {
                "module": "src/main.c",
                "local_includes": ["game.h"],
                "required_symbols": ["game_init", "game_update", "game_render"],
                "critical": True,
            },
            {
                "module": "src/game.c",
                "header": "src/game.h",
                "local_includes": ["game.h"],
                "exports": ["game_init", "game_update", "game_render"],
                "critical": True,
            },
        ],
        "asset_contract": {
            "required_assets": ["tileset_main"],
            "declared_assets": ["tileset_main"],
            "defined_assets": ["tileset_main"],
        },
        "integration_blueprint": {
            "planned_files": [
                "src/main.c",
                "src/game.c",
                "src/game.h",
                "src/data/tileset/main.h",
            ],
            "owned_files": [
                "src/main.c",
                "src/game.c",
                "src/game.h",
                "src/data/tileset/main.h",
            ],
            "asset_file_map": {
                "tileset_main": ["src/data/tileset/main.h"],
            },
            "files": {
                "src/main.c": (
                    '#include "game.h"\n'
                    'int main(void){ game_init(); while(1){ game_update(); game_render(); } }\n'
                ),
                "src/game.c": (
                    '#include "game.h"\n'
                    'void game_init(void){}\n'
                    'void game_update(void){}\n'
                    'void game_render(void){}\n'
                ),
                "src/data/tileset/main.h": (
                    '#ifndef DATA_TILESET_MAIN_H\n'
                    '#define DATA_TILESET_MAIN_H\n'
                    'extern const u8 tileset_main_data[];\n'
                    '#endif\n'
                ),
            },
        },
    }


def _issue_codes(result) -> set[str]:
    return {issue.code for issue in result.issues}


class ContractValidationServiceUnitTests(unittest.TestCase):
    def test_include_local_faltante_reporta_error(self):
        payload = copy.deepcopy(_valid_payload())
        payload["module_contracts"][0]["local_includes"] = ["missing_local.h"]
        payload["integration_blueprint"]["files"]["src/main.c"] = '#include "missing_local.h"\nint main(void){ game_init(); while(1){ game_update(); game_render(); } }\n'

        result = validate_contract(payload)

        self.assertEqual(result.status, "fail")
        self.assertGreater(len(result.issues), 0)
        self.assertIn("MISSING_LOCAL_INCLUDE", _issue_codes(result))

    def test_include_alias_por_guion_bajo_resuelve_header_generado(self):
        payload = copy.deepcopy(_valid_payload())

        payload["scaffold"]["allowed_files"].extend(
            [
                "src/systems/hud.c",
                "src/systems/hud.h",
                "src/data/assets/fontgothic.h",
            ]
        )
        payload["scaffold"]["create_if_missing"].extend(
            [
                "src/systems/hud.c",
                "src/systems/hud.h",
                "src/data/assets/fontgothic.h",
            ]
        )

        payload["integration_blueprint"]["planned_files"].extend(
            [
                "src/systems/hud.c",
                "src/systems/hud.h",
                "src/data/assets/fontgothic.h",
            ]
        )
        payload["integration_blueprint"]["owned_files"].extend(
            [
                "src/systems/hud.c",
                "src/systems/hud.h",
                "src/data/assets/fontgothic.h",
            ]
        )
        payload["integration_blueprint"]["asset_file_map"]["font_gothic"] = [
            "src/data/assets/fontgothic.h"
        ]

        payload["asset_contract"] = {
            "required_assets": ["tileset_main", "font_gothic"],
            "declared_assets": ["tileset_main", "font_gothic"],
            "defined_assets": ["tileset_main", "font_gothic"],
        }

        payload["module_contracts"].append(
            {
                "module": "src/systems/hud.c",
                "header": "src/systems/hud.h",
                "local_includes": ["font_gothic.h"],
                "required_assets": ["font_gothic"],
                "critical": False,
                "integrated": True,
            }
        )

        result = validate_contract(payload)

        self.assertEqual(result.status, "pass")
        self.assertNotIn("MISSING_LOCAL_INCLUDE", _issue_codes(result))

    def test_simbolo_requerido_no_exportado_reporta_error(self):
        payload = copy.deepcopy(_valid_payload())
        payload["module_contracts"][1]["exports"] = ["game_init", "game_update"]
        payload["integration_blueprint"]["files"]["src/game.c"] = (
            '#include "game.h"\n'
            'void game_init(void){}\n'
            'void game_update(void){}\n'
        )

        result = validate_contract(payload)

        self.assertEqual(result.status, "fail")
        self.assertGreater(len(result.issues), 0)
        self.assertIn("MISSING_REQUIRED_SYMBOL", _issue_codes(result))

    def test_simbolo_duplicado_exportado_por_dos_modulos_reporta_error(self):
        payload = copy.deepcopy(_valid_payload())
        payload["scaffold"]["allowed_files"].append("src/alt_game.c")
        payload["integration_blueprint"]["planned_files"].append("src/alt_game.c")
        payload["integration_blueprint"]["files"]["src/alt_game.c"] = "void game_update(void){}\n"
        payload["module_contracts"].append(
            {
                "module": "src/alt_game.c",
                "exports": ["game_update"],
                "critical": False,
            }
        )

        result = validate_contract(payload)

        self.assertEqual(result.status, "fail")
        self.assertGreater(len(result.issues), 0)
        self.assertIn("DUPLICATE_REQUIRED_SYMBOL", _issue_codes(result))

    def test_asset_faltante_reporta_error(self):
        payload = copy.deepcopy(_valid_payload())
        payload["asset_contract"] = {
            "required_assets": ["tileset_main", "hud_tiles"],
            "declared_assets": ["tileset_main"],
            "defined_assets": ["tileset_main"],
        }

        result = validate_contract(payload)

        self.assertEqual(result.status, "fail")
        self.assertGreater(len(result.issues), 0)
        codes = _issue_codes(result)
        self.assertIn("ASSET_NOT_DECLARED", codes)
        self.assertIn("ASSET_NOT_DEFINED", codes)

    def test_archivo_generado_fuera_allowed_files_reporta_error(self):
        payload = copy.deepcopy(_valid_payload())
        payload["integration_blueprint"]["planned_files"].append("src/rogue/forbidden.c")
        payload["integration_blueprint"]["files"]["src/rogue/forbidden.c"] = "int forbidden(void){ return 0; }\n"

        result = validate_contract(payload)

        self.assertEqual(result.status, "fail")
        self.assertGreater(len(result.issues), 0)
        self.assertIn("FILE_NOT_ALLOWED", _issue_codes(result))

    def test_required_file_no_cubierto_reporta_error(self):
        payload = copy.deepcopy(_valid_payload())
        payload["scaffold"]["required_files"].append("src/systems/hud.c")
        payload["scaffold"]["allowed_files"].append("src/systems/hud.c")

        result = validate_contract(payload)

        self.assertEqual(result.status, "fail")
        self.assertGreater(len(result.issues), 0)
        self.assertIn("REQUIRED_FILE_NOT_COVERED", _issue_codes(result))

    def test_caso_completamente_valido_pasa_sin_issues(self):
        payload = copy.deepcopy(_valid_payload())

        result = validate_contract(payload)

        self.assertEqual(result.status, "pass")
        self.assertEqual(result.issues, [])
        self.assertEqual(result.errors, [])

    def test_entrada_srcname_descriptiva_se_descarta_con_warning(self):
        payload = copy.deepcopy(_valid_payload())
        payload["integration_blueprint"]["planned_files"].append(
            "srcname srcdatalevel1.c, purpose define level data"
        )

        result = validate_contract(payload)

        warning_codes = {issue.code for issue in result.issues if issue.severity == "warning"}
        self.assertIn("NORMALIZATION_DROPPED_SRC_TOKEN", warning_codes)
        self.assertNotIn(
            "srcname srcdatalevel1.c, purpose define level data",
            result.out_of_scaffold_files,
        )

    def test_asset_descriptivo_largo_no_cuenta_como_asset_name(self):
        payload = copy.deepcopy(_valid_payload())
        payload["asset_contract"] = {
            "required_assets": [
                "hud sprite sheet for score and lives with detailed animation timing and notes"
            ],
            "declared_assets": [],
            "defined_assets": [],
        }

        result = validate_contract(payload)

        warning_codes = {issue.code for issue in result.issues if issue.severity == "warning"}
        self.assertIn("NORMALIZATION_DROPPED_ASSET_TOKEN", warning_codes)
        self.assertNotIn("ASSET_NOT_DECLARED", _issue_codes(result))
        self.assertNotIn("ASSET_NOT_DEFINED", _issue_codes(result))

    def test_include_concatenado_con_texto_no_pasa_como_include_valido(self):
        payload = copy.deepcopy(_valid_payload())
        payload["module_contracts"][0]["local_includes"] = [
            "game.h and this include is for main loop"
        ]

        result = validate_contract(payload)

        warning_codes = {issue.code for issue in result.issues if issue.severity == "warning"}
        self.assertIn("NORMALIZATION_DROPPED_INCLUDE_TOKEN", warning_codes)
        self.assertNotIn("MISSING_LOCAL_INCLUDE", _issue_codes(result))

    def test_deduplicacion_de_game_entrypoints(self):
        payload = copy.deepcopy(_valid_payload())
        payload["runtime_contract"]["required_entrypoints"] = [
            "game_init",
            "game_init",
            " game_update ",
            "game_update",
            "game_render",
            "game_render",
        ]

        result = validate_contract(payload)

        self.assertEqual(result.status, "pass")
        self.assertEqual(result.duplicate_symbols, [])

    def test_game_h_declara_y_game_c_define_es_valido(self):
        payload = copy.deepcopy(_valid_payload())
        payload["module_contracts"][1]["exports"] = []
        payload["module_contracts"][1]["declared_symbols"] = ["game_init", "game_update", "game_render"]
        payload["module_contracts"][1]["defined_symbols"] = ["game_init", "game_update", "game_render"]
        payload["integration_blueprint"]["provided_symbols"] = {
            "src/game.h": ["game_init", "game_update", "game_render"],
            "src/game.c": ["game_init", "game_update", "game_render"],
        }

        result = validate_contract(payload)

        self.assertEqual(result.status, "pass")
        self.assertNotIn("DUPLICATE_REQUIRED_SYMBOL", _issue_codes(result))
        self.assertNotIn("MULTIPLE_SYMBOL_DEFINITION", _issue_codes(result))

    def test_input_h_declara_y_input_c_define_es_valido(self):
        payload = copy.deepcopy(_valid_payload())
        payload["scaffold"]["allowed_files"].extend(["src/input.c", "src/input.h"])
        payload["integration_blueprint"]["planned_files"].extend(["src/input.c", "src/input.h"])
        payload["integration_blueprint"]["files"]["src/input.h"] = (
            "void input_init(void);\n"
            "void input_update(void);\n"
        )
        payload["integration_blueprint"]["files"]["src/input.c"] = (
            '#include "input.h"\n'
            "void input_init(void){}\n"
            "void input_update(void){}\n"
        )
        payload["module_contracts"][0]["required_symbols"].extend(["input_init", "input_update"])
        payload["module_contracts"].append(
            {
                "module": "src/input.c",
                "header": "src/input.h",
                "declared_symbols": ["input_init", "input_update"],
                "defined_symbols": ["input_init", "input_update"],
            }
        )

        result = validate_contract(payload)

        self.assertEqual(result.status, "pass")
        self.assertNotIn("MISSING_REQUIRED_SYMBOL", _issue_codes(result))

    def test_player_h_declara_y_dos_c_definen_reporta_error(self):
        payload = copy.deepcopy(_valid_payload())
        payload["scaffold"]["allowed_files"].extend(["src/player.c", "src/player_alt.c", "src/player.h"])
        payload["integration_blueprint"]["planned_files"].extend(["src/player.c", "src/player_alt.c", "src/player.h"])
        payload["integration_blueprint"]["files"]["src/player.h"] = "void player_init(void);\n"
        payload["integration_blueprint"]["files"]["src/player.c"] = "void player_init(void){}\n"
        payload["integration_blueprint"]["files"]["src/player_alt.c"] = "void player_init(void){}\n"
        payload["module_contracts"].append(
            {
                "module": "src/player.c",
                "header": "src/player.h",
                "declared_symbols": ["player_init"],
                "defined_symbols": ["player_init"],
            }
        )
        payload["module_contracts"].append(
            {
                "module": "src/player_alt.c",
                "defined_symbols": ["player_init"],
            }
        )

        result = validate_contract(payload)

        self.assertEqual(result.status, "fail")
        codes = _issue_codes(result)
        self.assertTrue(
            "MULTIPLE_SYMBOL_DEFINITION" in codes or "DUPLICATE_REQUIRED_SYMBOL" in codes
        )

    def test_collision_h_declara_pero_no_hay_definicion_reporta_error(self):
        payload = copy.deepcopy(_valid_payload())
        payload["module_contracts"].append(
            {
                "module": "src/collision.c",
                "header": "src/collision.h",
                "declared_symbols": ["collision_init"],
            }
        )

        result = validate_contract(payload)

        self.assertEqual(result.status, "fail")
        self.assertIn("DECLARED_SYMBOL_NOT_DEFINED", _issue_codes(result))
        self.assertIn("collision_init", result.missing_symbols)

    def test_asset_requerido_sin_planned_file_reporta_error(self):
        payload = copy.deepcopy(_valid_payload())
        payload["integration_blueprint"]["planned_files"].remove("src/data/tileset/main.h")

        result = validate_contract(payload)

        self.assertEqual(result.status, "fail")
        self.assertIn("REQUIRED_ASSET_MISSING_PLANNED_FILE", _issue_codes(result))

    def test_asset_planned_fuera_scaffold_reporta_error(self):
        payload = copy.deepcopy(_valid_payload())
        payload["integration_blueprint"]["asset_file_map"]["tileset_main"] = ["src/data/tileset/rogue.h"]
        payload["integration_blueprint"]["planned_files"].append("src/data/tileset/rogue.h")
        payload["integration_blueprint"]["owned_files"].append("src/data/tileset/rogue.h")

        result = validate_contract(payload)

        self.assertEqual(result.status, "fail")
        self.assertIn("REQUIRED_ASSET_OWNED_NOT_WRITABLE", _issue_codes(result))

    def test_asset_requerido_con_cadena_completa_pasa(self):
        payload = copy.deepcopy(_valid_payload())

        result = validate_contract(payload)

        self.assertEqual(result.status, "pass")
        self.assertNotIn("REQUIRED_ASSET_NO_WRITABLE_MAPPING", _issue_codes(result))


if __name__ == "__main__":
    unittest.main()
