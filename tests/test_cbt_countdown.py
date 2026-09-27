"""PRD §5.7 CBT countdown: server side of the timed session.

The client (templates/CBT.html) counts down from `time_limit_seconds` and auto-submits
at 0:00. What the server must guarantee:

  - the limit is derived deterministically from the attempt's question count, so client
    and server always agree without a schema change (cbt_time_limit_seconds);
  - written practice stays untimed (None) -- it's a study mode, not an exam;
  - the limit is actually issued on /api/cbt/start;
  - a reported duration can't exceed the limit (a tampered/stopped client clock can't
    record a "duration" longer than the attempt was ever allowed).
"""
import json

import pytest

from app.extensions import db
from app.models import CBTQuestion, CBTAttempt, User
from app.routes.cbt_routes import (cbt_time_limit_seconds, CBT_MIN_TIME_SECONDS,
                                   CBT_SECONDS_PER_QUESTION)


def _seed_questions(app, course_code='MTH101', count=3):
    with app.app_context():
        rows = []
        for i in range(count):
            rows.append(CBTQuestion(
                subject_code='MTH', course_code=course_code, question_type='cbt',
                question_text=f'Q{i}?', options_json=json.dumps(['a', 'b', 'c', 'd']),
                correct_index=0, explanation='because',
            ))
        db.session.add_all(rows)
        db.session.commit()
        return [r.id for r in rows]


def test_time_limit_derivation():
    # Written practice: never timed.
    assert cbt_time_limit_seconds('written', 10) is None
    # CBT: 1 minute per question, floored so a tiny set still isn't a speed run.
    assert cbt_time_limit_seconds('cbt', 1) == CBT_MIN_TIME_SECONDS
    assert cbt_time_limit_seconds('cbt', 10) == 10 * CBT_SECONDS_PER_QUESTION
    assert cbt_time_limit_seconds('cbt', 50) == 50 * CBT_SECONDS_PER_QUESTION
    # The floor must bind below 5 questions, not replace the per-question rate above it.
    assert cbt_time_limit_seconds('cbt', 4) == CBT_MIN_TIME_SECONDS
    assert cbt_time_limit_seconds('cbt', 6) == 6 * CBT_SECONDS_PER_QUESTION


def test_start_issues_time_limit_for_cbt(app, client, make_user, login_as):
    user = make_user('cbt_timer1')
    _seed_questions(app)
    login_as(client, user)

    res = client.post('/api/cbt/start', json={'course_code': 'MTH101', 'question_type': 'cbt'})
    data = res.get_json()
    assert data['success'] is True
    # 3 questions x 60s = 180s, below the floor -- the floor is what applies here.
    assert data['time_limit_seconds'] == CBT_MIN_TIME_SECONDS


def test_start_leaves_written_untimed(app, client, make_user, login_as):
    user = make_user('cbt_timer2')
    with app.app_context():
        db.session.add(CBTQuestion(
            subject_code='MTH', course_code='MTH101', question_type='written',
            question_text='Explain queues.', options_json=None, correct_index=None,
            mark_scheme='A queue is FIFO.',
        ))
        db.session.commit()
    login_as(client, user)

    res = client.post('/api/cbt/start', json={'course_code': 'MTH101', 'question_type': 'written'})
    data = res.get_json()
    assert data['success'] is True
    assert data['time_limit_seconds'] is None


def test_submit_clamps_reported_duration_to_the_limit(app, client, make_user, login_as):
    """A client claiming an absurd duration (tampered clock / forged payload) has it
    clamped to the same derived limit the countdown used; a normal duration passes
    through unchanged."""
    user = make_user('cbt_timer3')
    _seed_questions(app)
    login_as(client, user)

    start = client.post('/api/cbt/start', json={'course_code': 'MTH101', 'question_type': 'cbt'})
    data = start.get_json()
    attempt_id = data['attempt_id']
    limit = data['time_limit_seconds']
    issued = {q['id']: q for q in data['questions']}

    with app.app_context():
        truth = {q.id: q.correct_index
                 for q in CBTQuestion.query.filter(CBTQuestion.id.in_(issued.keys())).all()}
    answers = {str(qid): truth[qid] for qid in issued}

    # Normal duration: under the limit, recorded as-is.
    ok = client.post(f'/CBT/submit/{attempt_id}',
                     json={'answers': answers, 'duration_seconds': 42})
    assert ok.get_json()['duration_seconds'] == 42

    # Forged duration beyond the limit: clamped server-side.
    start2 = client.post('/api/cbt/start', json={'course_code': 'MTH101', 'question_type': 'cbt'})
    data2 = start2.get_json()
    with app.app_context():
        truth2 = {q.id: q.correct_index for q in CBTQuestion.query.filter(
            CBTQuestion.id.in_([q['id'] for q in data2['questions']])).all()}
    over = client.post(f'/CBT/submit/{data2["attempt_id"]}',
                       json={'answers': {str(qid): truth2[qid] for qid in truth2},
                             'duration_seconds': 999999})
    assert over.get_json()['duration_seconds'] == data2['time_limit_seconds']
