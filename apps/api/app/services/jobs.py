"""Enqueue a durable background job (model: app.models.jobs).

Kept deliberately small: services call `enqueue(db, "send_email", {...})` inside
their own transaction, so the job is committed exactly when the work that needs
it commits. There is no fire-and-forget path that can lose a verification email.
"""
from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.jobs import Job

logger = logging.getLogger(__name__)


def enqueue(
    db: Session,
    name: str,
    payload: dict[str, Any] | None = None,
    *,
    key: str | None = None,
    delay_seconds: int = 0,
) -> Job | None:
    """Insert one job, or return the existing one when `key` was already used."""
    if key:
        existing = db.scalar(select(Job).where(Job.idempotency_key == key))
        if existing is not None:
            return existing

    job = Job(
        name=name,
        payload=payload or {},
        idempotency_key=key,
        run_after=datetime.now(UTC) + timedelta(seconds=max(0, delay_seconds)),
    )
    try:
        with db.begin_nested():
            db.add(job)
            db.flush()
    except IntegrityError:
        # Lost the race on the unique key; the other insert wins.
        return db.scalar(select(Job).where(Job.idempotency_key == key))
    return job
