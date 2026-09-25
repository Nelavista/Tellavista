"""Migration-level tests for b3f7a91c4e28 (academic sessions, enrollments, topic
mastery, and CBTAttempt.course_id).

These run the migration's own upgrade()/downgrade() against a throwaway SQLite database
containing only the pre-migration tables it touches. SQLite is a convenience here rather
than the real target (production is Postgres), so the assertions stick to portable facts:
tables and columns exist, and the CBT backfill resolved exactly the codes it should have.

The backfill's *conservatism* is the part worth locking down. `course_code` stays the
authoritative value for every attempt, and `course_id` must only be filled in when a code
maps to a single Course -- a code shared across departments must stay NULL rather than
being attributed to whichever course happened to be found first.
"""
import os
import tempfile
from contextlib import contextmanager

import pytest
import sqlalchemy as sa
from flask import Flask
from flask_migrate import Migrate, downgrade, stamp, upgrade
from sqlalchemy.exc import IntegrityError

from app.extensions import db

MIGRATIONS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'migrations'
)
PREVIOUS_REVISION = 'a7f2c9e14b83'

# Only the columns the migration reads or alters. Deliberately not the full production
# schema -- these tests are about this migration's own behavior, not a schema replica.
_PRE_MIGRATION_DDL = (
    'CREATE TABLE universities (id INTEGER PRIMARY KEY, name VARCHAR(150) NOT NULL)',
    'CREATE TABLE "user" (id INTEGER PRIMARY KEY, username VARCHAR(150) NOT NULL)',
    'CREATE TABLE courses (id INTEGER PRIMARY KEY, code VARCHAR(20) NOT NULL, '
    'title VARCHAR(200) NOT NULL)',
    'CREATE TABLE topic_progress (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, '
    'topic_id INTEGER NOT NULL, completed_at DATETIME, '
    'CONSTRAINT uq_topic_progress_user_topic UNIQUE (user_id, topic_id))',
    'CREATE TABLE cbt_attempts (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, '
    'course_code VARCHAR(20) NOT NULL, question_type VARCHAR(10) NOT NULL, '
    'total_questions INTEGER NOT NULL, correct_count INTEGER NOT NULL DEFAULT 0, '
    'score_pct INTEGER NOT NULL DEFAULT 0, '
    'FOREIGN KEY (user_id) REFERENCES "user" (id))',
)


def _columns(table):
    """Column names for `table`. Must be called inside an app context."""
    return {c['name'] for c in sa.inspect(db.engine).get_columns(table)}


def _tables():
    """Table names in the test database. Must be called inside an app context."""
    return set(sa.inspect(db.engine).get_table_names())


@contextmanager
def _database_at_previous_revision():
    """A temp SQLite DB holding the pre-migration schema, stamped at the revision this
    migration revises -- so upgrade() applies b3f7a91c4e28 and nothing else."""
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
            db.session.commit()

            # One University, and three course codes covering all three backfill cases:
            # unambiguous, ambiguous (same code in two departments), and unmatched.
            db.session.execute(sa.text("INSERT INTO universities (id, name) VALUES (1, 'LASU')"))
            db.session.execute(sa.text('INSERT INTO "user" (id, username) VALUES (1, \'stu\')'))
            for cid, code, title in (
                (1, 'CSC213', 'Data Structures'),
                (2, 'MAT101', 'Elementary Mathematics I'),
                (3, 'MAT101', 'Engineering Mathematics I'),
            ):
                db.session.execute(
                    sa.text('INSERT INTO courses (id, code, title) VALUES (:id, :code, :title)'),
                    {'id': cid, 'code': code, 'title': title},
                )
            for aid, code in ((1, 'CSC213'), (2, 'MAT101'), (3, 'ZZZ999')):
                db.session.execute(
                    sa.text(
                        'INSERT INTO cbt_attempts (id, user_id, course_code, question_type, '
                        'total_questions) VALUES (:id, 1, :code, \'cbt\', 10)'
                    ),
                    {'id': aid, 'code': code},
                )
            db.session.execute(sa.text(
                'INSERT INTO topic_progress (id, user_id, topic_id, completed_at) '
                "VALUES (1, 1, 7, '2026-01-01 00:00:00')"
            ))
            db.session.commit()

            stamp(revision=PREVIOUS_REVISION)
            upgrade()
            yield app
    finally:
        with app.app_context():
            db.session.remove()
            db.engine.dispose()  # release SQLite's file handle before os.remove()
        try:
            os.remove(db_path)
        except OSError:
            pass


def test_upgrade_adds_tables_columns_and_backfills_only_unambiguous_codes():
    with _database_at_previous_revision():
        assert {'academic_sessions', 'semesters', 'enrollments'} <= _tables()

        assert {'mastery_score', 'last_activity_at'} <= _columns('topic_progress')
        assert 'course_id' in _columns('cbt_attempts')

        # The pre-existing progress row survives the column additions with the new fields
        # unset -- "never measured" must not be backfilled as a zero score.
        row = db.session.execute(sa.text(
            'SELECT mastery_score, last_activity_at FROM topic_progress WHERE id = 1'
        )).fetchone()
        assert row is not None
        assert row[0] is None
        assert row[1] is None

        resolved = dict(db.session.execute(sa.text(
            'SELECT course_code, course_id FROM cbt_attempts'
        )).fetchall())
        assert resolved['CSC213'] == 1, 'unambiguous code should resolve to its Course'
        assert resolved['MAT101'] is None, 'code shared by two Courses must stay NULL'
        assert resolved['ZZZ999'] is None, 'code with no Course must stay NULL'

        # course_code remains the authoritative value for every row -- the backfill must
        # not have touched it.
        codes = {r[0] for r in db.session.execute(sa.text('SELECT course_code FROM cbt_attempts'))}
        assert codes == {'CSC213', 'MAT101', 'ZZZ999'}


def test_enrollment_allows_repeat_rows_without_a_session_but_not_with_one():
    """As documented on the model: a NULL session_id does not collapse rows, because a
    retake in a later, not-yet-recorded session is real."""
    with _database_at_previous_revision():
        for _ in range(2):
            db.session.execute(sa.text(
                'INSERT INTO enrollments (user_id, course_id, session_id) VALUES (1, 1, NULL)'
            ))
        db.session.commit()

        db.session.execute(
            sa.text('INSERT INTO academic_sessions (id, university_id, label) '
                    'VALUES (1, 1, :label)'),
            {'label': '2025/2026'},
        )
        db.session.execute(sa.text(
            'INSERT INTO enrollments (user_id, course_id, session_id) VALUES (1, 1, 1)'
        ))
        db.session.commit()

        with pytest.raises(IntegrityError):
            db.session.execute(sa.text(
                'INSERT INTO enrollments (user_id, course_id, session_id) VALUES (1, 1, 1)'
            ))
            db.session.commit()
        db.session.rollback()


def test_downgrade_restores_the_previous_schema():
    with _database_at_previous_revision():
        downgrade()

        assert not {'academic_sessions', 'semesters', 'enrollments'} & _tables()
        assert 'mastery_score' not in _columns('topic_progress')
        assert 'last_activity_at' not in _columns('topic_progress')
        assert 'course_id' not in _columns('cbt_attempts')

        # Rows the backfill only annotated must survive the downgrade intact.
        codes = {r[0] for r in db.session.execute(sa.text('SELECT course_code FROM cbt_attempts'))}
        assert codes == {'CSC213', 'MAT101', 'ZZZ999'}
