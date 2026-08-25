"""Add rooms.teacher_user_id -- the real, stable room owner (a User.id, set once via the
/teacher/<room_id> HTTP route) that events.py's Socket.IO join-room handler now checks
before letting any socket claim the 'teacher' role, closing the previously-unauthenticated
live-class teacher takeover.

Revision ID: e2f7c5b830a4
Revises: d4b6f0a2e158
Create Date: 2026-08-25 00:00:00.000003

"""
from alembic import op
import sqlalchemy as sa

revision = 'e2f7c5b830a4'
down_revision = 'd4b6f0a2e158'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('room', schema=None) as batch_op:
        batch_op.add_column(sa.Column('teacher_user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_room_teacher_user_id', 'user', ['teacher_user_id'], ['id'])


def downgrade():
    with op.batch_alter_table('room', schema=None) as batch_op:
        batch_op.drop_constraint('fk_room_teacher_user_id', type_='foreignkey')
        batch_op.drop_column('teacher_user_id')
