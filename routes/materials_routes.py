import os
import time
import cloudinary
import cloudinary.uploader
import requests
from bs4 import BeautifulSoup
from flask import (Blueprint, render_template, request, jsonify, session,
                   flash, redirect, url_for)
from utils.helpers import login_required, admin_required, is_academic_book, check_profile_complete
from models import User, Material
from extensions import db
from config import OPENROUTER_API_KEY

materials_bp = Blueprint('materials', __name__)


# ===== CLOUDINARY CONFIG =====
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
    secure=True
)


# ===== ENFORCE PROFILE COMPLETION SITE-WIDE =====
@materials_bp.before_app_request
def enforce_profile_completion():
    """
    Enforce profile completion across the entire application.
    Exempts authentication, static files, PWA routes, and profile completion.
    """
    exempt_endpoints = (
        'auth.login', 'auth.logout', 'auth.signup',
        'auth.forgot_password', 'auth.reset_password',
        'dashboard.dashboard', 'dashboard.landing',
        'materials.complete_profile', 'static',
        'pwa.serve_manifest', 'pwa.serve_pwa_icons',
        'pages.about', 'pages.privacy_policy',
        'community.community_page',
        # 'Choose Your Path' must always be reachable — a brand-new signup has no profile
        # yet, so without this exemption every new account got bounced straight back to
        # /dashboard before ever seeing the picker.
        'dashboard.choose_path', 'tech.hub',
    )
    # Skills' own profile fields (faculty/department/level/semester) are Academia-specific,
    # so a student on the Skills path — and any admin managing Skills content — shouldn't
    # be redirected into the Academia dashboard just to fill them in. Matched by blueprint
    # prefix rather than one-by-one so a newly added skills.* route can't be silently
    # missed the way dashboard.choose_path was the first time this hook was extended.
    # Employer accounts have no Academia profile at all (they never see the student
    # signup form), so they're exempt entirely — this check just doesn't apply to them.
    exempt_prefixes = ('skills.', 'admin_skills.', 'employer.')

    if request.endpoint in exempt_endpoints:
        return None
    if request.endpoint and request.endpoint.startswith(exempt_prefixes):
        return None

    # Get user from session
    if 'user' not in session:
        return None

    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    if user and not check_profile_complete(user):
        # Redirect to dashboard; the modal will appear there
        return redirect(url_for('dashboard.dashboard'))


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
            course_code=course_code,
            next_topic=description if description else None,
            file_url=cloudinary_url,
            uploaded_by=author,
            source='uploaded',  # Set source as uploaded
            is_approved=False,
            # Tag with the uploader's own university so a student at a different
            # school doesn't see course-code-specific past questions/notes that
            # don't match their curriculum -- NULL (no university set) stays
            # universal, same historical behavior as before this field existed.
            university=user.university
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

        # University scoping: Material.university=NULL means universal (shown to
        # everyone). A student who has explicitly set a university OTHER than
        # Lagos State University shouldn't see LASU-specific past-questions/course
        # numbering tagged for a different school. Students with no university set
        # (the majority, historically LASU's own userbase before this field
        # existed) keep seeing everything, same as before this feature existed --
        # only an explicit "I'm at a different school" hides the mismatched content.
        username = session['user']['username']
        current_user = User.query.filter_by(username=username).first()
        if current_user and current_user.university and current_user.university != 'Lagos State University':
            query = query.filter(
                (Material.university.is_(None)) | (Material.university == current_user.university)
            )

        # Order by id descending
        results = query.order_by(Material.id.desc()).all()

        return jsonify({
            'success': True,
            'materials': [m.to_dict() for m in results]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===== DELETE MATERIAL (admin only) =====
@materials_bp.route('/api/delete-material/<int:material_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_material_api(material_id):
    try:
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
