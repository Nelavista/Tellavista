"""Periodic jobs that need no external scheduler (F3).

The worker already drains a durable queue. This module decides what should be on
it on a given day, so "reconcile the ledger daily" does not depend on a cron
service we have not provisioned.

Idempotency is the date: `reconcile:{YYYY-MM-DD}` is the job key, so however many
times the loop ticks, one day produces one run.
"""
from __future__ import annotations

from datetime import UTC, date, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.jobs import Job
from app.services.jobs import enqueue


def enqueue_scheduled(db: Session, *, today: date | None = None) -> int:
    """Add the jobs that are due today. Returns how many were created.

    `enqueue` hands back the existing row when the key was already used, so the
    presence of the key — not the returned job's state — decides whether this
    tick created work. Counting the returned job would report one new job on
    every tick of the same day.
    """
    day = today or datetime.now(UTC).date()
    created = 0

    key = f"reconcile:{day.isoformat()}"
    already_queued = db.scalar(select(Job.id).where(Job.idempotency_key == key))
    if already_queued is None:
        enqueue(db, "reconcile_daily", {"day": day.isoformat()}, key=key)
        created += 1
    db.commit()
    return created


__all__ = ["enqueue_scheduled"]
