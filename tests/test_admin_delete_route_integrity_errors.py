"""Regression tests for 5 admin "delete" routes that used to either crash with an
unhandled IntegrityError -> 500, or (for 3 of the 5) silently succeed while corrupting
data: no ForeignKey in models.py (or any migration) sets ondelete=, so a raw DB-level
delete would raise IntegrityError under Postgres's default ON DELETE NO ACTION -- but
for any referencing column that (a) is nullable and (b) has a `db.relationship()`
declared with a backref (ProjectTemplate.course, StudentProject.template, Material.course,
Material.topic), SQLAlchemy's default no-cascade behavior intervenes first and silently
sets that column to NULL instead of ever letting the delete reach the database, so an
`except IntegrityError` alone -- which is what these routes originally got -- would
never even fire for those three. The real fix is an explicit pre-delete existence check,
not error-catching:
- admin_skills_routes.py: delete_course (Skills/SkillCourse), delete_challenge,
  delete_project_template
- admin_academia_routes.py: delete_course (Academia/Course), delete_topic
"""
from extensions import db
from models import (
    SkillCategory, Skill, SkillCourse, Challenge, ChallengeSubmission,
    ProjectTemplate, StudentProject, University, Faculty, Department, Course, Topic,
    Material, TopicProgress,
)


def _make_admin(make_user, login_as, client, username):
    admin = make_user(username, is_admin=True)
    login_as(client, admin)
    return admin


def test_delete_skills_course_blocked_by_project_template_returns_friendly_400(app, client, make_user, login_as):
    admin = _make_admin(make_user, login_as, client, 'del_course_admin')
    with app.app_context():
        category = SkillCategory(name='DelCourseCat', slug='del-course-cat', order=0)
        db.session.add(category)
        db.session.commit()
        skill = Skill(category_id=category.id, name='Del Course Skill', slug='del-course-skill', is_published=True)
        db.session.add(skill)
        db.session.commit()
        course = SkillCourse(skill_id=skill.id, title='Del Course', slug='del-course', order=0, is_published=True)
        db.session.add(course)
        db.session.commit()
        template = ProjectTemplate(skill_id=skill.id, course_id=course.id, title='T', slug='t')
        db.session.add(template)
        db.session.commit()
        course_id = course.id

    res = client.delete(f'/admin/api/courses/{course_id}')
    assert res.status_code == 400
    data = res.get_json()
    assert data['success'] is False
    assert 'course' in data['error'].lower()

    with app.app_context():
        assert SkillCourse.query.get(course_id) is not None  # not partially deleted


def test_delete_challenge_blocked_by_submission_returns_friendly_400(app, client, make_user, login_as):
    admin = _make_admin(make_user, login_as, client, 'del_challenge_admin')
    student = make_user('del_challenge_student')
    with app.app_context():
        category = SkillCategory(name='DelChalCat', slug='del-chal-cat', order=0)
        db.session.add(category)
        db.session.commit()
        skill = Skill(category_id=category.id, name='Del Chal Skill', slug='del-chal-skill', is_published=True)
        db.session.add(skill)
        db.session.commit()
        challenge = Challenge(skill_id=skill.id, title='Del Challenge', slug='del-challenge')
        db.session.add(challenge)
        db.session.commit()
        db.session.add(ChallengeSubmission(challenge_id=challenge.id, student_id=student.id, content='my solution'))
        db.session.commit()
        challenge_id = challenge.id

    res = client.delete(f'/admin/api/challenges/{challenge_id}')
    assert res.status_code == 400
    assert res.get_json()['success'] is False

    with app.app_context():
        assert Challenge.query.get(challenge_id) is not None


def test_delete_project_template_blocked_by_student_project_returns_friendly_400(app, client, make_user, login_as):
    admin = _make_admin(make_user, login_as, client, 'del_template_admin')
    student = make_user('del_template_student')
    with app.app_context():
        category = SkillCategory(name='DelTplCat', slug='del-tpl-cat', order=0)
        db.session.add(category)
        db.session.commit()
        skill = Skill(category_id=category.id, name='Del Tpl Skill', slug='del-tpl-skill', is_published=True)
        db.session.add(skill)
        db.session.commit()
        template = ProjectTemplate(skill_id=skill.id, title='Del Template', slug='del-template')
        db.session.add(template)
        db.session.commit()
        db.session.add(StudentProject(student_id=student.id, project_template_id=template.id, title='My Project'))
        db.session.commit()
        template_id = template.id

    res = client.delete(f'/admin/api/projects/{template_id}')
    assert res.status_code == 400
    assert res.get_json()['success'] is False

    with app.app_context():
        assert ProjectTemplate.query.get(template_id) is not None


def test_delete_project_template_with_no_references_still_succeeds(app, client, make_user, login_as):
    """The guard must not false-positive on a template nothing actually references --
    same setup as the blocked test above, minus the StudentProject row."""
    admin = _make_admin(make_user, login_as, client, 'del_template_clean_admin')
    with app.app_context():
        category = SkillCategory(name='DelTplCleanCat', slug='del-tpl-clean-cat', order=0)
        db.session.add(category)
        db.session.commit()
        skill = Skill(category_id=category.id, name='Del Tpl Clean Skill', slug='del-tpl-clean-skill', is_published=True)
        db.session.add(skill)
        db.session.commit()
        template = ProjectTemplate(skill_id=skill.id, title='Del Template Clean', slug='del-template-clean')
        db.session.add(template)
        db.session.commit()
        template_id = template.id

    res = client.delete(f'/admin/api/projects/{template_id}')
    assert res.status_code == 200
    assert res.get_json()['success'] is True

    with app.app_context():
        assert ProjectTemplate.query.get(template_id) is None


def test_delete_academia_course_blocked_by_material_returns_friendly_400(app, client, make_user, login_as):
    admin = _make_admin(make_user, login_as, client, 'del_acad_course_admin')
    with app.app_context():
        uni = University(name='Del Course University')
        db.session.add(uni)
        db.session.flush()
        fac = Faculty(university_id=uni.id, name='Science')
        db.session.add(fac)
        db.session.flush()
        dept = Department(faculty_id=fac.id, name='Del Course Dept')
        db.session.add(dept)
        db.session.flush()
        course = Course(department_id=dept.id, code='DEL101', title='Del Course', level='100')
        db.session.add(course)
        db.session.commit()
        db.session.add(Material(title='Linked Material', department='Del Course Dept', level='100',
                                 semester='First Semester', course_id=course.id, is_approved=True))
        db.session.commit()
        course_id = course.id

    res = client.delete(f'/admin/academia/courses/{course_id}/delete')
    assert res.status_code == 400
    assert res.get_json()['success'] is False

    with app.app_context():
        assert Course.query.get(course_id) is not None


def test_delete_topic_blocked_by_topic_progress_returns_friendly_400(app, client, make_user, login_as):
    admin = _make_admin(make_user, login_as, client, 'del_topic_admin')
    student = make_user('del_topic_student')
    with app.app_context():
        uni = University(name='Del Topic University')
        db.session.add(uni)
        db.session.flush()
        fac = Faculty(university_id=uni.id, name='Science')
        db.session.add(fac)
        db.session.flush()
        dept = Department(faculty_id=fac.id, name='Del Topic Dept')
        db.session.add(dept)
        db.session.flush()
        course = Course(department_id=dept.id, code='DEL102', title='Del Topic Course', level='100')
        db.session.add(course)
        db.session.commit()
        topic = Topic(course_id=course.id, title='Del Topic', is_active=True)
        db.session.add(topic)
        db.session.commit()
        db.session.add(TopicProgress(user_id=student.id, topic_id=topic.id))
        db.session.commit()
        topic_id = topic.id

    res = client.delete(f'/admin/academia/topics/{topic_id}/delete')
    assert res.status_code == 400
    assert res.get_json()['success'] is False

    with app.app_context():
        assert Topic.query.get(topic_id) is not None
