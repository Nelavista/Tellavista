"""Regression test for the P2 performance fix: messages() (routes/skills_routes.py)
previously called t.other_party() (an un-eager-loaded relationship access -- a query),
t.unread_count_for() (a .count() query), and t.messages...first() (another query) once
PER thread in a loop. All three are now batched into a small, fixed number of queries
regardless of thread count. Proves the inbox still shows the correct unread count, last
message, and other-party name after the refactor.
"""
from extensions import db
from models import MessageThread, Message
from services.messaging_service import get_or_create_thread, send_message


def test_inbox_shows_correct_unread_count_and_last_message(app, client, make_user, login_as):
    employer = make_user('inbox_employer', is_admin=False)
    student = make_user('inbox_student')
    with app.app_context():
        from models import User
        emp = User.query.get(employer.id)
        emp.is_employer = True
        db.session.commit()

        thread = get_or_create_thread(employer.id, student.id)
        send_message(thread, student.id, 'First message')
        send_message(thread, student.id, 'Second message (most recent)')

    login_as(client, employer)
    res = client.get('/skills/messages')
    assert res.status_code == 200
    body = res.get_data(as_text=True)

    assert 'Second message (most recent)' in body  # last_message picked correctly
    assert 'First message' not in body  # only the LAST message previews, not both
    assert '>2<' in body  # unread badge -- both messages are unread by the employer
    # make_user(complete_profile=True) sets User.name to username.title() --
    # 'inbox_student'.title() == 'Inbox_Student' (the underscore is a word boundary).
    assert 'Inbox_Student' in body  # other-party name


def test_inbox_with_no_threads_does_not_crash(app, client, make_user, login_as):
    user = make_user('inbox_empty_student')
    login_as(client, user)
    res = client.get('/skills/messages')
    assert res.status_code == 200
