from __future__ import annotations

import os
import unittest
from unittest.mock import patch

import main as entrypoint


class MainDispatchTests(unittest.TestCase):
    def test_service_mode_dispatches_to_service_run(self) -> None:
        with patch.dict(os.environ, {"RUN_MODE": "service"}, clear=False):
            with patch("service.run") as run_service:
                entrypoint.main()

        run_service.assert_called_once_with()

    def test_cli_mode_dispatches_to_cli_main(self) -> None:
        with patch.dict(os.environ, {"RUN_MODE": "cli"}, clear=False):
            with patch("cli.main") as run_cli:
                entrypoint.main()

        run_cli.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
