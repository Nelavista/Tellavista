"""The operations overview as one read.

The screen used to issue six list requests and do its own arithmetic, so the
counts could disagree with each other and with the audit rows underneath them.
This endpoint is the single read that replaces them: every count comes from the
same rows as the timestamp beside it, and the latest audit rows are read after.

These tests pin the two things that would fail quietly: a count that no longer
matches its own list, and a student being able to read the ops summary.
"""
from __future__ import annotations

from datetime import UTC, datetime

from factories import make_assignment, make_opportunity, make_ops, make_project, make_user, unique
from sqlalchemy import select

from app.core.security import create_access_token
from app.models.ops import ImportRun, UniversityWaitlist
from app.models.verification import PracticalSubmission
from app.models.work import Submission


def _headers(user) -> dict:
    return {
        "Authorization": (
            f"Bearer {create_access_token(user.id, user.role.code if user.role else None)}"
        )
    }


def _queue(body: dict, key: str) -> dict:
    return next(row for row in body["queues"] if row["key"] == key)


def test_the_overview_is_one_read_with_every_queue(api) -> None:
    client, db = api
    ops = make_ops(db)

    response = client.get("/v1/ops/overview", headers=_headers(ops))
    assert response.status_code == 200
    body = response.json()

    assert [row["key"] for row in body["queues"]] == [
        "work_review",
        "practical_review",
        "waitlist",
        "imports",
    ]
    assert all(row["count"] == 0 for row in body["queues"])
    assert body["live_projects"] == []
    assert body["recent_audit"] == []
    assert body["generated_at"]


def test_counts_match_the_rows_they_describe(api) -> None:
    """Each queue is a real list length, and its stamp comes from those same rows."""
    client, db = api
    ops = make_ops(db)
    student = make_user(db)

    opportunity = make_opportunity(db, ops)
    project = make_project(db, ops, opportunity)
    assignment = make_assignment(db, project, student)
    submission = Submission(
        assignment_id=assignment.id,
        user_id=student.id,
        payload={"rows": 10},
        status="submitted",
    )
    db.add(submission)

    db.add(
        PracticalSubmission(
            practical_task_id=_first_practical_task_id(db),
            user_id=student.id,
            payload={"answer": "x"},
            status="submitted",
        )
    )
    db.add(UniversityWaitlist(university_name=unique("Test University"), email="a@example.test"))
    db.add(ImportRun(source="v1_export", mode="dry_run", status="done"))

    # An audit row, so the overview proves it reads the trail it always shows.
    from app.services import audit

    audit.record(db, action="overview.test", actor_user_id=ops.id, target_type="test", target_id=1)
    db.commit()

    body = client.get("/v1/ops/overview", headers=_headers(ops)).json()

    assert _queue(body, "work_review")["count"] == 1
    assert _queue(body, "practical_review")["count"] == 1
    assert _queue(body, "waitlist")["count"] == 1
    assert _queue(body, "imports")["count"] == 1
    assert _queue(body, "imports")["last_run"]["mode"] == "dry_run"
    assert body["totals"]["live_projects"] == 1
    assert body["totals"]["queues_with_items"] == 4
    assert len(body["live_projects"]) == 1
    assert body["live_projects"][0]["slug"] == project.slug
    assert body["recent_audit"][0]["action"] == "overview.test"


def test_the_oldest_stamp_is_the_oldest_pending_item(api) -> None:
    """The screen's promise is \"oldest\" means oldest, not \"most recently loaded\".
    Two submissions, created oldest first, must report the first one."""
    client, db = api
    ops = make_ops(db)
    student = make_user(db)
    opportunity = make_opportunity(db, ops)
    project = make_project(db, ops, opportunity)
    assignment = make_assignment(db, project, student)

    old = Submission(
        assignment_id=assignment.id,
        user_id=student.id,
        payload={},
        status="submitted",
        submitted_at=datetime(2026, 1, 1, tzinfo=UTC),
    )
    new = Submission(
        assignment_id=assignment.id,
        user_id=student.id,
        payload={},
        status="submitted",
        submitted_at=datetime(2026, 6, 1, tzinfo=UTC),
    )
    db.add_all([old, new])
    db.commit()

    queue = _queue(client.get("/v1/ops/overview", headers=_headers(ops)).json(), "work_review")
    assert queue["count"] == 2
    assert queue["stamp"].startswith("2026-01-01")


def test_a_student_cannot_read_the_ops_overview(api) -> None:
    client, db = api
    student = make_user(db)

    response = client.get("/v1/ops/overview", headers=_headers(student))
    assert response.status_code == 403


def test_the_overview_does_not_include_a_reviewed_submission(api) -> None:
    """The queue count is the same rule as the review queue page: once reviewed,
    a submission leaves the queue, and the overview must not keep counting it."""
    client, db = api
    ops = make_ops(db)
    student = make_user(db)
    opportunity = make_opportunity(db, ops)
    project = make_project(db, ops, opportunity)
    assignment = make_assignment(db, project, student)
    reviewed = Submission(
        assignment_id=assignment.id,
        user_id=student.id,
        payload={},
        status="approved",
    )
    db.add(reviewed)
    db.commit()

    assert _queue(client.get("/v1/ops/overview", headers=_headers(ops)).json(), "work_review")[
        "count"
    ] == 0


def _first_practical_task_id(db) -> int:
    """Practical tasks are seeded reference data; if none exists the test creates
    the row it needs rather than depending on a seed ordering."""
    from app.models.skills import Skill
    from app.models.verification import PracticalTask

    existing = db.scalar(select(PracticalTask.id).order_by(PracticalTask.id).limit(1))
    if existing is not None:
        return existing
    skill = db.scalar(select(Skill.id).order_by(Skill.id).limit(1))
    if skill is None:
        skill_row = Skill(slug=unique("skill"), name="Skill")
        db.add(skill_row)
        db.flush()
        skill = skill_row.id
    task = PracticalTask(
        skill_id=skill,
        slug=unique("practical"),
        title="Practical",
        brief_md="Do the work.",
        status="published",
    )
    db.add(task)
    db.flush()
    return task.id
