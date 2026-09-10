"""Regression tests for the admin-side content-integrity validation added to
routes/admin_skills_routes.py: rubric points must sum to 100 (AD-5), grade weights must
sum to 100 once all 4 components are set (AD-6), and a quiz question's correct_index
must be a real, in-range integer (AD-9).

Before these existed, the admin UI showed a live "sums to 100?" warning but never
blocked the save on it, and a quiz question with a bad correct_index saved fine and
became silently, permanently unwinnable.
"""
from app.extensions import db
from app.models import Skill, SkillCategory, SkillCourse, CourseModule, Lesson, ProjectTemplate


def _make_admin(make_user, login_as, client, username='content_admin'):
    admin = make_user(username, is_admin=True)
    login_as(client, admin)
    return admin


def _make_course(is_daily_class=False):
    category = SkillCategory(name='ContentCat', slug='content-cat', order=0)
    db.session.add(category)
    db.session.commit()
    skill = Skill(category_id=category.id, name='Content Skill', slug='content-skill', is_published=True)
    db.session.add(skill)
    db.session.commit()
    course = SkillCourse(skill_id=skill.id, title='Content Course', slug='content-course', order=0,
                          is_published=True, is_daily_class=is_daily_class)
    db.session.add(course)
    db.session.commit()
    return skill, course


# ===== Rubric sum validation (AD-5) =====

def test_update_project_template_rejects_rubric_not_summing_to_100(app, client, make_user, login_as):
    _make_admin(make_user, login_as, client)
    with app.app_context():
        skill, _ = _make_course()
        template = ProjectTemplate(skill_id=skill.id, title='Rubric Template', slug='rubric-template')
        db.session.add(template)
        db.session.commit()
        template_id = template.id

    res = client.put(f'/admin/api/projects/{template_id}', json={
        'rubric': [{'name': 'Functionality', 'max_points': 40}, {'name': 'Craft', 'max_points': 40}]  # sums to 80
    })
    assert res.status_code == 400

    with app.app_context():
        assert ProjectTemplate.query.get(template_id).rubric == []


def test_update_project_template_accepts_rubric_summing_to_100(app, client, make_user, login_as):
    _make_admin(make_user, login_as, client)
    with app.app_context():
        skill, _ = _make_course()
        template = ProjectTemplate(skill_id=skill.id, title='Rubric Template 2', slug='rubric-template-2')
        db.session.add(template)
        db.session.commit()
        template_id = template.id

    res = client.put(f'/admin/api/projects/{template_id}', json={
        'rubric': [{'name': 'Functionality', 'max_points': 60}, {'name': 'Craft', 'max_points': 40}]
    })
    assert res.status_code == 200

    with app.app_context():
        assert sum(c['max_points'] for c in ProjectTemplate.query.get(template_id).rubric) == 100


def test_create_final_project_rejects_bad_rubric(app, client, make_user, login_as):
    _make_admin(make_user, login_as, client)
    with app.app_context():
        skill, course = _make_course(is_daily_class=True)
        course_id = course.id

    res = client.post(f'/admin/api/courses/{course_id}/final-project', json={
        'title': 'Final Project',
        'rubric': [{'name': 'A', 'max_points': 30}, {'name': 'B', 'max_points': 30}],  # sums to 60
    })
    assert res.status_code == 400
    with app.app_context():
        assert ProjectTemplate.query.filter_by(course_id=course_id, is_final_project=True).first() is None


def test_empty_rubric_is_always_valid(app, client, make_user, login_as):
    """Not-configured-yet must never be blocked -- only a non-empty, wrong-summing rubric is."""
    _make_admin(make_user, login_as, client)
    with app.app_context():
        skill, _ = _make_course()
        template = ProjectTemplate(skill_id=skill.id, title='Empty Rubric Template', slug='empty-rubric-template')
        db.session.add(template)
        db.session.commit()
        template_id = template.id

    res = client.put(f'/admin/api/projects/{template_id}', json={'rubric': []})
    assert res.status_code == 200


# ===== Grade weight sum validation (AD-6) =====

def test_set_grade_weights_rejects_total_not_100_once_all_four_set(app, client, make_user, login_as):
    _make_admin(make_user, login_as, client)
    with app.app_context():
        _, course = _make_course(is_daily_class=True)
        course_id = course.id

    res = client.put(f'/admin/api/courses/{course_id}/grade-weights', json={
        'weights': {'assignments': 40, 'tests': 20, 'final_project': 20, 'participation': 10}  # sums to 90
    })
    assert res.status_code == 400

    with app.app_context():
        from app.models import GradeWeight
        assert GradeWeight.query.filter_by(course_id=course_id).count() == 0


def test_set_grade_weights_accepts_total_summing_to_100(app, client, make_user, login_as):
    _make_admin(make_user, login_as, client)
    with app.app_context():
        _, course = _make_course(is_daily_class=True)
        course_id = course.id

    res = client.put(f'/admin/api/courses/{course_id}/grade-weights', json={
        'weights': {'assignments': 40, 'tests': 25, 'final_project': 25, 'participation': 10}
    })
    assert res.status_code == 200


def test_set_grade_weights_allows_partial_configuration_mid_edit(app, client, make_user, login_as):
    """Not every component set yet -- must not be blocked, per GradeWeight's own
    'a partially-configured course is never blocked from saving' convention."""
    _make_admin(make_user, login_as, client)
    with app.app_context():
        _, course = _make_course(is_daily_class=True)
        course_id = course.id

    res = client.put(f'/admin/api/courses/{course_id}/grade-weights', json={
        'weights': {'assignments': 40}
    })
    assert res.status_code == 200


# ===== Quiz shape validation (AD-9) =====

def test_upsert_quiz_rejects_out_of_range_correct_index(app, client, make_user, login_as):
    _make_admin(make_user, login_as, client)
    with app.app_context():
        _, course = _make_course()
        module = CourseModule(course_id=course.id, title='Module', order=0)
        db.session.add(module)
        db.session.commit()
        lesson = Lesson(module_id=module.id, title='Lesson', slug='quiz-shape-lesson', order=0, is_published=True)
        db.session.add(lesson)
        db.session.commit()
        lesson_id = lesson.id

    res = client.put(f'/admin/api/lessons/{lesson_id}/quiz', json={
        'questions': [{'question': 'Q?', 'options': ['a', 'b'], 'correct_index': 5}]
    })
    assert res.status_code == 400


def test_upsert_quiz_rejects_non_list_options(app, client, make_user, login_as):
    _make_admin(make_user, login_as, client)
    with app.app_context():
        _, course = _make_course()
        module = CourseModule(course_id=course.id, title='Module', order=0)
        db.session.add(module)
        db.session.commit()
        lesson = Lesson(module_id=module.id, title='Lesson', slug='quiz-shape-lesson-2', order=0, is_published=True)
        db.session.add(lesson)
        db.session.commit()
        lesson_id = lesson.id

    res = client.put(f'/admin/api/lessons/{lesson_id}/quiz', json={
        'questions': [{'question': 'Q?', 'options': 'not-a-list', 'correct_index': 0}]
    })
    assert res.status_code == 400


def test_upsert_quiz_rejects_boolean_correct_index(app, client, make_user, login_as):
    """bool is a subclass of int in Python -- True/False must not silently pass as 1/0."""
    _make_admin(make_user, login_as, client)
    with app.app_context():
        _, course = _make_course()
        module = CourseModule(course_id=course.id, title='Module', order=0)
        db.session.add(module)
        db.session.commit()
        lesson = Lesson(module_id=module.id, title='Lesson', slug='quiz-shape-lesson-3', order=0, is_published=True)
        db.session.add(lesson)
        db.session.commit()
        lesson_id = lesson.id

    res = client.put(f'/admin/api/lessons/{lesson_id}/quiz', json={
        'questions': [{'question': 'Q?', 'options': ['a', 'b'], 'correct_index': True}]
    })
    assert res.status_code == 400


def test_upsert_quiz_accepts_valid_question(app, client, make_user, login_as):
    _make_admin(make_user, login_as, client)
    with app.app_context():
        _, course = _make_course()
        module = CourseModule(course_id=course.id, title='Module', order=0)
        db.session.add(module)
        db.session.commit()
        lesson = Lesson(module_id=module.id, title='Lesson', slug='quiz-shape-lesson-4', order=0, is_published=True)
        db.session.add(lesson)
        db.session.commit()
        lesson_id = lesson.id

    res = client.put(f'/admin/api/lessons/{lesson_id}/quiz', json={
        'questions': [{'question': 'Q?', 'options': ['a', 'b', 'c'], 'correct_index': 2}]
    })
    assert res.status_code == 200
