from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient


def test_health_endpoint_reports_runtime_settings() -> None:
    resource_root = Path(__file__).resolve().parents[1]
    previous_app_modules = {
        name: module
        for name, module in list(sys.modules.items())
        if name == "app" or name.startswith("app.")
    }

    for name in previous_app_modules:
        sys.modules.pop(name, None)

    sys.path.insert(0, str(resource_root))
    try:
        from app.config import settings
        from app.main import app

        client = TestClient(app)
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {
            "status": "ok",
            "issuer": settings.wso2_issuer,
            "jwks": settings.wso2_jwks_endpoint,
            "introspection": settings.wso2_introspection_endpoint,
        }
    finally:
        sys.path.remove(str(resource_root))
        for name in [name for name in list(sys.modules) if name == "app" or name.startswith("app.")]:
            sys.modules.pop(name, None)
        sys.modules.update(previous_app_modules)