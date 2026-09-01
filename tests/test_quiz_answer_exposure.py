"""Regression tests for the quiz-answer-exposure bug: lesson_view.html/day_view.html
used to render Quiz.questions (which carries correct_index/explanation) straight into
the page's initial HTML via `data-correct="{{ q.correct_index }}"`, visible to any
student via View Source before answering -- combined with unlimited retakes and
StudentQuizAttempt.score feeding into the Skill GPA (services/gpa_service.py's
_tests_component) and cohort rank shown on a student's public skill transcript, this was
a trivial way to inflate a credential the product explicitly positions as trustworthy to
employers.

The fix: routes pass a sanitized quiz_questions list (Quiz.to_dict(include_answers=False),
the model's own answer-stripped view) to the template instead of the raw ORM questions,
and the answer key is only ever returned by /skills/quiz/<id>/submit's JSON response,
after the server has already graded the submission.
"""
from extensions import db
from models import Skill, SkillCategory, SkillCourse, CourseModule, Lesson, Quiz


def _make_lesson_with_quiz(slug='quiz-lesson'):
    category = SkillCategory(name='QuizCat', slug=f'{slug}-cat', order=0)
    db.session.add(category)
    db.session.commit()
    skill = Skill(category_id=category.id, name='Quiz Skill', slug=f'{slug}-skill', is_published=True)
    db.session.add(skill)
    db.session.commit()
    course = SkillCourse(skill_id=skill.id, title='Quiz Course', slug=f'{slug}-course', order=0, is_published=True)
    db.session.add(course)
    db.session.commit()
    module = CourseModule(course_id=course.id, title='Module 1', order=0)
    db.session.add(module)
    db.session.commit()
    lesson = Lesson(module_id=module.id, title='Lesson 1', slug=slug, order=0, is_published=True, duration_minutes=5)
    lesson.videos = []  # skip the auto-fetch-on-first-view branch -- no network call in a test
    db.session.add(lesson)
    db.session.commit()
    quiz = Quiz(lesson_id=lesson.id, title='Check yourself')
    quiz.questions = [
        {'question': 'What is 2 + 2?', 'options': ['3', '4', '5'], 'correct_index': 1,
         'explanation': 'Basic arithmetic: 2 + 2 = 4.'},
    ]
    db.session.add(quiz)
    db.session.commit()
    return skill, course, lesson, quiz


def test_lesson_view_page_does_not_leak_quiz_answer(app, client, make_user, login_as):
    with app.app_context():
        skill, course, lesson, quiz = _make_lesson_with_quiz()
        skill_slug, course_slug, lesson_slug = skill.slug, course.slug, lesson.slug

    student = make_user('quiz_leak_student')
    login_as(client, student)

    res = client.get(f'/skills/{skill_slug}/learn/{course_slug}/{lesson_slug}')
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert 'data-correct' not in html
    assert 'Basic arithmetic' not in html  # the explanation text must not be pre-rendered
    assert 'What is 2 + 2?' in html  # the question itself is still shown


def test_quiz_submit_grades_correctly_and_returns_answer_key(app, client, make_user, login_as):
    with app.app_context():
        skill, course, lesson, quiz = _make_lesson_with_quiz(slug='quiz-submit')
        quiz_id = quiz.id

    student = make_user('quiz_submit_student')
    login_as(client, student)

    # Wrong answer (index 0, correct is index 1)
    res = client.post(f'/skills/quiz/{quiz_id}/submit', json={'answers': [0]})
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert data['score'] == 0
    assert data['correct'] == 0
    assert data['results'] == [{'correct_index': 1, 'explanation': 'Basic arithmetic: 2 + 2 = 4.'}]

    # Right answer
    res = client.post(f'/skills/quiz/{quiz_id}/submit', json={'answers': [1]})
    assert res.status_code == 200
    data = res.get_json()
    assert data['score'] == 100
    assert data['correct'] == 1
