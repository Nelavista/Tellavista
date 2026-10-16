"""Skeleton smoke tests: health, root, version headers, force-update, security headers."""
from __future__ import annotations

from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app

client = TestClient(app)
API = f"/{get_settings().API_VERSION}"


def test_health_ok() -> None:
    r = client.get(f"{API}/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["api_version"] == get_settings().API_VERSION
    assert body["app_env"] == "local"


def test_root_handshake() -> None:
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["service"] == "nelavista-api"


def test_api_version_header_present() -> None:
    r = client.get(f"{API}/health")
    assert r.headers.get("X-API-Version") == get_settings().API_VERSION


def test_security_headers_present() -> None:
    r = client.get(f"{API}/health")
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert r.headers["X-Frame-Options"] == "DENY"
    assert "Content-Security-Policy" in r.headers


def test_force_update_below_minimum() -> None:
    """A version below min_supported gets 426 with a machine-readable body."""
    r = client.get(f"{API}/health", headers={"X-App-Platform": "ios", "X-App-Version": "0.0.1"})
    assert r.status_code == 426
    body = r.json()
    assert body["upgrade"] == "required"
    assert "min_version" in body and "store_url" in body


def test_current_version_passes() -> None:
    r = client.get(f"{API}/health", headers={"X-App-Platform": "android", "X-App-Version": "99.0.0"})
    assert r.status_code == 200
