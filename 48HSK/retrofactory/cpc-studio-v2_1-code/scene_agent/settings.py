from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    local_ai_mode: str = Field(default="mock")
    local_ai_base_url: str = Field(default="http://127.0.0.1:1234/v1/chat/completions")
    local_ai_model: str = Field(default="gemma-3-12b-it")

    workspace_root: str = Field(default_factory=lambda: str(Path.cwd()))
    cpctelera_root: str = Field(default="")
    caprice32_root: str = Field(default="")
    caprice32_executable: str = Field(default="", description="Ruta absoluta al ejecutable de Caprice32 (cap32 o wrapper)")
    run_emulator: bool = Field(default=False, description="Lanzar Caprice32 tras el build")
    projects_root: str = Field(default="")
    project_root: str = Field(default="")
    emulator_timeout_seconds: int = Field(default=10, ge=1, le=120)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


def resolve_project_name(settings: AppSettings) -> str:
    """Return the project name, falling back through: explicit field → root dir name → 'proyecto'."""
    explicit = getattr(settings, "project_name", None)
    if explicit:
        return explicit
    root = settings.project_root or "."
    name = Path(root).name
    return name or "proyecto"