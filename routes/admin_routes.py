from flask import Blueprint, render_template, jsonify, session, request
from utils.helpers import login_required, admin_required
from models import User, Material, Video, Group, GroupMember, GroupMessage, Room, StudySession, Exam
from sqlalchemy import func
from services.meeting_service import end_room_session, rooms as live_rooms_memory
from extensions import db
import cloudinary
import cloudinary.uploader

admin_bp = Blueprint('admin', __name__)


def _current_admin():
    username = session['user']['username']
    return User.query.filter_by(username=username).first()


# ===== ADMIN DASHBOARD HUB =====
@admin_bp.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    stats = {
        'total_users': User.query.count(),
        'admin_count': User.query.filter_by(is_admin=True).count(),
        'total_materials': Material.query.count(),
        'pending_materials': Material.query.filter_by(is_approved=False).count(),
        'total_videos': Video.query.count(),
        'pending_videos': Video.query.filter_by(is_approved=False).count(),
        'total_groups': Group.query.count(),
        'total_messages': GroupMessage.query.count(),
        'live_rooms': Room.query.filter_by(is_live=True).count(),
        'total_rooms_ever': Room.query.count(),
        'total_study_sessions': StudySession.query.count(),
        'total_exams': Exam.query.count(),
    }
    recent_users = User.query.order_by(User.joined_on.desc()).limit(6).all()
    return render_template('admin_dashboard.html', stats=stats, recent_users=recent_users, active_page='dashboard')


# ===== USER MANAGEMENT =====
@admin_bp.route('/admin/users')
@login_required
@admin_required
def admin_users():
    search = request.args.get('search', '').strip()
    query = User.query
    if search:
        like = f'%{search}%'
        query = query.filter(
            (User.username.ilike(like)) | (User.email.ilike(like)) | (User.name.ilike(like))
        )
    users = query.order_by(User.joined_on.desc()).all()
    return render_template('admin_users.html', users=users, search=search, active_page='users')


@admin_bp.route('/admin/users/<int:user_id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_user_admin(user_id):
    actor = _current_admin()
    target = User.query.get(user_id)
    if not target:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    if target.id == actor.id and target.is_admin:
        return jsonify({'success': False, 'error': "You can't remove your own admin access"}), 400
    target.is_admin = not target.is_admin
    db.session.commit()
    return jsonify({'success': True, 'is_admin': target.is_admin})


@admin_bp.route('/admin/users/<int:user_id>/activity')
@login_required
@admin_required
def admin_user_activity(user_id):
    """Usage metadata only — logins, upload counts, message counts, study time.
    Deliberately excludes message content: this is a usage overview, not a
    surveillance log. For a specific reported message, use Community moderation."""
    target = User.query.get_or_404(user_id)

    total_seconds = db.session.query(func.sum(StudySession.seconds)).filter_by(user_id=target.id).scalar() or 0
    study_days = StudySession.query.filter_by(user_id=target.id).count()

    materials = Material.query.filter_by(uploaded_by=target.username).order_by(Material.created_at.desc()).all()
    videos = Video.query.filter_by(username=target.username).order_by(Video.created_at.desc()).all()
    exams = Exam.query.filter_by(user_id=target.id).count()
    groups_created = Group.query.filter_by(creator_id=target.id).count()

    memberships = GroupMember.query.filter_by(user_id=target.id).all()
    membership_data = []
    total_messages = 0
    for m in memberships:
        msg_count = GroupMessage.query.filter_by(group_id=m.group_id, sender_id=target.id).count()
        total_messages += msg_count
        membership_data.append({
            'group_name': m.group.name if m.group else 'Deleted group',
            'role': m.role,
            'joined_at': m.joined_at,
            'message_count': msg_count,
        })

    activity = {
        'total_study_hours': round(total_seconds / 3600, 1),
        'study_days': study_days,
        'materials_uploaded': len(materials),
        'materials_pending': sum(1 for m in materials if not m.is_approved),
        'videos_uploaded': len(videos),
        'videos_pending': sum(1 for v in videos if not v.is_approved),
        'exams_logged': exams,
        'groups_created': groups_created,
        'total_messages_sent': total_messages,
    }

    return render_template(
        'admin_user_activity.html',
        target=target,
        activity=activity,
        materials=materials[:10],
        videos=videos[:10],
        memberships=membership_data,
        active_page='users',
    )


@admin_bp.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    actor = _current_admin()
    target = User.query.get(user_id)
    if not target:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    if target.id == actor.id:
        return jsonify({'success': False, 'error': "You can't delete your own account here"}), 400
    try:
        db.session.delete(target)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        # This user owns groups/messages/etc. with foreign keys pointing at them — refuse
        # rather than silently cascading deletes into other users' shared data.
        return jsonify({
            'success': False,
            'error': 'This user has associated data (groups, messages, or materials) and cannot be deleted directly. Remove admin access instead, or clean up their content first.'
        }), 409


# ===== COMMUNITY MODERATION =====
@admin_bp.route('/admin/community')
@login_required
@admin_required
def admin_community():
    groups = Group.query.order_by(Group.created_at.desc()).all()
    groups_data = []
    for g in groups:
        groups_data.append({
            'id': g.id,
            'name': g.name,
            'description': g.description or '',
            'type': g.group_type,
            'privacy': g.privacy,
            'creator': g.creator.username if g.creator else 'unknown',
            'member_count': GroupMember.query.filter_by(group_id=g.id).count(),
            'message_count': GroupMessage.query.filter_by(group_id=g.id).count(),
            'created_at': g.created_at,
        })
    return render_template('admin_community.html', groups=groups_data, active_page='community')


@admin_bp.route('/admin/community/<int:group_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_group(group_id):
    group = Group.query.get(group_id)
    if not group:
        return jsonify({'success': False, 'error': 'Group not found'}), 404
    for f in group.files:
        if f.cloudinary_public_id:
            try:
                cloudinary.uploader.destroy(f.cloudinary_public_id, resource_type='raw')
            except Exception:
                pass
    db.session.delete(group)
    db.session.commit()
    return jsonify({'success': True})


# ===== LIVE ROOMS MONITOR =====
@admin_bp.route('/admin/live-rooms')
@login_required
@admin_required
def admin_live_rooms():
    rooms = Room.query.filter_by(is_active=True).order_by(Room.created_at.desc()).all()
    rooms_data = []
    for r in rooms:
        memory_state = live_rooms_memory.get(r.id, {})
        rooms_data.append({
            'id': r.id,
            'teacher_name': r.teacher_name,
            'is_live': r.is_live,
            'started_at': r.started_at,
            'created_at': r.created_at,
            'participant_count': len(memory_state.get('participants', {})),
        })
    return render_template('admin_live_rooms.html', rooms=rooms_data, active_page='live_rooms')


@admin_bp.route('/admin/live-rooms/<room_id>/end', methods=['POST'])
@login_required
@admin_required
def admin_end_room(room_id):
    room = Room.query.get(room_id)
    if not room:
        return jsonify({'success': False, 'error': 'Room not found'}), 404
    end_room_session(room_id)
    return jsonify({'success': True})


# ===== MATERIALS MODERATION (existing) =====
@admin_bp.route('/admin/materials')
@login_required
@admin_required
def admin_materials():
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()

    # Get all pending materials
    pending = Material.query.filter_by(is_approved=False).order_by(Material.id.desc()).all()

    return render_template('admin_materials.html', pending=pending, user=user, active_page='materials')


@admin_bp.route('/admin/materials/approve/<int:material_id>', methods=['POST'])
@login_required
@admin_required
def approve_material(material_id):
    material = Material.query.get(material_id)
    if not material:
        return jsonify({'error': 'Material not found'}), 404

    material.is_approved = True
    db.session.commit()

    return jsonify({'success': True, 'message': 'Material approved'})


@admin_bp.route('/admin/materials/reject/<int:material_id>', methods=['DELETE'])
@login_required
@admin_required
def reject_material(material_id):
    material = Material.query.get(material_id)
    if not material:
        return jsonify({'error': 'Material not found'}), 404

    # Delete from Cloudinary if needed
    if material.file_url and material.source == 'uploaded':
        try:
            parts = material.file_url.split('/upload/')
            if len(parts) == 2:
                path_part = parts[1]
                segments = path_part.split('/')
                if segments[0].startswith('v') and segments[0][1:].isdigit():
                    segments = segments[1:]
                public_id = '/'.join(segments)
                cloudinary.uploader.destroy(public_id, resource_type='raw')
        except Exception:
            pass

    db.session.delete(material)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Material rejected and deleted'})


@admin_bp.route('/debug/check-admin')
@login_required
@admin_required
def debug_check_admin():
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()

    return jsonify({
        'username': user.username,
        'is_admin': user.is_admin,
        'user_level': user.user_level,
        'all_user_fields': {
            'name': user.name,
            'department': user.department,
            'level': user.level,
            'semester': user.semester
        }
    })
