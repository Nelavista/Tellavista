from datetime import datetime
import json
from extensions import db

# ============================================
# Database Models
# ============================================
class User(db.Model):
    """User model for authentication and user management."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    user_level = db.Column(db.Integer, default=1)  # was 'level'
    joined_on = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Nelavista Student Profile fields
    name = db.Column(db.String(100))
    university = db.Column(db.String(150))
    faculty = db.Column(db.String(150))
    department = db.Column(db.String(150))
    level = db.Column(db.String(50))  # academic level

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)


class UserQuestions(db.Model):
    """Model for storing user questions and AI responses (memory system)."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, index=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    memory_layer = db.Column(db.String(50))


class UserProfile(db.Model):
    """Model for storing user preferences and learning styles."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    level = db.Column(db.String(50))
    department = db.Column(db.String(100))
    traits = db.Column(db.Text)  # JSON string
    explanation_style = db.Column(db.String(50))
    focus_areas = db.Column(db.Text)  # JSON string
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
    """Model for live meeting rooms."""
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