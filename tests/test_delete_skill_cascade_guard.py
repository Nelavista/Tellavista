"""Regression tests for delete_skill()'s new pre-delete reference checks
(routes/admin_skills_routes.py) -- Skill.courses/challenges/project_templates all
cascade='all, delete-orphan', which used to let deleting a Skill bypass delete_course()/
delete_challenge()/delete_project_template()'s own explicit checks entirely (those only
ever ran when their own route was hit directly), silently orphaning a StudentProject or
wiping a live cohort's enrollment history with zero warning.
"""
from datetime import datetime
from app.extensions import db
from app.models import (
    Skill, SkillCategory, SkillCourse, ProjectTemplate, StudentProject,
    Challenge, LearningPath, LearningPathStep, Cohort, CohortEnrollment,
)


def _make_admin(make_user, login_as, client, username='cascade_admin'):
    admin = make_user(username, is_admin=True)
    login_as(client, admin)
    return admin


def test_delete_skill_blocked_by_student_project_under_its_template(app, client, make_user, login_as):
    _make_admin(make_user, login_as, client)
    student = make_user('cascade_student1')
    with app.app_context():
        category = SkillCategory(name='CascadeCat1', slug='cascade-cat1', order=0)
        db.session.add(category)
        db.session.commit()
        skill = Skill(category_id=category.id, name='Cascade Skill 1', slug='cascade-skill1', is_published=True)
        db.session.add(skill)
        db.session.commit()
        template = ProjectTemplate(skill_id=skill.id, title='Cascade Template', slug='cascade-template')
        db.session.add(template)
        db.session.commit()
        db.session.add(StudentProject(student_id=student.id, project_template_id=template.id, title='My Project'))
        db.session.commit()
        skill_id, template_id = skill.id, template.id

    res = client.delete(f'/admin/api/skills/{skill_id}')
    assert res.status_code == 400

    with app.app_context():
        assert Skill.query.get(skill_id) is not None
        assert ProjectTemplate.query.get(template_id) is not None
        assert StudentProject.query.filter_by(project_template_id=template_id).first() is not None


def test_delete_skill_blocked_by_enrolled_cohort_under_its_course(app, client, make_user, login_as):
    _make_admin(make_user, login_as, client)
    student = make_user('cascade_student2')
    with app.app_context():
        category = SkillCategory(name='CascadeCat2', slug='cascade-cat2', order=0)
        db.session.add(category)
        db.session.commit()
        skill = Skill(category_id=category.id, name='Cascade Skill 2', slug='cascade-skill2', is_published=True)
        db.session.add(skill)
        db.session.commit()
        course = SkillCourse(skill_id=skill.id, title='Cascade Course', slug='cascade-course', order=0,
                              is_published=True, is_daily_class=True)
        db.session.add(course)
        db.session.commit()
        cohort = Cohort(course_id=course.id, name='Cascade Cohort', start_date=datetime.utcnow().date())
        db.session.add(cohort)
        db.session.commit()
        db.session.add(CohortEnrollment(cohort_id=cohort.id, student_id=student.id, current_day=3))
        db.session.commit()
        skill_id, course_id = skill.id, course.id

    res = client.delete(f'/admin/api/skills/{skill_id}')
    assert res.status_code == 400

    with app.app_context():
        assert Skill.query.get(skill_id) is not None
        assert SkillCourse.query.get(course_id) is not None
        assert CohortEnrollment.query.join(Cohort).filter(Cohort.course_id == course_id).count() == 1


def test_delete_course_directly_also_blocked_by_enrolled_cohort(app, client, make_user, login_as):
    """The same gap existed one level down -- delete_course() itself never checked
    Cohort/CohortEnrollment before this fix, only ProjectTemplate/LearningPathStep."""
    _make_admin(make_user, login_as, client)
    student = make_user('cascade_student3')
    with app.app_context():
        category = SkillCategory(name='CascadeCat3', slug='cascade-cat3', order=0)
        db.session.add(category)
        db.session.commit()
        skill = Skill(category_id=category.id, name='Cascade Skill 3', slug='cascade-skill3', is_published=True)
        db.session.add(skill)
        db.session.commit()
        course = SkillCourse(skill_id=skill.id, title='Direct Course', slug='direct-course', order=0,
                              is_published=True, is_daily_class=True)
        db.session.add(course)
        db.session.commit()
        cohort = Cohort(course_id=course.id, name='Direct Cohort', start_date=datetime.utcnow().date())
        db.session.add(cohort)
        db.session.commit()
        db.session.add(CohortEnrollment(cohort_id=cohort.id, student_id=student.id, current_day=1))
        db.session.commit()
        course_id = course.id

    res = client.delete(f'/admin/api/courses/{course_id}')
    assert res.status_code == 400
    with app.app_context():
        assert SkillCourse.query.get(course_id) is not None


def test_delete_skill_blocked_by_learning_path_step_referencing_its_challenge(app, client, make_user, login_as):
    _make_admin(make_user, login_as, client)
    with app.app_context():
        category = SkillCategory(name='CascadeCat4', slug='cascade-cat4', order=0)
        db.session.add(category)
        db.session.commit()
        skill = Skill(category_id=category.id, name='Cascade Skill 4', slug='cascade-skill4', is_published=True)
        db.session.add(skill)
        db.session.commit()
        challenge = Challenge(skill_id=skill.id, title='Cascade Challenge', slug='cascade-challenge')
        db.session.add(challenge)
        db.session.commit()
        path = LearningPath(skill_id=skill.id, title='Some Other Path')
        db.session.add(path)
        db.session.commit()
        db.session.add(LearningPathStep(path_id=path.id, order=0, step_type='challenge', title='Step',
                                         challenge_id=challenge.id))
        db.session.commit()
        skill_id = skill.id

    res = client.delete(f'/admin/api/skills/{skill_id}')
    assert res.status_code == 400
    with app.app_context():
        assert Skill.query.get(skill_id) is not None


def test_delete_skill_with_no_references_still_succeeds(app, client, make_user, login_as):
    """The guard must not false-positive on a skill nothing actually depends on."""
    _make_admin(make_user, login_as, client)
    with app.app_context():
        category = SkillCategory(name='CascadeCat5', slug='cascade-cat5', order=0)
        db.session.add(category)
        db.session.commit()
        skill = Skill(category_id=category.id, name='Clean Skill', slug='clean-skill', is_published=True)
        db.session.add(skill)
        db.session.commit()
        course = SkillCourse(skill_id=skill.id, title='Clean Course', slug='clean-course', order=0, is_published=True)
        db.session.add(course)
        challenge = Challenge(skill_id=skill.id, title='Clean Challenge', slug='clean-challenge')
        db.session.add(challenge)
        template = ProjectTemplate(skill_id=skill.id, title='Clean Template', slug='clean-template')
        db.session.add(template)
        db.session.commit()
        skill_id = skill.id

    res = client.delete(f'/admin/api/skills/{skill_id}')
    assert res.status_code == 200
    with app.app_context():
        assert Skill.query.get(skill_id) is None
