"""Add unique constraint on student_projects(student_id, project_template_id)

start_project() (routes/skills_routes.py) checks for an existing row before inserting a
new template-started project, but that check-then-act has no isolation of its own -- two
nearly simultaneous requests (a double-click, a slow-network retry) can both pass the
check before either commits, creating two independent project rows for the same
template and splitting that project's milestones/files/AI feedback across both. This
constraint makes that impossible at the database level; the route itself is updated
separately (not in this migration) to catch the resulting IntegrityError on the losing
request and redirect to the winning row instead of crashing.

project_template_id stays nullable -- custom ('custom') and AI-generated
('ai_generated') projects never set it, and a NULL is never considered equal to another
NULL by a UNIQUE constraint on Postgres or SQLite, so this only ever constrains
template-started projects (source='template'), which is exactly the set start_project()
already intends to be one-per-student.

IMPORTANT -- read before running against production: if any (student_id,
project_template_id) pair already has more than one row (i.e. this bug already fired for
a real student), `upgrade()` below will fail with a unique-violation error rather than
silently deleting/merging anything -- this migration deliberately does not attempt an
automatic cleanup, since picking which duplicate row to keep (they may have different
repo_url/description/AI-feedback content) is a judgment call, not something to automate.
Run this diagnostic query against the production database FIRST:

    SELECT student_id, project_template_id, COUNT(*), array_agg(id ORDER BY id)
    FROM student_projects
    WHERE project_template_id IS NOT NULL
    GROUP BY student_id, project_template_id
    HAVING COUNT(*) > 1;

If it returns zero rows, the migration is safe to run as-is. If it returns any rows,
decide per group which id to keep (e.g. the one with more progress/content) before this
migration can be applied -- ask before deleting anything.

Revision ID: c4a9f2e871b3
Revises: a1c3e7f2b984
Create Date: 2026-08-31 00:00:00.000000

"""
from alembic import op

revision = 'c4a9f2e871b3'
down_revision = 'a1c3e7f2b984'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('student_projects', schema=None) as batch_op:
        batch_op.create_unique_constraint(
            'uq_student_project_student_template', ['student_id', 'project_template_id']
        )


def downgrade():
    with op.batch_alter_table('student_projects', schema=None) as batch_op:
        batch_op.drop_constraint('uq_student_project_student_template', type_='unique')
