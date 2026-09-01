from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from sqlalchemy.exc import IntegrityError
from utils.helpers import login_required, admin_required
from models import University, Faculty, Department, Course, Topic, Material, TopicProgress, TutorConversation
from extensions import db
from services.ai_service import generate_course_topics, generate_topic_explanation
from services.youtube_service import search_youtube_videos, build_topic_video_query

admin_academia_bp = Blueprint('admin_academia', __name__)


def _bad_request(msg):
    # Same pattern as routes/admin_skills_routes.py's own _bad_request -- a friendly,
    # actionable 400 instead of an unhandled IntegrityError -> 500 (see delete_course()/
    # delete_topic() below, neither of which had this before).
    return jsonify({'success': False, 'error': msg}), 400


@admin_academia_bp.route('/admin/academia')
@login_required
@admin_required
def admin_academia_home():
    universities = University.query.order_by(University.name).all()
    return render_template('admin_academia.html', universities=universities, active_page='academia')


@admin_academia_bp.route('/admin/academia/universities/new', methods=['POST'])
@login_required
@admin_required
def new_university():
    name = (request.form.get('name') or '').strip()
    short_name = (request.form.get('short_name') or '').strip() or None
    if not name:
        return jsonify({'success': False, 'error': 'University name is required'}), 400
    if University.query.filter_by(name=name).first():
        return jsonify({'success': False, 'error': 'That university already exists'}), 409
    uni = University(name=name, short_name=short_name)
    db.session.add(uni)
    db.session.commit()
    return jsonify({'success': True, 'university': uni.to_dict()})


@admin_academia_bp.route('/admin/academia/faculties/new', methods=['POST'])
@login_required
@admin_required
def new_faculty():
    university_id = request.form.get('university_id', type=int)
    name = (request.form.get('name') or '').strip()
    if not university_id or not name:
        return jsonify({'success': False, 'error': 'University and faculty name are required'}), 400
    if Faculty.query.filter_by(university_id=university_id, name=name).first():
        return jsonify({'success': False, 'error': 'That faculty already exists at this university'}), 409
    fac = Faculty(university_id=university_id, name=name)
    db.session.add(fac)
    db.session.commit()
    return jsonify({'success': True, 'faculty': fac.to_dict()})


@admin_academia_bp.route('/admin/academia/departments/new', methods=['POST'])
@login_required
@admin_required
def new_department():
    faculty_id = request.form.get('faculty_id', type=int)
    name = (request.form.get('name') or '').strip()
    if not faculty_id or not name:
        return jsonify({'success': False, 'error': 'Faculty and department name are required'}), 400
    if Department.query.filter_by(faculty_id=faculty_id, name=name).first():
        return jsonify({'success': False, 'error': 'That department already exists in this faculty'}), 409
    dept = Department(faculty_id=faculty_id, name=name)
    db.session.add(dept)
    db.session.commit()
    return jsonify({'success': True, 'department': dept.to_dict()})


@admin_academia_bp.route('/admin/academia/departments/<int:department_id>')
@login_required
@admin_required
def admin_academia_department(department_id):
    department = Department.query.get_or_404(department_id)
    courses = Course.query.filter_by(department_id=department.id).order_by(Course.level, Course.code).all()
    return render_template(
        'admin_academia_department.html', department=department, courses=courses, active_page='academia'
    )


@admin_academia_bp.route('/admin/academia/courses/new', methods=['POST'])
@login_required
@admin_required
def new_course():
    department_id = request.form.get('department_id', type=int)
    code = (request.form.get('code') or '').strip().upper()
    title = (request.form.get('title') or '').strip()
    level = (request.form.get('level') or '').strip()
    semester = (request.form.get('semester') or '').strip() or None
    course_type = (request.form.get('course_type') or '').strip() or None
    description = (request.form.get('description') or '').strip() or None
    if not (department_id and code and title and level):
        return jsonify({'success': False, 'error': 'Department, code, title and level are required'}), 400
    if Course.query.filter_by(department_id=department_id, level=level, code=code).first():
        return jsonify({'success': False, 'error': 'That course code already exists at this level/department'}), 409
    course = Course(
        department_id=department_id, code=code, title=title, level=level,
        semester=semester, course_type=course_type, description=description,
    )
    db.session.add(course)
    db.session.commit()
    return jsonify({'success': True, 'course': course.to_dict()})


@admin_academia_bp.route('/admin/academia/courses/<int:course_id>/edit', methods=['POST'])
@login_required
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    for field in ('code', 'title', 'level', 'semester', 'course_type', 'description'):
        if field in request.form:
            value = request.form[field].strip()
            if field == 'code':
                value = value.upper()
            setattr(course, field, value or None if field in ('semester', 'course_type', 'description') else value)
    db.session.commit()
    return jsonify({'success': True, 'course': course.to_dict()})


@admin_academia_bp.route('/admin/academia/courses/<int:course_id>/delete', methods=['DELETE'])
@login_required
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    # Material.course_id references this course with a backref (Course.materials), is
    # nullable, and carries no cascade -- SQLAlchemy's default behavior is to silently
    # set Material.course_id back to NULL and let the delete through rather than raise
    # anything, which would detach real materials from their course instead of refusing
    # the delete. TutorConversation.course_id is nullable with no backref either way, so
    # it wouldn't be nullified or raise anything here either -- check both explicitly.
    # (Topic.course_id is nullable=False and already correctly ORM-cascaded via
    # Course.topics' cascade='all, delete-orphan' -- deleting topics along with their
    # course is intended, not guarded against here.)
    if Material.query.filter_by(course_id=course.id).first() or TutorConversation.query.filter_by(course_id=course.id).first():
        return _bad_request('Materials or tutor conversations are linked to this course — remove or reassign them first')
    try:
        db.session.delete(course)
        db.session.commit()
        return jsonify({'success': True})
    except IntegrityError:
        db.session.rollback()
        return _bad_request('This course is still referenced elsewhere and cannot be deleted')


# ============================================================
# ===== COURSE CONTENT: Topics, AI-assisted drafting, YouTube =====
# The content pipeline for the "course code should never feel empty" product
# principle -- a course's description + topic list + per-topic explanation/video are
# generated as a draft here, reviewed/edited by an admin, and only then persisted as
# real Topic rows. Nothing here auto-publishes to students without an admin having
# looked at it at least once (content_source stays 'ai_draft' until edited/approved).
# ============================================================

@admin_academia_bp.route('/admin/academia/courses/<int:course_id>')
@login_required
@admin_required
def admin_academia_course(course_id):
    course = Course.query.get_or_404(course_id)
    topics = course.topics.order_by(Topic.order).all()
    return render_template(
        'admin_academia_course.html', course=course, topics=topics, active_page='academia'
    )


@admin_academia_bp.route('/admin/academia/courses/<int:course_id>/generate-content', methods=['POST'])
@login_required
@admin_required
def generate_course_content(course_id):
    """Drafts a description + ordered topic titles for this course. Returns the draft
    for the admin UI to show for review/editing -- writes nothing until the admin hits
    apply-topics below."""
    course = Course.query.get_or_404(course_id)
    try:
        draft = generate_course_topics(
            course.code, course.title, course.department.name, course.level,
            existing_description=course.description,
        )
    except Exception:
        return jsonify({'success': False, 'error': 'AI content generation failed -- please try again.'}), 502
    return jsonify({'success': True, 'draft': draft})


@admin_academia_bp.route('/admin/academia/courses/<int:course_id>/apply-topics', methods=['POST'])
@login_required
@admin_required
def apply_course_topics(course_id):
    """Persists a reviewed draft: sets Course.description (if provided and the course
    doesn't already have one an admin wrote by hand -- never silently overwrites
    existing content) and creates one Topic row per title, in order, after the
    course's current topics. Each new Topic starts as content_source='ai_draft' with no
    explanation yet -- an admin fills those in per-topic afterward (or a student sees a
    topic with a title but no explanation yet, which is still more useful than nothing)."""
    course = Course.query.get_or_404(course_id)
    data = request.get_json(silent=True) or {}
    description = (data.get('description') or '').strip()
    topic_titles = [t.strip() for t in (data.get('topics') or []) if isinstance(t, str) and t.strip()]

    if description and not course.description:
        course.description = description

    next_order = (db.session.query(db.func.coalesce(db.func.max(Topic.order), -1))
                  .filter(Topic.course_id == course.id).scalar()) + 1
    created = []
    for i, title in enumerate(topic_titles):
        topic = Topic(course_id=course.id, title=title, order=next_order + i, content_source='ai_draft')
        db.session.add(topic)
        created.append(topic)
    db.session.commit()
    return jsonify({'success': True, 'topics': [t.to_dict() for t in created], 'course': course.to_dict()})


@admin_academia_bp.route('/admin/academia/courses/<int:course_id>/topics/new', methods=['POST'])
@login_required
@admin_required
def new_topic(course_id):
    course = Course.query.get_or_404(course_id)
    title = (request.form.get('title') or '').strip()
    if not title:
        return jsonify({'success': False, 'error': 'Topic title is required'}), 400
    next_order = (db.session.query(db.func.coalesce(db.func.max(Topic.order), -1))
                  .filter(Topic.course_id == course.id).scalar()) + 1
    topic = Topic(course_id=course.id, title=title, order=next_order, content_source='manual')
    db.session.add(topic)
    db.session.commit()
    return jsonify({'success': True, 'topic': topic.to_dict()})


@admin_academia_bp.route('/admin/academia/topics/<int:topic_id>/edit', methods=['POST'])
@login_required
@admin_required
def edit_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    if 'title' in request.form:
        title = request.form['title'].strip()
        if title:
            topic.title = title
    if 'order' in request.form:
        try:
            topic.order = int(request.form['order'])
        except (TypeError, ValueError):
            pass
    if 'explanation' in request.form:
        topic.explanation = request.form['explanation'].strip() or None
        # An admin who hand-edits the explanation has effectively reviewed it, even if
        # it started life as an AI draft -- content_source now reflects reality.
        topic.content_source = 'reviewed'
    if 'video_url' in request.form:
        topic.video_url = request.form['video_url'].strip() or None
    if 'is_active' in request.form:
        topic.is_active = request.form['is_active'] in ('1', 'true', 'on', 'yes')
    db.session.commit()
    return jsonify({'success': True, 'topic': topic.to_dict()})


@admin_academia_bp.route('/admin/academia/topics/<int:topic_id>/delete', methods=['DELETE'])
@login_required
@admin_required
def delete_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    # Material.topic_id is nullable with a backref (Topic.materials) -- same silent-
    # nullify trap as delete_course() above, so an except IntegrityError alone would
    # never fire for it. TopicProgress.topic_id is nullable=False (a real IntegrityError
    # would fire, but checking explicitly keeps this route's behavior consistent and
    # DB-agnostic rather than depending on the exact FK-enforcement/ORM-relationship
    # interaction). TutorConversation.topic_id is nullable with no backref either way.
    # Topic.is_active already exists for exactly this ("publish/hide without deleting"
    # per its own model comment) and is already toggleable from this same admin UI.
    if (Material.query.filter_by(topic_id=topic.id).first()
            or TopicProgress.query.filter_by(topic_id=topic.id).first()
            or TutorConversation.query.filter_by(topic_id=topic.id).first()):
        return _bad_request('Students have progress on this topic, or materials/conversations are linked to it — hide it instead of deleting')
    try:
        db.session.delete(topic)
        db.session.commit()
        return jsonify({'success': True})
    except IntegrityError:
        db.session.rollback()
        return _bad_request('This topic is still referenced elsewhere and cannot be deleted')


@admin_academia_bp.route('/admin/academia/topics/<int:topic_id>/videos', methods=['POST'])
@login_required
@admin_required
def refresh_topic_videos(topic_id):
    """Searches YouTube once and caches the results on the topic (same convention as
    admin_skills_routes.py's refresh_lesson_videos) -- a student page never triggers this
    itself, so the API is called at most once per admin refresh, not per student view."""
    topic = Topic.query.get_or_404(topic_id)
    course = topic.course
    query = build_topic_video_query(course.code, course.title, topic.title)
    result = search_youtube_videos(query)
    if result is None:
        return jsonify({'success': False, 'error': 'YouTube search is unavailable right now (quota or network) -- try again later.'}), 502
    topic.videos = result
    db.session.commit()
    return jsonify({'success': True, 'videos': topic.videos})


@admin_academia_bp.route('/admin/academia/topics/<int:topic_id>/generate-explanation', methods=['POST'])
@login_required
@admin_required
def generate_topic_explanation_draft(topic_id):
    """Drafts this topic's written explanation, anchored to its cached video if one
    exists. Returns the draft for the admin to review in the topic editor -- saving it
    to Topic.explanation happens through the normal edit_topic endpoint above, so
    nothing is written here."""
    topic = Topic.query.get_or_404(topic_id)
    course = topic.course
    if topic.videos is None:
        result = search_youtube_videos(build_topic_video_query(course.code, course.title, topic.title))
        if result is not None:
            topic.videos = result
            db.session.commit()
    video = topic.videos[0] if topic.videos else None
    try:
        content = generate_topic_explanation(course.code, course.title, topic.title, video=video)
    except Exception:
        return jsonify({'success': False, 'error': 'AI content generation failed -- please try again.'}), 502
    return jsonify({'success': True, 'content': content, 'video': video})


@admin_academia_bp.route('/admin/academia/videos/missing')
@login_required
@admin_required
def missing_videos_queue():
    """Fast one-at-a-time queue for manually pinning a video on topics the auto-search
    pipeline couldn't fill (quota exhausted, or a genuine no-match) -- sidesteps YouTube's
    search.list quota entirely, since pasting a URL costs zero API calls. Saves through
    the existing edit_topic endpoint (video_url), so no new write path is introduced.
    `after_id` moves the cursor forward without server-side session state -- both "Skip"
    and "Save & Next" just link/redirect to the next topic id past the current one."""
    after_id = request.args.get('after_id', type=int) or 0

    no_video = db.or_(Topic.video_url.is_(None), Topic.video_url == '')
    no_cached_search = db.or_(Topic.videos_json.is_(None), Topic.videos_json == '[]')

    base_query = Topic.query.join(Course).filter(
        Topic.is_active == True, no_video, no_cached_search,  # noqa: E712
    )
    remaining = base_query.filter(Topic.id > after_id).count()
    topic = base_query.filter(Topic.id > after_id).order_by(Topic.id).first()

    return render_template(
        'admin_missing_videos_queue.html', topic=topic, remaining=remaining,
        query=build_topic_video_query(topic.course.code, topic.course.title, topic.title) if topic else None,
        active_page='academia',
    )
