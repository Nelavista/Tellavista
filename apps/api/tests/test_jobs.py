"""Phase 0 PR 0.6 — the durable queue.

Written now, run with the rest of the suite in the verification pass.
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.time import as_utc
from app.models.jobs import DONE, FAILED, PENDING, Job
from app.services.jobs import enqueue
from app.worker import tasks
from app.worker.errors import PermanentJobError
from app.worker.runner import drain, run_one


def _boom(payload: dict) -> None:
    raise RuntimeError("handler exploded")


def _permanent(payload: dict) -> None:
    raise PermanentJobError("do not retry")


def test_enqueue_is_idempotent_by_key(db: Session) -> None:
    first = enqueue(db, "noop", {"n": 1}, key="job-1")
    second = enqueue(db, "noop", {"n": 2}, key="job-1")
    assert first is not None and second is not None
    assert first.id == second.id
    assert db.scalar(select(Job).where(Job.idempotency_key == "job-1")).payload == {"n": 1}


def test_run_one_marks_a_successful_job_done(db: Session) -> None:
    enqueue(db, "noop", {})
    db.commit()
    assert run_one(db) is True

    job = db.scalars(select(Job)).one()
    assert job.status == DONE and job.attempts == 1 and job.finished_at is not None
    assert run_one(db) is False  # nothing left


def test_failed_job_is_retried_then_given_up_on(db: Session) -> None:
    tasks.HANDLERS["boom"] = _boom
    try:
        job = enqueue(db, "boom", {})
        assert job is not None
        job.max_attempts = 1
        db.commit()

        assert run_one(db) is True
        stored = db.scalars(select(Job)).one()
        assert stored.status == FAILED
        assert stored.attempts == 1
        assert "handler exploded" in (stored.last_error or "")
    finally:
        tasks.HANDLERS.pop("boom", None)


def test_a_permanent_failure_is_not_retried(db: Session) -> None:
    tasks.HANDLERS["permanent"] = _permanent
    try:
        job = enqueue(db, "permanent", {})
        assert job is not None
        job.max_attempts = 5
        db.commit()

        assert run_one(db) is True
        stored = db.scalars(select(Job)).one()
        assert stored.status == FAILED
        assert stored.attempts == 1
        assert "do not retry" in (stored.last_error or "")
    finally:
        tasks.HANDLERS.pop("permanent", None)


def test_a_future_job_is_not_claimed(db: Session) -> None:
    job = enqueue(db, "noop", {}, delay_seconds=3600)
    assert job is not None
    db.commit()
    assert run_one(db) is False
    stored = db.scalars(select(Job)).one()
    assert stored.status == PENDING and stored.attempts == 0
    # SQLite hands back a naive datetime; `as_utc` normalises before comparing.
    assert as_utc(stored.run_after) > datetime.now(UTC) - timedelta(seconds=5)


def test_drain_processes_every_due_job(db: Session) -> None:
    for _ in range(3):
        enqueue(db, "noop", {})
    db.commit()
    assert drain(db, limit=10) == 3
    assert {j.status for j in db.scalars(select(Job))} == {DONE}


def test_unknown_handler_fails_rather_than_silently_succeeding(db: Session) -> None:
    job = enqueue(db, "does-not-exist", {})
    assert job is not None
    job.max_attempts = 1
    db.commit()
    assert run_one(db) is True
    stored = db.scalars(select(Job)).one()
    assert stored.status == FAILED and "no handler" in (stored.last_error or "")


@pytest.mark.parametrize("name", sorted(tasks.HANDLERS))
def test_every_handler_is_callable(name: str) -> None:
    assert callable(tasks.HANDLERS[name])
