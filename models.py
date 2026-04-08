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

    # ── misc ─────────────────────────────────────────────────────────────────
    course_type = db.Column(db.String(20), default='CORE')   # Stores course code like "CSC221", "BIO101"
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
            'course_code': self.course_type,  # Map course_type to course_code for frontend compatibility
            'author': self.author,
            'description': self.description,
            'license': self.license or 'Student Upload',
            'file_url': self.file_url,
            'course_type': self.course_type,
            'views': self.views or 0,
            'downloads': self.downloads or 0,
            'uploaded_by': self.uploaded_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_approved': self.is_approved
        }
