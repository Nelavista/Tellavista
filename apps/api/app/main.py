"""Nelavista V2 API — FastAPI modular monolith (ADR-0001).

Config is validated on import (fail-fast). The API path version comes from
settings and must exist in packages/config/versions.json.
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.v1.router import api_v1_router
from app.core.config import get_settings
from app.core.errors import register_exception_handlers
from app.core.request_id import RequestIdMiddleware
from app.core.security_headers import SecurityHeadersMiddleware
from app.core.versioning import VersioningMiddleware

settings = get_settings()  # raises RuntimeError on invalid config

app = FastAPI(
    title="Nelavista API",
    version=__version__,
    docs_url=None if settings.is_prod else "/docs",
    redoc_url=None if settings.is_prod else "/redoc",
    openapi_url=None if settings.is_prod else "/openapi.json",
)

# Middleware order: last added is outermost.
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(VersioningMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Idempotency-Key", "X-App-Version", "X-App-Platform"],
)
# Request id last, so it is outermost among ours and exists inside error handlers.
app.add_middleware(RequestIdMiddleware)

register_exception_handlers(app)

app.include_router(api_v1_router, prefix=f"/{settings.API_VERSION}")


@app.get("/", include_in_schema=False)
def root() -> dict:
    """Tiny handshake so a client can discover the current API path version."""
    return {
        "service": "nelavista-api",
        "app_version": __version__,
        "api_version": settings.API_VERSION,
        "health": f"/{settings.API_VERSION}/health",
    }
