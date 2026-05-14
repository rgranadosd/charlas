from __future__ import annotations

import base64
from typing import Any
from urllib.parse import urlencode

import httpx

from app.config import get_settings


class OAuthService:
    TOKEN_EXCHANGE_GRANT = "urn:ietf:params:oauth:grant-type:token-exchange"

    def __init__(self) -> None:
        self.settings = get_settings()

    def _basic_auth_header(self, client_id: str, client_secret: str) -> dict[str, str]:
        token = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("ascii")
        return {"Authorization": f"Basic {token}"}

    def build_authorization_url(self, *, state: str, code_challenge: str, scopes: list[str]) -> str:
        params = {
            "response_type": "code",
            "client_id": self.settings.obo_client_id,
            "redirect_uri": self.settings.obo_redirect_uri,
            "scope": " ".join(scopes),
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }
        prompt = self.settings.obo_authorization_prompt.strip()
        if prompt:
            params["prompt"] = prompt
        query = urlencode(params)
        return f"{self.settings.wso2_authorize_endpoint}?{query}"

    async def request_client_credentials_token(
        self, *, client_id: str, client_secret: str, scope: str
    ) -> dict[str, Any]:
        payload = {
            "grant_type": "client_credentials",
            "scope": scope,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        headers.update(self._basic_auth_header(client_id, client_secret))

        async with httpx.AsyncClient(timeout=20.0, verify=False) as client:
            response = await client.post(
                self.settings.wso2_token_endpoint,
                data=payload,
                headers=headers,
            )

        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
        }

    async def introspect_token(
        self, *, token: str, client_id: str, client_secret: str
    ) -> dict[str, Any]:
        payload = {"token": token}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        headers.update(self._basic_auth_header(client_id, client_secret))

        async with httpx.AsyncClient(timeout=20.0, verify=False) as client:
            response = await client.post(
                self.settings.wso2_introspection_endpoint,
                data=payload,
                headers=headers,
            )

        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
        }

    async def exchange_code_for_obo(
        self,
        *,
        code: str,
        code_verifier: str,
        agent_token: str,
    ) -> dict[str, Any]:
        payload: dict[str, str] = {
            "grant_type": self.settings.obo_grant_type,
            "scope": self.settings.obo_scope,
            self.settings.obo_agent_token_parameter: agent_token,
        }

        if self.settings.obo_grant_type == self.TOKEN_EXCHANGE_GRANT:
            payload[self.settings.obo_subject_token_parameter] = code
            if self.settings.obo_subject_token_type_parameter:
                payload[self.settings.obo_subject_token_type_parameter] = (
                    self.settings.obo_subject_token_type_value
                )
            # Some WSO2 setups still validate PKCE artifacts during exchange.
            payload["code_verifier"] = code_verifier
            payload["redirect_uri"] = self.settings.obo_redirect_uri
        else:
            payload["code"] = code
            payload["redirect_uri"] = self.settings.obo_redirect_uri
            payload["code_verifier"] = code_verifier

        if self.settings.obo_agent_token_type_parameter:
            payload[self.settings.obo_agent_token_type_parameter] = self.settings.obo_agent_token_type_value

        payload.update(self.settings.obo_extra_token_params)

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if self.settings.obo_client_secret:
            headers.update(
                self._basic_auth_header(self.settings.obo_client_id, self.settings.obo_client_secret)
            )
        else:
            payload["client_id"] = self.settings.obo_client_id

        async with httpx.AsyncClient(timeout=20.0, verify=False) as client:
            response = await client.post(
                self.settings.wso2_token_endpoint,
                data=payload,
                headers=headers,
            )

        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
            "request_payload": payload,
        }


oauth_service = OAuthService()
