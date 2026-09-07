"""Regression tests for services/skills_service.py's can_access_lesson() and its use in
routes/skills_routes.py's complete_lesson/submit_quiz/submit_assignment.

Before this existed, all three routes resolved their target straight from the URL's
numeric id (Lesson.query.get_or_404 / Quiz.query.get_or_404 /
Assignment.query.get_or_404) with no check that the lesson/quiz/assignment was published,
or -- for a daily class -- that the student had actually reached that day yet. That made
a quiz's answer key (only ever meant to be released by submit_quiz's own response, after
grading) scrapeable by enumerating quiz ids for content the student was never shown, and
let a student pre-submit graded work for days they hadn't unlocked.
"""
from datetime import datetime
from extensions import db
from models import (
    Skill, SkillCategory, SkillCourse, CourseModule, Lesson, Quiz, Assignment,
    Cohort, CohortEnrollment,
)


def _make_ordinary_lesson(published=True):
    category = SkillCategory(name='GateCat', slug='gate-cat', order=0)
    db.session.add(category)
    db.session.commit()
    skill = Skill(category_id=category.id, name='Gate Skill', slug='gate-skill', is_published=True)
    db.session.add(skill)
    db.session.commit()
    course = SkillCourse(skill_id=skill.id, title='Gate Course', slug='gate-course', order=0, is_published=True)
    db.session.add(course)
    db.session.commit()
    module = CourseModule(course_id=course.id, title='Module 1', order=0)
    db.session.add(module)
    db.session.commit()
    lesson = Lesson(module_id=module.id, title='Draft Lesson', slug='draft-lesson', order=0,
                     is_published=published, duration_minutes=5)
    db.session.add(lesson)
    db.session.commit()
    quiz = Quiz(lesson_id=lesson.id, title='Quiz')
    quiz.questions = [{'question': 'Q?', 'options': ['a', 'b'], 'correct_index': 0, 'explanation': 'because'}]
    db.session.add(quiz)
    db.session.commit()
    return lesson, quiz


def _make_daily_class(current_day=1):
    category = SkillCategory(name='DayGateCat', slug='day-gate-cat', order=0)
    db.session.add(category)
    db.session.commit()
    skill = Skill(category_id=category.id, name='Day Gate Skill', slug='day-gate-skill', is_published=True)
    db.session.add(skill)
    db.session.commit()
    course = SkillCourse(skill_id=skill.id, title='30 Day Class', slug='day-gate-class', order=0,
                          is_published=True, is_daily_class=True, duration_days=3)
    db.session.add(course)
    db.session.commit()
    module = CourseModule(course_id=course.id, title='Week 1', order=0)
    db.session.add(module)
    db.session.commit()
    day5 = Lesson(module_id=module.id, title='Day 5', slug='day-5', order=4, is_published=True,
                   duration_minutes=5, day_number=5)
    db.session.add(day5)
    db.session.commit()
    quiz = Quiz(lesson_id=day5.id, title='Day 5 Quiz')
    quiz.questions = [{'question': 'Q?', 'options': ['a', 'b'], 'correct_index': 1, 'explanation': 'because'}]
    db.session.add(quiz)
    assignment = Assignment(lesson_id=day5.id, title='Day 5 Assignment', instructions='Do the thing')
    db.session.add(assignment)
    db.session.commit()

    cohort = Cohort(course_id=course.id, name='Cohort A', start_date=datetime.utcnow().date())
    db.session.add(cohort)
    db.session.commit()
    return course, day5, quiz, assignment, cohort


# ===== complete_lesson =====

def test_complete_lesson_rejects_unpublished_lesson(app, client, make_user, login_as):
    with app.app_context():
        lesson, _ = _make_ordinary_lesson(published=False)
        lesson_id = lesson.id
    student = make_user('gate_complete_student')
    login_as(client, student)

    res = client.post(f'/skills/lesson/{lesson_id}/complete')
    assert res.status_code == 403
    assert res.get_json()['success'] is False


def test_complete_lesson_allows_published_lesson(app, client, make_user, login_as):
    with app.app_context():
        lesson, _ = _make_ordinary_lesson(published=True)
        lesson_id = lesson.id
    student = make_user('gate_complete_ok_student')
    login_as(client, student)

    res = client.post(f'/skills/lesson/{lesson_id}/complete')
    assert res.status_code == 200
    assert res.get_json()['success'] is True


def test_complete_lesson_rejects_locked_daily_class_day(app, client, make_user, login_as):
    student = make_user('gate_complete_locked_student')
    with app.app_context():
        course, day5, quiz, assignment, cohort = _make_daily_class()
        db.session.add(CohortEnrollment(cohort_id=cohort.id, student_id=student.id, current_day=1))
        db.session.commit()
        lesson_id = day5.id
    login_as(client, student)

    res = client.post(f'/skills/lesson/{lesson_id}/complete')
    assert res.status_code == 403


# ===== submit_quiz (the answer-key-scrape path) =====

def test_submit_quiz_rejects_unpublished_quiz_and_never_leaks_answer_key(app, client, make_user, login_as):
    with app.app_context():
        lesson, quiz = _make_ordinary_lesson(published=False)
        quiz_id = quiz.id
    student = make_user('gate_quiz_student')
    login_as(client, student)

    res = client.post(f'/skills/quiz/{quiz_id}/submit', json={'answers': [0]})
    assert res.status_code == 403
    body = res.get_json()
    assert body['success'] is False
    assert 'correct_index' not in str(body)  # the answer key must not leak in the rejection either


def test_submit_quiz_rejects_locked_daily_class_day(app, client, make_user, login_as):
    student = make_user('gate_quiz_locked_student')
    with app.app_context():
        course, day5, quiz, assignment, cohort = _make_daily_class()
        db.session.add(CohortEnrollment(cohort_id=cohort.id, student_id=student.id, current_day=1))
        db.session.commit()
        quiz_id = quiz.id
    login_as(client, student)

    res = client.post(f'/skills/quiz/{quiz_id}/submit', json={'answers': [1]})
    assert res.status_code == 403


def test_submit_quiz_allows_reached_daily_class_day(app, client, make_user, login_as):
    student = make_user('gate_quiz_reached_student')
    with app.app_context():
        course, day5, quiz, assignment, cohort = _make_daily_class()
        db.session.add(CohortEnrollment(cohort_id=cohort.id, student_id=student.id, current_day=5))
        db.session.commit()
        quiz_id = quiz.id
    login_as(client, student)

    res = client.post(f'/skills/quiz/{quiz_id}/submit', json={'answers': [1]})
    assert res.status_code == 200
    assert res.get_json()['score'] == 100


def test_submit_quiz_rejects_non_list_answers_payload(app, client, make_user, login_as):
    with app.app_context():
        lesson, quiz = _make_ordinary_lesson(published=True)
        quiz_id = quiz.id
    student = make_user('gate_quiz_badpayload_student')
    login_as(client, student)

    res = client.post(f'/skills/quiz/{quiz_id}/submit', json={'answers': None})
    assert res.status_code == 400

    res2 = client.post(f'/skills/quiz/{quiz_id}/submit', json={'answers': {'0': 1}})
    assert res2.status_code == 400


# ===== submit_assignment =====

def test_submit_assignment_rejects_locked_daily_class_day(app, client, make_user, login_as):
    student = make_user('gate_assignment_locked_student')
    with app.app_context():
        course, day5, quiz, assignment, cohort = _make_daily_class()
        db.session.add(CohortEnrollment(cohort_id=cohort.id, student_id=student.id, current_day=1))
        db.session.commit()
        assignment_id = assignment.id

    login_as(client, student)
    res = client.post(f'/skills/assignment/{assignment_id}/submit', data={'content': 'my early submission'},
                       follow_redirects=False)
    assert res.status_code == 302  # redirected back to class_overview with a flash, not accepted

    with app.app_context():
        from models import AssignmentSubmission
        assert AssignmentSubmission.query.filter_by(assignment_id=assignment_id).count() == 0
