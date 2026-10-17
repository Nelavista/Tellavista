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


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local"),
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
    MAIL_HOST: str = "localhost"
    MAIL_PORT: int = 1025
    MAIL_USE_TLS: bool = False
    MAIL_FROM: str = "noreply@nelavista.local"

    # --- Integrations (optional; unset = feature cleanly disabled) ---
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "openai/gpt-4o-mini"
    # Expo push endpoint (https://exp.host/--/api/v2/push/send). Unset = in-app only.
    PUSH_ENDPOINT: str = ""
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    CLOUDINARY_URL: str = ""
    SENTRY_DSN: str = ""
    POSTHOG_API_KEY: str = ""

    # --- Storage ---
    STORAGE_BACKEND: Literal["local", "cloudinary"] = "local"

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
            # Local convenience default; never acceptable in dev/prod.
            object.__setattr__(self, "SECRET_KEY", "local-dev-only-secret-change-me")

        if not self.DATABASE_URL:
            problems.append("DATABASE_URL is required (see .env.example).")

        # CORS must never be a wildcard in a deployed environment.
        if not self.is_local and "*" in self.cors_origins:
            problems.append("CORS_ORIGINS must not contain '*' outside local.")

        # Cloudinary backend needs the URL.
        if self.STORAGE_BACKEND == "cloudinary" and not self.CLOUDINARY_URL:
            problems.append("STORAGE_BACKEND=cloudinary requires CLOUDINARY_URL.")

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
