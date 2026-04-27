from __future__ import annotations

from contextlib import nullcontext
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from fastapi.testclient import TestClient

import service


def make_agent(*, ready: bool = True, answer: str = "ok", model_id: str = "gpt-4o-mini"):
    return SimpleNamespace(
        initialize=Mock(),
        is_ready=ready,
        model_id=model_id,
        ask=AsyncMock(return_value=answer),
    )


class ServiceContractTests(unittest.TestCase):
    def test_root_redirects_to_docs(self) -> None:
        fake_agent = make_agent()
        with patch.object(service, "agent", fake_agent):
            with TestClient(service.app) as client:
                response = client.get("/", follow_redirects=False)

        self.assertEqual(response.status_code, 307)
        self.assertEqual(response.headers["location"], "/docs")

    def test_health_returns_ok(self) -> None:
        fake_agent = make_agent()
        with patch.object(service, "agent", fake_agent):
            with TestClient(service.app) as client:
                response = client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_ready_reflects_agent_state(self) -> None:
        fake_agent = make_agent(ready=False)
        with patch.object(service, "agent", fake_agent):
            with TestClient(service.app) as client:
                response = client.get("/ready")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "initializing"})

    def test_invoke_uses_external_contract_defaults(self) -> None:
        fake_agent = make_agent(answer="respuesta")
        with patch.object(service, "agent", fake_agent):
            with TestClient(service.app) as client:
                response = client.post(
                    "/invoke",
                    json={
                        "message": "hola",
                        "session_id": "session-123",
                        "user_id": "user-1",
                        "metadata": {"channel": "test"},
                    },
                    headers={
                        "Authorization": "Bearer caller-token",
                        "x-trace-id": "trace-123",
                    },
                )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "answer": "respuesta",
                "session_id": "session-123",
                "model": "gpt-4o-mini",
                "trace_id": "trace-123",
                "status": "ok",
            },
        )
        fake_agent.ask.assert_awaited_once_with(
            "hola",
            silent=True,
            allow_interactive_auth=False,
        )

    def test_invoke_propagates_caller_identity_from_bearer_header(self) -> None:
        fake_agent = make_agent(answer="respuesta")
        with patch.object(service, "agent", fake_agent):
            with patch.object(service, "use_caller_identity", return_value=nullcontext()) as use_identity:
                with TestClient(service.app) as client:
                    response = client.post(
                        "/invoke",
                        json={
                            "message": "hola",
                            "user_id": "user-1",
                            "metadata": {"channel": "test"},
                        },
                        headers={"Authorization": "Bearer caller-token"},
                    )

        self.assertEqual(response.status_code, 200)
        use_identity.assert_called_once()
        identity = use_identity.call_args.args[0]
        self.assertIsInstance(identity, service.CallerIdentity)
        self.assertEqual(identity.access_token, "caller-token")
        self.assertEqual(identity.user_id, "user-1")
        self.assertEqual(identity.metadata, {"channel": "test"})

    def test_invoke_requires_bearer_token(self) -> None:
        fake_agent = make_agent(answer="respuesta")
        with patch.object(service, "agent", fake_agent):
            with TestClient(service.app) as client:
                response = client.post(
                    "/invoke",
                    json={
                        "message": "hola",
                    },
                )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Missing caller bearer token"})
        self.assertEqual(response.headers["www-authenticate"], "Bearer")
        fake_agent.ask.assert_not_awaited()

    def test_invoke_can_enable_interactive_auth(self) -> None:
        fake_agent = make_agent(answer="interactive")
        with patch.object(service, "agent", fake_agent):
            with TestClient(service.app) as client:
                response = client.post(
                    "/invoke",
                    json={
                        "message": "login",
                        "allow_interactive_auth": True,
                    },
                    headers={"Authorization": "Bearer caller-token"},
                )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        fake_agent.ask.assert_awaited_once_with(
            "login",
            silent=True,
            allow_interactive_auth=True,
        )


if __name__ == "__main__":
    unittest.main()
