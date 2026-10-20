"""Verification: proof, not claims (PRD §5, domain map `05`).

The rule this module encodes is the product's core promise: a student becomes
verified by **passing an assessment with known answers**, not by watching
lessons or pressing complete. So:

* `VerificationRecord` holds the *current* state for one student and one skill.
* `VerificationEvent` is the append-only history of every transition, and each
  row must name the evidence that caused it (`evidence_type` + `evidence_id`).
  There is no way to change a status without writing an event, because the
  service that changes it writes both in one transaction (M3).
* `Assessment` + `AssessmentTask` are the gold-standard input: known answers,
  a pass threshold and an attempt limit, all configuration.
* `PracticalTask` is the second evidence source: real work judged against a rubric.
* `TranscriptEntry` is the student-facing record, and every entry points at the
  evidence it came from — there is no free-text "skill" a student can claim.

Quality on real work (M5) feeds this module through the same event log, which is
what makes "good work strengthens it, poor quality weakens it" true rather than
aspirational.
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin
from app.models.admin import JSONPayload

# The five states from the PRD. `at_risk` and `suspended` are reached from real
# work quality (M5), never from inactivity alone.
UNVERIFIED = "unverified"
IN_PROGRESS = "in_progress"
VERIFIED = "verified"
AT_RISK = "at_risk"
SUSPENDED = "suspended"
VERIFICATION_STATUSES: tuple[str, ...] = (UNVERIFIED, IN_PROGRESS, VERIFIED, AT_RISK, SUSPENDED)

# What is allowed to move a state. `lesson` is deliberately absent.
EVIDENCE_ASSESSMENT = "assessment"
EVIDENCE_PRACTICAL_TASK = "practical_task"
EVIDENCE_QUALITY_RECORD = "quality_record"
EVIDENCE_OVERRIDE = "manual_override"
EVIDENCE_TYPES: tuple[str, ...] = (
    EVIDENCE_ASSESSMENT,
    EVIDENCE_PRACTICAL_TASK,
    EVIDENCE_QUALITY_RECORD,
    EVIDENCE_OVERRIDE,
)

# Transcript kinds: what was learned, what was proved, what was delivered.
TRANSCRIPT_LEARNED = "learned"
TRANSCRIPT_PROVED = "proved"
TRANSCRIPT_DELIVERED = "delivered"
TRANSCRIPT_KINDS: tuple[str, ...] = (TRANSCRIPT_LEARNED, TRANSCRIPT_PROVED, TRANSCRIPT_DELIVERED)


class VerificationRecord(Base, TimestampMixin):
    """One row per student and skill: the badge's current state."""

    __tablename__ = "verification_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(
        String(16), default=UNVERIFIED, server_default=UNVERIFIED, nullable=False
    )
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    # When the rules last ran (pass, fail, quality update). Used to explain staleness.
    last_evaluated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("user_id", "skill_id", name="uq_verification_user_skill"),
    )


class VerificationEvent(Base):
    """Append-only transition log. Never updated; it is the audit trail of proof."""

    __tablename__ = "verification_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    record_id: Mapped[int] = mapped_column(
        ForeignKey("verification_records.id", ondelete="CASCADE"), nullable=False, index=True
    )
    from_status: Mapped[str | None] = mapped_column(String(16))
    to_status: Mapped[str] = mapped_column(String(16), nullable=False)
    evidence_type: Mapped[str] = mapped_column(String(30), nullable=False)
    # String, because the evidence may be an assessment attempt, a submission or a
    # quality review — one column, not three nullable foreign keys.
    evidence_id: Mapped[str] = mapped_column(String(64), nullable=False)
    reason: Mapped[str | None] = mapped_column(String(255))
    # Null for system decisions (assessment auto-graded); set for a human override.
    actor_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )


class Assessment(Base, TimestampMixin):
    """A practical assessment: gold-standard tasks, a threshold, a attempt limit."""

    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True
    )
    slug: Mapped[str] = mapped_column(String(80), nullable=False, unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    # Percentage of available points needed to pass (0-100), not a raw score.
    pass_threshold: Mapped[int] = mapped_column(
        Integer, default=80, server_default="80", nullable=False
    )
    max_attempts: Mapped[int] = mapped_column(Integer, default=3, server_default="3", nullable=False)
    # How many of the assessment's tasks a sitting presents (randomised selection).
    task_count: Mapped[int] = mapped_column(Integer, default=5, server_default="5", nullable=False)
    status: Mapped[str] = mapped_column(
        String(16), default="draft", server_default="draft", nullable=False
    )


class AssessmentTask(Base, TimestampMixin):
    """One gold-standard task: the input shown, the answer known to be correct."""

    __tablename__ = "assessment_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    assessment_id: Mapped[int] = mapped_column(
        ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    ordinal: Mapped[int] = mapped_column(Integer, nullable=False)
    # SET NULL: retiring a task template must not silently delete assessment items
    # that already graded real attempts; the payload below is self-contained.
    template_id: Mapped[int | None] = mapped_column(
        ForeignKey("task_templates.id", ondelete="SET NULL")
    )
    payload: Mapped[dict] = mapped_column(JSONPayload, nullable=False)
    expected_answer: Mapped[dict] = mapped_column(JSONPayload, nullable=False)
    points: Mapped[int] = mapped_column(Integer, default=1, server_default="1", nullable=False)

    __table_args__ = (
        UniqueConstraint("assessment_id", "ordinal", name="uq_assessment_task_ordinal"),
    )


class AssessmentAttempt(Base):
    """A sitting. Multiple rows are expected: `max_attempts` is a service rule."""

    __tablename__ = "assessment_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    assessment_id: Mapped[int] = mapped_column(
        ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    # The randomised selection is frozen at start, so a replayed submit grades the
    # same tasks rather than a fresh draw.
    presented_task_ids: Mapped[list | None] = mapped_column(JSONPayload)
    answers: Mapped[dict | None] = mapped_column(JSONPayload)
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    score: Mapped[int | None] = mapped_column(Integer)  # percentage, 0-100
    passed: Mapped[bool | None] = mapped_column(Boolean)


class PracticalTask(Base, TimestampMixin):
    """Real work judged against a rubric — the second way to earn verification."""

    __tablename__ = "practical_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True
    )
    slug: Mapped[str] = mapped_column(String(80), nullable=False, unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    brief_md: Mapped[str] = mapped_column(
        Text, default="", server_default="", nullable=False
    )
    rubric: Mapped[dict | None] = mapped_column(JSONPayload)
    status: Mapped[str] = mapped_column(
        String(16), default="draft", server_default="draft", nullable=False
    )


class PracticalSubmission(Base, TimestampMixin):
    """A student's answer to a practical task, and the reviewer's rubric score."""

    __tablename__ = "practical_submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    practical_task_id: Mapped[int] = mapped_column(
        ForeignKey("practical_tasks.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    payload: Mapped[dict] = mapped_column(JSONPayload, nullable=False)
    status: Mapped[str] = mapped_column(
        String(16), default="submitted", server_default="submitted", nullable=False
    )
    score: Mapped[int | None] = mapped_column(Integer)  # percentage, 0-100
    passed: Mapped[bool | None] = mapped_column(Boolean)
    reviewed_by: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    review_notes: Mapped[str | None] = mapped_column(Text)
    client_key: Mapped[str | None] = mapped_column(String(64), unique=True)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class TranscriptEntry(Base):
    """A line in the Skill Transcript, always linked to its evidence.

    The unique constraint is the anti-duplication rule: re-running the projection
    or replaying an event cannot create a second "proved" line for the same
    assessment attempt.
    """

    __tablename__ = "transcript_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    skill_id: Mapped[int | None] = mapped_column(ForeignKey("skills.id", ondelete="SET NULL"))
    kind: Mapped[str] = mapped_column(String(16), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    evidence_type: Mapped[str] = mapped_column(String(30), nullable=False)
    evidence_id: Mapped[str] = mapped_column(String(64), nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id", "kind", "evidence_type", "evidence_id", name="uq_transcript_evidence"
        ),
    )
