"""Platform communications: announcements and the newsletter list.

Two things were missing from ops entirely, and they are the two an operations team
asks for within a week of launch: a way to announce something *inside* the product,
and a way to email the people who asked to hear from us.

`Announcement` is one row that can be delivered on two channels -- the in-product
banner (`platform`) and email (`email`). It is deliberately one table: the same
message usually goes to both, and splitting it into "banner" and "campaign" tables
is how the two versions start disagreeing. Publishing is the moment it becomes
visible/sent; `email_sent_at` and `email_recipient_count` record what the send
actually did, so a re-run cannot double-send silently.

`NewsletterSubscriber` is an email address and its consent state. It is separate
from `users` on purpose: most subscribers are not accounts, and an unsubscribed
address must stay on the list (as inactive) so a later import cannot quietly
re-subscribe someone who opted out.
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin

ANNOUNCEMENT_DRAFT = "draft"
ANNOUNCEMENT_PUBLISHED = "published"
ANNOUNCEMENT_ARCHIVED = "archived"
ANNOUNCEMENT_STATUSES: tuple[str, ...] = (
    ANNOUNCEMENT_DRAFT,
    ANNOUNCEMENT_PUBLISHED,
    ANNOUNCEMENT_ARCHIVED,
)

AUDIENCE_ALL = "all"
AUDIENCE_STUDENTS = "students"
AUDIENCE_STAFF = "staff"
AUDIENCES: tuple[str, ...] = (AUDIENCE_STUDENTS, AUDIENCE_STAFF, AUDIENCE_ALL)

CHANNEL_PLATFORM = "platform"
CHANNEL_EMAIL = "email"
CHANNEL_BOTH = "both"
CHANNELS: tuple[str, ...] = (CHANNEL_PLATFORM, CHANNEL_EMAIL, CHANNEL_BOTH)


class Announcement(Base, TimestampMixin):
    """A message ops publishes in the product and/or to the newsletter list."""

    __tablename__ = "announcements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    body: Mapped[str] = mapped_column(Text, default="", server_default="", nullable=False)
    audience: Mapped[str] = mapped_column(
        String(16), default=AUDIENCE_ALL, server_default=AUDIENCE_ALL, nullable=False
    )
    channel: Mapped[str] = mapped_column(
        String(16), default=CHANNEL_PLATFORM, server_default=CHANNEL_PLATFORM, nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(16), default=ANNOUNCEMENT_DRAFT, server_default=ANNOUNCEMENT_DRAFT, nullable=False
    )
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    archived_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    email_sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    # How many send jobs the publish actually enqueued -- not an estimate.
    email_recipient_count: Mapped[int] = mapped_column(
        Integer, default=0, server_default="0", nullable=False
    )
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))


class NewsletterSubscriber(Base):
    """One newsletter address with its consent state (active / unsubscribed)."""

    __tablename__ = "newsletter_subscribers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    source: Mapped[str] = mapped_column(
        String(40), default="public", server_default="public", nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true", nullable=False
    )
    # Opaque per-subscriber token for the unsubscribe link carried by every
    # newsletter email. Possession is the authorisation, so it is never returned
    # by an API response: a list of tokens would let one reader opt out everyone.
    unsubscribe_token: Mapped[str | None] = mapped_column(String(64), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    unsubscribed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
