from __future__ import annotations

import json
import os
from functools import lru_cache


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _as_list(value: str | None, default: list[str] | None = None) -> list[str]:
    if not value:
        return list(default or [])
    return [item.strip() for item in value.split(",") if item.strip()]


def _as_json_dict(value: str | None) -> dict[str, str]:
    if not value:
        return {}
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return {}
    if not isinstance(parsed, dict):
        return {}
    return {str(key): str(val) for key, val in parsed.items()}


def _require_str(value: str | None, env_name: str) -> str:
    if value is None:
        raise ValueError(f"{env_name} is required")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{env_name} is required")
    return normalized


class Settings:
    def __init__(self) -> None:
        self.app_name = os.getenv("APP_NAME", "WSO2 OBO Backend")
        self.backend_host = os.getenv("BACKEND_HOST", "0.0.0.0")
        self.backend_port = int(os.getenv("BACKEND_PORT", "8000"))
        self.frontend_origins = _as_list(os.getenv("FRONTEND_ORIGINS"), ["http://localhost:8091"])
        self.debug_show_full_tokens = _as_bool(os.getenv("DEBUG_SHOW_FULL_TOKENS"), False)

        self.wso2_issuer = os.getenv("WSO2_ISSUER", "https://localhost:9443/oauth2/token")
        self.wso2_authorize_endpoint = os.getenv(
            "WSO2_AUTHORIZE_ENDPOINT", "https://localhost:9443/oauth2/authorize"
        )
        self.wso2_token_endpoint = os.getenv("WSO2_TOKEN_ENDPOINT", "https://localhost:9443/oauth2/token")
        self.wso2_introspection_endpoint = os.getenv(
            "WSO2_INTROSPECTION_ENDPOINT", "https://localhost:9443/oauth2/introspect"
        )
        self.wso2_jwks_endpoint = os.getenv("WSO2_JWKS_ENDPOINT", "https://localhost:9443/oauth2/jwks")

        self.agent_client_id = os.getenv("AGENT_CLIENT_ID", "")
        self.agent_client_secret = os.getenv("AGENT_CLIENT_SECRET", "")
        self.agent_scope = os.getenv("AGENT_SCOPE", "openid profile files.read")
        self.agent_id = _require_str(os.getenv("AGENT_ID"), "AGENT_ID")
        self.introspection_client_id = os.getenv("INTROSPECTION_CLIENT_ID", self.agent_client_id)
        self.introspection_client_secret = os.getenv(
            "INTROSPECTION_CLIENT_SECRET", self.agent_client_secret
        )

        self.obo_client_id = os.getenv("OBO_CLIENT_ID", self.agent_client_id)
        self.obo_client_secret = os.getenv("OBO_CLIENT_SECRET", self.agent_client_secret)
        self.obo_redirect_uri = os.getenv("OBO_REDIRECT_URI", "http://localhost:8000/api/obo/callback")
        self.obo_scope = os.getenv(
            "OBO_SCOPE", "openid profile email files.read files.write files.share"
        )
        self.obo_grant_type = os.getenv("OBO_GRANT_TYPE", "authorization_code")
        self.obo_agent_token_parameter = os.getenv("OBO_AGENT_TOKEN_PARAMETER", "actor_token")
        self.obo_agent_token_type_parameter = os.getenv(
            "OBO_AGENT_TOKEN_TYPE_PARAMETER", "actor_token_type"
        )
        self.obo_agent_token_type_value = os.getenv(
            "OBO_AGENT_TOKEN_TYPE_VALUE", "urn:ietf:params:oauth:token-type:access_token"
        )
        self.obo_extra_token_params = _as_json_dict(os.getenv("OBO_EXTRA_TOKEN_PARAMS_JSON", "{}"))

        self.resource_api_base_url = os.getenv("RESOURCE_API_BASE_URL", "http://localhost:8001")
        self.resource_api_timeout_seconds = float(os.getenv("RESOURCE_API_TIMEOUT_SECONDS", "15"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
