"""One-time DATA backfill (separate from the SCHEMA migration in
migrations/versions/d00f3200eb0b_add_topics_and_material_taxonomy_links.py on purpose --
a schema migration should never also be a silent mass UPDATE).

For every existing Material row that has no course_id/department_id yet, tries to
resolve one from the real University/Faculty/Department/Course taxonomy using the
row's existing free-text course_code/department/university strings -- the same
resolution logic services/academic_context.py already uses for a live student, applied
once here to backfill history instead of leaving every pre-taxonomy row permanently
unlinked.

Matching rules (conservative on purpose -- a wrong link is worse than no link):
  1. department_id: matched by Department.name (case-insensitive) via Faculty, scoped
     to Material.university if set. If Material.university is NULL and the department
     name is ambiguous across more than one university, department_id is left NULL
     rather than guessing which school it meant.
  2. course_id: only attempted once department_id resolved, matched by
     Course.code (case-insensitive) + Course.level within that department. A
     course_code with no matching Course row (e.g. a department/school the taxonomy
     doesn't cover yet) is left NULL -- never invented.

Nothing here touches Material.course_code/department/university/course_type -- those
free-text columns are left exactly as they were. This only fills in the new nullable
course_id/department_id columns where a confident match exists.

Default is a DRY RUN: reports what it would link, changes nothing. Pass --apply to
commit. Idempotent -- rows that already have course_id/department_id set are skipped,
so re-running after new taxonomy data is added only fills in the newly-resolvable rows.

Usage:
    python backfill_material_taxonomy_links.py            # report only
    python backfill_material_taxonomy_links.py --apply     # actually link rows
"""
import sys
from collections import defaultdict

APPLY = '--apply' in sys.argv


def _resolve_department(material, dept_by_name):
    """Returns a single Department row, or None if unresolved/ambiguous."""
    if not material.department:
        return None
    key = material.department.strip().lower()
    candidates = dept_by_name.get(key, [])
    if not candidates:
        return None
    if material.university:
        uni_key = material.university.strip().lower()
        scoped = [d for d in candidates if d.faculty.university.name.strip().lower() == uni_key]
        return scoped[0] if len(scoped) == 1 else None
    # No university set on the material -- only safe to link if the department name
    # isn't ambiguous across schools (true today since only LASU has real departments,
    # but this stays correct as more schools get their own taxonomy).
    return candidates[0] if len(candidates) == 1 else None


def main():
    # Deferred on purpose: importing app.py at module level would connect to whatever
    # DATABASE_URL is configured (a real Postgres instance outside of a script run --
    # see tests/conftest.py's docstring for why this matters) the moment anything
    # imports this module, even just to reuse _resolve_department's pure matching logic.
    from app import app, db
    from models import Material, University, Faculty, Department, Course

    with app.app_context():
        departments = Department.query.join(Faculty).join(University).all()
        dept_by_name = defaultdict(list)
        for d in departments:
            dept_by_name[d.name.strip().lower()].append(d)

        candidates = Material.query.filter(
            db.or_(Material.course_id.is_(None), Material.department_id.is_(None))
        ).all()

        dept_linked = course_linked = unresolved_dept = unresolved_course = 0

        for m in candidates:
            dept = None
            if m.department_id:
                dept = Department.query.get(m.department_id)
            elif m.department:
                dept = _resolve_department(m, dept_by_name)
                if dept:
                    m.department_id = dept.id
                    dept_linked += 1
                else:
                    unresolved_dept += 1

            if not m.course_id and dept and m.course_code:
                code = m.course_code.strip().upper()
                course_query = Course.query.filter(
                    Course.department_id == dept.id,
                    db.func.upper(Course.code) == code,
                )
                if m.level:
                    course_query = course_query.filter(Course.level == m.level)
                course = course_query.first()
                if course:
                    m.course_id = course.id
                    course_linked += 1
                else:
                    unresolved_course += 1

        print(f"Checked {len(candidates)} materials missing course_id and/or department_id.")
        print(f"  department_id newly resolved: {dept_linked}  (unresolved/ambiguous: {unresolved_dept})")
        print(f"  course_id newly resolved:     {course_linked}  (no matching Course row: {unresolved_course})")

        if not APPLY:
            print("\nDry run only -- no changes made. Re-run with --apply to commit these links.")
            db.session.rollback()
            return

        db.session.commit()
        print(f"\nLinked {dept_linked} department_id and {course_linked} course_id values.")


if __name__ == '__main__':
    main()
