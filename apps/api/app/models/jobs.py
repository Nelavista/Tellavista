"""Durable background jobs (Phase 0 PR 0.6).

A row per job in Postgres, not an in-memory queue: a deploy or restart must not
lose a verification email or a payout batch. The worker claims due rows, runs the
registered handler, and on failure schedules a retry with exponential backoff
until `max_attempts`, then leaves the row `failed` for an operator to see.

`idempotency_key` is unique so the same logical job cannot be enqueued twice by a
retried request (the same rule as submissions, ADR-0007).
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin
from app.models.admin import JSONPayload

PENDING = "pending"
RUNNING = "running"
DONE = "done"
FAILED = "failed"
JOB_STATUSES: tuple[str, ...] = (PENDING, RUNNING, DONE, FAILED)


class Job(Base, TimestampMixin):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    payload: Mapped[dict] = mapped_column(JSONPayload, nullable=False)
    status: Mapped[str] = mapped_column(
        String(16), default=PENDING, server_default=PENDING, nullable=False
    )
    attempts: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)
    max_attempts: Mapped[int] = mapped_column(
        Integer, default=5, server_default="5", nullable=False
    )
    run_after: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_error: Mapped[str | None] = mapped_column(Text)
    idempotency_key: Mapped[str | None] = mapped_column(String(80), unique=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (Index("ix_jobs_status_run_after", "status", "run_after"),)
