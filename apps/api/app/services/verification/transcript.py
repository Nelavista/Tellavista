"""Skill Transcript: what was learned, proved and delivered, with evidence (PRD §5).

Every line is a projection of a real row — a lesson progress record, an assessment
attempt, an approved submission. There is no free-text skill a student can add, and
no line without an `evidence_type` + `evidence_id`. The unique constraint on
(user, kind, evidence) makes projection replay safe.
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.identity import User
from app.models.skills import Skill
from app.models.verification import (
    TRANSCRIPT_DELIVERED,
    TRANSCRIPT_KINDS,
    TRANSCRIPT_LEARNED,
    TRANSCRIPT_PROVED,
    TranscriptEntry,
)


def add_entry(
    db: Session,
    *,
    user_id: int,
    kind: str,
    title: str,
    evidence_type: str,
    evidence_id: int | str,
    skill_id: int | None = None,
) -> TranscriptEntry:
    if kind not in TRANSCRIPT_KINDS:
        raise ValueError(f"unknown transcript kind: {kind}")
    evidence = str(evidence_id)
    existing = db.scalar(
        select(TranscriptEntry).where(
            TranscriptEntry.user_id == user_id,
            TranscriptEntry.kind == kind,
            TranscriptEntry.evidence_type == evidence_type,
            TranscriptEntry.evidence_id == evidence,
        )
    )
    if existing is not None:
        return existing

    entry = TranscriptEntry(
        user_id=user_id,
        skill_id=skill_id,
        kind=kind,
        title=title[:200],
        evidence_type=evidence_type,
        evidence_id=evidence,
    )
    db.add(entry)
    db.flush()
    return entry


def get_transcript(db: Session, user: User) -> dict:
    entries = db.scalars(
        select(TranscriptEntry)
        .where(TranscriptEntry.user_id == user.id)
        .order_by(TranscriptEntry.occurred_at.desc(), TranscriptEntry.id.desc())
    ).all()
    skills = {skill.id: skill for skill in db.scalars(select(Skill)).all()}

    def serialise(entry: TranscriptEntry) -> dict:
        skill = skills.get(entry.skill_id) if entry.skill_id else None
        return {
            "id": entry.id,
            "kind": entry.kind,
            "title": entry.title,
            "skill": skill.name if skill else None,
            "skill_slug": skill.slug if skill else None,
            "evidence": {"type": entry.evidence_type, "id": entry.evidence_id},
            "occurred_at": entry.occurred_at,
        }

    grouped = {
        "learned": [serialise(e) for e in entries if e.kind == TRANSCRIPT_LEARNED],
        "proved": [serialise(e) for e in entries if e.kind == TRANSCRIPT_PROVED],
        "delivered": [serialise(e) for e in entries if e.kind == TRANSCRIPT_DELIVERED],
    }
    return {
        "entries": [serialise(e) for e in entries],
        "learned": grouped["learned"],
        "proved": grouped["proved"],
        "delivered": grouped["delivered"],
        "counts": {kind: len(grouped[kind]) for kind in ("learned", "proved", "delivered")},
    }
