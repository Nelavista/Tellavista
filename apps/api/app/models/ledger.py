"""Money: an append-only ledger with exact integer arithmetic (ADR-0008, PRD §9).

The rules this module makes structural:

* **No floating point.** Every amount is an integer in minor units plus an ISO
  currency code. A test asserts no float column exists anywhere in the module.
* **Append-only.** `LedgerTransaction` and `LedgerEntry` have no `updated_at` and
  are never edited. A correction is a new transaction that reverses the old one.
* **Balanced.** Every transaction's debits equal its credits; the service refuses
  to post one that does not, and reconciliation re-checks it from the rows.
* **Idempotent.** A transaction carries a unique `idempotency_key`, so a retried
  payout cannot pay twice.

`EarningLine` is the student-facing explanation of money: one line per approved
piece of work, showing tasks, rate and amount. Its status is the payment state
machine (quality → approved → payable → paid, with failed/reversed branches) and
it is deliberately *not* part of the ledger: it explains what is owed, the ledger
records what moved.
"""
from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin
from app.models.admin import JSONPayload

# Ledger accounts. A transaction moves value between them; the sum of all
# entries in one transaction is always zero.
ACCOUNT_ESCROW = "project_escrow"
ACCOUNT_STUDENT_PAYABLE = "student_payable"
ACCOUNT_PLATFORM_REVENUE = "platform_revenue"
ACCOUNT_DEPARTMENT_PAYABLE = "department_payable"
ACCOUNT_PAYOUT_CLEARING = "payout_clearing"
ACCOUNTS: tuple[str, ...] = (
    ACCOUNT_ESCROW,
    ACCOUNT_STUDENT_PAYABLE,
    ACCOUNT_PLATFORM_REVENUE,
    ACCOUNT_DEPARTMENT_PAYABLE,
    ACCOUNT_PAYOUT_CLEARING,
)

DEBIT = "debit"
CREDIT = "credit"
DIRECTIONS: tuple[str, ...] = (DEBIT, CREDIT)

TX_FUNDING = "project_funding"
TX_PAYOUT = "payout"
TX_REVERSAL = "reversal"
TX_ADJUSTMENT = "adjustment"
TX_KINDS: tuple[str, ...] = (TX_FUNDING, TX_PAYOUT, TX_REVERSAL, TX_ADJUSTMENT)

# Earning / payout states. Work is only ever payable after approval.
EARNING_PENDING_QUALITY = "pending_quality"
EARNING_APPROVED = "approved"
EARNING_PAYABLE = "payable"
EARNING_PAID = "paid"
EARNING_FAILED = "failed"
EARNING_REVERSED = "reversed"
EARNING_STATUSES: tuple[str, ...] = (
    EARNING_PENDING_QUALITY,
    EARNING_APPROVED,
    EARNING_PAYABLE,
    EARNING_PAID,
    EARNING_FAILED,
    EARNING_REVERSED,
)

BATCH_DRAFT = "draft"
BATCH_PENDING_APPROVAL = "pending_approval"
BATCH_APPROVED = "approved"
BATCH_PAID = "paid"
BATCH_FAILED = "failed"
BATCH_CANCELLED = "cancelled"
BATCH_STATUSES: tuple[str, ...] = (
    BATCH_DRAFT,
    BATCH_PENDING_APPROVAL,
    BATCH_APPROVED,
    BATCH_PAID,
    BATCH_FAILED,
    BATCH_CANCELLED,
)

# Above this amount (minor units) a payout batch needs a second approver.
SECOND_APPROVER_THRESHOLD_MINOR = 10_000_000  # 100,000.00 in a two-decimal currency


class LedgerTransaction(Base):
    """A balanced group of entries. Append-only: no updated_at, never edited."""

    __tablename__ = "ledger_transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    kind: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id", ondelete="SET NULL"), index=True
    )
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    total_minor: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    # Unique: a retried posting returns the original transaction, never a second one.
    idempotency_key: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    reverses_transaction_id: Mapped[int | None] = mapped_column(
        ForeignKey("ledger_transactions.id", ondelete="SET NULL")
    )
    actor_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )


class LedgerEntry(Base):
    """One side of one transaction. Signed by `direction`; amounts stay positive."""

    __tablename__ = "ledger_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    transaction_id: Mapped[int] = mapped_column(
        ForeignKey("ledger_transactions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    account: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    direction: Mapped[str] = mapped_column(String(6), nullable=False)
    amount_minor: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id", ondelete="SET NULL"), index=True
    )
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    department_id: Mapped[int | None] = mapped_column(
        ForeignKey("departments.id", ondelete="SET NULL"), index=True
    )
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )


class EarningLine(Base, TimestampMixin):
    """What one student earned for one approved submission, and why."""

    __tablename__ = "earning_lines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    submission_id: Mapped[int | None] = mapped_column(
        ForeignKey("submissions.id", ondelete="SET NULL"), unique=True
    )
    amount_minor: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    # The per-task rate used, so the line can be explained: amount = tasks * rate.
    rate_minor: Mapped[int | None] = mapped_column(Integer)
    task_count: Mapped[int] = mapped_column(
        Integer, default=1, server_default="1", nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(20), default=EARNING_PENDING_QUALITY,
        server_default=EARNING_PENDING_QUALITY, nullable=False, index=True,
    )
    ledger_transaction_id: Mapped[int | None] = mapped_column(
        ForeignKey("ledger_transactions.id", ondelete="SET NULL")
    )
    payout_item_id: Mapped[int | None] = mapped_column(Integer, index=True)
    description: Mapped[str | None] = mapped_column(String(255))


class DepartmentShare(Base, TimestampMixin):
    """The participating department's 2%, always taken from the fee, never the 90%."""

    __tablename__ = "department_shares"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    department_id: Mapped[int | None] = mapped_column(
        ForeignKey("departments.id", ondelete="SET NULL"), index=True
    )
    amount_minor: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), default=EARNING_APPROVED, server_default=EARNING_APPROVED, nullable=False
    )
    ledger_transaction_id: Mapped[int | None] = mapped_column(
        ForeignKey("ledger_transactions.id", ondelete="SET NULL")
    )

    __table_args__ = (
        UniqueConstraint("project_id", "department_id", name="uq_department_share_project_dept"),
    )


class PayoutBatch(Base, TimestampMixin):
    """A set of student payments released together.

    `approved_by` must differ from `created_by` above
    `SECOND_APPROVER_THRESHOLD_MINOR`; the service enforces it and the audit log
    records both actors.
    """

    __tablename__ = "payout_batches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    total_minor: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), default=BATCH_DRAFT, server_default=BATCH_DRAFT, nullable=False
    )
    provider: Mapped[str] = mapped_column(
        String(30), default="manual", server_default="manual", nullable=False
    )
    provider_reference: Mapped[str | None] = mapped_column(String(120))
    idempotency_key: Mapped[str | None] = mapped_column(String(80), unique=True)
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    approved_by: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    failure_reason: Mapped[str | None] = mapped_column(String(255))


class PayoutItem(Base, TimestampMixin):
    """One student's payment inside a batch."""

    __tablename__ = "payout_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    batch_id: Mapped[int] = mapped_column(
        ForeignKey("payout_batches.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    amount_minor: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), default=EARNING_APPROVED, server_default=EARNING_APPROVED, nullable=False
    )
    provider_reference: Mapped[str | None] = mapped_column(String(120))
    ledger_transaction_id: Mapped[int | None] = mapped_column(
        ForeignKey("ledger_transactions.id", ondelete="SET NULL")
    )
    failure_reason: Mapped[str | None] = mapped_column(String(255))

    __table_args__ = (
        UniqueConstraint("batch_id", "user_id", name="uq_payout_item_batch_user"),
    )


class ExchangeRateSnapshot(Base, TimestampMixin):
    """A rate captured at a point in time. Stored, never inferred later."""

    __tablename__ = "exchange_rate_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_currency: Mapped[str] = mapped_column(String(3), nullable=False)
    quote_currency: Mapped[str] = mapped_column(String(3), nullable=False)
    # Rate scaled by 1_000_000: 1 base = rate_micros / 1e6 quote. Integer, no float.
    rate_micros: Mapped[int] = mapped_column(Integer, nullable=False)
    source: Mapped[str] = mapped_column(String(80), nullable=False)
    captured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )


class ReconciliationRun(Base):
    """Result of checking that a project's ledger and earnings agree."""

    __tablename__ = "reconciliation_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id", ondelete="SET NULL"), index=True
    )
    as_of: Mapped[date] = mapped_column(Date, nullable=False)
    balanced: Mapped[bool] = mapped_column(nullable=False)
    expected: Mapped[dict | None] = mapped_column(JSONPayload)
    actual: Mapped[dict | None] = mapped_column(JSONPayload)
    details: Mapped[list | None] = mapped_column(JSONPayload)
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
