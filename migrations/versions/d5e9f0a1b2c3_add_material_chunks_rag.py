"""Add material_chunks -- vector storage for the PRD §5.5 RAG pipeline.

On Postgres (the deploy target) the embedding column is a native pgvector
`vector(1536)` and the extension is enabled here (CREATE EXTENSION IF NOT EXISTS
vector -- pgvector is available on all Render Postgres 13+ instances; see the
migration map's Step 2). On SQLite (the test suite) embedding is plain VARBINARY and
similarity is computed in Python -- the service layer owns that dialect split, so
this migration only needs the column to exist with matching name on both.

The table is deliberately standalone (material_id FK, denormalized course_code and
topic_id) so retrieval never has to join Materials to scope rows, and chunk metadata
carries material/page for future citation surfacing (PRD §5.5's design note).

Revision ID: d5e9f0a1b2c3
Revises: c4d8e2f1a7b3
Create Date: 2026-09-27 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'd5e9f0a1b2c3'
down_revision = 'c4d8e2f1a7b3'
branch_labels = None
depends_on = None


def upgrade():
    # Inline pgvector usage requires the extension; IF NOT EXISTS keeps re-runs and
    # SQLite (where this is simply skipped by the dialect check below) harmless.
    bind = op.get_bind()
    is_postgres = bind.dialect.name == 'postgresql'
    if is_postgres:
        bind.execute(sa.text('CREATE EXTENSION IF NOT EXISTS vector'))

    op.create_table(
        'material_chunks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('material_id', sa.Integer(), sa.ForeignKey('materials.id'), nullable=False),
        sa.Column('chunk_index', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('page_number', sa.Integer(), nullable=True),
        sa.Column('course_code', sa.String(length=20), nullable=True),
        sa.Column('topic_id', sa.Integer(), sa.ForeignKey('topics.id'), nullable=True),
        sa.Column('embedding_model', sa.String(length=120), nullable=True),
        # pgvector's vector type isn't a standard SQLAlchemy type; on Postgres the
        # column is altered to VECTOR(1536) right after creation, on SQLite it stays
        # binary (the service layer packs/unpacks floats identically either way).
        sa.Column('embedding', sa.LargeBinary(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_material_chunks_material_id', 'material_chunks', ['material_id'])
    op.create_index('ix_material_chunks_course_code', 'material_chunks', ['course_code'])
    op.create_index('ix_material_chunks_topic_id', 'material_chunks', ['topic_id'])

    if is_postgres:
        bind.execute(sa.text('ALTER TABLE material_chunks ALTER COLUMN embedding TYPE vector(1536) USING NULL'))


def downgrade():
    op.drop_index('ix_material_chunks_topic_id', table_name='material_chunks')
    op.drop_index('ix_material_chunks_course_code', table_name='material_chunks')
    op.drop_index('ix_material_chunks_material_id', table_name='material_chunks')
    op.drop_table('material_chunks')
