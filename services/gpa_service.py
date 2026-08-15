"""Skill GPA computation for 30-Day Skill Classes.

Named and always displayed as "Skill GPA" / "Nelavista Skill GPA" — never as academic
CGPA. It is computed entirely from a student's graded work inside one daily class
(assignments, tests, final project, participation), using ONLY the grade scale and
component weights an admin configured for that specific course (see GradeScale /
GradeWeight in models.py). There is no hardcoded scale or weighting baked into this
module — a course with nothing configured simply can't produce a GPA yet (see
compute_skill_gpa's 'not configured' branch) rather than silently guessing one.

Same "recompute, don't trust a stale cache" principle as services/skills_service.py:
CohortEnrollment.skill_gpa is a cache written by recompute_and_cache_gpa (called after
every grading event), but the calculation itself always re-derives from the underlying
AssignmentSubmission / StudentQuizAttempt / StudentProject rows.
"""
from datetime import datetime
from extensions import db
from models import (
    GradeScale, GradeWeight, Lesson, CourseModule, AssignmentSubmission,
    StudentQuizAttempt, StudentProject, ProjectTemplate, StudentLessonProgress,
)

# Seeded into a course's GradeWeight rows the first time an admin turns on grading for a
# daily class (see routes/admin_skills_routes.py) — a starting point, not a hardcoded rule;
# admins can change every number afterward per course.
DEFAULT_GRADE_WEIGHTS = {'assignments': 40, 'tests': 25, 'final_project': 25, 'participation': 10}

DEFAULT_GRADE_SCALE = [
    {'grade_letter': 'A', 'min_score': 90, 'max_score': 100, 'grade_point': 5.0, 'order': 1},
    {'grade_letter': 'B', 'min_score': 80, 'max_score': 89, 'grade_point': 4.0, 'order': 2},
    {'grade_letter': 'C', 'min_score': 70, 'max_score': 79, 'grade_point': 3.0, 'order': 3},
    {'grade_letter': 'D', 'min_score': 60, 'max_score': 69, 'grade_point': 2.0, 'order': 4},
    {'grade_letter': 'E', 'min_score': 50, 'max_score': 59, 'grade_point': 1.0, 'order': 5},
    {'grade_letter': 'F', 'min_score': 0, 'max_score': 49, 'grade_point': 0.0, 'order': 6},
]

COMPONENT_LABELS = {
    'assignments': 'Assignments', 'tests': 'Tests', 'final_project': 'Final Project',
    'participation': 'Participation',
}


def score_to_grade(course, score):
    """Maps a 0-100 percentage to (letter, point) using this course's own GradeScale rows.
    Returns (None, None) if the course has no scale configured yet."""
    scale = GradeScale.query.filter_by(course_id=course.id).order_by(GradeScale.order).all()
    if not scale:
        return None, None
    for row in scale:
        # Admin-entered bands are whole-percent integers (e.g. B: 80-89, A: 90-100), but a
        # weighted score is a continuous float — a plain `<= max_score` check leaves the
        # 89-90 sliver matching nothing (89.75 fits neither 80<=x<=89 nor 90<=x<=100). Treat
        # max_score as exclusive-at-the-next-integer instead, so bands tile with no gaps.
        if row.min_score <= score < row.max_score + 1:
            return row.grade_letter, row.grade_point
    # Score fell outside every configured band entirely (e.g. a negative score, or gaps
    # deliberately left by an admin edit) — fall back to whichever band's midpoint is
    # closest, rather than returning nothing.
    closest = min(scale, key=lambda r: abs(score - (r.min_score + r.max_score) / 2))
    return closest.grade_letter, closest.grade_point


def _reached_lessons(course, enrollment):
    """Lessons the student has actually reached (day_number <= their current_day) — GPA
    is computed only against work that's actually been assigned to them so far, so a
    student on Day 5 isn't penalized for Day 6-30 work that doesn't exist for them yet."""
    lessons = []
    for module in course.modules.order_by(CourseModule.order).all():
        for lesson in module.lessons.filter_by(is_published=True).all():
            if lesson.day_number and lesson.day_number <= enrollment.current_day:
                lessons.append(lesson)
    return lessons


def _assignments_component(student_id, lessons):
    graded_lessons = [l for l in lessons if l.assignment]
    if not graded_lessons:
        return None
    total = 0
    for l in graded_lessons:
        sub = (
            AssignmentSubmission.query.filter_by(assignment_id=l.assignment.id, student_id=student_id)
            .order_by(AssignmentSubmission.submitted_at.desc()).first()
        )
        # A reached-but-never-submitted assignment counts as 0 — an assignment that's
        # simply skipped over must not be invisible to grading, or a student could game
        # their GPA by only ever attempting the ones they're confident about.
        total += sub.score if (sub and sub.score is not None) else 0
    return total / len(graded_lessons)


def _tests_component(student_id, lessons):
    quiz_lessons = [l for l in lessons if l.quiz]
    if not quiz_lessons:
        return None
    total = 0
    for l in quiz_lessons:
        attempt = (
            StudentQuizAttempt.query.filter_by(quiz_id=l.quiz.id, student_id=student_id)
            .order_by(StudentQuizAttempt.completed_at.desc()).first()
        )
        total += attempt.score if attempt else 0
    return total / len(quiz_lessons)


def _final_project_component(course, student_id):
    template = ProjectTemplate.query.filter_by(course_id=course.id, is_final_project=True).first()
    if not template:
        return None
    project = StudentProject.query.filter_by(student_id=student_id, project_template_id=template.id).first()
    if not project:
        return 0  # the final project exists and is reachable, but not started yet
    return project.ai_overall_score if project.ai_overall_score is not None else 0


def _participation_component(student_id, lessons):
    if not lessons:
        return None
    lesson_ids = [l.id for l in lessons]
    done = StudentLessonProgress.query.filter(
        StudentLessonProgress.student_id == student_id, StudentLessonProgress.lesson_id.in_(lesson_ids)
    ).count()
    return round((done / len(lessons)) * 100, 1)


def compute_skill_gpa(enrollment):
    """Returns a full, transparent breakdown for one CohortEnrollment — every number a
    student would need to see exactly how their Skill GPA was calculated:
      {
        'gpa': float|None, 'grade_letter': str|None, 'percentage': float|None,
        'breakdown': [{'component','label','weight_pct','score_pct','contribution_pct'}],
        'configured': bool,
      }
    'gpa' is None when the course has no GradeWeight/GradeScale configured yet, or when
    the student has no graded work in any weighted component yet — never a guessed number.
    """
    course = enrollment.cohort.course
    weights = {w.component: w.weight_pct for w in GradeWeight.query.filter_by(course_id=course.id).all() if w.weight_pct > 0}
    if not weights:
        return {'gpa': None, 'grade_letter': None, 'percentage': None, 'breakdown': [], 'configured': False}

    lessons = _reached_lessons(course, enrollment)
    component_scores = {
        'assignments': _assignments_component(enrollment.student_id, lessons),
        'tests': _tests_component(enrollment.student_id, lessons),
        'final_project': _final_project_component(course, enrollment.student_id),
        'participation': _participation_component(enrollment.student_id, lessons),
    }

    # Only components that are both weighted by the admin AND actually applicable right
    # now (e.g. the final project isn't reachable yet, or this class has no quizzes) count
    # toward the total — their weight is excluded rather than treated as a zero, so a
    # class without a final-project component configured doesn't drag every student's GPA
    # down for something that was never assigned to them.
    breakdown = []
    weighted_sum = 0.0
    weight_total = 0
    for component, weight_pct in weights.items():
        score = component_scores.get(component)
        if score is None:
            continue
        weighted_sum += score * weight_pct
        weight_total += weight_pct
        breakdown.append({
            'component': component, 'label': COMPONENT_LABELS.get(component, component),
            'weight_pct': weight_pct, 'score_pct': round(score, 1),
        })

    if weight_total == 0:
        return {'gpa': None, 'grade_letter': None, 'percentage': None, 'breakdown': [], 'configured': True}

    overall_pct = weighted_sum / weight_total
    for row in breakdown:
        row['contribution_pct'] = round((row['weight_pct'] / weight_total) * 100, 1)
    letter, point = score_to_grade(course, overall_pct)

    return {
        'gpa': point, 'grade_letter': letter, 'percentage': round(overall_pct, 1),
        'breakdown': breakdown, 'configured': True,
    }


def recompute_and_cache_gpa(enrollment):
    """Recomputes and persists enrollment.skill_gpa — call after any grading event
    (assignment reviewed, test submitted, final project evaluated, lesson completed) that
    could move the number. Returns the same breakdown dict as compute_skill_gpa."""
    result = compute_skill_gpa(enrollment)
    enrollment.skill_gpa = result['gpa']
    enrollment.gpa_updated_at = datetime.utcnow()
    db.session.commit()
    return result


def get_cohort_rank(enrollment):
    """(rank, total) of this enrollment within its cohort, ranked by skill_gpa desc.
    Enrollments with no GPA yet (nothing graded) are excluded from ranking but still
    counted in 'total' — a student who hasn't started grading yet has no rank, not a
    last-place rank, since that would falsely imply their work was evaluated and scored low."""
    all_enrollments = enrollment.cohort.enrollments.all()
    total = len(all_enrollments)
    ranked = sorted(
        [e for e in all_enrollments if e.skill_gpa is not None],
        key=lambda e: e.skill_gpa, reverse=True,
    )
    for i, e in enumerate(ranked, start=1):
        if e.id == enrollment.id:
            return i, total
    return None, total
