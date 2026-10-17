"""Matching: why you qualify, or exactly what is missing (PRD §6).

Matching is not a job board. Every result is stored with its reasoning, and every
unmet requirement produces a `SkillGap` that points back at the learning path or
assessment which closes it — so a "no" always has a next step.

`Opportunity.type` is the fee switch: managed work (the 10% fee applies) versus
external opportunities (never a fee). Keeping that on the row, rather than in
code, means the money module can refuse to create a ledger entry for an external
opportunity by checking one column.
"""
from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin
from app.models.admin import JSONPayload

OPPORTUNITY_MANAGED = "managed"
OPPORTUNITY_EXTERNAL = "external"
OPPORTUNITY_TYPES: tuple[str, ...] = (OPPORTUNITY_MANAGED, OPPORTUNITY_EXTERNAL)

REQUIREMENT_SKILL = "skill"
REQUIREMENT_VERIFICATION = "verification"
REQUIREMENT_LANGUAGE = "language"
REQUIREMENT_UNIVERSITY = "university"
REQUIREMENT_AVAILABILITY = "availability"
REQUIREMENT_LOCATION = "location"
REQUIREMENT_KINDS: tuple[str, ...] = (
    REQUIREMENT_SKILL,
    REQUIREMENT_VERIFICATION,
    REQUIREMENT_LANGUAGE,
    REQUIREMENT_UNIVERSITY,
    REQUIREMENT_AVAILABILITY,
    REQUIREMENT_LOCATION,
)

GAP_MISSING = "missing"
GAP_MET = "met"


class Opportunity(Base, TimestampMixin):
    """Managed paid work (fee applies) or an external listing (no fee)."""

    __tablename__ = "opportunities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(
        String(16), default=OPPORTUNITY_MANAGED, server_default=OPPORTUNITY_MANAGED, nullable=False
    )
    slug: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", server_default="", nullable=False)
    # Company-side steps are run by our team by hand first; the fields exist so a
    # self-service surface can sit on top later without a rebuild.
    client_name: Mapped[str | None] = mapped_column(String(200))
    department_id: Mapped[int | None] = mapped_column(
        ForeignKey("departments.id", ondelete="SET NULL"), index=True
    )
    headcount: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(
        String(16), default="draft", server_default="draft", nullable=False
    )
    # The quality standard is a named text reference until M5 introduces
    # quality_standards; the foreign key arrives with that table.
    quality_standard: Mapped[str | None] = mapped_column(String(200))
    # Integer minor units + ISO 4217 code. No floats anywhere near money (ADR-0008).
    currency: Mapped[str | None] = mapped_column(String(3))
    rate_minor: Mapped[int | None] = mapped_column(Integer)
    starts_on: Mapped[date | None] = mapped_column(Date)
    ends_on: Mapped[date | None] = mapped_column(Date)
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))


class Requirement(Base, TimestampMixin):
    """One thing an opportunity demands. `skill` rows drive the gap calculation."""

    __tablename__ = "requirements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    opportunity_id: Mapped[int] = mapped_column(
        ForeignKey("opportunities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    kind: Mapped[str] = mapped_column(String(20), nullable=False)
    skill_id: Mapped[int | None] = mapped_column(
        ForeignKey("skills.id", ondelete="SET NULL"), index=True
    )
    # For verification: the required status ("verified"). For language/university/
    # location: the value. Kept as text so a new requirement kind needs no column.
    minimum_value: Mapped[str | None] = mapped_column(String(120))
    is_mandatory: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true", nullable=False
    )
    description: Mapped[str | None] = mapped_column(String(255))


class MatchResult(Base, TimestampMixin):
    """The stored verdict for one student and one opportunity, with its reasons."""

    __tablename__ = "match_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    opportunity_id: Mapped[int] = mapped_column(
        ForeignKey("opportunities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    eligible: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    score: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)
    # [{"requirement": 3, "met": false, "detail": "verification missing"}]
    explanation: Mapped[list | None] = mapped_column(JSONPayload)
    computed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("opportunity_id", "user_id", name="uq_match_opportunity_user"),
    )


class SkillGap(Base, TimestampMixin):
    """A missing requirement and the exact step that closes it.

    `closes_via_*` is the product rule made structural: a gap always points back
    into learning or verification, never into a dead end.
    """

    __tablename__ = "skill_gaps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    opportunity_id: Mapped[int] = mapped_column(
        ForeignKey("opportunities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    requirement_id: Mapped[int] = mapped_column(
        ForeignKey("requirements.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(
        String(16), default=GAP_MISSING, server_default=GAP_MISSING, nullable=False
    )
    detail: Mapped[str | None] = mapped_column(String(255))
    closes_via_learning_path_id: Mapped[int | None] = mapped_column(
        ForeignKey("learning_paths.id", ondelete="SET NULL")
    )
    closes_via_assessment_id: Mapped[int | None] = mapped_column(
        ForeignKey("assessments.id", ondelete="SET NULL")
    )

    __table_args__ = (
        UniqueConstraint("user_id", "requirement_id", name="uq_gap_user_requirement"),
    )
