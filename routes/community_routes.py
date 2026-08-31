import os
import time
import cloudinary
import cloudinary.uploader
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from utils.helpers import login_required
from models import User, Group, GroupMember, GroupMessage, GroupFile
from extensions import db, socketio
from datetime import datetime

community_bp = Blueprint('community', __name__)

cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
    secure=True
)

ALLOWED_FILE_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'png', 'jpg', 'jpeg', 'gif', 'txt'}


def _current_user():
    username = session.get('user', {}).get('username')
    if not username:
        return None
    return User.query.filter_by(username=username).first()


def _room_name(group_id):
    return f'community_{group_id}'


@community_bp.route('/community')
@login_required
def community_page():
    # Community was retired as an Academia destination -- the group-chat page is gone
    # from nav, but the API endpoints below and the Group/GroupMessage models stay
    # (admin moderation at /admin/community still reads them).
    return redirect(url_for('dashboard.dashboard'))


@community_bp.route('/api/groups/create', methods=['POST'])
@login_required
def create_group():
    try:
        data = request.json
        user = _current_user()

        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        if not data or not data.get('name') or not data.get('type'):
            return jsonify({'success': False, 'error': 'Name and type required'}), 400

        new_group = Group(
            name=data['name'],
            description=data.get('description', ''),
            group_type=data['type'],
            privacy=data.get('privacy', 'public'),
            creator_id=user.id,
            created_at=datetime.utcnow()
        )
        db.session.add(new_group)
        db.session.flush()

        creator_member = GroupMember(
            group_id=new_group.id,
            user_id=user.id,
            role='admin',
            joined_at=datetime.utcnow()
        )
        db.session.add(creator_member)
        db.session.commit()

        return jsonify({
            'success': True,
            'group': new_group.to_dict(),
            'message': 'Group created successfully'
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] create_group: {str(e)}")
        return jsonify({'success': False, 'error': 'Server error'}), 500


@community_bp.route('/api/groups/list', methods=['GET'])
@login_required
def list_groups():
    try:
        group_type = request.args.get('type', 'all')
        search_query = request.args.get('search', '')
        user = _current_user()

        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        user_memberships = GroupMember.query.filter_by(user_id=user.id).all()
        user_group_ids = [gm.group_id for gm in user_memberships]

        if user_group_ids:
            query = Group.query.filter(
                (Group.privacy == 'public') | (Group.id.in_(user_group_ids))
            )
        else:
            query = Group.query.filter(Group.privacy == 'public')

        if group_type != 'all':
            query = query.filter(Group.group_type == group_type)
        if search_query:
            query = query.filter(
                (Group.name.ilike(f'%{search_query}%')) |
                (Group.description.ilike(f'%{search_query}%'))
            )

        groups = query.order_by(Group.created_at.desc()).all()

        groups_data = []
        for group in groups:
            member_count = GroupMember.query.filter_by(group_id=group.id).count()
            last_message = GroupMessage.query.filter_by(group_id=group.id)\
                .order_by(GroupMessage.created_at.desc()).first()
            groups_data.append({
                'id': group.id,
                'name': group.name,
                'description': group.description or '',
                'type': group.group_type,
                'privacy': group.privacy,
                'member_count': member_count,
                'is_member': group.id in user_group_ids,
                'created_at': group.created_at.isoformat() if group.created_at else None,
                'last_message_at': last_message.created_at.isoformat() if last_message and last_message.created_at else None,
            })

        groups_data.sort(key=lambda g: g['last_message_at'] or g['created_at'] or '', reverse=True)

        return jsonify({'success': True, 'groups': groups_data})
    except Exception as e:
        print(f"[ERROR] list_groups: {str(e)}")
        return jsonify({'success': False, 'error': 'Server error'}), 500


@community_bp.route('/api/groups/<int:group_id>/join', methods=['POST'])
@login_required
def join_group(group_id):
    try:
        user = _current_user()
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        group = Group.query.get(group_id)
        if not group:
            return jsonify({'success': False, 'error': 'Group not found'}), 404

        existing = GroupMember.query.filter_by(group_id=group_id, user_id=user.id).first()
        if existing:
            return jsonify({'success': False, 'error': 'Already a member'}), 400
        if group.privacy == 'private':
            return jsonify({'success': False, 'error': 'Private group requires invite'}), 403

        new_member = GroupMember(group_id=group_id, user_id=user.id, role='member', joined_at=datetime.utcnow())
        db.session.add(new_member)

        display_name = (user.name or user.username).strip()
        system_msg = GroupMessage(
            group_id=group_id, sender_id=user.id,
            content=f'{display_name} joined the group', message_type='system',
            created_at=datetime.utcnow()
        )
        db.session.add(system_msg)
        db.session.commit()

        socketio.emit('community-message', system_msg.to_dict(), room=_room_name(group_id))
        socketio.emit('community-member-count', {'member_count': GroupMember.query.filter_by(group_id=group_id).count()}, room=_room_name(group_id))

        return jsonify({'success': True, 'message': 'Joined group successfully'})
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] join_group: {str(e)}")
        return jsonify({'success': False, 'error': 'Server error'}), 500


@community_bp.route('/api/groups/<int:group_id>/leave', methods=['POST'])
@login_required
def leave_group(group_id):
    try:
        user = _current_user()
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        membership = GroupMember.query.filter_by(group_id=group_id, user_id=user.id).first()
        if not membership:
            return jsonify({'success': False, 'error': 'Not a member'}), 400

        if membership.role == 'admin':
            admin_count = GroupMember.query.filter_by(group_id=group_id, role='admin').count()
            if admin_count <= 1:
                return jsonify({'success': False, 'error': 'You are the only admin'}), 400

        db.session.delete(membership)
        db.session.commit()

        socketio.emit('community-member-count', {'member_count': GroupMember.query.filter_by(group_id=group_id).count()}, room=_room_name(group_id))

        return jsonify({'success': True, 'message': 'Left group successfully'})
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] leave_group: {str(e)}")
        return jsonify({'success': False, 'error': 'Server error'}), 500


@community_bp.route('/api/groups/<int:group_id>/info', methods=['GET'])
@login_required
def group_info(group_id):
    """Get detailed group information"""
    try:
        user = _current_user()
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        group = Group.query.get(group_id)
        if not group:
            return jsonify({'success': False, 'error': 'Group not found'}), 404

        member_count = GroupMember.query.filter_by(group_id=group_id).count()

        membership = GroupMember.query.filter_by(group_id=group_id, user_id=user.id).first()
        is_member = membership is not None
        user_role = membership.role if membership else None

        return jsonify({
            'success': True,
            'group': {
                'id': group.id,
                'name': group.name,
                'description': group.description or '',
                'type': group.group_type,
                'privacy': group.privacy,
                'member_count': member_count,
                'is_member': is_member,
                'user_role': user_role,
                'is_creator': group.creator_id == user.id,
                'created_at': group.created_at.isoformat() if group.created_at else None
            }
        })
    except Exception as e:
        print(f"[ERROR] group_info: {str(e)}")
        return jsonify({'success': False, 'error': 'Server error: ' + str(e)}), 500


@community_bp.route('/api/groups/<int:group_id>/members', methods=['GET'])
@login_required
def get_group_members(group_id):
    try:
        user = _current_user()
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        membership = GroupMember.query.filter_by(group_id=group_id, user_id=user.id).first()
        if not membership:
            return jsonify({'success': False, 'error': 'Not a member'}), 403

        members = GroupMember.query.filter_by(group_id=group_id).order_by(GroupMember.joined_at.asc()).all()
        members_data = []
        for m in members:
            u = m.user
            members_data.append({
                'user_id': m.user_id,
                'username': u.username if u else 'unknown',
                'display_name': (u.name or u.username) if u else 'Unknown',
                'role': m.role,
                'joined_at': m.joined_at.isoformat() if m.joined_at else None,
            })

        return jsonify({'success': True, 'members': members_data, 'your_role': membership.role})
    except Exception as e:
        print(f"[ERROR] get_group_members: {str(e)}")
        return jsonify({'success': False, 'error': 'Server error'}), 500


@community_bp.route('/api/groups/<int:group_id>/members/<int:user_id>/remove', methods=['POST'])
@login_required
def remove_group_member(group_id, user_id):
    try:
        user = _current_user()
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        requester_membership = GroupMember.query.filter_by(group_id=group_id, user_id=user.id).first()
        if not requester_membership or requester_membership.role != 'admin':
            return jsonify({'success': False, 'error': 'Only group admins can remove members'}), 403

        if user_id == user.id:
            return jsonify({'success': False, 'error': 'Use Leave Group to remove yourself'}), 400

        target_membership = GroupMember.query.filter_by(group_id=group_id, user_id=user_id).first()
        if not target_membership:
            return jsonify({'success': False, 'error': 'That user is not a member'}), 404

        target_user = User.query.get(user_id)
        display_name = (target_user.name or target_user.username).strip() if target_user else 'A member'

        db.session.delete(target_membership)
        system_msg = GroupMessage(
            group_id=group_id, sender_id=user.id,
            content=f'{display_name} was removed from the group', message_type='system',
            created_at=datetime.utcnow()
        )
        db.session.add(system_msg)
        db.session.commit()

        socketio.emit('community-message', system_msg.to_dict(), room=_room_name(group_id))
        socketio.emit('community-member-removed', {'user_id': user_id}, room=_room_name(group_id))
        socketio.emit('community-member-count', {'member_count': GroupMember.query.filter_by(group_id=group_id).count()}, room=_room_name(group_id))

        return jsonify({'success': True, 'message': 'Member removed'})
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] remove_group_member: {str(e)}")
        return jsonify({'success': False, 'error': 'Server error'}), 500


@community_bp.route('/api/groups/<int:group_id>', methods=['DELETE'])
@login_required
def delete_group(group_id):
    try:
        user = _current_user()
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        group = Group.query.get(group_id)
        if not group:
            return jsonify({'success': False, 'error': 'Group not found'}), 404

        if group.creator_id != user.id and not user.is_admin:
            return jsonify({'success': False, 'error': 'Only the group creator or a platform admin can delete this group'}), 403

        # Best-effort cleanup of any files uploaded to this group before the cascade delete.
        for f in GroupFile.query.filter_by(group_id=group_id).all():
            if f.cloudinary_public_id:
                try:
                    cloudinary.uploader.destroy(f.cloudinary_public_id, resource_type='raw')
                except Exception as cleanup_err:
                    print(f"[WARN] Failed to clean up Cloudinary file {f.cloudinary_public_id}: {cleanup_err}")

        socketio.emit('community-group-deleted', {'group_id': group_id}, room=_room_name(group_id))

        db.session.delete(group)  # cascades to members/messages/files/events via relationship config
        db.session.commit()

        return jsonify({'success': True, 'message': 'Group deleted'})
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] delete_group: {str(e)}")
        return jsonify({'success': False, 'error': 'Server error'}), 500


@community_bp.route('/api/groups/<int:group_id>/messages', methods=['GET'])
@login_required
def get_group_messages(group_id):
    """Get messages for a group"""
    try:
        user = _current_user()
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        membership = GroupMember.query.filter_by(group_id=group_id, user_id=user.id).first()
        if not membership:
            return jsonify({'success': False, 'error': 'Not a member'}), 403

        limit = request.args.get('limit', 50, type=int)

        messages = GroupMessage.query.filter_by(group_id=group_id)\
            .order_by(GroupMessage.created_at.desc())\
            .limit(limit).all()
        messages.reverse()

        messages_data = [_serialize_message(msg, user.id) for msg in messages]

        return jsonify({'success': True, 'messages': messages_data})
    except Exception as e:
        print(f"[ERROR] get_group_messages: {str(e)}")
        return jsonify({'success': False, 'error': 'Server error'}), 500


def _serialize_message(msg, viewer_id):
    sender = msg.sender
    if sender and sender.name and sender.name.strip():
        sender_name = sender.name.strip()
    elif sender:
        sender_name = sender.username
    else:
        sender_name = 'Unknown'

    data = {
        'id': msg.id,
        'sender_name': sender_name,
        'sender_id': msg.sender_id,
        'is_mine': msg.sender_id == viewer_id,
        'content': msg.content,
        'message_type': msg.message_type,
        'reply_to_id': msg.reply_to_id,
        'created_at': msg.created_at.isoformat() if msg.created_at else None,
        'edited_at': msg.edited_at.isoformat() if msg.edited_at else None,
    }
    if msg.message_type == 'file' and msg.file:
        data['file'] = msg.file.to_dict()
    return data


@community_bp.route('/api/groups/<int:group_id>/send', methods=['POST'])
@login_required
def send_group_message(group_id):
    """Send a message to a group"""
    try:
        user = _current_user()
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        membership = GroupMember.query.filter_by(group_id=group_id, user_id=user.id).first()
        if not membership:
            return jsonify({'success': False, 'error': 'Not a member'}), 403

        data = request.json
        if not data or not data.get('content'):
            return jsonify({'success': False, 'error': 'Message content required'}), 400

        new_message = GroupMessage(
            group_id=group_id,
            sender_id=user.id,
            content=data['content'].strip()[:4000],
            message_type=data.get('type', 'text'),
            reply_to_id=data.get('reply_to_id'),
            created_at=datetime.utcnow()
        )
        db.session.add(new_message)
        db.session.commit()

        msg_data = _serialize_message(new_message, user.id)
        socketio.emit('community-message', {**msg_data, 'is_mine': False}, room=_room_name(group_id), skip_sid=request.headers.get('X-Socket-ID'))

        return jsonify({'success': True, 'message': msg_data})
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] send_group_message: {str(e)}")
        return jsonify({'success': False, 'error': 'Server error: ' + str(e)}), 500


@community_bp.route('/api/groups/<int:group_id>/messages/<int:message_id>/edit', methods=['POST'])
@login_required
def edit_group_message(group_id, message_id):
    try:
        user = _current_user()
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        msg = GroupMessage.query.filter_by(id=message_id, group_id=group_id).first()
        if not msg:
            return jsonify({'success': False, 'error': 'Message not found'}), 404
        if msg.sender_id != user.id:
            return jsonify({'success': False, 'error': 'You can only edit your own messages'}), 403
        if msg.message_type != 'text':
            return jsonify({'success': False, 'error': 'Only text messages can be edited'}), 400

        new_content = (request.json or {}).get('content', '').strip()
        if not new_content:
            return jsonify({'success': False, 'error': 'Message cannot be empty'}), 400

        msg.content = new_content[:4000]
        msg.edited_at = datetime.utcnow()
        db.session.commit()

        msg_data = _serialize_message(msg, user.id)
        socketio.emit('community-message-edited', {**msg_data, 'is_mine': False}, room=_room_name(group_id))

        return jsonify({'success': True, 'message': msg_data})
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] edit_group_message: {str(e)}")
        return jsonify({'success': False, 'error': 'Server error'}), 500


@community_bp.route('/api/groups/<int:group_id>/messages/<int:message_id>', methods=['DELETE'])
@login_required
def delete_group_message(group_id, message_id):
    try:
        user = _current_user()
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        msg = GroupMessage.query.filter_by(id=message_id, group_id=group_id).first()
        if not msg:
            return jsonify({'success': False, 'error': 'Message not found'}), 404

        membership = GroupMember.query.filter_by(group_id=group_id, user_id=user.id).first()
        is_own = msg.sender_id == user.id
        is_group_admin = membership and membership.role == 'admin'
        if not (is_own or is_group_admin):
            return jsonify({'success': False, 'error': 'You cannot delete this message'}), 403

        db.session.delete(msg)
        db.session.commit()

        socketio.emit('community-message-deleted', {'message_id': message_id}, room=_room_name(group_id))

        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] delete_group_message: {str(e)}")
        return jsonify({'success': False, 'error': 'Server error'}), 500


@community_bp.route('/api/groups/<int:group_id>/upload', methods=['POST'])
@login_required
def upload_group_file(group_id):
    try:
        user = _current_user()
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        membership = GroupMember.query.filter_by(group_id=group_id, user_id=user.id).first()
        if not membership:
            return jsonify({'success': False, 'error': 'Not a member'}), 403

        file = request.files.get('file')
        if not file or not file.filename:
            return jsonify({'success': False, 'error': 'No file provided'}), 400

        ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
        if ext not in ALLOWED_FILE_EXTENSIONS:
            return jsonify({'success': False, 'error': f'File type .{ext} is not allowed'}), 400

        is_image = ext in {'png', 'jpg', 'jpeg', 'gif'}
        public_id = f"nelavista_community/{group_id}_{int(time.time())}_{file.filename.rsplit('.', 1)[0][:40].replace(' ', '_')}"
        upload_result = cloudinary.uploader.upload(
            file,
            resource_type='image' if is_image else 'raw',
            public_id=public_id,
            overwrite=False
        )
        file_url = upload_result.get('secure_url')
        if not file_url:
            return jsonify({'success': False, 'error': 'Upload failed'}), 500

        group_file = GroupFile(
            group_id=group_id,
            uploader_id=user.id,
            file_name=file.filename,
            file_type=ext,
            cloudinary_url=file_url,
            cloudinary_public_id=upload_result.get('public_id'),
            file_size=upload_result.get('bytes'),
            uploaded_at=datetime.utcnow()
        )
        db.session.add(group_file)
        db.session.flush()  # assigns group_file.id so the message can reference it

        new_message = GroupMessage(
            group_id=group_id,
            sender_id=user.id,
            content=file.filename,
            message_type='file',
            file_id=group_file.id,
            created_at=datetime.utcnow()
        )
        db.session.add(new_message)
        db.session.commit()

        msg_data = _serialize_message(new_message, user.id)
        socketio.emit('community-message', {**msg_data, 'is_mine': False}, room=_room_name(group_id), skip_sid=request.headers.get('X-Socket-ID'))

        return jsonify({'success': True, 'message': msg_data})
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] upload_group_file: {str(e)}")
        return jsonify({'success': False, 'error': 'Server error: ' + str(e)}), 500
