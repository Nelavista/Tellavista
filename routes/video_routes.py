import os
import re
import time
import uuid
import requests
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, current_app
from werkzeug.utils import secure_filename
from models import Video
from extensions import db
from utils.helpers import login_required, allowed_video_file
from config import YOUTUBE_API_KEY

video_bp = Blueprint('video', __name__)

# VIDEO_UPLOAD_FOLDER is now defined inside upload_video() to avoid application context error

@video_bp.route('/video-upload', methods=['GET', 'POST'])
@login_required
def upload_video():
    if request.method == 'GET':
        return render_template('upload.html', user=session.get('user'))

    # Define upload folder inside the function where app context is available
    VIDEO_UPLOAD_FOLDER = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(VIDEO_UPLOAD_FOLDER, exist_ok=True)

    try:
        creator_name = request.form.get('creator_name', '').strip()
        department = request.form.get('department', '').strip()
        course = request.form.get('course', '').strip()
        level = request.form.get('level', '').strip()
        semester = request.form.get('semester', '').strip()
        caption = request.form.get('caption', '').strip()
        bank_name = request.form.get('bank_name', '').strip()
        account_number = request.form.get('account_number', '').strip()
        if len(level) > 50:
            level = level[:50]
        if len(semester) > 20:
            semester = semester[:20]
        if not all([creator_name, department, course, level, semester, bank_name, account_number]):
            flash('All fields except caption are required.')
            return redirect(url_for('video.upload_video'))
        if not re.match(r'^\d{10}$', account_number):
            flash('Account number must be exactly 10 digits.')
            return redirect(url_for('video.upload_video'))
        if 'video' not in request.files:
            flash('No video file selected.')
            return redirect(url_for('video.upload_video'))
        file = request.files['video']
        if file.filename == '':
            flash('No video file selected.')
            return redirect(url_for('video.upload_video'))
        if not allowed_video_file(file.filename):
            flash('Only video files (mp4, mov, avi, mkv, webm, flv) are allowed.')
            return redirect(url_for('video.upload_video'))
        original_filename = secure_filename(file.filename)
        name_parts = original_filename.rsplit('.', 1)
        base = name_parts[0]
        ext = name_parts[1] if len(name_parts) > 1 else ''
        unique_name = f"{base}_{int(time.time())}_{uuid.uuid4().hex[:8]}.{ext}"
        video_path = os.path.join(VIDEO_UPLOAD_FOLDER, unique_name)
        file.save(video_path)
        video_url = url_for('static', filename=f'uploads/{unique_name}')
        video = Video(
            creator_name=creator_name, department=department, course=course,
            level=level, semester=semester, caption=caption, video_url=video_url,
            bank_name=bank_name, account_number=account_number,
            username=session['user']['username'], is_approved=True
        )
        db.session.add(video)
        db.session.commit()
        flash('Video uploaded successfully!')
        return redirect(url_for('video.videos_page'))
    except Exception as e:
        flash(f'Upload failed: {str(e)}')
        return redirect(url_for('video.upload_video'))

@video_bp.route('/videos')
@login_required
def videos_page():
    return render_template('video.html', user=session.get('user'))

@video_bp.route('/api/youtube/search', methods=['GET'])
def youtube_search():
    if not YOUTUBE_API_KEY:
        return jsonify({'error': 'YouTube API key not configured'}), 500
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'error': 'Missing search query'}), 400
    try:
        url = 'https://www.googleapis.com/youtube/v3/search'
        params = {'part': 'snippet', 'maxResults': 3, 'q': query, 'type': 'video', 'key': YOUTUBE_API_KEY, 'videoCategoryId': '27'}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        items = [{'videoId': item['id']['videoId'], 'title': item['snippet']['title'], 'channelTitle': item['snippet']['channelTitle']} for item in data.get('items', [])]
        return jsonify({'items': items})
    except Exception as e:
        current_app.logger.error(f"YouTube search failed: {e}")
        return jsonify({'error': 'External API error'}), 500

@video_bp.route('/api/videos')
@login_required
def api_get_videos():
    course = request.args.get('course')
    level = request.args.get('level')
    semester = request.args.get('semester')
    query = Video.query.filter_by(is_approved=True).order_by(Video.created_at.desc())
    if course:
        query = query.filter(Video.course == course)
    if level:
        query = query.filter(Video.level == level)
    if semester:
        query = query.filter(Video.semester == semester)
    videos = query.all()
    return jsonify([v.to_dict() for v in videos])

@video_bp.route('/api/videos/<int:video_id>', methods=['DELETE'])
@login_required
def delete_video(video_id):
    if not session.get('user') or session['user'].get('username') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    video = Video.query.get_or_404(video_id)
    if video.video_url and not ('youtube.com' in video.video_url or 'youtu.be' in video.video_url):
        file_path = os.path.join(current_app.root_path, video.video_url.lstrip('/'))
        if os.path.exists(file_path):
            os.remove(file_path)
    db.session.delete(video)
    db.session.commit()
    return jsonify({'success': True, 'deleted_id': video_id})

@video_bp.route('/api/courses')
@login_required
def api_get_courses():
    courses = db.session.query(Video.course).filter_by(is_approved=True).distinct().all()
    course_list = [c[0] for c in courses if c[0]]
    return jsonify(course_list)

@video_bp.route('/api/videos/<int:video_id>/view', methods=['POST'])
@login_required
def api_increment_view(video_id):
    video = Video.query.get_or_404(video_id)
    video.views += 1
    db.session.commit()
    return jsonify({'success': True, 'views': video.views})

@video_bp.route('/api/videos/<int:video_id>/like', methods=['POST'])
@login_required
def api_increment_like(video_id):
    video = Video.query.get_or_404(video_id)
    video.likes += 1
    db.session.commit()
    return jsonify({'success': True, 'likes': video.likes})

@video_bp.route('/admin/videos')
@login_required
def admin_videos():
    if session['user']['username'] != 'admin':
        flash('Access denied')
        return redirect(url_for('dashboard.dashboard'))
    videos = Video.query.filter_by(is_approved=False).order_by(Video.created_at.desc()).all()
    return render_template('admin_videos.html', videos=videos)

@video_bp.route('/admin/videos/<int:video_id>/approve', methods=['POST'])
@login_required
def admin_approve_video(video_id):
    if session['user']['username'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    video = Video.query.get_or_404(video_id)
    video.is_approved = True
    db.session.commit()
    return jsonify({'success': True})