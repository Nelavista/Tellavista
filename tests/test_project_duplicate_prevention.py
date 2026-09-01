"""Regression test for the P1 fix: StudentProject had no defense against a double-click
(or slow-network retry) on 'Start Project' creating two independent project rows for the
same student+template. Fixed with a DB-level unique constraint on
(student_id, project_template_id) (see models.py's StudentProject.__table_args__ and
migrations/versions/c4a9f2e871b3_add_student_project_unique_constraint.py) plus an
IntegrityError catch in start_project() (routes/skills_routes.py) that redirects to the
winning row instead of crashing.
"""
import pytest
from sqlalchemy.exc import IntegrityError
from extensions import db
from models import SkillCategory, Skill, ProjectTemplate, StudentProject


@pytest.fixture
def template(app):
    with app.app_context():
        cat = SkillCategory(name='Tech', slug='tech-dup-test')
        db.session.add(cat)
        db.session.flush()
        skill = Skill(category_id=cat.id, name='Web Dev', slug='web-dev-dup-test', is_published=True)
        db.session.add(skill)
        db.session.flush()
        tpl = ProjectTemplate(skill_id=skill.id, title='Portfolio Site', slug='portfolio-dup-test', is_published=True)
        db.session.add(tpl)
        db.session.commit()
        return tpl.id


def test_start_project_twice_reuses_existing_row(app, client, make_user, login_as, template):
    user = make_user('dup_click_student')
    login_as(client, user)

    res1 = client.post(f'/skills/projects/start/{template}', follow_redirects=False)
    assert res1.status_code == 302
    res2 = client.post(f'/skills/projects/start/{template}', follow_redirects=False)
    assert res2.status_code == 302
    assert res1.headers['Location'] == res2.headers['Location']

    with app.app_context():
        count = StudentProject.query.filter_by(project_template_id=template).count()
        assert count == 1


def test_database_rejects_duplicate_student_template_pair(app, make_user, template):
    """The actual safety net for a true race (two requests committing at nearly the same
    instant, both past the app-level check) -- proves the constraint is real and active,
    not just declared in the model."""
    user = make_user('race_student')
    with app.app_context():
        db.session.add(StudentProject(student_id=user.id, project_template_id=template, title='A', source='template'))
        db.session.commit()

        db.session.add(StudentProject(student_id=user.id, project_template_id=template, title='B', source='template'))
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()


def test_custom_projects_are_not_constrained_by_null_template_id(app, make_user):
    """project_template_id is NULL for custom/AI-generated projects -- the unique
    constraint must never block a student from having more than one of those."""
    user = make_user('custom_project_student')
    with app.app_context():
        db.session.add(StudentProject(student_id=user.id, project_template_id=None, title='Custom 1', source='custom'))
        db.session.add(StudentProject(student_id=user.id, project_template_id=None, title='Custom 2', source='custom'))
        db.session.commit()  # must not raise
        count = StudentProject.query.filter_by(student_id=user.id).count()
        assert count == 2
