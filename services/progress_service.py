"""Real, activity-based academic progress -- no invented numbers. Every function here
reads or writes actual student activity (materials opened, CBT attempts); nothing is
estimated or defaulted to a nonzero value."""
from datetime import datetime

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
    never auto-scored (score_pct is always 0 for them, which would skew an average)."""
    query = CBTAttempt.query.filter_by(user_id=user.id)
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
