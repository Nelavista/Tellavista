"""API version + minimum-app-version enforcement (ADR-0010).

Product versions (V1/V2) and API versions (`/v1`) are deliberately distinct.
Every mobile request carries ``X-App-Version`` and ``X-App-Platform``; a version
below the platform's ``min_supported`` (packages/config/versions.json) gets
``426 Upgrade Required`` with a machine-readable body.
"""
from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.core.config import get_settings


def compare_versions(a: str, b: str) -> int:
    """Compare dotted numeric versions. Returns -1, 0 or 1. Non-numeric parts are 0."""
    pa = [int(x) if x.isdigit() else 0 for x in (a or "").split(".")]
    pb = [int(x) if x.isdigit() else 0 for x in (b or "").split(".")]
    for i in range(max(len(pa), len(pb))):
        d = (pa[i] if i < len(pa) else 0) - (pb[i] if i < len(pb) else 0)
        if d:
            return 1 if d > 0 else -1
    return 0


class VersioningMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        settings = get_settings()
        platform = (request.headers.get("X-App-Platform") or "").lower()
        app_version = request.headers.get("X-App-Version") or ""

        if platform in {"ios", "android"} and app_version:
            min_version = settings.min_supported_app_version(platform)
            if min_version and compare_versions(app_version, min_version) < 0:
                body = {
                    "upgrade": "required",
                    "min_version": min_version,
                    "store_url": (settings.versions_file().get("mobile", {}).get(platform) or {})
                    .get("store_url", ""),
                }
                return JSONResponse(
                    status_code=426,
                    content=body,
                    headers={"X-API-Version": settings.API_VERSION},
                )

        response = await call_next(request)
        response.headers["X-API-Version"] = settings.API_VERSION

        # Below-latest (but still supported) apps get a soft prompt header.
        if platform in {"ios", "android"} and app_version:
            policy = settings.versions_file().get("mobile", {}).get(platform) or {}
            latest = policy.get("latest")
            if latest and compare_versions(app_version, latest) < 0:
                response.headers["X-Update-Recommended"] = latest
        return response
