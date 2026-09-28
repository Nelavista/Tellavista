"""PRD §5.2 sequential academic onboarding: University → Faculty → Department →
Level → Academic Session → Semester → Courses, each step filtered by the prior
selection, ending in multi-select course enrollment (the PRD's `Enrollment` rows).

Relationship to the legacy single-shot profile-completion modal: that modal stays and
still enforces its minimum (name/university/faculty/department/level/semester) via
utils/helpers.check_profile_complete -- a §5.2-compliant flow cannot require every
student to re-run a 7-step wizard when the modal already captured the essentials, and
replacing it wholesale would be a bigger product change than this MVP stage warrants.
This flow is the *deep* onboarding: it adds the session/semester dimension (real
AcademicSession/Semester rows -- the tables Step 3 of the migration plan added), the
per-step filtered course list, multi-select enrollment, and waitlist capture for
students whose university/department isn't in the taxonomy yet.

Read-only taxonomy data comes from the same seeders the admin CRUD writes
(scripts/seed/seed_academia.py); sessions/semesters appear only when an admin has
entered them -- the codebase-wide "never invent sourced data" policy.
"""
from app.extensions import db
from app.models import (AcademicSession, Course, Department, Enrollment,
                        Faculty, Semester, University)
from app.services.academic_context import resolve_academic_context, sync_user_university

# Free-text fallback kept deliberately short and empty-safe: the taxonomy does not
# cover every Nigerian university yet, and §5.2 requires "graceful handling" --
# capture who's waiting rather than dead-ending them.
ONBOARDING_LEVELS = ['100', '200', '300', '400', '500']
MAX_COURSES_PER_ENROLLMENT = 12


def get_onboarding_options(user):
    """Everything the wizard's first renders need, resolved from the user's current
    profile so a returning student sees their own context pre-selected."""
    universities = (
        University.query.filter_by(active=True).order_by(University.name).all()
    )
    ctx = resolve_academic_context(user)
    return {
        'universities': [{'id': u.id, 'name': u.name, 'short_name': u.short_name} for u in universities],
        'levels': ONBOARDING_LEVELS,
        'resolved': ctx.resolved,
        'current': {
            'university': user.university,
            'faculty': user.faculty,
            'department': user.department,
            'level': user.level,
            'semester': user.semester,
        },
    }


def faculties_for(university_name):
    """Faculties of one active university, filtered by the prior step (§5.2)."""
    uni = University.query.filter(
        db.func.lower(University.name) == (university_name or '').strip().lower(),
        University.active == True,  # noqa: E712
    ).first()
    if not uni:
        return []
    return [{'id': f.id, 'name': f.name} for f in uni.faculties.order_by(Faculty.name).all()]


def departments_for(university_name, faculty_name):
    """Departments of one faculty, filtered by the university picked before it."""
    uni = University.query.filter(
        db.func.lower(University.name) == (university_name or '').strip().lower(),
        University.active == True,  # noqa: E712
    ).first()
    if not uni:
        return []
    fac = Faculty.query.filter(
        Faculty.university_id == uni.id,
        db.func.lower(Faculty.name) == (faculty_name or '').strip().lower(),
    ).first()
    if not fac:
        return []
    return [{'id': d.id, 'name': d.name} for d in fac.departments.order_by(Department.name).all()]


def sessions_for(university_name):
    """Academic sessions recorded for this university. Empty until an admin enters
    them -- the wizard degrades gracefully rather than inventing labels."""
    uni = University.query.filter(
        db.func.lower(University.name) == (university_name or '').strip().lower(),
        University.active == True,  # noqa: E712
    ).first()
    if not uni:
        return []
    rows = (
        AcademicSession.query.filter_by(university_id=uni.id, is_active=True)
        .order_by(AcademicSession.label.desc())
        .all()
    )
    return [{'id': s.id, 'label': s.label, 'semesters': [sem.to_dict() for sem in s.semesters]} for s in rows]


def courses_for(university_name, department_name, level):
    """Courses for the final multi-select step: scoped to the picked university's
    department and the picked level (per-step filtering, §5.2)."""
    uni = University.query.filter(
        db.func.lower(University.name) == (university_name or '').strip().lower(),
        University.active == True,  # noqa: E712
    ).first()
    if not uni or not level:
        return []
    dept = (
        Department.query.join(Faculty)
        .filter(
            Faculty.university_id == uni.id,
            db.func.lower(Department.name) == (department_name or '').strip().lower(),
        )
        .first()
    )
    if not dept:
        return []
    rows = (
        Course.query.filter_by(department_id=dept.id, level=str(level).strip())
        .order_by(Course.code)
        .all()
    )
    return [{'id': c.id, 'code': c.code, 'title': c.title, 'semester': c.semester} for c in rows]


def already_enrolled_course_ids(user):
    return {e.course_id for e in Enrollment.query.filter_by(user_id=user.id).all()}


def save_onboarding(user, data):
    """Persist the wizard's result: profile fields (the same ones the legacy modal
    writes, so every existing reader keeps working), optional session/semester, and
    Enrollment rows for the multi-selected courses.

    Returns (ok, error_or_none). Course ids are validated against the student's own
    resolved department+level -- a hand-crafted POST can't enroll someone in another
    faculty's course (§5.2's "final course list matches selected dept/level/semester").
    """
    university = (data.get('university') or '').strip()
    faculty = (data.get('faculty') or '').strip()
    department = (data.get('department') or '').strip()
    level = (data.get('level') or '').strip()
    semester = (data.get('semester') or '').strip()
    session_id = data.get('session_id')
    semester_id = data.get('semester_id')
    course_ids = data.get('course_ids') or []

    if not all([university, faculty, department, level]):
        return False, 'University, faculty, department and level are required.'

    session_row = semester_row = None
    if session_id is not None:
        session_row = AcademicSession.query.get(session_id)
        if not session_row:
            return False, 'Selected academic session was not found.'
    if semester_id is not None:
        semester_row = Semester.query.get(semester_id)
        if not semester_row or (session_row and semester_row.session_id != session_row.id):
            return False, 'Selected semester does not belong to the chosen session.'

    # Profile fields first (legacy readers depend on the free-text strings).
    user.name = user.name or (data.get('name') or '').strip() or user.name
    sync_user_university(user, university)
    user.faculty = faculty
    user.department = department
    user.level = level
    if semester:
        user.semester = semester

    # Enrollment rows -- validated against the student's own (university, department,
    # level) scope, so nothing cross-department can slip in via a forged payload.
    valid_course_ids = {c['id'] for c in courses_for(university, department, level)}
    existing = already_enrolled_course_ids(user)
    requested = []
    for cid in course_ids:
        try:
            cid = int(cid)
        except (TypeError, ValueError):
            continue
        if cid in valid_course_ids and cid not in existing and cid not in requested:
            requested.append(cid)
    if len(requested) > MAX_COURSES_PER_ENROLLMENT:
        return False, f'You can enroll in at most {MAX_COURSES_PER_ENROLLMENT} courses here.'

    for cid in requested:
        db.session.add(Enrollment(
            user_id=user.id, course_id=cid,
            session_id=session_row.id if session_row else None,
            semester_id=semester_row.id if semester_row else None,
        ))
    db.session.commit()
    return True, None


def save_waitlist(user, university_name, department_name, level=None):
    """§5.2's "graceful handling when a university/department isn't yet in the system":
    capture the request as a Notification to staff (the platform's existing generic
    message store -- no new table, nothing invented), and return whether the student's
    school is actually missing so the UI can say the honest thing."""
    uni = University.query.filter(
        db.func.lower(University.name) == (university_name or '').strip().lower()
    ).first()
    if uni:
        fac = (
            Faculty.query.filter_by(university_id=uni.id)
            .filter(db.func.lower(Faculty.name) == (department_name or '').strip().lower())
            .first()
        )
        # University exists; check the department specifically.
        dept = (
            Department.query.join(Faculty)
            .filter(
                Faculty.university_id == uni.id,
                db.func.lower(Department.name) == (department_name or '').strip().lower(),
            )
            .first()
        )
        if dept:
            return {'status': 'exists', 'university_known': True, 'department_known': True}
        message = f"Onboarding waitlist: {department_name or '(no department given)'} at {uni.name}"
        if level:
            message += f", {level} level"
        message += "."
        known = {'university_known': True, 'department_known': False}
    else:
        message = f"Onboarding waitlist: {university_name or '(no university given)'}"
        if department_name:
            message += f" / {department_name}"
        if level:
            message += f", {level} level"
        message += "."
        known = {'university_known': False, 'department_known': False}

    from app.services.notification_service import notify
    notify(
        user.id, 'onboarding_waitlist',
        'Course catalogue request received',
        message,
        link_url='/onboarding',
    )
    return {'status': 'waitlisted', **known}
