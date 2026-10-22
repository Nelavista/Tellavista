"""Phase 5 — work never duplicates and never gets lost on a dropped connection.

Two guarantees are tested here: the same client key stores one submission, and a
queued batch applies item by item so one bad item cannot discard the rest. Object
level authorisation is tested too: another student's assignment is a 404.
"""
from __future__ import annotations

import pytest
from factories import (
    make_assignment,
    make_member,
    make_opportunity,
    make_ops,
    make_project,
    make_skill,
    make_template,
    make_user,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.work import Assignment, Submission
from app.services.work import cohorts, delivery


def _setup(db: Session):
    ops = make_ops(db)
    student = make_user(db)
    skill = make_skill(db)
    template = make_template(db, skill)
    opportunity = make_opportunity(db, ops)
    project = make_project(db, ops, opportunity)
    make_member(db, project, student)
    assignment = make_assignment(db, project, student, template=template)
    return ops, student, project, assignment


def test_the_same_client_key_stores_one_submission(db: Session) -> None:
    _ops, student, _project, assignment = _setup(db)

    first, created_first = delivery.submit_work(
        db, student, assignment_id=assignment.id, payload={"label": "positive"}, client_key="k-1"
    )
    second, created_second = delivery.submit_work(
        db, student, assignment_id=assignment.id, payload={"label": "positive"}, client_key="k-1"
    )

    assert created_first is True and created_second is False
    assert first.id == second.id
    assert db.scalar(select(Submission).where(Submission.idempotency_key == "k-1")) is not None
    assert len(db.scalars(select(Submission)).all()) == 1


def test_a_client_key_cannot_be_reused_by_another_student(db: Session) -> None:
    _ops, student, _project, assignment = _setup(db)
    other = make_user(db)

    delivery.submit_work(
        db, student, assignment_id=assignment.id, payload={"label": "x"}, client_key="shared"
    )
    with pytest.raises(ApiError) as excinfo:
        delivery.submit_work(
            db, other, assignment_id=assignment.id, payload={"label": "x"}, client_key="shared"
        )
    assert excinfo.value.code == "idempotency.key_reused"


def test_another_students_assignment_is_not_found(db: Session) -> None:
    _ops, _student, _project, assignment = _setup(db)
    intruder = make_user(db)

    with pytest.raises(ApiError) as excinfo:
        delivery.submit_work(
            db, intruder, assignment_id=assignment.id, payload={"label": "x"}, client_key="k-2"
        )
    assert excinfo.value.status_code == 404
    assert excinfo.value.code == "assignment_not_found"


def test_an_empty_submission_is_rejected_before_anything_is_saved(db: Session) -> None:
    _ops, student, _project, assignment = _setup(db)

    with pytest.raises(ApiError) as excinfo:
        delivery.submit_work(
            db, student, assignment_id=assignment.id, payload={}, client_key="k-3"
        )
    assert excinfo.value.code == "empty_submission"
    assert db.scalars(select(Submission)).all() == []


def test_a_missing_client_key_is_rejected(db: Session) -> None:
    _ops, student, _project, assignment = _setup(db)
    with pytest.raises(ApiError) as excinfo:
        delivery.submit_work(db, student, assignment_id=assignment.id, payload={"a": 1}, client_key="")
    assert excinfo.value.code == "idempotency_key_required"


def test_a_paused_project_accepts_no_new_work(db: Session) -> None:
    _ops, student, project, assignment = _setup(db)
    project.status = "paused"
    db.flush()

    with pytest.raises(ApiError) as excinfo:
        delivery.submit_work(
            db, student, assignment_id=assignment.id, payload={"label": "x"}, client_key="k-4"
        )
    assert excinfo.value.code == "project_not_active"


def test_offline_sync_applies_the_good_items_and_reports_the_bad_one(db: Session) -> None:
    _ops, student, _project, assignment = _setup(db)

    results = delivery.sync_offline(
        db,
        student,
        [
            {"assignment_id": assignment.id, "payload": {"label": "a"}, "client_key": "sync-1"},
            {"assignment_id": 999_999, "payload": {"label": "b"}, "client_key": "sync-2"},
            {"assignment_id": assignment.id, "payload": {}, "client_key": "sync-3"},
        ],
    )

    assert [item["status"] for item in results] == ["saved", "rejected", "rejected"]
    assert results[1]["code"] == "assignment_not_found"
    assert results[2]["code"] == "empty_submission"
    stored = db.scalars(select(Submission)).all()
    assert len(stored) == 1 and stored[0].idempotency_key == "sync-1"


def test_replaying_a_sync_batch_is_safe(db: Session) -> None:
    _ops, student, _project, assignment = _setup(db)
    items = [
        {"assignment_id": assignment.id, "payload": {"label": "a"}, "client_key": "sync-9"}
    ]

    delivery.sync_offline(db, student, items)
    second = delivery.sync_offline(db, student, items)

    assert second[0]["status"] == "already_saved"
    assert len(db.scalars(select(Submission)).all()) == 1


def test_starting_work_moves_the_assignment_forward(db: Session) -> None:
    _ops, student, _project, assignment = _setup(db)

    row = delivery.start_assignment(db, student, assignment.id)
    assert row.status == "in_progress"
    # Starting twice is a no-op, not an error.
    assert delivery.start_assignment(db, student, assignment.id).status == "in_progress"


def test_my_assignments_only_lists_my_own(db: Session) -> None:
    _ops, student, _project, assignment = _setup(db)
    other = make_user(db)

    assert [row["id"] for row in cohorts.my_assignments(db, student)] == [assignment.id]
    assert cohorts.my_assignments(db, other) == []
    assert db.get(Assignment, assignment.id).user_id == student.id
