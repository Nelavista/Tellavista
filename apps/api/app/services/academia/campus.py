"""Campus: a light utility reachable from both paths (PRD §2).

Not a third product and not a social space: university information and map points.
It is scoped to the student's university, and an imported V1 account that has not
finished onboarding still resolves its university by name.
"""
from __future__ import annotations

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.academia import University
from app.models.identity import User
from app.models.ops import CampusInfo
from app.services.identity.onboarding import academic_context

MAP_KINDS = {"building", "library", "hall", "department", "hostel", "food", "map"}


def campus_for(db: Session, user: User) -> dict:
    context = academic_context(db, user)
    name = context.get("university")
    if not name:
        return {"university": None, "info": [], "map": []}

    university = db.scalar(
        select(University).where(or_(University.name == name, University.slug == name))
    )
    if university is None:
        return {"university": None, "info": [], "map": []}

    rows = db.scalars(
        select(CampusInfo)
        .where(CampusInfo.university_id == university.id, CampusInfo.is_published.is_(True))
        .order_by(CampusInfo.id)
    ).all()
    items = [
        {
            "id": row.id,
            "kind": row.kind,
            "title": row.title,
            "body": row.body,
            "latitude": (row.latitude_micro / 1_000_000) if row.latitude_micro is not None else None,
            "longitude": (row.longitude_micro / 1_000_000) if row.longitude_micro is not None else None,
        }
        for row in rows
    ]
    return {
        "university": {"id": university.id, "name": university.name, "slug": university.slug},
        "info": [item for item in items if item["kind"] not in MAP_KINDS],
        "map": [item for item in items if item["kind"] in MAP_KINDS],
    }
