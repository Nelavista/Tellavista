from flask import request, session
from flask_socketio import join_room, leave_room
from extensions import socketio
from models import GroupMember, User


def _current_user_id():
    username = session.get('user', {}).get('username')
    if not username:
        return None
    user = User.query.filter_by(username=username).first()
    return user.id if user else None


@socketio.on('join-community-group')
def handle_join_community_group(data):
    """A client opened a group's chat — put their socket in that group's room so they get
    community-message/edited/deleted events pushed live instead of polling for them."""
    group_id = data.get('group_id') if data else None
    if not group_id:
        return
    user_id = _current_user_id()
    if not user_id:
        return
    is_member = GroupMember.query.filter_by(group_id=group_id, user_id=user_id).first()
    if not is_member:
        return
    join_room(f'community_{group_id}')


@socketio.on('leave-community-group')
def handle_leave_community_group(data):
    group_id = data.get('group_id') if data else None
    if not group_id:
        return
    leave_room(f'community_{group_id}')
