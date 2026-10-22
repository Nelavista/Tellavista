"""Drain due jobs from Postgres.

Claiming uses `FOR UPDATE SKIP LOCKED` on Postgres, so two workers never run the
same job; SQLite (tests, local) ignores the clause, which is fine because there is
one process there. Retries use a fixed backoff ladder and stop at `max_attempts`,
leaving the row `failed` for an operator instead of retrying forever.
"""
from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.jobs import DONE, FAILED, PENDING, RUNNING, Job
from app.worker.errors import PermanentJobError
from app.worker.tasks import HANDLERS

logger = logging.getLogger(__name__)

BACKOFF_SECONDS: tuple[int, ...] = (30, 120, 600, 1800, 3600)


def _backoff(attempts: int) -> timedelta:
    index = min(max(attempts - 1, 0), len(BACKOFF_SECONDS) - 1)
    return timedelta(seconds=BACKOFF_SECONDS[index])


def claim_next(db: Session) -> Job | None:
    job = db.scalar(
        select(Job)
        .where(Job.status == PENDING, Job.run_after <= datetime.now(UTC))
        .order_by(Job.id)
        .limit(1)
        .with_for_update(skip_locked=True)
    )
    if job is not None:
        job.status = RUNNING
        job.attempts += 1
        db.flush()
    return job


def run_one(db: Session) -> bool:
    job = claim_next(db)
    if job is None:
        return False

    now = datetime.now(UTC)
    handler = HANDLERS.get(job.name)
    try:
        if handler is None:
            raise PermanentJobError(f"no handler registered for job {job.name!r}")
        handler(job.payload)
    except PermanentJobError as exc:
        # Bad payload, revoked key, plan limit: retrying wastes the window.
        logger.error("job permanently failed id=%s name=%s: %s", job.id, job.name, exc)
        job.last_error = f"{type(exc).__name__}: {exc}"[:2000]
        job.status = FAILED
        job.finished_at = now
        db.commit()
        return True
    except Exception as exc:  # noqa: BLE001 - any handler failure is a retry
        logger.exception("job failed id=%s name=%s attempt=%s", job.id, job.name, job.attempts)
        job.last_error = f"{type(exc).__name__}: {exc}"[:2000]
        if job.attempts >= job.max_attempts:
            job.status = FAILED
            job.finished_at = now
        else:
            job.status = PENDING
            job.run_after = now + _backoff(job.attempts)
        db.commit()
        return True

    job.status = DONE
    job.finished_at = now
    db.commit()
    return True


def drain(db: Session, *, limit: int = 50) -> int:
    processed = 0
    while processed < limit and run_one(db):
        processed += 1
    return processed
