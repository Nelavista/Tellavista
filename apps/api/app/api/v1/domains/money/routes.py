"""Money endpoints: earnings, ledger, payouts and reconciliation (Phase 6).

Students only ever read their own earnings; the ledger itself is ops-only. Amounts
are integers in minor units with a currency code — no endpoint accepts or returns
a float, and no endpoint edits a ledger row: a correction is a reversal.

Payout routes are deliberately narrow: create, approve, pay, cancel, and record a
failed item. The second-approver rule for large batches is enforced in the service,
not here, so a new caller cannot bypass it.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Header, Query, Response
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_flag
from app.core import flags
from app.core.authz import require_permission
from app.core.errors import ApiError
from app.db.session import get_db
from app.models.identity import User
from app.models.ledger import LedgerEntry, LedgerTransaction, PayoutBatch
from app.services.money import ledger, payouts, reconcile
from app.services.work import cohorts

router = APIRouter(
    prefix="/money",
    tags=["money"],
    dependencies=[Depends(require_flag(flags.LEDGER))],
)


class FundIn(BaseModel):
    total_minor: int = Field(gt=0)
    currency: str | None = Field(default=None, min_length=3, max_length=3)


class ReverseIn(BaseModel):
    reason: str = Field(min_length=3, max_length=255)


class BatchIn(BaseModel):
    earning_line_ids: list[int] | None = None
    provider: str = Field(default="manual", max_length=30)


class CancelIn(BaseModel):
    reason: str = Field(min_length=3, max_length=255)


class FailIn(BaseModel):
    reason: str = Field(min_length=3, max_length=255)


def _batch(db: Session, batch_id: int) -> PayoutBatch:
    row = db.get(PayoutBatch, batch_id)
    if row is None:
        raise ApiError(404, "payout_batch_not_found", "That payout batch does not exist.")
    return row


@router.get("/earnings")
def my_earnings(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    """Every line shows why: tasks approved, the rate used, and the status."""
    return ledger.my_earnings(db, user)


@router.get("/projects/{slug}/financials")
def project_financials(
    slug: str,
    _actor: User = Depends(require_permission("ledger.read")),
    db: Session = Depends(get_db),
) -> dict:
    project = cohorts.get_project(db, slug)
    return ledger.project_financials(db, project)


@router.post("/projects/{slug}/fund", status_code=201)
def fund_project(
    slug: str,
    payload: FundIn,
    actor: User = Depends(require_permission("payout.request")),
    db: Session = Depends(get_db),
) -> dict:
    """Reserve the client's payment and credit the 90/8/2 shares exactly once."""
    project = cohorts.get_project(db, slug)
    transaction, split = ledger.fund_project(
        db, actor, project=project, total_minor=payload.total_minor, currency=payload.currency
    )
    db.commit()
    return {
        "transaction_id": transaction.id,
        "currency": transaction.currency,
        "total_minor": transaction.total_minor,
        "student_pool_minor": split.student_pool_minor,
        "platform_fee_minor": split.platform_fee_minor,
        "department_share_minor": split.department_share_minor,
    }


@router.post("/transactions/{transaction_id}/reverse", status_code=201)
def reverse_transaction(
    transaction_id: int,
    payload: ReverseIn,
    actor: User = Depends(require_permission("payout.request")),
    db: Session = Depends(get_db),
) -> dict:
    row = ledger.reverse_transaction(db, actor, transaction_id=transaction_id, reason=payload.reason)
    db.commit()
    return {
        "id": row.id,
        "kind": row.kind,
        "reverses_transaction_id": row.reverses_transaction_id,
        "total_minor": row.total_minor,
    }


@router.get("/projects/{slug}/ledger")
def ledger_explorer(
    slug: str,
    limit: int = Query(default=100, ge=1, le=500),
    _actor: User = Depends(require_permission("ledger.read")),
    db: Session = Depends(get_db),
) -> dict:
    """The immutable rows behind every balance, newest first."""
    project = cohorts.get_project(db, slug)
    transactions = db.scalars(
        select(LedgerTransaction)
        .where(LedgerTransaction.project_id == project.id)
        .order_by(LedgerTransaction.id.desc())
        .limit(limit)
    ).all()
    ids = [row.id for row in transactions]
    entries: dict[int, list[dict]] = {row_id: [] for row_id in ids}
    if ids:
        for entry in db.scalars(
            select(LedgerEntry)
            .where(LedgerEntry.transaction_id.in_(ids))
            .order_by(LedgerEntry.id)
        ).all():
            entries[entry.transaction_id].append(
                {
                    "id": entry.id,
                    "account": entry.account,
                    "direction": entry.direction,
                    "amount_minor": entry.amount_minor,
                    "currency": entry.currency,
                    "user_id": entry.user_id,
                    "department_id": entry.department_id,
                    "description": entry.description,
                }
            )
    return {
        "project_id": project.id,
        "transactions": [
            {
                "id": row.id,
                "kind": row.kind,
                "currency": row.currency,
                "total_minor": row.total_minor,
                "description": row.description,
                "reverses_transaction_id": row.reverses_transaction_id,
                "created_at": row.created_at,
                "entries": entries[row.id],
            }
            for row in transactions
        ],
    }


@router.get("/projects/{slug}/ledger/export")
def export_ledger(
    slug: str,
    _actor: User = Depends(require_permission("ledger.read")),
    db: Session = Depends(get_db),
) -> Response:
    """A flat CSV of every entry, for an accountant or a support investigation."""
    project = cohorts.get_project(db, slug)
    rows = ["transaction_id,kind,account,direction,amount_minor,currency,user_id,department_id"]
    for entry, transaction in db.execute(
        select(LedgerEntry, LedgerTransaction)
        .join(LedgerTransaction, LedgerTransaction.id == LedgerEntry.transaction_id)
        .where(LedgerEntry.project_id == project.id)
        .order_by(LedgerEntry.id)
    ).all():
        rows.append(
            f"{transaction.id},{transaction.kind},{entry.account},{entry.direction},"
            f"{entry.amount_minor},{entry.currency},{entry.user_id or ''},{entry.department_id or ''}"
        )
    return Response(
        content="\n".join(rows) + "\n",
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="ledger-{project.slug}.csv"'},
    )


@router.get("/projects/{slug}/reconciliation")
def project_reconciliation(
    slug: str,
    _actor: User = Depends(require_permission("ledger.read")),
    db: Session = Depends(get_db),
) -> dict:
    project = cohorts.get_project(db, slug)
    return reconcile.project_report(db, project)


@router.post("/reconciliation/run", status_code=201)
def run_reconciliation(
    project_slug: str | None = Query(default=None),
    actor: User = Depends(require_permission("ledger.read")),
    db: Session = Depends(get_db),
) -> dict:
    project = cohorts.get_project(db, project_slug) if project_slug else None
    run = reconcile.run(db, actor=actor, project=project)
    db.commit()
    return {
        "id": run.id,
        "as_of": run.as_of,
        "balanced": run.balanced,
        "project_id": run.project_id,
    }


@router.get("/projects/{slug}/payout-batches")
def list_batches(
    slug: str,
    _actor: User = Depends(require_permission("ledger.read")),
    db: Session = Depends(get_db),
) -> dict:
    project = cohorts.get_project(db, slug)
    rows = db.scalars(
        select(PayoutBatch)
        .where(PayoutBatch.project_id == project.id)
        .order_by(PayoutBatch.id.desc())
    ).all()
    return {
        "batches": [
            {
                "id": row.id,
                "currency": row.currency,
                "total_minor": row.total_minor,
                "status": row.status,
                "provider": row.provider,
                "paid_at": row.paid_at,
            }
            for row in rows
        ]
    }


@router.post("/projects/{slug}/payout-batches", status_code=201)
def create_batch(
    slug: str,
    payload: BatchIn,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    actor: User = Depends(require_permission("payout.request")),
    db: Session = Depends(get_db),
) -> dict:
    project = cohorts.get_project(db, slug)
    batch = payouts.create_batch(
        db,
        actor,
        project=project,
        earning_line_ids=payload.earning_line_ids,
        provider=payload.provider,
        idempotency_key=idempotency_key,
    )
    db.commit()
    return {
        "id": batch.id,
        "currency": batch.currency,
        "total_minor": batch.total_minor,
        "status": batch.status,
    }


@router.get("/payout-batches/{batch_id}")
def batch_detail(
    batch_id: int,
    _actor: User = Depends(require_permission("ledger.read")),
    db: Session = Depends(get_db),
) -> dict:
    return payouts.batch_detail(db, _batch(db, batch_id))


@router.post("/payout-batches/{batch_id}/approve")
def approve_batch(
    batch_id: int,
    actor: User = Depends(require_permission("payout.request")),
    db: Session = Depends(get_db),
) -> dict:
    batch = payouts.approve_batch(db, actor, _batch(db, batch_id))
    db.commit()
    return {"id": batch.id, "status": batch.status, "approved_by": batch.approved_by}


@router.post("/payout-batches/{batch_id}/pay")
def pay_batch(
    batch_id: int,
    actor: User = Depends(require_permission("payout.request")),
    db: Session = Depends(get_db),
) -> dict:
    batch = payouts.pay_batch(db, actor, _batch(db, batch_id))
    db.commit()
    return {"id": batch.id, "status": batch.status, "paid_at": batch.paid_at}


@router.post("/payout-batches/{batch_id}/cancel")
def cancel_batch(
    batch_id: int,
    payload: CancelIn,
    actor: User = Depends(require_permission("payout.request")),
    db: Session = Depends(get_db),
) -> dict:
    batch = payouts.cancel_batch(db, actor, _batch(db, batch_id), reason=payload.reason)
    db.commit()
    return {"id": batch.id, "status": batch.status}


@router.post("/payout-items/{item_id}/fail")
def fail_item(
    item_id: int,
    payload: FailIn,
    actor: User = Depends(require_permission("payout.request")),
    db: Session = Depends(get_db),
) -> dict:
    item = payouts.fail_item(db, actor, item_id, reason=payload.reason)
    db.commit()
    return {"id": item.id, "status": item.status, "failure_reason": item.failure_reason}


@router.get("/payout-batches/{batch_id}/export")
def export_batch(
    batch_id: int,
    _actor: User = Depends(require_permission("ledger.read")),
    db: Session = Depends(get_db),
) -> Response:
    """A payout file ops can hand to a bank or the manual rail."""
    body = payouts.export_csv(db, _batch(db, batch_id))
    return Response(
        content=body,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="payout-batch-{batch_id}.csv"'},
    )


__all__ = ["router"]
