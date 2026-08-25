"""CBT integrity: the server must be the sole authority on correct answers and scores.

Red-team scenarios this file exercises directly:
  - correct answers are never present in the /api/cbt/start response
  - a forged/omitted selected_index doesn't fool the server's own grading
  - answers for question ids never issued to this attempt are ignored (no substitution)
  - an attempt cannot be submitted twice (no re-submission score manipulation)
  - one student cannot submit against another student's attempt_id (IDOR)
"""
import json
import pytest
from extensions import db
from models import CBTQuestion, CBTAttempt, User


def _seed_mth_questions(app):
    with app.app_context():
        q1 = CBTQuestion(subject_code='MTH', question_type='cbt', question_text='2+2=?',
                          options_json=json.dumps(['3', '4', '5', '6']), correct_index=1, explanation='basic addition')
        q2 = CBTQuestion(subject_code='MTH', question_type='cbt', question_text='3*3=?',
                          options_json=json.dumps(['6', '9', '12', '3']), correct_index=1, explanation='basic multiplication')
        q3 = CBTQuestion(subject_code='MTH', question_type='cbt', question_text='10-4=?',
                          options_json=json.dumps(['4', '5', '6', '7']), correct_index=2, explanation='basic subtraction')
        db.session.add_all([q1, q2, q3])
        db.session.commit()
        return [q1.id, q2.id, q3.id]


def test_start_never_leaks_correct_answers(app, client, make_user, login_as):
    user = make_user('cbt_student1')
    _seed_mth_questions(app)
    login_as(client, user)

    res = client.post('/api/cbt/start', json={'course_code': 'MTH101', 'question_type': 'cbt'})
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert len(data['questions']) == 3
    raw_body = res.get_data(as_text=True)
    # The literal words the answer key would appear under, and the actual correct
    # option strings, must never appear anywhere in this response body.
    assert 'correct_index' not in raw_body
    assert 'explanation' not in raw_body
    assert 'mark_scheme' not in raw_body
    for q in data['questions']:
        assert set(q.keys()) == {'id', 'subject_code', 'question_type', 'question_text', 'options'}


def test_start_requires_login(client):
    res = client.post('/api/cbt/start', json={'course_code': 'MTH101', 'question_type': 'cbt'})
    # login_required redirects (302) rather than 401 in this codebase's pattern
    assert res.status_code in (302, 401)


def test_correct_submission_scores_accurately(app, client, make_user, login_as):
    user = make_user('cbt_student2')
    question_ids = _seed_mth_questions(app)
    login_as(client, user)

    start = client.post('/api/cbt/start', json={'course_code': 'MTH101', 'question_type': 'cbt'})
    attempt_id = start.get_json()['attempt_id']
    issued = {q['id']: q for q in start.get_json()['questions']}

    with app.app_context():
        truth = {q.id: q.correct_index for q in CBTQuestion.query.filter(CBTQuestion.id.in_(issued.keys())).all()}

    # Answer everything correctly, straight from the DB truth (simulating a genuinely
    # correct student, not a cheat attempt).
    answers = {str(qid): truth[qid] for qid in issued}
    submit = client.post(f'/CBT/submit/{attempt_id}', json={'answers': answers, 'duration_seconds': 42})
    assert submit.status_code == 200
    result = submit.get_json()
    assert result['success'] is True
    assert result['correct_count'] == 3
    assert result['total_questions'] == 3
    assert result['score_pct'] == 100
    # Now that grading has happened, the response IS allowed to reveal correct answers
    # (for the review screen) -- confirm that data is actually present post-submit.
    assert all('correct_index' in r for r in result['results'])


def test_forged_score_is_ignored(app, client, make_user, login_as):
    """A malicious client tries to smuggle a fabricated correct_index/is_correct into the
    payload, and answers every question WRONG on purpose -- the server must still compute
    0% from its own database, never trusting anything the client asserts about
    correctness."""
    user = make_user('cbt_cheater')
    question_ids = _seed_mth_questions(app)
    login_as(client, user)

    start = client.post('/api/cbt/start', json={'course_code': 'MTH101', 'question_type': 'cbt'})
    attempt_id = start.get_json()['attempt_id']
    issued_ids = [q['id'] for q in start.get_json()['questions']]

    with app.app_context():
        truth = {q.id: q.correct_index for q in CBTQuestion.query.filter(CBTQuestion.id.in_(issued_ids)).all()}

    # Deliberately select a WRONG option for every question, while also trying to inject
    # forged fields the endpoint doesn't even read.
    wrong_answers = {str(qid): (truth[qid] + 1) % 4 for qid in issued_ids}
    payload = {
        'answers': wrong_answers,
        'duration_seconds': 5,
        'score_pct': 100,          # forged -- must be ignored
        'correct_count': 999,      # forged -- must be ignored
    }
    submit = client.post(f'/CBT/submit/{attempt_id}', json=payload)
    result = submit.get_json()
    assert result['correct_count'] == 0
    assert result['score_pct'] == 0


def test_substituted_question_id_is_ignored(app, client, make_user, login_as):
    """A question id that was never issued to this attempt (e.g. copied from a different
    attempt, or invented) must not be gradable through this endpoint -- confirms the
    server checks against attempt.issued_question_ids, not just "does this id exist"."""
    user = make_user('cbt_substitute')
    question_ids = _seed_mth_questions(app)
    login_as(client, user)

    # Issue only 2 of the 3 seeded questions by mocking a smaller bank via a second
    # subject so the third question id is guaranteed to be "foreign" to this attempt.
    with app.app_context():
        foreign_q = CBTQuestion(subject_code='PHY', question_type='cbt', question_text='F=ma?',
                                 options_json=json.dumps(['yes', 'no']), correct_index=0)
        db.session.add(foreign_q)
        db.session.commit()
        foreign_id = foreign_q.id

    start = client.post('/api/cbt/start', json={'course_code': 'MTH101', 'question_type': 'cbt'})
    attempt_id = start.get_json()['attempt_id']
    issued_ids = [q['id'] for q in start.get_json()['questions']]
    assert foreign_id not in issued_ids

    with app.app_context():
        truth = {q.id: q.correct_index for q in CBTQuestion.query.filter(CBTQuestion.id.in_(issued_ids)).all()}

    answers = {str(qid): truth[qid] for qid in issued_ids}
    answers[str(foreign_id)] = 0  # inject a foreign, never-issued question id

    submit = client.post(f'/CBT/submit/{attempt_id}', json={'answers': answers, 'duration_seconds': 10})
    result = submit.get_json()
    # Still exactly 3 questions graded (the foreign one contributes nothing, good or bad)
    assert result['total_questions'] == 3
    assert result['correct_count'] == 3
    assert not any(r['question_id'] == foreign_id for r in result['results'])


def test_cannot_resubmit_same_attempt(app, client, make_user, login_as):
    user = make_user('cbt_resubmit')
    _seed_mth_questions(app)
    login_as(client, user)

    start = client.post('/api/cbt/start', json={'course_code': 'MTH101', 'question_type': 'cbt'})
    attempt_id = start.get_json()['attempt_id']

    first = client.post(f'/CBT/submit/{attempt_id}', json={'answers': {}, 'duration_seconds': 1})
    assert first.status_code == 200

    second = client.post(f'/CBT/submit/{attempt_id}', json={'answers': {}, 'duration_seconds': 1})
    assert second.status_code == 409
    assert second.get_json()['success'] is False


def test_cannot_submit_another_students_attempt(app, client, make_user, login_as):
    """IDOR check: user B must not be able to grade/see user A's in-progress attempt."""
    user_a = make_user('cbt_victim')
    user_b = make_user('cbt_attacker')
    _seed_mth_questions(app)

    login_as(client, user_a)
    start = client.post('/api/cbt/start', json={'course_code': 'MTH101', 'question_type': 'cbt'})
    attempt_id = start.get_json()['attempt_id']

    # Switch session to user B
    login_as(client, user_b)
    submit = client.post(f'/CBT/submit/{attempt_id}', json={'answers': {}, 'duration_seconds': 1})
    assert submit.status_code == 404


def test_no_questions_available_response(app, client, make_user, login_as):
    user = make_user('cbt_nobank')
    login_as(client, user)
    # ZZZ999 -> subject prefix "ZZZ", nothing seeded for it
    res = client.post('/api/cbt/start', json={'course_code': 'ZZZ999', 'question_type': 'cbt'})
    data = res.get_json()
    assert data['success'] is False
    assert data['error'] == 'no_questions'
