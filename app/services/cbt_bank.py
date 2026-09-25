"""One place that resolves a course code to its CBTQuestion bank -- used by both
routes/cbt_routes.py (start/count an attempt) and routes/academia_routes.py (the course
detail page's CBT/written counts), so the two screens can never disagree about what's
available for a course the way they used to when each file kept its own duplicate
subject-prefix-matching helper.

Matches on the exact, normalized course code (e.g. "CSC101"), not the old 3-letter
subject prefix -- a course's bank is its own, never shared with every other course
under the same subject (see models.py's CBTQuestion.course_code)."""
from app.extensions import db
from app.models import CBTQuestion


def normalize_course_code(course_code):
    return (course_code or '').strip().upper() or None


def question_bank_query(course_code, question_type, user=None):
    """Base query for one course's active questions of one type, scoped to the
    requesting student's university the same 'universal (NULL) + specific' way
    Material.university already works (see routes/materials_routes.py) -- a row with
    university_id set only shows to students at that university; NULL shows to everyone.
    Returns an empty, never-executed query if course_code doesn't normalize to anything."""
    code = normalize_course_code(course_code)
    query = CBTQuestion.query.filter_by(
        course_code=code, question_type=question_type, is_active=True,
    )
    if code is None:
        query = query.filter(db.false())
    if user and user.university_id:
        query = query.filter(
            db.or_(CBTQuestion.university_id.is_(None), CBTQuestion.university_id == user.university_id)
        )
    return query


def question_counts(course_code, user=None):
    """{'cbt': n, 'written': n} for one course -- used to honestly show/disable the
    exam-type cards without ever shipping the questions themselves."""
    return {
        'cbt': question_bank_query(course_code, 'cbt', user).count(),
        'written': question_bank_query(course_code, 'written', user).count(),
    }
