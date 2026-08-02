"""Add GroupMessage.file_id

Revision ID: c3e9f21a6b58
Revises: b2c8d19f4a03
Create Date: 2026-08-01

Community file sharing needs a real link between a 'file' message and the GroupFile row it
represents. Without this column, the only way to find a message's file was matching on
"whichever GroupFile was uploaded right before this message's timestamp" — fragile and wrong
under any concurrent uploads.
"""
from alembic import op
import sqlalchemy as sa


revision = 'c3e9f21a6b58'
down_revision = 'b2c8d19f4a03'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('group_messages', sa.Column('file_id', sa.Integer(), nullable=True))
    with op.batch_alter_table('group_messages') as batch_op:
        batch_op.create_foreign_key('fk_group_messages_file_id', 'group_files', ['file_id'], ['id'])


def downgrade():
    with op.batch_alter_table('group_messages') as batch_op:
        batch_op.drop_constraint('fk_group_messages_file_id', type_='foreignkey')
    op.drop_column('group_messages', 'file_id')
