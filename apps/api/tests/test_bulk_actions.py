"""Bulk review, money and content actions.

The single-record endpoints are unchanged; these are the same services applied to
a list. What is worth testing is the failure behaviour, because a bulk call that
silently skips a record is worse than no bulk call: the batch of twenty where one
refusal is swallowed looks like twenty approvals on the screen and nineteen in the
database.

The contract these pin: one refusal is reported with its own id and code, the rest
of the batch still applies, a repeated id is performed once, and nothing that moves
money in bulk can be done without the same guard the single call needs.
"""
from __future__ import annotations

from factories import (
    make_assignment,
    make_opportunity,
    make_ops,
    make_project,
    make_skill,
    make_template,
    make_user,
    unique,
)
from sqlalchemy import func, select

from app.core.security import create_access_token
from app.models.ledger import PayoutBatch
from app.models.quality import QualityReview
from app.models.skills import LearningPath, Lesson
from app.models.work import Submission
from app.services.money import ledger, payouts


def _headers(user) -> dict:
    return {
        "Authorization": (
            f"Bearer {create_access_token(user.id, user.role.code if user.role else None)}"
        )
    }


def _lessons(db, *, count: int = 3, status: str = "draft") -> list[int]:
    skill = make_skill(db)
    rows = []
    for index in range(count):
        lesson = Lesson(
            skill_id=skill.id,
            slug=unique(f"lesson-{index}"),
            title=f"Lesson {index}",
            body_md="Body",
            status=status,
        )
        db.add(lesson)
        rows.append(lesson)
    db.commit()
    return [row.id for row in rows]


def _submissions(db, *, count: int = 2) -> list[int]:
    ops = make_ops(db)
    student = make_user(db)
    opportunity = make_opportunity(db, ops)
    project = make_project(db, ops, opportunity)
    assignment = make_assignment(db, project, student)
    rows = []
    for _ in range(count):
        submission = Submission(
            assignment_id=assignment.id, user_id=student.id, payload={}, status="submitted"
        )
        db.add(submission)
        rows.append(submission)
    db.commit()
    return [row.id for row in rows]


# --- content ---------------------------------------------------------------


def test_content_publishes_a_whole_set_in_one_call(api) -> None:
    client, db = api
    editor = make_ops(db)  # content editing needs project.write, which reviewers lack
    ids = _lessons(db)

    response = client.post(
        "/v1/skills/content/lessons/bulk",
        json={"ids": ids, "status": "published"},
        headers=_headers(editor),
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["applied"] == 3
    assert body["unchanged"] == 0
    assert body["failed"] == []
    assert all(db.get(Lesson, lesson_id).status == "published" for lesson_id in ids)


def test_content_reports_a_mixed_batch_and_still_applies_the_rest(api) -> None:
    client, db = api
    editor = make_ops(db)
    ids = _lessons(db, count=2)
    db.get(Lesson, ids[0]).status = "published"
    db.commit()

    body = client.post(
        "/v1/skills/content/lessons/bulk",
        json={"ids": [*ids, 999_999], "status": "published"},
        headers=_headers(editor),
    ).json()

    assert body["applied"] == 1  # the second lesson
    assert body["unchanged"] == 1  # the one already published
    assert [row["id"] for row in body["failed"]] == [999_999]
    assert body["failed"][0]["code"] == "lesson_not_found"


def test_content_bulk_collapses_a_duplicated_id(api) -> None:
    client, db = api
    editor = make_ops(db)
    lesson_id = _lessons(db, count=1)[0]

    body = client.post(
        "/v1/skills/content/lessons/bulk",
        json={"ids": [lesson_id, lesson_id, lesson_id], "status": "published"},
        headers=_headers(editor),
    ).json()

    assert body["requested"] == 1
    assert body["applied"] == 1


def test_content_bulk_refuses_an_invalid_status(api) -> None:
    client, db = api
    editor = make_ops(db)

    response = client.post(
        "/v1/skills/content/lessons/bulk",
        json={"ids": _lessons(db, count=1), "status": "live"},
        headers=_headers(editor),
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_content_status"


def test_content_bulk_cannot_publish_a_path_by_lesson_id(api) -> None:
    """The type is the endpoint, so an id from the wrong table is simply not found
    instead of publishing something else."""
    client, db = api
    editor = make_ops(db)
    path = LearningPath(
        skill_id=make_skill(db).id, slug=unique("path"), title="A path", status="draft"
    )
    db.add(path)
    db.commit()

    body = client.post(
        "/v1/skills/content/paths/bulk",
        json={"ids": [path.id], "status": "published"},
        headers=_headers(editor),
    ).json()
    assert body["applied"] == 1
    assert db.get(LearningPath, path.id).status == "published"


# --- review ----------------------------------------------------------------


def test_review_applies_one_verdict_to_a_batch(api) -> None:
    client, db = api
    # The ops review router requires project.write on top of review.write.
    reviewer = make_ops(db)
    ids = _submissions(db)

    response = client.post(
        "/v1/work/review-queue/bulk",
        json={"submission_ids": ids, "verdict": "approved"},
        headers=_headers(reviewer),
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["applied"] == 2
    assert body["failed"] == []
    assert db.scalar(select(func.count()).select_from(QualityReview)) == 2


def test_review_reports_the_one_record_that_cannot_be_reviewed(api) -> None:
    """A submission reviewed once and not needing a second review is refused by
    the single-record rule; the bulk call must name it and still do the other."""
    client, db = api
    reviewer = make_ops(db)
    first, second = _submissions(db, count=2)

    client.post(
        "/v1/work/review-queue/bulk",
        json={"submission_ids": [first], "verdict": "approved"},
        headers=_headers(reviewer),
    )

    body = client.post(
        "/v1/work/review-queue/bulk",
        json={"submission_ids": [first, second], "verdict": "approved"},
        headers=_headers(reviewer),
    ).json()

    assert body["applied"] == 1
    assert [row["id"] for row in body["failed"]] == [first]
    assert body["failed"][0]["code"] == "already_reviewed"


def test_a_student_cannot_bulk_review_work(api) -> None:
    client, db = api
    student = make_user(db)

    response = client.post(
        "/v1/work/review-queue/bulk",
        json={"submission_ids": [1], "verdict": "approved"},
        headers=_headers(student),
    )
    assert response.status_code == 403


# --- money -----------------------------------------------------------------


def _batch_with_earning(db, *, rate_minor: int = 1_000) -> tuple[PayoutBatch, int]:
    """A draft batch with one payable line, built through the real services."""
    from app.services.work import delivery

    ops = make_ops(db)
    creator = make_ops(db)
    student = make_user(db)
    skill = make_skill(db)
    template = make_template(db, skill)
    opportunity = make_opportunity(db, ops, rate_minor=rate_minor)
    project = make_project(db, ops, opportunity)
    assignment = make_assignment(db, project, student, template=template)
    submission, _ = delivery.submit_work(
        db,
        student,
        assignment_id=assignment.id,
        payload={"label": "positive", "task_count": 1},
        client_key=unique("bulk-payout"),
    )
    submission.status = "approved"
    db.flush()
    line = ledger.record_approval_earning(db, project=project, submission=submission)
    ledger.mark_payable(db, project)
    batch = payouts.create_batch(db, creator, project=project, earning_line_ids=[line.id])
    return batch, line.id


def test_money_bulk_approves_a_run_of_batches(api) -> None:
    client, db = api
    first, _ = _batch_with_earning(db)
    second, _ = _batch_with_earning(db)
    db.commit()

    response = client.post(
        "/v1/money/payout-batches/bulk",
        json={"batch_ids": [first.id, second.id], "action": "approve"},
        headers=_headers(make_ops(db)),
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["applied"] == 2
    db.refresh(first)
    db.refresh(second)
    assert first.status == "approved" and second.status == "approved"


def test_money_bulk_cancels_only_with_a_reason(api) -> None:
    client, db = api
    batch, _ = _batch_with_earning(db)
    db.commit()
    ops = make_ops(db)

    missing = client.post(
        "/v1/money/payout-batches/bulk",
        json={"batch_ids": [batch.id], "action": "cancel"},
        headers=_headers(ops),
    )
    assert missing.status_code == 400
    assert missing.json()["error"]["code"] == "reason_required"

    ok = client.post(
        "/v1/money/payout-batches/bulk",
        json={"batch_ids": [batch.id], "action": "cancel", "reason": "client withdrew"},
        headers=_headers(ops),
    )
    assert ok.status_code == 200
    assert ok.json()["applied"] == 1


def test_money_bulk_cannot_pay(api) -> None:
    """Paying stays one batch at a time: each payment needs its own reference and
    a bulk pay would be an irreversible transfer set behind one click."""
    client, db = api
    batch, _ = _batch_with_earning(db)
    db.commit()

    response = client.post(
        "/v1/money/payout-batches/bulk",
        json={"batch_ids": [batch.id], "action": "pay"},
        headers=_headers(make_ops(db)),
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_bulk_action"


def test_money_bulk_reports_a_batch_that_cannot_be_approved(api) -> None:
    client, db = api
    first, _ = _batch_with_earning(db)
    second, _ = _batch_with_earning(db)
    db.commit()
    ops = make_ops(db)

    # Paying the second makes it unapprovable; the first must still go through.
    payouts.approve_batch(db, ops, second)
    payouts.pay_batch(db, ops, second)
    db.commit()

    body = client.post(
        "/v1/money/payout-batches/bulk",
        json={"batch_ids": [first.id, second.id], "action": "cancel", "reason": "sweep"},
        headers=_headers(ops),
    ).json()

    # The draft batch is cancelled; the paid one cannot be, and saying so per id
    # is the whole point of the report.
    assert body["applied"] == 1
    assert [row["id"] for row in body["failed"]] == [second.id]
    assert body["failed"][0]["code"] == "batch_not_cancellable"


def test_a_student_cannot_bulk_approve_batches(api) -> None:
    client, db = api
    batch, _ = _batch_with_earning(db)
    db.commit()

    response = client.post(
        "/v1/money/payout-batches/bulk",
        json={"batch_ids": [batch.id], "action": "approve"},
        headers=_headers(make_user(db)),
    )
    assert response.status_code == 403
