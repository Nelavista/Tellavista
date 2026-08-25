"""Skills verification must require an actual review, never just the student's own
'completed' status flag -- this is the fix for the audit's most severe Skills finding
(the 'Verified' badge shown to employers was previously earnable by self-declaration
alone).
"""
from datetime import datetime
from extensions import db
from models import Skill, SkillCategory, SkillCourse, CourseModule, Lesson, StudentSkill, ProjectTemplate, StudentProject
from services.skills_service import is_skill_verified, recompute_student_skill


def _make_completed_skill_with_one_lesson(app, student_id, skill_slug='web-development'):
    """Sets up a Skill with exactly one published lesson, and marks the student as having
    completed that lesson (and therefore the whole skill, per recompute_student_skill's
    100%-of-lessons rule) -- the minimum setup for StudentSkill.status == 'completed'."""
    with app.app_context():
        category = SkillCategory(name='Tech', slug='tech', order=0)
        db.session.add(category)
        db.session.commit()

        skill = Skill(category_id=category.id, name='Web Development', slug=skill_slug, is_published=True)
        db.session.add(skill)
        db.session.commit()

        course = SkillCourse(skill_id=skill.id, title='Web Dev 101', slug='web-dev-101', order=0, is_published=True)
        db.session.add(course)
        db.session.commit()

        module = CourseModule(course_id=course.id, title='Module 1', order=0)
        db.session.add(module)
        db.session.commit()

        lesson = Lesson(module_id=module.id, title='Lesson 1', slug='lesson-1', order=0, is_published=True, duration_minutes=10)
        db.session.add(lesson)
        db.session.commit()

        from models import StudentLessonProgress
        db.session.add(StudentLessonProgress(student_id=student_id, lesson_id=lesson.id))
        db.session.commit()

        recompute_student_skill(student_id, skill.id)
        return skill.id


def _make_project_template(app, skill_id):
    with app.app_context():
        template = ProjectTemplate(skill_id=skill_id, title='Portfolio Site', slug='portfolio-site', is_published=True)
        db.session.add(template)
        db.session.commit()
        return template.id


def test_self_completed_project_alone_does_not_verify(app, make_user):
    """The core red-team scenario: a student marks their own project 'completed' with no
    review of any kind. is_skill_verified must return False."""
    user = make_user('skills_selfclaim')
    skill_id = _make_completed_skill_with_one_lesson(app, user.id)
    template_id = _make_project_template(app, skill_id)

    with app.app_context():
        project = StudentProject(
            student_id=user.id, project_template_id=template_id, title='My portfolio',
            status='completed', completed_at=datetime.utcnow(),
            # Deliberately NO verification_status/ai_feedback/ai_overall_score set --
            # this is exactly the student-self-declares-completion path.
        )
        db.session.add(project)
        db.session.commit()

        assert is_skill_verified(user.id, skill_id) is False


def test_reviewed_with_passing_score_verifies(app, make_user):
    """A project that actually went through AI review (verification_status='reviewed')
    and scored at/above the bar DOES count."""
    user = make_user('skills_reviewed_pass')
    skill_id = _make_completed_skill_with_one_lesson(app, user.id)
    template_id = _make_project_template(app, skill_id)

    with app.app_context():
        project = StudentProject(
            student_id=user.id, project_template_id=template_id, title='My portfolio',
            status='completed', completed_at=datetime.utcnow(),
            verification_status='reviewed',
        )
        project.ai_feedback = {'score': 75, 'strengths': ['clean layout'], 'improvements': [], 'explanation': 'solid', 'next_step': 'add tests'}
        db.session.add(project)
        db.session.commit()

        assert is_skill_verified(user.id, skill_id) is True


def test_reviewed_with_failing_score_does_not_verify(app, make_user):
    """A project that WAS reviewed but scored below the bar must not count -- being
    looked at is not the same as passing."""
    user = make_user('skills_reviewed_fail')
    skill_id = _make_completed_skill_with_one_lesson(app, user.id)
    template_id = _make_project_template(app, skill_id)

    with app.app_context():
        project = StudentProject(
            student_id=user.id, project_template_id=template_id, title='Half-finished thing',
            status='completed', completed_at=datetime.utcnow(),
            verification_status='reviewed',
        )
        project.ai_feedback = {'score': 25, 'strengths': [], 'improvements': ['finish it'], 'explanation': 'incomplete', 'next_step': 'finish'}
        db.session.add(project)
        db.session.commit()

        assert is_skill_verified(user.id, skill_id) is False


def test_final_project_rubric_score_also_counts(app, make_user):
    """The OTHER review path -- a daily-class final project graded via
    evaluate_final_project's rubric (ai_overall_score), never touching
    verification_status at all -- must also be honored, not just the ordinary
    'Request Review' path."""
    user = make_user('skills_rubric_pass')
    skill_id = _make_completed_skill_with_one_lesson(app, user.id)
    template_id = _make_project_template(app, skill_id)

    with app.app_context():
        project = StudentProject(
            student_id=user.id, project_template_id=template_id, title='Final Project',
            status='completed', completed_at=datetime.utcnow(),
            ai_overall_score=82,  # rubric-graded, verification_status stays 'none'
        )
        db.session.add(project)
        db.session.commit()

        assert is_skill_verified(user.id, skill_id) is True


def test_verification_requires_completed_project_status_too(app, make_user):
    """A project with a great review score that's still 'in_progress' (not marked
    completed by the student) must not verify -- review score alone isn't enough either."""
    user = make_user('skills_inprogress')
    skill_id = _make_completed_skill_with_one_lesson(app, user.id)
    template_id = _make_project_template(app, skill_id)

    with app.app_context():
        project = StudentProject(
            student_id=user.id, project_template_id=template_id, title='WIP',
            status='in_progress', verification_status='reviewed',
        )
        project.ai_feedback = {'score': 90}
        db.session.add(project)
        db.session.commit()

        assert is_skill_verified(user.id, skill_id) is False
