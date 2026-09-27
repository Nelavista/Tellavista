"""Migration-level test for c4d8e2f1a7b3 (material_views.last_page).

Same shape as tests/test_sessions_enrollment_migration.py: the migration's own
upgrade()/downgrade() run against a throwaway SQLite database holding only the table
it touches, stamped at the revision it revises. Assertions stay to portable facts --
the column exists after upgrade and is gone after downgrade, with existing rows NULL.

The NULL semantics are the point: a view row that never recorded a position must read
as "never recorded", not as page 1 (that distinction is what keeps "Continue learning"
from jumping students back to the start of a document they never finished).
"""
import os
import tempfile
from contextlib import contextmanager

import sqlalchemy as sa
from flask import Flask
from flask_migrate import Migrate, downgrade, stamp, upgrade

from app.extensions import db

MIGRATIONS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'migrations'
)
PREVIOUS_REVISION = 'b3f7a91c4e28'   # must track c4d8e2f1a7b3's down_revision
TARGET_REVISION = 'c4d8e2f1a7b3'

_PRE_MIGRATION_DDL = (
    'CREATE TABLE "user" (id INTEGER PRIMARY KEY, username VARCHAR(150) NOT NULL)',
    'CREATE TABLE materials (id INTEGER PRIMARY KEY, title VARCHAR(200) NOT NULL)',
    'CREATE TABLE material_views ('
    'id INTEGER PRIMARY KEY, '
    'user_id INTEGER NOT NULL, '
    'material_id INTEGER NOT NULL, '
    'viewed_at DATETIME, '
    'CONSTRAINT uq_material_view_user_material UNIQUE (user_id, material_id))',
)


@contextmanager
def _database_at_target_revision():
    """Temp SQLite DB with the pre-migration schema, stamped at PREVIOUS_REVISION and
    upgraded to TARGET_REVISION -- and nothing newer."""
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)

    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{db_path}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    db.init_app(app)
    Migrate(app, db, directory=MIGRATIONS_DIR)

    try:
        with app.app_context():
            for ddl in _PRE_MIGRATION_DDL:
                db.session.execute(sa.text(ddl))
            db.session.execute(sa.text(
                "INSERT INTO material_views (user_id, material_id, viewed_at) "
                "VALUES (1, 1, '2026-01-01 00:00:00')"
            ))
            db.session.commit()

            stamp(revision=PREVIOUS_REVISION)
            upgrade(revision=TARGET_REVISION)
            yield app
    finally:
        with app.app_context():
            db.session.remove()
            db.engine.dispose()   # release SQLite's file handle before os.remove()
        try:
            os.remove(db_path)
        except OSError:
            pass


def test_upgrade_adds_nullable_last_page_and_leaves_existing_rows_null():
    with _database_at_target_revision():
        with db.engine.connect() as conn:
            cols = {c['name'] for c in sa.inspect(db.engine).get_columns('material_views')}
            assert 'last_page' in cols

            # Existing view rows must land NULL -- "never recorded", not page 1.
            row = conn.execute(sa.text('SELECT last_page FROM material_views WHERE id = 1')).fetchone()
            assert row is not None
            assert row[0] is None

            # And the column must actually accept a value.
            conn.execute(sa.text('UPDATE material_views SET last_page = 7 WHERE id = 1'))
            conn.commit()
            row = conn.execute(sa.text('SELECT last_page FROM material_views WHERE id = 1')).fetchone()
            assert row[0] == 7


def test_downgrade_removes_the_column_and_keeps_the_rows():
    with _database_at_target_revision():
        downgrade()   # '-1' (flask_migrate default) = one step: back to PREVIOUS_REVISION
        with db.engine.connect() as conn:
            cols = {c['name'] for c in sa.inspect(db.engine).get_columns('material_views')}
            assert 'last_page' not in cols
            # The view row itself must survive the downgrade intact.
            count = conn.execute(sa.text('SELECT COUNT(*) FROM material_views')).scalar()
            assert count == 1
