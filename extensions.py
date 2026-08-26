from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_mail import Mail
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from authlib.integrations.flask_client import OAuth
from config import SOCKETIO_CORS_ORIGINS, REDIS_URL

db = SQLAlchemy()
# cors_allowed_origins is the real, narrow allow-list from config (never "*") -- see
# config.py's SOCKETIO_CORS_ORIGINS. message_queue is set in app.py's create_app() once
# the app is configured, so multi-worker deployments (REDIS_URL set) share live-class/
# chat state across workers instead of each worker only seeing its own local dict (see
# services/meeting_service.py).
socketio = SocketIO(cors_allowed_origins=SOCKETIO_CORS_ORIGINS, async_mode="eventlet")
mail = Mail()
csrf = CSRFProtect()
# Rate limiting storage: Redis when configured (required once more than one worker/dyno
# is running, so every worker enforces the same shared counters), falls back to Limiter's
# in-memory default otherwise -- correct for today's single-worker deployment, per
# config.py's REDIS_URL comment. default_limits is empty here; every limited route sets
# its own explicit limit (see routes/auth_routes.py, routes/ai_routes.py) rather than one
# blanket number that would be wrong for most of them.
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=(REDIS_URL if REDIS_URL else 'memory://'),
    default_limits=[],
)
# Google OAuth client (see routes/auth_routes.py). Registered in app.py's create_app()
# only when GOOGLE_CLIENT_ID/SECRET are configured -- oauth.google stays unset otherwise,
# which the routes check for before using it.
oauth = OAuth()
