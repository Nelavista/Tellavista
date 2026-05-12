import os
from flask import Flask, send_from_directory, render_template, request, jsonify
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

    # ==================== PWA ROUTES ====================
    
    @app.route('/manifest.json')
    def serve_manifest():
        """Serve the PWA manifest with correct MIME type and no-cache headers."""
        response = send_from_directory(
            os.path.join(app.root_path, 'static'),
            'manifest.json',
            mimetype='application/manifest+json'
        )
        response.headers['Cache-Control'] = 'public, max-age=3600'
        return response

    @app.route('/service-worker.js')
    @app.route('/sw.js')
    def serve_service_worker():
        """
        Serve the service worker from project root.
        CRITICAL: Must be at root path to control entire domain scope.
        Service workers should NOT be cached.
        """
        sw_path = os.path.join(app.root_path, 'service-worker.js')
        if not os.path.exists(sw_path):
            sw_path = os.path.join(app.root_path, 'static', 'js', 'service-worker.js')
        
        if not os.path.exists(sw_path):
            return "Service worker not found", 404
        
        response = send_from_directory(
            os.path.dirname(sw_path),
            os.path.basename(sw_path),
            mimetype='application/javascript'
        )
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        response.headers['Service-Worker-Allowed'] = '/'
        return response

    @app.route('/offline')
    def offline():
        """Render the offline fallback page."""
        return render_template('offline.html')

    @app.route('/static/icons/<path:filename>')
    def serve_pwa_icons(filename):
        """Serve PWA icons with long cache."""
        response = send_from_directory(
            os.path.join(app.root_path, 'static', 'icons'),
            filename
        )
        response.headers['Cache-Control'] = 'public, max-age=2592000'
        return response

    # ==================== ROOT ROUTE - LANDING PAGE ====================
    
    @app.route('/')
    def landing_page():
        """Serve the landing page with cache-busting."""
        import time
        response = app.make_response(render_template('landing.html', version=int(time.time())))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    # ==================== SECURITY HEADERS ====================
    
    @app.after_request
    def add_security_headers(response):
        """Add security and PWA headers to all responses."""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
        
        if response.content_type and 'text/html' in response.content_type:
            response.headers['Content-Security-Policy'] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' "
                "https://cdn.jsdelivr.net https://www.googletagmanager.com "
                "https://www.google-analytics.com https://ssl.google-analytics.com; "
                "style-src 'self' 'unsafe-inline' "
                "https://cdn.jsdelivr.net https://fonts.googleapis.com; "
                "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net; "
                "img-src 'self' data: https: blob:; "
                "connect-src 'self' https://openrouter.ai https://www.google-analytics.com "
                "https://*.google-analytics.com https://stats.g.doubleclick.net "
                "wss: ws:; "
                "media-src 'self' blob:; "
                "worker-src 'self' blob:; "
                "manifest-src 'self'; "
                "frame-src 'self'"
            )
        
        response.headers['X-Powered-By'] = 'Nelavista'
        return response

    # ==================== CORS HEADERS ====================
    
    @app.after_request
    def add_cors_headers(response):
        """Add CORS headers for PWA service worker scope."""
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        
        if response.content_type and 'application/javascript' in response.content_type:
            response.headers['Service-Worker-Allowed'] = '/'
        
        return response

    # ==================== ERROR HANDLERS ====================
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors."""
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Not found', 'code': 404}), 404
        return render_template('offline.html', error_code=404), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Internal server error', 'code': 500}), 500
        return render_template('offline.html', error_code=500), 500

    @app.errorhandler(503)
    def service_unavailable(error):
        """Handle 503 errors."""
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Service temporarily unavailable', 'code': 503}), 503
        return render_template('offline.html', error_code=503), 503

    # ==================== REGISTER BLUEPRINTS ====================
    
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(dashboard_bp, url_prefix='/')
    app.register_blueprint(profile_bp, url_prefix='/')
    app.register_blueprint(materials_bp, url_prefix='/')
    app.register_blueprint(video_bp, url_prefix='/')
    app.register_blueprint(ai_bp, url_prefix='/')
    app.register_blueprint(live_bp, url_prefix='/')
    app.register_blueprint(core_bp, url_prefix='/')

    return app


# ==================== APP CREATION ====================

app = create_app()

# Database initialization
with app.app_context():
    cleanup_stale_files()
    init_database(app)
    create_default_user(app)

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 NELLAVISTA PWA - COMPLETE EDUCATIONAL PLATFORM")
    print("="*70)
    print("🎯 PLATFORM FEATURES:")
    print("   1. 👤 User Authentication & Management")
    print("   2. 🧠 Turbo AI-Style PDF Analyzer")
    print("   3. 🎥 Live Meeting System (Full Mesh WebRTC)")
    print("   4. 🤖 AI Tutor (Nelavista) with Vision & Memory")
    print("   5. 📚 Study Materials Library")
    print("   6. 🎬 Educational Reels")
    print("   7. 📝 CBT Test System")
    print("   8. 🎥 Video Upload & Sharing")
    print("="*70)
    print("\n📱 PWA FEATURES:")
    print("   📲 Install to Home Screen")
    print("   📡 Offline Support with Service Worker")
    print("   🔔 Push Notifications (coming soon)")
    print("   📦 Background Sync")
    print("   🎨 Responsive Design")
    print("="*70)
    print("\n📡 Access at: http://localhost:5000")
    print("📊 Turbo Analyzer: http://localhost:5000/analyze")
    print("🤖 AI Tutor: http://localhost:5000/talk-to-nelavista")
    print("🎬 Videos: http://localhost:5000/videos")
    print("📱 PWA Manifest: http://localhost:5000/manifest.json")
    print("🔧 Service Worker: http://localhost:5000/service-worker.js")
    print("📴 Offline Page: http://localhost:5000/offline")
    print("="*70)
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=DEBUG_MODE, allow_unsafe_werkzeug=True)
