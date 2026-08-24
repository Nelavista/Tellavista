"""Best-effort mapping from a User's free-text university/faculty/department/level
fields (kept as-is on User for backward compat) to the normalized University/Faculty/
Department/Course taxonomy (see models.py's "ACADEMIA TAXONOMY" section).

User.university and User.department come from fixed <select>/picker values
(profile_completion_modal.html, static/js/faculty-departments.js), not free typing, so
exact case-insensitive-trim matching is sufficient here -- no fuzzy matching needed.

Faculty is deliberately NOT matched from User.faculty (a large picklist with real-world
naming variance across institutions, unreliable as a join key). It's derived from the
matched Department row instead, since that's the reliable side of the relationship.

A student whose university/department the taxonomy doesn't cover yet (anything outside
LASU/UNILAG/UI, or a department not seeded for their school) resolves to all-None
fields and an empty course list -- callers must treat that as "no data yet", never as
an error.
"""
from extensions import db
from models import University, Faculty, Department, Course


class AcademicContext:
    def __init__(self, university=None, faculty=None, department=None, courses=None):
        self.university = university
        self.faculty = faculty
        self.department = department
        self.courses = courses if courses is not None else []

    @property
    def resolved(self):
        return self.university is not None and self.department is not None


def resolve_academic_context(user, level=None):
    """level defaults to user.level; pass explicitly to look up a different level's
    course list without needing a second User."""
    if not user or not user.university or not user.department:
        return AcademicContext()

    university = University.query.filter(
        db.func.lower(University.name) == user.university.strip().lower()
    ).first()
    if not university:
        return AcademicContext()

    department = (
        Department.query.join(Faculty)
        .filter(
            Faculty.university_id == university.id,
            db.func.lower(Department.name) == user.department.strip().lower(),
        )
        .first()
    )
    if not department:
        return AcademicContext(university=university)

    faculty = department.faculty

    lvl = (level or user.level or '').strip()
    courses = []
    if lvl:
        courses = (
            Course.query.filter_by(department_id=department.id, level=lvl)
            .order_by(Course.code)
            .all()
        )

    return AcademicContext(university=university, faculty=faculty, department=department, courses=courses)


def find_course(department, code):
    """Single-course lookup for the course detail page / AI grounding -- case-
    insensitive on code since Material.course_code casing has been inconsistent."""
    if not department or not code:
        return None
    return Course.query.filter(
        Course.department_id == department.id,
        db.func.upper(Course.code) == code.strip().upper(),
    ).first()
