"""Liveness/readiness. Deliberately dependency-light: it must answer even when
the database is down, so the platform can tell "process up" from "app healthy".
"""
from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from app import __version__
from app.core.config import get_settings

router = APIRouter(tags=["health"])


class Health(BaseModel):
    status: str
    app_env: str
    api_version: str
    app_version: str


@router.get("/health", response_model=Health, summary="Health check")
def health() -> Health:
    settings = get_settings()
    return Health(
        status="ok",
        app_env=settings.APP_ENV,
        api_version=settings.API_VERSION,
        app_version=__version__,
    )
