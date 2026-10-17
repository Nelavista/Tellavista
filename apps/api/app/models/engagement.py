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

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
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
