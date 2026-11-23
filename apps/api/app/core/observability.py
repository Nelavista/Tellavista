"""Product analytics (Phase 0 PR 0.7).

PostHog is called over its HTTP capture endpoint with httpx rather than its SDK,
so there is no extra dependency and no monkey-patching. Every event name lives in
`EVENTS`, mirroring the journey stages the PRD cares about — dashboards built on
ad-hoc strings rot within a week. An unset key is a complete no-op.
"""
from __future__ import annotations

import logging
import traceback
from typing import Any

from app.core.config import get_settings

logger = logging.getLogger(__name__)

POSTHOG_HOST = "https://us.i.posthog.com"

# The seven journey stages from the brief. Do not add one-off strings.
EVENTS: dict[str, str] = {
    "enrolled": "student.enrolled",
    "lesson_completed": "student.lesson_completed",
    "assessment_passed": "student.assessment_passed",
    "matched": "student.matched",
    "task_submitted": "student.task_submitted",
    "approved": "student.work_approved",
    "paid": "student.paid",
}


def _post(payload: dict[str, Any]) -> None:
    """Send one capture payload. Never raises: telemetry is best effort."""
    try:
        import httpx

        httpx.post(f"{POSTHOG_HOST}/capture/", json=payload, timeout=2.0)
    except Exception:  # noqa: BLE001 - telemetry is best effort by design
        logger.debug("posthog capture failed", exc_info=True)


def capture(distinct_id: str | int, event: str, properties: dict[str, Any] | None = None) -> None:
    """Fire-and-forget analytics. Never raises: a lost event must not fail a write."""
    settings = get_settings()
    if not settings.POSTHOG_API_KEY:
        return
    _post(
        {
            "api_key": settings.POSTHOG_API_KEY,
            "event": event,
            "distinct_id": str(distinct_id),
            "properties": properties or {},
        }
    )


def capture_exception(
    exc: BaseException,
    *,
    request_id: str | None = None,
    path: str | None = None,
    method: str | None = None,
) -> None:
    """Report an unhandled server error to PostHog Error Tracking.

    Error Tracking is the other half of ``capture``: journey events answer "how
    far did students get", this answers "what broke". It is gated by the same
    key, so an environment without PostHog still logs to stdout and sends
    nothing. The exception text and traceback are server-side detail, not a
    client response -- ``errors.py`` still returns only a request id.
    """
    settings = get_settings()
    if not settings.POSTHOG_API_KEY:
        return
    try:
        stack = "".join(
            traceback.format_exception(type(exc), exc, exc.__traceback__)
        )[:20_000]
        _post(
            {
                "api_key": settings.POSTHOG_API_KEY,
                "event": "$exception",
                "distinct_id": f"server:{request_id or 'unknown'}",
                "properties": {
                    "$exception_list": [
                        {
                            "type": type(exc).__name__,
                            "value": str(exc),
                            "stacktrace": stack,
                            "mechanism": {"handled": False, "synthetic": False},
                        }
                    ],
                    "service": "nelavista-api",
                    "request_id": request_id,
                    "path": path,
                    "method": method,
                },
            }
        )
    except Exception:  # noqa: BLE001 - telemetry must not mask the real error
        logger.debug("posthog exception capture failed", exc_info=True)
