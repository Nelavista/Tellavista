from flask import Blueprint, request, jsonify, session
from utils.helpers import login_required
from models import User, Material, StudySession, Exam
from extensions import db
from datetime import datetime, date, timedelta

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
    """Get user's active courses based on department and level"""
    try:
        username = session['user']['username']
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Get materials that match user's department and level
        materials = Material.query.filter_by(
            department=user.department,
            level=user.level,
            is_approved=True
        ).limit(4).all()

        courses = []
        seen_courses = set()

        for material in materials:
            if material.department not in seen_courses:
                seen_courses.add(material.department)
                courses.append({
                    'name': material.department,
                    'type': material.course_type or 'CORE',
                    'next_topic': material.next_topic or 'Continue studying',
                    'progress': material.progress or 0
                })

        # If no courses found, add default ones based on department
        if not courses:
            default_courses = {
                'Computer Science': ['Data Structures', 'Algorithms', 'Database Systems'],
                'Biochemistry': ['Molecular Biology', 'Enzymology', 'Metabolism'],
                'Accounting': ['Financial Accounting', 'Management Accounting', 'Taxation'],
                'Botany': ['Plant Physiology', 'Plant Taxonomy', 'Ecology'],
                'Zoology': ['Animal Physiology', 'Evolution', 'Ecology']
            }

            dept_courses = default_courses.get(user.department, ['Introduction to ' + user.department])
            for course_name in dept_courses[:3]:
                courses.append({
                    'name': course_name,
                    'type': 'CORE',
                    'next_topic': 'Start learning',
                    'progress': 0
                })

        return jsonify({
            'success': True,
            'courses': courses
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
