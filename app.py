import os
from flask import Flask
from config import DEBUG_MODE, SECRET_KEY, DATABASE_URL, MAX_CONTENT_LENGTH
from extensions import db, socketio
from database import init_database, create_default_user, cleanup_stale_files
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.profile_routes import profile_bp
from routes.materials_routes import materials_bp
from routes.video_routes import video_bp
from routes.ai_routes import ai_bp
from routes.live_meeting_routes import live_bp
from routes.core_routes import core_bp



# Import socketio events to register handlers
import events

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    app.config['IMAGE_FOLDER'] = os.path.join(os.getcwd(), 'extracted_images')

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['IMAGE_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(dashboard_bp, url_prefix='/')
    app.register_blueprint(profile_bp, url_prefix='/')
    app.register_blueprint(materials_bp, url_prefix='/')
    app.register_blueprint(video_bp, url_prefix='/')
    app.register_blueprint(ai_bp, url_prefix='/')
    app.register_blueprint(live_bp, url_prefix='/')
    app.register_blueprint(core_bp, url_prefix='/')

    return app

app = create_app()

# Database initialization
cleanup_stale_files()
init_database(app)
create_default_user(app)

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 NELLAVISTA + TELLAVISTA INTEGRATED PLATFORM")
    print("="*70)
    print("🎯 COMPLETE EDUCATIONAL PLATFORM FEATURES:")
    print("   1. 👤 User Authentication & Management")
    print("   2. 🧠 Turbo AI-Style PDF Analyzer")
    print("   3. 🎥 Live Meeting System (Full Mesh WebRTC)")
    print("   4. 🤖 AI Tutor (Nelavista) with Vision & Memory")
    print("   5. 📚 Study Materials Library")
    print("   6. 🎬 Educational Reels")
    print("   7. 📝 CBT Test System")
    print("   8. 🎥 Video Upload & Sharing")
    print("="*70)
    print("\n📡 Access at: http://localhost:5000")
    print("👨‍🏫 Teacher test: http://localhost:5000/live_meeting/teacher")
    print("📊 Turbo Analyzer: http://localhost:5000/analyze")
    print("🤖 AI Tutor: http://localhost:5000/talk-to-nelavista")
    print("🎬 Videos: http://localhost:5000/videos")
    print("📤 Upload Video: http://localhost:5000/video-upload")
    print("="*70)
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=DEBUG_MODE)
