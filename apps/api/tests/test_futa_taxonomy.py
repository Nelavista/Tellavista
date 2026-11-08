"""FUTA provenance and V2 course metadata coverage."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.academia import Course, Department, Faculty, University
from app.seed import futa
from app.services.imports import v1 as importer


def test_futa_seed_contains_only_the_verified_svg_course_list(db: Session) -> None:
    first = futa.seed(db)
    second = futa.seed(db)

    assert first["departments"] == 42
    assert first["courses"] == 35
    assert second["courses"] == 0

    university = db.scalar(select(University).where(University.name == futa.FUTA_NAME))
    svg = db.scalar(
        select(Department)
        .join(Faculty, Faculty.id == Department.faculty_id)
        .where(
            Faculty.university_id == university.id,
            Department.name == "Surveying and Geoinformatics",
        )
    )
    courses = db.scalars(select(Course).where(Course.department_id == svg.id)).all()
    assert len(courses) == 35
    assert {course.source for course in courses} == {"futa_official"}
    assert {course.semester for course in courses} == {"First Semester", "Second Semester"}


def test_v1_taxonomy_import_preserves_and_updates_course_metadata(db: Session) -> None:
    data = {
        "taxonomy": [
            {
                "name": "FUTA Import Test",
                "slug": "futa-import-test",
                "faculties": [
                    {
                        "name": "School of Computing",
                        "departments": [
                            {
                                "name": "Computer Science",
                                "courses": [
                                    {
                                        "code": "CSC101",
                                        "title": "Introduction to Computing",
                                        "level": "100",
                                        "semester": "1st",
                                        "course_type": "CORE",
                                        "description": "Foundations of computing.",
                                        "source": "futa_official",
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }
        ]
    }

    importer.run_import(db, data=data, mode="apply")
    importer.run_import(
        db,
        data={
            "taxonomy": [
                {
                    **data["taxonomy"][0],
                    "faculties": [
                        {
                            **data["taxonomy"][0]["faculties"][0],
                            "departments": [
                                {
                                    **data["taxonomy"][0]["faculties"][0]["departments"][0],
                                    "courses": [
                                        {
                                            **data["taxonomy"][0]["faculties"][0]["departments"][0]["courses"][0],
                                            "description": "Updated description.",
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ]
        },
        mode="apply",
    )

    course = db.scalar(select(Course).where(Course.code == "CSC101"))
    assert course is not None
    assert course.semester == "1st"
    assert course.course_type == "CORE"
    assert course.description == "Updated description."
    assert course.source == "futa_official"
