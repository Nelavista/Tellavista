"""PRD §6 feedback loop (G10) + §21 usage monitoring (G6).

The loop's contract: a student flags an AI answer (ownership-checked), the flag lands
in exactly one open queue entry per (user, feature, reference), and an admin resolves
or dismisses it. Usage logging must count calls without ever storing prompt content.
"""
import json
from unittest.mock import patch, MagicMock

import pytest

from app.extensions import db
from app.models import AIUsageLog, CBTAnswer, CBTAttempt, CBTQuestion, FlaggedAIAnswer, User
from app.services.ai_monitoring import (flag_answer, open_flags, resolve_flag,
                                        log_ai_usage, usage_summary)


def _seed_attempt_with_answer(app, make_user, username='flaguser'):
    user = make_user(username)
    with app.app_context():
        q = CBTQuestion(subject_code='CSC', course_code='CSC213', question_type='cbt',
                        question_text='2+2=?', options_json=json.dumps(['3', '4', '5', '6']),
                        correct_index=1, explanation='basic addition')
        db.session.add(q)
        db.session.flush()
        attempt = CBTAttempt(user_id=user.id, course_code='CSC213', question_type='cbt',
                             total_questions=1, correct_count=0, score_pct=0,
                             submitted_at=__import__('datetime').datetime.utcnow())
        attempt.issued_question_ids = [q.id]
        db.session.add(attempt)
        db.session.flush()
        ans = CBTAnswer(attempt_id=attempt.id, question_id=q.id,
                        question_text=q.question_text, selected_index=0, is_correct=False)
        db.session.add(ans)
        db.session.commit()
        return user.id, ans.id


def test_flag_endpoint_requires_ownership(app, client, make_user, login_as):
    owner_id, answer_id = _seed_attempt_with_answer(app, make_user, 'flagowner')
    other = make_user('flagother')
    login_as(client, other)

    res = client.post('/api/ai/flag', json={'feature': 'cbt_explain', 'reference_id': answer_id})
    assert res.status_code == 404        # someone else's answer: indistinguishable from missing
    with app.app_context():
        assert FlaggedAIAnswer.query.count() == 0


def test_flag_endpoint_creates_single_open_flag(app, client, make_user, login_as):
    user_id, answer_id = _seed_attempt_with_answer(app, make_user)
    user = User.query.get(user_id) if app.app_context() else None
    login_as(client, user)

    r1 = client.post('/api/ai/flag', json={'feature': 'cbt_explain', 'reference_id': answer_id,
                                           'note': 'The explanation is wrong'})
    assert r1.get_json()['success'] is True
    r2 = client.post('/api/ai/flag', json={'feature': 'cbt_explain', 'reference_id': answer_id})
    body = r2.get_json()
    assert body['success'] is True
    assert 'already' in body['message'].lower()

    with app.app_context():
        flags = FlaggedAIAnswer.query.filter_by(user_id=user_id, feature='cbt_explain',
                                                reference_id=answer_id).all()
        assert len(flags) == 1               # deduplicated, not stacked
        assert flags[0].status == 'open'
        assert flags[0].note == 'The explanation is wrong'


def test_admin_resolve_and_dismiss(app, client, make_user, login_as):
    user_id, answer_id = _seed_attempt_with_answer(app, make_user)
    with app.app_context():
        user = User.query.get(user_id)
        ok, _ = flag_answer(user, 'cbt_explain', reference_id=answer_id, note='wrong')
        assert ok is True
        flags = open_flags()
        assert len(flags) == 1
        flag_id = flags[0].id

    admin = make_user('flagadmin', is_admin=True)
    login_as(client, admin)
    res = client.post(f'/admin/ai-flags/{flag_id}/resolve',
                      json={'status': 'resolved', 'note': 'Explanation corrected'})
    assert res.status_code == 200

    with app.app_context():
        flag = FlaggedAIAnswer.query.get(flag_id)
        assert flag.status == 'resolved'
        assert flag.resolved_at is not None
        assert flag.resolution_note == 'Explanation corrected'
        assert open_flags() == []            # queue is empty after resolution

    # Double-resolve is rejected (flag is no longer open).
    res2 = client.post(f'/admin/ai-flags/{flag_id}/resolve', json={'status': 'resolved'})
    assert res2.status_code == 400


def test_usage_logging_never_stores_content(app, make_user):
    user = make_user('usageuser')
    with app.app_context():
        log_ai_usage(user.id, 'tutor', model='openai/gpt-4o-mini',
                     prompt_tokens=120, completion_tokens=340, ok=True)
        row = AIUsageLog.query.filter_by(user_id=user.id, feature='tutor').first()
        assert row is not None
        assert row.prompt_tokens == 120 and row.completion_tokens == 340
        # The table has no column that could hold prompt/response content.
        cols = {c['name'] for c in db.session.execute(
            "PRAGMA table_info(ai_usage_log)").keys()} if False else \
            {c.name for c in AIUsageLog.__table__.columns}
        assert 'content' not in cols and 'prompt' not in cols and 'response' not in cols


def test_usage_summary_rolls_up_by_feature(app, make_user):
    user = make_user('usageuser2')
    with app.app_context():
        log_ai_usage(user.id, 'rag', model='m', prompt_tokens=10, completion_tokens=20, ok=True)
        log_ai_usage(user.id, 'rag', model='m', prompt_tokens=5, completion_tokens=0, ok=False)
        summary = usage_summary(days=30)
    rag = summary['rag']
    assert rag['calls'] == 2
    assert rag['ok_calls'] == 1
    assert rag['prompt_tokens'] == 15 and rag['completion_tokens'] == 20
    assert rag['users'] == 1
