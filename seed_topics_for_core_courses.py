"""Seeds an AI-drafted topic list + description for the ~30 course codes
seed_materials.py already has real, verified static materials for (CSC101, MAT101,
CHM101, ...) -- see CORE_MATERIALS in that file. This is deliberately NOT an attempt to
cover "thousands of courses" (see the Academia Materials implementation brief: "do not
randomly invent thousands of topics"). It proves the Course -> Topic -> explanation ->
video -> materials vertical slice end-to-end on courses we already know have real
student-facing content, so a student opening e.g. CSC213 sees both a real topic
breakdown AND real uploaded materials, not one without the other.

Every Topic this script creates starts as content_source='ai_draft', is_active=True --
draft, review-pending content, per the product principle that AI output must be
persisted and reviewable, never presented as an official syllabus. An admin reviews/
edits via /admin/academia/courses/<id> (templates/admin_academia_course.html) same as
any other topic. Per-topic explanation and reference video are intentionally NOT
generated here (that's a separate, more expensive AI call best done on demand from the
admin UI, or in a follow-up batch pass) -- this script only proves the topic *outline*
for a real, curriculum-backed subset of courses.

Idempotent: skips any course that already has at least one Topic row, so re-running
after partial completion (e.g. an API failure partway through) only fills in the rest.
Requires OPENROUTER_API_KEY (config.py) and network access to openrouter.ai -- this
calls a real, billed AI API, so it does NOT run automatically; review the printed plan,
then re-run with --apply.

Usage:
    python seed_topics_for_core_courses.py            # dry run: prints which courses
                                                        # would be seeded, makes no AI
                                                        # calls and no DB writes
    python seed_topics_for_core_courses.py --apply     # actually calls the AI and
                                                        # creates Topic rows
"""
import sys

from app import app, db
from models import Course, Department, Faculty, University, Topic
from services.ai_service import generate_course_topics
from seed_materials import CORE_MATERIALS

APPLY = '--apply' in sys.argv

# CORE_MATERIALS entries were authored against LASU's own department names -- this
# script only targets LASU since that's the university seed_materials.py's real static
# files were curated for. A future pass for another school's course codes belongs in
# its own script once that school has its own verified materials, not bolted onto this
# LASU-specific list.
UNIVERSITY_NAME = 'Lagos State University'


def _find_course(university, dept_name, code, level):
    dept = (
        Department.query.join(Faculty)
        .filter(Faculty.university_id == university.id, db.func.lower(Department.name) == dept_name.strip().lower())
        .first()
    )
    if not dept:
        return None, f"department '{dept_name}' not found at {UNIVERSITY_NAME}"
    course = Course.query.filter_by(department_id=dept.id, code=code, level=level).first()
    if not course:
        return None, f"course {code} (level {level}) not found under {dept_name}"
    return course, None


def main():
    with app.app_context():
        university = University.query.filter_by(name=UNIVERSITY_NAME).first()
        if not university:
            print(f"[ERROR] {UNIVERSITY_NAME} not found -- run seed_academia.py first.")
            return

        plan = []
        for code, info in CORE_MATERIALS.items():
            course, error = _find_course(university, info['department'], code, info['level'])
            if error:
                print(f"[SKIP] {code}: {error}")
                continue
            if course.topics.count() > 0:
                print(f"[SKIP] {code}: already has {course.topics.count()} topic(s)")
                continue
            plan.append(course)

        print(f"\n{len(plan)} course(s) ready to seed: {', '.join(c.code for c in plan)}")

        if not APPLY:
            print("\nDry run only -- no AI calls made, no changes written. Re-run with --apply.")
            return

        seeded = failed = 0
        for course in plan:
            try:
                draft = generate_course_topics(course.code, course.title, course.department.name, course.level)
            except Exception as e:
                print(f"[FAIL] {course.code}: AI generation failed -- {e}")
                failed += 1
                continue

            if draft.get('description') and not course.description:
                course.description = draft['description']

            titles = [t.strip() for t in (draft.get('topics') or []) if isinstance(t, str) and t.strip()]
            for i, title in enumerate(titles):
                db.session.add(Topic(course_id=course.id, title=title, order=i, content_source='ai_draft'))

            db.session.commit()
            print(f"[OK]   {course.code}: {len(titles)} topics")
            seeded += 1

        print(f"\nSeeded topics for {seeded} course(s), {failed} failed.")


if __name__ == '__main__':
    main()
