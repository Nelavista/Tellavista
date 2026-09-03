import os
import time
from datetime import datetime
import cloudinary
import cloudinary.uploader
from flask import (Blueprint, render_template, request, jsonify, session,
                   flash, redirect, url_for)
from utils.helpers import login_required, admin_required, check_profile_complete
from models import User, Material, Course, Topic
from extensions import db
from config import OPENROUTER_API_KEY
from services.progress_service import record_material_view, get_recent_material_views
from services.academic_context import resolve_academic_context

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
    # cbt.* is exempt too: CBT.html/routes/cbt_routes.py already handle an incomplete
    # profile gracefully on their own (checking department/level specifically, showing an
    # inline "complete your profile" warning) -- without this exemption, a student with
    # a not-fully-complete Academia profile hitting a JSON endpoint like
    # /api/cbt/start mid-exam would silently get this hook's HTML redirect back instead
    # of JSON, breaking the fetch() call with no visible error.
    # settings.* is exempt for the same reason CBT is, plus a sharper one: /account/delete
    # and /account/change-password live inside routes/settings_routes.py, and both must
    # stay reachable no matter how incomplete a student's Academia profile is -- a student
    # who signs up, never finishes onboarding, and wants to delete their account can't be
    # forced through "finish your profile" first just to leave. Confirmed by testing: a
    # deliberately incomplete test account got bounced to /dashboard on every /settings
    # request, so /account/delete's own POST silently never ran (it never got past this
    # hook), even though the route itself was correct -- theme/AI Tutor/notification
    # prefs have the same no-academic-fields-required argument, so the whole blueprint is
    # exempted rather than picking apart which of its routes "need" a finished profile.
    exempt_prefixes = ('skills.', 'admin_skills.', 'employer.', 'cbt.', 'settings.')

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
        # A flash queued by an earlier, interrupted attempt at this same form (validation
        # error the student then corrected, a request that never finished loading) must
        # never bleed into this submission's own flash -- same fix already applied to
        # login()/signup() in routes/auth_routes.py, which is where this exact bug (a
        # student seeing "Profile completed successfully!" rendered twice) was traced to.
        session.pop('_flashes', None)
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


@materials_bp.route('/my-uploads')
@login_required
def my_uploads():
    """A student's own contribution history -- what P1-6 of the Academia Materials audit
    found completely missing: after uploading, a student previously had no way to see
    whether their file was pending, approved, or rejected (and why). Server-rendered
    like course_detail.html rather than a JSON+JS round trip -- there's no interaction
    here beyond viewing, so a client-side fetch would just be a slower first paint."""
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    uploads = (
        Material.query.filter_by(uploaded_by=user.username, source='uploaded')
        .order_by(Material.created_at.desc())
        .all()
    )
    return render_template('my_uploads.html', user=user, uploads=uploads)


@materials_bp.route('/api/upload-course-picker-data')
@login_required
def upload_course_picker_data():
    """Feeds the upload modal's Course dropdown from the real taxonomy, scoped to the
    student's own resolved department/level where possible -- replaces the old
    hardcoded <select> of ~13 department names mislabeled 'Course' (Academia Materials
    audit P1-3). Falls back to every course in the student's department (any level) if
    their level has none yet, so the dropdown is never empty just because a student is
    uploading a past paper for a level below their own."""
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    ctx = resolve_academic_context(user)

    courses = []
    if ctx.department:
        courses = ctx.courses or (
            Course.query.filter_by(department_id=ctx.department.id).order_by(Course.level, Course.code).all()
        )
    return jsonify({
        'resolved': bool(ctx.department),
        'courses': [{'id': c.id, 'code': c.code, 'title': c.title, 'level': c.level} for c in courses],
        'material_types': [{'value': k, 'label': v} for k, v in Material.MATERIAL_TYPE_LABELS.items()],
    })


@materials_bp.route('/api/courses/<int:course_id>/topics')
@login_required
def course_topics_for_upload(course_id):
    """The upload modal's optional Topic dropdown, populated once a course is picked."""
    course = Course.query.get_or_404(course_id)
    topics = course.topics.filter_by(is_active=True).order_by(Topic.order).all()
    return jsonify({'topics': [{'id': t.id, 'title': t.title} for t in topics]})


# ===== UPLOAD MATERIAL TO CLOUDINARY + SAVE TO DB =====
@materials_bp.route('/api/upload-material', methods=['POST'])
@login_required
def upload_material():
    try:
        username = session['user']['username']
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 401

        title         = request.form.get('title', '').strip()
        course_id_raw = request.form.get('course_id', '').strip()
        topic_id_raw  = request.form.get('topic_id', '').strip()
        material_type = request.form.get('material_type', '').strip()
        author        = request.form.get('author', '').strip()
        description   = request.form.get('description', '').strip()
        file          = request.files.get('file')

        if not all([title, course_id_raw, material_type, author]):
            return jsonify({'error': 'Title, course, material type, and your name are required'}), 400

        if material_type not in Material.MATERIAL_TYPE_LABELS:
            return jsonify({'error': 'Invalid material type'}), 400

        try:
            course = Course.query.get(int(course_id_raw))
        except ValueError:
            course = None
        if not course:
            return jsonify({'error': 'Select a real course from the list'}), 400

        topic = None
        if topic_id_raw:
            try:
                topic = Topic.query.get(int(topic_id_raw))
            except ValueError:
                topic = None
            if not topic or topic.course_id != course.id:
                return jsonify({'error': 'Selected topic does not belong to that course'}), 400

        if not file:
            return jsonify({'error': 'No file provided'}), 400

        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Only PDF files are allowed'}), 400

        # Upload to Cloudinary — 'raw' resource_type is required for PDFs
        public_id = f"nelavista_materials/{course.code}_{title[:40].replace(' ', '_')}_{int(time.time())}"
        upload_result = cloudinary.uploader.upload(
            file,
            resource_type='raw',
            public_id=public_id,
            overwrite=False,
            tags=[course.department.name, course.level, course.code]
        )

        cloudinary_url = upload_result.get('secure_url')
        if not cloudinary_url:
            return jsonify({'error': 'Upload to Cloudinary failed — no URL returned'}), 500

        # Save metadata to Material table -- course_id/topic_id/department_id are the
        # real taxonomy links; course_code/department stay populated too (denormalized)
        # so every existing string-matching read path keeps working unchanged.
        #
        # `author` (the free-typed display credit, e.g. a real name for the PDF's
        # byline) and `uploaded_by` (the actual authenticated account) are deliberately
        # different columns -- the pre-existing code conflated them (uploaded_by was set
        # from the free-text author field, and Material.author was never populated at
        # all), which silently broke "My Uploads" the moment it started filtering by
        # uploaded_by == the real username: a student who typed their own name into
        # Author (which the form encourages by prefilling it) would never see their own
        # upload again. uploaded_by must be the real session username so it stays a
        # reliable identity to filter/moderate by, independent of whatever display text
        # a student types.
        new_material = Material(
            title=title,
            department=course.department.name,
            department_id=course.department_id,
            level=course.level,
            semester=user.semester or course.semester or '',
            course_code=course.code,
            course_id=course.id,
            topic_id=topic.id if topic else None,
            material_type=material_type,
            author=author,
            description=description if description else None,
            file_url=cloudinary_url,
            uploaded_by=username,
            source='uploaded',
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
            'message': 'Material uploaded successfully and pending admin approval! Track its status on My Uploads.',
            'material': new_material.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500


# ===== FETCH MATERIALS (real, scoped, paginated) =====
@materials_bp.route('/api/fetch-materials')
@login_required
def fetch_materials():
    """The Materials library's one real data source -- scoped to the logged-in
    student's own department/level by default (never a global cross-department
    dump), with an explicit course_code for 'this course's materials', free-text q
    for in-scope search, and type for the same category pills the UI already shows.
    Paginated so a department with hundreds of materials doesn't ship them all in
    one response."""
    try:
        username = session['user']['username']
        current_user = User.query.filter_by(username=username).first()
        if not current_user:
            return jsonify({'error': 'User not found'}), 404

        course_code = request.args.get('course_code', '').strip()
        q = request.args.get('q', '').strip()
        type_filter = request.args.get('type', '').strip()
        try:
            page = max(1, int(request.args.get('page', 1)))
        except ValueError:
            page = 1
        try:
            per_page = min(30, max(1, int(request.args.get('per_page', 12))))
        except ValueError:
            per_page = 12

        query = Material.query.filter_by(is_approved=True)

        if course_code:
            query = query.filter(Material.course_code.ilike(course_code))
        else:
            # Default scope: the student's own academic context -- never every
            # material in the database. A course_code-scoped request (from a
            # course page's "View all materials") skips this since it's already
            # precise.
            #
            # Prefer the real department_id link when the taxonomy resolves this
            # student's department -- three independent free-text "department"
            # strings (User.department, Material.department, Department.name) only
            # ever agreeing by exact case-sensitive luck was a real audit finding
            # (Academia Materials audit P1-4). Falls back to the legacy string match
            # OR'd in so a material the taxonomy backfill hasn't linked yet doesn't
            # just vanish from a resolved student's own browse list.
            ctx = resolve_academic_context(current_user)
            if ctx.department:
                query = query.filter(
                    db.or_(Material.department_id == ctx.department.id, Material.department == current_user.department)
                )
            elif current_user.department:
                query = query.filter_by(department=current_user.department)
            if current_user.level:
                query = query.filter_by(level=current_user.level)

        # University scoping: Material.university=NULL means universal (shown to
        # everyone). A student who has explicitly set a university shouldn't see
        # another school's university-specific past-questions/course numbering --
        # applied uniformly for every school, LASU included (a prior version of this
        # filter special-cased LASU out of it entirely, which meant a LASU student
        # could see materials tagged for a different university; that exception is
        # removed). Students with no university set at all (the majority,
        # historically the userbase before this field existed) keep seeing
        # everything, same as before this feature existed -- only an explicit "I'm
        # at this school" narrows what's shown.
        if current_user.university:
            query = query.filter(
                (Material.university.is_(None)) | (Material.university == current_user.university)
            )

        if q:
            like = f"%{q}%"
            query = query.filter(
                (Material.title.ilike(like)) | (Material.description.ilike(like)) | (Material.course_code.ilike(like))
            )

        # `type` is now a real stored column (Material.material_type) for every row
        # created after the taxonomy migration -- filtered at the DB level. Legacy rows
        # seeded before that column existed (material_type IS NULL) are matched in
        # Python against their title-heuristic label so old material doesn't just
        # disappear from every filter pill until someone manually classifies it.
        query = query.order_by(Material.created_at.desc())
        start = (page - 1) * per_page

        if type_filter and type_filter != 'all':
            # Legacy rows seeded before Material.material_type existed (NULL) are matched
            # against a Python title-heuristic (_legacy_inferred_type_label) that can't be
            # expressed in SQL, so this branch has to load every DB-level-matching row
            # before it can know the true filtered set/page -- unavoidable without a
            # one-time backfill of every legacy row's material_type (a separate, larger
            # change). Only this branch pays that cost; the far more common "browse
            # everything" / no-type-filter path below doesn't.
            query = query.filter(
                db.or_(Material.material_type == type_filter, Material.material_type.is_(None))
            )
            results = query.all()
            target_label = Material.MATERIAL_TYPE_LABELS.get(type_filter, type_filter)
            results = [
                m for m in results
                if m.material_type == type_filter
                or (m.material_type is None and m._legacy_inferred_type_label() == target_label)
            ]
            total = len(results)
            page_results = results[start:start + per_page]
        else:
            # Real DB-level pagination -- previously this branch also ran the .all() +
            # Python-slice above, loading and serializing every matching row on every
            # request just to throw all but `per_page` of them away. Materials is scoped
            # per-department/level so this was fine at today's per-department counts, but
            # scales linearly with content, not with what's actually shown.
            total = query.order_by(None).count()
            page_results = query.offset(start).limit(per_page).all()

        return jsonify({
            'success': True,
            'materials': [m.to_dict() for m in page_results],
            'page': page,
            'per_page': per_page,
            'total': total,
            'has_more': start + per_page < total,
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def _time_ago(dt):
    if not dt:
        return ''
    seconds = (datetime.utcnow() - dt).total_seconds()
    if seconds < 60:
        return 'just now'
    if seconds < 3600:
        return f"{int(seconds // 60)}m ago"
    if seconds < 86400:
        return f"{int(seconds // 3600)}h ago"
    return f"{int(seconds // 86400)}d ago"


def _material_link(material):
    """Where 'open this material again' should send a student -- its exact topic page
    when linked to one (that's where the material is actually shown), else its course's
    digital classroom when it has a course code, else the general library."""
    if material.topic_id and material.course_code:
        return f"/courses/{material.course_code}/topics/{material.topic_id}"
    return f"/courses/{material.course_code}" if material.course_code else "/materials"


# ===== MATERIAL VIEW TRACKING (real per-student progress) =====
@materials_bp.route('/api/materials/<int:material_id>/view', methods=['POST'])
@login_required
def track_material_view(material_id):
    """Fire-and-forget, called when a student actually opens a material -- powers
    Continue Studying / Recent Materials / progress counts. A failure here must never
    block the student from reading the material they already opened."""
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    material = Material.query.get(material_id)
    if not user or not material:
        return jsonify({'success': False}), 404
    record_material_view(user, material)
    return jsonify({'success': True})


@materials_bp.route('/api/continue-studying')
@login_required
def continue_studying():
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    views = get_recent_material_views(user, limit=1)
    if not views:
        return jsonify({'material': None})
    v = views[0]
    m = v.material
    return jsonify({'material': {
        'title': m.title, 'course_code': m.course_code, 'department': m.department,
        'link': _material_link(m), 'viewed_ago': _time_ago(v.viewed_at),
    }})


@materials_bp.route('/api/recent-materials')
@login_required
def recent_materials():
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    views = get_recent_material_views(user, limit=5)
    return jsonify({'materials': [{
        'title': v.material.title, 'course_code': v.material.course_code,
        'department': v.material.department, 'link': _material_link(v.material),
        'viewed_ago': _time_ago(v.viewed_at),
    } for v in views]})


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


# Removed (Level 1 cleanup pass): /api/materials and /ai/materials were unauthenticated
# routes that scraped pdfdrive.com/openlibrary.org live on every request -- confirmed
# unreferenced by any template or static JS file, and not part of the live materials
# flow (which is /api/fetch-materials above, scoped to the student's own department/
# level/university and backed by the real Material table). Pure unscoped, unauthenticated
# attack surface with no user-facing value.
