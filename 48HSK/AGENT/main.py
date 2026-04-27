"""Unified process entrypoint with CLI and service run modes."""

from __future__ import annotations

import os


def main() -> None:
    run_mode = (os.getenv("RUN_MODE") or "cli").strip().lower()
    if run_mode == "service":
        from service import run as run_service

        run_service()
        return

    from cli import main as run_cli

    run_cli()


if __name__ == "__main__":
    main()
