"""CLI entrypoint that preserves the legacy terminal UX."""

from __future__ import annotations

import runpy
from pathlib import Path


def main() -> None:
    legacy_script = Path(__file__).with_name("agent_gpt4.py")
    runpy.run_path(str(legacy_script), run_name="__main__")


if __name__ == "__main__":
    main()
