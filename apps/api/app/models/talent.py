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
APPLICATION_OFFERED = "offered"
APPLICATION_ACCEPTED = "accepted"
APPLICATION_IN_PROGRESS = "in_progress"
APPLICATION_SUBMITTED = "submitted"
APPLICATION_COMPLETED = "completed"
APPLICATION_REJECTED = "rejected"
APPLICATION_EXPIRED = "expired"
APPLICATION_STATUSES: tuple[str, ...] = (
    APPLICATION_INTERESTED,
    APPLICATION_APPLIED,
    APPLICATION_SHORTLISTED,
    APPLICATION_OFFERED,
    APPLICATION_ACCEPTED,
    APPLICATION_IN_PROGRESS,
    APPLICATION_SUBMITTED,
    APPLICATION_COMPLETED,
    APPLICATION_REJECTED,
    APPLICATION_WITHDRAWN,
    APPLICATION_EXPIRED,
)

# The lifecycle an application actually moves through, in order. Kept as a plain
# table rather than a state machine class: the whole point is that ops cannot
# skip a step, and a reviewer can read the allowed moves in one place.
#
# interested -> applied -> shortlisted -> offered -> accepted -> in_progress
#   -> submitted -> completed (paid downstream by the ledger)
# `submitted` can go back to `in_progress` for rework; `rejected` is reachable
# from any screening step; `withdrawn` (student) and `expired` (deadline passed)
# are reachable before work starts. completed/rejected/withdrawn/expired are
# terminal: no transition leaves them, so a paid application cannot be quietly
# reopened by a status edit.
APPLICATION_TRANSITIONS: dict[str, tuple[str, ...]] = {
    APPLICATION_INTERESTED: (APPLICATION_APPLIED, APPLICATION_WITHDRAWN, APPLICATION_EXPIRED),
    APPLICATION_APPLIED: (
        APPLICATION_SHORTLISTED,
        APPLICATION_REJECTED,
        APPLICATION_WITHDRAWN,
        APPLICATION_EXPIRED,
    ),
    APPLICATION_SHORTLISTED: (
        APPLICATION_OFFERED,
        APPLICATION_REJECTED,
        APPLICATION_WITHDRAWN,
        APPLICATION_EXPIRED,
    ),
    APPLICATION_OFFERED: (
        APPLICATION_ACCEPTED,
        APPLICATION_REJECTED,
        APPLICATION_WITHDRAWN,
        APPLICATION_EXPIRED,
    ),
    APPLICATION_ACCEPTED: (APPLICATION_IN_PROGRESS, APPLICATION_WITHDRAWN),
    APPLICATION_IN_PROGRESS: (APPLICATION_SUBMITTED, APPLICATION_WITHDRAWN),
    APPLICATION_SUBMITTED: (APPLICATION_COMPLETED, APPLICATION_IN_PROGRESS, APPLICATION_REJECTED),
    APPLICATION_COMPLETED: (),
    APPLICATION_REJECTED: (),
    APPLICATION_WITHDRAWN: (),
    APPLICATION_EXPIRED: (),
}

# Statuses that mean a human (or the clock) decided something about the
# application, so `decided_at` is stamped when entering them.
APPLICATION_DECIDED_STATUSES: frozenset[str] = frozenset(
    {
        APPLICATION_SHORTLISTED,
        APPLICATION_OFFERED,
        APPLICATION_ACCEPTED,
        APPLICATION_SUBMITTED,
        APPLICATION_COMPLETED,
        APPLICATION_REJECTED,
        APPLICATION_WITHDRAWN,
        APPLICATION_EXPIRED,
    }
)

# The application has turned into real work at this point; the money module and
# the work module read this set rather than comparing strings inline.
APPLICATION_WORK_STATUSES: frozenset[str] = frozenset(
    {APPLICATION_ACCEPTED, APPLICATION_IN_PROGRESS, APPLICATION_SUBMITTED, APPLICATION_COMPLETED}
)


def can_transition(current: str, target: str) -> bool:
    """True when `target` is an allowed next state. An unchanged status is not a
    transition -- callers treat it as a no-op instead of a failed edit."""
    return target in APPLICATION_TRANSITIONS.get(current, ())


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
