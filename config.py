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
# Optional second YouTube Data API project's key -- YouTube's search.list quota (100
# queries/day on the default tier) is per-project, not per-application, so a second real
# Google Cloud project (its own key, same app) gets its own separate 100/day allowance.
# search_youtube_videos() below tries this only after YOUTUBE_API_KEY is exhausted for
# the day; unset (the common case) is a complete no-op, same single-key behavior as before.
YOUTUBE_API_KEY_2 = os.getenv('YOUTUBE_API_KEY_2')
AGORA_APP_ID = os.getenv('AGORA_APP_ID')
# Optional -- raises GitHub's public REST API rate limit from 60/hr to 5000/hr, shared
# across every student's project review on this deploy (see services/link_fetch_service.py's
# fetch_github_summary). Same "unset = graceful no-op" pattern as YOUTUBE_API_KEY_2; a
# fine-grained token with no scopes (read-only access to public repos only) is enough.
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# "Sign in with Google" -- both must be set (from the Google Cloud Console OAuth client)
# for the feature to activate. Left unset, the Google button simply doesn't render and
# the /auth/google routes redirect back with a flash error instead of crashing -- see
# routes/auth_routes.py.
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_OAUTH_ENABLED = bool(GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET)

# Explicit environment marker -- distinct from DEBUG_MODE, which controls Flask/Werkzeug
# debug behavior. This controls things (like the database fallback below and the
# Socket.IO CORS allow-list) that must never silently relax just because DEBUG happens
# to be off; ENVIRONMENT defaults to 'production' unless explicitly told otherwise, so a
# misconfigured deploy fails loudly/safely rather than quietly behaving like local dev.
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development' if DEBUG_MODE else 'production').lower()
IS_PRODUCTION = ENVIRONMENT == 'production'

# Redis backs two things when configured: Socket.IO's cross-worker message queue (so
# live classes/chat work correctly with more than one gunicorn worker or dyno) and
# Flask-Limiter's rate-limit storage (so limits are shared across workers instead of
# each worker enforcing its own separate counter). Both degrade to an in-process
# equivalent when REDIS_URL is unset -- correct for today's single-worker deployment,
# but see docs/SECRETS_ROTATION.md-style deployment notes: REDIS_URL must be set before
# ever running more than one worker/dyno, or rate limits and real-time events will be
# inconsistent across requests that land on different workers.
REDIS_URL = os.getenv('REDIS_URL')

# Comma-separated list of origins allowed to open a Socket.IO connection. Defaults to
# the production frontend origin; add the local dev origin automatically in debug mode
# so `python app.py` keeps working without extra config. Never "*" -- an unauthenticated,
# wildcard-origin realtime channel is exactly what let any page on the internet open a
# socket to this server (see events.py's join-room auth fix in the same change).
_default_origins = 'https://nelavista.com'
if DEBUG_MODE:
    _default_origins += ',http://localhost:5000,http://127.0.0.1:5000'
SOCKETIO_CORS_ORIGINS = [o.strip() for o in os.getenv('SOCKETIO_CORS_ORIGINS', _default_origins).split(',') if o.strip()]

# Support contact shown in templates (footer, privacy policy, Terms of Service) instead
# of a personal address. Set SUPPORT_EMAIL in production; this default is clearly a
# placeholder rather than silently using someone's personal inbox.
SUPPORT_EMAIL = os.getenv('SUPPORT_EMAIL', 'support@nelavista.com')

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