"""Populates a topic OUTLINE (course description + ordered topic titles, via
generate_course_topics) for every real, taxonomy-backed course -- not a handful of demo
courses. This is the fix for "Nelavista hasn't added a topic breakdown for CSC201 yet":
that empty state should be the rare exception (a course the taxonomy doesn't cover, or
one an admin hasn't gotten to), not the default experience.

Deliberately scoped to OUTLINES only (title lists + a course description), not full
per-topic explanations or YouTube videos -- those are a much larger, separately-costed
pass (see seed_topics_for_core_courses.py for full explanation+video generation on the
smaller set of courses that already have real seeded materials to pair with). An
outline alone is already a large improvement: a student sees a real, ordered syllabus
instead of nothing, and can open any topic to at least see "no explanation yet" rather
than the course itself not existing.

Every course processed this way gets content_source='ai_draft' Topic rows -- draft,
review-pending content, exactly like the admin UI's per-course "Generate draft topics"
button, just run in bulk across the whole catalog instead of one course at a time.
Idempotent: skips any course that already has at least one Topic row, so re-running
after a partial failure (rate limit, network blip) only fills in what's left.

Requires OPENROUTER_API_KEY and network access -- this calls a real, billed AI API. Does
NOT run automatically; review the dry-run plan (course + department counts), then
re-run with --apply.

Usage:
    python seed_topics_broad.py                    # dry run: prints scope, no AI calls
    python seed_topics_broad.py --apply             # generate + persist for every course
    python seed_topics_broad.py --apply --limit 50  # cap how many courses this run
                                                      # processes (resume later for the rest)
    python seed_topics_broad.py --apply --course CSC201   # just one course code, any level
"""
import sys

APPLY = '--apply' in sys.argv
LIMIT = None
ONLY_COURSE_CODE = None
ONLY_DEPARTMENT = None
for i, arg in enumerate(sys.argv):
    if arg == '--limit' and i + 1 < len(sys.argv):
        LIMIT = int(sys.argv[i + 1])
    if arg == '--course' and i + 1 < len(sys.argv):
        ONLY_COURSE_CODE = sys.argv[i + 1].strip().upper()
    if arg == '--department' and i + 1 < len(sys.argv):
        ONLY_DEPARTMENT = sys.argv[i + 1].strip()


def main():
    from app import app, db
    from models import Course, Department
    from services.ai_service import generate_course_topics

    with app.app_context():
        query = Course.query.filter(~Course.topics.any())  # only courses with zero topics so far
        if ONLY_COURSE_CODE:
            query = query.filter(db.func.upper(Course.code) == ONLY_COURSE_CODE)
        if ONLY_DEPARTMENT:
            query = query.join(Department).filter(db.func.lower(Department.name) == ONLY_DEPARTMENT.lower())
        courses = query.order_by(Course.department_id, Course.level, Course.code).all()

        if LIMIT:
            courses = courses[:LIMIT]

        print(f"{len(courses)} course(s) with no topics yet, in scope for this run.")
        if not APPLY:
            by_dept = {}
            for c in courses:
                by_dept.setdefault(c.department.name, 0)
                by_dept[c.department.name] += 1
            for dept, count in sorted(by_dept.items(), key=lambda x: -x[1]):
                print(f"  {dept}: {count}")
            print("\nDry run only -- no AI calls made, no changes written. Re-run with --apply.")
            return

        from models import Topic
        succeeded = failed = 0
        for i, course in enumerate(courses):
            try:
                draft = generate_course_topics(course.code, course.title, course.department.name, course.level)

                if draft.get('description') and not course.description:
                    course.description = draft['description']

                titles = [t.strip() for t in (draft.get('topics') or []) if isinstance(t, str) and t.strip()]
                for order, title in enumerate(titles):
                    db.session.add(Topic(course_id=course.id, title=title, order=order, content_source='ai_draft'))

                db.session.commit()
                succeeded += 1
            except Exception as e:
                # Covers both the AI call (network/API failures) and the commit itself
                # (a dropped DB connection mid-commit) -- either way the session must be
                # rolled back before the next iteration's queries, or every subsequent
                # course fails too with a cascading PendingRollbackError even though
                # nothing is actually wrong with them.
                db.session.rollback()
                print(f"[FAIL] {course.code} ({course.department.name}): {e}")
                failed += 1
                continue

            if (i + 1) % 10 == 0:
                print(f"[{i + 1}/{len(courses)}] ok={succeeded} failed={failed} -- last: {course.code} ({len(titles)} topics)")

        print(f"\nDONE. {succeeded} course(s) seeded with topic outlines, {failed} failed.")


if __name__ == '__main__':
    main()
