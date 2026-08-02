from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_mail import Mail
from flask_wtf import CSRFProtect

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*", async_mode="eventlet")
mail = Mail()
csrf = CSRFProtect()
