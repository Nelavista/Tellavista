"""Talent: evidence-backed profile sharing and external opportunity interest (PRD §7).

The Talent profile itself is **computed** from evidence (verification, transcript,
approved work, quality) rather than stored as a student's claims. What is stored
here is the student's consent to share it:

* `TalentShare` is a revocable, expiring, scoped link. The token is stored hashed,
  so a database dump cannot be used to read a profile.
* `OpportunityApplication` records a student's interest in an external opportunity
  (and, for managed work, an invitation response). External opportunities never
  create a ledger entry — `Opportunity.type` is the switch the money module reads.
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin
from app.models.admin import JSONPayload

APPLICATION_INTERESTED = "interested"
APPLICATION_APPLIED = "applied"
APPLICATION_WITHDRAWN = "withdrawn"
APPLICATION_SHORTLISTED = "shortlisted"
APPLICATION_REJECTED = "rejected"
APPLICATION_STATUSES: tuple[str, ...] = (
    APPLICATION_INTERESTED,
    APPLICATION_APPLIED,
    APPLICATION_WITHDRAWN,
    APPLICATION_SHORTLISTED,
    APPLICATION_REJECTED,
)


class TalentShare(Base, TimestampMixin):
    """A student-owned, revocable grant to view part of their Talent profile."""

    __tablename__ = "talent_shares"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    token_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    label: Mapped[str | None] = mapped_column(String(120))
    # Scopes: ["transcript", "quality", "work_history"]. Empty means everything
    # the student is allowed to share.
    scopes: Mapped[list | None] = mapped_column(JSONPayload)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_viewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class OpportunityApplication(Base, TimestampMixin):
    """Interest in an external opportunity, or a response to a managed invitation."""

    __tablename__ = "opportunity_applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    opportunity_id: Mapped[int] = mapped_column(
        ForeignKey("opportunities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(
        String(20), default=APPLICATION_INTERESTED,
        server_default=APPLICATION_INTERESTED, nullable=False,
    )
    note: Mapped[str | None] = mapped_column(Text)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("opportunity_id", "user_id", name="uq_application_opportunity_user"),
    )
