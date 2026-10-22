"""Seed the V2 curriculum into a named department, without fake students.

    $env:APP_ENV = "prod"
    $env:DATABASE_URL = "<PROD external Postgres URL>"
    $env:PRODGUARD_ALLOW = "1"
    apps\\api\\.venv\\Scripts\\python.exe -m tools.seed_curriculum `
      --university "Lagos State University" `
      --faculty "Science" `
      --department "Computer Science"

The curriculum is the AI Data Annotation skill, its path, lessons, task
templates, assessment and practical task, plus the AID301 course. It is
idempotent: re-running fills gaps and never duplicates rows.

Use ``--department-id`` when the university/faculty/department already exist and
you do not want this tool to create them. Never run ``tools.seed_local`` against a
real database: that one also creates fake students.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "apps" / "api"))

from tools.prodguard import guard  # noqa: E402


def _slug(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "-" for ch in value.strip())
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-") or "university"


def ensure_department(
    db: Session,
    university_name: str,
    faculty_name: str,
    department_name: str,
) -> int:
    """Find or create the hierarchy. Returns the department id."""
    from app.models.academia import Department, Faculty, University

    university = db.scalar(select(University).where(University.name == university_name))
    if university is None:
        base = _slug(university_name)
        slug = base
        suffix = 2
        while db.scalar(select(University.id).where(University.slug == slug)) is not None:
            slug = f"{base}-{suffix}"
            suffix += 1
        university = University(name=university_name, slug=slug)
        db.add(university)
        db.flush()

    faculty = db.scalar(
        select(Faculty).where(
            Faculty.university_id == university.id, Faculty.name == faculty_name
        )
    )
    if faculty is None:
        faculty = Faculty(university_id=university.id, name=faculty_name)
        db.add(faculty)
        db.flush()

    department = db.scalar(
        select(Department).where(
            Department.faculty_id == faculty.id, Department.name == department_name
        )
    )
    if department is None:
        department = Department(faculty_id=faculty.id, name=department_name)
        db.add(department)
        db.flush()
    return department.id


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Seed the V2 curriculum only.")
    parser.add_argument("--university", help="University name; created if missing.")
    parser.add_argument("--faculty", help="Faculty name; created if missing.")
    parser.add_argument("--department", help="Department name; created if missing.")
    parser.add_argument("--department-id", type=int, help="Use an existing department id.")
    parser.add_argument(
        "--i-know-this-is-production",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args(argv)

    if args.department_id is None and not (args.university and args.faculty and args.department):
        parser.error("pass --department-id, or all of --university/--faculty/--department")

    guard("seed_curriculum")

    from app.db.session import SessionLocal
    from app.seed import curriculum

    with SessionLocal() as db:
        if args.department_id is not None:
            department_id = args.department_id
        else:
            department_id = ensure_department(
                db, args.university, args.faculty, args.department
            )
        counts = curriculum.run(db, department_id)
        db.commit()

    print(f"seed_curriculum complete: department_id={department_id}")
    for key, value in counts.items():
        print(f"  {key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
