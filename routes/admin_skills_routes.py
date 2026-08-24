import re
from datetime import datetime
from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from utils.helpers import login_required, admin_required
from models import (
    SkillCategory, Skill, LearningPath, LearningPathStep, SkillCourse, CourseModule,
    Lesson, Quiz, Challenge, ChallengeSubmission, ProjectTemplate, StudentProject, StudentSkill,
    StudentOnboarding, CareerTrack, CareerTrackStep, Assignment, AssignmentSubmission,
    GradeScale, GradeWeight, Cohort, CohortEnrollment, EmployerProfile, User,
    Opportunity, OpportunityApplication,
)
from extensions import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from services.skills_service import ONBOARDING_SKIPPED
from services.youtube_service import search_youtube_videos, build_lesson_video_query
from services.ai_service import generate_lesson_content_from_video as generate_ai_lesson_content
from services.ai_service import (
    generate_curriculum, generate_daily_class_outline, generate_daily_class_day_content,
    generate_day_assignment, generate_day_test,
)
from services.daily_class_service import get_days
from services.gpa_service import DEFAULT_GRADE_SCALE, DEFAULT_GRADE_WEIGHTS

admin_skills_bp = Blueprint('admin_skills', __name__)


def _slugify(text):
    slug = re.sub(r'[^a-z0-9]+', '-', (text or '').lower()).strip('-')
    return slug or 'item'


def _unique_slug(model, base_slug, scope_filters=None):
    """Appends -2, -3, ... until the slug is unique within the given scope."""
    slug = base_slug
    n = 2
    while True:
        query = model.query.filter_by(slug=slug)
        if scope_filters:
            query = query.filter_by(**scope_filters)
        if not query.first():
            return slug
        slug = f'{base_slug}-{n}'
        n += 1


def _bad_request(msg):
    return jsonify({'success': False, 'error': msg}), 400


# ==================== PAGES ====================

@admin_skills_bp.route('/admin/skills')
@login_required
@admin_required
def admin_skills_home():
    categories = SkillCategory.query.order_by(SkillCategory.order).all()
    stats = {
        'total_skills': Skill.query.count(),
        'published_skills': Skill.query.filter_by(is_published=True).count(),
        'students_with_progress': db.session.query(StudentSkill.student_id).distinct().count(),
        'challenge_submissions': ChallengeSubmission.query.count(),
        'projects_started': StudentProject.query.count(),
        'projects_completed': StudentProject.query.filter_by(status='completed').count(),
    }

    # What students actually asked for on their first Skills visit — matched interest
    # ranks existing skills by demand; unmatched free text is what to build next.
    matched_counts = (
        db.session.query(Skill.name, Skill.slug, func.count(StudentOnboarding.id).label('n'))
        .join(StudentOnboarding, StudentOnboarding.interested_skill_id == Skill.id)
        .group_by(Skill.id).order_by(func.count(StudentOnboarding.id).desc()).all()
    )
    unmatched = (
        db.session.query(StudentOnboarding.interest_text, func.count(StudentOnboarding.id).label('n'))
        .filter(StudentOnboarding.interested_skill_id.is_(None), StudentOnboarding.interest_text != ONBOARDING_SKIPPED)
        .group_by(StudentOnboarding.interest_text).order_by(func.count(StudentOnboarding.id).desc()).limit(20).all()
    )
    demand = {'matched': matched_counts, 'unmatched': unmatched}

    return render_template('admin_skills.html', categories=categories, stats=stats, demand=demand, active_page='skills')


@admin_skills_bp.route('/admin/skills/tracks')
@login_required
@admin_required
def admin_tracks_home():
    all_tracks = CareerTrack.query.order_by(CareerTrack.order).all()
    all_skills = Skill.query.order_by(Skill.name).all()
    return render_template('admin_tracks.html', tracks=all_tracks, all_skills=all_skills, active_page='skills')


@admin_skills_bp.route('/admin/skills/<int:skill_id>')
@login_required
@admin_required
def admin_skill_editor(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    if not skill.path:
        db.session.add(LearningPath(skill_id=skill.id, title=f'{skill.name} Path'))
        db.session.commit()
    courses = skill.courses.order_by(SkillCourse.order).all()
    challenges = skill.challenges.order_by(Challenge.order).all()
    project_templates = skill.project_templates.order_by(ProjectTemplate.order).all()
    steps = skill.path.steps.order_by(LearningPathStep.order).all()
    student_count = StudentSkill.query.filter_by(skill_id=skill.id).count()
    return render_template(
        'admin_skill_editor.html', skill=skill, courses=courses, challenges=challenges,
        project_templates=project_templates, steps=steps, student_count=student_count,
        active_page='skills',
    )


# ==================== CATEGORIES ====================

@admin_skills_bp.route('/admin/api/categories', methods=['POST'])
@login_required
@admin_required
def create_category():
    data = request.get_json() or {}
    name = (data.get('name') or '').strip()
    if not name:
        return _bad_request('Name is required')
    cat = SkillCategory(
        name=name, slug=_unique_slug(SkillCategory, _slugify(name)),
        icon=(data.get('icon') or '').strip() or None,
        description=(data.get('description') or '').strip() or None,
        order=int(data.get('order') or 0),
    )
    db.session.add(cat)
    db.session.commit()
    return jsonify({'success': True, 'category': cat.to_dict()})


@admin_skills_bp.route('/admin/api/categories/<int:category_id>', methods=['PUT'])
@login_required
@admin_required
def update_category(category_id):
    cat = SkillCategory.query.get_or_404(category_id)
    data = request.get_json() or {}
    if 'name' in data:
        cat.name = data['name'].strip()
    if 'icon' in data:
        cat.icon = (data['icon'] or '').strip() or None
    if 'description' in data:
        cat.description = (data['description'] or '').strip() or None
    if 'order' in data:
        cat.order = int(data['order'] or 0)
    if 'is_active' in data:
        cat.is_active = bool(data['is_active'])
    db.session.commit()
    return jsonify({'success': True, 'category': cat.to_dict()})


@admin_skills_bp.route('/admin/api/categories/<int:category_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_category(category_id):
    cat = SkillCategory.query.get_or_404(category_id)
    if cat.skills.count():
        return _bad_request('Move or delete the skills in this category first')
    db.session.delete(cat)
    db.session.commit()
    return jsonify({'success': True})


# ==================== SKILLS ====================

@admin_skills_bp.route('/admin/api/skills', methods=['POST'])
@login_required
@admin_required
def create_skill():
    data = request.get_json() or {}
    name = (data.get('name') or '').strip()
    category_id = data.get('category_id')
    if not name or not category_id:
        return _bad_request('Name and category are required')
    skill = Skill(
        category_id=category_id, name=name, slug=_unique_slug(Skill, _slugify(name)),
        tagline=(data.get('tagline') or '').strip() or None,
        description=(data.get('description') or '').strip() or None,
        level=data.get('level') or 'beginner',
        icon=(data.get('icon') or '').strip() or None,
        color=data.get('color') or '#3b82f6',
        estimated_hours=int(data.get('estimated_hours') or 0),
        order=int(data.get('order') or 0),
    )
    db.session.add(skill)
    db.session.flush()
    db.session.add(LearningPath(skill_id=skill.id, title=f'{skill.name} Path'))
    db.session.commit()
    return jsonify({'success': True, 'skill': skill.to_dict()})


@admin_skills_bp.route('/admin/api/skills/<int:skill_id>', methods=['PUT'])
@login_required
@admin_required
def update_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    data = request.get_json() or {}
    for field in ('name', 'tagline', 'description', 'level', 'icon', 'color'):
        if field in data:
            setattr(skill, field, (data[field] or '').strip() or None if field != 'level' else (data[field] or 'beginner'))
    if 'category_id' in data:
        skill.category_id = data['category_id']
    if 'estimated_hours' in data:
        skill.estimated_hours = int(data['estimated_hours'] or 0)
    if 'order' in data:
        skill.order = int(data['order'] or 0)
    if 'is_published' in data:
        skill.is_published = bool(data['is_published'])
    db.session.commit()
    return jsonify({'success': True, 'skill': skill.to_dict()})


@admin_skills_bp.route('/admin/api/skills/<int:skill_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    try:
        db.session.delete(skill)
        db.session.commit()
        return jsonify({'success': True})
    except IntegrityError:
        db.session.rollback()
        return _bad_request('Students have progress on this skill — unpublish it instead of deleting')


@admin_skills_bp.route('/admin/api/skills/<int:skill_id>/generate-curriculum', methods=['POST'])
@login_required
@admin_required
def generate_curriculum_route(skill_id):
    """AI proposes a starter course (2 modules, 4 lessons), a challenge, and a project
    brief for this skill — created here as DRAFT rows (is_published=False on every one)
    plus matching learning-path steps. Nothing is public until the admin reviews and
    publishes each piece individually through the normal editor. Refuses on a skill that
    already has courses, so this can't silently duplicate or clutter real content."""
    skill = Skill.query.get_or_404(skill_id)
    if skill.courses.count() > 0:
        return _bad_request(
            'This skill already has courses — generate curriculum is only for a fresh, '
            'empty skill. Use the course/lesson tools below to add more.'
        )

    try:
        plan = generate_curriculum(skill.name, skill.description or skill.tagline, skill.level)
    except Exception:
        return _bad_request('AI curriculum generation failed — please try again.')

    try:
        course = SkillCourse(
            skill_id=skill.id, title=plan.get('course_title') or f'{skill.name} Fundamentals',
            slug=_unique_slug(SkillCourse, _slugify(plan.get('course_title') or skill.name), {'skill_id': skill.id}),
            description=plan.get('course_description'), level=skill.level, order=1, is_published=False,
        )
        db.session.add(course)
        db.session.flush()

        for m_order, module_data in enumerate(plan.get('modules') or [], start=1):
            module = CourseModule(course_id=course.id, title=module_data.get('title') or f'Module {m_order}', order=m_order)
            db.session.add(module)
            db.session.flush()
            for l_order, lesson_data in enumerate(module_data.get('lessons') or [], start=1):
                lesson_title = lesson_data.get('title') or f'Lesson {l_order}'
                db.session.add(Lesson(
                    module_id=module.id, title=lesson_title,
                    slug=_unique_slug(Lesson, _slugify(lesson_title), {'module_id': module.id}),
                    content=lesson_data.get('content') or '', order=l_order,
                    duration_minutes=int(lesson_data.get('duration_minutes') or 10), is_published=False,
                ))

        challenge_data = plan.get('challenge') or {}
        challenge = None
        if challenge_data.get('title'):
            challenge = Challenge(
                skill_id=skill.id, title=challenge_data['title'],
                slug=_unique_slug(Challenge, _slugify(challenge_data['title']), {'skill_id': skill.id}),
                description=challenge_data.get('description'), instructions=challenge_data.get('instructions'),
                difficulty=challenge_data.get('difficulty') or 'beginner',
                estimated_minutes=int(challenge_data.get('estimated_minutes') or 30),
                order=1, is_published=False,
            )
            db.session.add(challenge)
            db.session.flush()

        project_data = plan.get('project') or {}
        project_template = None
        if project_data.get('title'):
            project_template = ProjectTemplate(
                skill_id=skill.id, title=project_data['title'],
                slug=_unique_slug(ProjectTemplate, _slugify(project_data['title']), {'skill_id': skill.id}),
                description=project_data.get('description'),
                difficulty=project_data.get('difficulty') or 'beginner',
                estimated_hours=int(project_data.get('estimated_hours') or 4),
                order=1, is_published=False,
            )
            project_template.skills_demonstrated = project_data.get('skills_demonstrated') or [skill.name]
            db.session.add(project_template)
            db.session.flush()

        if not skill.path:
            db.session.add(LearningPath(skill_id=skill.id, title=f'{skill.name} Path'))
            db.session.flush()
        step_order = 1
        db.session.add(LearningPathStep(path_id=skill.path.id, order=step_order, step_type='course',
                                         course_id=course.id, title=course.title))
        step_order += 1
        if challenge:
            db.session.add(LearningPathStep(path_id=skill.path.id, order=step_order, step_type='challenge',
                                             challenge_id=challenge.id, title=f'Practice: {challenge.title}'))
            step_order += 1
        if project_template:
            db.session.add(LearningPathStep(path_id=skill.path.id, order=step_order, step_type='project',
                                             project_template_id=project_template.id, title=f'Build: {project_template.title}'))

        db.session.commit()
    except Exception:
        db.session.rollback()
        return _bad_request('AI returned an unusable curriculum shape — please try again.')

    return jsonify({'success': True})


# ==================== LEARNING PATH STEPS ====================

@admin_skills_bp.route('/admin/api/skills/<int:skill_id>/path-steps', methods=['POST'])
@login_required
@admin_required
def create_path_step(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    if not skill.path:
        db.session.add(LearningPath(skill_id=skill.id, title=f'{skill.name} Path'))
        db.session.flush()
    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    step_type = data.get('step_type') or 'course'
    if not title or step_type not in ('course', 'challenge', 'project'):
        return _bad_request('Title and a valid step_type are required')
    max_order = db.session.query(db.func.max(LearningPathStep.order)).filter_by(path_id=skill.path.id).scalar() or 0
    step = LearningPathStep(
        path_id=skill.path.id, order=max_order + 1, step_type=step_type, title=title,
        description=(data.get('description') or '').strip() or None,
        course_id=data.get('course_id') if step_type == 'course' else None,
        challenge_id=data.get('challenge_id') if step_type == 'challenge' else None,
        project_template_id=data.get('project_template_id') if step_type == 'project' else None,
    )
    db.session.add(step)
    db.session.commit()
    return jsonify({'success': True, 'step': step.to_dict()})


@admin_skills_bp.route('/admin/api/path-steps/<int:step_id>', methods=['PUT'])
@login_required
@admin_required
def update_path_step(step_id):
    step = LearningPathStep.query.get_or_404(step_id)
    data = request.get_json() or {}
    if 'title' in data:
        step.title = data['title'].strip()
    if 'description' in data:
        step.description = (data['description'] or '').strip() or None
    if 'order' in data:
        step.order = int(data['order'] or 0)
    db.session.commit()
    return jsonify({'success': True, 'step': step.to_dict()})


@admin_skills_bp.route('/admin/api/path-steps/<int:step_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_path_step(step_id):
    step = LearningPathStep.query.get_or_404(step_id)
    db.session.delete(step)
    db.session.commit()
    return jsonify({'success': True})


@admin_skills_bp.route('/admin/api/path-steps/reorder', methods=['POST'])
@login_required
@admin_required
def reorder_path_steps():
    data = request.get_json() or {}
    ids = data.get('order') or []
    for i, step_id in enumerate(ids):
        step = LearningPathStep.query.get(step_id)
        if step:
            step.order = i
    db.session.commit()
    return jsonify({'success': True})


# ==================== COURSES ====================

@admin_skills_bp.route('/admin/api/skills/<int:skill_id>/courses', methods=['POST'])
@login_required
@admin_required
def create_course(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    if not title:
        return _bad_request('Title is required')
    max_order = db.session.query(db.func.max(SkillCourse.order)).filter_by(skill_id=skill.id).scalar() or 0
    course = SkillCourse(
        skill_id=skill.id, title=title,
        slug=_unique_slug(SkillCourse, _slugify(title), {'skill_id': skill.id}),
        description=(data.get('description') or '').strip() or None,
        level=data.get('level') or 'beginner',
        estimated_hours=int(data.get('estimated_hours') or 0),
        order=max_order + 1,
        is_daily_class=bool(data.get('is_daily_class')),
        duration_days=int(data['duration_days']) if data.get('duration_days') else None,
    )
    db.session.add(course)
    db.session.commit()
    return jsonify({'success': True, 'course': course.to_dict()})


@admin_skills_bp.route('/admin/api/courses/<int:course_id>', methods=['PUT'])
@login_required
@admin_required
def update_course(course_id):
    course = SkillCourse.query.get_or_404(course_id)
    data = request.get_json() or {}
    if 'title' in data:
        course.title = data['title'].strip()
    if 'description' in data:
        course.description = (data['description'] or '').strip() or None
    if 'level' in data:
        course.level = data['level'] or 'beginner'
    if 'estimated_hours' in data:
        course.estimated_hours = int(data['estimated_hours'] or 0)
    if 'order' in data:
        course.order = int(data['order'] or 0)
    if 'is_published' in data:
        course.is_published = bool(data['is_published'])
    if 'is_daily_class' in data:
        course.is_daily_class = bool(data['is_daily_class'])
    if 'duration_days' in data:
        course.duration_days = int(data['duration_days']) if data['duration_days'] else None
    db.session.commit()
    return jsonify({'success': True, 'course': course.to_dict()})


@admin_skills_bp.route('/admin/api/courses/<int:course_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_course(course_id):
    course = SkillCourse.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({'success': True})


# ==================== MODULES ====================

@admin_skills_bp.route('/admin/api/courses/<int:course_id>/modules', methods=['POST'])
@login_required
@admin_required
def create_module(course_id):
    course = SkillCourse.query.get_or_404(course_id)
    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    if not title:
        return _bad_request('Title is required')
    max_order = db.session.query(db.func.max(CourseModule.order)).filter_by(course_id=course.id).scalar() or 0
    module = CourseModule(course_id=course.id, title=title, order=max_order + 1)
    db.session.add(module)
    db.session.commit()
    return jsonify({'success': True, 'module': module.to_dict()})


@admin_skills_bp.route('/admin/api/modules/<int:module_id>', methods=['PUT'])
@login_required
@admin_required
def update_module(module_id):
    module = CourseModule.query.get_or_404(module_id)
    data = request.get_json() or {}
    if 'title' in data:
        module.title = data['title'].strip()
    if 'order' in data:
        module.order = int(data['order'] or 0)
    db.session.commit()
    return jsonify({'success': True, 'module': module.to_dict()})


@admin_skills_bp.route('/admin/api/modules/<int:module_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_module(module_id):
    module = CourseModule.query.get_or_404(module_id)
    db.session.delete(module)
    db.session.commit()
    return jsonify({'success': True})


# ==================== LESSONS ====================

@admin_skills_bp.route('/admin/api/modules/<int:module_id>/lessons', methods=['POST'])
@login_required
@admin_required
def create_lesson(module_id):
    module = CourseModule.query.get_or_404(module_id)
    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    if not title:
        return _bad_request('Title is required')
    max_order = db.session.query(db.func.max(Lesson.order)).filter_by(module_id=module.id).scalar() or 0
    lesson = Lesson(
        module_id=module.id, title=title,
        slug=_unique_slug(Lesson, _slugify(title), {'module_id': module.id}),
        content=data.get('content') or '',
        video_url=(data.get('video_url') or '').strip() or None,
        duration_minutes=int(data.get('duration_minutes') or 10),
        order=max_order + 1,
    )
    lesson.resources = data.get('resources') or []
    db.session.add(lesson)
    db.session.commit()
    return jsonify({'success': True, 'lesson': lesson.to_dict()})


@admin_skills_bp.route('/admin/api/lessons/<int:lesson_id>', methods=['PUT'])
@login_required
@admin_required
def update_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    data = request.get_json() or {}
    if 'title' in data:
        lesson.title = data['title'].strip()
    if 'content' in data:
        lesson.content = data['content']
    if 'video_url' in data:
        lesson.video_url = (data['video_url'] or '').strip() or None
    if 'duration_minutes' in data:
        lesson.duration_minutes = int(data['duration_minutes'] or 10)
    if 'order' in data:
        lesson.order = int(data['order'] or 0)
    if 'resources' in data:
        lesson.resources = data['resources'] or []
    if 'is_published' in data:
        lesson.is_published = bool(data['is_published'])
    if 'learning_objective' in data:
        lesson.learning_objective = (data['learning_objective'] or '').strip() or None
    if 'day_number' in data:
        lesson.day_number = int(data['day_number']) if data['day_number'] else None
    if 'week_number' in data:
        lesson.week_number = int(data['week_number']) if data['week_number'] else None
    if 'week_title' in data:
        lesson.week_title = (data['week_title'] or '').strip() or None
    db.session.commit()
    return jsonify({'success': True, 'lesson': lesson.to_dict()})


@admin_skills_bp.route('/admin/api/lessons/<int:lesson_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    db.session.delete(lesson)
    db.session.commit()
    return jsonify({'success': True})


@admin_skills_bp.route('/admin/api/lessons/<int:lesson_id>/videos/refresh', methods=['POST'])
@login_required
@admin_required
def refresh_lesson_videos(lesson_id):
    """Force a fresh YouTube search for one lesson — for after the title changes, or when
    the auto-matched videos weren't a good fit. Normal student traffic never re-fetches
    (see skills.lesson_view), so this is the only way to update a lesson's cached videos."""
    lesson = Lesson.query.get_or_404(lesson_id)
    skill = lesson.module.course.skill
    lesson.videos = search_youtube_videos(build_lesson_video_query(skill.name, lesson.title))
    db.session.commit()
    return jsonify({'success': True, 'videos': lesson.videos})


@admin_skills_bp.route('/admin/api/lessons/<int:lesson_id>/generate-content', methods=['POST'])
@login_required
@admin_required
def generate_lesson_content(lesson_id):
    """Drafts lesson text grounded in this lesson's (first) reference video, so the
    written explanation and the video actually teach the same material — the admin still
    reviews and edits the draft in the lesson modal before saving; nothing here writes to
    the lesson itself."""
    lesson = Lesson.query.get_or_404(lesson_id)
    skill = lesson.module.course.skill

    if lesson.videos is None:
        lesson.videos = search_youtube_videos(build_lesson_video_query(skill.name, lesson.title))
        db.session.commit()

    if not lesson.videos:
        return _bad_request(
            'No reference video found for this lesson yet — try 🔄 Videos first, '
            'or a real video for this topic may not exist on YouTube.'
        )

    try:
        content = generate_ai_lesson_content(skill.name, lesson.title, lesson.videos[0])
    except Exception:
        return _bad_request('AI content generation failed — please try again.')

    return jsonify({'success': True, 'content': content, 'video': lesson.videos[0]})


@admin_skills_bp.route('/admin/api/lessons/<int:lesson_id>/quiz', methods=['PUT'])
@login_required
@admin_required
def upsert_quiz(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    data = request.get_json() or {}
    questions = data.get('questions') or []
    for q in questions:
        if not isinstance(q, dict) or 'question' not in q or 'options' not in q or 'correct_index' not in q:
            return _bad_request('Each question needs question, options, and correct_index')
    quiz = lesson.quiz
    if not quiz:
        quiz = Quiz(lesson_id=lesson.id)
        db.session.add(quiz)
    quiz.title = data.get('title') or 'Check your understanding'
    quiz.questions = questions
    db.session.commit()
    return jsonify({'success': True, 'quiz': quiz.to_dict()})


@admin_skills_bp.route('/admin/api/lessons/<int:lesson_id>/quiz', methods=['DELETE'])
@login_required
@admin_required
def delete_quiz(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    if lesson.quiz:
        db.session.delete(lesson.quiz)
        db.session.commit()
    return jsonify({'success': True})


# ==================== CHALLENGES ====================

@admin_skills_bp.route('/admin/api/skills/<int:skill_id>/challenges', methods=['POST'])
@login_required
@admin_required
def create_challenge(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    if not title:
        return _bad_request('Title is required')
    max_order = db.session.query(db.func.max(Challenge.order)).filter_by(skill_id=skill.id).scalar() or 0
    challenge = Challenge(
        skill_id=skill.id, title=title,
        slug=_unique_slug(Challenge, _slugify(title), {'skill_id': skill.id}),
        description=(data.get('description') or '').strip() or None,
        challenge_type=data.get('challenge_type') or 'coding',
        difficulty=data.get('difficulty') or 'beginner',
        instructions=data.get('instructions') or '',
        estimated_minutes=int(data.get('estimated_minutes') or 30),
        order=max_order + 1,
    )
    db.session.add(challenge)
    db.session.commit()
    return jsonify({'success': True, 'challenge': challenge.to_dict()})


@admin_skills_bp.route('/admin/api/challenges/<int:challenge_id>', methods=['PUT'])
@login_required
@admin_required
def update_challenge(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    data = request.get_json() or {}
    if 'title' in data:
        challenge.title = data['title'].strip()
    if 'description' in data:
        challenge.description = (data['description'] or '').strip() or None
    if 'challenge_type' in data:
        challenge.challenge_type = data['challenge_type'] or 'coding'
    if 'difficulty' in data:
        challenge.difficulty = data['difficulty'] or 'beginner'
    if 'instructions' in data:
        challenge.instructions = data['instructions']
    if 'estimated_minutes' in data:
        challenge.estimated_minutes = int(data['estimated_minutes'] or 30)
    if 'order' in data:
        challenge.order = int(data['order'] or 0)
    if 'is_published' in data:
        challenge.is_published = bool(data['is_published'])
    db.session.commit()
    return jsonify({'success': True, 'challenge': challenge.to_dict()})


@admin_skills_bp.route('/admin/api/challenges/<int:challenge_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_challenge(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    db.session.delete(challenge)
    db.session.commit()
    return jsonify({'success': True})


@admin_skills_bp.route('/admin/api/challenges/<int:challenge_id>/submissions')
@login_required
@admin_required
def list_challenge_submissions(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    subs = ChallengeSubmission.query.filter_by(challenge_id=challenge.id).order_by(ChallengeSubmission.created_at.desc()).all()
    return jsonify({'success': True, 'submissions': [
        {**s.to_dict(), 'student': s.student.name or s.student.username, 'content': s.content} for s in subs
    ]})


# ==================== PROJECT TEMPLATES ====================

@admin_skills_bp.route('/admin/api/skills/<int:skill_id>/projects', methods=['POST'])
@login_required
@admin_required
def create_project_template(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    if not title:
        return _bad_request('Title is required')
    max_order = db.session.query(db.func.max(ProjectTemplate.order)).filter_by(skill_id=skill.id).scalar() or 0
    template = ProjectTemplate(
        skill_id=skill.id, title=title,
        slug=_unique_slug(ProjectTemplate, _slugify(title), {'skill_id': skill.id}),
        description=(data.get('description') or '').strip() or None,
        difficulty=data.get('difficulty') or 'beginner',
        estimated_hours=int(data.get('estimated_hours') or 0),
        order=max_order + 1,
    )
    template.skills_demonstrated = data.get('skills_demonstrated') or []
    db.session.add(template)
    db.session.commit()
    return jsonify({'success': True, 'project_template': template.to_dict()})


@admin_skills_bp.route('/admin/api/projects/<int:template_id>', methods=['PUT'])
@login_required
@admin_required
def update_project_template(template_id):
    template = ProjectTemplate.query.get_or_404(template_id)
    data = request.get_json() or {}
    if 'title' in data:
        template.title = data['title'].strip()
    if 'description' in data:
        template.description = (data['description'] or '').strip() or None
    if 'difficulty' in data:
        template.difficulty = data['difficulty'] or 'beginner'
    if 'estimated_hours' in data:
        template.estimated_hours = int(data['estimated_hours'] or 0)
    if 'skills_demonstrated' in data:
        template.skills_demonstrated = data['skills_demonstrated'] or []
    if 'order' in data:
        template.order = int(data['order'] or 0)
    if 'is_published' in data:
        template.is_published = bool(data['is_published'])
    if 'rubric' in data:
        template.rubric = data['rubric'] or []
    db.session.commit()
    return jsonify({'success': True, 'project_template': template.to_dict()})


@admin_skills_bp.route('/admin/api/projects/<int:template_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_project_template(template_id):
    template = ProjectTemplate.query.get_or_404(template_id)
    db.session.delete(template)
    db.session.commit()
    return jsonify({'success': True})


# ==================== CAREER TRACKS ====================

@admin_skills_bp.route('/admin/api/tracks', methods=['POST'])
@login_required
@admin_required
def create_track():
    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    if not title:
        return _bad_request('Title is required')
    track = CareerTrack(
        title=title, slug=_unique_slug(CareerTrack, _slugify(title)),
        tagline=(data.get('tagline') or '').strip() or None,
        description=(data.get('description') or '').strip() or None,
        icon=(data.get('icon') or '').strip() or None,
        color=data.get('color') or '#3b82f6',
    )
    db.session.add(track)
    db.session.commit()
    return jsonify({'success': True, 'track': track.to_dict()})


@admin_skills_bp.route('/admin/api/tracks/<int:track_id>', methods=['PUT'])
@login_required
@admin_required
def update_track(track_id):
    track = CareerTrack.query.get_or_404(track_id)
    data = request.get_json() or {}
    if 'title' in data:
        track.title = data['title'].strip()
    if 'tagline' in data:
        track.tagline = (data['tagline'] or '').strip() or None
    if 'description' in data:
        track.description = (data['description'] or '').strip() or None
    if 'icon' in data:
        track.icon = (data['icon'] or '').strip() or None
    if 'is_published' in data:
        track.is_published = bool(data['is_published'])
    db.session.commit()
    return jsonify({'success': True, 'track': track.to_dict()})


@admin_skills_bp.route('/admin/api/tracks/<int:track_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_track(track_id):
    track = CareerTrack.query.get_or_404(track_id)
    db.session.delete(track)
    db.session.commit()
    return jsonify({'success': True})


@admin_skills_bp.route('/admin/api/tracks/<int:track_id>/steps', methods=['POST'])
@login_required
@admin_required
def add_track_step(track_id):
    track = CareerTrack.query.get_or_404(track_id)
    data = request.get_json() or {}
    skill_id = data.get('skill_id')
    skill = Skill.query.get(skill_id) if skill_id else None
    if not skill:
        return _bad_request('A valid skill is required')
    if CareerTrackStep.query.filter_by(track_id=track.id, skill_id=skill.id).first():
        return _bad_request(f'{skill.name} is already in this track')
    max_order = db.session.query(db.func.max(CareerTrackStep.order)).filter_by(track_id=track.id).scalar() or 0
    step = CareerTrackStep(
        track_id=track.id, skill_id=skill.id, order=max_order + 1,
        note=(data.get('note') or '').strip() or None,
    )
    db.session.add(step)
    db.session.commit()
    return jsonify({'success': True, 'step': step.to_dict()})


@admin_skills_bp.route('/admin/api/track-steps/<int:step_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_track_step(step_id):
    step = CareerTrackStep.query.get_or_404(step_id)
    db.session.delete(step)
    db.session.commit()
    return jsonify({'success': True})


@admin_skills_bp.route('/admin/api/track-steps/reorder', methods=['POST'])
@login_required
@admin_required
def reorder_track_steps():
    data = request.get_json() or {}
    ids = data.get('order') or []
    for i, step_id in enumerate(ids):
        step = CareerTrackStep.query.get(step_id)
        if step:
            step.order = i
    db.session.commit()
    return jsonify({'success': True})


# ==================== 30-DAY SKILL CLASSES ====================

@admin_skills_bp.route('/admin/skills/classes/<int:course_id>')
@login_required
@admin_required
def admin_class_editor(course_id):
    course = SkillCourse.query.get_or_404(course_id)
    if not course.is_daily_class:
        return redirect(url_for('admin_skills.admin_skill_editor', skill_id=course.skill_id))
    weeks = get_days(course, published_only=False)
    grade_scale = course.grade_scale.order_by(GradeScale.order).all()
    grade_weights = {w.component: w for w in course.grade_weights}
    cohorts = course.cohorts.all()
    final_template = ProjectTemplate.query.filter_by(course_id=course.id, is_final_project=True).first()
    return render_template(
        'admin_class_editor.html', course=course, skill=course.skill, weeks=weeks,
        grade_scale=grade_scale, grade_weights=grade_weights, cohorts=cohorts,
        final_template=final_template, active_page='skills',
        default_weights=DEFAULT_GRADE_WEIGHTS, default_scale=DEFAULT_GRADE_SCALE,
    )


@admin_skills_bp.route('/admin/api/courses/<int:course_id>/generate-daily-outline', methods=['POST'])
@login_required
@admin_required
def generate_daily_outline_route(course_id):
    """AI proposes the week/day skeleton for a whole daily class as DRAFT lessons (every
    lesson is_published=False) — one CourseModule per week, one Lesson per day, no
    content/video/assignment/test yet (those are generated per-day afterward, once an
    admin reviews the outline). Refuses if the course already has day-lessons, so this
    can't silently duplicate an outline."""
    course = SkillCourse.query.get_or_404(course_id)
    if not course.is_daily_class:
        return _bad_request('This course is not marked as a daily class')
    if get_days(course, published_only=False):
        return _bad_request('This class already has days — use the day tools below to add more.')

    data = request.get_json() or {}
    total_days = max(3, min(60, int(data.get('total_days') or 30)))
    level = data.get('level') or course.level or 'beginner'

    try:
        plan = generate_daily_class_outline(course.skill.name, course.title, total_days, level)
    except Exception:
        return _bad_request('AI outline generation failed — please try again.')

    try:
        for week_data in plan.get('weeks') or []:
            week_number = int(week_data.get('week_number') or 1)
            week_title = week_data.get('week_title') or f'Week {week_number}'
            module = CourseModule(course_id=course.id, title=f'Week {week_number}: {week_title}', order=week_number)
            db.session.add(module)
            db.session.flush()
            for day_data in week_data.get('days') or []:
                day_number = int(day_data.get('day_number'))
                title = day_data.get('title') or f'Day {day_number}'
                db.session.add(Lesson(
                    module_id=module.id, title=title,
                    slug=_unique_slug(Lesson, _slugify(title), {'module_id': module.id}),
                    content='', order=day_number, day_number=day_number,
                    week_number=week_number, week_title=week_title,
                    learning_objective=day_data.get('learning_objective'), is_published=False,
                ))
        if not course.duration_days:
            course.duration_days = total_days
        db.session.commit()
    except Exception:
        db.session.rollback()
        return _bad_request('AI returned an unusable outline shape — please try again.')

    return jsonify({'success': True})


@admin_skills_bp.route('/admin/api/lessons/<int:lesson_id>/generate-daily-content', methods=['POST'])
@login_required
@admin_required
def generate_daily_content_route(lesson_id):
    """Same video-grounded drafting as generate-content, but produces the structured
    daily-class format (Simple Explanation / Analogy / Step-by-Step / Common Mistakes /
    Practical Application) via generate_daily_class_day_content."""
    lesson = Lesson.query.get_or_404(lesson_id)
    skill = lesson.module.course.skill

    if lesson.videos is None:
        lesson.videos = search_youtube_videos(build_lesson_video_query(skill.name, lesson.title))
        db.session.commit()
    if not lesson.videos:
        return _bad_request('No reference video found for this day yet — try 🔄 Videos first.')

    try:
        content = generate_daily_class_day_content(
            skill.name, lesson.title, lesson.learning_objective or lesson.title, lesson.videos[0]
        )
    except Exception:
        return _bad_request('AI content generation failed — please try again.')
    return jsonify({'success': True, 'content': content, 'video': lesson.videos[0]})


@admin_skills_bp.route('/admin/api/lessons/<int:lesson_id>/day-details')
@login_required
@admin_required
def get_day_details(lesson_id):
    """Feeds the admin day-editor modal's Assignment/Test sections with whatever already
    exists for this day — the lesson's own to_dict() only carries has_assignment/has_quiz
    flags, not the actual editable content."""
    lesson = Lesson.query.get_or_404(lesson_id)
    return jsonify({
        'success': True,
        'assignment': lesson.assignment.to_dict() if lesson.assignment else None,
        'quiz_questions': lesson.quiz.questions if lesson.quiz else [],
    })


@admin_skills_bp.route('/admin/api/lessons/<int:lesson_id>/assignment', methods=['PUT'])
@login_required
@admin_required
def upsert_assignment(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    if not title:
        return _bad_request('Title is required')
    assignment = lesson.assignment
    if not assignment:
        assignment = Assignment(lesson_id=lesson.id)
        db.session.add(assignment)
    assignment.title = title
    assignment.instructions = data.get('instructions') or ''
    assignment.due_offset_hours = int(data.get('due_offset_hours') or 48)
    db.session.commit()
    return jsonify({'success': True, 'assignment': assignment.to_dict()})


@admin_skills_bp.route('/admin/api/lessons/<int:lesson_id>/assignment', methods=['DELETE'])
@login_required
@admin_required
def delete_assignment(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    if lesson.assignment:
        db.session.delete(lesson.assignment)
        db.session.commit()
    return jsonify({'success': True})


@admin_skills_bp.route('/admin/api/lessons/<int:lesson_id>/generate-assignment', methods=['POST'])
@login_required
@admin_required
def generate_assignment_route(lesson_id):
    """Drafts an assignment brief scoped to this day's actual lesson content — the admin
    reviews/edits before saving via upsert_assignment above; nothing is written here."""
    lesson = Lesson.query.get_or_404(lesson_id)
    skill = lesson.module.course.skill
    try:
        draft = generate_day_assignment(skill.name, lesson.title, lesson.learning_objective or lesson.title, lesson.content)
    except Exception:
        return _bad_request('AI assignment generation failed — please try again.')
    return jsonify({'success': True, 'assignment': draft})


@admin_skills_bp.route('/admin/api/lessons/<int:lesson_id>/generate-test', methods=['POST'])
@login_required
@admin_required
def generate_test_route(lesson_id):
    """Drafts 5-10 MCQ test questions for this day, in the same shape Quiz.questions
    already uses — the admin reviews/edits then saves through the existing
    /admin/api/lessons/<id>/quiz endpoint, so no new storage path is needed."""
    lesson = Lesson.query.get_or_404(lesson_id)
    skill = lesson.module.course.skill
    data = request.get_json() or {}
    try:
        questions = generate_day_test(
            skill.name, lesson.title, lesson.learning_objective or lesson.title, lesson.content,
            num_questions=data.get('num_questions') or 6,
        )
    except Exception:
        return _bad_request('AI test generation failed — please try again.')
    return jsonify({'success': True, 'questions': questions})


# ==================== GRADING CONFIG ====================

@admin_skills_bp.route('/admin/api/courses/<int:course_id>/grade-scale', methods=['PUT'])
@login_required
@admin_required
def set_grade_scale(course_id):
    course = SkillCourse.query.get_or_404(course_id)
    data = request.get_json() or {}
    rows = data.get('rows') or []
    for row in rows:
        if 'grade_letter' not in row or 'min_score' not in row or 'max_score' not in row or 'grade_point' not in row:
            return _bad_request('Each row needs grade_letter, min_score, max_score, grade_point')

    GradeScale.query.filter_by(course_id=course.id).delete()
    for i, row in enumerate(rows):
        db.session.add(GradeScale(
            course_id=course.id, grade_letter=row['grade_letter'].strip(),
            min_score=int(row['min_score']), max_score=int(row['max_score']),
            grade_point=float(row['grade_point']), order=i,
        ))
    db.session.commit()
    return jsonify({'success': True})


@admin_skills_bp.route('/admin/api/courses/<int:course_id>/grade-weights', methods=['PUT'])
@login_required
@admin_required
def set_grade_weights(course_id):
    course = SkillCourse.query.get_or_404(course_id)
    data = request.get_json() or {}
    weights = data.get('weights') or {}
    valid_components = {'assignments', 'tests', 'final_project', 'participation'}
    for component, pct in weights.items():
        if component not in valid_components:
            return _bad_request(f'Unknown grading component: {component}')
        row = GradeWeight.query.filter_by(course_id=course.id, component=component).first()
        if not row:
            row = GradeWeight(course_id=course.id, component=component)
            db.session.add(row)
        row.weight_pct = int(pct or 0)
    db.session.commit()
    return jsonify({'success': True})


# ==================== COHORTS ====================

@admin_skills_bp.route('/admin/api/courses/<int:course_id>/cohorts', methods=['POST'])
@login_required
@admin_required
def create_cohort(course_id):
    course = SkillCourse.query.get_or_404(course_id)
    data = request.get_json() or {}
    name = (data.get('name') or '').strip()
    if not name:
        return _bad_request('Name is required')
    try:
        start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date() if data.get('start_date') else datetime.utcnow().date()
    except ValueError:
        return _bad_request('Invalid start_date — expected YYYY-MM-DD')
    cohort = Cohort(course_id=course.id, name=name, start_date=start_date, is_active=True)
    db.session.add(cohort)
    db.session.commit()
    return jsonify({'success': True, 'cohort': cohort.to_dict()})


@admin_skills_bp.route('/admin/api/cohorts/<int:cohort_id>', methods=['PUT'])
@login_required
@admin_required
def update_cohort(cohort_id):
    cohort = Cohort.query.get_or_404(cohort_id)
    data = request.get_json() or {}
    if 'name' in data:
        cohort.name = data['name'].strip()
    if 'is_active' in data:
        cohort.is_active = bool(data['is_active'])
    db.session.commit()
    return jsonify({'success': True, 'cohort': cohort.to_dict()})


# ==================== FINAL PROJECT / RUBRIC ====================

@admin_skills_bp.route('/admin/api/courses/<int:course_id>/final-project', methods=['POST'])
@login_required
@admin_required
def create_final_project(course_id):
    course = SkillCourse.query.get_or_404(course_id)
    if ProjectTemplate.query.filter_by(course_id=course.id, is_final_project=True).first():
        return _bad_request('This class already has a final project')
    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    if not title:
        return _bad_request('Title is required')
    template = ProjectTemplate(
        skill_id=course.skill_id, course_id=course.id, is_final_project=True, title=title,
        slug=_unique_slug(ProjectTemplate, _slugify(title), {'skill_id': course.skill_id}),
        description=(data.get('description') or '').strip() or None,
        difficulty=data.get('difficulty') or 'intermediate',
        estimated_hours=int(data.get('estimated_hours') or 0),
    )
    template.rubric = data.get('rubric') or []
    db.session.add(template)
    db.session.commit()
    return jsonify({'success': True, 'project_template': template.to_dict()})


# ==================== OPPORTUNITIES (the "Earn" phase) ====================

@admin_skills_bp.route('/admin/skills/opportunities')
@login_required
@admin_required
def admin_opportunities():
    all_opportunities = Opportunity.query.order_by(Opportunity.order).all()
    all_skills = Skill.query.order_by(Skill.name).all()
    return render_template('admin_opportunities.html', opportunities=all_opportunities, all_skills=all_skills, active_page='skills')


@admin_skills_bp.route('/admin/api/opportunities', methods=['POST'])
@login_required
@admin_required
def create_opportunity():
    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    skill_id = data.get('skill_id')
    if not title or not skill_id:
        return _bad_request('Title and skill are required')
    due_date = None
    if data.get('due_date'):
        try:
            due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
        except ValueError:
            return _bad_request('Invalid due_date — expected YYYY-MM-DD')
    max_order = db.session.query(db.func.max(Opportunity.order)).scalar() or 0
    opportunity = Opportunity(
        skill_id=skill_id, title=title, description=(data.get('description') or '').strip() or None,
        location=data.get('location') or 'Remote', payment_amount=int(data.get('payment_amount') or 0),
        currency=data.get('currency') or 'NGN', due_date=due_date, order=max_order + 1,
    )
    db.session.add(opportunity)
    db.session.commit()
    return jsonify({'success': True, 'opportunity': opportunity.to_dict()})


@admin_skills_bp.route('/admin/api/opportunities/<int:opportunity_id>', methods=['PUT'])
@login_required
@admin_required
def update_opportunity(opportunity_id):
    opportunity = Opportunity.query.get_or_404(opportunity_id)
    data = request.get_json() or {}
    if 'title' in data:
        opportunity.title = data['title'].strip()
    if 'description' in data:
        opportunity.description = (data['description'] or '').strip() or None
    if 'skill_id' in data:
        opportunity.skill_id = data['skill_id']
    if 'location' in data:
        opportunity.location = data['location'] or 'Remote'
    if 'payment_amount' in data:
        opportunity.payment_amount = int(data['payment_amount'] or 0)
    if 'due_date' in data:
        if data['due_date']:
            try:
                opportunity.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
            except ValueError:
                return _bad_request('Invalid due_date — expected YYYY-MM-DD')
        else:
            opportunity.due_date = None
    if 'is_published' in data:
        opportunity.is_published = bool(data['is_published'])
    db.session.commit()
    return jsonify({'success': True, 'opportunity': opportunity.to_dict()})


@admin_skills_bp.route('/admin/api/opportunities/<int:opportunity_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_opportunity(opportunity_id):
    opportunity = Opportunity.query.get_or_404(opportunity_id)
    db.session.delete(opportunity)
    db.session.commit()
    return jsonify({'success': True})


@admin_skills_bp.route('/admin/api/opportunities/<int:opportunity_id>/applications')
@login_required
@admin_required
def list_opportunity_applications(opportunity_id):
    opportunity = Opportunity.query.get_or_404(opportunity_id)
    apps = opportunity.applications.order_by(OpportunityApplication.applied_at.desc()).all()
    return jsonify({'success': True, 'applications': [
        {**a.to_dict(), 'student_name': a.student.name or a.student.username} for a in apps
    ]})


@admin_skills_bp.route('/admin/api/opportunity-applications/<int:application_id>', methods=['PUT'])
@login_required
@admin_required
def update_opportunity_application(application_id):
    """Moves an application through applied -> accepted -> completed -> paid. Paying sets
    payout_amount and paid_at — this is the only place Earnings numbers ever come from."""
    application = OpportunityApplication.query.get_or_404(application_id)
    data = request.get_json() or {}
    status = data.get('status')
    if status not in ('applied', 'accepted', 'completed', 'paid', 'rejected'):
        return _bad_request('Invalid status')
    application.status = status
    if status == 'completed' and not application.completed_at:
        application.completed_at = datetime.utcnow()
    if status == 'paid':
        application.paid_at = datetime.utcnow()
        application.payout_amount = int(data.get('payout_amount') or application.opportunity.payment_amount or 0)
    db.session.commit()
    return jsonify({'success': True, 'application': application.to_dict()})
