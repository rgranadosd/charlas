"""Shared runtime configuration for CLI and service modes."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

DEBUG_MODE = False
TOKEN_CACHE_FILE = "token_cache.json"


def _bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _auth_trace_enabled() -> bool:
    if DEBUG_MODE:
        return True
    return _bool_env("WSO2_AUTH_TRACE", False)


def _thinking_enabled() -> bool:
    return _bool_env("AGENT_SHOW_THINKING", False)


@dataclass(frozen=True)
class RuntimeProfile:
    name: str
    env_file: Path


def _profile_file(profile: str) -> Path:
    base = Path(__file__).parent
    if profile == "service":
        return base / ".env.service"
    if profile == "cli":
        return base / ".env.cli"
    return base / ".env"


def get_runtime_profile(profile: str | None = None) -> RuntimeProfile:
    selected = (profile or os.getenv("AGENT_ENV_PROFILE") or "cli").strip().lower()
    env_file = _profile_file(selected)
    if not env_file.exists():
        env_file = Path(__file__).parent / ".env"
    return RuntimeProfile(name=selected, env_file=env_file)


def load_environment(env_file: str | Path | None = None) -> Path:
    env_path = Path(env_file) if env_file else Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv()
    return env_path


def load_profile(profile: str | None = None) -> RuntimeProfile:
    runtime = get_runtime_profile(profile)
    load_environment(runtime.env_file)
    return runtime
