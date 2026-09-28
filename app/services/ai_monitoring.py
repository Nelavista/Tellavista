"""AI usage/cost tracking (G6) and the flagged-answer feedback loop (G10) -- PRD §21/§6.

Usage logging: one best-effort row per AI feature call. Best-effort is a hard rule --
an analytics failure must never break the AI response it measured, so every write is
wrapped and swallowed.

Flagging: students report an incorrect AI answer (from the CBT review screen today,
extensible to the tutor tomorrow); admins resolve the queue in /admin. The feedback
loop is the PRD §6 accuracy mechanism: flagged answers are countable, reviewable and
resolvable -- not a black hole.
"""
from datetime import datetime

from app.extensions import db
from app.models import AIUsageLog, FlaggedAIAnswer


def log_ai_usage(user_id, feature, model=None, prompt_tokens=None, completion_tokens=None,
                 ok=None):
    """Record one AI call. Never raises -- see module docstring."""
    try:
        db.session.add(AIUsageLog(
            user_id=user_id, feature=feature, model=model,
            prompt_tokens=prompt_tokens, completion_tokens=completion_tokens, ok=ok,
        ))
        db.session.commit()
    except Exception:
        db.session.rollback()


def log_usage_from_response(user_id, feature, model, data):
    """Extract OpenAI-shaped usage from a parsed response JSON and log it."""
    usage = {}
    if isinstance(data, dict):
        usage = data.get('usage') or {}
    log_ai_usage(
        user_id, feature, model,
        prompt_tokens=usage.get('prompt_tokens'),
        completion_tokens=usage.get('completion_tokens'),
        ok=True,
    )


def usage_summary(days=30):
    """Platform-wide per-feature rollup for the admin analytics page:
    {feature: {calls, ok_calls, prompt_tokens, completion_tokens, users}}."""
    from datetime import timedelta
    from sqlalchemy import func
    since = datetime.utcnow() - timedelta(days=days)
    rows = (
        db.session.query(
            AIUsageLog.feature,
            func.count(AIUsageLog.id).label('calls'),
            func.sum(db.case((AIUsageLog.ok == True, 1), else_=0)).label('ok_calls'),  # noqa: E712
            func.coalesce(func.sum(AIUsageLog.prompt_tokens), 0).label('prompt_tokens'),
            func.coalesce(func.sum(AIUsageLog.completion_tokens), 0).label('completion_tokens'),
            func.count(db.distinct(AIUsageLog.user_id)).label('users'),
        )
        .filter(AIUsageLog.created_at >= since)
        .group_by(AIUsageLog.feature)
        .all()
    )
    return {
        r.feature: {
            'calls': r.calls, 'ok_calls': int(r.ok_calls or 0),
            'prompt_tokens': int(r.prompt_tokens or 0),
            'completion_tokens': int(r.completion_tokens or 0),
            'users': r.users,
        }
        for r in rows
    }


# ---------------- flagged-answer feedback loop (G10) ----------------

def flag_answer(user, feature, reference_id=None, note=None):
    """A student reports an AI answer as incorrect. One open flag per
    (user, feature, reference_id) -- re-flagging updates the note instead of stacking
    duplicates. Returns (ok, message)."""
    note = (note or '').strip()[:1000] or None
    existing = FlaggedAIAnswer.query.filter_by(
        user_id=user.id, feature=feature,
        reference_id=reference_id, status='open',
    ).first()
    if existing:
        if note:
            existing.note = note
        db.session.commit()
        return True, "We already have your report on this answer — it's in the review queue."
    db.session.add(FlaggedAIAnswer(
        user_id=user.id, feature=feature, reference_id=reference_id, note=note,
    ))
    db.session.commit()
    return True, "Thanks — this answer has been flagged for review."


def open_flags():
    """The admin moderation queue, oldest first (longest-waiting reports first)."""
    return (
        FlaggedAIAnswer.query.filter_by(status='open')
        .order_by(FlaggedAIAnswer.created_at.asc())
        .limit(200)
        .all()
    )


def resolve_flag(flag_id, admin_user, status='resolved', resolution_note=None):
    """Admin decision. status must be 'resolved' or 'dismissed' (both close the flag;
    'resolved' means the content was actually corrected)."""
    if status not in ('resolved', 'dismissed'):
        return False
    flag = FlaggedAIAnswer.query.get(flag_id)
    if not flag or flag.status != 'open':
        return False
    flag.status = status
    flag.resolution_note = (resolution_note or '').strip()[:1000] or None
    flag.resolved_by = admin_user.id
    flag.resolved_at = datetime.utcnow()
    db.session.commit()
    return True
