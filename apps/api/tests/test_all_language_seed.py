from __future__ import annotations

from sqlalchemy import func, select

from app.models.skills import (
    CareerTrack,
    CareerTrackStep,
    Lesson,
    Skill,
    SkillCategory,
    TaskTemplate,
)
from app.models.verification import Assessment, AssessmentTask
from app.seed import all_language
from app.seed.all_skills import CATEGORIES, SKILLS, TRACKS
from app.services.skills.tasks import validate


def test_all_catalogue_has_the_complete_v2_shape(db) -> None:
    all_language.run(db)
    db.flush()

    assert db.scalar(
        select(func.count(SkillCategory.id)).where(SkillCategory.program == all_language.PROGRAM)
    ) == len(CATEGORIES) == 9
    assert db.scalar(
        select(func.count(Skill.id))
        .join(SkillCategory, SkillCategory.id == Skill.category_id)
        .where(SkillCategory.program == all_language.PROGRAM)
    ) == len(SKILLS) == 94
    assert db.scalar(
        select(func.count(CareerTrack.id)).where(CareerTrack.program == all_language.PROGRAM)
    ) == len(TRACKS) == 10

    for spec in SKILLS:
        skill = db.scalar(select(Skill).where(Skill.slug == spec["slug"]))
        assert skill is not None
        assert skill.language == spec.get("language")
        assert skill.tags == spec.get("tags", [])
        assert db.scalar(select(func.count(Lesson.id)).where(Lesson.skill_id == skill.id)) == len(
            spec["lessons"]
        )
        template = db.scalar(
            select(TaskTemplate).where(TaskTemplate.slug == f"{skill.slug}-practice")
        )
        assert template is not None
        assert template.status == "published"
        assert template.validator == all_language.VALIDATOR
        assessment = db.scalar(
            select(Assessment).where(Assessment.slug == f"{skill.slug}-assessment")
        )
        assert assessment is not None
        task = db.scalar(
            select(AssessmentTask).where(AssessmentTask.assessment_id == assessment.id)
        )
        assert task is not None
        result = validate(
            template.validator,
            task.expected_answer,
            task.expected_answer,
            template.config,
        )
        assert result.is_correct

    for track_spec in TRACKS:
        track = db.scalar(select(CareerTrack).where(CareerTrack.slug == track_spec["slug"]))
        assert track is not None
        steps = list(
            db.scalars(
                select(CareerTrackStep)
                .where(CareerTrackStep.track_id == track.id)
                .order_by(CareerTrackStep.ordinal)
            )
        )
        assert [step.skill_id for step in steps] == [
            db.scalar(select(Skill.id).where(Skill.slug == slug)) for slug in track_spec["skills"]
        ]


def test_all_catalogue_seed_is_idempotent(db) -> None:
    all_language.run(db)
    db.flush()
    before = (
        db.scalar(select(func.count(Skill.id))),
        db.scalar(select(func.count(Lesson.id))),
        db.scalar(select(func.count(CareerTrack.id))),
        db.scalar(select(func.count(Assessment.id))),
    )
    all_language.run(db)
    db.flush()
    after = (
        db.scalar(select(func.count(Skill.id))),
        db.scalar(select(func.count(Lesson.id))),
        db.scalar(select(func.count(CareerTrack.id))),
        db.scalar(select(func.count(Assessment.id))),
    )
    assert after == before
