import os
import requests
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, current_app
from models import Video
from extensions import db
from utils.helpers import login_required, admin_required
from config import YOUTUBE_API_KEY

video_bp = Blueprint('video', __name__)

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
@admin_required
def delete_video(video_id):
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
@admin_required
def admin_videos():
    videos = Video.query.filter_by(is_approved=False).order_by(Video.created_at.desc()).all()
    return render_template('admin_videos.html', videos=videos, active_page='videos')

@video_bp.route('/admin/videos/<int:video_id>/approve', methods=['POST'])
@login_required
@admin_required
def admin_approve_video(video_id):
    video = Video.query.get_or_404(video_id)
    video.is_approved = True
    db.session.commit()
    return jsonify({'success': True})