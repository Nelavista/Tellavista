"""Add unique constraint on lessons(module_id, slug)

create_lesson() (routes/admin_skills_routes.py) checks for an existing lesson with the
same slug before inserting, but that check-then-act has no isolation of its own -- two
near-simultaneous create_lesson calls for the same module (a double-click, or the
curriculum-generation loop racing a manual add) can both pass the check before either
commits. Every sibling content model already has this at the DB level (SkillCourse's
uq_skill_course_slug, Challenge's uq_challenge_slug, ProjectTemplate's
uq_project_template_slug) -- Lesson was the one left without it.

IMPORTANT -- read before running against production: if any (module_id, slug) pair
already has more than one row, `upgrade()` below will fail with a unique-violation error
rather than silently deleting/merging anything. Run this diagnostic query against the
production database FIRST (also run by scripts/phase0_audit.py, check #3):

    SELECT module_id, slug, COUNT(*), array_agg(id ORDER BY id)
    FROM lessons
    GROUP BY module_id, slug
    HAVING COUNT(*) > 1;

If it returns zero rows, this migration is safe to run as-is. Confirmed clean against
production on 2026-09-05 (Phase 0 of the Skills implementation plan) -- re-run the query
above before applying if any time has passed since, since new lessons may have been
created in the meantime.

Revision ID: e6b4c8f21a07
Revises: d3f8a52b1c9e
Create Date: 2026-09-05 00:00:00.000000

"""
from alembic import op

revision = 'e6b4c8f21a07'
down_revision = 'd3f8a52b1c9e'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('lessons', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_lesson_module_slug', ['module_id', 'slug'])


def downgrade():
    with op.batch_alter_table('lessons', schema=None) as batch_op:
        batch_op.drop_constraint('uq_lesson_module_slug', type_='unique')
