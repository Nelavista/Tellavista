from flask import request
from flask_socketio import emit, join_room, leave_room
from extensions import socketio, db
from models import Room
from services.meeting_service import rooms, participants, room_authority, get_or_create_room, get_room_authority, get_participants_list, cleanup_room
from utils.helpers import debug_print
from datetime import datetime

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
        authority_state = get_room_authority(room_id)
        if role == 'teacher' and room['teacher_sid']:
            emit('error', {'message': 'Room already has a teacher'})
            return
        room['participants'][sid] = {'username': username, 'role': role, 'joined_at': datetime.utcnow().isoformat()}
        if role == 'teacher':
            room['teacher_sid'] = sid
            authority_state['teacher_sid'] = sid
            with db.engine.connect() as conn:
                existing_room = Room.query.get(room_id)
                if not existing_room:
                    room_db = Room(id=room_id, teacher_id=sid, teacher_name=username, is_active=True)
                    db.session.add(room_db)
                else:
                    existing_room.teacher_id = sid
                    existing_room.teacher_name = username
                db.session.commit()
            for p_sid in room['participants']:
                if room['participants'][p_sid]['role'] == 'student':
                    emit('teacher-joined', {'teacher_sid': sid, 'teacher_name': username}, room=p_sid)
        participants[sid] = {'room_id': room_id, 'username': username, 'role': role}
        join_room(room_id)
        existing_participants = get_participants_list(room_id, exclude_sid=sid)
        emit('room-joined', {'room': room_id, 'sid': sid, 'username': username, 'role': role, 'existing_participants': existing_participants, 'teacher_sid': room['teacher_sid'], 'is_waiting': (role == 'student' and not room['teacher_sid'])})
        emit('new-participant', {'sid': sid, 'username': username, 'role': role}, room=room_id, skip_sid=sid)
        if role == 'student' and room['teacher_sid']:
            emit('room-state', {'muted_all': authority_state['muted_all'], 'cameras_disabled': authority_state['cameras_disabled'], 'questions_enabled': authority_state['questions_enabled'], 'question_visibility': authority_state['question_visibility']})
        debug_print(f"✅ {username} joined room {room_id}. Total participants: {len(room['participants'])}")
    except Exception as e:
        debug_print(f"❌ Error in join-room: {e}")
        emit('error', {'message': str(e)})

@socketio.on('webrtc-offer')
def handle_webrtc_offer(data):
    try:
        room_id = data.get('room')
        target_sid = data.get('target_sid')
        offer = data.get('offer')
        if not all([room_id, target_sid, offer]):
            return
        sender = participants.get(request.sid)
        target = participants.get(target_sid)
        if not sender or not target or sender['room_id'] != room_id or target['room_id'] != room_id:
            return
        emit('webrtc-offer', {'from_sid': request.sid, 'offer': offer, 'room': room_id}, room=target_sid)
    except Exception as e:
        debug_print(f"❌ Error relaying offer: {e}")

@socketio.on('webrtc-answer')
def handle_webrtc_answer(data):
    try:
        room_id = data.get('room')
        target_sid = data.get('target_sid')
        answer = data.get('answer')
        if not all([room_id, target_sid, answer]):
            return
        sender = participants.get(request.sid)
        target = participants.get(target_sid)
        if not sender or not target or sender['room_id'] != room_id or target['room_id'] != room_id:
            return
        emit('webrtc-answer', {'from_sid': request.sid, 'answer': answer, 'room': room_id}, room=target_sid)
    except Exception as e:
        debug_print(f"❌ Error relaying answer: {e}")

@socketio.on('webrtc-ice-candidate')
def handle_webrtc_ice_candidate(data):
    try:
        room_id = data.get('room')
        target_sid = data.get('target_sid')
        candidate = data.get('candidate')
        if not all([room_id, target_sid, candidate]):
            return
        sender = participants.get(request.sid)
        target = participants.get(target_sid)
        if not sender or not target or sender['room_id'] != room_id or target['room_id'] != room_id:
            return
        emit('webrtc-ice-candidate', {'from_sid': request.sid, 'candidate': candidate, 'room': room_id}, room=target_sid)
    except Exception as e:
        debug_print(f"❌ Error relaying ICE candidate: {e}")

@socketio.on('request-full-mesh')
def handle_request_full_mesh(data):
    try:
        room_id = data.get('room')
        sid = request.sid
        if not room_id or room_id not in rooms or sid not in rooms[room_id]['participants']:
            return
        room = rooms[room_id]
        other_participants = [{'sid': other_sid, 'username': info['username'], 'role': info['role']} for other_sid, info in room['participants'].items() if other_sid != sid]
        emit('initiate-mesh-connections', {'peers': other_participants, 'room': room_id}, room=sid)
        debug_print(f"🔗 Initiating full mesh for {sid[:8]} with {len(other_participants)} peers")
    except Exception as e:
        debug_print(f"❌ Error in request-full-mesh: {e}")

@socketio.on('teacher-mute-all')
def handle_teacher_mute_all(data):
    try:
        room_id = data.get('room')
        if not room_id or room_id not in rooms:
            return
        room = rooms[room_id]
        teacher_sid = request.sid
        if teacher_sid != room['teacher_sid']:
            return
        authority = get_room_authority(room_id)
        authority['muted_all'] = True
        for sid in room['participants']:
            if room['participants'][sid]['role'] == 'student':
                emit('room-muted', {'muted': True}, room=sid)
        debug_print(f"🔇 Teacher muted all in room {room_id}")
    except Exception as e:
        debug_print(f"❌ Error in teacher-mute-all: {e}")

@socketio.on('teacher-unmute-all')
def handle_teacher_unmute_all(data):
    try:
        room_id = data.get('room')
        if not room_id or room_id not in rooms:
            return
        room = rooms[room_id]
        teacher_sid = request.sid
        if teacher_sid != room['teacher_sid']:
            return
        authority = get_room_authority(room_id)
        authority['muted_all'] = False
        for sid in room['participants']:
            if room['participants'][sid]['role'] == 'student':
                emit('room-muted', {'muted': False}, room=sid)
        debug_print(f"🔊 Teacher unmuted all in room {room_id}")
    except Exception as e:
        debug_print(f"❌ Error in teacher-unmute-all: {e}")

@socketio.on('start-broadcast')
def handle_start_broadcast(data):
    try:
        room_id = data.get('room')
        if room_id not in rooms:
            emit('error', {'message': 'Room not found'})
            return
        room = rooms[room_id]
        teacher_sid = request.sid
        if teacher_sid != room['teacher_sid']:
            emit('error', {'message': 'Only teacher can start broadcast'})
            return
        debug_print(f"📢 Teacher starting broadcast in room: {room_id}")
        student_sids = []
        student_info = []
        for sid, info in room['participants'].items():
            if info['role'] == 'student':
                student_sids.append(sid)
                student_info.append({'sid': sid, 'username': info['username']})
        emit('broadcast-ready', {'student_sids': student_sids, 'student_info': student_info, 'student_count': len(student_sids), 'room': room_id}, room=teacher_sid)
        for student_sid in student_sids:
            peers_to_connect = [{'sid': other_sid, 'username': room['participants'][other_sid]['username'], 'role': room['participants'][other_sid]['role']} for other_sid in room['participants'] if other_sid != student_sid]
            emit('initiate-full-mesh', {'peers': peers_to_connect, 'teacher_sid': teacher_sid, 'room': room_id}, room=student_sid)
    except Exception as e:
        debug_print(f"❌ Error in start-broadcast: {e}")
        emit('error', {'message': str(e)})

@socketio.on('ping')
def handle_ping(data):
    emit('pong', {'timestamp': datetime.utcnow().isoformat()})