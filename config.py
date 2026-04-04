import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# Flask Configuration
# ============================================
DEBUG_MODE = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///tellavista.db')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# File upload settings
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv', 'webm', 'flv'}
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_video_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS