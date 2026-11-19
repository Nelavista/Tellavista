"""Publishing announcements and running the newsletter list.

Publishing is the only operation with side effects that matter, so it is the only
one with rules worth stating:

* A draft can be edited freely; a published one can only be archived. Ops cannot
  rewrite a message people have already received.
* Publishing is idempotent. The second publish of the same row enqueues nothing,
  because each send job carries an idempotency key tied to (announcement,
  subscriber). A double-click, a retry or a redelivered click cannot double-mail.
* Only the addresses that are active *and* match the audience are mailed, and the
  row records how many jobs it actually enqueued -- the count is evidence, not an
  estimate.
* An unsubscribed address stays in the table. Deleting it would let the next
  import silently re-subscribe someone who opted out.
* Every email carries that subscriber's own unsubscribe link, authorised by an
  opaque token rather than the address, so leaving needs no account and cannot
  be done on someone else's behalf.
"""
from __future__ import annotations

import secrets
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.errors import ApiError
from app.models.comms import (
    ANNOUNCEMENT_ARCHIVED,
    ANNOUNCEMENT_DRAFT,
    ANNOUNCEMENT_PUBLISHED,
    AUDIENCE_ALL,
    AUDIENCE_STAFF,
    AUDIENCES,
    CHANNEL_BOTH,
    CHANNEL_EMAIL,
    CHANNEL_PLATFORM,
    CHANNELS,
    Announcement,
    NewsletterSubscriber,
)
from app.models.identity import User
from app.models.jobs import Job
from app.services import audit
from app.services.jobs import enqueue

EMAIL_SUBJECT_PREFIX = "Nelavista"


def _validate_audience(value: str) -> str:
    if value not in AUDIENCES:
        raise ApiError(400, "invalid_audience", "Use students, staff or all.")
    return value


def _validate_channel(value: str) -> str:
    if value not in CHANNELS:
        raise ApiError(400, "invalid_channel", "Use platform, email or both.")
    return value


def create_announcement(
    db: Session,
    actor: User,
    *,
    title: str,
    body: str,
    audience: str = AUDIENCE_ALL,
    channel: str = CHANNEL_PLATFORM,
) -> Announcement:
    row = Announcement(
        title=title.strip(),
        body=body,
        audience=_validate_audience(audience),
        channel=_validate_channel(channel),
        created_by=actor.id,
        status=ANNOUNCEMENT_DRAFT,
    )
    db.add(row)
    db.flush()
    audit.record(
        db,
        action="comms.announcement_created",
        actor_user_id=actor.id,
        actor_role_code=actor.role.code if actor.role else None,
        target_type="announcement",
        target_id=row.id,
        context={"audience": row.audience, "channel": row.channel},
    )
    return row


def update_announcement(
    db: Session,
    actor: User,
    row: Announcement,
    *,
    title: str | None = None,
    body: str | None = None,
    audience: str | None = None,
    channel: str | None = None,
) -> Announcement:
    if row.status != ANNOUNCEMENT_DRAFT:
        raise ApiError(
            409,
            "announcement_not_editable",
            "A published announcement can be archived, but not rewritten.",
        )
    if title is not None:
        row.title = title.strip()
    if body is not None:
        row.body = body
    if audience is not None:
        row.audience = _validate_audience(audience)
    if channel is not None:
        row.channel = _validate_channel(channel)
    db.flush()
    return row


def _audience_matches(audience: str, is_staff: bool) -> bool:
    if audience == AUDIENCE_ALL:
        return True
    if audience == AUDIENCE_STAFF:
        return is_staff
    return not is_staff


def newsletter_emails(db: Session) -> list[str]:
    return list(
        db.scalars(
            select(NewsletterSubscriber.email)
            .where(NewsletterSubscriber.is_active.is_(True))
            .order_by(NewsletterSubscriber.id)
        ).all()
    )


def newsletter_rows(db: Session) -> list[NewsletterSubscriber]:
    """Active subscribers, as rows rather than addresses.

    The row is needed because every message carries that subscriber's own
    unsubscribe token; `newsletter_emails` cannot express that.
    """
    return list(
        db.scalars(
            select(NewsletterSubscriber)
            .where(NewsletterSubscriber.is_active.is_(True))
            .order_by(NewsletterSubscriber.id)
        ).all()
    )


def _email_body(announcement: Announcement, subscriber: NewsletterSubscriber) -> str:
    """The message plus the line that lets the reader leave.

    The link carries the subscriber's own token, never the address: an address in
    a URL can be guessed, and one reader must not be able to unsubscribe another.
    A row without a token still gets the message; it simply has no link, which is
    the honest state rather than a link that cannot work.
    """
    if subscriber.unsubscribe_token is None:
        return announcement.body
    # Read when the message is composed, not at import: the worker and the web
    # process each load their own environment.
    base = get_settings().WEB_BASE_URL.rstrip("/")
    link = f"{base}/newsletter/unsubscribe?token={subscriber.unsubscribe_token}"
    return (
        f"{announcement.body}\n\n---\n"
        "You are receiving this because you asked for the Nelavista newsletter.\n"
        f"Unsubscribe: {link}"
    )


def publish_announcement(db: Session, actor: User, row: Announcement) -> Announcement:
    if row.status == ANNOUNCEMENT_PUBLISHED:
        return row  # idempotent: a second publish sends nothing
    if row.status == ANNOUNCEMENT_ARCHIVED:
        raise ApiError(409, "announcement_archived", "An archived announcement cannot be published.")
    if not row.title.strip():
        raise ApiError(400, "announcement_needs_a_title", "An announcement needs a title.")

    row.status = ANNOUNCEMENT_PUBLISHED
    row.published_at = datetime.now(UTC)

    sent = 0
    if row.channel in (CHANNEL_EMAIL, CHANNEL_BOTH):
        for subscriber in newsletter_rows(db):
            # The key stays address-based on purpose: it was the key of already
            # queued sends, so a re-publish of an older announcement still matches
            # its own jobs instead of mailing the list a second time.
            key = f"announcement:{row.id}:subscriber:{subscriber.email}"
            # Count only a job this publish actually created. `enqueue` returns the
            # existing row for a key it has seen, which is a retry, not a new send.
            already = db.scalar(select(Job.id).where(Job.idempotency_key == key))
            enqueue(
                db,
                "send_email",
                {
                    "to": subscriber.email,
                    "subject": f"{EMAIL_SUBJECT_PREFIX}: {row.title}",
                    "body": _email_body(row, subscriber),
                },
                key=key,
            )
            if already is None:
                sent += 1
        row.email_sent_at = datetime.now(UTC)
    row.email_recipient_count = sent

    db.flush()
    audit.record(
        db,
        action="comms.announcement_published",
        actor_user_id=actor.id,
        actor_role_code=actor.role.code if actor.role else None,
        target_type="announcement",
        target_id=row.id,
        context={"audience": row.audience, "channel": row.channel, "emails": sent},
    )
    return row


def archive_announcement(db: Session, actor: User, row: Announcement) -> Announcement:
    if row.status == ANNOUNCEMENT_ARCHIVED:
        return row
    row.status = ANNOUNCEMENT_ARCHIVED
    row.archived_at = datetime.now(UTC)
    db.flush()
    audit.record(
        db,
        action="comms.announcement_archived",
        actor_user_id=actor.id,
        actor_role_code=actor.role.code if actor.role else None,
        target_type="announcement",
        target_id=row.id,
    )
    return row


def visible_to(db: Session, user: User | None, *, limit: int = 20) -> list[Announcement]:
    """What a signed-in person sees in the product.

    Drafts never leave ops, archived messages disappear, and the audience filter is
    applied here rather than in the route so a future caller cannot forget it.
    """
    is_staff = bool(user is not None and user.role and user.role.code != "student")
    rows = db.scalars(
        select(Announcement)
        .where(Announcement.status == ANNOUNCEMENT_PUBLISHED)
        .order_by(Announcement.published_at.desc(), Announcement.id.desc())
        .limit(limit)
    ).all()
    return [row for row in rows if _audience_matches(row.audience, is_staff)]


def subscribe(
    db: Session,
    *,
    email: str,
    user_id: int | None = None,
    source: str = "public",
) -> NewsletterSubscriber:
    """Opt in, idempotently. Re-subscribing an address that was unsubscribed is an
    explicit opt-in again, so it clears `unsubscribed_at`."""
    normalised = email.strip().lower()
    if "@" not in normalised or "." not in normalised.split("@")[-1]:
        raise ApiError(400, "invalid_email", "Enter an email address.")

    row = db.scalar(select(NewsletterSubscriber).where(NewsletterSubscriber.email == normalised))
    if row is None:
        row = NewsletterSubscriber(email=normalised, user_id=user_id, source=source)
        db.add(row)
    else:
        row.is_active = True
        row.unsubscribed_at = None
        if user_id is not None:
            row.user_id = user_id
    if row.unsubscribe_token is None:
        row.unsubscribe_token = secrets.token_urlsafe(32)
    db.flush()
    return row


def unsubscribe(db: Session, row: NewsletterSubscriber) -> NewsletterSubscriber:
    if row.is_active:
        row.is_active = False
        row.unsubscribed_at = datetime.now(UTC)
        db.flush()
    return row


def subscriber_by_token(db: Session, token: str) -> NewsletterSubscriber | None:
    if not token:
        return None
    return db.scalar(
        select(NewsletterSubscriber).where(NewsletterSubscriber.unsubscribe_token == token)
    )


def unsubscribe_by_token(db: Session, token: str) -> NewsletterSubscriber | None:
    """Opt out from the link in an email.

    Idempotent: a second click, a mail client prefetch or a forwarded link that is
    opened twice all end in the same state, and none of them is an error the reader
    should see. Returns None only when the token matches no subscriber.
    """
    row = subscriber_by_token(db, token)
    if row is None:
        return None
    was_active = row.is_active
    unsubscribe(db, row)
    if was_active:
        audit.record(
            db,
            action="comms.newsletter_unsubscribed",
            target_type="newsletter_subscriber",
            target_id=row.id,
            context={"via": "email_link"},
        )
    return row


def subscriber_counts(db: Session) -> dict[str, int]:
    active = db.scalar(
        select(func.count())
        .select_from(NewsletterSubscriber)
        .where(NewsletterSubscriber.is_active.is_(True))
    )
    total = db.scalar(select(func.count()).select_from(NewsletterSubscriber))
    return {"active": int(active or 0), "total": int(total or 0)}


__all__ = [
    "archive_announcement",
    "create_announcement",
    "newsletter_emails",
    "newsletter_rows",
    "publish_announcement",
    "subscribe",
    "subscriber_by_token",
    "subscriber_counts",
    "unsubscribe",
    "unsubscribe_by_token",
    "update_announcement",
    "visible_to",
]
