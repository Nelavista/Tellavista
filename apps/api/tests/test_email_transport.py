"""Email transport: SMTP for local/relay, Sendhiiv's HTTP API for DEV/PROD."""
from __future__ import annotations

from collections.abc import Iterator

import httpx
import pytest

from app.core.config import get_settings
from app.worker import tasks
from app.worker.errors import PermanentJobError


class _Response:
    def __init__(self, status_code: int, payload: dict | None = None) -> None:
        self.status_code = status_code
        self._payload = payload or {}

    def json(self) -> dict:
        return self._payload

    @property
    def text(self) -> str:
        return str(self._payload)


@pytest.fixture(autouse=True)
def _fresh_settings() -> Iterator[None]:
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def _sendhiiv(monkeypatch, *, status: int, payload: dict | None = None) -> list[dict]:
    """Configure Sendhiiv and return the list of captured httpx.post kwargs."""
    monkeypatch.setenv("EMAIL_PROVIDER", "sendhiiv")
    monkeypatch.setenv("SENDHIIV_API_KEY", "sh_live_test")
    monkeypatch.setenv("APP_ENV", "local")
    monkeypatch.delenv("EMAIL_REDIRECT_TO", raising=False)
    get_settings.cache_clear()

    calls: list[dict] = []

    def fake_post(url: str, **kwargs: object) -> _Response:
        calls.append(kwargs)
        return _Response(status, payload)

    monkeypatch.setattr(tasks.httpx, "post", fake_post)
    return calls


def test_sendhiiv_posts_the_message(monkeypatch) -> None:
    calls = _sendhiiv(monkeypatch, status=202, payload={"success": True, "status": "queued"})

    tasks.send_email({"to": "student@example.test", "subject": "Verify", "body": "Click me"})

    assert len(calls) == 1
    kwargs = calls[0]
    headers = kwargs["headers"]
    assert isinstance(headers, dict)
    assert headers == {"Authorization": "Bearer sh_live_test"}
    assert kwargs["json"] == {
        "to": "student@example.test",
        "subject": "Verify",
        "text": "Click me",
    }


def test_sendhiiv_includes_from_only_when_configured(monkeypatch) -> None:
    calls = _sendhiiv(monkeypatch, status=202)
    monkeypatch.setenv("SENDHIIV_FROM", "Nelavista <no-reply@nelavista.com>")
    get_settings.cache_clear()

    tasks.send_email({"to": "student@example.test", "subject": "Hi", "body": "Body"})

    assert calls[0]["json"]["from"] == "Nelavista <no-reply@nelavista.com>"


def test_sendhiiv_4xx_is_permanent(monkeypatch) -> None:
    _sendhiiv(monkeypatch, status=400, payload={"error": "bad request"})

    with pytest.raises(PermanentJobError, match="400"):
        tasks.send_email({"to": "student@example.test", "subject": "Hi", "body": "Body"})


def test_sendhiiv_5xx_is_permanent_because_it_may_be_queued(monkeypatch) -> None:
    _sendhiiv(monkeypatch, status=503, payload={"error": "unavailable"})

    with pytest.raises(PermanentJobError, match="delivery state unknown"):
        tasks.send_email({"to": "student@example.test", "subject": "Hi", "body": "Body"})


def test_sendhiiv_timeout_is_permanent_because_it_may_be_queued(monkeypatch) -> None:
    _sendhiiv(monkeypatch, status=202)

    def timeout(url: str, **kwargs: object) -> _Response:
        raise httpx.ConnectTimeout("timed out")

    monkeypatch.setattr(tasks.httpx, "post", timeout)

    with pytest.raises(PermanentJobError, match="delivery state unknown"):
        tasks.send_email({"to": "student@example.test", "subject": "Hi", "body": "Body"})


def test_sendhiiv_rate_limit_is_retryable(monkeypatch) -> None:
    _sendhiiv(monkeypatch, status=429, payload={"error": "too many requests"})

    with pytest.raises(RuntimeError, match="rate limited"):
        tasks.send_email({"to": "student@example.test", "subject": "Hi", "body": "Body"})


def test_sendhiiv_quota_exceeded_is_permanent(monkeypatch) -> None:
    _sendhiiv(
        monkeypatch,
        status=429,
        payload={"success": False, "code": "QUOTA_EXCEEDED", "msg": "monthly quota reached"},
    )

    with pytest.raises(PermanentJobError, match="quota"):
        tasks.send_email({"to": "student@example.test", "subject": "Hi", "body": "Body"})


def test_sendhiiv_without_a_key_fails_permanently(monkeypatch) -> None:
    monkeypatch.setenv("EMAIL_PROVIDER", "sendhiiv")
    monkeypatch.delenv("SENDHIIV_API_KEY", raising=False)
    get_settings.cache_clear()

    with pytest.raises(PermanentJobError, match="SENDHIIV_API_KEY"):
        tasks.send_email({"to": "student@example.test", "subject": "Hi", "body": "Body"})


def test_non_production_redirects_all_mail_to_one_inbox(monkeypatch) -> None:
    calls = _sendhiiv(monkeypatch, status=202)
    monkeypatch.setenv("APP_ENV", "dev")
    monkeypatch.setenv("EMAIL_REDIRECT_TO", "ops@example.test")
    get_settings.cache_clear()

    tasks.send_email({"to": "student@example.test", "subject": "Verify", "body": "Click me"})

    assert calls[0]["json"]["to"] == "ops@example.test"
    assert calls[0]["json"]["subject"] == "[DEV -> student@example.test] Verify"


def test_production_never_redirects(monkeypatch) -> None:
    calls = _sendhiiv(monkeypatch, status=202)
    monkeypatch.setenv("APP_ENV", "prod")
    monkeypatch.setenv("EMAIL_REDIRECT_TO", "ops@example.test")
    get_settings.cache_clear()

    tasks.send_email({"to": "student@example.test", "subject": "Verify", "body": "Click me"})

    assert calls[0]["json"]["to"] == "student@example.test"
    assert calls[0]["json"]["subject"] == "Verify"


def test_smtp_fallback_authenticates_when_credentials_are_set(monkeypatch) -> None:
    monkeypatch.setenv("EMAIL_PROVIDER", "smtp")
    monkeypatch.setenv("APP_ENV", "local")
    monkeypatch.setenv("MAIL_USERNAME", "smtp-user")
    monkeypatch.setenv("MAIL_PASSWORD", "smtp-pass")
    monkeypatch.delenv("EMAIL_REDIRECT_TO", raising=False)
    get_settings.cache_clear()

    instances: list = []

    class FakeSMTP:
        def __init__(self, host: str, port: int, timeout: int) -> None:
            self.host = host
            self.login_args: tuple[str, str] | None = None
            self.sent = None
            instances.append(self)

        def __enter__(self) -> FakeSMTP:
            return self

        def __exit__(self, exc_type, exc, tb) -> bool:  # noqa: ANN001
            return False

        def starttls(self) -> None:
            pass

        def login(self, username: str, password: str) -> None:
            self.login_args = (username, password)

        def send_message(self, message) -> None:  # noqa: ANN001
            self.sent = message

    monkeypatch.setattr(tasks.smtplib, "SMTP", FakeSMTP)
    tasks.send_email({"to": "student@example.test", "subject": "Hi", "body": "Body"})

    assert instances[0].login_args == ("smtp-user", "smtp-pass")
    assert instances[0].sent["To"] == "student@example.test"
