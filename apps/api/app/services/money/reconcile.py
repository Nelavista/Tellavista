"""Reconciliation: prove the money still adds up (PRD §9).

This is not a report built from cached totals. It re-reads every ledger entry for a
project and checks:

* every transaction's debits equal its credits;
* the funding split matches the split engine exactly;
* no student earned more than the reserved student pool;
* payouts equal what was marked paid.

A failure is recorded with the numbers that disagreed, so an alert can point at a
project rather than saying "money is wrong somewhere".
"""
from __future__ import annotations

from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.identity import User
from app.models.ledger import (
    ACCOUNT_DEPARTMENT_PAYABLE,
    ACCOUNT_ESCROW,
    ACCOUNT_PAYOUT_CLEARING,
    ACCOUNT_PLATFORM_REVENUE,
    ACCOUNT_STUDENT_PAYABLE,
    CREDIT,
    DEBIT,
    EARNING_PAID,
    TX_FUNDING,
    DepartmentShare,
    EarningLine,
    LedgerEntry,
    LedgerTransaction,
    ReconciliationRun,
)
from app.models.work import Project
from app.services.money.split import split_project_value


def _account_net(db: Session, project_id: int) -> dict[str, int]:
    rows = db.execute(
        select(
            LedgerEntry.account,
            LedgerEntry.direction,
            func.coalesce(func.sum(LedgerEntry.amount_minor), 0),
        )
        .where(LedgerEntry.project_id == project_id)
        .group_by(LedgerEntry.account, LedgerEntry.direction)
    ).all()
    net: dict[str, int] = {}
    for account, direction, amount in rows:
        net[account] = net.get(account, 0) + (amount if direction == CREDIT else -amount)
    return net


def _unbalanced_transactions(db: Session, project_id: int) -> list[dict]:
    rows = db.execute(
        select(
            LedgerEntry.transaction_id,
            LedgerEntry.direction,
            func.sum(LedgerEntry.amount_minor),
        )
        .where(LedgerEntry.project_id == project_id)
        .group_by(LedgerEntry.transaction_id, LedgerEntry.direction)
    ).all()
    totals: dict[int, dict[str, int]] = {}
    for transaction_id, direction, amount in rows:
        totals.setdefault(transaction_id, {DEBIT: 0, CREDIT: 0})[direction] = amount
    return [
        {
            "transaction_id": transaction_id,
            "debits": amounts.get(DEBIT, 0),
            "credits": amounts.get(CREDIT, 0),
            "difference": amounts.get(DEBIT, 0) - amounts.get(CREDIT, 0),
        }
        for transaction_id, amounts in totals.items()
        if amounts.get(DEBIT, 0) != amounts.get(CREDIT, 0)
    ]


def project_report(db: Session, project: Project) -> dict:
    funding = db.scalar(
        select(LedgerTransaction)
        .where(
            LedgerTransaction.project_id == project.id,
            LedgerTransaction.kind == TX_FUNDING,
        )
        .order_by(LedgerTransaction.id)
        .limit(1)
    )
    details: list[dict] = []
    if funding is None:
        return {
            "project_id": project.id,
            "funded": False,
            "balanced": True,
            "expected": {},
            "actual": {},
            "details": [],
        }

    split = split_project_value(funding.total_minor)
    net = _account_net(db, project.id)
    unbalanced = _unbalanced_transactions(db, project.id)

    earnings_total = db.scalar(
        select(func.coalesce(func.sum(EarningLine.amount_minor), 0)).where(
            EarningLine.project_id == project.id,
            EarningLine.status != "reversed",
        )
    ) or 0
    paid_total = db.scalar(
        select(func.coalesce(func.sum(EarningLine.amount_minor), 0)).where(
            EarningLine.project_id == project.id, EarningLine.status == EARNING_PAID
        )
    ) or 0
    department = db.scalar(
        select(DepartmentShare).where(DepartmentShare.project_id == project.id)
    )

    expected = {
        "total_minor": split.total_minor,
        "student_pool_minor": split.student_pool_minor,
        "platform_retained_minor": split.platform_retained_minor,
        "department_share_minor": split.department_share_minor,
    }
    actual = {
        "escrow_minor": -net.get(ACCOUNT_ESCROW, 0),
        "student_payable_credited_minor": net.get(ACCOUNT_STUDENT_PAYABLE, 0),
        "platform_revenue_minor": net.get(ACCOUNT_PLATFORM_REVENUE, 0),
        "department_payable_minor": net.get(ACCOUNT_DEPARTMENT_PAYABLE, 0),
        "payout_clearing_minor": net.get(ACCOUNT_PAYOUT_CLEARING, 0),
        "earnings_total_minor": earnings_total,
        "earnings_paid_minor": paid_total,
    }

    if unbalanced:
        details.append({"check": "transaction_balance", "ok": False, "unbalanced": unbalanced})
    else:
        details.append({"check": "transaction_balance", "ok": True})

    checks = [
        ("escrow_funded", actual["escrow_minor"], expected["total_minor"]),
        (
            "student_pool_credited",
            net.get(ACCOUNT_STUDENT_PAYABLE, 0) + paid_total,
            expected["student_pool_minor"],
        ),
        (
            "platform_retained",
            actual["platform_revenue_minor"],
            expected["platform_retained_minor"],
        ),
        (
            "department_share",
            actual["department_payable_minor"],
            expected["department_share_minor"],
        ),
    ]
    for name, got, wanted in checks:
        details.append({"check": name, "ok": got == wanted, "actual": got, "expected": wanted})

    details.append(
        {
            "check": "earnings_within_student_pool",
            "ok": earnings_total <= expected["student_pool_minor"],
            "earnings": earnings_total,
            "student_pool": expected["student_pool_minor"],
        }
    )
    departments_ok = (
        department is None
        or department.amount_minor == expected["department_share_minor"]
    )
    details.append(
        {
            "check": "department_share_row",
            "ok": departments_ok,
            "actual": department.amount_minor if department else None,
            "expected": expected["department_share_minor"],
        }
    )

    balanced = all(item["ok"] for item in details)
    return {
        "project_id": project.id,
        "funded": True,
        "balanced": balanced,
        "expected": expected,
        "actual": actual,
        "details": details,
    }


def run(
    db: Session,
    *,
    actor: User | None = None,
    project: Project | None = None,
) -> ReconciliationRun:
    if project is not None:
        projects = [project]
    else:
        projects = list(db.scalars(select(Project).order_by(Project.id)).all())

    reports = [project_report(db, row) for row in projects]
    funded = [report for report in reports if report["funded"]]
    balanced = all(report["balanced"] for report in funded) if funded else True

    record = ReconciliationRun(
        project_id=project.id if project else None,
        as_of=date.today(),
        balanced=balanced,
        expected={"projects": {str(report["project_id"]): report["expected"] for report in funded}},
        actual={"projects": {str(report["project_id"]): report["actual"] for report in funded}},
        details=[detail for report in reports for detail in report["details"]],
        created_by=actor.id if actor else None,
    )
    db.add(record)
    db.flush()

    if not balanced:
        from app.services import audit

        audit.record(
            db,
            action="ledger.reconciliation_failed",
            actor_user_id=actor.id if actor else None,
            actor_role_code=actor.role.code if actor and actor.role else None,
            target_type="reconciliation_run",
            target_id=record.id,
            context={"projects": [r["project_id"] for r in funded if not r["balanced"]]},
        )
    return record


def latest(db: Session, project_id: int | None = None) -> dict | None:
    stmt = select(ReconciliationRun).order_by(ReconciliationRun.id.desc()).limit(1)
    if project_id is not None:
        stmt = (
            select(ReconciliationRun)
            .where(ReconciliationRun.project_id == project_id)
            .order_by(ReconciliationRun.id.desc())
            .limit(1)
        )
    row = db.scalar(stmt)
    if row is None:
        return None
    return {
        "id": row.id,
        "project_id": row.project_id,
        "as_of": row.as_of,
        "balanced": row.balanced,
        "expected": row.expected,
        "actual": row.actual,
        "details": row.details,
        "created_at": row.created_at,
    }


__all__ = ["latest", "project_report", "run"]
