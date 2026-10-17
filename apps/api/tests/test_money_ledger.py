"""Phase 6 — an append-only, balanced, idempotent ledger.

The tests read the rows back rather than trusting the service's own return value:
debits must equal credits in every transaction, funding must be replayable without
duplicating entries, a correction must be a new reversal transaction, and a
student-facing earning line must explain itself.
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
    ACCOUNT_DEPARTMENT_PAYABLE,
    ACCOUNT_ESCROW,
    ACCOUNT_PLATFORM_REVENUE,
    ACCOUNT_STUDENT_PAYABLE,
    DEBIT,
    EarningLine,
    LedgerEntry,
    LedgerTransaction,
)
from app.services.money import ledger
from app.services.work import delivery


def _setup(db: Session, *, rate_minor: int = 1_000):
    ops = make_ops(db)
    student = make_user(db)
    skill = make_skill(db)
    template = make_template(db, skill)
    opportunity = make_opportunity(db, ops, rate_minor=rate_minor)
    project = make_project(db, ops, opportunity)
    assignment = make_assignment(db, project, student, template=template)
    return ops, student, project, assignment


def _approved_submission(db: Session, student, assignment, key: str = "money-1"):
    submission, _ = delivery.submit_work(
        db, student, assignment_id=assignment.id, payload={"label": "positive"}, client_key=key
    )
    submission.status = "approved"
    db.flush()
    return submission


def _entry_totals(db: Session, transaction_id: int) -> dict[str, int]:
    rows = db.execute(
        select(LedgerEntry.direction, func.sum(LedgerEntry.amount_minor))
        .where(LedgerEntry.transaction_id == transaction_id)
        .group_by(LedgerEntry.direction)
    ).all()
    return dict(rows)


def test_funding_posts_a_balanced_90_8_2_transaction(db: Session) -> None:
    ops, _student, project, _assignment = _setup(db)

    transaction, split = ledger.fund_project(db, ops, project=project, total_minor=1_000_000)

    totals = _entry_totals(db, transaction.id)
    assert totals[DEBIT] == totals["credit"] == 1_000_000
    assert split.student_pool_minor == 900_000

    credits = {
        entry.account: entry.amount_minor
        for entry in db.scalars(
            select(LedgerEntry).where(
                LedgerEntry.transaction_id == transaction.id,
                LedgerEntry.direction == "credit",
            )
        ).all()
    }
    assert credits[ACCOUNT_STUDENT_PAYABLE] == 900_000
    assert credits[ACCOUNT_PLATFORM_REVENUE] == 80_000
    assert credits[ACCOUNT_DEPARTMENT_PAYABLE] == 20_000
    assert ACCOUNT_ESCROW not in credits


def test_funding_twice_returns_the_original_and_does_not_duplicate_rows(db: Session) -> None:
    ops, _student, project, _assignment = _setup(db)

    first, _ = ledger.fund_project(db, ops, project=project, total_minor=500_000)
    second, _ = ledger.fund_project(db, ops, project=project, total_minor=500_000)

    assert first.id == second.id
    assert db.scalar(select(func.count()).select_from(LedgerTransaction)) == 1
    assert (
        db.scalar(
            select(func.count())
            .select_from(LedgerEntry)
            .where(LedgerEntry.transaction_id == first.id)
        )
        == 4
    )


def test_a_different_amount_with_the_same_funding_key_is_refused(db: Session) -> None:
    ops, _student, project, _assignment = _setup(db)
    ledger.fund_project(db, ops, project=project, total_minor=500_000)

    with pytest.raises(ApiError) as excinfo:
        ledger.post_transaction(
            db,
            kind="project_funding",
            currency="USD",
            entries=[
                {"account": ACCOUNT_ESCROW, "direction": "debit", "amount_minor": 1},
                {"account": ACCOUNT_STUDENT_PAYABLE, "direction": "credit", "amount_minor": 1},
            ],
            idempotency_key=f"funding:project:{project.id}:500000",
            project_id=project.id,
        )
    assert excinfo.value.code == "ledger.key_reused"


def test_an_unbalanced_transaction_is_refused(db: Session) -> None:
    ops, _student, project, _assignment = _setup(db)

    with pytest.raises(ApiError) as excinfo:
        ledger.post_transaction(
            db,
            kind="adjustment",
            currency="USD",
            entries=[
                {"account": ACCOUNT_ESCROW, "direction": "debit", "amount_minor": 100},
                {"account": ACCOUNT_STUDENT_PAYABLE, "direction": "credit", "amount_minor": 99},
            ],
            idempotency_key="unbalanced-1",
            project_id=project.id,
        )
    assert excinfo.value.code == "ledger_unbalanced"
    assert db.scalars(select(LedgerTransaction)).all() == []


def test_a_float_amount_is_never_accepted(db: Session) -> None:
    ops, _student, project, _assignment = _setup(db)

    with pytest.raises(ApiError) as excinfo:
        ledger.post_transaction(
            db,
            kind="adjustment",
            currency="USD",
            entries=[
                {"account": ACCOUNT_ESCROW, "direction": "debit", "amount_minor": 10.5},
                {"account": ACCOUNT_STUDENT_PAYABLE, "direction": "credit", "amount_minor": 10.5},
            ],
            idempotency_key="float-1",
            project_id=project.id,
        )
    assert excinfo.value.code == "ledger_invalid_amount"


def test_a_reversal_is_a_new_balanced_transaction(db: Session) -> None:
    ops, _student, project, _assignment = _setup(db)
    original, _ = ledger.fund_project(db, ops, project=project, total_minor=1_000_000)

    reversal = ledger.reverse_transaction(
        db, ops, transaction_id=original.id, reason="client cancelled"
    )

    assert reversal.id != original.id
    assert reversal.kind == "reversal"
    assert reversal.reverses_transaction_id == original.id
    totals = _entry_totals(db, reversal.id)
    assert totals[DEBIT] == totals["credit"] == 1_000_000

    # The original rows were not edited: its balance still holds.
    original_totals = _entry_totals(db, original.id)
    assert original_totals[DEBIT] == original_totals["credit"]


def test_reversing_twice_returns_the_same_reversal(db: Session) -> None:
    ops, _student, project, _assignment = _setup(db)
    original, _ = ledger.fund_project(db, ops, project=project, total_minor=100_000)

    first = ledger.reverse_transaction(db, ops, transaction_id=original.id, reason="duplicate")
    second = ledger.reverse_transaction(db, ops, transaction_id=original.id, reason="duplicate")

    assert first.id == second.id
    assert db.scalar(select(func.count()).select_from(LedgerTransaction)) == 2


def test_a_reversal_needs_a_reason(db: Session) -> None:
    ops, _student, project, _assignment = _setup(db)
    original, _ = ledger.fund_project(db, ops, project=project, total_minor=10_000)

    with pytest.raises(ApiError) as excinfo:
        ledger.reverse_transaction(db, ops, transaction_id=original.id, reason="   ")
    assert excinfo.value.code == "reason_required"


def test_earnings_explain_tasks_rate_and_amount(db: Session) -> None:
    _ops, student, project, assignment = _setup(db)
    submission = _approved_submission(db, student, assignment)

    line = ledger.record_approval_earning(
        db, project=project, submission=submission, task_count=4
    )

    assert line.amount_minor == 4_000
    assert line.rate_minor == 1_000
    assert line.task_count == 4
    assert line.currency == "USD"
    assert line.status == "approved"
    assert "4 task(s) at 1000 USD each" in line.description


def test_only_approved_work_can_earn(db: Session) -> None:
    _ops, student, project, assignment = _setup(db)
    submission, _ = delivery.submit_work(
        db, student, assignment_id=assignment.id, payload={"a": 1}, client_key="money-2"
    )

    with pytest.raises(ApiError) as excinfo:
        ledger.record_approval_earning(db, project=project, submission=submission)
    assert excinfo.value.code == "not_approved"


def test_recording_an_earning_twice_returns_one_line(db: Session) -> None:
    _ops, student, project, assignment = _setup(db)
    submission = _approved_submission(db, student, assignment)

    first = ledger.record_approval_earning(db, project=project, submission=submission)
    second = ledger.record_approval_earning(db, project=project, submission=submission)

    assert first.id == second.id
    assert db.scalar(select(func.count()).select_from(EarningLine)) == 1


def test_payable_requires_approval_and_shows_in_my_earnings(db: Session) -> None:
    ops, student, project, assignment = _setup(db)
    submission = _approved_submission(db, student, assignment)
    ledger.record_approval_earning(db, project=project, submission=submission)

    assert ledger.mark_payable(db, project, actor=ops) == 1
    payload = ledger.my_earnings(db, student)
    assert payload["lines"][0]["status"] == "payable"
    assert payload["totals"] == [{"currency": "USD", "amount_minor": 1_000}]


def test_financials_track_funding_earnings_and_payment_status(db: Session) -> None:
    ops, student, project, assignment = _setup(db)
    ledger.fund_project(db, ops, project=project, total_minor=1_000_000)
    submission = _approved_submission(db, student, assignment)
    ledger.record_approval_earning(db, project=project, submission=submission)

    financials = ledger.project_financials(db, project)

    assert financials["funding"]["student_pool_minor"] == 900_000
    assert financials["department_share"]["amount_minor"] == 20_000
    assert financials["earnings_by_status"] == {"approved": 1_000}
    assert financials["payment_status"] == "approved"


def test_student_balance_never_goes_negative_without_a_payout(db: Session) -> None:
    _ops, student, project, assignment = _setup(db)
    submission = _approved_submission(db, student, assignment)
    ledger.record_approval_earning(db, project=project, submission=submission)

    balances = ledger.student_balances(db, student.id, "USD")
    assert balances["outstanding_minor"] == 0  # nothing has moved through the ledger yet
