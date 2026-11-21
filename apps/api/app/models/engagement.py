"""Notifications and messages (PRD §8).

Two channels, one record: an in-app notification is a row a student reads, and
the same row is what the push job delivers. Keeping the row as the source of truth
means a push that fails is a retry, not a lost message.

`Message` is assignment-scoped rather than a general social inbox: the PRD has no
Community product, and every message in V2 exists to move work forward (rework,
clarification, payment).
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin
from app.models.admin import JSONPayload

# Notification kinds mirror the journey stages that need a nudge.
NOTIFY_ASSIGNMENT = "assignment"
NOTIFY_REVIEW = "review"
NOTIFY_REWORK = "rework"
NOTIFY_PAYMENT = "payment"
NOTIFY_INVITE = "invite"
NOTIFY_VERIFICATION = "verification"
NOTIFY_SYSTEM = "system"
NOTIFY_KINDS: tuple[str, ...] = (
    NOTIFY_ASSIGNMENT,
    NOTIFY_REVIEW,
    NOTIFY_REWORK,
    NOTIFY_PAYMENT,
    NOTIFY_INVITE,
    NOTIFY_VERIFICATION,
    NOTIFY_SYSTEM,
)


class Notification(Base, TimestampMixin):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    kind: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    body: Mapped[str] = mapped_column(String(500), nullable=False)
    # Free-form reference: {"assignment_id": 12} or {"payout_id": 3}.
    data: Mapped[dict | None] = mapped_column(JSONPayload)
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    pushed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class PushDevice(Base, TimestampMixin):
    """One install that can receive push (D1/F4).

    The token is the address; `platform` says which transport it belongs to.
    A token can move between accounts on a shared phone, so the same token is
    unique and is reassigned to the newest owner rather than duplicated.

    A browser install has no provider token: its address is the service-worker
    subscription endpoint, and the encryption keys needed to deliver to it live
    in `subscription`. Native installs leave `subscription` empty.
    """

    __tablename__ = "push_devices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    token: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)
    platform: Mapped[str] = mapped_column(
        String(10), default="android", server_default="android", nullable=False
    )
    # Web Push subscription: {endpoint, p256dh, auth}. Null for ios/android.
    subscription: Mapped[dict[str, Any] | None] = mapped_column(JSONPayload, nullable=True)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (UniqueConstraint("token", name="uq_push_devices_token"),)


class Message(Base, TimestampMixin):
    """A message tied to a piece of work, not a chat product."""

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sender_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    recipient_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assignment_id: Mapped[int | None] = mapped_column(
        ForeignKey("assignments.id", ondelete="CASCADE"), index=True
    )
    body: Mapped[str] = mapped_column(Text, nullable=False)
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
