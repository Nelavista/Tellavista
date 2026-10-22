"""Product analytics (Phase 0 PR 0.7).

PostHog is called over its HTTP capture endpoint with httpx rather than its SDK,
so there is no extra dependency and no monkey-patching. Every event name lives in
`EVENTS`, mirroring the journey stages the PRD cares about — dashboards built on
ad-hoc strings rot within a week. An unset key is a complete no-op.
"""
from __future__ import annotations

import logging
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


def capture(distinct_id: str | int, event: str, properties: dict[str, Any] | None = None) -> None:
    """Fire-and-forget analytics. Never raises: a lost event must not fail a write."""
    settings = get_settings()
    if not settings.POSTHOG_API_KEY:
        return
    try:
        import httpx

        httpx.post(
            f"{POSTHOG_HOST}/capture/",
            json={
                "api_key": settings.POSTHOG_API_KEY,
                "event": event,
                "distinct_id": str(distinct_id),
                "properties": properties or {},
            },
            timeout=2.0,
        )
    except Exception:  # noqa: BLE001 - analytics is best effort by design
        logger.debug("posthog capture failed event=%s", event, exc_info=True)
