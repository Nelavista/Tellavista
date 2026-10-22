"""platform settings: currency, payout guardrails, ages and curriculum ownership

Revision ID: 20261020_1000
Revises: 20261018_0900
Create Date: 2026-10-20

G1–G5. One row (id = 1) holds the decisions that are policy rather than code:
the billing/payout currency, the second-approver threshold, the minimum working
age, the contributor terms in force and the curriculum owner.

The row is created on first read by the service, with the same defaults as the
server defaults below, so this migration does not need to guess at timestamps.
No existing table changes, so the upgrade is safe with traffic running.
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20261020_1000"
down_revision: str | None = "20261018_0900"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

JSONPayload = sa.JSON().with_variant(JSONB, "postgresql")

ALLOWED_CURRENCIES = '["NGN", "USD", "GBP", "EUR", "GHS", "KES", "ZAR"]'
CONTRIBUTOR_TERMS = "\n\n".join(
    (
        "Contributing work to Nelavista means the following.",
        "1. You do the work yourself. Subcontracting or reselling an assignment is "
        "not allowed, and a submission must be your own output.",
        "2. You may use the material you are given only for the assigned work. Do not "
        "share client data, task instructions or gold answers with anyone else.",
        "3. You keep ownership of the underlying skills you bring; you grant Nelavista "
        "a licence to deliver, review and improve the work you submit.",
        "4. Payment is per approved task at the rate shown on the assignment. A "
        "rejected or reworked task is reviewed again under the published quality "
        "standard.",
        "5. You can stop at any time. Work already approved is still paid.",
        "6. If you are under the guardian-consent age, a parent or guardian must agree "
        "before you accept paid work.",
    )
)


def upgrade() -> None:
    op.create_table(
        "platform_settings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "billing_currency", sa.String(length=3), nullable=False, server_default="NGN"
        ),
        sa.Column(
            "payout_currency", sa.String(length=3), nullable=False, server_default="NGN"
        ),
        sa.Column(
            "allowed_currencies", JSONPayload, nullable=False, server_default=ALLOWED_CURRENCIES
        ),
        sa.Column(
            "payout_second_approver_threshold_minor",
            sa.Integer(),
            nullable=False,
            server_default="5000000",
        ),
        sa.Column(
            "payout_second_approver_always",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column(
            "payout_require_verified_email",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.Column("min_student_age", sa.Integer(), nullable=False, server_default="16"),
        sa.Column(
            "guardian_consent_below_age", sa.Integer(), nullable=False, server_default="18"
        ),
        sa.Column(
            "terms_version", sa.String(length=20), nullable=False, server_default="2026-10-01"
        ),
        sa.Column(
            "contributor_terms_version",
            sa.String(length=20),
            nullable=False,
            server_default="2026-10-01",
        ),
        sa.Column(
            "contributor_terms_body", sa.Text(), nullable=False, server_default=CONTRIBUTOR_TERMS
        ),
        sa.Column(
            "curriculum_owner", sa.String(length=160), nullable=False, server_default="Nelavista"
        ),
        sa.Column(
            "curriculum_license",
            sa.String(length=80),
            nullable=False,
            server_default="Nelavista Contributor Licence 1.0",
        ),
        sa.Column(
            "curriculum_authoring_model",
            sa.String(length=40),
            nullable=False,
            server_default="in_house",
        ),
        sa.Column("target_launch_date", sa.Date(), nullable=True),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(["updated_by"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("platform_settings")
