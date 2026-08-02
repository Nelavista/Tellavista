from flask import request
from flask_socketio import emit, join_room, leave_room
from extensions import socketio, db
from models import Room
from services.meeting_service import (
    rooms, participants, room_authority,
    get_or_create_room, get_room_authority, get_participants_list,
    append_chat_message, cleanup_room, end_room_session,
)
from utils.helpers import debug_print
from datetime import datetime

MAX_CHAT_LEN = 500


@socketio.on('connect')
def handle_connect():
    sid = request.sid
    join_room(sid)
    participants[sid] = {'room_id': None, 'username': None, 'role': None}
    debug_print(f"✅ Client connected: {sid}")


@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    participant = participants.get(sid)
    if not participant:
        return
    room_id = participant['room_id']
    if room_id in rooms:
        room = rooms[room_id]
        if sid in room['participants']:
            participant_info = room['participants'][sid]
            del room['participants'][sid]
            if sid == room['teacher_sid']:
                room['teacher_sid'] = None
                for p_sid in room['participants']:
                    if room['participants'][p_sid]['role'] == 'student':
                        emit('teacher-disconnected', room=p_sid)
            emit('participant-left', {'sid': sid, 'username': participant_info['username'], 'role': participant_info['role']}, room=room_id, skip_sid=sid)
            debug_print(f"❌ {participant_info['username']} left room {room_id}")
    cleanup_room(room_id)
    if sid in participants:
        del participants[sid]


@socketio.on('join-room')
def handle_join_room(data):
    try:
        sid = request.sid
        room_id = data.get('room')
        role = data.get('role', 'student')
        username = data.get('username', 'Teacher' if role == 'teacher' else f'Student_{sid[:6]}')
        if not room_id:
            emit('error', {'message': 'Room ID required'})
            return
        debug_print(f"👤 {username} ({role}) joining room: {room_id}")
        room = get_or_create_room(room_id)
        get_room_authority(room_id)
        if role == 'teacher' and room['teacher_sid']:
            emit('error', {'message': 'Room already has a teacher'})
            return
        room['participants'][sid] = {'username': username, 'role': role, 'joined_at': datetime.utcnow().isoformat()}
        if role == 'teacher':
            room['teacher_sid'] = sid
            existing_room = Room.query.get(room_id)
            if not existing_room:
                room_db = Room(id=room_id, teacher_id=sid, teacher_name=username, is_active=True)
                db.session.add(room_db)
            else:
                existing_room.teacher_id = sid
                existing_room.teacher_name = username
                existing_room.is_active = True
                # A reconnect (dropped wifi, refreshed tab) also drops the teacher's Agora
                # publish, so the stream itself actually stopped even though the DB still
                # says is_live — the frontend uses this to prompt "click Go Live to resume"
                # rather than falsely claiming the video is still playing for everyone.
                room['is_live'] = existing_room.is_live
            db.session.commit()
            for p_sid in room['participants']:
                if room['participants'][p_sid]['role'] == 'student':
                    emit('teacher-joined', {'teacher_sid': sid, 'teacher_name': username}, room=p_sid)
        participants[sid] = {'room_id': room_id, 'username': username, 'role': role}
        join_room(room_id)
        existing_participants = get_participants_list(room_id, exclude_sid=sid)
        emit('room-joined', {
            'room': room_id,
            'sid': sid,
            'username': username,
            'role': role,
            'existing_participants': existing_participants,
            'teacher_sid': room['teacher_sid'],
            'is_waiting': (role == 'student' and not room['teacher_sid']),
            'is_live': room.get('is_live', False),
            'chat_log': room.get('chat_log', []),
        })
        emit('new-participant', {'sid': sid, 'username': username, 'role': role}, room=room_id, skip_sid=sid)
        debug_print(f"✅ {username} joined room {room_id}. Total participants: {len(room['participants'])}")
    except Exception as e:
        debug_print(f"❌ Error in join-room: {e}")
        emit('error', {'message': str(e)})


@socketio.on('teacher-go-live')
def handle_teacher_go_live(data):
    """Teacher has started broadcasting their camera through Agora. We just flip the is_live
    flag and tell everyone in the room — the video itself never touches this server at all;
    the teacher's browser publishes straight to Agora's network under a channel named after
    the room id, and every viewer's browser subscribes to that same channel directly. That's
    what makes 1000+ viewers over a 10-hour session realistic here."""
    try:
        room_id = data.get('room')
        if not room_id or room_id not in rooms:
            emit('error', {'message': 'Room not found'})
            return
        room = rooms[room_id]
        if request.sid != room['teacher_sid']:
            emit('error', {'message': 'Only the teacher can go live'})
            return
        room['is_live'] = True
        room_db = Room.query.get(room_id)
        if room_db:
            room_db.is_live = True
            if not room_db.started_at:
                room_db.started_at = datetime.utcnow()
            db.session.commit()
        emit('stream-live', {}, room=room_id)
        debug_print(f"📡 Room {room_id} went live")
    except Exception as e:
        debug_print(f"❌ Error in teacher-go-live: {e}")
        emit('error', {'message': str(e)})


@socketio.on('teacher-end-live')
def handle_teacher_end_live(data):
    """Teacher stopped broadcasting but the session/room itself stays open (e.g. a short
    break) — distinct from ending the whole session, which uses teacher-end-session below."""
    try:
        room_id = data.get('room')
        if not room_id or room_id not in rooms:
            return
        room = rooms[room_id]
        if request.sid != room['teacher_sid']:
            return
        room['is_live'] = False
        room_db = Room.query.get(room_id)
        if room_db:
            room_db.is_live = False
            db.session.commit()
        emit('stream-ended', {}, room=room_id)
    except Exception as e:
        debug_print(f"❌ Error in teacher-end-live: {e}")


@socketio.on('teacher-end-session')
def handle_teacher_end_session(data=None):
    try:
        room_id = (data or {}).get('room') if data else None
        sid = request.sid
        participant = participants.get(sid)
        if not room_id and participant:
            room_id = participant['room_id']
        if not room_id or room_id not in rooms:
            return
        room = rooms[room_id]
        if sid != room['teacher_sid']:
            return
        emit('session-ended', {}, room=room_id)
        end_room_session(room_id)
        debug_print(f"🔚 Teacher ended session in room {room_id}")
    except Exception as e:
        debug_print(f"❌ Error in teacher-end-session: {e}")


@socketio.on('chat-message')
def handle_chat_message(data):
    try:
        room_id = data.get('room')
        text = (data.get('text') or '').strip()
        participant = participants.get(request.sid)
        if not room_id or not participant or participant['room_id'] != room_id:
            return
        if not text:
            return
        text = text[:MAX_CHAT_LEN]
        entry = {
            'username': participant['username'],
            'role': participant['role'],
            'text': text,
            'ts': datetime.utcnow().isoformat(),
        }
        append_chat_message(room_id, entry)
        emit('chat-message', entry, room=room_id)
    except Exception as e:
        debug_print(f"❌ Error in chat-message: {e}")


@socketio.on('student-request-mic')
def handle_student_request_mic(data):
    """Lightweight 'raise hand to ask a question' signal — there is no live audio/video from
    students in this design (that's what makes 1000 concurrent viewers feasible); this just
    notifies the teacher who can then read the question out or unmute them manually should a
    separate voice-call feature exist later."""
    try:
        room_id = data.get('room')
        if not room_id or room_id not in rooms:
            return
        room = rooms[room_id]
        sid = request.sid
        if sid not in room['participants']:
            return
        username = room['participants'][sid]['username']
        authority = get_room_authority(room_id)
        authority['mic_requests'][sid] = username
        if room['teacher_sid']:
            emit('mic-request-received', {'username': username, 'student_sid': sid}, room=room['teacher_sid'])
    except Exception as e:
        debug_print(f"❌ Error in student-request-mic: {e}")


@socketio.on('teacher-approve-mic')
def handle_teacher_approve_mic(data):
    try:
        room_id = data.get('room')
        student_sid = data.get('student_sid')
        if not room_id or room_id not in rooms:
            return
        room = rooms[room_id]
        if request.sid != room['teacher_sid']:
            return
        authority = get_room_authority(room_id)
        authority['mic_requests'].pop(student_sid, None)
        emit('mic-approved', {'approved': True}, room=student_sid)
    except Exception as e:
        debug_print(f"❌ Error in teacher-approve-mic: {e}")


@socketio.on('teacher-deny-mic')
def handle_teacher_deny_mic(data):
    try:
        room_id = data.get('room')
        student_sid = data.get('student_sid')
        if not room_id or room_id not in rooms:
            return
        room = rooms[room_id]
        if request.sid != room['teacher_sid']:
            return
        authority = get_room_authority(room_id)
        authority['mic_requests'].pop(student_sid, None)
        emit('mic-approved', {'approved': False}, room=student_sid)
    except Exception as e:
        debug_print(f"❌ Error in teacher-deny-mic: {e}")


@socketio.on('student-struggle-signal')
def handle_student_struggle_signal(data):
    try:
        room_id = data.get('room')
        signal = data.get('signal')
        if not room_id or room_id not in rooms or not signal:
            return
        room = rooms[room_id]
        sid = request.sid
        if sid not in room['participants']:
            return
        username = room['participants'][sid]['username']
        if room['teacher_sid']:
            emit('student-struggle-signal', {'username': username, 'type': signal}, room=room['teacher_sid'])
    except Exception as e:
        debug_print(f"❌ Error in student-struggle-signal: {e}")


@socketio.on('ping')
def handle_ping(data):
    emit('pong', {'timestamp': datetime.utcnow().isoformat()})
