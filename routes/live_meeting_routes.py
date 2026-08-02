import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.helpers import login_required
from config import AGORA_APP_ID

live_bp = Blueprint('live', __name__)

@live_bp.route('/teacher')
@login_required
def teacher_create():
    room_id = str(uuid.uuid4())[:8]
    return redirect(f'/teacher/{room_id}')

@live_bp.route('/teacher/<room_id>')
@login_required
def teacher_view(room_id):
    return render_template('teacher_live.html', room_id=room_id, agora_app_id=AGORA_APP_ID)

@live_bp.route('/student/<room_id>')
def student_view(room_id):
    username = session.get('live_username') or (session.get('user') or {}).get('username') or f'Student_{room_id[:4]}'
    return render_template('student_live.html', room_id=room_id, username=username, agora_app_id=AGORA_APP_ID)

@live_bp.route('/join', methods=['POST'])
def join_room_post():
    room_id = request.form.get('room_id', '').strip()
    if not room_id:
        flash('Please enter a room ID')
        return redirect('/')
    return redirect(f'/student/{room_id}')

@live_bp.route('/live-meeting')
@live_bp.route('/live_meeting')
@login_required
def live_meeting():
    return render_template('live_meeting.html')

@live_bp.route('/live-meeting/teacher')
@live_bp.route('/live_meeting/teacher')
@login_required
def live_meeting_teacher_create():
    room_id = str(uuid.uuid4())[:8]
    return redirect(url_for('live.live_meeting_teacher_view', room_id=room_id))

@live_bp.route('/live-meeting/teacher/<room_id>')
@live_bp.route('/live_meeting/teacher/<room_id>')
@login_required
def live_meeting_teacher_view(room_id):
    return render_template('teacher_live.html', room_id=room_id, agora_app_id=AGORA_APP_ID)

@live_bp.route('/live-meeting/student/<room_id>')
@live_bp.route('/live_meeting/student/<room_id>')
def live_meeting_student_view(room_id):
    username = session.get('live_username') or (session.get('user') or {}).get('username') or f'Student_{room_id[:4]}'
    return render_template('student_live.html', room_id=room_id, username=username, agora_app_id=AGORA_APP_ID)

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
