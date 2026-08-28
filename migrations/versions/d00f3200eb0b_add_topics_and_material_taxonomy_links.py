"""Add Topic model and Material->Course/Topic/Department taxonomy links

Revision ID: d00f3200eb0b
Revises: 709ede46b4ed
Create Date: 2026-08-27 00:00:00.000000

Adds the `topics` table (one teachable unit per Course -- see models.py's Topic) and
four new nullable columns on `materials` (course_id, topic_id, department_id,
material_type, rejection_reason) that let a Material be linked to the real academic
taxonomy instead of only matched by free-text string equality.

All new FK columns are nullable and this migration does NOT delete or rewrite
Material.course_code/department/course_type -- those stay exactly as they are, so
nothing that already reads them breaks. Backfilling course_id/topic_id/department_id
for pre-existing rows is a separate, explicit, idempotent, dry-run-by-default data
script (backfill_material_taxonomy_links.py) -- schema changes and data backfills are
kept separate on purpose so a schema migration is never also a silent mass UPDATE.
"""
from alembic import op
import sqlalchemy as sa

revision = 'd00f3200eb0b'
down_revision = '709ede46b4ed'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'topics',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('course_id', sa.Integer(), sa.ForeignKey('courses.id'), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('explanation', sa.Text(), nullable=True),
        sa.Column('video_url', sa.String(length=500), nullable=True),
        sa.Column('videos_json', sa.Text(), nullable=True),
        sa.Column('content_source', sa.String(length=20), nullable=True, server_default='ai_draft'),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.true()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_topics_course_id', 'topics', ['course_id'])

    with op.batch_alter_table('materials', schema=None) as batch_op:
        batch_op.add_column(sa.Column('course_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('topic_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('department_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('material_type', sa.String(length=30), nullable=True))
        batch_op.add_column(sa.Column('rejection_reason', sa.String(length=300), nullable=True))
        batch_op.create_foreign_key('fk_materials_course_id', 'courses', ['course_id'], ['id'])
        batch_op.create_foreign_key('fk_materials_topic_id', 'topics', ['topic_id'], ['id'])
        batch_op.create_foreign_key('fk_materials_department_id', 'departments', ['department_id'], ['id'])
        batch_op.create_index('ix_materials_course_id', ['course_id'])
        batch_op.create_index('ix_materials_topic_id', ['topic_id'])
        batch_op.create_index('ix_materials_department_id', ['department_id'])
        batch_op.create_index('ix_materials_material_type', ['material_type'])


def downgrade():
    with op.batch_alter_table('materials', schema=None) as batch_op:
        batch_op.drop_index('ix_materials_material_type')
        batch_op.drop_index('ix_materials_department_id')
        batch_op.drop_index('ix_materials_topic_id')
        batch_op.drop_index('ix_materials_course_id')
        batch_op.drop_constraint('fk_materials_department_id', type_='foreignkey')
        batch_op.drop_constraint('fk_materials_topic_id', type_='foreignkey')
        batch_op.drop_constraint('fk_materials_course_id', type_='foreignkey')
        batch_op.drop_column('rejection_reason')
        batch_op.drop_column('material_type')
        batch_op.drop_column('department_id')
        batch_op.drop_column('topic_id')
        batch_op.drop_column('course_id')

    op.drop_index('ix_topics_course_id', table_name='topics')
    op.drop_table('topics')
