from datetime import datetime
from extensions import db
from models import Room

# In-memory storage for live meetings
rooms = {}           # room_id -> room data
participants = {}    # socket_id -> participant info
room_authority = {}  # room_id -> authority state

def get_or_create_room(room_id):
    """Get existing room or create new one."""
    if room_id not in rooms:
        rooms[room_id] = {
            'participants': {},
            'teacher_sid': None,
            'created_at': datetime.utcnow().isoformat()
        }
    return rooms[room_id]

def get_room_authority(room_id):
    """Get or create authority state for a room."""
    if room_id not in room_authority:
        room_authority[room_id] = {
            'muted_all': False,
            'cameras_disabled': False,
            'mic_requests': {},
            'questions_enabled': True,
            'question_visibility': 'public'
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

def cleanup_room(room_id):
    """Remove empty rooms."""
    if room_id in rooms:
        room = rooms[room_id]
        if not room['participants']:
            del rooms[room_id]
            if room_id in room_authority:
                del room_authority[room_id]
            with db.engine.connect() as conn:
                Room.query.filter_by(id=room_id).delete()
                db.session.commit()