import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# Flask Configuration
# ============================================
DEBUG_MODE = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    if DEBUG_MODE:
        SECRET_KEY = 'dev-secret-key-change-in-production'
    else:
        raise RuntimeError(
            'SECRET_KEY environment variable is not set. Refusing to start with a '
            'default/guessable key outside of debug mode — set SECRET_KEY in the '
            'environment (e.g. `python -c "import secrets; print(secrets.token_hex(32))"`).'
        )

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///tellavista.db')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
AGORA_APP_ID = os.getenv('AGORA_APP_ID')

# Session cookie hardening — SESSION_COOKIE_SECURE requires HTTPS, so it's opt-in via env
# for local HTTP development and forced on by default otherwise (real deploys are HTTPS).
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False' if DEBUG_MODE else 'True').lower() == 'true'
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_HTTPONLY = True
PERMANENT_SESSION_LIFETIME_DAYS = int(os.getenv('PERMANENT_SESSION_LIFETIME_DAYS', '7'))

# File upload settings
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv', 'webm', 'flv'}
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_video_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS