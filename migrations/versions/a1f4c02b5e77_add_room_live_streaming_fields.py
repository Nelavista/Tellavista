"""Add live-streaming fields to Room

Revision ID: a1f4c02b5e77
Revises: 9893c38d608c
Create Date: 2026-07-31

The live meeting feature is being rebuilt around teachers going live on YouTube (so the
stream itself scales to hundreds/thousands of viewers via YouTube's own CDN, rather than
this app trying to fan out video to everyone itself). Room needs to track which YouTube
video a session is tied to and its live/ended timestamps so a 10-hour session survives a
worker restart instead of living only in the in-memory rooms dict.
"""
from alembic import op
import sqlalchemy as sa


revision = 'a1f4c02b5e77'
down_revision = '9893c38d608c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('room', sa.Column('youtube_video_id', sa.String(length=32), nullable=True))
    op.add_column('room', sa.Column('is_live', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('room', sa.Column('started_at', sa.DateTime(), nullable=True))
    op.add_column('room', sa.Column('ended_at', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('room', 'ended_at')
    op.drop_column('room', 'started_at')
    op.drop_column('room', 'is_live')
    op.drop_column('room', 'youtube_video_id')
