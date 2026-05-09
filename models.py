from datetime import datetime
import json
from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    user_level = db.Column(db.Integer, default=1)
    joined_on = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    name = db.Column(db.String(100))
    university = db.Column(db.String(150))
    faculty = db.Column(db.String(150))
    department = db.Column(db.String(150))
    level = db.Column(db.String(50))
    semester = db.Column(db.String(20))

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)


class UserQuestions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, index=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    memory_layer = db.Column(db.String(50))


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    level = db.Column(db.String(50))
    department = db.Column(db.String(100))
    traits = db.Column(db.Text)
    explanation_style = db.Column(db.String(50))
    focus_areas = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "username": self.username,
            "level": self.level,
            "department": self.department,
            "traits": json.loads(self.traits) if self.traits else [],
            "explanation_style": self.explanation_style,
            "focus_areas": json.loads(self.focus_areas) if self.focus_areas else []
        }


class Room(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    teacher_id = db.Column(db.String(120))
    teacher_name = db.Column(db.String(80))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Video(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    creator_name = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(200), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    caption = db.Column(db.Text)
    video_url = db.Column(db.String(500), nullable=False)
    bank_name = db.Column(db.String(100))
    account_number = db.Column(db.String(20))
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_approved = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(150))

    def to_dict(self):
        return {
            'id': self.id,
            'creator_name': self.creator_name,
            'department': self.department,
            'course': self.course,
            'level': self.level,
            'semester': self.semester,
            'caption': self.caption,
            'video_url': self.video_url,
            'views': self.views,
            'likes': self.likes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_approved': self.is_approved
        }


class Material(db.Model):
    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    # ── core classification ──────────────────────────────────────────────────
    department = db.Column(db.String(150), nullable=False)   # e.g. "Computer Science"
    level = db.Column(db.String(50), nullable=False)         # e.g. "200"
    semester = db.Column(db.String(20), nullable=False)      # "First Semester" / "Second Semester"

    # ── authorship / description ─────────────────────────────────────────────
    author = db.Column(db.String(200))
    description = db.Column(db.Text)
    license = db.Column(db.String(100), default='Student Upload')

    # ── file storage ─────────────────────────────────────────────────────────
    file_url = db.Column(db.String(500))                     # Cloudinary secure URL
    cloudinary_public_id = db.Column(db.String(300))

    # ── GOOGLE CUSTOM SEARCH INTEGRATION ─────────────────────────────────────
    external_url = db.Column(db.String(500))                 # Direct PDF link from Google search
    source = db.Column(db.String(50), default='uploaded')    # 'static', 'uploaded', 'google_auto'
    course_code = db.Column(db.String(20))                   # Actual course code column (MAT101, CSC111, etc.)

    # ── misc ─────────────────────────────────────────────────────────────────
    course_type = db.Column(db.String(20), default='CORE')   # Stores course type like "CORE", "ELECTIVE"
    next_topic = db.Column(db.String(200))
    progress = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    downloads = db.Column(db.Integer, default=0)
    uploaded_by = db.Column(db.String(150))                  # username of uploader
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_approved = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'department': self.department,
            'level': self.level,
            'semester': self.semester,
            'course_code': self.course_code or self.course_type,
            'author': self.author,
            'description': self.description,
            'license': self.license or 'Student Upload',
            'file_url': self.file_url,
            'external_url': self.external_url,
            'source': self.source or 'uploaded',
            'course_type': self.course_type,
            'views': self.views or 0,
            'downloads': self.downloads or 0,
            'uploaded_by': self.uploaded_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_approved': self.is_approved
        }


# ===== Study Session Tracking =====
class StudySession(db.Model):
    __tablename__ = 'study_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    seconds = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('study_sessions', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.isoformat() if self.date else None,
            'seconds': self.seconds,
            'hours': round(self.seconds / 3600, 1)
        }


# ===== Exam Tracking =====
class Exam(db.Model):
    __tablename__ = 'exams'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('exams', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'course': self.course,
            'date': self.date.isoformat() if self.date else None,
            'duration': self.duration
        }


# ===== Google Search Cache =====
class GoogleSearchCache(db.Model):
    """
    Optional table to track Google API calls and cache search results.
    Helps avoid duplicate API calls within a time window.
    """
    __tablename__ = 'google_search_cache'
    
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), nullable=False, index=True)
    search_query = db.Column(db.String(500))
    result_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'course_code': self.course_code,
            'search_query': self.search_query,
            'result_count': self.result_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        }


# ============================================================
# ===== COMMUNITY FEATURE MODELS =====
# ============================================================

class Group(db.Model):
    """Community groups"""
    __tablename__ = 'groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    group_type = db.Column(db.String(20), nullable=False)  # course, study, social
    privacy = db.Column(db.String(20), default='public')  # public, private
    avatar_url = db.Column(db.String(500))
    cover_image_url = db.Column(db.String(500))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', foreign_keys=[creator_id], backref='created_groups')
    members = db.relationship('GroupMember', back_populates='group', cascade='all, delete-orphan')
    messages = db.relationship('GroupMessage', back_populates='group', cascade='all, delete-orphan')
    files = db.relationship('GroupFile', back_populates='group', cascade='all, delete-orphan')
    events = db.relationship('GroupEvent', back_populates='group', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.group_type,
            'privacy': self.privacy,
            'creator_id': self.creator_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class GroupMember(db.Model):
    """Group membership"""
    __tablename__ = 'group_members'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(20), default='member')  # admin, member
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    group = db.relationship('Group', back_populates='members')
    user = db.relationship('User', backref='group_memberships')
    
    def to_dict(self):
        return {
            'id': self.id,
            'group_id': self.group_id,
            'user_id': self.user_id,
            'role': self.role,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None
        }


class GroupMessage(db.Model):
    """Messages in groups"""
    __tablename__ = 'group_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(20), default='text')  # text, file, poll, system
    reply_to_id = db.Column(db.Integer, db.ForeignKey('group_messages.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    edited_at = db.Column(db.DateTime)
    
    # Relationships
    group = db.relationship('Group', back_populates='messages')
    sender = db.relationship('User', backref='sent_messages')
    replies = db.relationship('GroupMessage', backref=db.backref('parent', remote_side=[id]))
    
    def to_dict(self):
        return {
            'id': self.id,
            'sender_name': self.sender.name or self.sender.username if self.sender else 'Unknown',
            'sender_id': self.sender_id,
            'content': self.content,
            'message_type': self.message_type,
            'reply_to_id': self.reply_to_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class GroupFile(db.Model):
    """Files shared in groups"""
    __tablename__ = 'group_files'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50))
    cloudinary_url = db.Column(db.String(500), nullable=False)
    cloudinary_public_id = db.Column(db.String(255))
    file_size = db.Column(db.Integer)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    group = db.relationship('Group', back_populates='files')
    uploader = db.relationship('User', backref='uploaded_group_files')
    
    def to_dict(self):
        return {
            'id': self.id,
            'file_name': self.file_name,
            'file_type': self.file_type,
            'cloudinary_url': self.cloudinary_url,
            'file_size': self.file_size,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }


class GroupEvent(db.Model):
    """Events scheduled in groups (lectures, study sessions)"""
    __tablename__ = 'group_events'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50))  # lecture, study_session, hangout, exam_prep
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    livekit_room_id = db.Column(db.String(255))
    is_live = db.Column(db.Boolean, default=False)
    attendee_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    group = db.relationship('Group', back_populates='events')
    creator = db.relationship('User', backref='created_group_events')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'event_type': self.event_type,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'is_live': self.is_live,
            'attendee_count': self.attendee_count
        }


class GroupInvite(db.Model):
    """Invite links for private groups"""
    __tablename__ = 'group_invites'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    invite_token = db.Column(db.String(100), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime)
    max_uses = db.Column(db.Integer)
    current_uses = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    group = db.relationship('Group', backref='invites')
    creator = db.relationship('User', backref='created_invites')
    
    def to_dict(self):
        return {
            'id': self.id,
            'invite_token': self.invite_token,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'current_uses': self.current_uses,
            'max_uses': self.max_uses
        }
