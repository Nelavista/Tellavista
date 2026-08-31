"""Add user_preferences table (real Settings backing store), User.is_deleted/deleted_at
for self-service account deletion, and drop the dead, never-read/written user_profile
table it replaces.

Revision ID: a1c3e7f2b984
Revises: d8e1f4a7c952
Create Date: 2026-08-29 00:00:00.000002

"""
from alembic import op
import sqlalchemy as sa

revision = 'a1c3e7f2b984'
down_revision = 'd8e1f4a7c952'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.false()))
        batch_op.add_column(sa.Column('deleted_at', sa.DateTime(), nullable=True))

    op.create_table(
        'user_preferences',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('theme', sa.String(length=10), nullable=False, server_default='dark'),
        sa.Column('ai_response_style', sa.String(length=20), nullable=False, server_default='balanced'),
        sa.Column('ai_teaching_approach', sa.String(length=20), nullable=False, server_default='step_by_step'),
        sa.Column('ai_difficulty', sa.String(length=20), nullable=False, server_default='university'),
        sa.Column('ai_use_academic_context', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('ai_use_conversation_history', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('ai_personal_context', sa.Text(), nullable=True),
        sa.Column('cbt_default_mode', sa.String(length=10), nullable=False, server_default='cbt'),
        sa.Column('cbt_auto_explain', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('notify_cbt_results', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', name='uq_user_preferences_user_id'),
    )

    op.drop_table('user_profile')


def downgrade():
    op.create_table(
        'user_profile',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=150), nullable=False),
        sa.Column('level', sa.String(length=50), nullable=True),
        sa.Column('department', sa.String(length=100), nullable=True),
        sa.Column('traits', sa.Text(), nullable=True),
        sa.Column('explanation_style', sa.String(length=50), nullable=True),
        sa.Column('focus_areas', sa.Text(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
    )

    op.drop_table('user_preferences')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('deleted_at')
        batch_op.drop_column('is_deleted')
