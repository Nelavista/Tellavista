"""Money contracts (B10, C6).

Amounts are integers in minor units with a currency code — the models make it
impossible to describe a balance as a float. Every earning line carries the rate
and task count that produced it, because "where did this number come from?" is
the only question an earnings screen has to answer.
"""
from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel


class CurrencyTotalOut(BaseModel):
    currency: str
    amount_minor: int


class EarningProjectOut(BaseModel):
    slug: str
    title: str


class EarningLineOut(BaseModel):
    id: int
    project: EarningProjectOut
    submission_id: int | None = None
    amount_minor: int
    currency: str
    rate_minor: int | None = None
    task_count: int | None = None
    status: str
    description: str | None = None
    paid: bool


class EarningsOut(BaseModel):
    totals: list[CurrencyTotalOut]
    lines: list[EarningLineOut]


class SplitOut(BaseModel):
    total_minor: int
    student_pool_minor: int
    platform_fee_minor: int
    platform_retained_minor: int
    department_share_minor: int


class DepartmentShareOut(BaseModel):
    department_id: int | None = None
    amount_minor: int
    currency: str
    status: str


class FinancialsOut(BaseModel):
    project_id: int
    currency: str | None = None
    funding: SplitOut | None = None
    student_pool_minor: int
    earnings_by_status: dict[str, int]
    earning_total_minor: int
    department_share: DepartmentShareOut | None = None
    work_status: str | None = None
    quality_status: str | None = None
    payment_status: str


class FundOut(BaseModel):
    transaction_id: int
    currency: str
    total_minor: int
    student_pool_minor: int
    platform_fee_minor: int
    department_share_minor: int


class ReverseOut(BaseModel):
    id: int
    kind: str
    reverses_transaction_id: int | None = None
    total_minor: int


class LedgerEntryOut(BaseModel):
    id: int
    account: str
    direction: str
    amount_minor: int
    currency: str
    user_id: int | None = None
    department_id: int | None = None
    description: str | None = None


class LedgerTransactionOut(BaseModel):
    id: int
    kind: str
    currency: str
    total_minor: int
    description: str | None = None
    reverses_transaction_id: int | None = None
    created_at: datetime
    entries: list[LedgerEntryOut]


class LedgerOut(BaseModel):
    project_id: int
    transactions: list[LedgerTransactionOut]


class ReconcileReportOut(BaseModel):
    project_id: int
    funded: bool
    balanced: bool
    expected: dict[str, Any]
    actual: dict[str, Any]
    details: list[dict[str, Any]]


class ReconcileRunOut(BaseModel):
    id: int
    as_of: date
    balanced: bool
    project_id: int | None = None


class PayoutBatchOut(BaseModel):
    id: int
    currency: str
    total_minor: int
    status: str
    provider: str | None = None
    paid_at: datetime | None = None


class PayoutBatchListOut(BaseModel):
    batches: list[PayoutBatchOut]


class PayoutItemOut(BaseModel):
    id: int
    user_id: int
    name: str | None = None
    email: str
    amount_minor: int
    status: str
    provider_reference: str | None = None


class PayoutBatchDetailOut(BaseModel):
    id: int
    project_id: int
    currency: str
    total_minor: int
    status: str
    provider: str
    created_by: int | None = None
    approved_by: int | None = None
    approved_at: datetime | None = None
    paid_at: datetime | None = None
    failure_reason: str | None = None
    items: list[PayoutItemOut]


class BatchStateOut(BaseModel):
    id: int
    status: str
    currency: str | None = None
    total_minor: int | None = None
    approved_by: int | None = None
    paid_at: datetime | None = None


class PayoutItemStateOut(BaseModel):
    id: int
    status: str
    failure_reason: str | None = None


__all__ = [
    "BatchStateOut",
    "CurrencyTotalOut",
    "DepartmentShareOut",
    "EarningLineOut",
    "EarningProjectOut",
    "EarningsOut",
    "FinancialsOut",
    "FundOut",
    "LedgerEntryOut",
    "LedgerOut",
    "LedgerTransactionOut",
    "PayoutBatchDetailOut",
    "PayoutBatchListOut",
    "PayoutBatchOut",
    "PayoutItemOut",
    "PayoutItemStateOut",
    "ReconcileReportOut",
    "ReconcileRunOut",
    "ReverseOut",
    "SplitOut",
]
