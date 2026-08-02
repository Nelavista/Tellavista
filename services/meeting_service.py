from datetime import datetime
from extensions import db
from models import Room

# In-memory storage for live meetings. This is per-process state — fine for a single
# eventlet worker (which is what this app runs as), but it means room/chat state does not
# survive a process restart. The Room DB row (id, teacher, is_live, started_at/ended_at) is
# the durable record of a session; these dicts are just the live presence/signaling layer on
# top of it. The actual video never touches this server at all — the teacher's camera and
# every viewer talk directly to Agora's network, using the room id as the channel name.
rooms = {}           # room_id -> room data
participants = {}    # socket_id -> participant info
room_authority = {}  # room_id -> authority state


def get_or_create_room(room_id):
    """Get existing in-memory room, or create one — rehydrated from the DB Room row if the
    session was already live. Without this, a room that gets emptied and cleaned up (e.g.
    the teacher's tab briefly disconnects while no student has joined yet) would forget it
    was live the moment the next person joins, even though the DB row still says so."""
    if room_id not in rooms:
        is_live = False
        existing_room = Room.query.get(room_id)
        if existing_room:
            is_live = existing_room.is_live
        rooms[room_id] = {
            'participants': {},
            'teacher_sid': None,
            'created_at': datetime.utcnow().isoformat(),
            'is_live': is_live,
            'chat_log': [],  # last N chat messages, for late joiners
        }
    return rooms[room_id]


def get_room_authority(room_id):
    """Get or create authority state for a room."""
    if room_id not in room_authority:
        room_authority[room_id] = {
            'mic_requests': {},
        }
    return room_authority[room_id]


def get_participants_list(room_id, exclude_sid=None):
    """Get list of all participants in room except exclude_sid."""
    if room_id not in rooms:
        return []
    room = rooms[room_id]
    result = []
    for sid, info in room['participants'].items():
        if sid != exclude_sid:
            result.append({
                'sid': sid,
                'username': info['username'],
                'role': info['role']
            })
    return result


def append_chat_message(room_id, entry, max_history=100):
    """Keep a bounded chat history in memory so students who join mid-session see recent
    context. Bounded so a 10-hour session's chat can't grow this dict without limit."""
    room = rooms.get(room_id)
    if not room:
        return
    room['chat_log'].append(entry)
    if len(room['chat_log']) > max_history:
        room['chat_log'] = room['chat_log'][-max_history:]


def cleanup_room(room_id):
    """Drop the in-memory room once it's genuinely empty. Does NOT touch the Room DB row —
    a session that's gone temporarily quiet (everyone's connection blipped at once) or that
    the teacher paused should still exist when people reconnect. The DB row is only closed
    out explicitly, when the teacher ends the session (see end_room_session below)."""
    if room_id in rooms:
        room = rooms[room_id]
        if not room['participants']:
            del rooms[room_id]
            if room_id in room_authority:
                del room_authority[room_id]


def end_room_session(room_id):
    """Explicit teacher-initiated end of a session: marks the DB row inactive/ended and
    drops the in-memory room. Safe to call even if the room was already cleaned up."""
    room = Room.query.get(room_id)
    if room:
        room.is_active = False
        room.is_live = False
        room.ended_at = datetime.utcnow()
        db.session.commit()
    if room_id in rooms:
        del rooms[room_id]
    if room_id in room_authority:
        del room_authority[room_id]
