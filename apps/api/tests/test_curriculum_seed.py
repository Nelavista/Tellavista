"""The F7 curriculum is data, so the test checks the data is complete and true.

Two things matter beyond "rows exist": every gold task must validate against its
own template (a wrong offset in a span is a broken assessment), and re-running the
seed must change nothing. The second is what makes it safe in local/dev.
"""
from __future__ import annotations

from sqlalchemy import func, select

from app.models.academia import (
    Course,
    Department,
    Faculty,
    Material,
    MaterialChunk,
    Question,
    Topic,
    University,
)
from app.models.skills import (
    STATUS_PUBLISHED,
    LearningPath,
    LearningPathStep,
    Lesson,
    Skill,
    TaskTemplate,
)
from app.models.verification import Assessment, AssessmentTask, PracticalTask
from app.seed import curriculum
from app.services.skills.tasks import validate


def _department(db) -> int:
    university = University(name="Test University", slug="test-university")
    db.add(university)
    db.flush()
    faculty = Faculty(university_id=university.id, name="Science")
    db.add(faculty)
    db.flush()
    department = Department(faculty_id=faculty.id, name="Computer Science")
    db.add(department)
    db.flush()
    return department.id


def test_curriculum_is_complete_and_every_gold_task_validates(db) -> None:
    department_id = _department(db)
    counts = curriculum.run(db, department_id)
    db.flush()

    assert counts["skills"] == 1
    assert counts["lessons"] == len(curriculum.LESSONS)
    assert counts["task_templates"] == len(curriculum.TEMPLATES)
    assert counts["learning_paths"] == 1
    assert counts["assessments"] == 1
    assert counts["practical_tasks"] == 1

    skill = db.scalar(select(Skill).where(Skill.slug == curriculum.SKILL_SLUG))
    assert skill is not None and skill.is_active

    lessons = list(db.scalars(select(Lesson).where(Lesson.skill_id == skill.id)))
    assert len(lessons) == len(curriculum.LESSONS)
    assert all(row.status == STATUS_PUBLISHED for row in lessons)
    assert all(row.body_md.strip() for row in lessons)

    templates = {
        row.slug: row
        for row in db.scalars(select(TaskTemplate).where(TaskTemplate.skill_id == skill.id))
    }
    assert set(templates) == {spec["slug"] for spec in curriculum.TEMPLATES}
    for template in templates.values():
        assert template.status == STATUS_PUBLISHED
        # Practice is only usable when a sample and its expected answer exist.
        assert isinstance(template.config, dict)
        assert template.config.get("sample")
        assert isinstance(template.config.get("expected_answer"), dict)

    path = db.scalar(select(LearningPath).where(LearningPath.slug == curriculum.PATH_SLUG))
    assert path is not None and path.status == STATUS_PUBLISHED
    steps = list(
        db.scalars(
            select(LearningPathStep)
            .where(LearningPathStep.path_id == path.id)
            .order_by(LearningPathStep.ordinal)
        )
    )
    assert [step.ordinal for step in steps] == list(range(1, len(steps) + 1))
    assert any(step.kind == "lesson" and step.lesson_id for step in steps)
    assert any(step.kind == "practice" and step.task_template_id for step in steps)
    assert any(step.kind == "assessment" for step in steps)

    assessment = db.scalar(
        select(Assessment).where(Assessment.slug == curriculum.ASSESSMENT_SLUG)
    )
    assert assessment is not None and assessment.status == STATUS_PUBLISHED
    assert assessment.pass_threshold == 80
    assert assessment.task_count == len(curriculum.ASSESSMENT_TASKS)

    tasks = list(
        db.scalars(
            select(AssessmentTask)
            .where(AssessmentTask.assessment_id == assessment.id)
            .order_by(AssessmentTask.ordinal)
        )
    )
    assert len(tasks) == len(curriculum.ASSESSMENT_TASKS)
    for task in tasks:
        template = db.get(TaskTemplate, task.template_id)
        assert template is not None
        result = validate(
            template.validator,
            task.expected_answer,
            task.expected_answer,
            template.config or {},
        )
        assert result.is_correct, f"assessment task {task.ordinal} does not validate: {result.feedback}"
        assert task.payload
        assert task.expected_answer

    practical = db.scalar(select(PracticalTask).where(PracticalTask.slug == curriculum.PRACTICAL_SLUG))
    assert practical is not None and practical.status == STATUS_PUBLISHED
    assert isinstance(practical.rubric, list) and len(practical.rubric) >= 3
    assert sum(int(row["weight"]) for row in practical.rubric) == 100


def test_curriculum_course_has_searchable_content_and_questions(db) -> None:
    department_id = _department(db)
    curriculum.run(db, department_id)
    db.flush()

    course = db.scalar(
        select(Course).where(Course.code == curriculum.COURSE_CODE, Course.level == "300")
    )
    assert course is not None

    topics = list(db.scalars(select(Topic).where(Topic.course_id == course.id)))
    assert len(topics) == len(curriculum.TOPICS)

    materials = list(db.scalars(select(Material).where(Material.course_id == course.id)))
    assert len(materials) == len(curriculum.MATERIALS)
    chunks = db.scalar(
        select(func.count(MaterialChunk.id))
        .join(Material, Material.id == MaterialChunk.material_id)
        .where(Material.course_id == course.id)
    )
    assert chunks == sum(len(spec["chunks"]) for spec in curriculum.MATERIALS)

    questions = list(db.scalars(select(Question).where(Question.course_id == course.id)))
    assert len(questions) == len(curriculum.QUESTIONS)
    for question in questions:
        assert question.is_active
        keys = {str(option["key"]) for option in question.options}
        assert question.correct_key in keys
        assert question.explanation


def test_re_running_the_seed_changes_nothing(db) -> None:
    department_id = _department(db)
    first = curriculum.run(db, department_id)
    db.flush()
    second = curriculum.run(db, department_id)
    db.flush()

    assert any(value > 0 for value in first.values())
    assert all(value == 0 for value in second.values())
