"""Regression tests for the orphaned-live-room bug: if a teacher's socket disconnected
abnormally (crash, closed laptop, lost wifi) while students were still connected,
events.py's handle_disconnect cleared teacher_sid and told them, but never touched the
Room DB row -- Room.is_live/is_active stayed true forever, with no background reaper and
no other caller besides an explicit "End Session" click or an admin manually ending it
from /admin/live-rooms. And if the teacher was the room's last participant,
cleanup_room() dropped the in-memory room entirely (by design), leaving nothing at all
to ever notice the DB row was still marked live.

The fix (services/meeting_service.py): a grace-period check, scheduled from
handle_disconnect via schedule_teacher_reconnect_check(), closes the session out --
exactly like end_room_session() already does for an explicit end -- if the teacher
hasn't reclaimed the room within TEACHER_RECONNECT_GRACE_SECONDS. These tests call the
check directly (_close_room_if_still_abandoned) rather than waiting out the real sleep,
and separately confirm handle_disconnect actually wires it up.
"""
import uuid
import pytest
from extensions import db, socketio
import events  # noqa: F401 -- registers @socketio.on handlers onto the shared socketio instance
from models import Room
import services.meeting_service as meeting_service
from services.meeting_service import rooms, room_authority, _close_room_if_still_abandoned


@pytest.fixture
def socket_app(app):
    socketio.init_app(app, message_queue=None)
    return app


def _make_live_room(app, owner_id, room_id):
    with app.app_context():
        room = Room(id=room_id, teacher_user_id=owner_id, teacher_name='Teacher',
                    is_active=True, is_live=True)
        db.session.add(room)
        db.session.commit()


def test_abandoned_room_gets_closed_when_teacher_never_returns(socket_app, make_user):
    owner = make_user('reaper_owner1')
    room_id = uuid.uuid4().hex[:8]
    _make_live_room(socket_app, owner.id, room_id)
    # Simulates the "students still around" shape of the bug: the in-memory room still
    # exists, but the teacher's slot is empty (handle_disconnect already cleared it).
    rooms[room_id] = {'participants': {'some-student-sid': {'username': 'S', 'role': 'student'}},
                       'teacher_sid': None, 'created_at': '', 'is_live': True, 'chat_log': []}

    _close_room_if_still_abandoned(socket_app, room_id)

    with socket_app.app_context():
        reloaded = Room.query.get(room_id)
        assert reloaded.is_live is False
        assert reloaded.is_active is False
        assert reloaded.ended_at is not None
    assert room_id not in rooms


def test_abandoned_room_gets_closed_even_after_cleanup_room_dropped_it(socket_app, make_user):
    """The other shape of the bug: the teacher was the room's last participant, so
    cleanup_room() already deleted rooms[room_id] entirely -- nothing left in memory to
    even check, but the DB row is still live and nothing else was going to close it."""
    owner = make_user('reaper_owner2')
    room_id = uuid.uuid4().hex[:8]
    _make_live_room(socket_app, owner.id, room_id)
    assert room_id not in rooms  # never populated -- room dict genuinely absent

    _close_room_if_still_abandoned(socket_app, room_id)

    with socket_app.app_context():
        reloaded = Room.query.get(room_id)
        assert reloaded.is_live is False
        assert reloaded.is_active is False


def test_reconnected_teacher_is_not_treated_as_abandoned(socket_app, make_user):
    owner = make_user('reaper_owner3')
    room_id = uuid.uuid4().hex[:8]
    _make_live_room(socket_app, owner.id, room_id)
    # A real reconnect within the grace period sets teacher_sid again before the check runs.
    rooms[room_id] = {'participants': {'new-teacher-sid': {'username': 'Teacher', 'role': 'teacher'}},
                       'teacher_sid': 'new-teacher-sid', 'created_at': '', 'is_live': True, 'chat_log': []}
    try:
        _close_room_if_still_abandoned(socket_app, room_id)
        with socket_app.app_context():
            reloaded = Room.query.get(room_id)
            assert reloaded.is_live is True
            assert reloaded.is_active is True
        assert room_id in rooms  # untouched
    finally:
        rooms.pop(room_id, None)
        room_authority.pop(room_id, None)


def test_teacher_disconnect_schedules_the_abandonment_check(socket_app, client, make_user, login_as, monkeypatch):
    owner = make_user('reaper_owner4')
    room_id = uuid.uuid4().hex[:8]
    _make_live_room(socket_app, owner.id, room_id)

    scheduled = []
    monkeypatch.setattr(
        meeting_service.socketio, 'start_background_task',
        lambda target, *args, **kwargs: scheduled.append((target, args)),
    )

    owner_http_client = socket_app.test_client()
    login_as(owner_http_client, owner)
    sio_client = socketio.test_client(socket_app, flask_test_client=owner_http_client)
    sio_client.emit('join-room', {'room': room_id, 'role': 'teacher', 'username': owner.username})
    sio_client.disconnect()

    assert len(scheduled) == 1
    target, args = scheduled[0]
    assert target is meeting_service._reap_abandoned_room
    assert args[1] == room_id
