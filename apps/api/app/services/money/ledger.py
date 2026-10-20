"""The ledger service: balanced postings, funding and earnings (ADR-0008).

Callers never write `LedgerEntry` directly. `post_transaction` validates that the
entries are a real transaction (debits equal credits, one currency, positive integer
amounts) and gives it an idempotency key. A retry returns the first transaction.

`EarningLine` is the explanation layer: each approved submission becomes a line
showing the task count, rate and amount, with a payment state of its own. The sum
of the student pool is reserved at funding; individual lines are what students see.
"""
from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.identity import User
from app.models.ledger import (
    ACCOUNT_DEPARTMENT_PAYABLE,
    ACCOUNT_ESCROW,
    ACCOUNT_PAYOUT_CLEARING,
    ACCOUNT_PLATFORM_REVENUE,
    ACCOUNT_STUDENT_PAYABLE,
    ACCOUNTS,
    CREDIT,
    DEBIT,
    DIRECTIONS,
    EARNING_APPROVED,
    EARNING_PAID,
    EARNING_PAYABLE,
    EARNING_PENDING_QUALITY,
    EARNING_REVERSED,
    TX_ADJUSTMENT,
    TX_FUNDING,
    TX_KINDS,
    TX_PAYOUT,
    TX_REVERSAL,
    DepartmentShare,
    EarningLine,
    LedgerEntry,
    LedgerTransaction,
)
from app.models.matching import OPPORTUNITY_MANAGED
from app.models.work import Project, Submission
from app.services import audit
from app.services.money.split import Split, split_project_value


def _validate_entries(entries: list[dict], currency: str) -> int:
    if not entries:
        raise ApiError(400, "ledger_empty", "A transaction needs at least two entries.")
    debits = 0
    credits = 0
    for entry in entries:
        if entry.get("account") not in ACCOUNTS:
            raise ApiError(400, "ledger_invalid_account", "Unknown ledger account.")
        if entry.get("direction") not in DIRECTIONS:
            raise ApiError(400, "ledger_invalid_direction", "Direction must be debit or credit.")
        amount = entry.get("amount_minor")
        if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
            raise ApiError(
                400, "ledger_invalid_amount", "Every amount must be a positive integer."
            )
        if entry.get("currency", currency) != currency:
            raise ApiError(400, "ledger_currency_mismatch", "One transaction, one currency.")
        if entry["direction"] == DEBIT:
            debits += amount
        else:
            credits += amount
    if debits != credits:
        raise ApiError(
            400,
            "ledger_unbalanced",
            "This transaction does not balance.",
            {"debits": debits, "credits": credits},
        )
    return debits


def post_transaction(
    db: Session,
    *,
    kind: str,
    currency: str,
    entries: list[dict],
    idempotency_key: str,
    project_id: int | None = None,
    description: str | None = None,
    actor_user_id: int | None = None,
    reverses_transaction_id: int | None = None,
) -> LedgerTransaction:
    if kind not in TX_KINDS:
        raise ApiError(400, "ledger_invalid_kind", "Unknown ledger transaction kind.")
    if not idempotency_key or len(idempotency_key) > 80:
        raise ApiError(400, "ledger_key_required", "A transaction needs an idempotency key.")
    currency = currency.upper()
    if len(currency) != 3:
        raise ApiError(400, "invalid_currency", "Use a three-letter currency code.")
    total = _validate_entries(entries, currency)

    existing = db.scalar(
        select(LedgerTransaction).where(
            LedgerTransaction.idempotency_key == idempotency_key
        )
    )
    if existing is not None:
        if existing.total_minor != total or existing.currency != currency:
            raise ApiError(
                409,
                "ledger.key_reused",
                "This ledger key was already used for a different transaction.",
            )
        return existing

    transaction = LedgerTransaction(
        kind=kind,
        project_id=project_id,
        currency=currency,
        total_minor=total,
        description=description,
        idempotency_key=idempotency_key,
        reverses_transaction_id=reverses_transaction_id,
        actor_user_id=actor_user_id,
    )
    db.add(transaction)
    db.flush()
    for entry in entries:
        db.add(
            LedgerEntry(
                transaction_id=transaction.id,
                account=entry["account"],
                direction=entry["direction"],
                amount_minor=entry["amount_minor"],
                currency=currency,
                project_id=project_id,
                user_id=entry.get("user_id"),
                department_id=entry.get("department_id"),
                description=entry.get("description"),
            )
        )
    db.flush()
    return transaction


def fund_project(
    db: Session,
    actor: User,
    *,
    project: Project,
    total_minor: int,
    currency: str | None = None,
) -> tuple[LedgerTransaction, Split]:
    """Reserve a project's value and credit the three shares."""
    from app.models.matching import Opportunity

    opportunity = db.get(Opportunity, project.opportunity_id)
    if opportunity is None:
        raise ApiError(404, "opportunity_not_found", "This project has no opportunity.")
    if opportunity.type != OPPORTUNITY_MANAGED:
        raise ApiError(
            403,
            "external_has_no_ledger",
            "External opportunities never create ledger entries.",
        )
    # G1: the fallback is the configured billing currency, not a hardcoded code.
    # A project that names its own currency still wins, so existing contracts do
    # not change meaning when ops switches the default.
    from app.services.platform import settings as policy

    configured = policy.get_platform_settings(db)
    project_currency = (currency or opportunity.currency or configured.billing_currency).upper()
    if len(project_currency) != 3:
        raise ApiError(400, "invalid_currency", "This project has no currency.")
    if project_currency not in {code.upper() for code in configured.allowed_currencies}:
        raise ApiError(
            400,
            "unsupported_currency",
            "That currency is not enabled for billing.",
            {"allowed": list(configured.allowed_currencies)},
        )
    split = split_project_value(total_minor)

    entries: list[dict[str, Any]] = [
        {
            "account": ACCOUNT_ESCROW,
            "direction": DEBIT,
            "amount_minor": total_minor,
            "description": "client funds received",
        },
        {
            "account": ACCOUNT_STUDENT_PAYABLE,
            "direction": CREDIT,
            "amount_minor": split.student_pool_minor,
            "description": "student pool (90%)",
        },
        {
            "account": ACCOUNT_PLATFORM_REVENUE,
            "direction": CREDIT,
            "amount_minor": split.platform_retained_minor,
            "description": "platform share (8%)",
        },
    ]
    if split.department_share_minor:
        entries.append(
            {
                "account": ACCOUNT_DEPARTMENT_PAYABLE,
                "direction": CREDIT,
                "amount_minor": split.department_share_minor,
                "department_id": opportunity.department_id,
                "description": "department share (2%, from the fee)",
            }
        )

    transaction = post_transaction(
        db,
        kind=TX_FUNDING,
        currency=project_currency,
        entries=entries,
        project_id=project.id,
        idempotency_key=f"funding:project:{project.id}:{total_minor}",
        description=f"Fund {project.title}",
        actor_user_id=actor.id,
    )

    share = db.scalar(
        select(DepartmentShare).where(
            DepartmentShare.project_id == project.id,
            DepartmentShare.department_id == opportunity.department_id,
        )
    )
    if share is None:
        share = DepartmentShare(
            project_id=project.id,
            department_id=opportunity.department_id,
            amount_minor=split.department_share_minor,
            currency=project_currency,
            ledger_transaction_id=transaction.id,
        )
        db.add(share)
    else:
        share.amount_minor = split.department_share_minor
        share.ledger_transaction_id = transaction.id
    db.flush()

    audit.record(
        db,
        action="ledger.project_funded",
        actor_user_id=actor.id,
        actor_role_code=actor.role.code if actor.role else None,
        target_type="project",
        target_id=project.id,
        context={**split.as_dict(), "currency": project_currency},
    )
    return transaction, split


def record_approval_earning(
    db: Session,
    *,
    project: Project,
    submission: Submission,
    task_count: int | None = None,
) -> EarningLine:
    """Create the student-visible earning line for an approved submission."""
    if submission.status != "approved":
        raise ApiError(400, "not_approved", "Only approved work can earn.")
    existing = db.scalar(
        select(EarningLine).where(EarningLine.submission_id == submission.id)
    )
    if existing is not None:
        return existing

    from app.models.matching import Opportunity

    opportunity = db.get(Opportunity, project.opportunity_id)
    if opportunity is None or opportunity.type != OPPORTUNITY_MANAGED:
        raise ApiError(403, "external_has_no_ledger", "Only managed work earns.")
    if opportunity.currency is None or opportunity.rate_minor is None:
        raise ApiError(400, "rate_missing", "This project has no rate, so work cannot be paid.")

    count = task_count or int((submission.payload or {}).get("task_count", 1) or 1)
    count = max(1, count)
    amount = opportunity.rate_minor * count
    line = EarningLine(
        user_id=submission.user_id,
        project_id=project.id,
        submission_id=submission.id,
        amount_minor=amount,
        currency=opportunity.currency,
        rate_minor=opportunity.rate_minor,
        task_count=count,
        status=EARNING_APPROVED,
        description=f"{count} task(s) at {opportunity.rate_minor} {opportunity.currency} each",
    )
    db.add(line)
    db.flush()
    return line


def mark_payable(db: Session, project: Project, *, actor: User | None = None) -> int:
    lines = db.scalars(
        select(EarningLine).where(
            EarningLine.project_id == project.id,
            EarningLine.status == EARNING_APPROVED,
        )
    ).all()
    for line in lines:
        line.status = EARNING_PAYABLE
    db.flush()
    if actor is not None:
        audit.record(
            db,
            action="ledger.earnings_payable",
            actor_user_id=actor.id,
            actor_role_code=actor.role.code if actor.role else None,
            target_type="project",
            target_id=project.id,
            context={"lines": len(lines)},
        )
    return len(lines)


def apply_earning_status(
    db: Session, earning_line_ids: list[int], status: str
) -> int:
    rows = db.scalars(
        select(EarningLine).where(EarningLine.id.in_(earning_line_ids))
    ).all()
    for row in rows:
        row.status = status
    db.flush()
    return len(rows)


def reverse_transaction(
    db: Session, actor: User, *, transaction_id: int, reason: str
) -> LedgerTransaction:
    """Undo a posting with a new transaction. The original is never edited."""
    if not reason.strip():
        raise ApiError(400, "reason_required", "A reversal needs a reason.")
    original = db.get(LedgerTransaction, transaction_id)
    if original is None:
        raise ApiError(404, "transaction_not_found", "That ledger transaction does not exist.")
    if original.kind == TX_REVERSAL:
        raise ApiError(400, "cannot_reverse_reversal", "A reversal cannot itself be reversed.")
    already = db.scalar(
        select(LedgerTransaction).where(
            LedgerTransaction.reverses_transaction_id == original.id
        )
    )
    if already is not None:
        return already

    entries = []
    for entry in db.scalars(
        select(LedgerEntry).where(LedgerEntry.transaction_id == original.id)
    ).all():
        entries.append(
            {
                "account": entry.account,
                "direction": CREDIT if entry.direction == DEBIT else DEBIT,
                "amount_minor": entry.amount_minor,
                "user_id": entry.user_id,
                "department_id": entry.department_id,
                "description": f"reversal of #{entry.id}",
            }
        )
    reversal = post_transaction(
        db,
        kind=TX_REVERSAL,
        currency=original.currency,
        entries=entries,
        project_id=original.project_id,
        idempotency_key=f"reversal:{original.id}",
        description=reason[:255],
        actor_user_id=actor.id,
        reverses_transaction_id=original.id,
    )
    for line in db.scalars(
        select(EarningLine).where(EarningLine.ledger_transaction_id == original.id)
    ).all():
        line.status = EARNING_REVERSED
    db.flush()
    audit.record(
        db,
        action="ledger.reversed",
        actor_user_id=actor.id,
        actor_role_code=actor.role.code if actor.role else None,
        target_type="ledger_transaction",
        target_id=original.id,
        reason=reason,
    )
    return reversal


def payout_transaction(
    db: Session,
    *,
    project_id: int,
    currency: str,
    items: list[dict],
    idempotency_key: str,
    actor_user_id: int,
) -> LedgerTransaction:
    """Move payable money to payout clearing, one credit entry per student."""
    total = sum(item["amount_minor"] for item in items)
    entries: list[dict[str, Any]] = [
        {
            "account": ACCOUNT_STUDENT_PAYABLE,
            "direction": DEBIT,
            "amount_minor": total,
            "description": "student payouts released",
        }
    ]
    for item in items:
        entries.append(
            {
                "account": ACCOUNT_PAYOUT_CLEARING,
                "direction": CREDIT,
                "amount_minor": item["amount_minor"],
                "user_id": item["user_id"],
                "description": "paid to student",
            }
        )
    return post_transaction(
        db,
        kind=TX_PAYOUT,
        currency=currency,
        entries=entries,
        project_id=project_id,
        idempotency_key=idempotency_key,
        description="Student payout batch",
        actor_user_id=actor_user_id,
    )


def project_financials(db: Session, project: Project) -> dict:
    from app.models.matching import Opportunity

    opportunity = db.get(Opportunity, project.opportunity_id)
    funding = db.scalar(
        select(LedgerTransaction)
        .where(
            LedgerTransaction.project_id == project.id,
            LedgerTransaction.kind == TX_FUNDING,
        )
        .order_by(LedgerTransaction.id)
        .limit(1)
    )
    split = split_project_value(funding.total_minor) if funding else None
    earnings = dict(
        db.execute(
            select(EarningLine.status, func.coalesce(func.sum(EarningLine.amount_minor), 0))
            .where(EarningLine.project_id == project.id)
            .group_by(EarningLine.status)
        ).all()
    )
    share = db.scalar(
        select(DepartmentShare).where(DepartmentShare.project_id == project.id)
    )
    return {
        "project_id": project.id,
        "currency": opportunity.currency if opportunity else None,
        "funding": split.as_dict() if split else None,
        "student_pool_minor": split.student_pool_minor if split else 0,
        "earnings_by_status": earnings,
        "earning_total_minor": sum(earnings.values()),
        "department_share": (
            {
                "department_id": share.department_id,
                "amount_minor": share.amount_minor,
                "currency": share.currency,
                "status": share.status,
            }
            if share
            else None
        ),
        "work_status": None,
        "quality_status": None,
        "payment_status": _payment_status(earnings),
    }


def _payment_status(earnings: dict[str, int]) -> str:
    if not earnings:
        return "unpaid"
    if earnings.get(EARNING_PAID):
        return "partially_paid" if len(earnings) > 1 else "paid"
    if earnings.get(EARNING_PAYABLE):
        return "payable"
    if earnings.get(EARNING_APPROVED):
        return "approved"
    if earnings.get(EARNING_PENDING_QUALITY):
        return "pending_quality"
    if earnings.get(EARNING_REVERSED):
        return "reversed"
    return "unpaid"


def my_earnings(db: Session, user: User) -> dict:
    rows = db.execute(
        select(EarningLine, Project)
        .join(Project, Project.id == EarningLine.project_id)
        .where(EarningLine.user_id == user.id)
        .order_by(EarningLine.id.desc())
    ).all()
    totals: dict[str, int] = {}
    for line, _project in rows:
        totals[line.currency] = totals.get(line.currency, 0) + (
            line.amount_minor if line.status != EARNING_REVERSED else -line.amount_minor
        )
    return {
        "totals": [
            {"currency": currency, "amount_minor": amount}
            for currency, amount in sorted(totals.items())
        ],
        "lines": [
            {
                "id": line.id,
                "project": {"slug": project.slug, "title": project.title},
                "submission_id": line.submission_id,
                "amount_minor": line.amount_minor,
                "currency": line.currency,
                "rate_minor": line.rate_minor,
                "task_count": line.task_count,
                "status": line.status,
                "description": line.description,
                "paid": line.status == EARNING_PAID,
            }
            for line, project in rows
        ],
    }


def student_balances(db: Session, user_id: int, currency: str) -> dict[str, int]:
    rows = db.execute(
        select(LedgerEntry.direction, func.coalesce(func.sum(LedgerEntry.amount_minor), 0))
        .where(
            LedgerEntry.user_id == user_id,
            LedgerEntry.account == ACCOUNT_STUDENT_PAYABLE,
            LedgerEntry.currency == currency,
        )
        .group_by(LedgerEntry.direction)
    ).all()
    balances = dict(rows)
    return {
        "earned_minor": balances.get(CREDIT, 0),
        "paid_minor": balances.get(DEBIT, 0),
        "outstanding_minor": balances.get(CREDIT, 0) - balances.get(DEBIT, 0),
    }


__all__ = [
    "TX_ADJUSTMENT",
    "apply_earning_status",
    "fund_project",
    "mark_payable",
    "my_earnings",
    "payout_transaction",
    "post_transaction",
    "project_financials",
    "record_approval_earning",
    "reverse_transaction",
    "student_balances",
]
