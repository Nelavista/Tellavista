"""Ops records for Phase 1: imports, campus utility and the university waitlist.

`ImportRun` is the receipt for a V1 bridge import. Every run keeps its mode
(dry-run or apply), its counts and its checksums, so the reconciliation report can
be compared against V1 later without trusting the tool's console output.

`CampusInfo` is the light Campus utility reachable from both paths: university
information and map points, not a third product.

`UniversityWaitlist` is what the onboarding wizard writes when a student's
university is not covered yet — a signal for ops, not a dead end.
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin
from app.models.admin import JSONPayload

IMPORT_PENDING = "pending"
IMPORT_RUNNING = "running"
IMPORT_DONE = "done"
IMPORT_FAILED = "failed"
IMPORT_STATUSES: tuple[str, ...] = (IMPORT_PENDING, IMPORT_RUNNING, IMPORT_DONE, IMPORT_FAILED)

IMPORT_DRY_RUN = "dry_run"
IMPORT_APPLY = "apply"
IMPORT_MODES: tuple[str, ...] = (IMPORT_DRY_RUN, IMPORT_APPLY)


class ImportRun(Base):
    """One import attempt with its reconciliation report."""

    __tablename__ = "import_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    mode: Mapped[str] = mapped_column(String(10), nullable=False)
    status: Mapped[str] = mapped_column(
        String(16), default=IMPORT_PENDING, server_default=IMPORT_PENDING, nullable=False
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    # {"users": {"read": 10, "created": 8, "updated": 2, ...}, ...}
    counts: Mapped[dict | None] = mapped_column(JSONPayload)
    # {"users": "sha256:..."} — a checksum of what V2 saw, comparable to V1's export.
    checksums: Mapped[dict | None] = mapped_column(JSONPayload)
    errors: Mapped[list | None] = mapped_column(JSONPayload)
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))


class CampusInfo(Base, TimestampMixin):
    """A campus map point or a piece of university-specific information."""

    __tablename__ = "campus_info"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university_id: Mapped[int] = mapped_column(
        ForeignKey("universities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    kind: Mapped[str] = mapped_column(
        String(30), default="info", server_default="info", nullable=False
    )
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    body: Mapped[str] = mapped_column(Text, default="", server_default="", nullable=False)
    # Coordinates are stored as micro-degrees (integer) for the same reason money
    # is integer: no floating point in persisted data.
    latitude_micro: Mapped[int | None] = mapped_column(Integer)
    longitude_micro: Mapped[int | None] = mapped_column(Integer)
    is_published: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true", nullable=False
    )


class UniversityWaitlist(Base):
    """A student waiting for their university to be covered."""

    __tablename__ = "university_waitlist"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    university_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    email: Mapped[str | None] = mapped_column(String(255))
    note: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    __table_args__ = (
        UniqueConstraint("user_id", "university_name", name="uq_waitlist_user_university"),
    )
