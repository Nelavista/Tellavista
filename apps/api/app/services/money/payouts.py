"""Payout batches with a provider abstraction (PRD §9).

The first provider is `manual`: ops marks a batch paid after transferring money
outside V2, and exports the batch as CSV. The abstraction is deliberately small
(`pay(batch, items) -> references`) so a real rail can be added without touching
the ledger, the approval rules or the student's Earnings screen.

Approval is two-person above a threshold. That rule lives here, not in the admin
UI, because an ops tool must not be able to bypass it.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.core.time import utcnow
from app.models.identity import User
from app.models.ledger import (
    BATCH_APPROVED,
    BATCH_CANCELLED,
    BATCH_DRAFT,
    BATCH_FAILED,
    BATCH_PAID,
    EARNING_APPROVED,
    EARNING_FAILED,
    EARNING_PAID,
    EARNING_PAYABLE,
    SECOND_APPROVER_THRESHOLD_MINOR,
    EarningLine,
    PayoutBatch,
    PayoutItem,
)
from app.models.work import Project
from app.services import audit
from app.services.money.ledger import payout_transaction
from app.services.notifications import notify


class PayoutProvider(Protocol):
    name: str

    def pay(self, batch: PayoutBatch, items: list[PayoutItem]) -> dict[int, str]: ...


@dataclass
class ManualProvider:
    """Ops pays outside the system and pastes back a reference."""

    name: str = "manual"

    def pay(self, batch: PayoutBatch, items: list[PayoutItem]) -> dict[int, str]:
        return {item.id: f"manual:{batch.id}:{item.id}" for item in items}


PROVIDERS: dict[str, PayoutProvider] = {"manual": ManualProvider()}


def create_batch(
    db: Session,
    actor: User,
    *,
    project: Project,
    earning_line_ids: list[int] | None = None,
    provider: str = "manual",
    idempotency_key: str | None = None,
) -> PayoutBatch:
    if provider not in PROVIDERS:
        raise ApiError(400, "unknown_provider", "That payout provider is not configured.")
    if idempotency_key:
        existing = db.scalar(
            select(PayoutBatch).where(PayoutBatch.idempotency_key == idempotency_key)
        )
        if existing is not None:
            return existing

    stmt = select(EarningLine).where(
        EarningLine.project_id == project.id,
        EarningLine.status.in_([EARNING_PAYABLE, EARNING_APPROVED]),
    )
    if earning_line_ids is not None:
        stmt = stmt.where(EarningLine.id.in_(earning_line_ids))
    lines = list(db.scalars(stmt).all())
    if not lines:
        raise ApiError(409, "nothing_payable", "There is no approved work to pay.")

    currencies = {line.currency for line in lines}
    if len(currencies) > 1:
        raise ApiError(409, "mixed_currencies", "A payout batch must use one currency.")
    currency = currencies.pop()

    by_user: dict[int, list[EarningLine]] = {}
    for line in lines:
        by_user.setdefault(line.user_id, []).append(line)

    batch = PayoutBatch(
        project_id=project.id,
        currency=currency,
        total_minor=sum(line.amount_minor for line in lines),
        status=BATCH_DRAFT,
        provider=provider,
        idempotency_key=idempotency_key,
        created_by=actor.id,
    )
    db.add(batch)
    db.flush()

    for user_id, user_lines in by_user.items():
        amount = sum(line.amount_minor for line in user_lines)
        item = PayoutItem(
            batch_id=batch.id,
            user_id=user_id,
            amount_minor=amount,
            currency=currency,
            status=EARNING_APPROVED,
        )
        db.add(item)
        db.flush()
        for line in user_lines:
            line.status = EARNING_PAYABLE
            line.payout_item_id = item.id
    db.flush()

    audit.record(
        db,
        action="payout.batch_created",
        actor_user_id=actor.id,
        actor_role_code=actor.role.code if actor.role else None,
        target_type="payout_batch",
        target_id=batch.id,
        context={"project_id": project.id, "total_minor": batch.total_minor},
    )
    return batch


def approve_batch(db: Session, actor: User, batch: PayoutBatch) -> PayoutBatch:
    if batch.status not in {BATCH_DRAFT, BATCH_APPROVED}:
        raise ApiError(409, "batch_not_approvable", "This batch cannot be approved now.")
    if batch.status == BATCH_APPROVED:
        return batch
    if (
        batch.total_minor >= SECOND_APPROVER_THRESHOLD_MINOR
        and batch.created_by == actor.id
    ):
        raise ApiError(
            403,
            "second_approver_required",
            "A second person must approve a payout this large.",
            {"threshold_minor": SECOND_APPROVER_THRESHOLD_MINOR},
        )
    batch.status = BATCH_APPROVED
    batch.approved_by = actor.id
    batch.approved_at = utcnow()
    db.flush()
    audit.record(
        db,
        action="payout.batch_approved",
        actor_user_id=actor.id,
        actor_role_code=actor.role.code if actor.role else None,
        target_type="payout_batch",
        target_id=batch.id,
        context={"total_minor": batch.total_minor, "created_by": batch.created_by},
    )
    return batch


def pay_batch(db: Session, actor: User, batch: PayoutBatch) -> PayoutBatch:
    if batch.status == BATCH_PAID:
        return batch
    if batch.status != BATCH_APPROVED:
        raise ApiError(409, "batch_not_approved", "Approve this batch before paying it.")
    items = list(
        db.scalars(select(PayoutItem).where(PayoutItem.batch_id == batch.id)).all()
    )
    if not items:
        raise ApiError(409, "batch_empty", "This batch has no items.")
    provider = PROVIDERS.get(batch.provider)
    if provider is None:
        raise ApiError(400, "unknown_provider", "That payout provider is not configured.")

    try:
        references = provider.pay(batch, items)
    except Exception as exc:  # noqa: BLE001 - a provider failure must be recorded
        batch.status = BATCH_FAILED
        batch.failure_reason = f"{type(exc).__name__}: {exc}"[:255]
        db.flush()
        audit.record(
            db,
            action="payout.batch_failed",
            actor_user_id=actor.id,
            target_type="payout_batch",
            target_id=batch.id,
            reason=batch.failure_reason,
        )
        raise ApiError(502, "payout_failed", "The payout provider failed. Nothing was marked paid.") from exc

    transaction = payout_transaction(
        db,
        project_id=batch.project_id,
        currency=batch.currency,
        items=[
            {"user_id": item.user_id, "amount_minor": item.amount_minor} for item in items
        ],
        idempotency_key=f"payout:batch:{batch.id}",
        actor_user_id=actor.id,
    )

    for item in items:
        item.status = EARNING_PAID
        item.provider_reference = references.get(item.id)
        item.ledger_transaction_id = transaction.id
        for line in db.scalars(
            select(EarningLine).where(EarningLine.payout_item_id == item.id)
        ).all():
            line.status = EARNING_PAID
            line.ledger_transaction_id = transaction.id
        from app.core import observability

        observability.capture(
            item.user_id,
            observability.EVENTS["paid"],
            {"batch_id": batch.id, "amount_minor": item.amount_minor},
        )
        notify(
            db,
            user_id=item.user_id,
            kind="payment",
            title="Payment sent",
            body=f"{item.amount_minor} {item.currency} minor units is on its way.",
            data={"batch_id": batch.id, "amount_minor": item.amount_minor},
        )

    batch.status = BATCH_PAID
    batch.paid_at = utcnow()
    db.flush()
    audit.record(
        db,
        action="payout.batch_paid",
        actor_user_id=actor.id,
        actor_role_code=actor.role.code if actor.role else None,
        target_type="payout_batch",
        target_id=batch.id,
        context={"total_minor": batch.total_minor, "items": len(items)},
    )
    return batch


def fail_item(
    db: Session, actor: User, item_id: int, *, reason: str
) -> PayoutItem:
    item = db.get(PayoutItem, item_id)
    if item is None:
        raise ApiError(404, "payout_item_not_found", "That payout item does not exist.")
    if item.status == EARNING_PAID:
        raise ApiError(409, "already_paid", "A paid item needs a reversal, not a failure.")
    item.status = EARNING_FAILED
    item.failure_reason = reason[:255]
    for line in db.scalars(
        select(EarningLine).where(EarningLine.payout_item_id == item.id)
    ).all():
        line.status = EARNING_FAILED
    db.flush()
    audit.record(
        db,
        action="payout.item_failed",
        actor_user_id=actor.id,
        target_type="payout_item",
        target_id=item.id,
        reason=reason,
    )
    return item


def cancel_batch(db: Session, actor: User, batch: PayoutBatch, *, reason: str) -> PayoutBatch:
    if batch.status in {BATCH_PAID, BATCH_CANCELLED}:
        raise ApiError(409, "batch_not_cancellable", "This batch cannot be cancelled.")
    for item in db.scalars(select(PayoutItem).where(PayoutItem.batch_id == batch.id)).all():
        for line in db.scalars(
            select(EarningLine).where(EarningLine.payout_item_id == item.id)
        ).all():
            line.status = EARNING_PAYABLE
            line.payout_item_id = None
        item.status = EARNING_FAILED
    batch.status = BATCH_CANCELLED
    batch.failure_reason = reason[:255]
    db.flush()
    audit.record(
        db,
        action="payout.batch_cancelled",
        actor_user_id=actor.id,
        actor_role_code=actor.role.code if actor.role else None,
        target_type="payout_batch",
        target_id=batch.id,
        reason=reason,
    )
    return batch


def batch_detail(db: Session, batch: PayoutBatch) -> dict:
    items = db.execute(
        select(PayoutItem, User)
        .join(User, User.id == PayoutItem.user_id)
        .where(PayoutItem.batch_id == batch.id)
        .order_by(PayoutItem.id)
    ).all()
    return {
        "id": batch.id,
        "project_id": batch.project_id,
        "currency": batch.currency,
        "total_minor": batch.total_minor,
        "status": batch.status,
        "provider": batch.provider,
        "created_by": batch.created_by,
        "approved_by": batch.approved_by,
        "approved_at": batch.approved_at,
        "paid_at": batch.paid_at,
        "failure_reason": batch.failure_reason,
        "items": [
            {
                "id": item.id,
                "user_id": item.user_id,
                "name": user.name,
                "email": user.email,
                "amount_minor": item.amount_minor,
                "status": item.status,
                "provider_reference": item.provider_reference,
            }
            for item, user in items
        ],
    }


def export_csv(db: Session, batch: PayoutBatch) -> str:
    """A payout file ops can hand to a bank or a manual rail."""
    rows = ["user_id,email,amount_minor,currency,status,reference"]
    for item, user in db.execute(
        select(PayoutItem, User)
        .join(User, User.id == PayoutItem.user_id)
        .where(PayoutItem.batch_id == batch.id)
        .order_by(PayoutItem.id)
    ).all():
        reference = item.provider_reference or ""
        rows.append(
            f"{user.id},{user.email},{item.amount_minor},{item.currency},"
            f"{item.status},{reference}"
        )
    return "\n".join(rows) + "\n"


__all__ = [
    "ManualProvider",
    "PROVIDERS",
    "approve_batch",
    "batch_detail",
    "cancel_batch",
    "create_batch",
    "export_csv",
    "fail_item",
    "pay_batch",
]
