import unittest

from app.services.c_codegen_service import (
    detect_c_generation_issues,
    render_c_array_decl,
    render_c_const_array,
    render_c_function_decl,
    render_c_function_def,
    render_c_include,
    render_c_struct,
)


class CCodegenServiceTests(unittest.TestCase):
    def test_player_enemy_projectile_structs_validos(self):
        player = render_c_struct("Player", [("u8", "x"), ("u8", "y"), ("u8", "health")])
        enemy = render_c_struct("Enemy", [("u8", "x"), ("u8", "y"), ("u8", "health")])
        projectile = render_c_struct("Projectile", [("u8", "x"), ("u8", "y"), ("u8", "speed")])

        self.assertEqual(player, "typedef struct {\n    u8 x;\n    u8 y;\n    u8 health;\n} Player;")
        self.assertTrue(enemy.endswith("} Enemy;"))
        self.assertTrue(projectile.endswith("} Projectile;"))

    def test_header_hud_con_parametros_escalares(self):
        decl = render_c_function_decl(
            "void",
            "hudUpdate",
            [("u8", "health"), ("u16", "score"), ("u8", "time"), ("u8", "lives")],
        )

        self.assertEqual(decl, "void hudUpdate(u8 health, u16 score, u8 time, u8 lives);")

    def test_funcion_sin_parametros_usa_void(self):
        decl = render_c_function_decl("void", "f", [])

        self.assertEqual(decl, "void f(void);")

    def test_funcion_con_multiples_parametros_tipados(self):
        definition = render_c_function_def(
            "void",
            "hudUpdate",
            [("u8", "health"), ("u16", "score"), ("u8", "time"), ("u8", "lives")],
            body_lines=["cpct_waitVSYNC();"],
        )

        self.assertIn("void hudUpdate(u8 health, u16 score, u8 time, u8 lives) {", definition)

    def test_header_y_source_usan_misma_firma(self):
        header = "\n".join(
            [
                render_c_include("game.h"),
                render_c_function_decl(
                    "void",
                    "hudUpdate",
                    [("u8", "health"), ("u16", "score"), ("u8", "time"), ("u8", "lives")],
                ),
                "",
            ]
        )
        source = "\n".join(
            [
                render_c_include("hud.h"),
                "",
                render_c_function_def(
                    "void",
                    "hudUpdate",
                    [("u8", "health"), ("u16", "score"), ("u8", "time"), ("u8", "lives")],
                    body_lines=[],
                ).rstrip(),
                "",
            ]
        )

        issues = detect_c_generation_issues(
            {
                "src/hud.h": header,
                "src/hud.c": source,
            }
        )

        self.assertEqual(issues, [])

    def test_level1tileproperties_array_global_valido(self):
        declaration = render_c_const_array("u8", "level1tileproperties", ["0x00", "0x01", "0x01", "0x00"])

        self.assertEqual(
            declaration,
            "const u8 level1tileproperties[] = { 0x00, 0x01, 0x01, 0x00 };",
        )

    def test_asset_header_extern_const_valido(self):
        declaration = render_c_array_decl(
            "u8",
            "sprplayerknight_data",
            None,
            qualifiers=["extern", "const"],
        )

        self.assertEqual(declaration, "extern const u8 sprplayerknight_data[];")

    def test_struct_no_dispara_falso_positivo_de_prototipo(self):
        header = "\n".join(
            [
                render_c_struct("Player", [("u8", "x"), ("u8", "y"), ("u8", "health")]),
                "",
            ]
        )

        issues = detect_c_generation_issues({"src/entities.h": header})

        self.assertFalse(any("without valid parentheses" in issue for issue in issues))

    def test_declaracion_multiple_variables_no_falso_positivo(self):
        source = "\n".join(
            [
                "void player_collision(void) {",
                "    u8 tile_x, tile_y, tile_w, tile_h;",
                "    tile_x = 0;",
                "}",
                "",
            ]
        )

        issues = detect_c_generation_issues({"src/entities/player.c": source})

        self.assertFalse(any("without valid parentheses" in issue for issue in issues))

    def test_prebuild_detecta_patrones_invalidos(self):
        issues = detect_c_generation_issues(
            {
                "src/systems/hud.h": "hudupdateu8 health, u16 score, u8 time, u8 lives;\n",
                "src/main.c": '#include "xyz.hinclude"\n',
            }
        )

        self.assertTrue(any("hudupdateu8" in issue.lower() for issue in issues))
        self.assertTrue(any(".hinclude" in issue for issue in issues))
        self.assertTrue(any("without valid parentheses" in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()