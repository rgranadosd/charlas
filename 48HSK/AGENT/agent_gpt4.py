"""Compatibility wrapper for the extracted Rafa agent modules."""

from __future__ import annotations

from banners import get_banner, list_available_banners
from cli import main
from config import TOKEN_CACHE_FILE, _auth_trace_enabled, _thinking_enabled, get_debug_mode, load_environment, load_profile, set_debug_mode
from oauth_session import OAuthCallbackHandler, OAuthClient, TokenStore
from orchestration import AgentRunner
from orchestration.agent_runner import _parse_percent_adjustment
from plugins import PriceMemory, ShopifyPlugin, WeatherPlugin
from ui_console import APP_NAME, APP_VERSION, Colors, ThinkingIndicator, _safe_version, _strip_ansi, print_start_motd

Agent = AgentRunner
DEBUG_MODE = False


def __getattr__(name: str):
    if name == "DEBUG_MODE":
        return get_debug_mode()
    raise AttributeError(name)


__all__ = [
    "APP_NAME",
    "APP_VERSION",
    "Agent",
    "AgentRunner",
    "Colors",
    "DEBUG_MODE",
    "OAuthCallbackHandler",
    "OAuthClient",
    "PriceMemory",
    "ShopifyPlugin",
    "TOKEN_CACHE_FILE",
    "ThinkingIndicator",
    "TokenStore",
    "WeatherPlugin",
    "_auth_trace_enabled",
    "_parse_percent_adjustment",
    "_safe_version",
    "_strip_ansi",
    "_thinking_enabled",
    "get_banner",
    "list_available_banners",
    "load_environment",
    "load_profile",
    "main",
    "print_start_motd",
    "set_debug_mode",
]


if __name__ == "__main__":
    main()
