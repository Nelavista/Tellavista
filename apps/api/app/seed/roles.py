"""Role seeding — roles are data, not code (app/models/admin.py).

Idempotent and authoritative: it inserts missing roles and refreshes names/flags
if the definition changed, so re-running it is always safe. Called by the local
seed and by tests; the role rows are a prerequisite for any user insert because
`users.role_id` references them.
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.admin import SEED_ROLES, Role


def seed_roles(db: Session) -> int:
    """Insert/refresh the seeded roles. Returns the number created."""
    created = 0
    for code, name, is_staff in SEED_ROLES:
        role = db.scalar(select(Role).where(Role.code == code))
        if role is None:
            db.add(Role(code=code, name=name, is_staff=is_staff))
            created += 1
            continue
        if role.name != name or role.is_staff != is_staff:
            role.name = name
            role.is_staff = is_staff
    db.flush()
    return created
