from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import parse_qs, urlparse

import pytest
from fastapi import HTTPException

os.environ.setdefault("AGENT_ID", "test-agent")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.obo_service import obo_service
from app.services.oauth_service import oauth_service
from app.state.session_store import session_store


@pytest.fixture(autouse=True)
def reset_state() -> None:
    session_store._sessions.clear()
    session_store._state_index.clear()
    yield
    session_store._sessions.clear()
    session_store._state_index.clear()


@pytest.fixture(autouse=True)
def fake_settings(monkeypatch: pytest.MonkeyPatch) -> SimpleNamespace:
    settings = SimpleNamespace(
        obo_client_id="obo-client",
        obo_client_secret="obo-secret",
        obo_redirect_uri="http://localhost:8000/api/obo/callback",
        obo_scope="openid profile files.read",
        obo_authorization_prompt="consent",
        obo_grant_type="urn:ietf:params:oauth:grant-type:token-exchange",
        obo_agent_token_parameter="actor_token",
        obo_agent_token_type_parameter="actor_token_type",
        obo_agent_token_type_value="urn:ietf:params:oauth:token-type:access_token",
        obo_subject_token_parameter="subject_token",
        obo_subject_token_type_parameter="subject_token_type",
        obo_subject_token_type_value="urn:ietf:params:oauth:token-type:authorization_code",
        obo_extra_token_params={},
        obo_require_act_claim=True,
        wso2_authorize_endpoint="https://localhost:9443/oauth2/authorize",
        wso2_token_endpoint="https://localhost:9443/oauth2/token",
        wso2_issuer="https://localhost:9443/oauth2/token",
        introspection_client_id="introspection-client",
        introspection_client_secret="introspection-secret",
        debug_show_full_tokens=False,
    )
    monkeypatch.setattr(oauth_service, "settings", settings)
    monkeypatch.setattr(obo_service, "settings", settings)
    return settings


def _seed_agent_session(session_id: str) -> None:
    session_store.set_agent_token(
        session_id,
        artifact={"token": "agent-token", "claims": {}},
        configured_agent_id="agent-123",
        oauth_client_id="obo-client",
        token_sub="technical-agent",
        token_authentication_type="client_credentials",
        security_meaning="technical agent identity",
    )


def _seed_pending_exchange(session_id: str) -> None:
    _seed_agent_session(session_id)
    session_store.start_delegation(
        session_id,
        authorization_url="https://localhost:9443/oauth2/authorize?prompt=consent",
        state="state-123",
        code_verifier="verifier-123",
        code_challenge="challenge-123",
        scopes=["openid", "profile", "files.read"],
    )
    session_store.complete_callback("state-123", "auth-code-123")


def _build_enriched_artifact(subject: str, delegated_actor: str | None) -> dict[str, object]:
    claims: dict[str, object] = {"sub": subject, "scope": "openid files.read"}
    if delegated_actor:
        claims["act"] = {"sub": delegated_actor}
    return {
        "token": "obo-token",
        "claims": claims,
        "scopes": ["openid", "files.read"],
        "subject": subject,
        "actor": delegated_actor,
        "issuer": "https://localhost:9443/oauth2/token",
        "status": "available",
        "audience": None,
        "issued_at": None,
        "expires_at": None,
    }


def test_build_authorization_url_forces_prompt_consent() -> None:
    url = oauth_service.build_authorization_url(
        state="state-123",
        code_challenge="challenge-123",
        scopes=["openid", "profile", "files.read"],
    )

    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    assert parsed.scheme == "https"
    assert parsed.netloc == "localhost:9443"
    assert params["prompt"] == ["consent"]
    assert params["code_challenge_method"] == ["S256"]


def test_start_records_prompt_in_trace_and_authorization_url() -> None:
    _seed_agent_session("session-1")

    result = obo_service.start("session-1")

    assert result["artifacts"]["delegation"]["authorization_url"]["raw"] is not None
    assert "prompt=consent" in result["artifacts"]["delegation"]["authorization_url"]["raw"]
    assert result["traces"][0]["request_parameters"]["prompt"] == "consent"


def test_exchange_rejects_obo_token_without_act_sub(monkeypatch: pytest.MonkeyPatch) -> None:
    _seed_pending_exchange("session-2")

    async def fake_exchange_code_for_obo(*, code: str, code_verifier: str, agent_token: str) -> dict[str, object]:
        assert code == "auth-code-123"
        assert code_verifier == "verifier-123"
        assert agent_token == "agent-token"
        return {
            "status_code": 200,
            "body": {"access_token": "obo-token"},
            "request_payload": {"grant_type": "urn:ietf:params:oauth:grant-type:token-exchange"},
        }

    async def fake_enrich_opaque_token_artifact(artifact: dict[str, object]) -> dict[str, object]:
        return _build_enriched_artifact("alice", None)

    monkeypatch.setattr(oauth_service, "exchange_code_for_obo", fake_exchange_code_for_obo)
    monkeypatch.setattr(obo_service, "_enrich_opaque_token_artifact", fake_enrich_opaque_token_artifact)

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(obo_service.exchange("session-2"))

    assert exc_info.value.status_code == 502
    assert exc_info.value.detail["message"] == "WSO2 emitted OBO_TOKEN without act.sub"


def test_exchange_accepts_real_obo_token_with_act_sub(monkeypatch: pytest.MonkeyPatch) -> None:
    _seed_pending_exchange("session-3")

    async def fake_exchange_code_for_obo(*, code: str, code_verifier: str, agent_token: str) -> dict[str, object]:
        return {
            "status_code": 200,
            "body": {"access_token": "obo-token"},
            "request_payload": {"grant_type": "urn:ietf:params:oauth:grant-type:token-exchange"},
        }

    async def fake_enrich_opaque_token_artifact(artifact: dict[str, object]) -> dict[str, object]:
        return _build_enriched_artifact("alice", "agent-123")

    monkeypatch.setattr(oauth_service, "exchange_code_for_obo", fake_exchange_code_for_obo)
    monkeypatch.setattr(obo_service, "_enrich_opaque_token_artifact", fake_enrich_opaque_token_artifact)

    result = asyncio.run(obo_service.exchange("session-3"))

    assert result["delegated_user_id"] == "alice"
    assert result["delegated_agent_id"] == "agent-123"
    assert result["artifacts"]["obo"]["subject"] == "alice"
    assert result["artifacts"]["obo"]["actor"] == "agent-123"