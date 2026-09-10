"""Production and local development entry point for Nelavista."""

from app import app
from app.config import DEBUG_MODE
from app.extensions import socketio


if __name__ == '__main__':
    import os

    socketio.run(
        app,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=DEBUG_MODE,
        allow_unsafe_werkzeug=True,
    )
