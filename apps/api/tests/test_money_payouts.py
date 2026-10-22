"""Phase 6 — payouts are approved, idempotent and traceable.

The manual provider is the first rail, so these tests exercise the real batch
lifecycle: draft → approved → paid, the second-approver rule for large amounts, a
cancelled batch that returns money to payable, and the export ops hands to a rail.
"""
from __future__ import annotations

import pytest
from factories import (
    make_assignment,
    make_opportunity,
    make_ops,
    make_project,
    make_skill,
    make_template,
    make_user,
)
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.ledger import (
    EarningLine,
    LedgerTransaction,
    PayoutBatch,
    PayoutItem,
)
from app.services.money import ledger, payouts
from app.services.work import delivery


def _payable_setup(db: Session, *, rate_minor: int = 1_000, task_count: int = 1):
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
        payload={"label": "positive", "task_count": task_count},
        client_key="payout-1",
    )
    submission.status = "approved"
    db.flush()
    line = ledger.record_approval_earning(db, project=project, submission=submission)
    ledger.mark_payable(db, project)
    return ops, creator, student, project, line


def test_a_batch_lifecycle_pays_the_student_once(db: Session) -> None:
    _ops, creator, student, project, line = _payable_setup(db)

    batch = payouts.create_batch(db, creator, project=project, earning_line_ids=[line.id])
    assert batch.status == "draft"
    assert batch.total_minor == 1_000
    assert db.scalars(select(PayoutItem)).one().status == "approved"

    payouts.approve_batch(db, creator, batch)
    assert batch.status == "approved" and batch.approved_by == creator.id

    payouts.pay_batch(db, creator, batch)
    assert batch.status == "paid" and batch.paid_at is not None
    assert db.get(EarningLine, line.id).status == "paid"

    payments = db.scalars(
        select(LedgerTransaction).where(LedgerTransaction.kind == "payout")
    ).all()
    assert len(payments) == 1
    assert payments[0].total_minor == 1_000


def test_paying_a_batch_twice_does_not_pay_twice(db: Session) -> None:
    _ops, creator, _student, project, line = _payable_setup(db)
    batch = payouts.create_batch(db, creator, project=project, earning_line_ids=[line.id])
    payouts.approve_batch(db, creator, batch)
    payouts.pay_batch(db, creator, batch)

    again = payouts.pay_batch(db, creator, batch)

    assert again.status == "paid"
    assert (
        db.scalar(
            select(func.count())
            .select_from(LedgerTransaction)
            .where(LedgerTransaction.kind == "payout")
        )
        == 1
    )


def test_a_large_batch_needs_a_second_approver(db: Session) -> None:
    # 20,000 tasks at 1,000 minor units is well above the threshold.
    _ops, creator, _student, project, line = _payable_setup(db, task_count=20_000)
    batch = payouts.create_batch(db, creator, project=project, earning_line_ids=[line.id])

    with pytest.raises(ApiError) as excinfo:
        payouts.approve_batch(db, creator, batch)
    assert excinfo.value.status_code == 403
    assert excinfo.value.code == "second_approver_required"

    second = make_ops(db)
    payouts.approve_batch(db, second, batch)
    assert batch.approved_by == second.id


def test_payment_requires_approval_first(db: Session) -> None:
    _ops, creator, _student, project, line = _payable_setup(db)
    batch = payouts.create_batch(db, creator, project=project, earning_line_ids=[line.id])

    with pytest.raises(ApiError) as excinfo:
        payouts.pay_batch(db, creator, batch)
    assert excinfo.value.code == "batch_not_approved"


def test_a_batch_is_idempotent_on_its_key(db: Session) -> None:
    _ops, creator, _student, project, line = _payable_setup(db)

    first = payouts.create_batch(
        db, creator, project=project, earning_line_ids=[line.id], idempotency_key="batch-1"
    )
    second = payouts.create_batch(
        db, creator, project=project, earning_line_ids=[line.id], idempotency_key="batch-1"
    )

    assert first.id == second.id
    assert db.scalar(select(func.count()).select_from(PayoutBatch)) == 1


def test_a_cancelled_batch_returns_the_money_to_payable(db: Session) -> None:
    _ops, creator, _student, project, line = _payable_setup(db)
    batch = payouts.create_batch(db, creator, project=project, earning_line_ids=[line.id])

    payouts.cancel_batch(db, creator, batch, reason="wrong bank file")

    assert batch.status == "cancelled"
    refreshed = db.get(EarningLine, line.id)
    assert refreshed.status == "payable"
    assert refreshed.payout_item_id is None


def test_a_failed_item_is_recorded_not_swallowed(db: Session) -> None:
    _ops, creator, _student, project, line = _payable_setup(db)
    batch = payouts.create_batch(db, creator, project=project, earning_line_ids=[line.id])
    assert batch.status == "draft"
    item = db.scalars(select(PayoutItem)).one()

    payouts.fail_item(db, creator, item.id, reason="account name mismatch")

    assert item.status == "failed"
    assert item.failure_reason == "account name mismatch"
    assert db.get(EarningLine, line.id).status == "failed"


def test_the_export_has_one_row_per_student(db: Session) -> None:
    _ops, creator, student, project, line = _payable_setup(db)
    batch = payouts.create_batch(db, creator, project=project, earning_line_ids=[line.id])

    csv = payouts.export_csv(db, batch)

    lines = csv.strip().splitlines()
    assert lines[0] == "user_id,email,amount_minor,currency,status,reference"
    assert lines[1].startswith(f"{student.id},{student.email},1000,USD,approved,")


def test_an_unknown_provider_is_refused(db: Session) -> None:
    _ops, creator, _student, project, line = _payable_setup(db)

    with pytest.raises(ApiError) as excinfo:
        payouts.create_batch(
            db, creator, project=project, earning_line_ids=[line.id], provider="paystack"
        )
    assert excinfo.value.code == "unknown_provider"


def test_batch_detail_lists_items_with_the_student(db: Session) -> None:
    _ops, creator, student, project, line = _payable_setup(db)
    batch = payouts.create_batch(db, creator, project=project, earning_line_ids=[line.id])

    detail = payouts.batch_detail(db, batch)

    assert detail["total_minor"] == 1_000
    assert detail["items"][0]["user_id"] == student.id
    assert detail["items"][0]["email"] == student.email
