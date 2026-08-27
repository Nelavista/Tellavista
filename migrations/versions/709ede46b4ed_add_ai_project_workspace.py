"""Add the AI project workspace: a free-text idea can now generate a full StudentProject
brief, developer/writer/designer projects get a real in-browser workspace instead of just
repo_url/live_url links, and each project gets its own persistent AI mentor chat.

- student_projects.source distinguishes how a project was started (template/custom/
  ai_generated) -- backfilled below from the existing project_template_id link so no
  historical row is left with an inaccurate provenance.
- student_projects.workspace_type (+ the matching project_templates column, for an admin
  to opt a curated template in later) selects developer/writer/designer/NULL. NULL keeps
  today's plain link-based flow unchanged -- every existing row stays NULL.
- The AI-brief columns (idea_text, objectives, features_json, ...) and writer/designer
  workspace payload (doc_content, design_assets_json, ...) live directly on student_projects,
  same convention as the existing screenshots_json/rubric_scores_json columns, since each is
  a small piece of that one project's own state, never queried independently.
- project_files is a new table rather than a JSON blob, because the code editor's
  save/rename/delete calls need a stable id to address one specific file (same reasoning as
  project_milestones already being its own table instead of JSON-on-the-row).
- project_messages is a new table for the per-project AI mentor chat -- deliberately
  separate from the site-wide, stateless "Ask Nelavista" widget, which stays exactly as
  it is; this gives one project a real, persistent, multi-turn conversation.

Revision ID: 709ede46b4ed
Revises: c2a8f4e91d67
Create Date: 2026-08-27 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '709ede46b4ed'
down_revision = 'c2a8f4e91d67'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('project_templates', schema=None) as batch_op:
        batch_op.add_column(sa.Column('workspace_type', sa.String(length=20), nullable=True))

    with op.batch_alter_table('student_projects', schema=None) as batch_op:
        batch_op.add_column(sa.Column('source', sa.String(length=20), nullable=False, server_default='custom'))
        batch_op.add_column(sa.Column('workspace_type', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('idea_text', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('objectives', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('features_json', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('deliverables_json', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('tech_stack_json', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('success_criteria_json', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('difficulty', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('estimated_time', sa.String(length=60), nullable=True))
        batch_op.add_column(sa.Column('doc_content', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('doc_versions_json', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('design_notes', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('design_assets_json', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('reflection_problem_solved', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('reflection_challenges', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('reflection_improvements', sa.Text(), nullable=True))

    # Backfill: every row already tied to a template was started FROM that template, so it's
    # 'template' provenance, not the 'custom' the column's server_default just gave it.
    op.execute("UPDATE student_projects SET source = 'template' WHERE project_template_id IS NOT NULL")

    op.create_table(
        'project_files',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('student_project_id', sa.Integer(), sa.ForeignKey('student_projects.id'), nullable=False),
        sa.Column('filename', sa.String(length=200), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'project_messages',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('student_project_id', sa.Integer(), sa.ForeignKey('student_projects.id'), nullable=False),
        sa.Column('role', sa.String(length=10), nullable=False),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )


def downgrade():
    op.drop_table('project_messages')
    op.drop_table('project_files')

    with op.batch_alter_table('student_projects', schema=None) as batch_op:
        batch_op.drop_column('reflection_improvements')
        batch_op.drop_column('reflection_challenges')
        batch_op.drop_column('reflection_problem_solved')
        batch_op.drop_column('design_assets_json')
        batch_op.drop_column('design_notes')
        batch_op.drop_column('doc_versions_json')
        batch_op.drop_column('doc_content')
        batch_op.drop_column('estimated_time')
        batch_op.drop_column('difficulty')
        batch_op.drop_column('success_criteria_json')
        batch_op.drop_column('tech_stack_json')
        batch_op.drop_column('deliverables_json')
        batch_op.drop_column('features_json')
        batch_op.drop_column('objectives')
        batch_op.drop_column('idea_text')
        batch_op.drop_column('workspace_type')
        batch_op.drop_column('source')

    with op.batch_alter_table('project_templates', schema=None) as batch_op:
        batch_op.drop_column('workspace_type')
