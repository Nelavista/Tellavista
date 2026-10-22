"""Phase 2 — the learn and practise stages, with honest progress.

Completing a lesson is progress, never proof: it writes a `learned` transcript line
and leaves verification alone. Path order is enforced so "next" means next, and a
practice answer is validated against configuration rather than a hard-coded type.
"""
from __future__ import annotations

import pytest
from factories import make_skill, make_template, make_user, unique
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.skills import (
    STATUS_PUBLISHED,
    LearningPath,
    LearningPathStep,
    Lesson,
    LessonProgress,
)
from app.models.verification import TranscriptEntry, VerificationRecord
from app.services.skills import learning, tasks


def _path_with_two_lessons(db: Session):
    skill = make_skill(db)
    path = LearningPath(
        skill_id=skill.id,
        slug=unique("path"),
        title="AI Data Annotation",
        status=STATUS_PUBLISHED,
    )
    db.add(path)
    db.flush()
    first = Lesson(
        skill_id=skill.id,
        slug=unique("lesson"),
        title="What annotation is",
        body_md="Annotation turns raw data into labels.",
        status=STATUS_PUBLISHED,
    )
    second = Lesson(
        skill_id=skill.id,
        slug=unique("lesson"),
        title="Label quality",
        body_md="Good labels are consistent.",
        status=STATUS_PUBLISHED,
    )
    db.add_all([first, second])
    db.flush()
    db.add_all(
        [
            LearningPathStep(path_id=path.id, ordinal=1, kind="lesson", lesson_id=first.id),
            LearningPathStep(path_id=path.id, ordinal=2, kind="lesson", lesson_id=second.id),
        ]
    )
    db.flush()
    return skill, path, first, second


def test_a_later_lesson_is_locked_until_the_earlier_one_is_done(db: Session) -> None:
    _skill, _path, _first, second = _path_with_two_lessons(db)
    student = make_user(db)

    with pytest.raises(ApiError) as excinfo:
        learning.complete_lesson(db, student, second.id)
    assert excinfo.value.status_code == 409
    assert excinfo.value.code == "step_locked"


def test_finishing_a_lesson_is_progress_not_verification(db: Session) -> None:
    skill, _path, first, second = _path_with_two_lessons(db)
    student = make_user(db)

    progress = learning.complete_lesson(db, student, first.id)

    assert progress.status == "completed" and progress.completed_at is not None
    assert db.scalars(select(VerificationRecord)).all() == []
    assert learning.get_skill(db, skill.slug)["paths"][0]["slug"]
    entry = db.scalars(select(TranscriptEntry)).one()
    assert entry.kind == "learned"
    assert entry.evidence_type == "lesson_progress"

    # The next lesson unlocks only after the first is complete.
    assert learning.complete_lesson(db, student, second.id).status == "completed"


def test_completing_a_lesson_twice_is_idempotent(db: Session) -> None:
    _skill, _path, first, _second = _path_with_two_lessons(db)
    student = make_user(db)

    once = learning.complete_lesson(db, student, first.id)
    twice = learning.complete_lesson(db, student, first.id)

    assert once.id == twice.id
    assert len(db.scalars(select(LessonProgress)).all()) == 1
    assert len(db.scalars(select(TranscriptEntry)).all()) == 1


def test_an_unpublished_lesson_is_not_available(db: Session) -> None:
    skill = make_skill(db)
    draft = Lesson(skill_id=skill.id, slug=unique("lesson"), title="Draft", status="draft")
    db.add(draft)
    db.flush()

    with pytest.raises(ApiError) as excinfo:
        learning.complete_lesson(db, make_user(db), draft.id)
    assert excinfo.value.code == "lesson_not_found"


def test_path_progress_reports_next_step_and_never_claims_verification(db: Session) -> None:
    _skill, path, first, second = _path_with_two_lessons(db)
    student = make_user(db)

    before = learning.path_with_progress(db, student, path)
    assert before["next_step"]["lesson_id"] == first.id
    assert before["completed_steps"] == 0

    learning.complete_lesson(db, student, first.id)
    after = learning.path_with_progress(db, student, path)
    assert after["completed_steps"] == 1
    assert after["next_step"]["lesson_id"] == second.id


def test_practice_is_validated_against_the_template_config(db: Session) -> None:
    skill = make_skill(db)
    template = make_template(
        db,
        skill,
        config={"expected_answer": {"key": "B"}, "gold_expected": {"key": "B"}},
    )
    student = make_user(db)

    right, result = tasks.submit_practice(
        db, student, template_id=template.id, answer={"key": "B"}
    )
    assert result.is_correct is True
    assert right.is_correct is True

    wrong, result_wrong = tasks.submit_practice(
        db, student, template_id=template.id, answer={"key": "A"}
    )
    assert result_wrong.is_correct is False
    assert result_wrong.details == {"expected_key": "B"}
    assert wrong.id != right.id


def test_practice_brief_never_leaks_the_expected_answer(db: Session) -> None:
    skill = make_skill(db)
    template = make_template(
        db,
        skill,
        config={"expected_answer": {"key": "B"}, "sample": {"key": "B"}},
    )

    brief = tasks.practice_brief(db, template.id)

    assert "expected_answer" not in brief
    assert brief["sample"] == {"key": "B"}


def test_a_template_without_a_sample_answer_says_so(db: Session) -> None:
    skill = make_skill(db)
    template = make_template(db, skill, config={})
    student = make_user(db)

    with pytest.raises(ApiError) as excinfo:
        tasks.submit_practice(db, student, template_id=template.id, answer={"key": "A"})
    assert excinfo.value.status_code == 503
    assert excinfo.value.code == "practice_unavailable"


def test_a_draft_template_is_not_practisable(db: Session) -> None:
    skill = make_skill(db)
    template = make_template(db, skill, status="draft")

    with pytest.raises(ApiError) as excinfo:
        tasks.practice_brief(db, template.id)
    assert excinfo.value.code == "task_not_found"


def test_the_skill_catalog_lists_paths_with_their_counts(db: Session) -> None:
    skill, path, _first, _second = _path_with_two_lessons(db)

    catalog = learning.list_skills(db)

    entry = next(row for row in catalog if row["id"] == skill.id)
    assert entry["published_paths"] == 1
    assert any(row["slug"] == path.slug for row in learning.get_skill(db, skill.slug)["paths"])
