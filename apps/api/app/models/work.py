"""Work: projects, cohorts, assignments and submissions (PRD §8).

A managed opportunity becomes one `Project`; students are grouped into cohorts,
receive assignments drawn from task templates, and submit work. Submissions carry
a client-generated `idempotency_key`, so a retry from a flaky connection records
one submission, not two — the same guarantee ADR-0007 makes for every write that
matters.

Quality review (approve / rework / reject) is M5's `quality` module. The status
column here is the work's own lifecycle, not the quality verdict.
"""
from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin
from app.models.admin import JSONPayload

PROJECT_DRAFT = "draft"
PROJECT_ACTIVE = "active"
PROJECT_PAUSED = "paused"
PROJECT_COMPLETED = "completed"

COHORT_FORMING = "forming"
COHORT_ACTIVE = "active"
COHORT_CLOSED = "closed"

MEMBER_INVITED = "invited"
MEMBER_ACTIVE = "active"
MEMBER_REMOVED = "removed"
MEMBER_COMPLETED = "completed"

ASSIGNMENT_ASSIGNED = "assigned"
ASSIGNMENT_IN_PROGRESS = "in_progress"
ASSIGNMENT_SUBMITTED = "submitted"
ASSIGNMENT_APPROVED = "approved"
ASSIGNMENT_REWORK = "rework"
ASSIGNMENT_REJECTED = "rejected"

SUBMISSION_SUBMITTED = "submitted"
SUBMISSION_APPROVED = "approved"
SUBMISSION_REWORK = "rework"
SUBMISSION_REJECTED = "rejected"


class Project(Base, TimestampMixin):
    """One managed project per opportunity; the container for work and money."""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    opportunity_id: Mapped[int] = mapped_column(
        ForeignKey("opportunities.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    slug: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(
        String(16), default=PROJECT_DRAFT, server_default=PROJECT_DRAFT, nullable=False
    )
    starts_on: Mapped[date | None] = mapped_column(Date)
    ends_on: Mapped[date | None] = mapped_column(Date)


class Cohort(Base, TimestampMixin):
    """A group of students running the same work for one project."""

    __tablename__ = "cohorts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    capacity: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(
        String(16), default=COHORT_FORMING, server_default=COHORT_FORMING, nullable=False
    )


class CohortMember(Base, TimestampMixin):
    """Invitation and participation state. Removal is recorded, never deleted."""

    __tablename__ = "cohort_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cohort_id: Mapped[int] = mapped_column(
        ForeignKey("cohorts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(
        String(16), default=MEMBER_INVITED, server_default=MEMBER_INVITED, nullable=False
    )
    joined_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (UniqueConstraint("cohort_id", "user_id", name="uq_cohort_member"),)


class Assignment(Base, TimestampMixin):
    """A piece of work given to one student, drawn from a task template."""

    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    cohort_id: Mapped[int | None] = mapped_column(
        ForeignKey("cohorts.id", ondelete="SET NULL"), index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    template_id: Mapped[int | None] = mapped_column(
        ForeignKey("task_templates.id", ondelete="SET NULL")
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(
        String(16), default=ASSIGNMENT_ASSIGNED, server_default=ASSIGNMENT_ASSIGNED, nullable=False
    )
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Submission(Base, TimestampMixin):
    """A student's answer to an assignment, safe to retry.

    `idempotency_key` is unique: the client generates it once per logical
    submission and resends it after a dropped connection, so the same work is
    stored once. A NULL key is allowed for ops-created rows, hence uniqueness
    rather than non-nullability.
    """

    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    assignment_id: Mapped[int] = mapped_column(
        ForeignKey("assignments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    payload: Mapped[dict] = mapped_column(JSONPayload, nullable=False)
    status: Mapped[str] = mapped_column(
        String(16), default=SUBMISSION_SUBMITTED, server_default=SUBMISSION_SUBMITTED, nullable=False
    )
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    idempotency_key: Mapped[str | None] = mapped_column(String(64), unique=True)
    # Gold tasks are mixed into live work so a reviewer's judgement can be checked
    # against a known answer. `gold_expected` is never sent to the student.
    is_gold: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    gold_expected: Mapped[dict | None] = mapped_column(JSONPayload)
