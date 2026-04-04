import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from utils.helpers import login_required

live_bp = Blueprint('live', __name__)

@live_bp.route('/teacher')
def teacher_create():
    room_id = str(uuid.uuid4())[:8]
    return redirect(f'/teacher/{room_id}')

@live_bp.route('/teacher/<room_id>')
def teacher_view(room_id):
    return render_template('teacher.html', room_id=room_id)

@live_bp.route('/student/<room_id>')
def student_view(room_id):
    return render_template('student.html', room_id=room_id)

@live_bp.route('/join', methods=['POST'])
def join_room_post():
    room_id = request.form.get('room_id', '').strip()
    if not room_id:
        flash('Please enter a room ID')
        return redirect('/')
    return redirect(f'/student/{room_id}')

@live_bp.route('/live-meeting')
@live_bp.route('/live_meeting')
def live_meeting():
    return render_template('live_meeting.html')

@live_bp.route('/live-meeting/teacher')
@live_bp.route('/live_meeting/teacher')
def live_meeting_teacher_create():
    room_id = str(uuid.uuid4())[:8]
    return redirect(url_for('live.live_meeting_teacher_view', room_id=room_id))

@live_bp.route('/live-meeting/teacher/<room_id>')
@live_bp.route('/live_meeting/teacher/<room_id>')
def live_meeting_teacher_view(room_id):
    return render_template('teacher_live.html', room_id=room_id)

@live_bp.route('/live-meeting/student/<room_id>')
@live_bp.route('/live_meeting/student/<room_id>')
def live_meeting_student_view(room_id):
    return render_template('student_live.html', room_id=room_id)

@live_bp.route('/live-meeting/join', methods=['POST'])
@live_bp.route('/live_meeting/join', methods=['POST'])
def live_meeting_join():
    room_id = request.form.get('room_id', '').strip()
    username = request.form.get('username', '').strip()
    if not room_id:
        flash('Please enter a meeting ID')
        return redirect('/live_meeting')
    if not username:
        username = f"Student_{str(uuid.uuid4())[:4]}"
    session['live_username'] = username
    return redirect(url_for('live.live_meeting_student_view', room_id=room_id))

@live_bp.route('/test-connection')
def test_connection():
    return """
<!DOCTYPE html>
<html>
<head>
<title>Connection Test</title>
<script src="https://cdn.socket.io/4.5.0/socket.io.min.js"></script>
</head>
<body>
<h1>Socket.IO Connection Test</h1>
<div id="status">Connecting...</div>
<div id="events"></div>
<script>
    const socket = io();
    socket.on('connect', () => {
        document.getElementById('status').innerHTML = '✅ Connected! SID: ' + socket.id;
        logEvent('Connected to server');
    });
    socket.on('disconnect', () => {
        document.getElementById('status').innerHTML = '❌ Disconnected';
        logEvent('Disconnected from server');
    });
    socket.on('connect_error', (error) => {
        document.getElementById('status').innerHTML = '❌ Connection Error';
        logEvent('Error: ' + error.message);
    });
    function logEvent(msg) {
        const eventsDiv = document.getElementById('events');
        eventsDiv.innerHTML = new Date().toLocaleTimeString() + ': ' + msg + '<br>' + eventsDiv.innerHTML;
    }
</script>
</body>
</html>
"""

@live_bp.route('/debug/rooms')
def debug_rooms():
    from services.meeting_service import rooms, participants, room_authority
    import json
    debug_info = {'rooms': rooms, 'participants': participants, 'room_authority': room_authority, 'total_rooms': len(rooms), 'total_participants': len(participants)}
    return json.dumps(debug_info, indent=2, default=str)