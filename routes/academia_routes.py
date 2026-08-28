from flask import Blueprint, render_template, session, request, jsonify, abort
from sqlalchemy import or_
from utils.helpers import login_required
from models import User, Material, CBTQuestion, CBTAttempt, Course, Topic
from services.academic_context import resolve_academic_context, find_course
from services.progress_service import get_course_materials_progress, get_cbt_summary
from extensions import db

academia_bp = Blueprint('academia', __name__)


def _course_materials_query(course):
    """A course's approved materials, matched by the real course_id link where it
    exists and falling back to the legacy free-text course_code for rows the taxonomy
    backfill hasn't linked yet (see backfill_material_taxonomy_links.py) -- the two
    conditions never double-count a row since they describe the same Material."""
    return Material.query.filter(
        or_(Material.course_id == course.id, Material.course_code.ilike(course.code)),
        Material.is_approved == True,  # noqa: E712
    )


def _cbt_subject_prefix(course_code):
    """Strip trailing digits: 'MAT101' -> 'MAT' -- matches CBT.html's own
    createCbtSet()/createWrittenSet() regex (`code.match(/[A-Z]+/)[0]`)."""
    prefix = course_code.rstrip('0123456789')
    return prefix.upper()


@academia_bp.route('/courses/<course_code>')
@login_required
def course_detail(course_code):
    """The course's 'digital classroom' -- resolved for the logged-in student's own
    department, so the URL is stable/shareable but never shows an ambiguous
    cross-department match. If the taxonomy doesn't cover this student/code yet, the
    page still renders with an honest empty state rather than a 404."""
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()

    ctx = resolve_academic_context(user)
    course = find_course(ctx.department, course_code) if ctx.department else None

    materials = []
    topics = []
    topic_material_counts = {}
    if course:
        query = _course_materials_query(course)
        if user.university:
            query = query.filter((Material.university.is_(None)) | (Material.university == user.university))
        materials = query.order_by(Material.created_at.desc()).all()
        topics = course.topics.filter_by(is_active=True).order_by(Topic.order).all()
        # Computed from the `materials` list already fetched above -- avoids the N+1
        # pattern of a separate `t.materials.count()` query per topic in the template.
        for m in materials:
            if m.topic_id:
                topic_material_counts[m.topic_id] = topic_material_counts.get(m.topic_id, 0) + 1

    subject = _cbt_subject_prefix(course_code)
    cbt_count = CBTQuestion.query.filter_by(subject_code=subject, question_type='cbt', is_active=True).count()
    written_count = CBTQuestion.query.filter_by(subject_code=subject, question_type='written', is_active=True).count()

    recent_attempts = (
        CBTAttempt.query.filter_by(user_id=user.id, course_code=course_code.upper())
        .order_by(CBTAttempt.submitted_at.desc())
        .limit(5)
        .all()
    )

    materials_viewed = materials_total = 0
    cbt_progress = None
    if course:
        materials_viewed, materials_total = get_course_materials_progress(user, course.code)
        cbt_progress = get_cbt_summary(user, course.code)

    return render_template(
        'course_detail.html',
        user=user, ctx=ctx, course=course, course_code=course_code.upper(),
        materials=materials, topics=topics, topic_material_counts=topic_material_counts,
        cbt_count=cbt_count, written_count=written_count,
        recent_attempts=recent_attempts, materials_viewed=materials_viewed,
        materials_total=materials_total, cbt_progress=cbt_progress,
    )


@academia_bp.route('/courses/<course_code>/topics/<int:topic_id>')
@login_required
def topic_detail(course_code, topic_id):
    """The actual learning page: one topic within one course. Renders even for a topic
    that has no video yet and no student-uploaded materials yet -- the written
    explanation alone is meant to already be useful (see Topic.explanation), per the
    'a course should not feel empty just because nobody has uploaded a PDF yet' product
    principle. 404s only if the topic doesn't exist or doesn't belong to the course code
    in the URL (never leaks a topic from a course the URL didn't ask for)."""
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()

    ctx = resolve_academic_context(user)
    course = find_course(ctx.department, course_code) if ctx.department else None
    if not course:
        abort(404)

    topic = Topic.query.filter_by(id=topic_id, course_id=course.id).first()
    if not topic:
        abort(404)

    other_topics = course.topics.filter_by(is_active=True).order_by(Topic.order).all()
    topic_position = next((i for i, t in enumerate(other_topics) if t.id == topic.id), None)
    next_topic = (
        other_topics[topic_position + 1]
        if topic_position is not None and topic_position + 1 < len(other_topics) else None
    )
    prev_topic = other_topics[topic_position - 1] if topic_position else None

    materials_query = Material.query.filter(
        or_(Material.topic_id == topic.id, Material.course_code.ilike(course.code)),
        Material.is_approved == True,  # noqa: E712
    )
    if user.university:
        materials_query = materials_query.filter(
            (Material.university.is_(None)) | (Material.university == user.university)
        )
    all_course_materials = materials_query.order_by(Material.created_at.desc()).all()
    topic_materials = [m for m in all_course_materials if m.topic_id == topic.id]
    other_course_materials = [m for m in all_course_materials if m.topic_id != topic.id]

    return render_template(
        'topic_detail.html',
        user=user, ctx=ctx, course=course, topic=topic, other_topics=other_topics,
        topic_materials=topic_materials, other_course_materials=other_course_materials,
        next_topic=next_topic, prev_topic=prev_topic,
    )


@academia_bp.route('/courses')
@login_required
def browse_courses():
    """'Browse all courses' -- the escape hatch from 'My Courses' (which only shows the
    student's own current level) to their whole department's catalog across every level,
    e.g. a 200-level CS student checking what CSC courses come in 300/400 level. Grouped
    by level. Honest empty state (not a 404, not invented courses) when the taxonomy
    doesn't cover this student's university/department yet -- same convention as
    course_detail."""
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    ctx = resolve_academic_context(user)

    courses_by_level = {}
    course_topic_counts = {}
    if ctx.department:
        all_courses = (
            Course.query.filter_by(department_id=ctx.department.id)
            .order_by(Course.level, Course.code).all()
        )
        for c in all_courses:
            courses_by_level.setdefault(c.level, []).append(c)

        # One grouped query for every course's active-topic count, instead of a
        # per-course `.count()` query in the template (N+1 across a whole department's
        # course list, which can be dozens of rows).
        if all_courses:
            course_ids = [c.id for c in all_courses]
            rows = (
                db.session.query(Topic.course_id, db.func.count(Topic.id))
                .filter(Topic.course_id.in_(course_ids), Topic.is_active.is_(True))
                .group_by(Topic.course_id)
                .all()
            )
            course_topic_counts = dict(rows)

    return render_template(
        'browse_courses.html', user=user, ctx=ctx,
        courses_by_level=courses_by_level, course_topic_counts=course_topic_counts,
    )


@academia_bp.route('/search')
@login_required
def academic_search_page():
    return render_template('academic_search.html')


@academia_bp.route('/api/academic-search')
@login_required
def academic_search():
    """Search Course + Material scoped to the logged-in student's own resolved
    department/university -- never a global cross-university result set. A student
    the taxonomy doesn't cover yet gets an honest 'complete your profile' response
    rather than a silently empty/global search."""
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify({'courses': [], 'materials': [], 'resolved': False})

    ctx = resolve_academic_context(user)
    if not ctx.department:
        return jsonify({'courses': [], 'materials': [], 'resolved': False})

    like = f"%{q}%"
    courses = (
        Course.query.filter(
            Course.department_id == ctx.department.id,
            or_(Course.code.ilike(like), Course.title.ilike(like)),
        ).order_by(Course.level, Course.code).limit(20).all()
    )
    materials_query = Material.query.filter(
        Material.department == user.department,
        Material.is_approved == True,  # noqa: E712
        or_(Material.title.ilike(like), Material.description.ilike(like), Material.course_code.ilike(like)),
    )
    if user.university:
        materials_query = materials_query.filter(
            (Material.university.is_(None)) | (Material.university == user.university)
        )
    materials = materials_query.order_by(Material.created_at.desc()).limit(20).all()

    return jsonify({
        'resolved': True,
        'courses': [{'code': c.code, 'title': c.title, 'link': f"/courses/{c.code}"} for c in courses],
        'materials': [{
            'title': m.title, 'course_code': m.course_code,
            'link': f"/courses/{m.course_code}" if m.course_code else "/materials",
        } for m in materials],
    })
