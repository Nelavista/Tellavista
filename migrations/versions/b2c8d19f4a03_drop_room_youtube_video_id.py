"""Drop Room.youtube_video_id

Revision ID: b2c8d19f4a03
Revises: a1f4c02b5e77
Create Date: 2026-08-01

The live meeting feature briefly routed video through a teacher-pasted YouTube Live link.
That's been replaced with in-app broadcasting via Agora (teacher clicks Go Live, camera
streams directly through Nelavista, no external site involved) — the Agora channel is just
the room id itself, so there's no separate video id left to persist.
"""
from alembic import op
import sqlalchemy as sa


revision = 'b2c8d19f4a03'
down_revision = 'a1f4c02b5e77'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('room', 'youtube_video_id')


def downgrade():
    op.add_column('room', sa.Column('youtube_video_id', sa.String(length=32), nullable=True))
