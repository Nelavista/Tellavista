"""Add tutor_conversations / tutor_messages -- threaded AI Tutor chat history, scoped
optionally to a Course/Topic/Material.

Revision ID: d8e1f4a7c952
Revises: c7d1e94a2f83
Create Date: 2026-08-29 00:00:00.000001

"""
from alembic import op
import sqlalchemy as sa

revision = 'd8e1f4a7c952'
down_revision = 'c7d1e94a2f83'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tutor_conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=True),
        sa.Column('course_id', sa.Integer(), nullable=True),
        sa.Column('topic_id', sa.Integer(), nullable=True),
        sa.Column('material_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id']),
        sa.ForeignKeyConstraint(['topic_id'], ['topics.id']),
        sa.ForeignKeyConstraint(['material_id'], ['materials.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    with op.batch_alter_table('tutor_conversations', schema=None) as batch_op:
        batch_op.create_index('ix_tutor_conversations_user_id', ['user_id'], unique=False)

    op.create_table(
        'tutor_messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=10), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['tutor_conversations.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    with op.batch_alter_table('tutor_messages', schema=None) as batch_op:
        batch_op.create_index('ix_tutor_messages_conversation_id', ['conversation_id'], unique=False)


def downgrade():
    with op.batch_alter_table('tutor_messages', schema=None) as batch_op:
        batch_op.drop_index('ix_tutor_messages_conversation_id')
    op.drop_table('tutor_messages')

    with op.batch_alter_table('tutor_conversations', schema=None) as batch_op:
        batch_op.drop_index('ix_tutor_conversations_user_id')
    op.drop_table('tutor_conversations')
