import os
from flask import Blueprint, current_app, send_from_directory

pwa_bp = Blueprint('pwa', __name__)


@pwa_bp.route('/manifest.json')
def serve_manifest():
    """Serve the PWA manifest with correct MIME type and no-cache headers."""
    response = send_from_directory(
        os.path.join(current_app.root_path, 'static'),
        'manifest.json',
        mimetype='application/manifest+json'
    )
    response.headers['Cache-Control'] = 'public, max-age=3600'  # 1 hour cache
    return response


@pwa_bp.route('/static/icons/<path:filename>')
def serve_pwa_icons(filename):
    """Serve PWA icons with long cache."""
    response = send_from_directory(
        os.path.join(current_app.root_path, 'static', 'icons'),
        filename
    )
    response.headers['Cache-Control'] = 'public, max-age=2592000'  # 30 days
    return response
