"""Academia Settings -- the student's real control center (templates/settings.html).

Every preference here is backed by models.UserPreferences (one row per user, created
lazily) and has exactly one real consumer elsewhere in the app -- see the comment above
each column in models.py. This blueprint intentionally does NOT duplicate anything
Profile already owns (name/university/faculty/department/level/semester -- see
routes/profile_routes.py) or anything Skills' own settings own (bio/portfolio/photo/
CGPA/employer-visibility -- see routes/skills_routes.py's edit_profile/privacy_settings).
"""
import json
from datetime import datetime

from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify, Response

from extensions import db, limiter
from models import User, UserPreferences, UserQuestions, CBTAttempt, TopicProgress, TutorConversation
from utils.helpers import login_required
from services.academic_context import resolve_academic_context

settings_bp = Blueprint('settings', __name__)

# One entry per UserPreferences column exposed to Settings. A set of strings = allowed
# enum values; 'bool' / 'text' = coerced by type. Anything not listed here can never be
# written by /settings/update, no matter what a request sends.
_PREF_FIELDS = {
    'theme': {'light', 'dark', 'system'},
    'ai_response_style': {'concise', 'balanced', 'detailed'},
    'ai_teaching_approach': {'step_by_step', 'concept_first', 'example_first', 'exam_focused'},
    'ai_difficulty': {'beginner', 'university', 'advanced'},
    'ai_use_academic_context': 'bool',
    'ai_use_conversation_history': 'bool',
    'ai_personal_context': 'text',
    'cbt_default_mode': {'cbt', 'written'},
    'cbt_auto_explain': 'bool',
    'notify_cbt_results': 'bool',
}

_RESET_SCOPES = {
    'appearance': ['theme'],
    'ai_tutor': ['ai_response_style', 'ai_teaching_approach', 'ai_difficulty',
                 'ai_use_academic_context', 'ai_use_conversation_history', 'ai_personal_context'],
    'study': ['cbt_default_mode', 'cbt_auto_explain'],
    'notifications': ['notify_cbt_results'],
    'all': list(_PREF_FIELDS.keys()),
}


def _current_user():
    username = session['user']['username']
    return User.query.filter_by(username=username).first()


def _get_or_create_prefs(user):
    prefs = UserPreferences.query.filter_by(user_id=user.id).first()
    if not prefs:
        prefs = UserPreferences(user_id=user.id)
        db.session.add(prefs)
        db.session.commit()
    return prefs


@settings_bp.route('/settings')
@login_required
def settings():
    user = _current_user()
    prefs = _get_or_create_prefs(user)
    ctx = resolve_academic_context(user)
    return render_template(
        'settings.html', user=user, prefs=prefs, ctx=ctx,
        has_password=bool(user.password_hash),
        active_page='settings',
    )


@settings_bp.route('/settings/update', methods=['POST'])
@login_required
def update_preference():
    """One generic, whitelisted setter used by every immediate-save control on the
    Settings page -- a select/toggle posts {field, value} and gets the saved value back,
    no page reload, no giant form. See _PREF_FIELDS above for exactly what's writable."""
    user = _current_user()
    prefs = _get_or_create_prefs(user)

    body = request.get_json(silent=True) or {}
    field = body.get('field')
    value = body.get('value')

    if field not in _PREF_FIELDS:
        return jsonify({'success': False, 'error': 'Unknown field'}), 400

    kind = _PREF_FIELDS[field]
    if kind == 'bool':
        value = bool(value)
    elif kind == 'text':
        value = (value or '').strip()[:2000] or None
    else:  # enum set
        if value not in kind:
            return jsonify({'success': False, 'error': 'Invalid value'}), 400

    setattr(prefs, field, value)
    db.session.commit()
    return jsonify({'success': True, 'field': field, 'value': value})


@settings_bp.route('/settings/reset', methods=['POST'])
@login_required
def reset_preferences():
    user = _current_user()
    prefs = _get_or_create_prefs(user)

    body = request.get_json(silent=True) or {}
    scope = body.get('scope')
    fields = _RESET_SCOPES.get(scope)
    if not fields:
        return jsonify({'success': False, 'error': 'Unknown reset scope'}), 400

    for field in fields:
        setattr(prefs, field, UserPreferences.DEFAULTS[field])
    db.session.commit()
    return jsonify({'success': True, 'scope': scope, 'values': {f: getattr(prefs, f) for f in fields}})


@settings_bp.route('/settings/clear-ai-history', methods=['POST'])
@login_required
@limiter.limit('10 per hour')
def clear_ai_history():
    """Deletes every UserQuestions row Nelavista has logged from this student's AI Tutor
    chats (routes/ai_routes.py's /ask, /ask_with_files) and resets the current session's
    short-term chat memory. Deliberately does NOT touch TutorConversation/TutorMessage
    (the newer /ai-tutor's threaded chats) -- those are a browsable resource the student
    manages one conversation at a time from that page's own delete button, not a single
    bulk "history" a Settings toggle should wipe unannounced. Also does not touch
    CBTAttempt/TopicProgress -- that is academic record (learning progress), not AI
    personalization data; see templates/settings.html's Privacy & Data copy."""
    user = _current_user()
    UserQuestions.query.filter_by(username=user.username).delete()
    db.session.commit()
    session['chat_memory'] = []
    return jsonify({'success': True})


@settings_bp.route('/settings/export')
@login_required
@limiter.limit('5 per hour')
def export_data():
    user = _current_user()
    prefs = _get_or_create_prefs(user)
    questions = UserQuestions.query.filter_by(username=user.username).order_by(UserQuestions.timestamp).all()
    attempts = CBTAttempt.query.filter_by(user_id=user.id).order_by(CBTAttempt.started_at).all()
    topic_progress = TopicProgress.query.filter_by(user_id=user.id).all()
    # Ask Nelavista's Q&A log (UserQuestions, above) and the newer /ai-tutor's threaded
    # conversations (TutorConversation/TutorMessage) are two different tables -- both are
    # real AI Tutor history, so both belong in a "download everything" export even though
    # only the former is covered by the "Clear history" button (see clear_ai_history's
    # docstring for why threaded conversations are deleted one at a time from /ai-tutor
    # itself instead).
    conversations = (TutorConversation.query.filter_by(user_id=user.id)
                      .order_by(TutorConversation.created_at).all())

    payload = {
        'exported_at': datetime.utcnow().isoformat() + 'Z',
        'profile': {
            'username': user.username, 'email': user.email, 'name': user.name,
            'university': user.university, 'faculty': user.faculty,
            'department': user.department, 'level': user.level, 'semester': user.semester,
            'joined_on': user.joined_on.isoformat() if user.joined_on else None,
        },
        'preferences': prefs.to_dict(),
        'ask_nelavista_history': [
            {'question': q.question, 'answer': q.answer, 'timestamp': q.timestamp.isoformat() if q.timestamp else None}
            for q in questions
        ],
        'ai_tutor_conversations': [
            {
                'id': c.id, 'title': c.title, 'created_at': c.created_at.isoformat() if c.created_at else None,
                'course': c.course.code if c.course else None, 'topic': c.topic.title if c.topic else None,
                'messages': [{'role': m.role, 'content': m.content,
                              'timestamp': m.created_at.isoformat() if m.created_at else None}
                             for m in c.messages],
            }
            for c in conversations
        ],
        'mock_exam_attempts': [a.to_dict() for a in attempts],
        'topic_progress': [
            {'topic_id': tp.topic_id, 'topic_title': tp.topic.title if tp.topic else None,
             'completed_at': tp.completed_at.isoformat() if tp.completed_at else None}
            for tp in topic_progress
        ],
    }
    body = json.dumps(payload, indent=2)
    return Response(
        body, mimetype='application/json',
        headers={'Content-Disposition': f'attachment; filename=nelavista-data-{user.username}.json'},
    )


@settings_bp.route('/account/change-password', methods=['POST'])
@login_required
@limiter.limit('10 per hour')
def change_password():
    user = _current_user()
    if not user.password_hash:
        flash('Your account signs in with Google, so there is no password to change.')
        return redirect(url_for('settings.settings'))

    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')

    if not user.check_password(current_password):
        flash('Current password is incorrect.')
    elif len(new_password) < 8:
        flash('New password must be at least 8 characters.')
    elif new_password != confirm_password:
        flash('New passwords do not match.')
    else:
        user.set_password(new_password)
        db.session.commit()
        flash('Password updated.')
    return redirect(url_for('settings.settings'))


@settings_bp.route('/account/delete', methods=['POST'])
@login_required
@limiter.limit('5 per hour')
def delete_account():
    """Anonymize-and-deactivate, not a hard row delete: dozens of tables across Academia
    and Skills carry a user_id FK back to this row (CBTAttempt, TutorConversation,
    StudentProject, GroupMessage, MessageThread, ...), most without ON DELETE CASCADE, so
    actually deleting the row would either violate FK constraints or silently orphan rows
    all over the schema. This scrubs every personally-identifying field, blocks future
    login (is_deleted), and signs the current session out -- functionally "deleted" from
    the student's perspective, safe for every other table that references them."""
    user = _current_user()

    confirm_text = request.form.get('confirm_text', '').strip()
    password = request.form.get('password', '')

    if confirm_text != 'DELETE':
        flash('Type DELETE to confirm account deletion.')
        return redirect(url_for('settings.settings'))
    if user.password_hash and not user.check_password(password):
        flash('Incorrect password.')
        return redirect(url_for('settings.settings'))

    user.username = f'deleted_user_{user.id}'
    user.email = f'deleted_{user.id}@deleted.nelavista.com'
    user.password_hash = None
    user.google_sub = None
    user.name = None
    user.university = None
    user.faculty = None
    user.department = None
    user.level = None
    user.semester = None
    user.bio = None
    user.portfolio_url = None
    user.profile_photo_url = None
    user.academic_cgpa = None
    user.is_deleted = True
    user.deleted_at = datetime.utcnow()
    db.session.commit()

    session.clear()
    flash('Your account has been deleted.')
    return redirect(url_for('auth.login'))
