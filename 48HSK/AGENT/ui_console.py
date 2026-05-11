"""Console-only UI helpers for the legacy interactive mode."""

from __future__ import annotations

import os
import shutil
import sys
import threading
import textwrap
import time
from typing import Optional

from banners import get_banner


class Colors:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    GRAY = "\033[90m"
    DARK_GREEN = "\033[32;2m"
    DIM = "\033[2m"
    RESET = "\033[0m"

    @staticmethod
    def blue(text):
        return f"{Colors.BLUE}{text}{Colors.RESET}"

    @staticmethod
    def debug(text):
        return f"{Colors.DARK_GREEN}[DEBUG] {text}{Colors.RESET}"

    @staticmethod
    def red(text):
        return f"{Colors.RED}[ERROR] {text}{Colors.RESET}"

    @staticmethod
    def green(text):
        return f"{Colors.GREEN}[OK] {text}{Colors.RESET}"

    @staticmethod
    def cyan(text):
        trimmed = text.lstrip()
        if trimmed.startswith("[DEBUG]") or trimmed.startswith("[API]"):
            return f"{Colors.DARK_GREEN}{text}{Colors.RESET}"
        return f"{Colors.CYAN}{text}{Colors.RESET}"

    @staticmethod
    def yellow(text):
        return f"{Colors.YELLOW}{text}{Colors.RESET}"

    @staticmethod
    def gray(text):
        return f"{Colors.DIM}{Colors.GRAY}{text}{Colors.RESET}"

    @staticmethod
    def dark_green(text):
        return f"{Colors.DARK_GREEN}{text}{Colors.RESET}"


APP_NAME = "Rafa’s Agent"
APP_VERSION = "v2.5 FINAL"


def _strip_ansi(text: str) -> str:
    import re

    return re.sub(r"\x1b\[[0-9;]*m", "", text)


def _safe_version(module_name: str) -> str:
    try:
        mod = __import__(module_name)
        return getattr(mod, "__version__", "?")
    except Exception:
        return "?"


def _wrap_plain_lines(lines: list[str], width: int) -> list[str]:
    wrapped: list[str] = []
    safe_width = max(1, width)
    for line in lines:
        parts = textwrap.wrap(
            line,
            width=safe_width,
            break_long_words=False,
            break_on_hyphens=False,
        )
        wrapped.extend(parts or [""])
    return wrapped


def print_start_motd(banner_name: str = "default") -> None:
    """Print ANSI MOTD with dynamic banners."""
    reset = "\033[0m"
    dim = "\033[2m"
    bold = "\033[1m"
    orange = "\033[38;5;208m"

    python_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    sk_ver = _safe_version("semantic_kernel")
    openai_ver = _safe_version("openai")
    httpx_ver = _safe_version("httpx")
    requests_ver = _safe_version("requests")

    info_values = [
        f"Python {python_ver}",
        f"semantic-kernel {sk_ver}",
        f"openai {openai_ver}",
        f"httpx {httpx_ver}",
        f"requests {requests_ver}",
        f"WSO2 IS {os.getenv('WSO2_AUTH_ENDPOINT', 'https://localhost:9443')}",
        f"WSO2 APIM {os.getenv('WSO2_APIM_TOKEN_ENDPOINT', 'https://localhost:9453')}",
    ]

    try:
        banner_data = get_banner(banner_name)
        big = banner_data["lines"]
        title = banner_data["title"]
    except Exception as exc:
        print(f"WARN: Error cargando banner '{banner_name}': {exc}")
        big = [f"{orange}{bold}(Banner no disponible){reset}"]
        title = f"{orange}{bold}{APP_NAME}{reset} {orange}{APP_VERSION}{reset}"

    line_prefix = "\r" if getattr(sys.stdout, "isatty", lambda: False)() else ""
    term_width = shutil.get_terminal_size((120, 20)).columns
    banner_width = max((len(_strip_ansi(line)) for line in big), default=0)
    title_width = len(_strip_ansi(title))
    divider_len = min(term_width, max(24, title_width, banner_width))
    format_info = lambda text: f"{orange}{text}{reset}"
    min_right_width = 24
    column_gap = 3
    use_two_columns = banner_width + column_gap + min_right_width <= term_width

    print("\n" + line_prefix + title)
    print(line_prefix + f"{orange}{dim}{'─' * divider_len}{reset}")

    if use_two_columns:
        right_width = max(min_right_width, term_width - banner_width - column_gap)
        info_lines = [format_info(line) for line in _wrap_plain_lines(info_values, right_width)]
        max_rows = max(len(big), len(info_lines))
        right_offset = max(0, max_rows - len(info_lines))
        for index in range(max_rows):
            left = big[index] if index < len(big) else ""
            right = info_lines[index - right_offset] if index >= right_offset and (index - right_offset) < len(info_lines) else ""
            pad = " " * max(0, banner_width - len(_strip_ansi(left)) + column_gap)
            print(line_prefix + f"{left}{pad}{right}")
    else:
        if banner_width <= term_width:
            for line in big:
                print(line_prefix + line)
        else:
            print(line_prefix + format_info(f"{APP_NAME} {APP_VERSION}"))

        print(line_prefix + f"{orange}{dim}{'─' * divider_len}{reset}")
        for line in _wrap_plain_lines(info_values, max(20, term_width - 2)):
            print(line_prefix + format_info(line))

    print(line_prefix + f"{orange}{dim}{'─' * divider_len}{reset}\n")


class ThinkingIndicator:
    """Non-blocking terminal thinking animation."""

    def __init__(self, message: str = "Thinking"):
        self.message = message
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.style = os.getenv("THINKING_STYLE", "dots")

    def start(self) -> None:
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._animate, daemon=True)
            self.thread.start()

    def stop(self) -> None:
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
        sys.stdout.write(f"\r{' ' * 80}\r")
        sys.stdout.flush()

    def _animate(self) -> None:
        index = 0
        if self.style == "spinner":
            chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        elif self.style == "pulse":
            chars = ["●    ", " ●   ", "  ●  ", "   ● ", "    ●", "   ● ", "  ●  ", " ●   "]
        elif self.style == "wave":
            chars = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
        else:
            chars = ["   ", ".  ", ".. ", "...", ".. ", ".  "]

        while self.running:
            sys.stdout.write(f"\r{Colors.cyan(self.message)} {Colors.yellow(chars[index % len(chars)])}")
            sys.stdout.flush()
            time.sleep(0.25)
            index += 1


__all__ = [
    "APP_NAME",
    "APP_VERSION",
    "Colors",
    "ThinkingIndicator",
    "_safe_version",
    "_strip_ansi",
    "print_start_motd",
]
