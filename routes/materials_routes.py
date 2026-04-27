import os
import cloudinary
import cloudinary.uploader
import requests
from bs4 import BeautifulSoup
from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
from utils.helpers import login_required, is_academic_book, check_profile_complete
from models import User, Material, StudySession, Exam
from extensions import db
from config import OPENROUTER_API_KEY
from datetime import datetime, date, timedelta


# ===== PROFILE COMPLETION HELPER FUNCTION =====
def check_profile_complete(user):
    """
    Check if user has completed their profile.
    Returns True if profile is complete, False otherwise.
    """
    required_fields = ['name', 'university', 'faculty', 'department', 'level', 'semester']
    
    for field in required_fields:
        value = getattr(user, field, None)
        if not value or str(value).strip() == '':
            return False
    
    return True


# ===== CLOUDINARY CONFIG =====
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
    secure=True
)

# ===== GOOGLE CUSTOM SEARCH CONFIG =====
GOOGLE_API_KEY = os.environ.get('GOOGLE_CUSTOM_SEARCH_API_KEY')
GOOGLE_SEARCH_ENGINE_ID = os.environ.get('GOOGLE_SEARCH_ENGINE_ID')

materials_bp = Blueprint('materials', __name__)


# ===== ENFORCE PROFILE COMPLETION SITE-WIDE =====
@materials_bp.before_app_request
def enforce_profile_completion():
    # Skip for static files, login/logout, dashboard, and the completion endpoint itself
    if request.endpoint in ('auth.login', 'auth.logout', 'dashboard.dashboard',
                            'materials.complete_profile', 'static'):
        return None

    # Get user from session
    if 'user' not in session:
        return None

    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    if user and not check_profile_complete(user):
        # Redirect to dashboard; the modal will appear there
        return redirect(url_for('dashboard.dashboard'))


# ===== GOOGLE CUSTOM SEARCH FUNCTION =====
def search_google_pdfs(course_code, max_results=10):
    """
    Search Google Custom Search API for PDF materials related to a course code.
    Returns list of dicts with title, url, snippet.
    """
    if not GOOGLE_API_KEY or not GOOGLE_SEARCH_ENGINE_ID:
        print("[WARNING] Google API credentials not configured")
        return []
    
    # Try multiple query variations for better results
    queries = [
        f'{course_code} lecture notes filetype:pdf',
        f'{course_code} past questions filetype:pdf',
        f'{course_code} study material filetype:pdf'
    ]
    
    all_results = []
    seen_urls = set()
    
    for query in queries[:2]:  # Limit to 2 queries to stay within free tier
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': GOOGLE_API_KEY,
                'cx': GOOGLE_SEARCH_ENGINE_ID,
                'q': query,
                'num': min(max_results, 10),
                'fileType': 'pdf'
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                
                for item in items:
                    pdf_url = item.get('link', '')
                    if pdf_url and pdf_url not in seen_urls:
                        seen_urls.add(pdf_url)
                        all_results.append({
                            'title': item.get('title', f'{course_code} Material'),
                            'url': pdf_url,
                            'snippet': item.get('snippet', '')
                        })
            else:
                print(f"[ERROR] Google API error: {response.status_code} - {response.text[:200]}")
                
        except Exception as e:
            print(f"[ERROR] Google search exception: {str(e)}")
            continue
    
    return all_results[:max_results]


# ===== FETCH GOOGLE MATERIALS FOR A COURSE CODE =====
@materials_bp.route('/api/fetch-google-materials/<course_code>')
@login_required
def fetch_google_materials(course_code):
    """
    Fetch materials from Google Custom Search for a specific course code.
    Caches results in database to avoid repeated API calls.
    """
    try:
        course_code = course_code.upper().strip()
        
        # Check if we already have cached Google materials for this course code
        cached = Material.query.filter_by(
            course_code=course_code,
            source='google_auto',
            is_approved=True
        ).all()
        
        if cached:
            return jsonify({
                'success': True,
                'materials': [m.to_dict() for m in cached],
                'cached': True
            })
        
        # No cached results - fetch from Google
        results = search_google_pdfs(course_code, max_results=8)
        
        if not results:
            return jsonify({
                'success': True,
                'materials': [],
                'message': 'No PDF materials found for this course code'
            })
        
        # Save results to database
        saved_materials = []
        for r in results:
            # Check if this URL already exists
            existing = Material.query.filter_by(
                external_url=r['url'],
                source='google_auto'
            ).first()
            
            if existing:
                saved_materials.append(existing)
                continue
            
            new_material = Material(
                title=r['title'][:200],  # Truncate to fit DB
                course_code=course_code,
                external_url=r['url'],
                source='google_auto',
                is_approved=True,  # Auto-approve Google results
                uploaded_by='Google Search',
                department='General',  # Can be updated later
                level='100',  # Default, can be refined
                semester='First Semester'
            )
            db.session.add(new_material)
            saved_materials.append(new_material)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'materials': [m.to_dict() for m in saved_materials],
            'cached': False,
            'count': len(saved_materials)
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] fetch_google_materials: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ===== BATCH FETCH GOOGLE MATERIALS FOR MULTIPLE COURSES =====
@materials_bp.route('/api/fetch-google-materials-batch', methods=['POST'])
@login_required
def fetch_google_materials_batch():
    """
    Fetch Google materials for multiple course codes at once.
    Expects JSON: {'course_codes': ['MAT101', 'CSC111', ...]}
    """
    try:
        data = request.get_json()
        course_codes = data.get('course_codes', [])
        
        if not course_codes:
            return jsonify({'error': 'No course codes provided'}), 400
        
        all_materials = []
        
        for code in course_codes[:5]:  # Limit to 5 courses per batch request
            code = code.upper().strip()
            
            # Check cache first
            cached = Material.query.filter_by(
                course_code=code,
                source='google_auto',
                is_approved=True
            ).all()
            
            if cached:
                all_materials.extend([m.to_dict() for m in cached])
            else:
                # Fetch and save
                results = search_google_pdfs(code, max_results=5)
                for r in results:
                    existing = Material.query.filter_by(
                        external_url=r['url'],
                        source='google_auto'
                    ).first()
                    
                    if not existing:
                        new_material = Material(
                            title=r['title'][:200],
                            course_code=code,
                            external_url=r['url'],
                            source='google_auto',
                            is_approved=True,
                            uploaded_by='Google Search',
                            department='General',
                            level='100',
                            semester='First Semester'
                        )
                        db.session.add(new_material)
                        all_materials.append(new_material.to_dict())
                    else:
                        all_materials.append(existing.to_dict())
                
                db.session.commit()
        
        return jsonify({
            'success': True,
            'materials': all_materials,
            'count': len(all_materials)
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] fetch_google_materials_batch: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ===== PROFILE COMPLETION ROUTE =====
@materials_bp.route('/complete-profile', methods=['GET', 'POST'])
@login_required
def complete_profile():
    """
    Route to handle profile completion modal.
    GET: Display the modal (fallback)
    POST: Process the form submission
    """
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    
    if not user:
        flash('User not found. Please log in again.')
        return redirect(url_for('auth.login'))
    
    # If profile is already complete, redirect to dashboard
    if check_profile_complete(user):
        return redirect(url_for('dashboard.dashboard'))
    
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name', '').strip()
            university = request.form.get('university', '').strip()
            faculty = request.form.get('faculty', '').strip()
            department = request.form.get('department', '').strip()
            user_level = request.form.get('user_level', '').strip()
            semester = request.form.get('semester', '').strip()
            
            # Validate all fields are filled
            if not all([name, university, faculty, department, user_level, semester]):
                flash('Please fill in all required fields.', 'error')
                return render_template('profile_completion_modal.html', user=user)
            
            # Update user profile
            user.name = name
            user.university = university
            user.faculty = faculty
            user.department = department
            user.level = user_level
            user.semester = semester
            
            # Commit to database
            db.session.commit()
            
            flash('Profile completed successfully! Welcome to Nelavista 🎉', 'success')
            
            # Redirect to dashboard
            return redirect(url_for('dashboard.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'error')
            return render_template('profile_completion_modal.html', user=user)
    
    # GET request - show the modal (fallback)
    return render_template('profile_completion_modal.html', user=user)


@materials_bp.route('/about')
def about():
    return render_template('about.html')


@materials_bp.route('/campus-map')
def campus_map():
    return render_template('campus-map.html')


@materials_bp.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')


@materials_bp.route('/settings')
@login_required
def settings():
    memory = {
        "traits": session.get('traits', []),
        "more_info": session.get('more_info', ''),
        "enable_memory": session.get('enable_memory', False)
    }
    return render_template('settings.html', memory=memory,
                           theme=session.get('theme'), language=session.get('language'))


@materials_bp.route('/memory', methods=['POST'])
@login_required
def save_memory():
    session['theme'] = request.form.get('theme')
    session['language'] = request.form.get('language')
    session['notifications'] = 'notifications' in request.form
    flash('Settings saved!')
    return redirect(url_for('materials.settings'))


@materials_bp.route('/materials')
@login_required
def materials():
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User not found. Please log in again.')
        return redirect(url_for('auth.login'))
    
    # Profile completeness is now handled by before_request
    return render_template("materials.html", user=user)


# ===== UPLOAD MATERIAL TO CLOUDINARY + SAVE TO DB =====
@materials_bp.route('/api/upload-material', methods=['POST'])
@login_required
def upload_material():
    try:
        username = session['user']['username']
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 401

        title       = request.form.get('title', '').strip()
        course      = request.form.get('course', '').strip()
        level       = request.form.get('level', '').strip()
        semester    = request.form.get('semester', '').strip()
        course_code = request.form.get('course_code', '').strip().upper()
        author      = request.form.get('author', '').strip()
        description = request.form.get('description', '').strip()
        file        = request.files.get('file')

        if not all([title, course, level, semester, course_code, author]):
            return jsonify({'error': 'All required fields must be filled'}), 400

        if not file:
            return jsonify({'error': 'No file provided'}), 400

        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Only PDF files are allowed'}), 400

        # Upload to Cloudinary — 'raw' resource_type is required for PDFs
        import time
        public_id = f"nelavista_materials/{course_code}_{title[:40].replace(' ', '_')}_{int(time.time())}"
        upload_result = cloudinary.uploader.upload(
            file,
            resource_type='raw',
            public_id=public_id,
            overwrite=False,
            tags=[course, level, semester, course_code]
        )

        cloudinary_url = upload_result.get('secure_url')
        if not cloudinary_url:
            return jsonify({'error': 'Upload to Cloudinary failed — no URL returned'}), 500

        # Save metadata to Material table
        new_material = Material(
            title=title,
            department=course,
            level=level,
            semester=semester,
            course_type=course_code,
            next_topic=description if description else None,
            file_url=cloudinary_url,
            uploaded_by=author,
            source='uploaded',  # Set source as uploaded
            is_approved=False
        )
        db.session.add(new_material)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Material uploaded successfully and pending admin approval!',
            'material': new_material.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500


# ===== FETCH UPLOADED MATERIALS FROM DB =====
@materials_bp.route('/api/fetch-materials')
@login_required
def fetch_materials():
    try:
        course   = request.args.get('course', '').strip()
        level    = request.args.get('level', '').strip()
        semester = request.args.get('semester', '').strip()

        # Build query - only show approved materials
        query = Material.query.filter_by(is_approved=True)
        
        # Apply filters if provided
        if course:
            query = query.filter_by(department=course)
        if level:
            query = query.filter_by(level=level)
        if semester:
            query = query.filter_by(semester=semester)
        
        # Order by id descending
        results = query.order_by(Material.id.desc()).all()

        return jsonify({
            'success': True,
            'materials': [m.to_dict() for m in results]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===== DELETE MATERIAL (Admin: user_level >= 5) =====
@materials_bp.route('/api/delete-material/<int:material_id>', methods=['DELETE'])
@login_required
def delete_material_api(material_id):
    try:
        username = session['user']['username']
        user = User.query.filter_by(username=username).first()
        
        # Convert user_level to int for comparison
        if not user or int(user.user_level or 0) < 5:
            return jsonify({'error': 'Unauthorized — admin only'}), 403

        material = Material.query.get(material_id)
        if not material:
            return jsonify({'error': 'Material not found'}), 404

        # Try to delete from Cloudinary if it's an uploaded file
        if material.file_url and material.source == 'uploaded':
            try:
                parts = material.file_url.split('/upload/')
                if len(parts) == 2:
                    path_part = parts[1]
                    # Strip version segment like v1234567890/
                    segments = path_part.split('/')
                    if segments[0].startswith('v') and segments[0][1:].isdigit():
                        segments = segments[1:]
                    public_id = '/'.join(segments)
                    cloudinary.uploader.destroy(public_id, resource_type='raw')
            except Exception:
                pass  # Still delete from DB even if Cloudinary delete fails

        db.session.delete(material)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Material deleted'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ===== ADMIN MATERIALS MANAGEMENT =====
@materials_bp.route('/admin/materials')
@login_required
def admin_materials():
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    
    # Only allow admins (user_level >= 5)
    if not user or int(user.user_level or 0) < 5:
        flash('Unauthorized access')
        return redirect(url_for('dashboard.dashboard'))
    
    # Get all pending materials
    pending = Material.query.filter_by(is_approved=False).order_by(Material.id.desc()).all()
    
    return render_template('admin_materials.html', pending=pending, user=user)


@materials_bp.route('/admin/materials/approve/<int:material_id>', methods=['POST'])
@login_required
def approve_material(material_id):
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    
    if not user or int(user.user_level or 0) < 5:
        return jsonify({'error': 'Unauthorized'}), 403
    
    material = Material.query.get(material_id)
    if not material:
        return jsonify({'error': 'Material not found'}), 404
    
    material.is_approved = True
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Material approved'})


@materials_bp.route('/admin/materials/reject/<int:material_id>', methods=['DELETE'])
@login_required
def reject_material(material_id):
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    
    if not user or int(user.user_level or 0) < 5:
        return jsonify({'error': 'Unauthorized'}), 403
    
    material = Material.query.get(material_id)
    if not material:
        return jsonify({'error': 'Material not found'}), 404
    
    # Delete from Cloudinary if needed
    if material.file_url and material.source == 'uploaded':
        try:
            parts = material.file_url.split('/upload/')
            if len(parts) == 2:
                path_part = parts[1]
                segments = path_part.split('/')
                if segments[0].startswith('v') and segments[0][1:].isdigit():
                    segments = segments[1:]
                public_id = '/'.join(segments)
                cloudinary.uploader.destroy(public_id, resource_type='raw')
        except Exception:
            pass
    
    db.session.delete(material)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Material rejected and deleted'})


@materials_bp.route('/debug/check-admin')
@login_required
def debug_check_admin():
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    
    return jsonify({
        'username': user.username,
        'user_level': user.user_level,
        'user_level_type': type(user.user_level).__name__,
        'converted_to_int': int(user.user_level or 0),
        'is_admin': int(user.user_level or 0) >= 5,
        'all_user_fields': {
            'name': user.name,
            'department': user.department,
            'level': user.level,
            'semester': user.semester
        }
    })


# ===== STUDY SESSION TRACKING =====
@materials_bp.route('/api/track-session', methods=['POST'])
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
@materials_bp.route('/api/study-stats', methods=['GET'])
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
@materials_bp.route('/api/exams', methods=['GET', 'POST'])
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
@materials_bp.route('/api/user-courses')
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


# ========== REMAINING ROUTES ==========

@materials_bp.route('/api/materials')
def get_study_materials():
    query = request.args.get("q", "python")
    pdfs = []
    try:
        pdf_html = requests.get(
            f"https://www.pdfdrive.com/search?q={query}",
            headers={"User-Agent": "Mozilla/5.0"}, timeout=10).text
        soup = BeautifulSoup(pdf_html, 'html.parser')
        for book in soup.select('.file-left')[:5]:
            title = book.select_one('img')['alt']
            link = "https://www.pdfdrive.com" + book.parent['href']
            pdfs.append({'title': title, 'link': link})
    except Exception as e:
        pdfs = [{"error": str(e)}]
    books = []
    try:
        ol_data = requests.get(
            f"https://openlibrary.org/search.json?q={query}", timeout=10).json()
        for doc in ol_data.get("docs", [])[:5]:
            books.append({
                "title": doc.get("title"),
                "author": ', '.join(doc.get("author_name", [])) if doc.get("author_name") else "Unknown",
                "link": f"https://openlibrary.org{doc.get('key')}"
            })
    except Exception as e:
        books = [{"error": str(e)}]
    return jsonify({"query": query, "pdfs": pdfs, "books": books})


@materials_bp.route('/ai/materials')
def ai_materials():
    topic      = request.args.get("topic")
    level      = request.args.get("level")
    department = request.args.get("department")
    goal       = request.args.get("goal", "general")
    if not topic or not level or not department:
        return jsonify({"error": "Missing one or more parameters: topic, level, department"}), 400
    prompt = (
        f"You're an educational AI helping a {level} student in the {department} department. "
        f"They want to learn: '{goal}' in the topic of {topic}. "
        f"Provide a short and clear explanation. End with: '📚 Here are materials to study further:'"
    )
    explanation = ""
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://nelavista.com",
            "X-Title": "Nelavista AI Tutor"
        }
        payload = {
            "model": "openai/gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are an educational AI assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7, "max_tokens": 500
        }
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            explanation = response.json()["choices"][0]["message"]["content"]
        else:
            explanation = f"Let me help you learn {topic}. 📚 Here are materials to study further:"
    except Exception:
        explanation = f"Let me help you learn {topic}. 📚 Here are materials to study further:"
    pdfs = []
    try:
        pdf_html = requests.get(
            f"https://www.pdfdrive.com/search?q={topic}",
            headers={"User-Agent": "Mozilla/5.0"}, timeout=10).text
        soup = BeautifulSoup(pdf_html, 'html.parser')
        for book in soup.select('.file-left')[:10]:
            title = book.select_one('img')['alt']
            if is_academic_book(title, topic, department):
                link = "https://www.pdfdrive.com" + book.parent['href']
                pdfs.append({'title': title, 'link': link})
    except Exception:
        pdfs = [{"error": "Failed to fetch PDFs"}]
    books = []
    try:
        ol_data = requests.get(
            f"https://openlibrary.org/search.json?q={topic}", timeout=10).json()
        for doc in ol_data.get("docs", [])[:10]:
            title = doc.get("title", "")
            if is_academic_book(title, topic, department):
                books.append({
                    "title": doc.get("title"),
                    "author": ', '.join(doc.get("author_name", [])) if doc.get("author_name") else "Unknown",
                    "link": f"https://openlibrary.org{doc.get('key')}"
                })
    except Exception:
        books = [{"error": "Failed to fetch books"}]
    return jsonify({"query": topic, "ai_explanation": explanation, "pdfs": pdfs, "books": books})


@materials_bp.route("/mat101")
def math101():
    return render_template("mat101.html")


@materials_bp.route('/reels')
def reels():
    categories = ["Tech", "Motivation", "Islamic", "AI"]
    selected_category = request.args.get("category")
    videos = []
    if selected_category:
        videos = [
            {"title": f"{selected_category} Reel 1", "video_id": "abc123"},
            {"title": f"{selected_category} Reel 2", "video_id": "def456"}
        ]
    return render_template("reels.html", user=session.get("user"), categories=categories,
                           selected_category=selected_category, videos=videos)


@materials_bp.route("/api/reels")
def get_reels():
    course = request.args.get("course")
    all_reels = [
        {"course": "Accountancy", "caption": "Introduction to Accounting", "video_url": "https://youtu.be/Gua2Bo_G-J0?si=FNnNZBbmBh0yqvrk"},
        {"course": "Accountancy", "caption": "Financial Statements Basics", "video_url": "https://youtu.be/fb7YCVR5fIU?si=XWozkxGoBV2HP2HW"},
        {"course": "Accountancy", "caption": "Management Accounting Overview", "video_url": "https://youtu.be/qISkyoiGHcI?si=BKRnkFfl-fqKXgLG"},
        {"course": "Accountancy", "caption": "Auditing Principles", "video_url": "https://youtu.be/27gabbJQZqc?si=rsOLmkD2QXOoxSoi"},
        {"course": "Accountancy", "caption": "Taxation Fundamentals", "video_url": "https://youtu.be/Cox8rLXYAGQ?si=CvKUaPuPJOxPb6cr"},
        {"course": "Accountancy", "caption": "Learn Accounting in under 5 hours", "video_url": "https://youtu.be/gPBhGkBN30s?si=bUYfaccZPlBni3aZ"},
        {"course": "Accountancy", "caption": "The ACCOUNTING BASICS for BEGINNERS (3 core parts)", "video_url": "https://youtu.be/Gua2Bo_G-J0?si=aM8ZPO-OqtV-ZbJ9"},
        {"course": "Accounting", "caption": "Basics of Double Entry", "video_url": "https://youtu.be/cjO8qHM5Wjg?si=P0hcqm9x-wjmXpN3"},
        {"course": "Accounting", "caption": "Trail Balance Explained", "video_url": "https://youtu.be/3_PfoTzSCQE?si=SGRI7KVJ6ZC3iJe7"},
        {"course": "Accounting", "caption": "Financial Analysis Techniques", "video_url": "https://youtu.be/g2wEFJ7upNs?si=ht44vAply2f7b-P0"},
        {"course": "Accounting", "caption": "Cost Accounting Overview", "video_url": "https://youtu.be/a5D3Iopi0-4?si=vXOVFcV1NqPGt6Tk"},
        {"course": "Accounting", "caption": "Budgeting and Forecasting", "video_url": "https://youtu.be/GjxhDo9luh8?si=BXn4Z5J-RdKJdBoP"},
        {"course": "Agriculture", "caption": "Introduction to Agriculture", "video_url": "https://youtu.be/1FLcijYWHZQ?si=B6iWcOVNXYCDWsKR"},
        {"course": "Agriculture", "caption": "Crop Production Techniques", "video_url": "https://youtu.be/j4-0rNhxoKs?si=XaUcN8zOq1EtkVbX"},
        {"course": "Agriculture", "caption": "Soil Fertility Management", "video_url": "https://youtu.be/TjbxOEEOCh0?si=grkiA5OewbgtFF78"},
        {"course": "Agriculture", "caption": "Livestock Management", "video_url": "https://youtu.be/TjbxOEEOCh0?si=Jr_UpYvei_oieZxz"},
        {"course": "Agriculture", "caption": "Agricultural Economics", "video_url": "https://youtu.be/fbOiwV3gBLg?si=f8HcQW1xdOEfQXEy"},
        {"course": "Arabic Studies", "caption": "Arabic Language Basics", "video_url": "https://youtu.be/X1mC1XY65Kc?si=gIIUVXBrseXau1Tj"},
        {"course": "Arabic Studies", "caption": "Arabic Grammar Essentials", "video_url": "https://youtu.be/CKD1O4tKZUA?si=JwH8Hb090aZTAI7n"},
        {"course": "Arabic Studies", "caption": "Conversational Arabic", "video_url": "https://youtu.be/dinQIb4ZFXY?si=eGF1Vhsdwm8imJ3Y"},
        {"course": "Arabic Studies", "caption": "Arabic Poetry Introduction", "video_url": "https://youtu.be/ZmjK5cu81RA?si=XnRGefNNXTCws278"},
        {"course": "Arabic Studies", "caption": "Arabic Writing Skills", "video_url": "https://youtu.be/b_WdZCrKr3k?si=pYe0F4bLx8FiT8HT"},
        {"course": "Banking and Finance", "caption": "Banking Systems Overview", "video_url": "https://youtu.be/fTTGALaRZoc?si=ThB2kkYTd_iIhFX1"},
        {"course": "Banking and Finance", "caption": "Financial Markets Basics", "video_url": "https://youtu.be/UOwi7MBSfhk?si=XSyvxPRp4mEQx2OH"},
        {"course": "Banking and Finance", "caption": "Loan and Credit Management", "video_url": "https://youtu.be/f3VgVOgAUoE?si=JwfSWSogIZeIMpY8"},
        {"course": "Banking and Finance", "caption": "Investment Banking Intro", "video_url": "https://youtu.be/-PkN15TtFnc?si=xgcAoZBAdge-PBjb"},
        {"course": "Banking and Finance", "caption": "Risk Management in Banking", "video_url": "https://youtu.be/BLAEuVSAlVM?si=hubXYQaexc2Iizjd"},
        {"course": "Biochemistry", "caption": "Introduction to Biochemistry", "video_url": "https://youtu.be/CHJsaq2lNjU?si=owCTFJffO4MyBtPB"},
        {"course": "Biochemistry", "caption": "Enzymes and their Functions", "video_url": "https://youtu.be/ozdO1mLXBQE?si=Xj6z5vY8rAgRMdA_"},
        {"course": "Biochemistry", "caption": "Metabolism Basics", "video_url": "https://youtu.be/onDQ9KgDSVw?si=4IKHj5VVJoahw51B"},
        {"course": "Biochemistry", "caption": "Protein Synthesis", "video_url": "https://youtu.be/8wAwLwJAGHs?si=vDuhcZbjQ0nNyhoL"},
        {"course": "Biochemistry", "caption": "Biochemical Techniques", "video_url": "https://youtu.be/lDWL_EEhReo?si=F4nhulNv3l0nxRcA"},
        {"course": "Botany", "caption": "Plant Classification", "video_url": "https://youtu.be/SAM5mcHkSxU?si=P1cX_dbg0pGJFDBB"},
        {"course": "Botany", "caption": "Photosynthesis Process", "video_url": "https://youtu.be/-ZRsLhaukn8?si=CfNMcb-tVWwq6-be"},
        {"course": "Botany", "caption": "Plant Anatomy", "video_url": "https://youtu.be/pvVvCt6Kdp8?si=3ubgF8WibXgzFLcI"},
        {"course": "Botany", "caption": "Plant Reproduction", "video_url": "https://youtu.be/h077JEQ8w6g?si=O5vHjcnuPetMLbCo"},
        {"course": "Botany", "caption": "Ecology and Environment", "video_url": "https://youtu.be/fxVGiq1kggg?si=ESD-BALtjmX0Qxcb"},
        {"course": "Zoology", "caption": "Animal Classification", "video_url": "https://example.com/videos/zoology1.mp4"},
    ]
    if course:
        matching = [r for r in all_reels if r["course"].lower() == course.lower()]
        return jsonify({"reels": matching})
    return jsonify({"reels": all_reels})


@materials_bp.route('/CBT', methods=['GET'])
@login_required
def CBT():
    """Mock Exam / CBT Practice page"""
    
    # Get username from session (custom auth)
    username = session.get('user', {}).get('username')
    if not username:
        flash('Please log in to continue.', 'error')
        return redirect(url_for('auth.login'))
    
    # Query the user from database
    user = User.query.filter_by(username=username).first()
    
    if not user:
        flash('User not found. Please log in again.', 'error')
        return redirect(url_for('auth.login'))
    
    return render_template(
        "CBT.html",
        user_dept=user.department or '',
        user_level=user.level or '',
        user_name=user.name or 'Student'
    )


@materials_bp.route('/teach-me-ai')
@login_required
def teach_me_ai():
    return render_template('teach-me-ai.html')


@materials_bp.route('/api/ai-teach')
def ai_teach():
    course = request.args.get("course")
    level  = request.args.get("level")
    if not course or not level:
        return jsonify({"error": "Missing course or level"}), 400
    prompt = f"You're a tutor. Teach a {level} student the basics of {course} in a friendly and easy-to-understand way."
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://nelavista.com",
            "X-Title": "Nelavista AI Tutor"
        }
        payload = {
            "model": "openai/gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are an educational AI assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7, "max_tokens": 800
        }
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            summary = response.json()["choices"][0]["message"]["content"]
        else:
            summary = f"Let me teach you the basics of {course}. We'll start with fundamental concepts and build up from there. This is perfect for {level} students!"
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)})
