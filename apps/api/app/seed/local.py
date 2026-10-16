"""Sample data for LOCAL and DEV. Idempotent, and safe to re-run.

Creates: one fake university (Lagos Test University), a Science faculty, a Computer
Science department, two courses, two sample students and a few materials.

It NEVER reads production and never copies real data. It is invoked through the
guarded entrypoint `tools/seed_local.py` (which enforces the prod guard).
"""
from __future__ import annotations

from sqlalchemy import select

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.academia import Course, Department, Faculty, Material, University
from app.models.identity import User

FAKE_DOMAIN = "example.test"


def run() -> dict[str, int]:
    """Create the sample data. Returns a count of what now exists."""
    # Skeleton convenience: ensure tables exist. In real environments schema is
    # managed by Alembic (`alembic upgrade head`).
    Base.metadata.create_all(engine)

    created = {"universities": 0, "faculties": 0, "departments": 0, "courses": 0,
               "students": 0, "materials": 0}

    with SessionLocal() as db:
        uni = db.scalar(select(University).where(University.name == "Lagos Test University"))
        if uni is None:
            uni = University(name="Lagos Test University", slug="lagos-test-university")
            db.add(uni)
            db.flush()
            created["universities"] += 1

        fac = db.scalar(select(Faculty).where(Faculty.university_id == uni.id, Faculty.name == "Science"))
        if fac is None:
            fac = Faculty(university_id=uni.id, name="Science")
            db.add(fac)
            db.flush()
            created["faculties"] += 1

        dept = db.scalar(
            select(Department).where(
                Department.faculty_id == fac.id, Department.name == "Computer Science"
            )
        )
        if dept is None:
            dept = Department(faculty_id=fac.id, name="Computer Science")
            db.add(dept)
            db.flush()
            created["departments"] += 1

        courses = [
            ("CSC213", "Data Structures & Algorithm Analysis", "200"),
            ("CSC315", "Operating Systems", "300"),
        ]
        for code, title, level in courses:
            exists = db.scalar(
                select(Course).where(
                    Course.department_id == dept.id, Course.code == code, Course.level == level
                )
            )
            if exists is None:
                course = Course(department_id=dept.id, code=code, title=title, level=level)
                db.add(course)
                db.flush()
                created["courses"] += 1
                for i in range(1, 3):
                    db.add(Material(
                        course_id=course.id,
                        title=f"{code} — Sample Material {i}",
                        file_url=None,
                        source="seed",
                    ))
                    created["materials"] += 1

        for i in range(1, 3):
            email = f"student{i}@{FAKE_DOMAIN}"
            if db.scalar(select(User).where(User.email == email)) is None:
                db.add(User(
                    email=email,
                    username=f"student{i}",
                    password_hash=None,          # auth not built yet -> requires reset (ADR-0009)
                    name=f"Sample Student {i}",
                    email_verified=True,
                    university=uni.name,
                    department=dept.name,
                    level="200",
                ))
                created["students"] += 1

        db.commit()

    return created


if __name__ == "__main__":  # convenience; still guarded by tools/seed_local.py
    print(run())
