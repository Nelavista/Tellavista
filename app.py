import os
from flask import Flask, send_from_directory, render_template
from config import DEBUG_MODE, SECRET_KEY, DATABASE_URL, MAX_CONTENT_LENGTH
from extensions import db, socketio, mail
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

    # --- Email Configuration ---
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'your-email@gmail.com')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your-app-password')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@nelavista.com')

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['IMAGE_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    mail.init_app(app)

    # ==================== PWA ROUTES ====================
    
    @app.route('/manifest.json')
    def serve_manifest():
        """Serve the PWA manifest with correct MIME type and no-cache headers."""
        response = send_from_directory(
            os.path.join(app.root_path, 'static'),
            'manifest.json',
            mimetype='application/manifest+json'
        )
        response.headers['Cache-Control'] = 'public, max-age=3600'  # 1 hour cache
        return response

    @app.route('/service-worker.js')
    @app.route('/sw.js')
    def serve_service_worker():
        """
        Serve the service worker from project root.
        CRITICAL: Must be at root path to control entire domain scope.
        Service workers should NOT be cached.
        """
        # Try from root first, then from static/js
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
        # Service workers must never be cached
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
        # Cache icons for 30 days
        response.headers['Cache-Control'] = 'public, max-age=2592000'
        return response

    # ==================== SECURITY HEADERS ====================
    
    @app.after_request
    def add_security_headers(response):
        """Add security and PWA headers to all responses."""
        # Security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
        
        # Only add CSP to HTML responses
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
        
        # PWA-specific headers
        response.headers['X-Powered-By'] = 'Nelavista'
        
        return response

    # ==================== CORS HEADERS FOR PWA ====================
    
    @app.after_request
    def add_cors_headers(response):
        """Add CORS headers for PWA service worker scope."""
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        
        # Allow service worker to register
        if response.content_type and 'application/javascript' in response.content_type:
            response.headers['Service-Worker-Allowed'] = '/'
        
        return response

    # ==================== ERROR HANDLERS ====================
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors - return JSON for API, HTML for pages."""
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
        """Handle 503 errors (service unavailable)."""
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


def generate_pwa_icons():
    """Generate all required PWA icons if they don't exist."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        icons_dir = os.path.join(os.path.dirname(__file__), 'static', 'icons')
        os.makedirs(icons_dir, exist_ok=True)
        
        sizes = [16, 32, 72, 96, 120, 128, 144, 152, 167, 180, 192, 384, 512]
        
        for size in sizes:
            filename = os.path.join(icons_dir, f'nelavista-{size}x{size}.png')
            
            # Skip if already exists
            if os.path.exists(filename):
                print(f'⏭️  Icon already exists: {size}x{size}')
                continue
            
            # Create image with transparent background
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Draw gradient background
            for i in range(size):
                color = (
                    int(56 + (i / size) * 20),    # R: 56 -> 76
                    int(189 - (i / size) * 40),   # G: 189 -> 149
                    int(248 - (i / size) * 50),   # B: 248 -> 198
                    255
                )
                draw.rectangle([0, i, size, i + 1], fill=color)
            
            # Draw rounded rectangle background
            margin = size // 8
            draw.rounded_rectangle(
                [margin, margin, size - margin, size - margin],
                radius=size // 6,
                fill=(5, 8, 16, 230)
            )
            
            # Draw 'N' character
            try:
                # Try to use system font
                font_size = size // 2
                font = ImageFont.truetype(
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 
                    font_size
                )
            except:
                try:
                    # Try alternative font path
                    font = ImageFont.truetype(
                        "/System/Library/Fonts/Helvetica.ttc", 
                        size // 2
                    )
                except:
                    # Fallback to default font
                    font = ImageFont.load_default()
            
            # Draw the letter 'N' centered
            text = 'N'
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (size - text_width) // 2
            y = (size - text_height) // 2
            
            # Draw text with gradient
            draw.text((x, y), text, fill=(56, 189, 248, 255), font=font)
            
            # Draw subtle border
            draw.rounded_rectangle(
                [margin, margin, size - margin, size - margin],
                radius=size // 6,
                outline=(56, 189, 248, 60),
                width=max(1, size // 60)
            )
            
            # Add shine effect (smaller sizes look better without it)
            if size >= 72:
                shine_margin = size // 3
                draw.ellipse(
                    [shine_margin, shine_margin, 
                     size - shine_margin, size - shine_margin],
                    outline=(255, 255, 255, 30),
                    width=max(1, size // 80)
                )
            
            img.save(filename, 'PNG')
            print(f'✅ Created icon: {size}x{size}')
        
        # Create favicon (32x32 ICO format or use PNG)
        favicon_path = os.path.join(icons_dir, 'favicon.ico')
        if not os.path.exists(favicon_path):
            # For favicon, just copy the 32x32 PNG
            import shutil
            shutil.copy(
                os.path.join(icons_dir, 'nelavista-32x32.png'),
                favicon_path
            )
            print('✅ Created favicon.ico')
        
        # Create maskable icon (with padding for safe area)
        maskable_path = os.path.join(icons_dir, 'nelavista-maskable-512x512.png')
        if not os.path.exists(maskable_path):
            create_maskable_icon(icons_dir)
            print('✅ Created maskable icon')
        
        print(f'\n📦 All {len(sizes)} icons generated in: {icons_dir}')
        
    except ImportError:
        print('⚠️  Pillow not installed. Install with: pip install Pillow')
        print('   Icons must be created manually or run: python generate_icons.py')
    except Exception as e:
        print(f'❌ Error generating icons: {e}')
        print('   You can manually create icons or install Pillow: pip install Pillow')

def create_maskable_icon(icons_dir):
    """Create a maskable icon with safe zone padding."""
    from PIL import Image, ImageDraw, ImageFont
    
    size = 512
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Safe zone (80% of icon)
    safe_margin = int(size * 0.1)  # 10% padding on each side
    icon_size = size - (2 * safe_margin)
    
    # Draw gradient background in safe zone
    for i in range(icon_size):
        color = (
            int(56 + (i / icon_size) * 20),
            int(189 - (i / icon_size) * 40),
            int(248 - (i / icon_size) * 50),
            255
        )
        draw.rectangle(
            [safe_margin, safe_margin + i, 
             size - safe_margin, safe_margin + i + 1],
            fill=color
        )
    
    # Draw 'N' letter
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            icon_size // 2
        )
    except:
        font = ImageFont.load_default()
    
    text = 'N'
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), text, fill=(56, 189, 248, 255), font=font)
    
    img.save(os.path.join(icons_dir, 'nelavista-maskable-512x512.png'), 'PNG')


# ==================== APP CREATION ====================

app = create_app()

# Database initialization
with app.app_context():
    cleanup_stale_files()
    init_database(app)
    create_default_user(app)

# Generate icons on startup (development only)
if DEBUG_MODE:
    generate_pwa_icons()

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
