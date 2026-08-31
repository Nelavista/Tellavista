import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.helpers import login_required
from config import AGORA_APP_ID
from extensions import db
from models import Room, User

live_bp = Blueprint('live', __name__)


def _claim_room_ownership(room_id):
    """First logged-in visit to /teacher/<room_id> for a given room_id registers that
    user as the room's real owner (Room.teacher_user_id) -- events.py's Socket.IO
    join-room handler requires this to match before letting any socket claim the
    'teacher' role for the room, so knowing/guessing a room_id alone is no longer
    enough to become its teacher. A room_id is only ever handed out fresh (see
    teacher_create below), so the first claimant is legitimately the room's creator;
    a second, different logged-in user hitting the same URL later is refused rather
    than silently taking over an already-claimed room.
    """
    username = session.get('user', {}).get('username')
    user = User.query.filter_by(username=username).first() if username else None
    if not user:
        return None, False

    room = Room.query.get(room_id)
    if not room:
        room = Room(id=room_id, teacher_user_id=user.id, teacher_name=user.name or user.username)
        db.session.add(room)
        db.session.commit()
        return user, True
    if room.teacher_user_id is None:
        room.teacher_user_id = user.id
        db.session.commit()
        return user, True
    return user, room.teacher_user_id == user.id


@live_bp.route('/teacher')
@login_required
def teacher_create():
    room_id = str(uuid.uuid4())[:8]
    return redirect(f'/teacher/{room_id}')

@live_bp.route('/teacher/<room_id>')
@login_required
def teacher_view(room_id):
    user, owns_room = _claim_room_ownership(room_id)
    if not owns_room:
        flash("This room already has a different host.", 'error')
        return redirect(url_for('live.teacher_create'))
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
    # Live Meeting was retired as an Academia destination -- the landing page is gone
    # from nav. The teacher/student room routes below are left as-is (nothing in the
    # app links to them anymore, so they're unreachable via normal navigation) rather
    # than deleted, since the Room model/Socket.IO events may be reused later.
    return redirect(url_for('dashboard.dashboard'))

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
    user, owns_room = _claim_room_ownership(room_id)
    if not owns_room:
        flash("This room already has a different host.", 'error')
        return redirect(url_for('live.live_meeting_teacher_create'))
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
