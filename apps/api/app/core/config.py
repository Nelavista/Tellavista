"""Application settings — environment-variable only, validated at startup.

One switch drives behaviour: ``APP_ENV`` ∈ {local, dev, prod} (ADR-0002).
The app **fails fast** with a readable message when a required variable is missing.
"""
from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

AppEnv = Literal["local", "dev", "prod"]

# Repo-root/packages/config/versions.json — the single source of version truth.
_VERSIONS_FILE = Path(__file__).resolve().parents[4] / "packages" / "config" / "versions.json"
# V2 reads its own env files only. The V1 app has a separate root .env; loading
# that here would let V1's DATABASE_URL/SECRET_KEY leak into V2 (ADR-0002).
_API_DIR = Path(__file__).resolve().parents[2]
_ENV_FILES = (str(_API_DIR / ".env"), str(_API_DIR / ".env.local"))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILES,
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    # --- Core ---
    APP_ENV: AppEnv = "local"
    API_VERSION: str = "v1"
    SECRET_KEY: str = ""
    CORS_ORIGINS: str = ""

    # --- Database / cache ---
    DATABASE_URL: str = ""
    REDIS_URL: str = ""

    # --- Mail ---
    # `smtp` = Mailpit locally or any SMTP relay; `sendhiiv` = Sendhiiv's HTTP API;
    # `console` = print the message in the worker log (no Docker/Mailpit needed).
    EMAIL_PROVIDER: Literal["smtp", "sendhiiv", "console"] = "smtp"
    MAIL_HOST: str = "localhost"
    MAIL_PORT: int = 1025
    MAIL_USE_TLS: bool = False
    MAIL_FROM: str = "noreply@nelavista.local"
    # SMTP AUTH. Mailpit ignores both; a real relay requires them.
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    # Non-production only: send every message to this one address instead of the
    # real recipient. The original recipient is prefixed into the subject.
    EMAIL_REDIRECT_TO: str = ""
    # Sendhiiv (https://sendhiiv.com): HTTP API, no outbound SMTP port needed.
    # `SENDHIIV_FROM` is optional; empty uses the shared sender until the domain
    # is verified.
    SENDHIIV_API_KEY: str = ""
    SENDHIIV_API_URL: str = "https://api.sendhiiv.com/api/v1/messages"
    SENDHIIV_FROM: str = ""
    # Links in email must be absolute: a relative `/auth/verify` is meaningless
    # in an inbox (F9). Each environment points at its own web origin.
    WEB_BASE_URL: str = "http://localhost:5173"

    # --- Integrations (optional; unset = feature cleanly disabled) ---
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "openai/gpt-4o-mini"
    # Expo push endpoint (https://exp.host/--/api/v2/push/send). Unset = in-app only.
    PUSH_ENDPOINT: str = ""
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    POSTHOG_API_KEY: str = ""

    @field_validator("CORS_ORIGINS")
    @classmethod
    def _strip_origins(cls, v: str) -> str:
        return ",".join(o.strip() for o in v.split(",") if o.strip())

    @property
    def cors_origins(self) -> list[str]:
        return [o for o in self.CORS_ORIGINS.split(",") if o]

    @property
    def is_prod(self) -> bool:
        return self.APP_ENV == "prod"

    @property
    def is_local(self) -> bool:
        return self.APP_ENV == "local"

    @model_validator(mode="after")
    def _validate_for_env(self) -> Settings:
        problems: list[str] = []

        # SECRET_KEY is mandatory outside local; refuse to boot with a guessable key.
        if not self.is_local and not self.SECRET_KEY:
            problems.append("SECRET_KEY is required when APP_ENV is 'dev' or 'prod'.")
        if self.is_local and not self.SECRET_KEY:
            # Local convenience default; never acceptable in dev/prod. 32+ bytes
            # keeps PyJWT from warning about a short HMAC key.
            object.__setattr__(
                self, "SECRET_KEY", "local-dev-only-secret-change-me-please-32bytes"
            )

        if not self.DATABASE_URL:
            if self.is_local:
                # Zero-config local mode: SQLite instead of Docker Postgres. The
                # local runner (scripts/dev-local.ps1) uses the same path.
                local_dir = _API_DIR / ".local"
                local_dir.mkdir(parents=True, exist_ok=True)
                object.__setattr__(
                    self, "DATABASE_URL", f"sqlite:///{local_dir.as_posix()}/v2-local.db"
                )
            else:
                problems.append("DATABASE_URL is required (see .env.example).")

        # An emailed link that is not absolute cannot be clicked.
        if not self.WEB_BASE_URL.startswith(("http://", "https://")):
            problems.append("WEB_BASE_URL must be an absolute http(s) URL.")

        # CORS must never be a wildcard in a deployed environment.
        if not self.is_local and "*" in self.cors_origins:
            problems.append("CORS_ORIGINS must not contain '*' outside local.")

        if problems:
            raise RuntimeError(
                "Invalid configuration for APP_ENV="
                f"{self.APP_ENV!r}:\n  - " + "\n  - ".join(problems)
            )
        return self

    # --- version policy (reads packages/config/versions.json) ---
    def versions_file(self) -> dict:
        try:
            return json.loads(_VERSIONS_FILE.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return {}

    def min_supported_app_version(self, platform: str) -> str | None:
        return (self.versions_file().get("mobile", {}).get(platform) or {}).get("min_supported")


@lru_cache
def get_settings() -> Settings:
    """Cached singleton. Raises RuntimeError (fail-fast) on invalid config."""
    # Allow an override for tooling/tests that must not read a real .env file.
    if os.environ.get("NELAVISTA_SKIP_ENV_FILE") == "1":
        return Settings(_env_file=None)  # type: ignore[call-arg]
    return Settings()
