from flask import Blueprint, request, jsonify, session
from utils.helpers import login_required
from models import User, StudySession, Exam
from extensions import db
from datetime import datetime, date, timedelta
from services.academic_context import resolve_academic_context
from services.progress_service import get_courses_materials_progress_bulk
from models import Topic
from sqlalchemy import func

study_bp = Blueprint('study', __name__)


# ===== STUDY SESSION TRACKING =====
@study_bp.route('/api/track-session', methods=['POST'])
@login_required
def track_session():
    """Track user study session time"""
    try:
        data = request.get_json()
        seconds = data.get('seconds', 0)

        username = session['user']['username']
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Get or create today's study record
        today = date.today()

        study_record = StudySession.query.filter_by(
            user_id=user.id,
            date=today
        ).first()

        if not study_record:
            study_record = StudySession(
                user_id=user.id,
                date=today,
                seconds=0
            )
            db.session.add(study_record)

        study_record.seconds += seconds
        db.session.commit()

        return jsonify({
            'success': True,
            'total_seconds': study_record.seconds,
            'total_hours': round(study_record.seconds / 3600, 1)
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ===== GET STUDY STATISTICS =====
@study_bp.route('/api/study-stats', methods=['GET'])
@login_required
def get_study_stats():
    """Get weekly study statistics"""
    try:
        username = session['user']['username']
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Get last 7 days
        today = date.today()
        week_ago = today - timedelta(days=6)

        records = StudySession.query.filter(
            StudySession.user_id == user.id,
            StudySession.date >= week_ago,
            StudySession.date <= today
        ).all()

        # Build day-by-day data
        days_data = {
            'Mon': 0, 'Tue': 0, 'Wed': 0, 'Thu': 0,
            'Fri': 0, 'Sat': 0, 'Sun': 0
        }

        total_seconds = 0
        for record in records:
            day_name = record.date.strftime('%a')
            hours = round(record.seconds / 3600, 1)
            days_data[day_name] = hours
            total_seconds += record.seconds

        total_hours = round(total_seconds / 3600, 1)

        return jsonify({
            'success': True,
            'total': total_hours,
            'days': days_data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===== EXAM MANAGEMENT =====
@study_bp.route('/api/exams', methods=['GET', 'POST'])
@login_required
def manage_exams():
    """Get or create exams"""
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if request.method == 'POST':
        try:
            data = request.get_json()
            course = data.get('course', '').strip()
            exam_date = data.get('date', '').strip()
            duration = data.get('duration', '').strip()

            if not course or not exam_date:
                return jsonify({'error': 'Course and date are required'}), 400

            # Parse date
            exam_date_obj = datetime.strptime(exam_date, '%Y-%m-%d').date()

            new_exam = Exam(
                user_id=user.id,
                course=course,
                date=exam_date_obj,
                duration=duration
            )
            db.session.add(new_exam)
            db.session.commit()

            return jsonify({
                'success': True,
                'exam': new_exam.to_dict()
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    else:  # GET request
        try:
            exams = Exam.query.filter_by(user_id=user.id).order_by(Exam.date.asc()).all()
            return jsonify({
                'success': True,
                'exams': [e.to_dict() for e in exams]
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500


# ===== USER COURSES =====
@study_bp.route('/api/user-courses')
@login_required
def get_user_courses():
    """Real courses for this student's actual university/faculty/department/level,
    resolved from the taxonomy (see services/academic_context.py) -- never a hardcoded
    or invented course list. A student the taxonomy doesn't cover yet (unresolved
    university/department) genuinely gets an empty list; the dashboard already has an
    honest empty state for that ("No courses found. Browse materials →")."""
    try:
        username = session['user']['username']
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        ctx = resolve_academic_context(user)
        all_courses = list(ctx.courses)

        # Bulk-computed instead of one query per course -- a student with 20+ courses
        # (the normal case for a whole department/level) previously cost 2-3 remote
        # round-trips *per course* here, which is what made "Loading your courses..."
        # visibly slow. Both are now O(1) queries regardless of course count.
        progress_by_code = get_courses_materials_progress_bulk(user, [c.code for c in all_courses])
        topic_counts = dict(
            db.session.query(Topic.course_id, func.count(Topic.id))
            .filter(Topic.course_id.in_([c.id for c in all_courses]), Topic.is_active == True)  # noqa: E712
            .group_by(Topic.course_id)
            .all()
        ) if all_courses else {}

        courses = []
        for course in all_courses:
            viewed, total = progress_by_code.get(course.code, (0, 0))
            progress = round(viewed / total * 100) if total else 0
            courses.append({
                'code': course.code,
                'title': course.title,
                'name': f"{course.code} — {course.title}",
                'type': course.course_type or 'CORE',
                'topic_count': topic_counts.get(course.id, 0),
                'next_topic': 'Continue studying' if viewed else 'Start learning',
                'progress': progress,
                'link': f"/courses/{course.code}",
            })

        return jsonify({
            'success': True,
            'courses': courses
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
