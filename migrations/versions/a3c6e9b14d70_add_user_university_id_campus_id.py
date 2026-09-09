"""Add User.university_id/campus_id + backfill from the free-text university column

Multi-university expansion, step 3. `user.university` (free text) is kept as-is -- every
existing template/filter that reads it keeps working unchanged -- but every user now also
gets a proper relational university_id (and campus_id, from that university's main
campus), backfilled here by case-insensitive matching against universities.name, the same
matching rule already used by services/academic_context.py. A user whose university
string doesn't match any known row (typo, blank, or a school not yet added) simply keeps
university_id/campus_id NULL -- an honest "unresolved" state, never a guessed match.

Revision ID: a3c6e9b14d70
Revises: f2b5d8a03c69
Create Date: 2026-09-06 00:00:00.000002

"""
from alembic import op
import sqlalchemy as sa

revision = 'a3c6e9b14d70'
down_revision = 'f2b5d8a03c69'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('university_id', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('campus_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_user_university_id', 'user', 'universities', ['university_id'], ['id'])
    op.create_foreign_key('fk_user_campus_id', 'user', 'campuses', ['campus_id'], ['id'])

    conn = op.get_bind()
    conn.execute(sa.text(
        """
        UPDATE "user" u
        SET university_id = uni.id
        FROM universities uni
        WHERE u.university IS NOT NULL
          AND lower(trim(u.university)) = lower(trim(uni.name))
        """
    ))
    conn.execute(sa.text(
        """
        UPDATE "user" u
        SET campus_id = c.id
        FROM campuses c
        WHERE u.university_id = c.university_id
          AND c.is_main = true
          AND u.campus_id IS NULL
        """
    ))


def downgrade():
    op.drop_constraint('fk_user_campus_id', 'user', type_='foreignkey')
    op.drop_constraint('fk_user_university_id', 'user', type_='foreignkey')
    op.drop_column('user', 'campus_id')
    op.drop_column('user', 'university_id')
