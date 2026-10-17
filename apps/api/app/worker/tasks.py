"""Job handlers, registered by name.

A handler takes the job payload and either returns or raises. Raising is the
retry signal — the runner decides backoff and when to give up, so handlers stay
small and do not implement their own retry loops.

`send_email` is the first handler because verification and reset links are the
first thing that must not be lost. It uses SMTP so local Mailpit (port 1025) and
any transactional provider share one code path.
"""
from __future__ import annotations

import logging
import smtplib
from collections.abc import Callable
from email.message import EmailMessage
from typing import Any

from app.core.config import get_settings

logger = logging.getLogger(__name__)


def send_email(payload: dict[str, Any]) -> None:
    settings = get_settings()
    to = payload.get("to")
    if not to:
        raise ValueError("send_email requires a 'to' address")
    message = EmailMessage()
    message["From"] = settings.MAIL_FROM
    message["To"] = to
    message["Subject"] = payload.get("subject", "")
    message.set_content(payload.get("body", ""))
    with smtplib.SMTP(settings.MAIL_HOST, settings.MAIL_PORT, timeout=10) as smtp:
        if settings.MAIL_USE_TLS:
            smtp.starttls()
        smtp.send_message(message)


def send_push(payload: dict[str, Any]) -> None:
    """Deliver a push through the configured endpoint, then mark it pushed.

    With no `PUSH_ENDPOINT` configured this is in-app only: the notification row
    is already visible, so nothing is lost. The transport is a single httpx call
    so swapping it for Expo's API or a provider SDK later is local to this file.
    """
    settings = get_settings()
    if settings.PUSH_ENDPOINT:
        import httpx

        response = httpx.post(
            settings.PUSH_ENDPOINT,
            json={
                "to": payload.get("user_id"),
                "title": payload.get("title"),
                "body": payload.get("body"),
                "data": payload.get("data") or {},
            },
            timeout=10.0,
        )
        response.raise_for_status()
    else:
        logger.info("push skipped (PUSH_ENDPOINT unset) notification=%s", payload.get("notification_id"))

    from app.db.session import SessionLocal
    from app.models.engagement import Notification

    notification_id = payload.get("notification_id")
    if notification_id:
        with SessionLocal() as db:
            row = db.get(Notification, notification_id)
            if row is not None and row.pushed_at is None:
                from datetime import UTC, datetime

                row.pushed_at = datetime.now(UTC)
                db.commit()


def noop(payload: dict[str, Any]) -> None:
    logger.info("noop job payload=%s", payload)


HANDLERS: dict[str, Callable[[dict[str, Any]], None]] = {
    "send_email": send_email,
    "send_push": send_push,
    "noop": noop,
}
