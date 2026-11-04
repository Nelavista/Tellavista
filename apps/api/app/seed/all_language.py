"""Seed the African Languages Lab into the V2 curriculum tables.

The catalogue is kept as data in ``app.seed.all_skills`` and is converted into
V2's existing skills, learning paths, task templates and assessment tables. This
module is deliberately separate from the V1 seeder: V2 owns the rows it creates
and can rerun this seed safely.
"""
from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.skills import (
    STATUS_PUBLISHED,
    CareerTrack,
    CareerTrackStep,
    LearningPath,
    LearningPathStep,
    Lesson,
    Skill,
    SkillCategory,
    TaskTemplate,
)
from app.models.verification import Assessment, AssessmentTask
from app.seed.all_skills import CATEGORIES, SKILLS, TRACKS

PROGRAM = "all"
VALIDATOR = "all_language_task"


def _expected_answer(spec: dict[str, Any]) -> dict[str, Any]:
    kind = spec["kind"]
    if kind == "labeling":
        responses: dict[str, dict[str, Any]] = {}
        for item in spec.get("items", []):
            responses[item["id"]] = {
                field["name"]: field["expected"] for field in item.get("fields", [])
            }
        return {"responses": responses}
    if kind == "transcription":
        return {"responses": {item["id"]: item["reference"] for item in spec.get("segments", [])}}
    if kind == "translation":
        return {"responses": {item["id"]: item["references"][0] for item in spec.get("items", [])}}
    if kind == "recording":
        requirements = spec.get("requirements", {})
        return {
            "responses": {
                item["id"]: {
                    "duration_seconds": requirements.get("min_seconds", 1.5),
                    "clip_pct": 0,
                    "rms_db": requirements.get("min_rms_db", -40),
                    "silence_pct": 0,
                }
                for item in spec.get("prompts", [])
            }
        }
    raise ValueError(f"Unsupported ALL task kind: {kind}")


def _category(db: Session, spec: dict[str, Any]) -> SkillCategory:
    row = db.scalar(select(SkillCategory).where(SkillCategory.slug == spec["slug"]))
    if row is None:
        row = SkillCategory(
            slug=spec["slug"],
            name=spec["name"],
            description=spec.get("description"),
            ordinal=spec.get("order", 0),
            program=PROGRAM,
        )
        db.add(row)
        db.flush()
    else:
        row.name = spec["name"]
        row.description = spec.get("description")
        row.ordinal = spec.get("order", 0)
        row.program = PROGRAM
    return row


def _skill(db: Session, spec: dict[str, Any], category: SkillCategory) -> Skill:
    row = db.scalar(select(Skill).where(Skill.slug == spec["slug"]))
    if row is None:
        row = Skill(
            slug=spec["slug"],
            name=spec["name"],
            description=spec.get("description") or spec.get("tagline"),
            category_id=category.id,
            language=spec.get("language"),
            tags=spec.get("tags", []),
            is_active=True,
        )
        db.add(row)
        db.flush()
    else:
        row.name = spec["name"]
        row.description = spec.get("description") or spec.get("tagline")
        row.category_id = category.id
        row.language = spec.get("language")
        row.tags = spec.get("tags", [])
        row.is_active = True
    return row


def _content(
    db: Session, skill: Skill, spec: dict[str, Any]
) -> tuple[LearningPath, int, int, int, int]:
    lesson_rows: list[Lesson] = []
    created_lessons = 0
    for ordinal, lesson_spec in enumerate(spec["lessons"], start=1):
        slug = f"{skill.slug}-lesson-{ordinal}"
        row = db.scalar(select(Lesson).where(Lesson.slug == slug))
        if row is None:
            row = Lesson(
                skill_id=skill.id,
                slug=slug,
                title=lesson_spec["title"],
                body_md=lesson_spec["content"],
                estimated_minutes=lesson_spec.get("minutes"),
                status=STATUS_PUBLISHED,
            )
            db.add(row)
            db.flush()
            created_lessons += 1
        else:
            row.skill_id = skill.id
            row.title = lesson_spec["title"]
            row.body_md = lesson_spec["content"]
            row.estimated_minutes = lesson_spec.get("minutes")
            row.status = STATUS_PUBLISHED
        lesson_rows.append(row)

    task_spec = spec["practice"]["spec"]
    template_slug = f"{skill.slug}-practice"
    template = db.scalar(select(TaskTemplate).where(TaskTemplate.slug == template_slug))
    expected = _expected_answer(task_spec)
    if template is None:
        template = TaskTemplate(
            skill_id=skill.id,
            slug=template_slug,
            name=spec["practice"]["title"],
            instructions_md=spec["practice"]["instructions"],
            input_schema={"type": "object", "task_spec": task_spec},
            answer_schema={"type": "object", "properties": {"responses": {"type": "object"}}},
            validator=VALIDATOR,
            config={
                "task_kind": task_spec["kind"],
                "expected_answer": expected,
                "requirements": task_spec.get("requirements", {}),
            },
            status=STATUS_PUBLISHED,
        )
        db.add(template)
        db.flush()
        created_templates = 1
    else:
        template.skill_id = skill.id
        template.name = spec["practice"]["title"]
        template.instructions_md = spec["practice"]["instructions"]
        template.input_schema = {"type": "object", "task_spec": task_spec}
        template.answer_schema = {"type": "object", "properties": {"responses": {"type": "object"}}}
        template.validator = VALIDATOR
        template.config = {
            "task_kind": task_spec["kind"],
            "expected_answer": expected,
            "requirements": task_spec.get("requirements", {}),
        }
        template.status = STATUS_PUBLISHED
        created_templates = 0

    path_slug = f"{skill.slug}-path"
    path = db.scalar(select(LearningPath).where(LearningPath.slug == path_slug))
    if path is None:
        path = LearningPath(
            skill_id=skill.id,
            slug=path_slug,
            title=f"{spec['name']} learning path",
            summary=spec.get("tagline") or spec.get("description"),
            level=spec["level"],
            estimated_hours=spec.get("estimated_hours"),
            status=STATUS_PUBLISHED,
        )
        db.add(path)
        db.flush()
        created_path = 1
    else:
        path.skill_id = skill.id
        path.title = f"{spec['name']} learning path"
        path.summary = spec.get("tagline") or spec.get("description")
        path.level = spec["level"]
        path.estimated_hours = spec.get("estimated_hours")
        path.status = STATUS_PUBLISHED
        created_path = 0

    existing_steps = list(
        db.scalars(
            select(LearningPathStep)
            .where(LearningPathStep.path_id == path.id)
            .order_by(LearningPathStep.ordinal)
        )
    )
    if not existing_steps:
        for ordinal, lesson in enumerate(lesson_rows, start=1):
            db.add(
                LearningPathStep(
                    path_id=path.id,
                    ordinal=ordinal,
                    kind="lesson",
                    title=lesson.title,
                    lesson_id=lesson.id,
                )
            )
        db.add(
            LearningPathStep(
                path_id=path.id,
                ordinal=len(lesson_rows) + 1,
                kind="practice",
                title=spec["practice"]["title"],
                task_template_id=template.id,
            )
        )
        db.add(
            LearningPathStep(
                path_id=path.id,
                ordinal=len(lesson_rows) + 2,
                kind="assessment",
                title=spec["assessment"]["title"],
            )
        )
        db.flush()

    assessment_slug = f"{skill.slug}-assessment"
    assessment = db.scalar(select(Assessment).where(Assessment.slug == assessment_slug))
    if assessment is None:
        assessment = Assessment(
            skill_id=skill.id,
            slug=assessment_slug,
            title=spec["assessment"]["title"],
            pass_threshold=spec["assessment"].get("pass_score", 70),
            max_attempts=3,
            task_count=1,
            status=STATUS_PUBLISHED,
        )
        db.add(assessment)
        db.flush()
        db.add(
            AssessmentTask(
                assessment_id=assessment.id,
                ordinal=1,
                template_id=template.id,
                payload={"task_spec": spec["assessment"]["spec"]},
                expected_answer=_expected_answer(spec["assessment"]["spec"]),
                points=1,
            )
        )
        db.flush()
        created_assessment = 1
    else:
        assessment.skill_id = skill.id
        assessment.title = spec["assessment"]["title"]
        assessment.pass_threshold = spec["assessment"].get("pass_score", 70)
        assessment.status = STATUS_PUBLISHED
        created_assessment = 0

    return path, created_lessons, created_templates, created_path, created_assessment


def _tracks(db: Session, skill_ids: dict[str, int]) -> int:
    created = 0
    for spec in TRACKS:
        row = db.scalar(select(CareerTrack).where(CareerTrack.slug == spec["slug"]))
        if row is None:
            row = CareerTrack(
                slug=spec["slug"],
                title=spec["title"],
                tagline=spec.get("tagline"),
                icon=spec.get("icon"),
                color=spec.get("color"),
                program=PROGRAM,
                status=STATUS_PUBLISHED,
            )
            db.add(row)
            db.flush()
            created += 1
        else:
            row.title = spec["title"]
            row.tagline = spec.get("tagline")
            row.icon = spec.get("icon")
            row.color = spec.get("color")
            row.program = PROGRAM
            row.status = STATUS_PUBLISHED
        if db.scalar(select(CareerTrackStep.id).where(CareerTrackStep.track_id == row.id)) is None:
            for ordinal, slug in enumerate(spec["skills"], start=1):
                db.add(CareerTrackStep(track_id=row.id, skill_id=skill_ids[slug], ordinal=ordinal))
            db.flush()
    return created


def run(db: Session) -> dict[str, int]:
    """Upsert the complete ALL catalogue and return rows created in this run."""
    categories = {_spec["slug"]: _category(db, _spec) for _spec in CATEGORIES}
    skill_ids: dict[str, int] = {}
    counts = {
        "categories": len(CATEGORIES),
        "skills": 0,
        "lessons": 0,
        "task_templates": 0,
        "learning_paths": 0,
        "assessments": 0,
        "tracks": 0,
        "track_steps": sum(len(track["skills"]) for track in TRACKS),
    }
    for spec in SKILLS:
        skill = _skill(db, spec, categories[spec["category"]])
        skill_ids[skill.slug] = skill.id
        _, lessons, templates, created_path, created_assessment = _content(db, skill, spec)
        counts["skills"] += 1
        counts["lessons"] += lessons
        counts["task_templates"] += templates
        counts["learning_paths"] += created_path
        counts["assessments"] += created_assessment
    counts["tracks"] = _tracks(db, skill_ids)
    return counts
