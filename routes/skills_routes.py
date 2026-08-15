from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, session, flash, jsonify, request
from utils.helpers import login_required
from models import (
    User, SkillCategory, Skill, LearningPath, LearningPathStep, SkillCourse, CourseModule,
    Lesson, Quiz, Challenge, ChallengeSubmission, ProjectTemplate, StudentProject,
    StudentSkill, StudentLessonProgress, StudentQuizAttempt, StudentOnboarding,
    CareerTrack, CareerTrackStep, Assignment, AssignmentSubmission, StudentPrivacySettings,
    CohortEnrollment,
)
from extensions import db
from services.skills_service import (
    get_dashboard_data, get_path_step_states, get_course_progress, mark_lesson_complete,
    touch_skill_activity, match_skill_from_text, ONBOARDING_SKIPPED,
    get_track_step_states, get_track_progress_pct, student_has_track_activity,
)
from services.youtube_service import search_youtube_videos, build_lesson_video_query
from services.ai_service import generate_challenge_feedback, generate_assignment_feedback, evaluate_final_project
from services.daily_class_service import (
    get_or_create_enrollment, get_day_states, get_day_lesson, get_class_progress_pct,
    advance_enrollment_day, compute_assignment_due_at,
)
from services.gpa_service import compute_skill_gpa, recompute_and_cache_gpa, get_cohort_rank

EXPERIENCE_LABELS = {
    'new': "I'm completely new to this",
    'some_basics': 'I know some basics',
    'experienced': 'I already have real experience',
}
GOAL_LABELS = {
    'get_a_job': 'Get a job or internship',
    'build_projects': 'Build real projects',
    'exploring': "I'm just exploring",
    'start_a_business': 'Start something of my own',
}

skills_bp = Blueprint('skills', __name__)


def _current_user():
    return User.query.filter_by(username=session['user']['username']).first()


@skills_bp.before_request
def _ensure_session_user_exists():
    """Every Skills route calls _current_user() and assumes it's non-None. A session can
    outlive its user (account deleted by an admin while still logged in, a dev DB reset,
    etc.) — without this, that produces a 500 deep inside a route instead of a clean
    redirect. login_required (already on every route below) still handles 'not logged in
    at all'; this only covers the narrower 'logged in, but the DB row is gone' case."""
    if 'user' not in session:
        return None
    if not User.query.filter_by(username=session['user']['username']).first():
        session.clear()
        flash('Your session has expired. Please log in again.')
        return redirect(url_for('auth.login'))


# ===== FIRST-VISIT ONBOARDING =====
@skills_bp.route('/skills/onboarding', methods=['GET', 'POST'])
@login_required
def onboarding():
    """Gathers what a student wants to learn, their experience level, and their goal on
    their first visit to Skills, then routes them straight into a focused experience
    instead of a generic catalog. Reusable later (e.g. a 'change what you're learning'
    link) since it just upserts the one row per student."""
    user = _current_user()
    existing = StudentOnboarding.query.filter_by(student_id=user.id).first()

    if request.method == 'POST':
        if request.form.get('skip'):
            record = existing or StudentOnboarding(student_id=user.id)
            record.interest_text = ONBOARDING_SKIPPED
            record.interested_skill_id = None
            record.experience_level = 'new'
            record.goal = None
            if not existing:
                db.session.add(record)
            db.session.commit()
            flash("No problem — browse the catalog whenever you're ready.")
            return redirect(url_for('skills.catalog'))

        skill_id = request.form.get('skill_id', '').strip()
        interest_text = request.form.get('interest_text', '').strip()
        experience_level = request.form.get('experience_level', 'new')
        goal = request.form.get('goal', '').strip() or None

        matched_skill = None
        if skill_id:
            matched_skill = Skill.query.filter_by(id=skill_id, is_published=True).first()
            if matched_skill:
                interest_text = matched_skill.name
        if not matched_skill and interest_text:
            matched_skill = match_skill_from_text(interest_text)

        if not interest_text:
            flash('Tell us what you want to learn, or pick one from the list.')
            return redirect(url_for('skills.onboarding'))
        if experience_level not in EXPERIENCE_LABELS:
            experience_level = 'new'
        if goal not in GOAL_LABELS:
            goal = None

        record = existing or StudentOnboarding(student_id=user.id)
        record.interest_text = interest_text[:200]
        record.interested_skill_id = matched_skill.id if matched_skill else None
        record.experience_level = experience_level
        record.goal = goal
        if not existing:
            db.session.add(record)
        db.session.commit()

        if matched_skill:
            flash(f"Great — we've focused things around {matched_skill.name}.")
            return redirect(url_for('skills.skill_detail', slug=matched_skill.slug))
        flash(f'We don\'t have a full path for "{interest_text}" yet — we\'ve noted it. Here\'s what\'s closest for now.')
        return redirect(url_for('skills.catalog'))

    categories = SkillCategory.query.filter_by(is_active=True).order_by(SkillCategory.order).all()
    first_name = user.name.strip().split()[0] if user and user.name else session['user'].get('username', 'Student')
    return render_template('skills_onboarding.html', categories=categories, first_name=first_name,
                            existing=existing, experience_labels=EXPERIENCE_LABELS, goal_labels=GOAL_LABELS)


# ===== SKILLS HOME =====
@skills_bp.route('/skills')
@login_required
def home():
    user = _current_user()
    onboarding = StudentOnboarding.query.filter_by(student_id=user.id).first()
    if not onboarding:
        return redirect(url_for('skills.onboarding'))
    data = get_dashboard_data(user.id)
    categories = SkillCategory.query.filter_by(is_active=True).order_by(SkillCategory.order).all()
    first_name = user.name.strip().split()[0] if user and user.name else session['user'].get('username', 'Student')

    # Surface the student's own stated interest once, prominently — not duplicated into
    # the generic "Recommended for You" rail below it.
    started_ids = {s.skill_id for s in data['in_progress_skills']} | {s.skill_id for s in data['completed_skills']}
    spotlight_skill = None
    if onboarding.interested_skill and onboarding.interested_skill.id not in started_ids:
        spotlight_skill = onboarding.interested_skill
        data['recommended'] = [s for s in data['recommended'] if s.id != spotlight_skill.id]

    # "Your Learning Paths" — tracks with activity first, then a couple of unstarted ones
    # to explore. Capped at 4 so the home page stays a dashboard, not a full catalog.
    all_tracks = CareerTrack.query.filter_by(is_published=True).order_by(CareerTrack.order).all()
    tracks_data = [{
        'track': t, 'pct': get_track_progress_pct(user.id, t),
        'started': student_has_track_activity(user.id, t),
    } for t in all_tracks]
    tracks_data.sort(key=lambda x: not x['started'])
    tracks_data = tracks_data[:4]

    return render_template('skills_home.html', first_name=first_name, data=data, categories=categories,
                            active_page='home', ask_context='the Nelavista Skills home page',
                            onboarding=onboarding, spotlight_skill=spotlight_skill, tracks_data=tracks_data)


# ===== CATALOG =====
@skills_bp.route('/skills/catalog')
@login_required
def catalog():
    category_slug = request.args.get('category', '').strip()
    search = request.args.get('q', '').strip()
    categories = SkillCategory.query.filter_by(is_active=True).order_by(SkillCategory.order).all()

    query = Skill.query.filter_by(is_published=True)
    active_category = None
    if category_slug:
        active_category = SkillCategory.query.filter_by(slug=category_slug).first()
        if active_category:
            query = query.filter_by(category_id=active_category.id)
    if search:
        query = query.filter(Skill.name.ilike(f'%{search}%'))
    skills = query.order_by(Skill.order).all()

    return render_template('skills_catalog.html', categories=categories, skills=skills,
                            active_category=active_category, search=search, active_page='catalog')


# ===== UNIFIED SEARCH (skills, courses, lessons, challenges, projects) =====
@skills_bp.route('/skills/search')
@login_required
def search():
    q = request.args.get('q', '').strip()
    results = {'skills': [], 'courses': [], 'lessons': [], 'challenges': [], 'projects': []}

    if q:
        like = f'%{q}%'
        results['skills'] = Skill.query.filter(
            Skill.is_published.is_(True),
            db.or_(Skill.name.ilike(like), Skill.tagline.ilike(like), Skill.description.ilike(like)),
        ).order_by(Skill.order).limit(10).all()

        results['courses'] = (
            SkillCourse.query.filter(SkillCourse.is_published.is_(True), SkillCourse.title.ilike(like))
            .join(Skill, SkillCourse.skill_id == Skill.id).filter(Skill.is_published.is_(True))
            .limit(10).all()
        )

        results['lessons'] = (
            Lesson.query.join(CourseModule, Lesson.module_id == CourseModule.id)
            .join(SkillCourse, CourseModule.course_id == SkillCourse.id)
            .join(Skill, SkillCourse.skill_id == Skill.id)
            .filter(Lesson.is_published.is_(True), SkillCourse.is_published.is_(True),
                    Skill.is_published.is_(True), Lesson.title.ilike(like))
            .limit(10).all()
        )

        results['challenges'] = (
            Challenge.query.filter(Challenge.is_published.is_(True), Challenge.title.ilike(like))
            .join(Skill, Challenge.skill_id == Skill.id).filter(Skill.is_published.is_(True))
            .limit(10).all()
        )

        results['projects'] = (
            ProjectTemplate.query.filter(ProjectTemplate.is_published.is_(True), ProjectTemplate.title.ilike(like))
            .join(Skill, ProjectTemplate.skill_id == Skill.id).filter(Skill.is_published.is_(True))
            .limit(10).all()
        )

    total = sum(len(v) for v in results.values())
    return render_template('skills_search.html', q=q, results=results, total=total)


# ===== CAREER TRACKS (multi-skill paths, e.g. "AI Engineer") =====
@skills_bp.route('/skills/tracks')
@login_required
def tracks():
    user = _current_user()
    all_tracks = CareerTrack.query.filter_by(is_published=True).order_by(CareerTrack.order).all()
    tracks_data = [{
        'track': t,
        'pct': get_track_progress_pct(user.id, t),
        'started': student_has_track_activity(user.id, t),
    } for t in all_tracks]
    return render_template('skills_tracks.html', tracks_data=tracks_data, active_page='tracks')


@skills_bp.route('/skills/tracks/<slug>')
@login_required
def track_detail(slug):
    track = CareerTrack.query.filter_by(slug=slug, is_published=True).first_or_404()
    user = _current_user()
    step_states = get_track_step_states(user.id, track)
    return render_template('skills_track_detail.html', track=track, step_states=step_states,
                            pct=get_track_progress_pct(user.id, track),
                            ask_context=f'the {track.title} career track')


# ===== SKILL DETAIL (learning path + practice + projects for this skill) =====
@skills_bp.route('/skills/<slug>')
@login_required
def skill_detail(slug):
    skill = Skill.query.filter_by(slug=slug, is_published=True).first_or_404()
    user = _current_user()

    step_states = get_path_step_states(user.id, skill.path)
    student_skill = StudentSkill.query.filter_by(student_id=user.id, skill_id=skill.id).first()
    challenges = skill.challenges.filter_by(is_published=True).order_by(Challenge.order).all()
    project_templates = skill.project_templates.filter_by(is_published=True).order_by(ProjectTemplate.order).all()

    challenge_ids = [c.id for c in challenges]
    challenge_done_ids = set()
    if challenge_ids:
        done = ChallengeSubmission.query.filter(
            ChallengeSubmission.student_id == user.id, ChallengeSubmission.challenge_id.in_(challenge_ids)
        ).all()
        challenge_done_ids = {d.challenge_id for d in done}

    student_project_template_ids = {
        p.project_template_id for p in StudentProject.query.filter_by(student_id=user.id).all() if p.project_template_id
    }

    onboarding = StudentOnboarding.query.filter_by(student_id=user.id).first()
    onboarding_match = onboarding if (onboarding and onboarding.interested_skill_id == skill.id) else None

    return render_template(
        'skill_detail.html', skill=skill, step_states=step_states, student_skill=student_skill,
        challenges=challenges, project_templates=project_templates,
        challenge_done_ids=challenge_done_ids, student_project_template_ids=student_project_template_ids,
        ask_context=f'the {skill.name} skill page', onboarding_match=onboarding_match,
        experience_labels=EXPERIENCE_LABELS,
    )


# ===== COURSE VIEW (module/lesson list + progress) =====
@skills_bp.route('/skills/<skill_slug>/learn/<course_slug>')
@login_required
def course_view(skill_slug, course_slug):
    skill = Skill.query.filter_by(slug=skill_slug, is_published=True).first_or_404()
    course = SkillCourse.query.filter_by(skill_id=skill.id, slug=course_slug, is_published=True).first_or_404()
    if course.is_daily_class:
        return redirect(url_for('skills.class_overview', skill_slug=skill_slug, course_slug=course_slug))
    user = _current_user()

    modules = course.modules.order_by(CourseModule.order).all()
    completed_ids = {
        p.lesson_id for p in StudentLessonProgress.query
        .join(Lesson, StudentLessonProgress.lesson_id == Lesson.id)
        .join(CourseModule, Lesson.module_id == CourseModule.id)
        .filter(CourseModule.course_id == course.id, StudentLessonProgress.student_id == user.id).all()
    }
    completed, total, pct = get_course_progress(user.id, course)

    next_lesson = None
    for m in modules:
        for l in m.lessons.filter_by(is_published=True).order_by(Lesson.order).all():
            if l.id not in completed_ids:
                next_lesson = l
                break
        if next_lesson:
            break

    return render_template('course_view.html', skill=skill, course=course, modules=modules,
                            completed_ids=completed_ids,
                            progress={'completed': completed, 'total': total, 'pct': pct},
                            next_lesson=next_lesson, ask_context=f'the {course.title} course')


# ===== LESSON VIEW =====
@skills_bp.route('/skills/<skill_slug>/learn/<course_slug>/<lesson_slug>')
@login_required
def lesson_view(skill_slug, course_slug, lesson_slug):
    skill = Skill.query.filter_by(slug=skill_slug, is_published=True).first_or_404()
    course = SkillCourse.query.filter_by(skill_id=skill.id, slug=course_slug, is_published=True).first_or_404()
    lesson = (
        Lesson.query.join(CourseModule, Lesson.module_id == CourseModule.id)
        .filter(CourseModule.course_id == course.id, Lesson.slug == lesson_slug, Lesson.is_published.is_(True))
        .first_or_404()
    )
    if course.is_daily_class and lesson.day_number:
        return redirect(url_for('skills.day_view', skill_slug=skill_slug, course_slug=course_slug, day_number=lesson.day_number))
    user = _current_user()

    if lesson.videos is None:
        # Fetched once and cached on the lesson (shared by every student, not per-student
        # like Geeg's AI-generated courses) — search_youtube_videos already degrades to []
        # if YOUTUBE_API_KEY isn't configured, so this is safe to call unconditionally.
        lesson.videos = search_youtube_videos(build_lesson_video_query(skill.name, lesson.title))
        db.session.commit()

    all_lessons = []
    for m in course.modules.order_by(CourseModule.order).all():
        all_lessons.extend(m.lessons.filter_by(is_published=True).order_by(Lesson.order).all())
    completed_ids = {
        p.lesson_id for p in StudentLessonProgress.query.filter(
            StudentLessonProgress.student_id == user.id,
            StudentLessonProgress.lesson_id.in_([l.id for l in all_lessons]),
        ).all()
    }
    idx = next((i for i, l in enumerate(all_lessons) if l.id == lesson.id), 0)
    prev_lesson = all_lessons[idx - 1] if idx > 0 else None
    next_lesson = all_lessons[idx + 1] if idx < len(all_lessons) - 1 else None

    quiz_attempt = None
    if lesson.quiz:
        quiz_attempt = (
            StudentQuizAttempt.query.filter_by(student_id=user.id, quiz_id=lesson.quiz.id)
            .order_by(StudentQuizAttempt.completed_at.desc()).first()
        )

    # An admin-set video_url always wins the primary player slot; auto-fetched videos fill
    # it only when there isn't one, and the rest become the "more videos" strip either way.
    fetched = lesson.videos or []
    if lesson.video_url:
        primary_video, more_videos = None, fetched
    else:
        primary_video, more_videos = (fetched[0], fetched[1:]) if fetched else (None, [])

    return render_template(
        'lesson_view.html', skill=skill, course=course, lesson=lesson,
        is_completed=lesson.id in completed_ids, prev_lesson=prev_lesson, next_lesson=next_lesson,
        quiz_attempt=quiz_attempt, lessons_done=len(completed_ids), lessons_total=len(all_lessons),
        primary_video=primary_video, more_videos=more_videos,
        ask_context=f'the lesson "{lesson.title}" in {course.title}',
        ask_suggestions=['Explain this simply', 'Why does this matter?', 'Give me a practice example', 'Test me on this lesson'],
    )


def _touch_daily_class_progress(user, lesson):
    """After a lesson (in a daily class) is completed — via mark-complete or a passed
    quiz — advances the student's day frontier and refreshes their cached Skill GPA. A
    no-op for ordinary (non-daily-class) courses, so this is safe to call unconditionally
    from complete_lesson/submit_quiz below."""
    course = lesson.module.course
    if not course.is_daily_class:
        return
    enrollment = get_or_create_enrollment(user.id, course)
    advance_enrollment_day(enrollment, lesson)
    recompute_and_cache_gpa(enrollment)


@skills_bp.route('/skills/lesson/<int:lesson_id>/complete', methods=['POST'])
@login_required
def complete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    user = _current_user()
    record = mark_lesson_complete(user.id, lesson)
    _touch_daily_class_progress(user, lesson)
    return jsonify({'success': True, 'skill_progress': record.progress_pct if record else 0})


@skills_bp.route('/skills/quiz/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    user = _current_user()
    data = request.get_json() or {}
    answers = data.get('answers', [])
    questions = quiz.questions

    correct = 0
    for i, q in enumerate(questions):
        if i < len(answers) and answers[i] == q.get('correct_index'):
            correct += 1
    score = round((correct / len(questions)) * 100) if questions else 0

    attempt = StudentQuizAttempt(student_id=user.id, quiz_id=quiz.id, score=score)
    attempt.answers = answers
    db.session.add(attempt)
    db.session.commit()

    mark_lesson_complete(user.id, quiz.lesson)
    _touch_daily_class_progress(user, quiz.lesson)
    return jsonify({'success': True, 'score': score, 'correct': correct, 'total': len(questions)})


# ===== 30-DAY SKILL CLASSES =====
@skills_bp.route('/skills/<skill_slug>/class/<course_slug>')
@login_required
def class_overview(skill_slug, course_slug):
    skill = Skill.query.filter_by(slug=skill_slug, is_published=True).first_or_404()
    course = SkillCourse.query.filter_by(
        skill_id=skill.id, slug=course_slug, is_published=True, is_daily_class=True
    ).first_or_404()
    user = _current_user()
    enrollment = get_or_create_enrollment(user.id, course)

    states, weeks, all_lessons = get_day_states(course, enrollment)
    pct = get_class_progress_pct(course, enrollment)
    rank, cohort_total = get_cohort_rank(enrollment)
    gpa_data = compute_skill_gpa(enrollment)

    final_template = ProjectTemplate.query.filter_by(
        course_id=course.id, is_final_project=True, is_published=True
    ).first()
    final_project = None
    if final_template:
        final_project = StudentProject.query.filter_by(
            student_id=user.id, project_template_id=final_template.id
        ).first()

    current_day_num = min(enrollment.current_day, all_lessons[-1].day_number) if all_lessons else 1

    return render_template(
        'class_overview.html', skill=skill, course=course, enrollment=enrollment,
        weeks=weeks, states=states, pct=pct, rank=rank, cohort_total=cohort_total,
        gpa_data=gpa_data, final_template=final_template, final_project=final_project,
        current_day_num=current_day_num, total_days_count=len(all_lessons),
        ask_context=f'the {course.title} 30-day class',
    )


@skills_bp.route('/skills/<skill_slug>/class/<course_slug>/day/<int:day_number>')
@login_required
def day_view(skill_slug, course_slug, day_number):
    skill = Skill.query.filter_by(slug=skill_slug, is_published=True).first_or_404()
    course = SkillCourse.query.filter_by(
        skill_id=skill.id, slug=course_slug, is_published=True, is_daily_class=True
    ).first_or_404()
    lesson = get_day_lesson(course, day_number)
    if not lesson:
        return redirect(url_for('skills.class_overview', skill_slug=skill_slug, course_slug=course_slug))

    user = _current_user()
    enrollment = get_or_create_enrollment(user.id, course)
    states, weeks, all_lessons = get_day_states(course, enrollment)

    if states.get(day_number) == 'locked':
        flash(f"Day {day_number} isn't unlocked yet — finish Day {enrollment.current_day} first.")
        return redirect(url_for('skills.class_overview', skill_slug=skill_slug, course_slug=course_slug))

    if lesson.videos is None:
        lesson.videos = search_youtube_videos(build_lesson_video_query(skill.name, lesson.title))
        db.session.commit()
    fetched = lesson.videos or []
    if lesson.video_url:
        primary_video, more_videos = None, fetched
    else:
        primary_video, more_videos = (fetched[0], fetched[1:]) if fetched else (None, [])

    quiz_attempt = None
    if lesson.quiz:
        quiz_attempt = (
            StudentQuizAttempt.query.filter_by(student_id=user.id, quiz_id=lesson.quiz.id)
            .order_by(StudentQuizAttempt.completed_at.desc()).first()
        )

    assignment_submission = None
    due_at = None
    if lesson.assignment:
        assignment_submission = (
            AssignmentSubmission.query.filter_by(assignment_id=lesson.assignment.id, student_id=user.id)
            .order_by(AssignmentSubmission.submitted_at.desc()).first()
        )
        due_at = compute_assignment_due_at(enrollment, lesson)

    day_numbers = sorted(states.keys())
    idx = day_numbers.index(day_number) if day_number in day_numbers else 0
    prev_day = day_numbers[idx - 1] if idx > 0 else None
    next_day = day_numbers[idx + 1] if idx < len(day_numbers) - 1 else None
    next_day_locked = next_day is not None and states.get(next_day) == 'locked'

    is_completed = states.get(day_number) == 'completed'

    return render_template(
        'day_view.html', skill=skill, course=course, lesson=lesson, day_number=day_number,
        is_completed=is_completed, primary_video=primary_video, more_videos=more_videos,
        quiz_attempt=quiz_attempt, assignment_submission=assignment_submission, due_at=due_at,
        prev_day=prev_day, next_day=next_day, next_day_locked=next_day_locked,
        total_days=len(day_numbers),
        ask_context=f'Day {day_number} of {course.title}: "{lesson.title}"',
        ask_suggestions=['Explain this simply', 'Give me a real-world example', 'Test me on this', 'What should I focus on?'],
    )


@skills_bp.route('/skills/assignment/<int:assignment_id>/submit', methods=['POST'])
@login_required
def submit_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    lesson = assignment.lesson
    course = lesson.module.course
    user = _current_user()

    content = request.form.get('content', '').strip()
    if not content:
        flash('Write your submission before submitting.')
        return redirect(url_for('skills.day_view', skill_slug=course.skill.slug, course_slug=course.slug, day_number=lesson.day_number))

    enrollment = get_or_create_enrollment(user.id, course)
    due_at = compute_assignment_due_at(enrollment, lesson)

    earlier = (
        AssignmentSubmission.query.filter_by(assignment_id=assignment.id, student_id=user.id)
        .order_by(AssignmentSubmission.first_submitted_at.asc()).first()
    )
    first_submitted_at = earlier.first_submitted_at if earlier else datetime.utcnow()
    status = 'late' if (due_at and first_submitted_at > due_at) else 'submitted'

    submission = AssignmentSubmission(
        assignment_id=assignment.id, student_id=user.id, content=content,
        status=status, first_submitted_at=first_submitted_at,
    )
    db.session.add(submission)
    db.session.commit()

    try:
        feedback = generate_assignment_feedback(assignment.title, assignment.instructions, content)
        submission.feedback = feedback
        submission.score = feedback.get('score')
        submission.review_status = 'passed' if (feedback.get('score') or 0) >= 70 else 'needs_improvement'
        db.session.commit()
    except Exception:
        db.session.rollback()

    recompute_and_cache_gpa(enrollment)
    flash('Assignment submitted!')
    return redirect(url_for('skills.day_view', skill_slug=course.skill.slug, course_slug=course.slug, day_number=lesson.day_number))


# ===== PRACTICE / CHALLENGES =====
@skills_bp.route('/skills/<skill_slug>/challenge/<challenge_slug>', methods=['GET', 'POST'])
@login_required
def challenge_view(skill_slug, challenge_slug):
    skill = Skill.query.filter_by(slug=skill_slug, is_published=True).first_or_404()
    challenge = Challenge.query.filter_by(skill_id=skill.id, slug=challenge_slug, is_published=True).first_or_404()
    user = _current_user()

    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        if not content:
            flash('Write your solution before submitting.')
            return redirect(url_for('skills.challenge_view', skill_slug=skill_slug, challenge_slug=challenge_slug))
        submission = ChallengeSubmission(challenge_id=challenge.id, student_id=user.id, content=content)
        db.session.add(submission)
        db.session.commit()
        touch_skill_activity(user.id, skill.id)

        # Best-effort — a slow or failed AI call must never lose the student's actual
        # submission. "Correct ✓" alone isn't useful feedback, so we try for real
        # feedback, but the submission already stands regardless of whether this works.
        try:
            submission.feedback = generate_challenge_feedback(challenge.title, challenge.instructions, content)
            submission.status = 'reviewed'
            db.session.commit()
        except Exception:
            db.session.rollback()

        flash('Challenge submitted!')
        return redirect(url_for('skills.challenge_view', skill_slug=skill_slug, challenge_slug=challenge_slug))

    submissions = (
        ChallengeSubmission.query.filter_by(challenge_id=challenge.id, student_id=user.id)
        .order_by(ChallengeSubmission.created_at.desc()).all()
    )
    return render_template('challenge_view.html', skill=skill, challenge=challenge, submissions=submissions,
                            ask_context=f'the challenge "{challenge.title}"',
                            ask_suggestions=['Give me a hint', 'Review my approach', 'What am I missing?'])


# ===== PROJECTS =====
@skills_bp.route('/skills/projects')
@login_required
def projects():
    user = _current_user()
    my_projects = StudentProject.query.filter_by(student_id=user.id).order_by(StudentProject.updated_at.desc()).all()
    return render_template('projects.html', projects=my_projects, active_page='projects')


@skills_bp.route('/skills/projects/start/<int:template_id>', methods=['POST'])
@login_required
def start_project(template_id):
    template = ProjectTemplate.query.get_or_404(template_id)
    user = _current_user()

    existing = StudentProject.query.filter_by(student_id=user.id, project_template_id=template.id).first()
    if existing:
        return redirect(url_for('skills.project_detail', project_id=existing.id))

    project = StudentProject(
        student_id=user.id, project_template_id=template.id,
        title=template.title, description=template.description,
    )
    project.skills_demonstrated = template.skills_demonstrated
    db.session.add(project)
    db.session.commit()
    touch_skill_activity(user.id, template.skill_id)
    flash('Project started! Track your progress here as you build.')
    return redirect(url_for('skills.project_detail', project_id=project.id))


@skills_bp.route('/skills/<skill_slug>/projects/custom', methods=['POST'])
@login_required
def start_custom_project(skill_slug):
    skill = Skill.query.filter_by(slug=skill_slug, is_published=True).first_or_404()
    user = _current_user()
    title = request.form.get('title', '').strip()
    if not title:
        flash('Give your project a title first.')
        return redirect(url_for('skills.skill_detail', slug=skill_slug))

    project = StudentProject(student_id=user.id, title=title,
                              description=request.form.get('description', '').strip() or None)
    project.skills_demonstrated = [skill.name]
    db.session.add(project)
    db.session.commit()
    touch_skill_activity(user.id, skill.id)
    return redirect(url_for('skills.project_detail', project_id=project.id))


@skills_bp.route('/skills/projects/<int:project_id>')
@login_required
def project_detail(project_id):
    user = _current_user()
    project = StudentProject.query.filter_by(id=project_id, student_id=user.id).first_or_404()
    return render_template('project_detail.html', project=project, active_page='projects',
                            ask_context=f'the project "{project.title}"',
                            ask_suggestions=['Review my project', 'What should I add next?', 'Help me debug something'])


@skills_bp.route('/skills/projects/<int:project_id>/update', methods=['POST'])
@login_required
def update_project(project_id):
    user = _current_user()
    project = StudentProject.query.filter_by(id=project_id, student_id=user.id).first_or_404()
    data = request.get_json() or {}

    if 'progress_pct' in data:
        try:
            project.progress_pct = max(0, min(100, int(data['progress_pct'])))
        except (TypeError, ValueError):
            pass
    if data.get('status') in ('in_progress', 'submitted', 'completed'):
        project.status = data['status']
        if project.status == 'completed':
            project.progress_pct = 100
            project.completed_at = datetime.utcnow()
        else:
            project.completed_at = None
    if 'repo_url' in data:
        project.repo_url = (data['repo_url'] or '').strip() or None
    if 'live_url' in data:
        project.live_url = (data['live_url'] or '').strip() or None
    if 'description' in data:
        project.description = (data['description'] or '').strip() or None

    db.session.commit()

    # A final-project submission (template.is_final_project) triggers AI evaluation
    # against the admin-configured rubric — this is the only path that ever writes
    # StudentProject.rubric_scores/ai_overall_score, and it only runs once per submission
    # event (status just flipped to 'submitted'), not on every routine progress update.
    just_submitted = data.get('status') == 'submitted'
    if just_submitted and project.project_template_id and project.template and project.template.is_final_project:
        try:
            submission_details = (
                f"Description: {project.description or '(none provided)'}\n"
                f"Repository: {project.repo_url or '(none provided)'}\n"
                f"Live URL: {project.live_url or '(none provided)'}"
            )
            result = evaluate_final_project(
                project.template.rubric, project.template.title, project.template.description, submission_details
            )
            project.rubric_scores = result['criteria']
            project.ai_overall_score = result['overall_score']
            db.session.commit()
        except Exception:
            db.session.rollback()

    if project.project_template_id and project.template:
        touch_skill_activity(user.id, project.template.skill_id)
        if project.template.course_id:
            enrollment = get_or_create_enrollment(user.id, project.template.course)
            recompute_and_cache_gpa(enrollment)
    return jsonify({'success': True, 'project': project.to_dict()})


# ===== SKILL TRANSCRIPT =====
@skills_bp.route('/skills/transcript')
@login_required
def skill_transcript():
    """Aggregates every 30-Day Skill Class the student has enrolled in: Skill GPA (with
    full transparent breakdown), grade letter, cohort rank, and completion — the evidence
    page a student can point an employer to (subject to their own privacy settings, see
    StudentPrivacySettings). Never mixes in University academic CGPA — that's shown
    separately, clearly labeled self-reported/unverified, only if the student chose to add it."""
    user = _current_user()
    enrollments = CohortEnrollment.query.filter_by(student_id=user.id).order_by(CohortEnrollment.enrolled_at.desc()).all()

    rows = []
    for enrollment in enrollments:
        course = enrollment.cohort.course
        gpa_data = compute_skill_gpa(enrollment)
        rank, cohort_total = get_cohort_rank(enrollment)
        rows.append({
            'enrollment': enrollment, 'course': course, 'skill': course.skill,
            'gpa_data': gpa_data, 'rank': rank, 'cohort_total': cohort_total,
            'pct': get_class_progress_pct(course, enrollment),
        })

    overall_gpas = [r['gpa_data']['gpa'] for r in rows if r['gpa_data']['gpa'] is not None]
    overall_gpa = round(sum(overall_gpas) / len(overall_gpas), 2) if overall_gpas else None

    privacy = StudentPrivacySettings.query.filter_by(student_id=user.id).first()

    return render_template(
        'skills_transcript.html', rows=rows, overall_gpa=overall_gpa, privacy=privacy,
        active_page='transcript', ask_context='your Nelavista Skill Transcript',
    )


# ===== PRIVACY SETTINGS (what employers can see) =====
@skills_bp.route('/skills/settings', methods=['GET', 'POST'])
@login_required
def privacy_settings():
    user = _current_user()
    privacy = StudentPrivacySettings.query.filter_by(student_id=user.id).first()

    if request.method == 'POST':
        visibility = request.form.get('profile_visibility', 'private')
        if visibility not in ('private', 'employers', 'public'):
            visibility = 'private'
        if not privacy:
            privacy = StudentPrivacySettings(student_id=user.id)
            db.session.add(privacy)
        privacy.profile_visibility = visibility
        privacy.show_academic_cgpa = bool(request.form.get('show_academic_cgpa'))
        privacy.show_projects = bool(request.form.get('show_projects'))
        privacy.show_skill_transcript = bool(request.form.get('show_skill_transcript'))

        cgpa_raw = request.form.get('academic_cgpa', '').strip()
        if cgpa_raw:
            try:
                cgpa = float(cgpa_raw)
                user.academic_cgpa = max(0.0, min(5.0, cgpa))
            except ValueError:
                flash('Academic CGPA must be a number.')
        else:
            user.academic_cgpa = None

        db.session.commit()
        flash('Privacy settings saved.')
        return redirect(url_for('skills.privacy_settings'))

    return render_template('skills_settings.html', privacy=privacy, user=user, active_page='settings')
