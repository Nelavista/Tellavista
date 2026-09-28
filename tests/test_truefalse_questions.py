"""PRD §5.6: true/false question type.

T/F questions are stored as two-option 'truefalse' rows (index 0=True, 1=False) and
flow through the same auto-scored pipeline as 'cbt' -- grading, scoring, timing,
counts, mastery write-back and insights all treat them as first-class scored formats.
"""
import json


from app.extensions import db
from app.models import CBTQuestion, CBTAttempt, User
from app.services.cbt_bank import question_counts
from app.routes.cbt_routes import cbt_time_limit_seconds
from app.services.insights_service import get_performance_summary


def _seed_tf(app, course_code='CSC213', count=3, correct='True'):
    with app.app_context():
        rows = []
        for i in range(count):
            rows.append(CBTQuestion(
                subject_code='CSC', course_code=course_code, question_type='truefalse',
                question_text=f'Statement {i} is accurate.',
                options_json=json.dumps(['True', 'False']),
                correct_index=0 if correct == 'True' else 1,
                explanation=f'Statement {i} is {correct.lower()}.',
            ))
        db.session.add_all(rows)
        db.session.commit()
        return [r.id for r in rows]


def test_counts_include_truefalse(app, make_user):
    user = make_user('tf1')
    _seed_tf(app)
    with app.app_context():
        counts = question_counts('CSC213', User.query.get(user.id))
    assert counts['truefalse'] == 3
    assert counts['cbt'] == 0 and counts['written'] == 0


def test_tf_is_timed_like_cbt():
    assert cbt_time_limit_seconds('truefalse', 3) == cbt_time_limit_seconds('cbt', 3)
    assert cbt_time_limit_seconds('truefalse', 3) is not None
    assert cbt_time_limit_seconds('written', 3) is None


def test_tf_start_and_grade_end_to_end(app, client, make_user, login_as):
    user = make_user('tf2')
    ids = _seed_tf(app)
    login_as(client, user)

    start = client.post('/api/cbt/start', json={'course_code': 'CSC213', 'question_type': 'truefalse'})
    data = start.get_json()
    assert data['success'] is True
    assert data['time_limit_seconds'] is not None
    for q in data['questions']:
        assert q['options'] == ['True', 'False']
        assert set(q.keys()) == {'id', 'subject_code', 'question_type', 'question_text', 'options'}

    # Answer everything correctly: index 0 everywhere (all seeded True).
    answers = {str(qid): 0 for qid in ids}
    res = client.post(f"/CBT/submit/{data['attempt_id']}", json={'answers': answers, 'duration_seconds': 30})
    result = res.get_json()
    assert result['success'] is True
    assert result['score_pct'] == 100
    assert result['correct_count'] == 3

    # Selecting index 1 (False) on a True-statement grades wrong.
    start2 = client.post('/api/cbt/start', json={'course_code': 'CSC213', 'question_type': 'truefalse'})
    d2 = start2.get_json()
    wrong = {str(qid): 1 for qid in ids}
    res2 = client.post(f"/CBT/submit/{d2['attempt_id']}", json={'answers': wrong, 'duration_seconds': 10})
    assert res2.get_json()['score_pct'] == 0


def test_tf_feeds_performance_summary(app, make_user):
    """A T/F attempt must count toward the dashboard's quiz average -- it's
    auto-scored, exactly like CBT."""
    user = make_user('tf3')
    ids = _seed_tf(app)
    with app.app_context():
        from datetime import datetime
        attempt = CBTAttempt(user_id=user.id, course_code='CSC213', question_type='truefalse',
                             total_questions=3, correct_count=2, score_pct=67,
                             started_at=datetime.utcnow(), submitted_at=datetime.utcnow())
        attempt.issued_question_ids = ids
        db.session.add(attempt)
        db.session.commit()
        summary = get_performance_summary(User.query.get(user.id))
    assert summary['quiz_average'] == 67
    assert summary['cbt_attempts'] == 1
