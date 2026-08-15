"""Add career_tracks + career_track_steps — multi-skill career paths.

Revision ID: c9e5a2b7d3f8
Revises: b8d4f1a6c2e7
Create Date: 2026-08-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'c9e5a2b7d3f8'
down_revision = 'b8d4f1a6c2e7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'career_tracks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('slug', sa.String(length=150), nullable=False),
        sa.Column('tagline', sa.String(length=200)),
        sa.Column('description', sa.Text()),
        sa.Column('icon', sa.String(length=10)),
        sa.Column('color', sa.String(length=20), server_default='#3b82f6'),
        sa.Column('is_published', sa.Boolean(), server_default=sa.false()),
        sa.Column('order', sa.Integer(), server_default='0'),
        sa.Column('created_at', sa.DateTime()),
        sa.UniqueConstraint('slug', name='uq_career_track_slug'),
    )
    op.create_table(
        'career_track_steps',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('track_id', sa.Integer(), sa.ForeignKey('career_tracks.id'), nullable=False),
        sa.Column('skill_id', sa.Integer(), sa.ForeignKey('skills.id'), nullable=False),
        sa.Column('order', sa.Integer(), server_default='0'),
        sa.Column('note', sa.String(length=200)),
    )


def downgrade():
    op.drop_table('career_track_steps')
    op.drop_table('career_tracks')
