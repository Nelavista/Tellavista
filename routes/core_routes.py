import os
from datetime import datetime
from flask import Blueprint, jsonify, send_from_directory, session, request, current_app
from utils.helpers import login_required, debug_print

core_bp = Blueprint('core', __name__)

@core_bp.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Nellavista + Tellavista Integrated Platform",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "3.0",
        "features": ["User Authentication", "Turbo AI PDF Analyzer", "Live Meeting System", "AI Tutor", "Study Materials", "Educational Reels", "CBT System"]
    })

@core_bp.route('/cleanup_attachments', methods=['POST'])
@login_required
def cleanup_attachments():
    try:
        keys_to_remove = ['last_file_id', 'last_file_type', 'last_file_name', 'last_file_path', 'last_upload_time', 'last_image_base64', 'last_file_content', 'last_file_preview']
        for key in keys_to_remove:
            session.pop(key, None)
        return jsonify({"success": True, "message": "Attachment context cleared"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@core_bp.route('/clear_context', methods=['POST'])
@login_required
def clear_context():
    try:
        file_path = session.get('last_file_path')
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        for key in ['last_file_content', 'last_file_type', 'last_upload_time', 'last_image_base64', 'last_file_path', 'last_file_id', 'last_file_name']:
            session.pop(key, None)
        return jsonify({"success": True, "message": "File context cleared successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": "Failed to clear context"}), 500

@core_bp.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(current_app.root_path, 'templates', 'images'), filename)