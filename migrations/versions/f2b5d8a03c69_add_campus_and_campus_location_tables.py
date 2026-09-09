"""Add campuses / campus_locations tables -- multi-university expansion, step 2

University -> Campus -> CampusLocation, per the multi-university map architecture. One
Campus row ("Main Campus") is created here for every existing University so every school
has somewhere for locations to attach to later -- LASU's row also gets the real
latitude/longitude already live in templates/campus-map.html (6.4700, 3.2000), migrated
rather than invented; every other school's campus stays coordinate-less until real data
exists (see seed_campus_map.py for the location rows themselves).

Revision ID: f2b5d8a03c69
Revises: e1a4c7f92b58
Create Date: 2026-09-06 00:00:00.000001

"""
from alembic import op
import sqlalchemy as sa

revision = 'f2b5d8a03c69'
down_revision = 'e1a4c7f92b58'
branch_labels = None
depends_on = None

LASU_LAT, LASU_LNG = 6.4700, 3.2000


def upgrade():
    op.create_table(
        'campuses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('university_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False, server_default='Main Campus'),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('is_main', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['university_id'], ['universities.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_campuses_university_id', 'campuses', ['university_id'])

    op.create_table(
        'campus_locations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('campus_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('category', sa.String(length=40), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('image_path', sa.String(length=200), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['campus_id'], ['campuses.id']),
        sa.ForeignKeyConstraint(['created_by'], ['user.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_campus_locations_campus_id', 'campus_locations', ['campus_id'])

    conn = op.get_bind()
    universities = conn.execute(sa.text('SELECT id, short_name FROM universities')).fetchall()
    for uni_id, short_name in universities:
        lat, lng = (LASU_LAT, LASU_LNG) if short_name == 'LASU' else (None, None)
        conn.execute(
            sa.text(
                'INSERT INTO campuses (university_id, name, latitude, longitude, is_main) '
                'VALUES (:uid, :name, :lat, :lng, true)'
            ),
            {'uid': uni_id, 'name': 'Main Campus', 'lat': lat, 'lng': lng},
        )


def downgrade():
    op.drop_index('ix_campus_locations_campus_id', table_name='campus_locations')
    op.drop_table('campus_locations')
    op.drop_index('ix_campuses_university_id', table_name='campuses')
    op.drop_table('campuses')
