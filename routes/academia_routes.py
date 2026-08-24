from flask import Blueprint, render_template, session, request, jsonify
from sqlalchemy import or_
from utils.helpers import login_required
from models import User, Material, CBTQuestion, CBTAttempt, Course
from services.academic_context import resolve_academic_context, find_course
from services.progress_service import get_course_materials_progress, get_cbt_summary

academia_bp = Blueprint('academia', __name__)


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
    if course:
        query = Material.query.filter(
            Material.course_code.ilike(course.code),
            Material.is_approved == True,  # noqa: E712
        )
        if user.university:
            query = query.filter((Material.university.is_(None)) | (Material.university == user.university))
        materials = query.order_by(Material.created_at.desc()).all()

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
        materials=materials, cbt_count=cbt_count, written_count=written_count,
        recent_attempts=recent_attempts, materials_viewed=materials_viewed,
        materials_total=materials_total, cbt_progress=cbt_progress,
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
