import os
import time
import base64
import uuid
from functools import wraps
from flask import session, redirect, url_for, request
from config import DEBUG_MODE, ALLOWED_EXTENSIONS, ALLOWED_VIDEO_EXTENSIONS

def debug_print(*args, **kwargs):
    if DEBUG_MODE:
        print(*args, **kwargs)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_video_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

def get_session_memory():
    if 'chat_memory' not in session:
        session['chat_memory'] = []
    return session['chat_memory']

def add_to_session_memory(role, content, max_messages=5):
    memory = get_session_memory()
    memory.append({"role": role, "content": content})
    if len(memory) > max_messages * 2:
        memory = memory[-max_messages * 2:]
    session['chat_memory'] = memory

def cleanup_old_files():
    """Remove old uploaded files from session and disk."""
    try:
        current_time = time.time()
        if session.get('last_upload_time') and (current_time - session.get('last_upload_time', 0)) > 3600:
            if session.get('last_file_path'):
                try:
                    if os.path.exists(session['last_file_path']):
                        os.remove(session['last_file_path'])
                        debug_print(f"🗑️ Cleaned up old file: {session['last_file_path']}")
                except Exception as e:
                    debug_print(f"⚠️ Could not delete file: {e}")
            for key in ['last_file_id', 'last_file_type', 'last_file_name', 'last_file_path', 'last_image_base64', 'last_file_preview', 'last_upload_time']:
                session.pop(key, None)
    except Exception as e:
        debug_print(f"⚠️ Cleanup error: {e}")

def check_profile_complete(user):
    """
    Check if user has completed their profile.
    Returns True if profile is complete, False otherwise.
    """
    required_fields = ['name', 'university', 'faculty', 'department', 'level', 'semester']
    for field in required_fields:
        value = getattr(user, field, None)
        if not value or str(value).strip() == '':
            return False
    return True
    
def encode_image_to_base64(file):
    try:
        file.seek(0)
        image_bytes = file.read()
        return base64.b64encode(image_bytes).decode('utf-8')
    except Exception as e:
        debug_print(f"❌ Error encoding image: {e}")
        return None

def is_academic_book(title, topic, department):
    if not title:
        return False
    title_lower = title.lower()
    topic_lower = topic.lower()
    department_lower = department.lower()
    academic_keywords = ["principles", "fundamentals", "introduction", "basics", "theory", "textbook", "manual", "engineering", "mathematics", "analysis", "guide", "mechanics", "accounting", "algebra", "economics", "physics", "statistics", topic_lower, department_lower]
    fiction_keywords = ["novel", "jedi", "star wars", "story", "episode", "adventure", "magic", "wizard", "putting", "love", "mystery", "thriller", "detective", "vampire", "romance", "oz", "dragon", "ghost", "horror"]
    if any(bad in title_lower for bad in fiction_keywords):
        return False
    return any(good in title_lower for good in academic_keywords)
