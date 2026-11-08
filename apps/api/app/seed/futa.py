"""Verified FUTA undergraduate structure and Surveying & GeoInformatics courses.

The school and department names were read from FUTA pages on 2026-11-01. The
course rows are limited to the 35 entries published by the SVG department's
course synopsis pages; unlisted codes are deliberately not invented.
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.academia import Course, Department, Faculty, University

FUTA_NAME = "Federal University of Technology, Akure"
FUTA_SOURCE = "futa_official"

SCHOOLS: dict[str, tuple[str, ...]] = {
    "School of Agriculture and Agricultural Technology": (
        "Agricultural & Resource Economics",
        "Agricultural Extension & Comm. Tech.",
        "Animal Production and Health",
        "Crop, Soil & Pest Mangt.",
        "Ecotourism & Wildlife Management",
        "Fisheries & Aquaculture",
        "Food Science & Technology",
        "Forestry & Wood Technology",
        "Nutrition and Dietetics",
    ),
    "School of Computing": (
        "Computer Science", "Information Technology", "Cybersecurity",
        "Information Systems", "Data Science", "Software Engineering",
    ),
    "School of Earth and Mineral Sciences": (
        "Applied Geophysics", "Applied Geology", "Meteorology",
        "Marine Science & Technology", "Remote Sensing & GIS",
    ),
    "School of Environmental Technology": (
        "Architecture", "Building", "Estate Management", "Industrial Design",
        "Quantity Surveying", "Surveying and Geoinformatics", "Urban & Regional Planning",
    ),
    "School of Physical Sciences": ("Chemistry", "Mathematics", "Physics", "Statistics"),
    "School of Life Sciences": (
        "Biology", "Biochemistry", "Microbiology", "Plant Biology",
        "Animal and Environmental Biology", "Biotechnology",
    ),
    "School of Logistic and Innovation Technology": (
        "Entrepreneurship Management Tech.", "Project Management Technology",
        "Business Administration", "Logistics and Transport Technology",
        "Securities and Investment Management Technology",
    ),
}

SVG_COURSES: tuple[tuple[str, str, str, str, str], ...] = (
    ("100", "First Semester", "SVG101", "Introduction to Surveying and Geoinformatics"),
    ("100", "First Semester", "SVG103", "MAP READINGAND INTERPRETATION"),
    ("100", "Second Semester", "SVG102", "Surveying Instrumentation 1"),
    ("200", "First Semester", "SVG201", "Basic Surveying 1"),
    ("200", "First Semester", "SVG203", "Cadastral Surveying 1"),
    ("200", "First Semester", "SVG205", "Photogrammetry I"),
    ("200", "First Semester", "SVG207", "Field Astronomy"),
    ("200", "First Semester", "SVG209", "Survey Computation"),
    ("200", "First Semester", "SVG211", "Computer Application in Surveying 1"),
    ("200", "Second Semester", "SVG202", "Basic Surveying II"),
    ("200", "Second Semester", "SVG204", "Cadastral Surveying 2"),
    ("200", "Second Semester", "SVG206", "Geodetic Astronomy"),
    ("200", "Second Semester", "SVG208", "SURVEYING CARTOGRAPHY"),
    ("200", "Second Semester", "SVG210", "Computer Application in Surveying 2"),
    ("200", "Second Semester", "SVG212", "Surveying Instrumentation 11"),
    ("300", "First Semester", "MTS315", "Engineering Mathematics"),
    ("300", "First Semester", "RSG301", "Satellite Remote Sensing"),
    ("300", "First Semester", "SVG303", "Photogrammetry II"),
    ("300", "First Semester", "SVG305", "topographic surveying"),
    ("300", "First Semester", "SVG307", "Adjustment Computation I"),
    ("300", "First Semester", "SVG309", "Geodetic Surveying"),
    ("300", "Second Semester", "SVG302", "Engineering Surveying II"),
    ("300", "Second Semester", "SVG304", "Electronic Surveying"),
    ("300", "Second Semester", "SVG306", "Mining and underground Surveying"),
    ("300", "Second Semester", "SVG308", "Adjustment computation II"),
    ("300", "Second Semester", "SVG310", "Spatial Statistics"),
    ("300", "Second Semester", "SVG314", "Safety and swimming in Surveying"),
    ("300", "Second Semester", "SVG316", "DATA QUALITY AND STRUCTURE"),
    ("400", "First Semester", "RSG401", "Geographic Information Systems II"),
    ("400", "First Semester", "SVG401", "Map Projection"),
    ("400", "First Semester", "SVG403", "Hydrographic Surveying 1"),
    ("400", "First Semester", "SVG405", "Digital Photogrammetry"),
    ("400", "First Semester", "SVG407", "Digital Mapping"),
    ("400", "First Semester", "SVG409", "Introduction to Geodesy"),
    ("400", "First Semester", "SVG411", "Potential Theory and Spherical Harmonics"),
)


def seed(db: Session) -> dict[str, int]:
    university = db.scalar(select(University).where(University.name == FUTA_NAME))
    if university is None:
        university = University(name=FUTA_NAME, slug="federal-university-of-technology-akure")
        db.add(university)
        db.flush()

    departments: dict[str, Department] = {}
    for school, names in SCHOOLS.items():
        faculty = db.scalar(
            select(Faculty).where(Faculty.university_id == university.id, Faculty.name == school)
        )
        if faculty is None:
            faculty = Faculty(university_id=university.id, name=school)
            db.add(faculty)
            db.flush()
        for name in names:
            department = db.scalar(
                select(Department).where(
                    Department.faculty_id == faculty.id, Department.name == name
                )
            )
            if department is None:
                department = Department(faculty_id=faculty.id, name=name)
                db.add(department)
                db.flush()
            departments[name] = department

    svg = departments["Surveying and Geoinformatics"]
    created_courses = 0
    for level, semester, code, title in SVG_COURSES:
        course = db.scalar(
            select(Course).where(
                Course.department_id == svg.id,
                Course.code == code,
                Course.level == level,
            )
        )
        if course is None:
            db.add(
                Course(
                    department_id=svg.id,
                    code=code,
                    title=title,
                    level=level,
                    semester=semester,
                    source=FUTA_SOURCE,
                )
            )
            created_courses += 1
    db.flush()
    return {"universities": 1, "faculties": len(SCHOOLS), "departments": len(departments), "courses": created_courses}
