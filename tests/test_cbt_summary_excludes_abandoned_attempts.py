"""Regression test for the P1 fix: get_cbt_summary()/cbt_history() previously counted
every CBTAttempt row regardless of whether it was ever submitted. start_cbt_attempt()
creates the row up front with submitted_at=None, score_pct=0 -- a student who starts an
exam and never finishes it (closed tab, double-click, opened a second attempt instead)
left a phantom 0% attempt that dragged average_score down and could even win
"last_attempt" outright over a real, finished result (NULL sorts first on a DESC order
in Postgres). Both now only ever consider attempts that were actually submitted.
"""
from datetime import datetime, timedelta
from extensions import db
from models import CBTAttempt
from services.progress_service import get_cbt_summary


def test_abandoned_attempt_excluded_from_summary_and_average(app, make_user):
    user = make_user('cbt_abandon_student')
    with app.app_context():
        # A real, finished attempt: scored 80%.
        db.session.add(CBTAttempt(
            user_id=user.id, course_code='MTH101', question_type='cbt',
            total_questions=10, correct_count=8, score_pct=80,
            started_at=datetime.utcnow() - timedelta(minutes=10),
            submitted_at=datetime.utcnow() - timedelta(minutes=5),
        ))
        # An abandoned attempt started AFTER the real one (e.g. a second tab, or a
        # retry) -- never submitted, submitted_at stays None, score_pct stays its
        # column default of 0.
        db.session.add(CBTAttempt(
            user_id=user.id, course_code='MTH101', question_type='cbt',
            total_questions=10, correct_count=0, score_pct=0,
            started_at=datetime.utcnow(), submitted_at=None,
        ))
        db.session.commit()

        summary = get_cbt_summary(user)

        assert summary['attempts_count'] == 1
        assert summary['average_score'] == 80
        assert summary['last_attempt']['score_pct'] == 80


def test_cbt_history_page_excludes_abandoned_attempt(app, client, make_user, login_as):
    user = make_user('cbt_history_student')
    with app.app_context():
        db.session.add(CBTAttempt(
            user_id=user.id, course_code='MTH101', question_type='cbt',
            total_questions=10, correct_count=8, score_pct=80,
            submitted_at=datetime.utcnow(),
        ))
        db.session.add(CBTAttempt(
            user_id=user.id, course_code='MTH101', question_type='cbt',
            total_questions=10, correct_count=0, score_pct=0, submitted_at=None,
        ))
        db.session.commit()

    login_as(client, user)
    res = client.get('/CBT/history')
    assert res.status_code == 200
    body = res.get_data(as_text=True)
    # Exactly one <a class="ch-row"> rendered -- not '0%' not in body, which would be a
    # false negative here since '80%' itself contains '0%' as a substring.
    assert body.count('class="ch-row"') == 1
    assert '80%' in body
