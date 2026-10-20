"""Skills: the Learn → Practise → Build spine (PRD §4, domain map `05`).

The design rule for this module is the PRD's own: **skill number two must be
content, not code.** So a learning path is rows (path → ordered steps → lessons),
and the practice stage is driven by `TaskTemplate`, whose instructions, input
shape, expected answer shape and validation rule are all configuration. Adding
"entity tagging" or "image labelling" later means inserting templates, not
shipping a branch.

What this module deliberately does **not** contain is verification. A completed
lesson is `LessonProgress`, which is a progress record; it can never make a
student verified. Verification is granted in M3 from assessments and practical
tasks with known answers, and is strengthened or weakened by quality on real work
(M5). `lessons.status` and `task_templates.status` are the draft/publish gate the
M2 ops slice operates.
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin
from app.models.admin import JSONPayload

# Content lifecycle. A published lesson or template is what a student sees; drafts
# are ops-only and must never leak into the student API.
STATUS_DRAFT = "draft"
STATUS_PUBLISHED = "published"
STATUS_ARCHIVED = "archived"
CONTENT_STATUSES: tuple[str, ...] = (STATUS_DRAFT, STATUS_PUBLISHED, STATUS_ARCHIVED)

# What a step in a learning path can be. The first three map onto the journey;
# `assessment` is a link out to M3's assessments, never a lesson in disguise.
STEP_KINDS: tuple[str, ...] = ("lesson", "practice", "project", "assessment")

NOT_STARTED = "not_started"
IN_PROGRESS = "in_progress"
COMPLETED = "completed"


class SkillCategory(Base, TimestampMixin):
    """Groups skills for discovery, e.g. "AI & Data", "Design"."""

    __tablename__ = "skill_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(80), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500))
    ordinal: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)


class Skill(Base, TimestampMixin):
    """A skill someone can be verified in — "AI Data Annotation" is the first."""

    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # SET NULL: retiring a category must not delete the skills inside it.
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("skill_categories.id", ondelete="SET NULL"), index=True
    )
    slug: Mapped[str] = mapped_column(String(80), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000))
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true", nullable=False
    )


class LearningPath(Base, TimestampMixin):
    """The ordered route from knowing nothing to being ready to be assessed."""

    __tablename__ = "learning_paths"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True
    )
    slug: Mapped[str] = mapped_column(String(80), nullable=False, unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    summary: Mapped[str | None] = mapped_column(String(500))
    level: Mapped[str] = mapped_column(
        String(20), default="beginner", server_default="beginner", nullable=False
    )
    estimated_hours: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(
        String(16), default=STATUS_DRAFT, server_default=STATUS_DRAFT, nullable=False
    )


class Lesson(Base, TimestampMixin):
    """A unit of learning. Finishing it changes nothing but `LessonProgress`."""

    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True
    )
    slug: Mapped[str] = mapped_column(String(80), nullable=False, unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    body_md: Mapped[str] = mapped_column(Text, default="", server_default="", nullable=False)
    estimated_minutes: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(
        String(16), default=STATUS_DRAFT, server_default=STATUS_DRAFT, nullable=False
    )


class LearningPathStep(Base, TimestampMixin):
    """One position in a path. A lesson step points at a lesson; a project step
    points at the project the student builds in M2."""

    __tablename__ = "learning_path_steps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    path_id: Mapped[int] = mapped_column(
        ForeignKey("learning_paths.id", ondelete="CASCADE"), nullable=False, index=True
    )
    ordinal: Mapped[int] = mapped_column(Integer, nullable=False)
    kind: Mapped[str] = mapped_column(String(16), nullable=False)
    title: Mapped[str | None] = mapped_column(String(200))
    # SET NULL: a lesson can be rewritten or retired without breaking path order;
    # the step then shows as "coming soon" rather than disappearing.
    lesson_id: Mapped[int | None] = mapped_column(ForeignKey("lessons.id", ondelete="SET NULL"))
    # A practice or project step points at the task template the student works on;
    # an assessment step points at the assessment via `verification`.
    task_template_id: Mapped[int | None] = mapped_column(
        ForeignKey("task_templates.id", ondelete="SET NULL")
    )

    __table_args__ = (
        UniqueConstraint("path_id", "ordinal", name="uq_path_step_ordinal"),
    )


class TaskTemplate(Base, TimestampMixin):
    """A configurable annotation task type — the core of "skill two is content".

    `input_schema` describes what the student is shown, `answer_schema` what they
    submit, and `config` holds the knobs a validator needs (minimum entities,
    allowed labels, time limit). `version` exists because a live cohort must not
    have its task silently redefined underneath it: a new definition is a new
    version (or a new slug), and existing work keeps pointing at the old row.

    `validator` names a rule the API implements once ("exact_key",
    "label_set", "span_overlap"); a task type that needs a *new* validator is the
    one case that is code, and it is a small, tested, registered function.
    """

    __tablename__ = "task_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True
    )
    slug: Mapped[str] = mapped_column(String(80), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    instructions_md: Mapped[str] = mapped_column(
        Text, default="", server_default="", nullable=False
    )
    input_schema: Mapped[dict] = mapped_column(JSONPayload, nullable=False)
    answer_schema: Mapped[dict] = mapped_column(JSONPayload, nullable=False)
    validator: Mapped[str] = mapped_column(
        String(40), default="exact_key", server_default="exact_key", nullable=False
    )
    config: Mapped[dict | None] = mapped_column(JSONPayload)
    version: Mapped[int] = mapped_column(Integer, default=1, server_default="1", nullable=False)
    status: Mapped[str] = mapped_column(
        String(16), default=STATUS_DRAFT, server_default=STATUS_DRAFT, nullable=False
    )


class LessonProgress(Base, TimestampMixin):
    """Progress, not proof.

    The honesty rule from the PRD: completing every lesson leaves a student
    **unverified**. This table exists so "what did I study recently" and "what
    should I practise" have data; verification reads assessments instead.
    """

    __tablename__ = "lesson_progress"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(
        String(16), default=NOT_STARTED, server_default=NOT_STARTED, nullable=False
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("user_id", "lesson_id", name="uq_lesson_progress_user_lesson"),
    )


class PracticeAttempt(Base):
    """One practice answer with instant feedback.

    Practice is *not* evidence: `is_correct` here never reaches verification. It
    exists so "what should I practise next?" has data and so the deterministic
    validator has a place to write its verdict.
    """

    __tablename__ = "practice_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    template_id: Mapped[int] = mapped_column(
        ForeignKey("task_templates.id", ondelete="CASCADE"), nullable=False, index=True
    )
    answer: Mapped[dict] = mapped_column(JSONPayload, nullable=False)
    is_correct: Mapped[bool | None] = mapped_column(Boolean)
    feedback: Mapped[str | None] = mapped_column(Text)
    duration_ms: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
