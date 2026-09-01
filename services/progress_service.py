"""Real, activity-based academic progress -- no invented numbers. Every function here
reads or writes actual student activity (materials opened, CBT attempts); nothing is
estimated or defaulted to a nonzero value."""
from datetime import datetime

from sqlalchemy import func

from extensions import db
from models import MaterialView, Material, CBTAttempt


def record_material_view(user, material):
    """Upsert one (user, material) view -- bumps the timestamp on repeat views rather
    than inserting duplicate rows, and increments Material.views (previously a dead
    column, never incremented anywhere)."""
    view = MaterialView.query.filter_by(user_id=user.id, material_id=material.id).first()
    if view:
        view.viewed_at = datetime.utcnow()
    else:
        view = MaterialView(user_id=user.id, material_id=material.id)
        db.session.add(view)
    material.views = (material.views or 0) + 1
    db.session.commit()


def get_recent_material_views(user, limit=5):
    """Most recently viewed materials, newest first -- one row per distinct material."""
    return (
        MaterialView.query.filter_by(user_id=user.id)
        .order_by(MaterialView.viewed_at.desc())
        .limit(limit)
        .all()
    )


def get_cbt_summary(user, course_code=None):
    """{attempts_count, average_score, last_attempt} from real CBTAttempt rows only --
    average_score is over 'cbt' (auto-scored) attempts, since written attempts are
    never auto-scored (score_pct is always 0 for them, which would skew an average).

    Only ever counts attempts that were actually submitted. start_cbt_attempt() (see
    routes/cbt_routes.py) creates the row up front with submitted_at=None and
    score_pct=0, then fills in the real result on submit -- a student who starts an
    exam and never finishes it (closes the tab, opens a second tab and starts over,
    double-clicks "Start Exam") would otherwise leave a phantom 0% attempt sitting in
    this query forever, dragging average_score down and, worse, potentially winning
    "last_attempt" outright over a real finished result (submitted_at=NULL sorts before
    every real timestamp on a DESC order in Postgres)."""
    query = CBTAttempt.query.filter(CBTAttempt.user_id == user.id, CBTAttempt.submitted_at.isnot(None))
    if course_code:
        query = query.filter_by(course_code=course_code.upper())
    attempts = query.order_by(CBTAttempt.submitted_at.desc()).all()

    scored = [a for a in attempts if a.question_type == 'cbt']
    average_score = round(sum(a.score_pct for a in scored) / len(scored)) if scored else None

    last = attempts[0] if attempts else None
    return {
        'attempts_count': len(attempts),
        'average_score': average_score,
        'last_attempt': {
            'course_code': last.course_code,
            'score_pct': last.score_pct,
            'question_type': last.question_type,
            'submitted_at': last.submitted_at.isoformat() if last.submitted_at else None,
        } if last else None,
    }


def get_course_materials_progress(user, course_code):
    """(viewed_count, total_count) of approved materials for one course code, for this
    student -- used by the course page's Progress section."""
    total_count = Material.query.filter(
        Material.course_code.ilike(course_code), Material.is_approved == True  # noqa: E712
    ).count()
    if total_count == 0:
        return 0, 0
    viewed_count = (
        MaterialView.query.join(Material, MaterialView.material_id == Material.id)
        .filter(MaterialView.user_id == user.id, Material.course_code.ilike(course_code))
        .count()
    )
    return viewed_count, total_count


def get_courses_materials_progress_bulk(user, course_codes):
    """Same (viewed, total) pairs as get_course_materials_progress, for many course
    codes at once -- 2 queries total instead of up to 2 per course. Built for
    /api/user-courses, where looping the single-course helper turned a student with N
    courses into 2-3N remote round-trips (the real cause of a slow-loading course list --
    each courses-taxonomy query call was 100 courses+, not a page-load-once cost).
    Matching is case-insensitive (uppercased on both sides) to mirror the single-course
    helper's .ilike(); codes not present in the result had zero approved materials."""
    if not course_codes:
        return {}
    upper_codes = [c.upper() for c in course_codes]

    totals = dict(
        db.session.query(func.upper(Material.course_code), func.count(Material.id))
        .filter(func.upper(Material.course_code).in_(upper_codes), Material.is_approved == True)  # noqa: E712
        .group_by(func.upper(Material.course_code))
        .all()
    )
    if not totals:
        return {code: (0, 0) for code in course_codes}

    viewed = dict(
        db.session.query(func.upper(Material.course_code), func.count(MaterialView.id))
        .join(Material, MaterialView.material_id == Material.id)
        .filter(MaterialView.user_id == user.id, func.upper(Material.course_code).in_(upper_codes))
        .group_by(func.upper(Material.course_code))
        .all()
    )

    return {code: (viewed.get(code.upper(), 0), totals.get(code.upper(), 0)) for code in course_codes}
