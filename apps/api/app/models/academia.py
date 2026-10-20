"""Academia: University › Faculty › Department › Course › Material (PRD §3).

Phase 0 PR 0.2a completes the shape V1 already has as data (audit §2.3, domain
map `05`): the academic calendar (`AcademicSession`, `Semester`), what a student
is actually enrolled in (`Enrolment`), the course breakdown (`Topic`), the RAG
chunks (`MaterialChunk`) and the CBT question bank (`Question`,
`QuestionAttempt`).

The free-string `users.university/department/level` columns stay for now; Phase 1
backfills them from `Enrolment` and drops the strings in a later expand/contract
step. Nothing here grants verification: an attempt is a record of what a student
answered, never proof of skill.
"""
from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.admin import JSONPayload


class University(Base, TimestampMixin):
    __tablename__ = "universities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)


class Faculty(Base, TimestampMixin):
    __tablename__ = "faculties"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university_id: Mapped[int] = mapped_column(ForeignKey("universities.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    __table_args__ = (UniqueConstraint("university_id", "name", name="uq_faculty_university_name"),)


class Department(Base, TimestampMixin):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculties.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    __table_args__ = (UniqueConstraint("faculty_id", "name", name="uq_department_faculty_name"),)


class Course(Base, TimestampMixin):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id", ondelete="CASCADE"))
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    level: Mapped[str] = mapped_column(String(10), nullable=False)
    __table_args__ = (UniqueConstraint("department_id", "code", "level", name="uq_course_dept_level_code"),)

    materials: Mapped[list[Material]] = relationship(back_populates="course")


class Material(Base, TimestampMixin):
    __tablename__ = "materials"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int | None] = mapped_column(ForeignKey("courses.id", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    file_url: Mapped[str | None] = mapped_column(String(1024))
    source: Mapped[str] = mapped_column(String(30), default="local", nullable=False)

    course: Mapped[Course | None] = relationship(back_populates="materials")


# --- Phase 0 PR 0.2a: calendar, enrolment, course breakdown, CBT bank ---

# Session names are shared labels ("2025/2026"); the dates are what differ when a
# university's calendar shifts. A per-university override can be added without
# touching a single foreign key, because enrolment points at the session row.
class AcademicSession(Base, TimestampMixin):
    __tablename__ = "academic_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    starts_on: Mapped[date | None] = mapped_column(Date)
    ends_on: Mapped[date | None] = mapped_column(Date)
    # Exactly one current session is a service-level rule (Phase 1); the flag makes it
    # cheap to query and lets ops fix a bad calendar without a data migration.
    is_current: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )


class Semester(Base, TimestampMixin):
    __tablename__ = "semesters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("academic_sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    ordinal: Mapped[int] = mapped_column(Integer, nullable=False)
    starts_on: Mapped[date | None] = mapped_column(Date)
    ends_on: Mapped[date | None] = mapped_column(Date)

    __table_args__ = (UniqueConstraint("session_id", "ordinal", name="uq_semester_session_ordinal"),)


class Enrolment(Base, TimestampMixin):
    """A student's real registration for one course in one session (PRD §3).

    This is the record the onboarding wizard writes and the dashboard reads; the
    free-string `users.university/department/level` columns are a skeleton
    leftover, not the source of truth.
    """

    __tablename__ = "enrolments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    session_id: Mapped[int] = mapped_column(
        ForeignKey("academic_sessions.id", ondelete="CASCADE"), nullable=False
    )
    # Optional: not every university exposes a semester when registering.
    semester_id: Mapped[int | None] = mapped_column(ForeignKey("semesters.id", ondelete="SET NULL"))
    status: Mapped[str] = mapped_column(
        String(16), default="active", server_default="active", nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id", "course_id", "session_id", name="uq_enrolment_user_course_session"
        ),
    )


class Topic(Base, TimestampMixin):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    ordinal: Mapped[int] = mapped_column(Integer, nullable=False)
    summary: Mapped[str | None] = mapped_column(String(500))

    __table_args__ = (UniqueConstraint("course_id", "ordinal", name="uq_topic_course_ordinal"),)


class MaterialChunk(Base, TimestampMixin):
    """Retrieval unit for grounded Q&A (M8, ported from V1's `MaterialChunk`).

    The embedding column is deliberately absent: pgvector and the embedding
    dimension are M8 decisions, and a half-migrated store is worse than none.
    """

    __tablename__ = "material_chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    material_id: Mapped[int] = mapped_column(
        ForeignKey("materials.id", ondelete="CASCADE"), nullable=False, index=True
    )
    ordinal: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    token_count: Mapped[int | None] = mapped_column(Integer)

    __table_args__ = (
        UniqueConstraint("material_id", "ordinal", name="uq_chunk_material_ordinal"),
    )


class Question(Base, TimestampMixin):
    """A CBT question. Options are JSON so an imported bank needs no join table.

    `correct_key` refers to an option key (`"A"`..`"E"`), not to a position, so
    shuffling options for display does not corrupt the answer.
    """

    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    topic_id: Mapped[int | None] = mapped_column(ForeignKey("topics.id", ondelete="SET NULL"))
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    options: Mapped[list] = mapped_column(JSONPayload, nullable=False)
    correct_key: Mapped[str] = mapped_column(String(8), nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text)
    difficulty: Mapped[str] = mapped_column(
        String(10), default="medium", server_default="medium", nullable=False
    )
    source: Mapped[str] = mapped_column(
        String(30), default="seed", server_default="seed", nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true", nullable=False
    )


class QuestionAttempt(Base):
    """One answer to one question — a practice record, not evidence of skill.

    Verification (M3) is granted by assessments with known answers, never by
    practising. The shape is here so offline answer-saving has something to sync
    into, with `selected_key` nullable for an abandoned attempt.
    """

    __tablename__ = "question_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    selected_key: Mapped[str | None] = mapped_column(String(8))
    is_correct: Mapped[bool | None] = mapped_column(Boolean)
    duration_ms: Mapped[int | None] = mapped_column(Integer)
    # Client-generated key so an offline answer can be synced twice without
    # creating two attempts (ADR-0007). Nullable for server-created rows.
    client_key: Mapped[str | None] = mapped_column(String(64), unique=True)
    answered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class AskSession(Base, TimestampMixin):
    """One Ask Nelavista conversation, scoped to a course when the student chose one.

    Keeping the session is what makes the assistant *course-aware* rather than a
    generic chatbot: the retrieval step always filters by this student's
    enrolments, and the citations stored with each answer say which material it
    came from.
    """

    __tablename__ = "ask_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    course_id: Mapped[int | None] = mapped_column(
        ForeignKey("courses.id", ondelete="SET NULL"), index=True
    )
    title: Mapped[str | None] = mapped_column(String(160))


class AskMessage(Base):
    """A question or an answer. `declined` records an honest decline."""

    __tablename__ = "ask_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("ask_sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(String(12), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    # [{"material_id": 4, "chunk_id": 9, "title": "..."}]
    citations: Mapped[list | None] = mapped_column(JSONPayload)
    declined: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
