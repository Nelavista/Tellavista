"""Add trust/security columns and tables from the Level 1 production-readiness pass:
email verification (user), CBT attempt question-issuance tracking (cbt_attempts),
opportunity payment audit trail + dispute/refund states (opportunity_applications,
opportunity_status_events), and admin privilege-change audit log (admin_audit_log).

Existing users are backfilled email_verified=True so nobody already using the product
is locked out by a column that didn't exist when they signed up -- only new signups
(see routes/auth_routes.py) start out unverified.

Revision ID: c8e1a2f4b937
Revises: b7f3e9a4c216
Create Date: 2026-08-25 00:00:00.000001

"""
from alembic import op
import sqlalchemy as sa

revision = 'c8e1a2f4b937'
down_revision = 'b7f3e9a4c216'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email_verified', sa.Boolean(), nullable=False, server_default=sa.true()))
        batch_op.add_column(sa.Column('email_verify_token', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('email_verify_token_expiry', sa.DateTime(), nullable=True))

    with op.batch_alter_table('cbt_attempts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('issued_question_ids_json', sa.Text(), nullable=True))

    with op.batch_alter_table('opportunity_applications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('payment_reference', sa.String(length=150), nullable=True))
        batch_op.add_column(sa.Column('paid_by_admin_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('dispute_reason', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('disputed_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('refunded_at', sa.DateTime(), nullable=True))
        batch_op.create_foreign_key(
            'fk_opportunity_applications_paid_by_admin_id', 'user', ['paid_by_admin_id'], ['id']
        )

    op.create_table(
        'opportunity_status_events',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('application_id', sa.Integer(), sa.ForeignKey('opportunity_applications.id'), nullable=False),
        sa.Column('actor_user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=True),
        sa.Column('from_status', sa.String(length=20), nullable=True),
        sa.Column('to_status', sa.String(length=20), nullable=False),
        sa.Column('note', sa.String(length=300), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )
    op.create_index(
        'ix_opportunity_status_events_application_id', 'opportunity_status_events', ['application_id']
    )

    op.create_table(
        'admin_audit_log',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('target_user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('actor_user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=True),
        sa.Column('action', sa.String(length=30), nullable=False),
        sa.Column('source', sa.String(length=30), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )


def downgrade():
    op.drop_table('admin_audit_log')
    op.drop_index('ix_opportunity_status_events_application_id', table_name='opportunity_status_events')
    op.drop_table('opportunity_status_events')

    with op.batch_alter_table('opportunity_applications', schema=None) as batch_op:
        batch_op.drop_constraint('fk_opportunity_applications_paid_by_admin_id', type_='foreignkey')
        batch_op.drop_column('refunded_at')
        batch_op.drop_column('disputed_at')
        batch_op.drop_column('dispute_reason')
        batch_op.drop_column('paid_by_admin_id')
        batch_op.drop_column('payment_reference')

    with op.batch_alter_table('cbt_attempts', schema=None) as batch_op:
        batch_op.drop_column('issued_question_ids_json')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('email_verify_token_expiry')
        batch_op.drop_column('email_verify_token')
        batch_op.drop_column('email_verified')
