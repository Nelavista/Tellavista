"""Add indexes on high-traffic foreign-key/lookup columns identified by the Level 1
scale audit: student_skills.student_id, student_lesson_progress.student_id,
cohort_enrollments.student_id, cbt_attempts.user_id, opportunity_applications.student_id,
ratings.student_id, notifications.user_id, message_threads.employer_id/student_id,
messages.thread_id/sender_id. These are the columns actually filtered on in
services/skills_service.py, services/gpa_service.py, services/messaging_service.py,
services/notification_service.py, and routes/cbt_routes.py -- not a blanket "index
everything" pass.

Revision ID: d4b6f0a2e158
Revises: c8e1a2f4b937
Create Date: 2026-08-25 00:00:00.000002

"""
from alembic import op

revision = 'd4b6f0a2e158'
down_revision = 'c8e1a2f4b937'
branch_labels = None
depends_on = None

INDEXES = [
    ('ix_student_skills_student_id', 'student_skills', 'student_id'),
    ('ix_student_lesson_progress_student_id', 'student_lesson_progress', 'student_id'),
    ('ix_cohort_enrollments_student_id', 'cohort_enrollments', 'student_id'),
    ('ix_cbt_attempts_user_id', 'cbt_attempts', 'user_id'),
    ('ix_opportunity_applications_student_id', 'opportunity_applications', 'student_id'),
    ('ix_ratings_student_id', 'ratings', 'student_id'),
    ('ix_notifications_user_id', 'notifications', 'user_id'),
    ('ix_message_threads_employer_id', 'message_threads', 'employer_id'),
    ('ix_message_threads_student_id', 'message_threads', 'student_id'),
    ('ix_messages_thread_id', 'messages', 'thread_id'),
    ('ix_messages_sender_id', 'messages', 'sender_id'),
]


def upgrade():
    for name, table, column in INDEXES:
        op.create_index(name, table, [column])


def downgrade():
    for name, table, column in reversed(INDEXES):
        op.drop_index(name, table_name=table)
