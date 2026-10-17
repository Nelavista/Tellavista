"""Study materials for the student's own courses (PRD §8).

A student never searches a global library: the query is scoped to the courses they
are enrolled in. Search is lexical and portable (title plus chunk content) because
the embedding store and pgvector are a later decision; the interface is the same
when vector search replaces the scoring behind it.

Retrieval returns scored chunks with their material and course, which is what makes
an Ask Nelavista answer citable.
"""
from __future__ import annotations

import math

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.academia import Course, Enrolment, Material, MaterialChunk
from app.models.identity import User
from app.services.ai.provider import ContextChunk, terms


def enrolled_course_ids(db: Session, user: User) -> set[int]:
    return {
        row
        for row in db.scalars(
            select(Enrolment.course_id).where(
                Enrolment.user_id == user.id, Enrolment.status == "active"
            )
        ).all()
    }


def _course_map(db: Session, course_ids: set[int]) -> dict[int, Course]:
    if not course_ids:
        return {}
    return {
        course.id: course
        for course in db.scalars(select(Course).where(Course.id.in_(course_ids))).all()
    }


def my_materials(db: Session, user: User, *, course_id: int | None = None) -> list[dict]:
    course_ids = enrolled_course_ids(db, user)
    if course_id is not None:
        if course_id not in course_ids:
            raise ApiError(403, "not_enrolled", "You are not enrolled in that course.")
        course_ids = {course_id}
    if not course_ids:
        return []
    courses = _course_map(db, course_ids)
    rows = db.scalars(
        select(Material)
        .where(Material.course_id.in_(course_ids))
        .order_by(Material.course_id, Material.title)
    ).all()
    return [
        {
            "id": material.id,
            "title": material.title,
            "file_url": material.file_url,
            "source": material.source,
            "course": (
                {
                    "id": courses[material.course_id].id,
                    "code": courses[material.course_id].code,
                    "title": courses[material.course_id].title,
                }
                if material.course_id in courses
                else None
            ),
        }
        for material in rows
    ]


def search_materials(
    db: Session, user: User, query: str, *, limit: int = 20
) -> list[dict]:
    """Find notes, textbooks and past questions for the student's courses."""
    cleaned = query.strip()
    if len(cleaned) < 2:
        raise ApiError(400, "query_too_short", "Type at least two characters.")
    course_ids = enrolled_course_ids(db, user)
    if not course_ids:
        return []
    courses = _course_map(db, course_ids)
    q_terms = terms(cleaned)
    pattern = f"%{cleaned}%"

    materials = db.scalars(
        select(Material).where(
            Material.course_id.in_(course_ids),
            or_(Material.title.ilike(pattern), Material.source.ilike(pattern)),
        )
    ).all()
    matched: dict[int, dict] = {
        material.id: {
            "material_id": material.id,
            "title": material.title,
            "course": (
                {"code": courses[material.course_id].code, "id": material.course_id}
                if material.course_id in courses
                else None
            ),
            "snippet": material.title,
            "score": 1.0,
        }
        for material in materials
    }

    # Chunk-level matches find content whose title says nothing about the query.
    chunks = db.execute(
        select(MaterialChunk, Material)
        .join(Material, Material.id == MaterialChunk.material_id)
        .where(Material.course_id.in_(course_ids))
    ).all()
    for chunk, material in chunks:
        chunk_terms = terms(chunk.content)
        if not q_terms:
            continue
        overlap = len(q_terms & chunk_terms)
        if not overlap:
            continue
        score = overlap / math.sqrt(len(chunk_terms) + 1)
        current = matched.get(material.id)
        if current is None or score > current["score"]:
            matched[material.id] = {
                "material_id": material.id,
                "title": material.title,
                "course": (
                    {"code": courses[material.course_id].code, "id": material.course_id}
                    if material.course_id in courses
                    else None
                ),
                "snippet": _snippet(chunk.content, q_terms),
                "score": round(score, 4),
            }

    ranked = sorted(matched.values(), key=lambda item: (-item["score"], item["material_id"]))
    return ranked[:limit]


def _snippet(content: str, q_terms: set[str], *, width: int = 180) -> str:
    lowered = content.lower()
    positions = [lowered.find(term) for term in q_terms if lowered.find(term) >= 0]
    start = max(0, (min(positions) if positions else 0) - 40)
    snippet = content[start : start + width].strip()
    return ("…" if start else "") + snippet + ("…" if start + width < len(content) else "")


def material_detail(db: Session, user: User, material_id: int) -> dict:
    material = db.get(Material, material_id)
    if material is None:
        raise ApiError(404, "material_not_found", "That material does not exist.")
    if material.course_id not in enrolled_course_ids(db, user):
        raise ApiError(403, "not_enrolled", "You are not enrolled in that course.")
    course = db.get(Course, material.course_id) if material.course_id else None
    chunks = db.scalars(
        select(MaterialChunk)
        .where(MaterialChunk.material_id == material.id)
        .order_by(MaterialChunk.ordinal)
    ).all()
    return {
        "id": material.id,
        "title": material.title,
        "file_url": material.file_url,
        "course": {"id": course.id, "code": course.code, "title": course.title} if course else None,
        "chunks": [{"id": chunk.id, "ordinal": chunk.ordinal, "content": chunk.content} for chunk in chunks],
    }


def retrieve(
    db: Session,
    user: User,
    question: str,
    *,
    course_id: int | None = None,
    limit: int = 4,
) -> list[tuple[ContextChunk, float]]:
    """Best grounded chunks for a question, with a lexical relevance score."""
    course_ids = enrolled_course_ids(db, user)
    if course_id is not None:
        if course_id not in course_ids:
            raise ApiError(403, "not_enrolled", "You are not enrolled in that course.")
        course_ids = {course_id}
    if not course_ids:
        return []

    q_terms = terms(question)
    if not q_terms:
        return []

    rows = db.execute(
        select(MaterialChunk, Material, Course)
        .join(Material, Material.id == MaterialChunk.material_id)
        .join(Course, Course.id == Material.course_id)
        .where(Material.course_id.in_(course_ids))
    ).all()

    scored: list[tuple[ContextChunk, float]] = []
    for chunk, material, course in rows:
        chunk_terms = terms(chunk.content)
        overlap = q_terms & chunk_terms
        if not overlap:
            continue
        # Normalising by chunk length stops a long appendix from always winning.
        score = len(overlap) / math.sqrt(len(chunk_terms) + 1)
        if len(overlap) >= 2:
            score *= 1.2
        scored.append(
            (
                ContextChunk(
                    chunk_id=chunk.id,
                    material_id=material.id,
                    material_title=material.title,
                    course_code=course.code,
                    content=chunk.content,
                ),
                round(score, 4),
            )
        )
    scored.sort(key=lambda item: (-item[1], item[0].chunk_id))
    return scored[:limit]
