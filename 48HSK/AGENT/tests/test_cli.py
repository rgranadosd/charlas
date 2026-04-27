from __future__ import annotations

import io
import os
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

import cli


class CliTests(unittest.TestCase):
    def test_list_banners_prints_available_banners(self) -> None:
        stdout = io.StringIO()
        with patch("sys.argv", ["cli.py", "--list-banners"]):
            with patch.object(cli, "list_available_banners", return_value=["default", "retro"]):
                with patch("sys.stdout", stdout):
                    cli.main()

        output = stdout.getvalue()
        self.assertIn("Banners disponibles:", output)
        self.assertIn("default", output)
        self.assertIn("retro", output)

    def test_cli_initializes_agent_and_exits_on_salir(self) -> None:
        fake_runtime = SimpleNamespace(weather_plugin=None)
        fake_agent = SimpleNamespace(initialize=Mock(), agent=fake_runtime)

        with patch.dict(os.environ, {}, clear=False):
            with patch("sys.argv", ["cli.py"]):
                with patch.object(cli, "load_profile") as load_profile:
                    with patch.object(cli, "print_start_motd"):
                        with patch.object(cli, "RafaAgent", return_value=fake_agent) as rafa_agent:
                            with patch("builtins.input", side_effect=["salir"]):
                                cli.main()

        load_profile.assert_called_once_with("cli")
        rafa_agent.assert_called_once()
        fake_agent.initialize.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
