"""ledger: balanced append-only money, earnings, payouts, reconciliation

Revision ID: 20261017_1000
Revises: 20261017_0900
Create Date: 2026-10-17

Phase 6. Nine new tables.

Every amount is an integer in minor units; no Numeric/Float column exists on
purpose (ADR-0008). `ledger_transactions.idempotency_key` is unique, so a retried
posting returns the original transaction instead of moving money twice.

`payout_items.earning_line_id` is not a foreign key: the link is many earnings to
one item, recorded on `earning_lines.payout_item_id`. Keeping the columns in one
direction avoids a circular FK while leaving the query simple.
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20261017_1000"
down_revision: str | None = "20261017_0900"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

JSONPayload = sa.JSON().with_variant(JSONB, "postgresql")


def _timestamps() -> tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )


def upgrade() -> None:
    op.create_table(
        "ledger_transactions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("kind", sa.String(length=20), nullable=False),
        sa.Column(
            "project_id",
            sa.Integer(),
            sa.ForeignKey("projects.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("total_minor", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("idempotency_key", sa.String(length=80), nullable=False, unique=True),
        sa.Column(
            "reverses_transaction_id",
            sa.Integer(),
            sa.ForeignKey("ledger_transactions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "actor_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_ledger_transactions_kind", "ledger_transactions", ["kind"])
    op.create_index("ix_ledger_transactions_project_id", "ledger_transactions", ["project_id"])
    op.create_index("ix_ledger_transactions_created_at", "ledger_transactions", ["created_at"])

    op.create_table(
        "ledger_entries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "transaction_id",
            sa.Integer(),
            sa.ForeignKey("ledger_transactions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("account", sa.String(length=32), nullable=False),
        sa.Column("direction", sa.String(length=6), nullable=False),
        sa.Column("amount_minor", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column(
            "project_id",
            sa.Integer(),
            sa.ForeignKey("projects.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True
        ),
        sa.Column(
            "department_id",
            sa.Integer(),
            sa.ForeignKey("departments.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_ledger_entries_transaction_id", "ledger_entries", ["transaction_id"])
    op.create_index("ix_ledger_entries_account", "ledger_entries", ["account"])
    op.create_index("ix_ledger_entries_project_id", "ledger_entries", ["project_id"])
    op.create_index("ix_ledger_entries_user_id", "ledger_entries", ["user_id"])
    op.create_index("ix_ledger_entries_department_id", "ledger_entries", ["department_id"])
    op.create_index("ix_ledger_entries_created_at", "ledger_entries", ["created_at"])

    op.create_table(
        "earning_lines",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column(
            "project_id",
            sa.Integer(),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "submission_id",
            sa.Integer(),
            sa.ForeignKey("submissions.id", ondelete="SET NULL"),
            nullable=True,
            unique=True,
        ),
        sa.Column("amount_minor", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("rate_minor", sa.Integer(), nullable=True),
        sa.Column("task_count", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending_quality"),
        sa.Column(
            "ledger_transaction_id",
            sa.Integer(),
            sa.ForeignKey("ledger_transactions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("payout_item_id", sa.Integer(), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
        *_timestamps(),
    )
    op.create_index("ix_earning_lines_user_id", "earning_lines", ["user_id"])
    op.create_index("ix_earning_lines_project_id", "earning_lines", ["project_id"])
    op.create_index("ix_earning_lines_status", "earning_lines", ["status"])
    op.create_index("ix_earning_lines_payout_item_id", "earning_lines", ["payout_item_id"])

    op.create_table(
        "department_shares",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "project_id",
            sa.Integer(),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "department_id",
            sa.Integer(),
            sa.ForeignKey("departments.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("amount_minor", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="approved"),
        sa.Column(
            "ledger_transaction_id",
            sa.Integer(),
            sa.ForeignKey("ledger_transactions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        *_timestamps(),
        sa.UniqueConstraint("project_id", "department_id", name="uq_department_share_project_dept"),
    )
    op.create_index("ix_department_shares_project_id", "department_shares", ["project_id"])
    op.create_index("ix_department_shares_department_id", "department_shares", ["department_id"])

    op.create_table(
        "payout_batches",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "project_id",
            sa.Integer(),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("total_minor", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="draft"),
        sa.Column("provider", sa.String(length=30), nullable=False, server_default="manual"),
        sa.Column("provider_reference", sa.String(length=120), nullable=True),
        sa.Column("idempotency_key", sa.String(length=80), nullable=True, unique=True),
        sa.Column(
            "created_by", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True
        ),
        sa.Column(
            "approved_by", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True
        ),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("failure_reason", sa.String(length=255), nullable=True),
        *_timestamps(),
    )
    op.create_index("ix_payout_batches_project_id", "payout_batches", ["project_id"])

    op.create_table(
        "payout_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "batch_id",
            sa.Integer(),
            sa.ForeignKey("payout_batches.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("amount_minor", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="approved"),
        sa.Column("provider_reference", sa.String(length=120), nullable=True),
        sa.Column(
            "ledger_transaction_id",
            sa.Integer(),
            sa.ForeignKey("ledger_transactions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("failure_reason", sa.String(length=255), nullable=True),
        *_timestamps(),
        sa.UniqueConstraint("batch_id", "user_id", name="uq_payout_item_batch_user"),
    )
    op.create_index("ix_payout_items_batch_id", "payout_items", ["batch_id"])
    op.create_index("ix_payout_items_user_id", "payout_items", ["user_id"])

    op.create_table(
        "exchange_rate_snapshots",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("base_currency", sa.String(length=3), nullable=False),
        sa.Column("quote_currency", sa.String(length=3), nullable=False),
        sa.Column("rate_micros", sa.Integer(), nullable=False),
        sa.Column("source", sa.String(length=80), nullable=False),
        sa.Column(
            "captured_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        *_timestamps(),
    )
    op.create_index(
        "ix_exchange_rate_snapshots_captured_at", "exchange_rate_snapshots", ["captured_at"]
    )

    op.create_table(
        "reconciliation_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "project_id",
            sa.Integer(),
            sa.ForeignKey("projects.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("as_of", sa.Date(), nullable=False),
        sa.Column("balanced", sa.Boolean(), nullable=False),
        sa.Column("expected", JSONPayload, nullable=True),
        sa.Column("actual", JSONPayload, nullable=True),
        sa.Column("details", JSONPayload, nullable=True),
        sa.Column(
            "created_by", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_reconciliation_runs_project_id", "reconciliation_runs", ["project_id"])
    op.create_index("ix_reconciliation_runs_created_at", "reconciliation_runs", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_reconciliation_runs_created_at", table_name="reconciliation_runs")
    op.drop_index("ix_reconciliation_runs_project_id", table_name="reconciliation_runs")
    op.drop_table("reconciliation_runs")

    op.drop_index("ix_exchange_rate_snapshots_captured_at", table_name="exchange_rate_snapshots")
    op.drop_table("exchange_rate_snapshots")

    op.drop_index("ix_payout_items_user_id", table_name="payout_items")
    op.drop_index("ix_payout_items_batch_id", table_name="payout_items")
    op.drop_table("payout_items")

    op.drop_index("ix_payout_batches_project_id", table_name="payout_batches")
    op.drop_table("payout_batches")

    op.drop_index("ix_department_shares_department_id", table_name="department_shares")
    op.drop_index("ix_department_shares_project_id", table_name="department_shares")
    op.drop_table("department_shares")

    op.drop_index("ix_earning_lines_payout_item_id", table_name="earning_lines")
    op.drop_index("ix_earning_lines_status", table_name="earning_lines")
    op.drop_index("ix_earning_lines_project_id", table_name="earning_lines")
    op.drop_index("ix_earning_lines_user_id", table_name="earning_lines")
    op.drop_table("earning_lines")

    op.drop_index("ix_ledger_entries_created_at", table_name="ledger_entries")
    op.drop_index("ix_ledger_entries_department_id", table_name="ledger_entries")
    op.drop_index("ix_ledger_entries_user_id", table_name="ledger_entries")
    op.drop_index("ix_ledger_entries_project_id", table_name="ledger_entries")
    op.drop_index("ix_ledger_entries_account", table_name="ledger_entries")
    op.drop_index("ix_ledger_entries_transaction_id", table_name="ledger_entries")
    op.drop_table("ledger_entries")

    op.drop_index("ix_ledger_transactions_created_at", table_name="ledger_transactions")
    op.drop_index("ix_ledger_transactions_project_id", table_name="ledger_transactions")
    op.drop_index("ix_ledger_transactions_kind", table_name="ledger_transactions")
    op.drop_table("ledger_transactions")
