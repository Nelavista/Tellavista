"""Quality control: the standard, the review and the record (PRD §8).

Quality is a first-class stage, not a moderation afterthought. Three tables carry
the rule:

* `QualityStandard` is the standard a project's work is judged against. It is
  configuration (thresholds, sampling rates, consequence rules), so a new project
  is rows, not a branch.
* `QualityReview` is one human (or gold-task) verdict on one submission. Reviews
  are append-only: a reviewer who changes their mind creates a new review, and the
  latest one is the current verdict. That keeps "why was this paid?" answerable.
* `QualityRecord` is the rolling per-student score that feeds verification,
  matching and the Talent profile. It is a projection of reviews and can always be
  recomputed from them.

Gold tasks are the anti-drift mechanism: a submission marked `is_gold` has a known
correct answer, so the reviewer's verdict can be checked against it. The agreement
between the two is what makes a reviewer's judgement trustworthy.
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin
from app.models.admin import JSONPayload

VERDICT_APPROVED = "approved"
VERDICT_REWORK = "rework"
VERDICT_REJECTED = "rejected"
VERDICTS: tuple[str, ...] = (VERDICT_APPROVED, VERDICT_REWORK, VERDICT_REJECTED)

# Consequence kinds, least to most severe. Every one is configurable per project.
CONSEQUENCE_WARN = "warn"
CONSEQUENCE_RESTRICT_MATCHING = "restrict_matching"
CONSEQUENCE_REQUIRE_REVERIFICATION = "require_reverification"
CONSEQUENCE_REMOVE_FROM_PROJECT = "remove_from_project"
CONSEQUENCE_KINDS: tuple[str, ...] = (
    CONSEQUENCE_WARN,
    CONSEQUENCE_RESTRICT_MATCHING,
    CONSEQUENCE_REQUIRE_REVERIFICATION,
    CONSEQUENCE_REMOVE_FROM_PROJECT,
)

# Default rules. Ops can override any of them per project in `rules`.
DEFAULT_RULES: dict = {
    # Percentage of live work that is a gold task.
    "gold_rate_percent": 10,
    # Percentage of submissions reviewed twice (agreement scoring).
    "double_review_percent": 5,
    # Rolling score below this is a failed quality bar.
    "pass_threshold": 80,
    # Number of consecutive poor reviews before each consequence fires.
    "warn_after": 1,
    "restrict_matching_after": 2,
    "require_reverification_after": 3,
    "remove_from_project_after": 5,
}


class QualityStandard(Base, TimestampMixin):
    """The bar for one project. One active standard per project."""

    __tablename__ = "quality_standards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    instructions_md: Mapped[str] = mapped_column(Text, default="", server_default="", nullable=False)
    # Rubric is a list of criteria: [{"key": "accuracy", "weight": 60}].
    rubric: Mapped[list | None] = mapped_column(JSONPayload)
    pass_threshold: Mapped[int] = mapped_column(
        Integer, default=80, server_default="80", nullable=False
    )
    rules: Mapped[dict] = mapped_column(JSONPayload, nullable=False)


class QualityReview(Base):
    """One verdict on one submission. Append-only; the latest review wins."""

    __tablename__ = "quality_reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    submission_id: Mapped[int] = mapped_column(
        ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    reviewer_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    verdict: Mapped[str] = mapped_column(String(16), nullable=False)
    score: Mapped[int | None] = mapped_column(Integer)
    notes: Mapped[str | None] = mapped_column(Text)
    # True when the reviewer judged a gold task; `gold_correct` is then the check.
    is_gold: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    gold_correct: Mapped[bool | None] = mapped_column(Boolean)
    # Second review of the same submission points at the first (agreement scoring).
    agrees_with_review_id: Mapped[int | None] = mapped_column(
        ForeignKey("quality_reviews.id", ondelete="SET NULL")
    )
    # True for an ops override; `reason` is then mandatory.
    is_override: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    reason: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )


class QualityRecord(Base, TimestampMixin):
    """Rolling quality score per student (per project, and `project_id NULL` overall).

    `average_score` is a 0-100 integer. It is a projection: `recompute` in the
    service rebuilds it from reviews, so a support question ("why is my score 62?")
    can be answered by listing the reviews that produced it.
    """

    __tablename__ = "quality_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )
    reviews_count: Mapped[int] = mapped_column(
        Integer, default=0, server_default="0", nullable=False
    )
    approvals: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)
    reworks: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)
    rejections: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)
    average_score: Mapped[int] = mapped_column(
        Integer, default=0, server_default="0", nullable=False
    )
    gold_tasks: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)
    gold_correct: Mapped[int] = mapped_column(
        Integer, default=0, server_default="0", nullable=False
    )
    # Consecutive poor reviews. Reset by an approval, so consequences are about a
    # pattern rather than a lifetime total.
    poor_streak: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)
    last_review_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("user_id", "project_id", name="uq_quality_record_user_project"),
    )


class QualityConsequence(Base, TimestampMixin):
    """A consequence applied to a student, with the rule and reason that fired it."""

    __tablename__ = "quality_consequences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    quality_record_id: Mapped[int | None] = mapped_column(
        ForeignKey("quality_records.id", ondelete="SET NULL")
    )
    actor_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true", nullable=False
    )
    lifted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
