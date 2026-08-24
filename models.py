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
    reset_token = db.Column(db.String(200), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    # Which top-level experience the user starts in: 'academia' or 'tech_skills'.
    # NULL means "never chosen" — legacy accounts default to Academia at login time
    # (see routes/auth_routes.py) rather than being forced through path selection.
    preferred_path = db.Column(db.String(20), nullable=True)
    # Sibling flag to is_admin — a third account type (see EmployerProfile) that reuses
    # this same auth system rather than a parallel one.
    is_employer = db.Column(db.Boolean, nullable=False, default=False)
    # Self-reported only. Nelavista has no mechanism to verify a university-issued CGPA —
    # never compute or claim to verify this from Skill GPA / Nelavista activity data.
    # Shown to employers only if the student explicitly opts in (see StudentPrivacySettings).
    academic_cgpa = db.Column(db.Float, nullable=True)
    # Skills profile fields — power the "Profile strength" checklist on the Skills
    # dashboard (see services/skills_service.py's profile_completeness()).
    bio = db.Column(db.Text, nullable=True)
    portfolio_url = db.Column(db.String(300), nullable=True)
    profile_photo_url = db.Column(db.String(500), nullable=True)

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
    is_live = db.Column(db.Boolean, default=False)
    started_at = db.Column(db.DateTime, nullable=True)
    ended_at = db.Column(db.DateTime, nullable=True)


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
    university = db.Column(db.String(150), nullable=True)    # NULL = universal (shown to everyone);
                                                               # set = specific to that school's own
                                                               # curriculum/past-questions (e.g. exact
                                                               # course-code numbering, professor's own
                                                               # exam), not shown to students at a
                                                               # different, explicitly-set university

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

    # ── AI content-retrieval cache ──────────────────────────────────────────
    # Lazily populated the first time a student asks the AI about this specific
    # material (see services/material_service.py::get_or_extract_material_text) --
    # avoids re-downloading/re-parsing the same PDF on every question. Null means
    # "never successfully extracted yet", not "empty file".
    extracted_text = db.Column(db.Text, nullable=True)
    extracted_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'department': self.department,
            'level': self.level,
            'semester': self.semester,
            'university': self.university,
            'course_code': self.course_code,
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
    file_id = db.Column(db.Integer, db.ForeignKey('group_files.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    edited_at = db.Column(db.DateTime)

    # Relationships
    group = db.relationship('Group', back_populates='messages')
    sender = db.relationship('User', backref='sent_messages')
    replies = db.relationship('GroupMessage', backref=db.backref('parent', remote_side=[id]))
    file = db.relationship('GroupFile', foreign_keys=[file_id])
    
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


# ============================================================
# ===== SKILLS SYSTEM =====
# Learn -> Practice -> Build -> Prove -> Progress. Mirrors the existing codebase's
# JSON-as-text convention (see UserProfile.traits/focus_areas above) rather than native
# JSON columns, so every JSON-ish field ships with a `_list`/`_dict` accessor pair.
# ============================================================

class SkillCategory(db.Model):
    """Top-level grouping shown on the Skills catalog, e.g. Tech, Design, Business."""
    __tablename__ = 'skill_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    icon = db.Column(db.String(10))            # a single emoji, rendered directly
    description = db.Column(db.String(300))
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    skills = db.relationship('Skill', backref='category', lazy='dynamic', order_by='Skill.order')

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'slug': self.slug, 'icon': self.icon,
            'description': self.description, 'order': self.order, 'is_active': self.is_active,
        }


class Skill(db.Model):
    """One learnable skill, e.g. Python, UI/UX Design. The unit everything else hangs off:
    its own LearningPath, courses, challenges, and project templates."""
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('skill_categories.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    tagline = db.Column(db.String(200))         # e.g. "Build the foundation you need to start developing real software."
    description = db.Column(db.Text)
    level = db.Column(db.String(20), default='beginner')   # beginner | intermediate | advanced
    icon = db.Column(db.String(10))
    color = db.Column(db.String(20), default='#3b82f6')
    estimated_hours = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    path = db.relationship('LearningPath', backref='skill', uselist=False, cascade='all, delete-orphan')
    courses = db.relationship('SkillCourse', backref='skill', lazy='dynamic', order_by='SkillCourse.order', cascade='all, delete-orphan')
    challenges = db.relationship('Challenge', backref='skill', lazy='dynamic', order_by='Challenge.order', cascade='all, delete-orphan')
    project_templates = db.relationship('ProjectTemplate', backref='skill', lazy='dynamic', order_by='ProjectTemplate.order', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id, 'category_id': self.category_id, 'name': self.name, 'slug': self.slug,
            'tagline': self.tagline, 'description': self.description, 'level': self.level,
            'icon': self.icon, 'color': self.color, 'estimated_hours': self.estimated_hours,
            'is_published': self.is_published, 'order': self.order,
        }


class LearningPath(db.Model):
    """The structured, ordered route through a Skill — what makes Nelavista's Skills
    section a curriculum rather than a pile of courses. One path per skill."""
    __tablename__ = 'learning_paths'

    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), unique=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    steps = db.relationship('LearningPathStep', backref='path', lazy='dynamic', order_by='LearningPathStep.order', cascade='all, delete-orphan')

    def to_dict(self):
        return {'id': self.id, 'skill_id': self.skill_id, 'title': self.title, 'description': self.description}


class LearningPathStep(db.Model):
    """One numbered stage in a LearningPath — a course to complete, a challenge to pass,
    or a project to build. step_type decides which foreign key is populated."""
    __tablename__ = 'learning_path_steps'

    id = db.Column(db.Integer, primary_key=True)
    path_id = db.Column(db.Integer, db.ForeignKey('learning_paths.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    step_type = db.Column(db.String(20), nullable=False, default='course')  # course | challenge | project
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(300))
    course_id = db.Column(db.Integer, db.ForeignKey('skill_courses.id'), nullable=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=True)
    project_template_id = db.Column(db.Integer, db.ForeignKey('project_templates.id'), nullable=True)

    course = db.relationship('SkillCourse')
    challenge = db.relationship('Challenge')
    project_template = db.relationship('ProjectTemplate')

    def to_dict(self):
        return {
            'id': self.id, 'path_id': self.path_id, 'order': self.order, 'step_type': self.step_type,
            'title': self.title, 'description': self.description, 'course_id': self.course_id,
            'challenge_id': self.challenge_id, 'project_template_id': self.project_template_id,
        }


class SkillCourse(db.Model):
    """A course within a skill (named SkillCourse, not Course, to avoid colliding with
    the unrelated 'course' string fields already used by Material/Video)."""
    __tablename__ = 'skill_courses'

    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    level = db.Column(db.String(20), default='beginner')
    estimated_hours = db.Column(db.Integer, default=0)
    order = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # A daily class (e.g. a 30-Day Skill Class) is still a SkillCourse — same modules/
    # lessons — but its lessons are additionally sequenced by day_number/week_number
    # (see Lesson below) and it gets Cohorts, grading, and a final project on top.
    is_daily_class = db.Column(db.Boolean, default=False)
    duration_days = db.Column(db.Integer, nullable=True)

    modules = db.relationship('CourseModule', backref='course', lazy='dynamic', order_by='CourseModule.order', cascade='all, delete-orphan')
    grade_scale = db.relationship('GradeScale', backref='course', lazy='dynamic', order_by='GradeScale.order', cascade='all, delete-orphan')
    grade_weights = db.relationship('GradeWeight', backref='course', lazy='dynamic', cascade='all, delete-orphan')
    cohorts = db.relationship('Cohort', backref='course', lazy='dynamic', order_by='Cohort.created_at.desc()', cascade='all, delete-orphan')

    __table_args__ = (db.UniqueConstraint('skill_id', 'slug', name='uq_skill_course_slug'),)

    def to_dict(self):
        return {
            'id': self.id, 'skill_id': self.skill_id, 'title': self.title, 'slug': self.slug,
            'description': self.description, 'level': self.level, 'estimated_hours': self.estimated_hours,
            'order': self.order, 'is_published': self.is_published,
            'is_daily_class': self.is_daily_class, 'duration_days': self.duration_days,
        }


class CourseModule(db.Model):
    """A group of lessons within a SkillCourse."""
    __tablename__ = 'course_modules'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('skill_courses.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    order = db.Column(db.Integer, default=0)

    lessons = db.relationship('Lesson', backref='module', lazy='dynamic', order_by='Lesson.order', cascade='all, delete-orphan')

    def to_dict(self):
        return {'id': self.id, 'course_id': self.course_id, 'title': self.title, 'order': self.order}


class Lesson(db.Model):
    """One unit of learning content: written lesson body, optional video, optional
    downloadable/linked resources, optional quiz (see Quiz)."""
    __tablename__ = 'lessons'

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('course_modules.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), nullable=False)
    order = db.Column(db.Integer, default=0)
    content = db.Column(db.Text)              # lesson body, simple markdown-ish text
    video_url = db.Column(db.String(500))     # admin-set embeddable URL, optional, takes priority
    duration_minutes = db.Column(db.Integer, default=10)
    resources_json = db.Column(db.Text)       # JSON list of {"label": "...", "url": "..."}
    # Auto-fetched YouTube results (see services/youtube_service.py), cached so the API is
    # called once per lesson rather than on every student's every view. NULL = never
    # fetched yet; "[]" = fetched and genuinely found nothing — that distinction is what
    # the `videos` property below preserves (None vs an empty list).
    videos_json = db.Column(db.Text)
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Populated only when this lesson belongs to a daily class (course.is_daily_class) —
    # NULL for ordinary courses. day_number is the sequence a student must follow
    # (Day 1 -> Day 2 -> ...); week_number/week_title group days for display only.
    day_number = db.Column(db.Integer, nullable=True)
    week_number = db.Column(db.Integer, nullable=True)
    week_title = db.Column(db.String(150), nullable=True)
    learning_objective = db.Column(db.String(300), nullable=True)

    quiz = db.relationship('Quiz', backref='lesson', uselist=False, cascade='all, delete-orphan')
    assignment = db.relationship('Assignment', backref='lesson', uselist=False, cascade='all, delete-orphan')

    @property
    def resources(self):
        try:
            return json.loads(self.resources_json) if self.resources_json else []
        except (ValueError, TypeError):
            return []

    @resources.setter
    def resources(self, value):
        self.resources_json = json.dumps(value or [])

    @property
    def videos(self):
        """None means 'never fetched'; [] means 'fetched, found nothing'."""
        if self.videos_json is None:
            return None
        try:
            return json.loads(self.videos_json)
        except (ValueError, TypeError):
            return None

    @videos.setter
    def videos(self, value):
        self.videos_json = json.dumps(value if value is not None else [])

    def to_dict(self):
        return {
            'id': self.id, 'module_id': self.module_id, 'title': self.title, 'slug': self.slug,
            'order': self.order, 'content': self.content, 'video_url': self.video_url,
            'duration_minutes': self.duration_minutes, 'resources': self.resources,
            'videos': self.videos,
            'is_published': self.is_published, 'has_quiz': self.quiz is not None,
            'day_number': self.day_number, 'week_number': self.week_number,
            'week_title': self.week_title, 'learning_objective': self.learning_objective,
            'has_assignment': self.assignment is not None,
        }


class Quiz(db.Model):
    """A short check-for-understanding attached to one Lesson. Questions are stored as a
    JSON blob (admin-authored) rather than a separate QuizQuestion table — a quiz never
    needs to be queried question-by-question, only rendered/graded as a whole."""
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), unique=True, nullable=False)
    title = db.Column(db.String(150), default='Check your understanding')
    questions_json = db.Column(db.Text)  # [{"question","options":[...],"correct_index","explanation"}]

    @property
    def questions(self):
        try:
            return json.loads(self.questions_json) if self.questions_json else []
        except (ValueError, TypeError):
            return []

    @questions.setter
    def questions(self, value):
        self.questions_json = json.dumps(value or [])

    def to_dict(self, include_answers=True):
        qs = self.questions
        if not include_answers:
            qs = [{k: v for k, v in q.items() if k not in ('correct_index', 'explanation')} for q in qs]
        return {'id': self.id, 'lesson_id': self.lesson_id, 'title': self.title, 'questions': qs}


class Challenge(db.Model):
    """A practical exercise for a skill — coding, design, business, or content — kept
    separate from Lesson so 'practice' is a first-class layer, not another video."""
    __tablename__ = 'challenges'

    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(300))
    challenge_type = db.Column(db.String(20), default='coding')  # coding | design | business | content | general
    difficulty = db.Column(db.String(20), default='beginner')
    instructions = db.Column(db.Text)
    estimated_minutes = db.Column(db.Integer, default=30)
    is_published = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('skill_id', 'slug', name='uq_challenge_slug'),)

    def to_dict(self):
        return {
            'id': self.id, 'skill_id': self.skill_id, 'title': self.title, 'slug': self.slug,
            'description': self.description, 'challenge_type': self.challenge_type,
            'difficulty': self.difficulty, 'instructions': self.instructions,
            'estimated_minutes': self.estimated_minutes, 'is_published': self.is_published, 'order': self.order,
        }


class ChallengeSubmission(db.Model):
    """A student's attempt at a Challenge — their write-up/solution, kept so 'practice'
    produces a real, reviewable artifact rather than a silent checkbox. feedback_json holds
    AI-generated feedback (strengths/improvements/explanation/score/next step) — 'Correct ✓'
    is not useful feedback on its own, so this is what a student actually sees after
    submitting. NULL feedback_json means feedback generation hasn't run or failed; the
    submission itself still stands either way."""
    __tablename__ = 'challenge_submissions'

    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='submitted')  # submitted | reviewed
    feedback_json = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    challenge = db.relationship('Challenge', backref='submissions')
    student = db.relationship('User', backref='challenge_submissions')

    @property
    def feedback(self):
        if not self.feedback_json:
            return None
        try:
            return json.loads(self.feedback_json)
        except (ValueError, TypeError):
            return None

    @feedback.setter
    def feedback(self, value):
        self.feedback_json = json.dumps(value) if value is not None else None

    def to_dict(self):
        return {
            'id': self.id, 'challenge_id': self.challenge_id, 'status': self.status,
            'feedback': self.feedback,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class ProjectTemplate(db.Model):
    """An admin-curated project brief tied to a skill (e.g. 'Student Marketplace' for
    Web Development) that students can start as their own StudentProject."""
    __tablename__ = 'project_templates'

    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    # Set only when this is the final project for a specific daily class (course_id +
    # is_final_project=True) rather than a general skill-level project brief. A daily
    # class's final project is evaluated by AI strictly against rubric_json — see
    # services/ai_service.py's evaluate_final_project and StudentProject.rubric_scores below.
    course_id = db.Column(db.Integer, db.ForeignKey('skill_courses.id'), nullable=True)
    is_final_project = db.Column(db.Boolean, default=False)
    course = db.relationship('SkillCourse', backref='final_project_templates')
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    skills_demonstrated_json = db.Column(db.Text)  # JSON list of tag strings, e.g. ["HTML","CSS","Git"]
    difficulty = db.Column(db.String(20), default='beginner')
    estimated_hours = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Admin-configurable weighted evaluation criteria: [{"name": str, "max_points": int}, ...]
    # where max_points across all criteria should sum to 100. The AI evaluator is given
    # exactly these criteria and must score against them — it never invents its own scale.
    rubric_json = db.Column(db.Text)

    __table_args__ = (db.UniqueConstraint('skill_id', 'slug', name='uq_project_template_slug'),)

    @property
    def skills_demonstrated(self):
        try:
            return json.loads(self.skills_demonstrated_json) if self.skills_demonstrated_json else []
        except (ValueError, TypeError):
            return []

    @skills_demonstrated.setter
    def skills_demonstrated(self, value):
        self.skills_demonstrated_json = json.dumps(value or [])

    @property
    def rubric(self):
        try:
            return json.loads(self.rubric_json) if self.rubric_json else []
        except (ValueError, TypeError):
            return []

    @rubric.setter
    def rubric(self, value):
        self.rubric_json = json.dumps(value or [])

    def to_dict(self):
        return {
            'id': self.id, 'skill_id': self.skill_id, 'course_id': self.course_id,
            'is_final_project': self.is_final_project,
            'title': self.title, 'slug': self.slug,
            'description': self.description, 'skills_demonstrated': self.skills_demonstrated,
            'difficulty': self.difficulty, 'estimated_hours': self.estimated_hours,
            'is_published': self.is_published, 'order': self.order, 'rubric': self.rubric,
        }


class StudentProject(db.Model):
    """A student's own instance of building something — started from a ProjectTemplate,
    or (in future) from their own idea. This is the tangible proof-of-work layer."""
    __tablename__ = 'student_projects'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_template_id = db.Column(db.Integer, db.ForeignKey('project_templates.id'), nullable=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='in_progress')  # in_progress | submitted | completed
    progress_pct = db.Column(db.Integer, default=0)
    repo_url = db.Column(db.String(500))
    live_url = db.Column(db.String(500))
    skills_demonstrated_json = db.Column(db.Text)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    # AI evaluation against the template's rubric (see ProjectTemplate.rubric), populated
    # when a final-project submission is evaluated. rubric_scores is a list parallel to
    # the rubric's criteria: [{"name","max_points","score","comment"}, ...] — ai_overall_score
    # is always the sum of those per-criterion scores, never a separately invented number.
    rubric_scores_json = db.Column(db.Text)
    ai_overall_score = db.Column(db.Integer, nullable=True)

    student = db.relationship('User', backref='student_projects')
    template = db.relationship('ProjectTemplate', backref='student_instances')

    @property
    def skills_demonstrated(self):
        try:
            return json.loads(self.skills_demonstrated_json) if self.skills_demonstrated_json else []
        except (ValueError, TypeError):
            return []

    @skills_demonstrated.setter
    def skills_demonstrated(self, value):
        self.skills_demonstrated_json = json.dumps(value or [])

    @property
    def rubric_scores(self):
        try:
            return json.loads(self.rubric_scores_json) if self.rubric_scores_json else None
        except (ValueError, TypeError):
            return None

    @rubric_scores.setter
    def rubric_scores(self, value):
        self.rubric_scores_json = json.dumps(value) if value is not None else None

    def to_dict(self):
        return {
            'id': self.id, 'title': self.title, 'description': self.description, 'status': self.status,
            'progress_pct': self.progress_pct, 'repo_url': self.repo_url, 'live_url': self.live_url,
            'skills_demonstrated': self.skills_demonstrated,
            'skill_name': (self.template.skill.name if self.template and self.template.skill else None)
                          or (self.skills_demonstrated[0] if self.skills_demonstrated else None),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'rubric_scores': self.rubric_scores, 'ai_overall_score': self.ai_overall_score,
        }


class StudentSkill(db.Model):
    """Aggregate per-student-per-skill progress — the row that powers the skill profile
    bars and the dashboard's 'Continue learning'. Recomputed (not incrementally patched)
    whenever a lesson/challenge/project changes, so it can never drift out of sync."""
    __tablename__ = 'student_skills'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    status = db.Column(db.String(20), default='in_progress')  # in_progress | completed
    progress_pct = db.Column(db.Integer, default=0)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    student = db.relationship('User', backref='student_skills')
    skill = db.relationship('Skill', backref='student_progress')

    __table_args__ = (db.UniqueConstraint('student_id', 'skill_id', name='uq_student_skill'),)

    def to_dict(self):
        return {
            'skill_id': self.skill_id, 'skill_name': self.skill.name if self.skill else None,
            'status': self.status, 'progress_pct': self.progress_pct,
            'last_activity_at': self.last_activity_at.isoformat() if self.last_activity_at else None,
        }


class StudentLessonProgress(db.Model):
    """One student's completion of one lesson — the atomic unit every higher-level
    progress number (course %, path step state, skill %) is computed from."""
    __tablename__ = 'student_lesson_progress'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('User', backref='lesson_progress')
    lesson = db.relationship('Lesson', backref='completions')

    __table_args__ = (db.UniqueConstraint('student_id', 'lesson_id', name='uq_student_lesson'),)


class StudentQuizAttempt(db.Model):
    """A student's answers + score for one Quiz. Kept even after the lesson is complete
    so 'review your answers' and skill-profile credibility both stay possible."""
    __tablename__ = 'student_quiz_attempts'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    answers_json = db.Column(db.Text)  # JSON list of selected option indices, parallel to quiz.questions
    score = db.Column(db.Integer)      # 0-100
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('User', backref='quiz_attempts')
    quiz = db.relationship('Quiz', backref='attempts')

    @property
    def answers(self):
        try:
            return json.loads(self.answers_json) if self.answers_json else []
        except (ValueError, TypeError):
            return []

    @answers.setter
    def answers(self, value):
        self.answers_json = json.dumps(value or [])


class StudentOnboarding(db.Model):
    """What a student told us they want on their first visit to Skills — captured once so
    the experience can open focused on what they actually asked for, instead of a generic
    catalog. interest_text is always kept (even when it matched a skill) so admins can see
    the student's own words; interested_skill_id is set only when it resolved to a real,
    published skill in the catalog."""
    __tablename__ = 'student_onboarding'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    interest_text = db.Column(db.String(200), nullable=False)
    interested_skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=True)
    experience_level = db.Column(db.String(20), nullable=False)  # new | some_basics | experienced
    goal = db.Column(db.String(30))  # get_a_job | build_projects | exploring | start_a_business
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('User', backref=db.backref('skills_onboarding', uselist=False))
    interested_skill = db.relationship('Skill')

    def to_dict(self):
        return {
            'id': self.id, 'interest_text': self.interest_text,
            'interested_skill_id': self.interested_skill_id,
            'interested_skill_name': self.interested_skill.name if self.interested_skill else None,
            'experience_level': self.experience_level, 'goal': self.goal,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class CareerTrack(db.Model):
    """A multi-skill career track (e.g. 'AI Engineer', 'Web Developer') that sequences
    several whole Skills together. Distinct from LearningPath, which only sequences one
    skill's own courses/challenges/projects — a CareerTrack is the layer above that,
    telling a student which skills to learn in what order to get somewhere specific."""
    __tablename__ = 'career_tracks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    tagline = db.Column(db.String(200))
    description = db.Column(db.Text)
    icon = db.Column(db.String(10))
    color = db.Column(db.String(20), default='#3b82f6')
    is_published = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    steps = db.relationship('CareerTrackStep', backref='track', lazy='dynamic',
                             order_by='CareerTrackStep.order', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id, 'title': self.title, 'slug': self.slug, 'tagline': self.tagline,
            'description': self.description, 'icon': self.icon, 'color': self.color,
            'is_published': self.is_published, 'order': self.order,
            'step_count': self.steps.count(),
        }


class CareerTrackStep(db.Model):
    """One skill within a CareerTrack, in sequence. A step's 'completion' is derived from
    the student's StudentSkill row for skill_id — no separate progress table, same
    recompute-don't-cache principle used everywhere else in the Skills system."""
    __tablename__ = 'career_track_steps'

    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey('career_tracks.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    note = db.Column(db.String(200))  # optional context, e.g. "just the math you'll actually use"

    skill = db.relationship('Skill')

    def to_dict(self):
        return {
            'id': self.id, 'track_id': self.track_id, 'skill_id': self.skill_id,
            'skill_name': self.skill.name if self.skill else None, 'order': self.order,
            'note': self.note,
        }


# ============================================================
# ===== 30-DAY SKILL CLASSES: assignments, grading, cohorts, projects =====
# Layered on top of the Skills system above rather than duplicating it: a "30-Day Skill
# Class" is a SkillCourse with is_daily_class=True, whose Lesson rows carry day_number/
# week_number. Everything below (Assignment, grading, Cohort) hangs off that same course.
# ============================================================

class Assignment(db.Model):
    """A graded, per-day deliverable — distinct from Challenge (ungraded, open-ended
    practice with AI feedback but no score/weight) and from Quiz (auto-graded, not
    submission-reviewed). One assignment per daily-class Lesson."""
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), unique=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    instructions = db.Column(db.Text)
    due_offset_hours = db.Column(db.Integer, default=48)  # hours after the day unlocks before it counts "late"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    submissions = db.relationship('AssignmentSubmission', backref='assignment', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id, 'lesson_id': self.lesson_id, 'title': self.title,
            'instructions': self.instructions, 'due_offset_hours': self.due_offset_hours,
        }


class AssignmentSubmission(db.Model):
    """A student's graded submission for one Assignment. status distinguishes on-time vs
    late (set at submit time, from the enrollment's day-unlock timestamp) from the AI's
    qualitative read of the work (passed / needs_improvement) — two different questions
    ('was it on time' and 'was it good'), both needed for Skill GPA and ranking to resist
    gaming. One student may resubmit; only the latest submission counts toward grading
    (enforced in services/gpa_service.py), so duplicate submissions can't be used to farm
    attempts — the ORIGINAL submitted_at is what decides on-time/late, not the latest."""
    __tablename__ = 'assignment_submissions'

    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='submitted')  # submitted | late
    review_status = db.Column(db.String(20), default='pending')  # pending | passed | needs_improvement
    score = db.Column(db.Integer, nullable=True)  # 0-100, from AI feedback
    feedback_json = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    first_submitted_at = db.Column(db.DateTime, default=datetime.utcnow)  # never overwritten by resubmits

    student = db.relationship('User', backref='assignment_submissions')

    @property
    def feedback(self):
        if not self.feedback_json:
            return None
        try:
            return json.loads(self.feedback_json)
        except (ValueError, TypeError):
            return None

    @feedback.setter
    def feedback(self, value):
        self.feedback_json = json.dumps(value) if value is not None else None

    def to_dict(self):
        return {
            'id': self.id, 'assignment_id': self.assignment_id, 'status': self.status,
            'review_status': self.review_status, 'score': self.score, 'feedback': self.feedback,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
        }


class GradeScale(db.Model):
    """Admin-configurable letter-grade -> grade-point mapping, scoped per course (not
    global) so different classes can use different scales. Powers Skill GPA — never
    hardcoded, and explicitly modeled on university CGPA mechanics but kept namespaced
    as 'Skill GPA', never presented as academic CGPA (see User.academic_cgpa)."""
    __tablename__ = 'grade_scales'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('skill_courses.id'), nullable=False)
    grade_letter = db.Column(db.String(5), nullable=False)   # e.g. "A", "B+"
    min_score = db.Column(db.Integer, nullable=False)        # inclusive, 0-100
    max_score = db.Column(db.Integer, nullable=False)        # inclusive, 0-100
    grade_point = db.Column(db.Float, nullable=False)        # e.g. 5.0, 4.0 ... 0.0
    order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id, 'course_id': self.course_id, 'grade_letter': self.grade_letter,
            'min_score': self.min_score, 'max_score': self.max_score,
            'grade_point': self.grade_point, 'order': self.order,
        }


class GradeWeight(db.Model):
    """Admin-configurable weight (as a % of Skill GPA) for one grading component of a
    course. component weights for a course should sum to 100 — enforced by the admin API,
    not the DB, so a partially-configured course (mid-edit) is never blocked from saving."""
    __tablename__ = 'grade_weights'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('skill_courses.id'), nullable=False)
    component = db.Column(db.String(30), nullable=False)  # assignments | tests | final_project | participation
    weight_pct = db.Column(db.Integer, nullable=False, default=0)

    __table_args__ = (db.UniqueConstraint('course_id', 'component', name='uq_course_grade_component'),)

    def to_dict(self):
        return {'id': self.id, 'course_id': self.course_id, 'component': self.component, 'weight_pct': self.weight_pct}


class Cohort(db.Model):
    """A time-boxed intake of a daily class, e.g. 'August 2026 Cohort'. Exists so ranking
    is always relative to peers who started together, not the whole all-time student
    body — comparing a Day 3 student against a Day 28 student would be meaningless."""
    __tablename__ = 'cohorts'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('skill_courses.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    is_active = db.Column(db.Boolean, default=True)  # accepting new enrollments
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    enrollments = db.relationship('CohortEnrollment', backref='cohort', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id, 'course_id': self.course_id, 'name': self.name,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_active': self.is_active, 'student_count': self.enrollments.count(),
        }


class CohortEnrollment(db.Model):
    """One student's membership in one Cohort of one daily class. skill_gpa is a cache —
    recomputed (see services/gpa_service.py) after any grading event, never hand-edited —
    kept here (rather than computed live on every page view) only because it's also the
    sort key for the cohort leaderboard and recomputing 300 students' GPAs on every
    leaderboard view would be wasteful; every individual student's own transcript view
    still recomputes on the fly to guarantee it's never stale for the one person looking."""
    __tablename__ = 'cohort_enrollments'

    id = db.Column(db.Integer, primary_key=True)
    cohort_id = db.Column(db.Integer, db.ForeignKey('cohorts.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    current_day = db.Column(db.Integer, default=1)
    skill_gpa = db.Column(db.Float, nullable=True)
    gpa_updated_at = db.Column(db.DateTime, nullable=True)

    student = db.relationship('User', backref='cohort_enrollments')

    __table_args__ = (db.UniqueConstraint('cohort_id', 'student_id', name='uq_cohort_student'),)

    def to_dict(self):
        return {
            'id': self.id, 'cohort_id': self.cohort_id, 'student_id': self.student_id,
            'current_day': self.current_day, 'skill_gpa': self.skill_gpa,
            'enrolled_at': self.enrolled_at.isoformat() if self.enrolled_at else None,
        }


class EmployerProfile(db.Model):
    """The employer-side counterpart to a User row — reuses the exact same auth (User.
    is_employer flag, same login/session), not a parallel account system. is_verified is
    manually toggled by an admin (see routes/admin_skills_routes.py); no automated
    verification mechanism exists, so 'verified' means an admin actually checked."""
    __tablename__ = 'employer_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    company_name = db.Column(db.String(150), nullable=False)
    company_description = db.Column(db.Text)
    website = db.Column(db.String(300))
    industry = db.Column(db.String(120))
    logo_url = db.Column(db.String(500))
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('employer_profile', uselist=False))

    def to_dict(self):
        return {
            'id': self.id, 'user_id': self.user_id, 'company_name': self.company_name,
            'company_description': self.company_description, 'website': self.website,
            'industry': self.industry, 'logo_url': self.logo_url, 'is_verified': self.is_verified,
        }


class StudentPrivacySettings(db.Model):
    """What a student has opted to let employers see. Defaults are deliberately closed
    (profile_visibility defaults to 'private') — a student must actively opt in before
    employer discovery surfaces them at all; the per-field toggles then narrow further
    what's visible even once discoverable. No row means the same as profile_visibility=
    'private' (the safe default), so employer queries treat a missing row as fully hidden."""
    __tablename__ = 'student_privacy_settings'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    # private: invisible to employer discovery entirely.
    # employers: discoverable by employers, not shown on any public page.
    # public: discoverable and shown to anyone with the profile link.
    profile_visibility = db.Column(db.String(20), nullable=False, default='private')
    show_academic_cgpa = db.Column(db.Boolean, default=False)
    show_projects = db.Column(db.Boolean, default=True)
    show_skill_transcript = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = db.relationship('User', backref=db.backref('privacy_settings', uselist=False))

    def to_dict(self):
        return {
            'profile_visibility': self.profile_visibility,
            'show_academic_cgpa': self.show_academic_cgpa,
            'show_projects': self.show_projects,
            'show_skill_transcript': self.show_skill_transcript,
        }


# ============================================================
# ===== ACADEMIA TAXONOMY: University -> Faculty -> Department -> Course =====
# Normalizes what User.university/faculty/department/level (free strings, kept as-is
# for backward compat -- see services/academic_context.py for the resolver bridging
# the two) actually refer to. Seeded ONLY from Nelavista_Course_Codes.csv (real
# curriculum data for LASU/UNILAG/UI) via seed_academia.py. Do not hand-add fake
# departments/courses here -- if a school/department isn't covered, it stays
# unresolved (see resolver) rather than getting invented rows.
# ============================================================

class University(db.Model):
    __tablename__ = 'universities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)  # exact match to the
    # <option value="..."> strings in profile_completion_modal.html / profile.html's
    # university <select>, e.g. "Lagos State University"
    short_name = db.Column(db.String(20))  # "LASU", "UNILAG", "UI" -- display only
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    faculties = db.relationship('Faculty', backref='university', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'short_name': self.short_name}


class Faculty(db.Model):
    """Scoped per-university, not shared across schools -- a faculty's department
    composition isn't verified to be identical at every institution."""
    __tablename__ = 'faculties'

    id = db.Column(db.Integer, primary_key=True)
    university_id = db.Column(db.Integer, db.ForeignKey('universities.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)  # e.g. "Science", "Management Sciences",
    # or "General Studies" for university-wide GST/GES courses that don't belong to
    # one real faculty (see seed_academia.py)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    departments = db.relationship('Department', backref='faculty', lazy='dynamic', cascade='all, delete-orphan')

    __table_args__ = (db.UniqueConstraint('university_id', 'name', name='uq_faculty_university_name'),)

    def to_dict(self):
        return {'id': self.id, 'university_id': self.university_id, 'name': self.name}


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)  # exact match to the department strings
    # in static/js/faculty-departments.js / User.department -- resolver.py relies on
    # case-insensitive exact matching against this
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    courses = db.relationship('Course', backref='department', lazy='dynamic', cascade='all, delete-orphan')

    __table_args__ = (db.UniqueConstraint('faculty_id', 'name', name='uq_department_faculty_name'),)

    def to_dict(self):
        return {'id': self.id, 'faculty_id': self.faculty_id, 'name': self.name}


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    code = db.Column(db.String(20), nullable=False, index=True)   # "MAT101" -- matches
    # Material.course_code / CBT's subject-code-prefixed keys exactly
    title = db.Column(db.String(200), nullable=False)             # from the curriculum source
    level = db.Column(db.String(10), nullable=False)              # "100".."400", matches User.level
    # The CSV source has no semester or course_type column -- these stay null until an
    # admin sets them (see routes/admin_academia_routes.py). Never invented at seed time.
    semester = db.Column(db.String(20), nullable=True)
    course_type = db.Column(db.String(20), nullable=True)         # "CORE" / "ELECTIVE", admin-set only
    # Course overview/outline text -- also admin-set only, stays null (no "Overview"
    # section rendered) rather than ever being auto-filled with invented content.
    description = db.Column(db.Text, nullable=True)
    # Where this row's code/title actually came from -- lets students and admins tell a
    # department's own registrar-verified numbering (e.g. LASU's CSV, source=NULL) apart from
    # the NUC-mandated national core curriculum (CCMAS) used as an honest starting point for
    # schools with no school-specific catalog yet (see seed_ccmas_core.py). CCMAS defines the
    # compulsory floor every accredited Nigerian programme must teach, but a school may use
    # different local numbering or add its own electives on top of it -- 'nuc_ccmas_core' is
    # not a claim that this is that exact school's own published course list.
    source = db.Column(db.String(30), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('department_id', 'level', 'code', name='uq_course_dept_level_code'),)

    def to_dict(self):
        return {
            'id': self.id, 'department_id': self.department_id, 'code': self.code,
            'title': self.title, 'level': self.level, 'semester': self.semester,
            'course_type': self.course_type, 'description': self.description, 'source': self.source,
        }


# ============================================================
# ===== CBT PERSISTENCE: question bank + graded attempts =====
# CBTQuestion is seeded from templates/CBT.html's generateFullQuestionBank() (hand-
# authored, verified-accurate practice questions) via seed_cbt_questions.py -- no new
# question content is invented here. Grain is subject_code (e.g. "MTH", "CSC"),
# matching the JS bank's own design: a subject prefix with no entry deliberately has
# no questions, never a silent substitution from a different subject. CBTAttempt links
# to a free-string course_code (not a Course FK) so a student can still practice and
# have it persisted even for a course/university the taxonomy above doesn't cover yet.
# ============================================================

class CBTQuestion(db.Model):
    __tablename__ = 'cbt_questions'

    id = db.Column(db.Integer, primary_key=True)
    subject_code = db.Column(db.String(10), nullable=False, index=True)  # "MTH", "CSC", ...
    question_type = db.Column(db.String(10), nullable=False, default='cbt')  # 'cbt' | 'written'
    question_text = db.Column(db.Text, nullable=False)
    # MCQ-only fields (question_type='cbt'); left null for 'written'
    options_json = db.Column(db.Text)
    correct_index = db.Column(db.Integer)
    explanation = db.Column(db.Text)
    # Written-only field (question_type='written'); left null for 'cbt'
    mark_scheme = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def options(self):
        try:
            return json.loads(self.options_json) if self.options_json else []
        except (ValueError, TypeError):
            return []

    @options.setter
    def options(self, value):
        self.options_json = json.dumps(value or [])

    def to_dict(self, include_answer=False):
        d = {
            'id': self.id, 'subject_code': self.subject_code, 'question_type': self.question_type,
            'question_text': self.question_text, 'options': self.options,
        }
        if include_answer:
            d['correct_index'] = self.correct_index
            d['explanation'] = self.explanation
            d['mark_scheme'] = self.mark_scheme
        return d


class CBTAttempt(db.Model):
    __tablename__ = 'cbt_attempts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_code = db.Column(db.String(20), nullable=False, index=True)  # free string, not a
    # Course FK -- a student can practice a subject the taxonomy doesn't cover yet
    # (e.g. a non-seeded university); forcing a FK would break CBT for exactly those students
    question_type = db.Column(db.String(10), nullable=False)  # 'cbt' | 'written'
    total_questions = db.Column(db.Integer, nullable=False)
    correct_count = db.Column(db.Integer, nullable=False, default=0)
    score_pct = db.Column(db.Integer, nullable=False, default=0)
    duration_seconds = db.Column(db.Integer)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    submitted_at = db.Column(db.DateTime)

    user = db.relationship('User', backref=db.backref('cbt_attempts', lazy='dynamic'))
    answers = db.relationship('CBTAnswer', backref='attempt', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id, 'course_code': self.course_code, 'question_type': self.question_type,
            'total_questions': self.total_questions, 'correct_count': self.correct_count,
            'score_pct': self.score_pct, 'duration_seconds': self.duration_seconds,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
        }


class CBTAnswer(db.Model):
    """One question's answer within one CBTAttempt -- snapshotted at submit time so a
    later edit/removal of the source CBTQuestion never changes what a review screen
    shows for a past attempt."""
    __tablename__ = 'cbt_answers'

    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('cbt_attempts.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('cbt_questions.id'), nullable=True)
    question_text = db.Column(db.Text, nullable=False)
    selected_index = db.Column(db.Integer, nullable=True)   # MCQ only, null = skipped
    written_answer = db.Column(db.Text, nullable=True)      # written only
    is_correct = db.Column(db.Boolean, nullable=True)       # null for unmarked written answers

    question = db.relationship('CBTQuestion')

    def to_dict(self):
        return {
            'id': self.id, 'question_text': self.question_text,
            'selected_index': self.selected_index, 'written_answer': self.written_answer,
            'is_correct': self.is_correct,
        }


# ============================================================
# ===== MATERIAL VIEW TRACKING =====
# Real per-student "viewed this material" events -- powers Continue Studying, Recent
# Materials, and a materials-viewed progress count on the dashboard/course page. Not a
# page-view analytics log: one row per (user, material) pair, timestamp bumped on
# repeat views, so it reflects genuine distinct materials studied, not refresh-spam.
# ============================================================

class MaterialView(db.Model):
    __tablename__ = 'material_views'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('material_views', lazy='dynamic'))
    material = db.relationship('Material')

    __table_args__ = (db.UniqueConstraint('user_id', 'material_id', name='uq_material_view_user_material'),)


# ============================================================
# ===== OPPORTUNITIES: the "Earn" phase of Learn -> Practice -> Build -> Verify -> Earn =====
# Real, paid gigs tied to a skill. Admin-curated for now (not an open employer-posting
# marketplace) — a student applies, an admin moves the application through
# accepted -> completed -> paid. Earnings on the student dashboard are always summed
# live from OpportunityApplication rows, never a separately-tracked balance that could
# drift out of sync with what was actually paid.
# ============================================================

class Opportunity(db.Model):
    """A real, paid gig matched to one skill."""
    __tablename__ = 'opportunities'

    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(50), default='Remote')  # Remote | On-site
    payment_amount = db.Column(db.Integer, nullable=False, default=0)  # whole naira
    currency = db.Column(db.String(10), default='NGN')
    due_date = db.Column(db.Date, nullable=True)
    is_published = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    skill = db.relationship('Skill', backref='opportunities')
    applications = db.relationship('OpportunityApplication', backref='opportunity', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id, 'skill_id': self.skill_id, 'skill_name': self.skill.name if self.skill else None,
            'title': self.title, 'description': self.description, 'location': self.location,
            'payment_amount': self.payment_amount, 'currency': self.currency,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'is_published': self.is_published, 'order': self.order,
        }


class OpportunityApplication(db.Model):
    """A student's application to one Opportunity, tracked through to payment — this is
    what makes Earnings a real, derived number instead of a static UI element."""
    __tablename__ = 'opportunity_applications'

    id = db.Column(db.Integer, primary_key=True)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='applied')  # applied | accepted | completed | paid | rejected
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    paid_at = db.Column(db.DateTime, nullable=True)
    payout_amount = db.Column(db.Integer, nullable=True)  # set once paid; may differ from the listed amount

    student = db.relationship('User', backref='opportunity_applications')

    __table_args__ = (db.UniqueConstraint('opportunity_id', 'student_id', name='uq_opportunity_student'),)

    def to_dict(self):
        return {
            'id': self.id, 'opportunity_id': self.opportunity_id, 'status': self.status,
            'applied_at': self.applied_at.isoformat() if self.applied_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None,
            'payout_amount': self.payout_amount,
        }