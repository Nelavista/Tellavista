"""Regression test for the gpa_service.py N+1 fix (services/gpa_service.py's
_reached_lessons/_assignments_component/_tests_component were rewritten from
one-query-per-lesson to bulk queries) -- confirms the GPA math still comes out
identical to what the original per-lesson-query version would have produced."""
from datetime import datetime, timedelta
from extensions import db
from models import (
    Skill, SkillCategory, SkillCourse, CourseModule, Lesson, Cohort, CohortEnrollment,
    GradeScale, GradeWeight, Assignment, AssignmentSubmission, Quiz, StudentQuizAttempt,
    StudentLessonProgress,
)
from services.gpa_service import compute_skill_gpa, DEFAULT_GRADE_SCALE, DEFAULT_GRADE_WEIGHTS


def test_compute_skill_gpa_bulk_queries_match_expected_math(app, make_user):
    user = make_user('gpa_student')
    with app.app_context():
        category = SkillCategory(name='GpaCat', slug='gpacat', order=0)
        db.session.add(category)
        db.session.commit()
        skill = Skill(category_id=category.id, name='GPA Skill', slug='gpa-skill', is_published=True)
        db.session.add(skill)
        db.session.commit()
        course = SkillCourse(skill_id=skill.id, title='30-Day Class', slug='30-day-class',
                              order=0, is_published=True, is_daily_class=True, duration_days=3)
        db.session.add(course)
        db.session.commit()

        for c in DEFAULT_GRADE_SCALE:
            db.session.add(GradeScale(course_id=course.id, **c))
        for component, pct in DEFAULT_GRADE_WEIGHTS.items():
            db.session.add(GradeWeight(course_id=course.id, component=component, weight_pct=pct))
        db.session.commit()

        module = CourseModule(course_id=course.id, title='Week 1', order=0)
        db.session.add(module)
        db.session.commit()

        # 2 lessons with assignments, 1 with a quiz, all reached (day_number <= current_day=3)
        lesson1 = Lesson(module_id=module.id, title='Day 1', slug='day-1', order=0, is_published=True, day_number=1)
        lesson2 = Lesson(module_id=module.id, title='Day 2', slug='day-2', order=1, is_published=True, day_number=2)
        lesson3 = Lesson(module_id=module.id, title='Day 3', slug='day-3', order=2, is_published=True, day_number=3)
        db.session.add_all([lesson1, lesson2, lesson3])
        db.session.commit()

        a1 = Assignment(lesson_id=lesson1.id, title='A1', instructions='x')
        a2 = Assignment(lesson_id=lesson2.id, title='A2', instructions='x')
        db.session.add_all([a1, a2])
        q1 = Quiz(lesson_id=lesson3.id, title='Q1')
        db.session.add(q1)
        db.session.commit()

        # Submissions: a1 has two submissions (must pick the LATEST by submitted_at), a2 has none (counts as 0)
        db.session.add(AssignmentSubmission(assignment_id=a1.id, student_id=user.id, score=60,
                                             submitted_at=datetime.utcnow() - timedelta(days=1), content='first try'))
        db.session.add(AssignmentSubmission(assignment_id=a1.id, student_id=user.id, score=90,
                                             submitted_at=datetime.utcnow(), content='resubmit, better'))
        db.session.commit()

        db.session.add(StudentQuizAttempt(quiz_id=q1.id, student_id=user.id, score=80, completed_at=datetime.utcnow()))
        db.session.commit()

        cohort = Cohort(course_id=course.id, name='Cohort A', start_date=datetime.utcnow().date())
        db.session.add(cohort)
        db.session.commit()
        enrollment = CohortEnrollment(cohort_id=cohort.id, student_id=user.id, current_day=3)
        db.session.add(enrollment)
        db.session.commit()

        result = compute_skill_gpa(enrollment)

        assert result['configured'] is True
        by_component = {b['component']: b['score_pct'] for b in result['breakdown']}
        # assignments: (90 [latest a1 submission, not 60] + 0 [a2 never submitted]) / 2 = 45.0
        assert by_component['assignments'] == 45.0
        # tests: only one quiz lesson, scored 80
        assert by_component['tests'] == 80.0
        # participation: 0 of 3 reached lessons marked complete via StudentLessonProgress
        assert by_component['participation'] == 0.0
        assert result['gpa'] is not None
