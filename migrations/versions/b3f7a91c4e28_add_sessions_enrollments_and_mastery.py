"""Add AcademicSession/Semester/Enrollment, TopicProgress.mastery_score, and
CBTAttempt.course_id -- the academic-context backbone the PRD's data model assumes.

Three gaps closed here. All of it is additive; no existing column is dropped, narrowed,
or re-typed, so this can be deployed before any code reads the new fields.

1. `academic_sessions` + `semesters`. Session and semester existed only as unvalidated
   free-text strings on User.semester and Course.semester, so nothing could reference
   "which semester" as a fact and no two rows agreed on spelling. Rows are deliberately
   NOT seeded here: no session labels are invented, matching the policy already applied
   to University.location and Course.semester, which stay blank until an admin enters
   sourced data via /admin/academia.

2. `enrollments` -- the user<->course registration row whose absence made "which courses
   is this student taking this semester" unanswerable. session_id / semester_id are
   nullable so a student can be enrolled before their school's sessions are recorded.

3. `topic_progress.mastery_score` / `last_activity_at`, and `cbt_attempts.course_id`.

The CBTAttempt backfill is deliberately conservative. `course_code` remains the
authoritative, always-set value -- it exists precisely so students at universities with
no seeded taxonomy can still use CBT, and nothing here changes that. `course_id` is
populated only when a code resolves to exactly ONE Course row; a code shared by several
departments or levels is left NULL rather than attributed to an arbitrary course, since a
wrong course attribution is worse than a missing one.

Revision ID: b3f7a91c4e28
Revises: a7f2c9e14b83
Create Date: 2026-09-25 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'b3f7a91c4e28'
down_revision = 'a7f2c9e14b83'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'academic_sessions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('university_id', sa.Integer(), sa.ForeignKey('universities.id'), nullable=False),
        sa.Column('label', sa.String(length=40), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('created_at', sa.DateTime()),
        sa.UniqueConstraint('university_id', 'label', name='uq_academic_session_university_label'),
    )
    op.create_index('ix_academic_sessions_university_id', 'academic_sessions', ['university_id'])

    op.create_table(
        'semesters',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('session_id', sa.Integer(), sa.ForeignKey('academic_sessions.id'), nullable=False),
        sa.Column('label', sa.String(length=40), nullable=False),
        sa.Column('created_at', sa.DateTime()),
        sa.UniqueConstraint('session_id', 'label', name='uq_semester_session_label'),
    )
    op.create_index('ix_semesters_session_id', 'semesters', ['session_id'])

    op.create_table(
        'enrollments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('course_id', sa.Integer(), sa.ForeignKey('courses.id'), nullable=False),
        sa.Column('session_id', sa.Integer(), sa.ForeignKey('academic_sessions.id'), nullable=True),
        sa.Column('semester_id', sa.Integer(), sa.ForeignKey('semesters.id'), nullable=True),
        sa.Column('created_at', sa.DateTime()),
        sa.UniqueConstraint('user_id', 'course_id', 'session_id', name='uq_enrollment_user_course_session'),
    )
    op.create_index('ix_enrollments_user_id', 'enrollments', ['user_id'])
    op.create_index('ix_enrollments_course_id', 'enrollments', ['course_id'])
    op.create_index('ix_enrollments_session_id', 'enrollments', ['session_id'])
    op.create_index('ix_enrollments_semester_id', 'enrollments', ['semester_id'])

    # Unconstrained columns can be added directly -- no constraint to alter.
    op.add_column('topic_progress', sa.Column('mastery_score', sa.Float(), nullable=True))
    op.add_column('topic_progress', sa.Column('last_activity_at', sa.DateTime(), nullable=True))

    # course_id carries a foreign key, so batch mode is required: the SQLite dialect
    # refuses ALTER TABLE ADD COLUMN with a constraint ("No support for ALTER of
    # constraints") and batch mode does a copy-and-move instead. On Postgres, batch mode
    # takes the direct path and emits a normal ADD COLUMN + ADD CONSTRAINT, so both
    # dialects end up with the same schema.
    with op.batch_alter_table('cbt_attempts', schema=None) as batch_op:
        batch_op.add_column(sa.Column(
            'course_id', sa.Integer(),
            # Named explicitly: batch mode refuses an unnamed constraint ("Constraint must
            # have a name"), and an unnamed FK also can't be referenced later. The model
            # leaves its FK unnamed like every other FK in this codebase -- the DB-level
            # name is only needed for this ALTER.
            sa.ForeignKey('courses.id', name='fk_cbt_attempts_course_id'),
            nullable=True,
        ))
    op.create_index('ix_cbt_attempts_course_id', 'cbt_attempts', ['course_id'])

    _backfill_cbt_course_id()


def _backfill_cbt_course_id():
    """Point existing CBT attempts at their Course where -- and only where -- the match
    is unambiguous.

    Done in Python rather than one UPDATE ... FROM so it behaves identically on Postgres
    (the deploy target) and SQLite (the test suite), following the backfill style already
    used by migration e1a4c7f92b58. Codes are compared case-insensitively, matching the
    existing convention in services/resolver.py and routes/materials_routes.py.
    """
    conn = op.get_bind()
    codes = conn.execute(sa.text(
        "SELECT DISTINCT course_code FROM cbt_attempts "
        "WHERE course_code IS NOT NULL AND course_code != ''"
    )).fetchall()

    resolved = ambiguous = unmatched = 0
    for (code,) in codes:
        matches = conn.execute(
            sa.text('SELECT id FROM courses WHERE UPPER(code) = UPPER(:code) ORDER BY id'),
            {'code': code},
        ).fetchall()

        if len(matches) == 1:
            conn.execute(
                sa.text('UPDATE cbt_attempts SET course_id = :cid WHERE course_code = :code'),
                {'cid': matches[0][0], 'code': code},
            )
            resolved += 1
        elif matches:
            ambiguous += 1
        else:
            unmatched += 1

    print(
        'cbt_attempts.course_id backfill: %d code(s) resolved, %d ambiguous (left NULL), '
        '%d with no matching Course (left NULL)' % (resolved, ambiguous, unmatched)
    )


def downgrade():
    op.drop_index('ix_cbt_attempts_course_id', table_name='cbt_attempts')
    with op.batch_alter_table('cbt_attempts', schema=None) as batch_op:
        batch_op.drop_column('course_id')

    with op.batch_alter_table('topic_progress', schema=None) as batch_op:
        batch_op.drop_column('last_activity_at')
        batch_op.drop_column('mastery_score')

    op.drop_index('ix_enrollments_semester_id', table_name='enrollments')
    op.drop_index('ix_enrollments_session_id', table_name='enrollments')
    op.drop_index('ix_enrollments_course_id', table_name='enrollments')
    op.drop_index('ix_enrollments_user_id', table_name='enrollments')
    op.drop_table('enrollments')

    op.drop_index('ix_semesters_session_id', table_name='semesters')
    op.drop_table('semesters')

    op.drop_index('ix_academic_sessions_university_id', table_name='academic_sessions')
    op.drop_table('academic_sessions')
