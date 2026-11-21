"""Job handlers, registered by name.

A handler takes the job payload and either returns or raises. Raising is the
retry signal — the runner decides backoff and when to give up, so handlers stay
small and do not implement their own retry loops. A `PermanentJobError` marks the
job failed at once: a 400 from the provider will not fix itself.

`send_email` is the first handler because verification and reset links are the
first thing that must not be lost. Two transports share the same handler:

* `EMAIL_PROVIDER=smtp` — Mailpit locally, or any SMTP relay with AUTH;
* `EMAIL_PROVIDER=sendhiiv` — Sendhiiv's HTTP API. No outbound SMTP port, which
  matters on Render's free tier (SMTP 25/465/587 is blocked);
* `EMAIL_PROVIDER=console` — print the message in the worker log. This is the
  no-Docker local default used by `scripts/dev-local.ps1`.

Sendhiiv's delivery contract is narrow: only HTTP 429 (rate limit) is safe to
retry, because it is rejected before anything is queued. A 5xx or a timeout may
already have queued the message, so those fail permanently rather than risk a
duplicate verification email.

In non-production, `EMAIL_REDIRECT_TO` can funnel every message to one inbox.
That is the safe way to exercise DEV without a test-key mode: no real student
ever receives the preview's mail.
"""
from __future__ import annotations

import logging
import smtplib
from collections.abc import Callable
from email.message import EmailMessage
from typing import Any

import httpx

from app.core.config import get_settings
from app.core.time import utcnow
from app.worker.errors import PermanentJobError

logger = logging.getLogger(__name__)


def _send_smtp(settings: Any, *, to: str, subject: str, body: str) -> None:
    message = EmailMessage()
    message["From"] = settings.MAIL_FROM
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)

    if settings.MAIL_PORT == 465:
        client: smtplib.SMTP = smtplib.SMTP_SSL(settings.MAIL_HOST, settings.MAIL_PORT, timeout=10)
    else:
        client = smtplib.SMTP(settings.MAIL_HOST, settings.MAIL_PORT, timeout=10)

    with client as smtp:
        if settings.MAIL_USE_TLS and settings.MAIL_PORT != 465:
            smtp.starttls()
        if settings.MAIL_USERNAME:
            smtp.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
        smtp.send_message(message)


def _sendhiiv_rejection(response: httpx.Response) -> tuple[str, str]:
    """Return (machine code, human detail), tolerating a non-JSON body."""
    try:
        data = response.json()
    except ValueError:
        return "", response.text[:300]
    if not isinstance(data, dict):
        return "", str(data)[:300]
    code = str(data.get("code") or "")
    detail = str(data.get("error") or data.get("msg") or data)[:300]
    return code, detail


def _send_sendhiiv(settings: Any, *, to: str, subject: str, body: str) -> None:
    """POST one message; mark only genuinely retryable failures as transient.

    202 is the success code. `429` is a rate limit unless its code says the
    monthly quota is exhausted. Everything else — 400/401/402/403/413, 5xx and
    transport errors — is permanent. The provider may already have queued a 5xx,
    so a retry could send a second verification email.
    """
    payload: dict[str, Any] = {"to": to, "subject": subject, "text": body}
    if settings.SENDHIIV_FROM:
        payload["from"] = settings.SENDHIIV_FROM

    try:
        response = httpx.post(
            settings.SENDHIIV_API_URL,
            json=payload,
            headers={"Authorization": f"Bearer {settings.SENDHIIV_API_KEY}"},
            timeout=15.0,
        )
    except httpx.HTTPError as exc:
        raise PermanentJobError(
            f"sendhiiv transport error; delivery state unknown, not retrying: {exc}"
        ) from exc

    if response.status_code in (200, 202):
        return

    code, detail = _sendhiiv_rejection(response)
    if response.status_code == 429:
        if code == "QUOTA_EXCEEDED":
            raise PermanentJobError(f"sendhiiv monthly quota exhausted: {detail}")
        # Rejected before queueing: the one thing that is safe to retry.
        raise RuntimeError(f"sendhiiv rate limited; retrying: {detail}")
    if response.status_code >= 500:
        raise PermanentJobError(
            f"sendhiiv {response.status_code}; delivery state unknown, not retrying: {detail}"
        )
    raise PermanentJobError(f"sendhiiv rejected {response.status_code}: {detail}")


def send_email(payload: dict[str, Any]) -> None:
    settings = get_settings()
    to = str(payload.get("to") or "")
    if not to:
        # A malformed payload is not going to fix itself on a retry.
        raise PermanentJobError("send_email requires a 'to' address")
    subject = str(payload.get("subject", ""))
    body = str(payload.get("body", ""))

    if settings.EMAIL_REDIRECT_TO and settings.APP_ENV != "prod":
        # Keep the real recipient visible in the subject so a preview inbox is
        # still a useful test log. Never applies in production.
        subject = f"[DEV -> {to}] {subject}"
        to = settings.EMAIL_REDIRECT_TO

    if settings.EMAIL_PROVIDER == "console":
        logger.info("email (console)\nto: %s\nsubject: %s\n\n%s", to, subject, body)
        return

    if settings.EMAIL_PROVIDER == "sendhiiv":
        if not settings.SENDHIIV_API_KEY:
            raise PermanentJobError("EMAIL_PROVIDER=sendhiiv but SENDHIIV_API_KEY is empty")
        _send_sendhiiv(settings, to=to, subject=subject, body=body)
        return

    _send_smtp(settings, to=to, subject=subject, body=body)


def _device_tokens(user_id: Any) -> list[str]:
    """Live tokens for one account, read in their own short session.

    A revoked device is never sent to: after sign-out the phone may belong to
    somebody else, and a push would leak the notification title.
    """
    if not user_id:
        return []
    from sqlalchemy import select

    from app.db.session import SessionLocal
    from app.models.engagement import PushDevice

    with SessionLocal() as db:
        return list(
            db.scalars(
                select(PushDevice.token).where(
                    PushDevice.user_id == int(user_id),
                    PushDevice.revoked_at.is_(None),
                )
            ).all()
        )


def _web_subscriptions(user_id: Any) -> list[tuple[int, dict[str, Any]]]:
    """Live browser subscriptions for a user, as (device id, subscription)."""
    if not user_id:
        return []
    from sqlalchemy import select

    from app.db.session import SessionLocal
    from app.models.engagement import PushDevice

    with SessionLocal() as db:
        rows = db.execute(
            select(PushDevice.id, PushDevice.subscription).where(
                PushDevice.user_id == int(user_id),
                PushDevice.revoked_at.is_(None),
                PushDevice.platform == "web",
                PushDevice.subscription.is_not(None),
            )
        ).all()
        return [(row[0], row[1]) for row in rows if isinstance(row[1], dict)]


def _revoke_push_device(device_id: int, reason: str) -> None:
    """Stop trying a dead endpoint. The browser registers again when it can."""
    from app.db.session import SessionLocal
    from app.models.engagement import PushDevice

    with SessionLocal() as db:
        row = db.get(PushDevice, device_id)
        if row is not None and row.revoked_at is None:
            row.revoked_at = utcnow()
            db.commit()
    logger.info("push revoked device=%s reason=%s", device_id, reason)


def send_push(payload: dict[str, Any]) -> None:
    """Deliver a push to every live device, then mark the notification pushed.

    Two transports, chosen by the row rather than by the caller:

    * native installs carry a provider token and go to `PUSH_ENDPOINT` (Expo);
    * browser installs carry a Web Push subscription and are signed with the
      VAPID key pair via `pywebpush`.

    With neither configured this is in-app only: the notification row is already
    visible, so nothing is lost. Neither branch fails the whole notification, so
    one dead device cannot silence the others.
    """
    settings = get_settings()
    tokens = payload.get("device_tokens") or _device_tokens(payload.get("user_id"))
    if settings.PUSH_ENDPOINT and tokens:
        import httpx

        for token in tokens:
            response = httpx.post(
                settings.PUSH_ENDPOINT,
                json={
                    "to": token,
                    "title": payload.get("title"),
                    "body": payload.get("body"),
                    "data": payload.get("data") or {},
                },
                timeout=10.0,
            )
            # A dead token must not fail the whole notification; the next
            # registration replaces it.
            if response.status_code >= 400:
                logger.warning(
                    "push rejected token=%s status=%s", token[-6:], response.status_code
                )
    elif not settings.PUSH_ENDPOINT:
        logger.info("push skipped (PUSH_ENDPOINT unset) notification=%s", payload.get("notification_id"))

    _send_web_push(payload, settings)

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


def _send_web_push(payload: dict[str, Any], settings: Any) -> None:
    """Sign and deliver to each browser subscription, if VAPID is configured."""
    if not settings.VAPID_PRIVATE_KEY:
        return
    targets = _web_subscriptions(payload.get("user_id"))
    if not targets:
        return

    import json

    try:
        from pywebpush import WebPushException, webpush
    except ImportError:  # pragma: no cover - dependency is declared
        logger.warning("web push skipped (pywebpush not installed)")
        return

    body = json.dumps(
        {
            "title": payload.get("title"),
            "body": payload.get("body"),
            "data": payload.get("data") or {},
            "notification_id": payload.get("notification_id"),
        },
        default=str,
    )
    for device_id, subscription in targets:
        try:
            webpush(
                subscription_info={
                    "endpoint": subscription.get("endpoint"),
                    "keys": {
                        "p256dh": subscription.get("p256dh"),
                        "auth": subscription.get("auth"),
                    },
                },
                data=body,
                vapid_private_key=settings.VAPID_PRIVATE_KEY,
                vapid_claims={"sub": settings.VAPID_SUBJECT},
                timeout=10,
            )
        except WebPushException as exc:
            status = getattr(getattr(exc, "response", None), "status_code", None)
            # 404/410 mean the browser threw the subscription away. Revoking is
            # the only correct answer: retrying that endpoint can never succeed.
            if status in {404, 410}:
                _revoke_push_device(device_id, f"web_push_{status}")
            else:
                logger.warning("web push failed device=%s status=%s", device_id, status)
        except Exception:  # noqa: BLE001 - one bad subscription must not stop the rest
            logger.exception("web push failed device=%s", device_id)


def noop(payload: dict[str, Any]) -> None:
    logger.info("noop job payload=%s", payload)


def reconcile_daily(payload: dict[str, Any]) -> None:
    """Run the ledger reconciliation for every funded project (F3).

    The job exists so the same check a human can trigger by hand also happens on
    its own every day; a failure is a retry like any other job.
    """
    from app.db.session import SessionLocal
    from app.services.money import reconcile

    with SessionLocal() as db:
        run = reconcile.run(db, actor=None, project=None)
        db.commit()
        logger.info(
            "daily reconciliation run=%s balanced=%s", run.id, run.balanced
        )


HANDLERS: dict[str, Callable[[dict[str, Any]], None]] = {
    "send_email": send_email,
    "send_push": send_push,
    "reconcile_daily": reconcile_daily,
    "noop": noop,
}
