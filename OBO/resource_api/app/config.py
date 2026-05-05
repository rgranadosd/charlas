from __future__ import annotations

import os
from pathlib import Path


def _as_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _resolve_repo_path(raw_path: str) -> Path:
    path = Path(raw_path).expanduser()
    if path.is_absolute():
        return path
    repo_root = Path(__file__).resolve().parents[2]
    return repo_root / path


class Settings:
    def __init__(self) -> None:
        self.app_name = os.getenv("APP_NAME", "WSO2 OBO Resource API")
        self.resource_api_host = os.getenv("RESOURCE_API_HOST", "0.0.0.0")
        self.resource_api_port = int(os.getenv("RESOURCE_API_PORT", "8001"))

        self.wso2_issuer = os.getenv("WSO2_ISSUER", "https://localhost:9443/oauth2/token")
        self.wso2_jwks_endpoint = os.getenv("WSO2_JWKS_ENDPOINT", "https://localhost:9443/oauth2/jwks")
        self.wso2_introspection_endpoint = os.getenv(
            "WSO2_INTROSPECTION_ENDPOINT", "https://localhost:9443/oauth2/introspect"
        )
        self.introspection_client_id = os.getenv("INTROSPECTION_CLIENT_ID", "admin")
        self.introspection_client_secret = os.getenv("INTROSPECTION_CLIENT_SECRET", "admin")
        self.expected_audience = os.getenv("EXPECTED_AUDIENCE", "")

        self.app_env = os.getenv("APP_ENV", "local").strip().lower()
        self.use_in_memory_demo_files = _as_bool(os.getenv("USE_IN_MEMORY_DEMO_FILES"), True)
        self.demo_files_json_path = _resolve_repo_path(
            os.getenv("DEMO_FILES_JSON_PATH", "dev-data/demo-files.json")
        )
        self.is_local_or_dev = self.app_env in {"local", "dev"}
        self.demo_files_enabled = self.is_local_or_dev and self.use_in_memory_demo_files


settings = Settings()