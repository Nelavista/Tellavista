"""Live-class Socket.IO authentication: only the logged-in user who registered as a
room's owner (via GET /teacher/<room_id>) may claim the 'teacher' role on that room's
socket connection. Previously any anonymous socket claiming role:'teacher' was simply
believed -- this is the red-team test for that fix (events.py's handle_join_room).
"""
import uuid
import pytest
from extensions import db, socketio
import events  # noqa: F401 -- registers @socketio.on handlers onto the shared socketio instance
from models import Room


@pytest.fixture
def socket_app(app):
    """The base `app` fixture doesn't register live_bp/socketio -- add what's needed for
    live-class tests specifically without bloating every other test's setup."""
    socketio.init_app(app, message_queue=None)
    return app


def test_anonymous_socket_cannot_claim_teacher_role(socket_app, client, make_user):
    """The original vulnerability: an anonymous connection (no login at all) claiming
    role:'teacher' for a real room must be rejected outright."""
    owner = make_user('room_owner1')
    room_id = uuid.uuid4().hex[:8]
    with socket_app.app_context():
        db.session.add(Room(id=room_id, teacher_user_id=owner.id, teacher_name=owner.username))
        db.session.commit()

    # A fresh, unauthenticated test client -- no session['user'] at all.
    anon_client = socket_app.test_client()
    sio_client = socketio.test_client(socket_app, flask_test_client=anon_client)
    sio_client.emit('join-room', {'room': room_id, 'role': 'teacher', 'username': 'Attacker'})
    received = sio_client.get_received()
    errors = [e for e in received if e['name'] == 'error']
    assert errors, f"expected an error event rejecting the anonymous teacher claim, got: {received}"
    assert 'logged in' in errors[0]['args'][0]['message'].lower()
    sio_client.disconnect()


def test_logged_in_non_owner_cannot_claim_teacher_role(socket_app, client, make_user, login_as):
    """A real, logged-in Nelavista account that is NOT this room's registered owner must
    also be rejected -- confirms the fix checks ownership, not just 'is someone logged in.'"""
    owner = make_user('room_owner2')
    attacker = make_user('room_attacker2')
    room_id = uuid.uuid4().hex[:8]
    with socket_app.app_context():
        db.session.add(Room(id=room_id, teacher_user_id=owner.id, teacher_name=owner.username))
        db.session.commit()

    attacker_http_client = socket_app.test_client()
    login_as(attacker_http_client, attacker)
    sio_client = socketio.test_client(socket_app, flask_test_client=attacker_http_client)
    sio_client.emit('join-room', {'room': room_id, 'role': 'teacher', 'username': 'Attacker'})
    received = sio_client.get_received()
    errors = [e for e in received if e['name'] == 'error']
    assert errors, f"expected an error event rejecting the non-owner's teacher claim, got: {received}"
    assert 'not authorized' in errors[0]['args'][0]['message'].lower()
    sio_client.disconnect()


def test_real_owner_can_claim_teacher_role(socket_app, client, make_user, login_as):
    """The legitimate path must still work: the logged-in user who actually owns this
    room (Room.teacher_user_id) can become its teacher."""
    owner = make_user('room_owner3')
    room_id = uuid.uuid4().hex[:8]
    with socket_app.app_context():
        db.session.add(Room(id=room_id, teacher_user_id=owner.id, teacher_name=owner.username))
        db.session.commit()

    owner_http_client = socket_app.test_client()
    login_as(owner_http_client, owner)
    sio_client = socketio.test_client(socket_app, flask_test_client=owner_http_client)
    sio_client.emit('join-room', {'room': room_id, 'role': 'teacher', 'username': owner.username})
    received = sio_client.get_received()
    joined = [e for e in received if e['name'] == 'room-joined']
    assert joined, f"expected a room-joined event for the legitimate owner, got: {received}"
    assert joined[0]['args'][0]['role'] == 'teacher'
    sio_client.disconnect()


def test_teacher_role_rejected_for_room_never_claimed_via_http(socket_app, client, make_user, login_as):
    """A room_id that was never registered via GET /teacher/<room_id> at all (no Room row
    exists yet) must not be claimable as teacher by anyone, logged in or not -- confirms
    the check is 'does a Room row already say this user owns it', not 'does some Room
    row exist that I can attach myself to.'"""
    user = make_user('no_room_row_user')
    room_id = uuid.uuid4().hex[:8]  # deliberately never created via the HTTP route

    http_client = socket_app.test_client()
    login_as(http_client, user)
    sio_client = socketio.test_client(socket_app, flask_test_client=http_client)
    sio_client.emit('join-room', {'room': room_id, 'role': 'teacher', 'username': user.username})
    received = sio_client.get_received()
    errors = [e for e in received if e['name'] == 'error']
    assert errors
    assert 'not authorized' in errors[0]['args'][0]['message'].lower()
    sio_client.disconnect()


def test_anonymous_student_join_still_allowed(socket_app, client, make_user):
    """The student side of a live class is deliberately still open to guests-by-link (the
    /student/<room_id> HTTP route has no login requirement by design) -- confirms the fix
    didn't accidentally lock out the intended anonymous-student flow while closing the
    teacher hole."""
    owner = make_user('room_owner4')
    room_id = uuid.uuid4().hex[:8]
    with socket_app.app_context():
        db.session.add(Room(id=room_id, teacher_user_id=owner.id, teacher_name=owner.username))
        db.session.commit()

    guest_client = socket_app.test_client()
    sio_client = socketio.test_client(socket_app, flask_test_client=guest_client)
    sio_client.emit('join-room', {'room': room_id, 'role': 'student', 'username': 'Guest_Student'})
    received = sio_client.get_received()
    joined = [e for e in received if e['name'] == 'room-joined']
    assert joined, f"expected the anonymous student join to succeed, got: {received}"
    assert joined[0]['args'][0]['role'] == 'student'
    sio_client.disconnect()


def test_http_route_registers_ownership_for_first_visitor(socket_app):
    """routes/live_meeting_routes.py's teacher_view: the first logged-in visitor to a
    fresh room_id becomes its owner in the database, which is what the socket-layer check
    above depends on."""
    # live_bp is already registered by the base `app` fixture in conftest.py.
    from models import User
    with socket_app.app_context():
        u = User(username='http_claim_user', email='http_claim_user@example.com', name='X',
                  university='Lagos State University', faculty='Science', department='CS',
                  level='200', semester='First Semester')
        u.set_password('x')
        db.session.add(u)
        db.session.commit()
        uid = u.id

    c = socket_app.test_client()
    with c.session_transaction() as sess:
        sess['user'] = {'username': 'http_claim_user', 'email': 'http_claim_user@example.com',
                         'joined_on': '2026-01-01', 'last_login': '2026-01-01', 'is_admin': False, 'preferred_path': None}
    room_id = uuid.uuid4().hex[:8]
    res = c.get(f'/teacher/{room_id}')
    assert res.status_code == 200

    with socket_app.app_context():
        room = Room.query.get(room_id)
        assert room is not None
        assert room.teacher_user_id == uid
