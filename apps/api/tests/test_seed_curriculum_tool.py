"""The production curriculum tool creates only the named hierarchy, once."""
from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import func, select

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from tools.seed_curriculum import ensure_department  # noqa: E402

from app.models.academia import Department, Faculty, University  # noqa: E402
from app.seed import curriculum  # noqa: E402


def test_ensure_department_is_idempotent_and_seeds_curriculum(db) -> None:
    first = ensure_department(db, "Real University", "Science", "Computer Science")
    second = ensure_department(db, "Real University", "Science", "Computer Science")

    assert first == second
    assert db.scalar(select(func.count()).select_from(University)) == 1
    assert db.scalar(select(func.count()).select_from(Faculty)) == 1
    assert db.scalar(select(func.count()).select_from(Department)) == 1

    counts = curriculum.run(db, first)
    assert counts["skills"] == 1
    assert counts["learning_paths"] == 1
    assert counts["assessments"] == 1

    again = curriculum.run(db, first)
    assert all(value == 0 for value in again.values())
