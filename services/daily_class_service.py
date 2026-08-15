"""Cohort enrollment and day-by-day progress for 30-Day Skill Classes.

A daily class is self-paced (a student advances from Day N to Day N+1 by completing
Day N — there's no time-lockstep forcing everyone through the same day on the same
date), but every student's assignment due dates are still anchored to when THEY
personally enrolled, so "late" is a real, individually-meaningful signal rather than a
fiction. Cohort membership exists for peer comparison (ranking), not pacing.
"""
from datetime import datetime, timedelta
from extensions import db
from models import Cohort, CohortEnrollment, CourseModule, Lesson, StudentLessonProgress


def get_or_create_active_cohort(course):
    """Returns the course's current open-for-enrollment cohort, creating a first one
    (named after the current month) if none exists yet. Admins can also create named
    cohorts explicitly (see routes/admin_skills_routes.py) — this is only the fallback
    so a daily class is usable the moment it's published, without requiring an admin to
    remember to set up a cohort first."""
    active = Cohort.query.filter_by(course_id=course.id, is_active=True).order_by(Cohort.created_at.desc()).first()
    if active:
        return active
    cohort = Cohort(
        course_id=course.id, name=f"{datetime.utcnow().strftime('%B %Y')} Cohort",
        start_date=datetime.utcnow().date(), is_active=True,
    )
    db.session.add(cohort)
    db.session.commit()
    return cohort


def get_or_create_enrollment(student_id, course):
    """Idempotent — a student re-visiting a daily class they've already joined gets their
    existing enrollment, not a duplicate one in a newer cohort."""
    existing = (
        CohortEnrollment.query.join(Cohort, CohortEnrollment.cohort_id == Cohort.id)
        .filter(Cohort.course_id == course.id, CohortEnrollment.student_id == student_id).first()
    )
    if existing:
        return existing
    cohort = get_or_create_active_cohort(course)
    enrollment = CohortEnrollment(cohort_id=cohort.id, student_id=student_id, current_day=1)
    db.session.add(enrollment)
    db.session.commit()
    return enrollment


def get_days(course, published_only=True):
    """All day-lessons for a daily class, ordered by day_number, grouped for display as
    {week_number, week_title, days: [lesson, ...]}. Admin views pass published_only=False
    to see drafts too."""
    lessons = []
    for module in course.modules.order_by(CourseModule.order).all():
        q = module.lessons.filter(Lesson.day_number.isnot(None))
        if published_only:
            q = q.filter_by(is_published=True)
        lessons.extend(q.all())
    lessons.sort(key=lambda l: l.day_number)

    weeks = []
    current_week = None
    for lesson in lessons:
        wn = lesson.week_number or 0
        if current_week is None or current_week['week_number'] != wn:
            current_week = {'week_number': wn, 'week_title': lesson.week_title, 'days': []}
            weeks.append(current_week)
        current_week['days'].append(lesson)
    return weeks


def get_day_lesson(course, day_number):
    for module in course.modules.order_by(CourseModule.order).all():
        lesson = module.lessons.filter_by(is_published=True, day_number=day_number).first()
        if lesson:
            return lesson
    return None


def get_day_states(course, enrollment):
    """{day_number: 'completed'|'current'|'locked'} for the whole class, driven purely by
    enrollment.current_day and real StudentLessonProgress rows — same completed/current/
    locked vocabulary as get_path_step_states in services/skills_service.py."""
    weeks = get_days(course)
    all_lessons = [l for w in weeks for l in w['days']]
    completed_ids = {
        p.lesson_id for p in StudentLessonProgress.query.filter(
            StudentLessonProgress.student_id == enrollment.student_id,
            StudentLessonProgress.lesson_id.in_([l.id for l in all_lessons]),
        ).all()
    } if all_lessons else set()

    states = {}
    for lesson in all_lessons:
        if lesson.id in completed_ids:
            states[lesson.day_number] = 'completed'
        elif lesson.day_number <= enrollment.current_day:
            states[lesson.day_number] = 'current'
        else:
            states[lesson.day_number] = 'locked'
    return states, weeks, all_lessons


def get_class_progress_pct(course, enrollment):
    weeks = get_days(course)
    all_lessons = [l for w in weeks for l in w['days']]
    if not all_lessons:
        return 0
    completed = StudentLessonProgress.query.filter(
        StudentLessonProgress.student_id == enrollment.student_id,
        StudentLessonProgress.lesson_id.in_([l.id for l in all_lessons]),
    ).count()
    return round((completed / len(all_lessons)) * 100)


def advance_enrollment_day(enrollment, lesson):
    """Bumps current_day past a just-completed day so the next day unlocks. No-op if the
    completed lesson wasn't the current frontier (e.g. a student revisiting an earlier,
    already-passed day)."""
    if lesson.day_number and lesson.day_number == enrollment.current_day:
        enrollment.current_day = lesson.day_number + 1
        db.session.commit()


def compute_assignment_due_at(enrollment, lesson):
    """This student's personal due date for the assignment on `lesson` — anchored to when
    THEY enrolled, not a shared class-wide deadline, since the class is self-paced."""
    if not lesson.assignment or not lesson.day_number:
        return None
    day_unlock = enrollment.enrolled_at + timedelta(days=lesson.day_number - 1)
    return day_unlock + timedelta(hours=lesson.assignment.due_offset_hours or 48)
