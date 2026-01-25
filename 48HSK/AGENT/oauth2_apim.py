"""OAuth2 Client Credentials helper para WSO2 APIM.

Crea un cliente OpenAI (AsyncOpenAI) apuntando al Gateway APIM.
Pensado para entornos locales con certificados self-signed (https://localhost).
"""

from __future__ import annotations

import asyncio
import base64
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import httpx
import requests
import urllib3
from dotenv import load_dotenv
from openai import AsyncOpenAI

urllib3.disable_warnings()


@dataclass
class _TokenCache:
    token: Optional[str] = None
    expires_at: float = 0.0


_TOKEN_CACHE = _TokenCache()


def _is_localhost_url(url: str) -> bool:
    try:
        host = urlparse(url).hostname
    except Exception:
        host = None
    return host in {"localhost", "127.0.0.1"}


def _get_bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _load_env_if_present() -> None:
    env_file = Path(__file__).with_name(".env")
    if env_file.exists():
        load_dotenv(dotenv_path=env_file)
    else:
        load_dotenv()


def _fetch_oauth2_token_sync() -> tuple[str, int]:
    """Devuelve (access_token, expires_in_seconds)."""
    _load_env_if_present()

    consumer_key = os.getenv("WSO2_APIM_CONSUMER_KEY") or os.getenv("WSO2_CONSUMER_KEY")
    consumer_secret = os.getenv("WSO2_APIM_CONSUMER_SECRET") or os.getenv("WSO2_CONSUMER_SECRET")
    token_endpoint = (
        os.getenv("WSO2_APIM_TOKEN_ENDPOINT")
        or os.getenv("WSO2_TOKEN_ENDPOINT")
        or "https://localhost:9453/oauth2/token"
    )

    if not consumer_key or not consumer_secret:
        raise RuntimeError(
            "Falta WSO2_APIM_CONSUMER_KEY/WSO2_APIM_CONSUMER_SECRET (o WSO2_CONSUMER_KEY/WSO2_CONSUMER_SECRET) en .env"
        )

    verify_ssl_default = not _is_localhost_url(token_endpoint)
    verify_ssl = _get_bool_env("WSO2_TOKEN_VERIFY_SSL", verify_ssl_default)

    creds = f"{consumer_key}:{consumer_secret}"
    basic_auth = base64.b64encode(creds.encode()).decode()

    response = requests.post(
        token_endpoint,
        headers={
            "Authorization": f"Basic {basic_auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data="grant_type=client_credentials",
        verify=verify_ssl,
        timeout=15,
    )

    if response.status_code != 200:
        raise RuntimeError(f"Error OAuth2: {response.status_code} - {response.text}")

    token_data = response.json()
    access_token = token_data.get("access_token")
    if not access_token:
        raise RuntimeError("No se recibió access_token")

    expires_in = int(token_data.get("expires_in") or 3600)
    return access_token, expires_in


async def _get_oauth2_token_cached() -> str:
    # Reusar token si todavía es válido (con margen)
    now = time.time()
    if _TOKEN_CACHE.token and now < (_TOKEN_CACHE.expires_at - 30):
        return _TOKEN_CACHE.token

    token, expires_in = await asyncio.to_thread(_fetch_oauth2_token_sync)
    _TOKEN_CACHE.token = token
    _TOKEN_CACHE.expires_at = time.time() + max(0, expires_in)
    return token


def create_openai_client_with_gateway() -> Optional[AsyncOpenAI]:
    """Crea un cliente OpenAI AsyncOpenAI apuntando al Gateway APIM."""
    _load_env_if_present()

    gateway_base_url = (
        os.getenv("WSO2_OPENAI_API_URL")
        or os.getenv("OPENAI_BASE_URL")
        or "https://localhost:8253/openaiapi/2.3.0"
    )

    # Quitar /chat/completions si existe para obtener base_url
    gateway_base_url = gateway_base_url.rsplit("/chat/completions", 1)[0]

    verify_ssl_default = not _is_localhost_url(gateway_base_url)
    verify_ssl = _get_bool_env("WSO2_GATEWAY_VERIFY_SSL", verify_ssl_default)

    try:
        http_client = httpx.AsyncClient(verify=verify_ssl, timeout=httpx.Timeout(30.0))
        client = AsyncOpenAI(
            base_url=gateway_base_url,
            api_key=_get_oauth2_token_cached,
            http_client=http_client,
        )
        return client
    except Exception as e:
        print(f"⚠️  Error creando cliente Gateway: {e}")
        return None
