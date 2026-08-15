"""Progress computation for the Skills system.

Nothing here stores progress incrementally — every percentage is recomputed from the
underlying completion rows (StudentLessonProgress, ChallengeSubmission, StudentProject)
each time it's needed, then written back to the StudentSkill cache row. That means the
cache can never drift out of sync with reality: if it's ever wrong, the next read fixes it.
"""
from datetime import datetime, timedelta
from extensions import db
from models import (
    Skill, SkillCourse, CourseModule, Lesson, LearningPathStep,
    StudentLessonProgress, StudentSkill, ChallengeSubmission, StudentProject,
    CareerTrackStep,
)

# Stored as StudentOnboarding.interest_text when a student explicitly skips the
# "what do you want to learn" question, so a completed-but-empty onboarding is
# distinguishable from one that hasn't happened yet (no row at all).
ONBOARDING_SKIPPED = '(skipped)'

# Free-text -> skill-slug hints for onboarding matching, covering how students actually
# phrase interests rather than requiring them to type a catalog skill's exact name.
_ONBOARDING_KEYWORDS = {
    'web development': 'web-development', 'web dev': 'web-development', 'website': 'web-development',
    'frontend': 'web-development', 'front-end': 'web-development', 'front end': 'web-development',
    'backend': 'web-development', 'back-end': 'web-development', 'full stack': 'web-development',
    'html': 'web-development', 'css': 'web-development', 'javascript': 'web-development',
    'python': 'python', 'coding': 'python', 'programming': 'python', 'software development': 'python',
    'software engineering': 'python', 'app development': 'python', 'developer': 'python',
    'design': 'ui-ux-design', 'ui': 'ui-ux-design', 'ux': 'ui-ux-design', 'product design': 'ui-ux-design',
    'graphic design': 'ui-ux-design', 'figma': 'ui-ux-design',
    'marketing': 'digital-marketing', 'social media': 'digital-marketing', 'seo': 'digital-marketing',
    'content': 'content-creation', 'video editing': 'content-creation', 'video': 'content-creation',
    'copywriting': 'content-creation', 'writing': 'content-creation', 'youtube': 'content-creation',
    'cv': 'cv-interview-prep', 'resume': 'cv-interview-prep', 'interview': 'cv-interview-prep',
    'linkedin': 'cv-interview-prep', 'career': 'cv-interview-prep',
}


def match_skill_from_text(text):
    """Best-effort match of a student's own words to a published catalog Skill. Tries an
    exact/substring name match first, then falls back to a curated keyword map, so 'I want
    to learn to build websites' still resolves to Web Development. Returns None (not an
    error) when nothing fits — the caller decides how to handle an unmet request."""
    text_lower = (text or '').strip().lower()
    if not text_lower:
        return None

    published = Skill.query.filter_by(is_published=True).all()
    for s in published:
        if s.name.lower() == text_lower:
            return s
    for s in published:
        if s.name.lower() in text_lower or text_lower in s.name.lower():
            return s
    for keyword, slug in _ONBOARDING_KEYWORDS.items():
        if keyword in text_lower:
            match = Skill.query.filter_by(slug=slug, is_published=True).first()
            if match:
                return match
    return None


def _lesson_ids_for_course(course_id):
    module_ids = [m.id for m in CourseModule.query.filter_by(course_id=course_id).all()]
    if not module_ids:
        return []
    return [l.id for l in Lesson.query.filter(Lesson.module_id.in_(module_ids), Lesson.is_published.is_(True)).all()]


def get_course_progress(student_id, course):
    """Returns (completed_count, total_count, pct) for one student on one SkillCourse."""
    lesson_ids = _lesson_ids_for_course(course.id)
    total = len(lesson_ids)
    if total == 0:
        return 0, 0, 0
    completed = StudentLessonProgress.query.filter(
        StudentLessonProgress.student_id == student_id,
        StudentLessonProgress.lesson_id.in_(lesson_ids),
    ).count()
    pct = round((completed / total) * 100)
    return completed, total, pct


def is_step_complete(student_id, step):
    """A path step is complete when its underlying content is fully done, regardless of
    step_type — course steps need every lesson done, challenge/project steps need one
    real submission/completion."""
    if step.step_type == 'course' and step.course_id:
        completed, total, _ = get_course_progress(student_id, step.course)
        return total > 0 and completed == total
    if step.step_type == 'challenge' and step.challenge_id:
        return ChallengeSubmission.query.filter_by(student_id=student_id, challenge_id=step.challenge_id).first() is not None
    if step.step_type == 'project' and step.project_template_id:
        return StudentProject.query.filter_by(
            student_id=student_id, project_template_id=step.project_template_id, status='completed'
        ).first() is not None
    return False


def get_path_step_states(student_id, path):
    """Returns an ordered list of {step, state} where state is 'completed', 'current', or
    'locked'. The first not-yet-complete step is 'current'; everything after it is
    'locked' — so a student always knows exactly where they are (spec requirement)."""
    steps = path.steps.all() if path else []
    result = []
    found_current = False
    for step in steps:
        done = is_step_complete(student_id, step)
        if done:
            state = 'completed'
        elif not found_current:
            state = 'current'
            found_current = True
        else:
            state = 'locked'
        result.append({'step': step, 'state': state})
    return result


def get_track_step_states(student_id, track):
    """Same completed/current/locked shape as get_path_step_states, but one level up: each
    step here is a whole Skill, and 'complete' means the student's StudentSkill for that
    skill has status == 'completed' (i.e. every published course in it is fully done)."""
    steps = track.steps.all() if track else []
    completed_skill_ids = {
        s.skill_id for s in StudentSkill.query.filter_by(student_id=student_id, status='completed').all()
    }
    result = []
    found_current = False
    for step in steps:
        done = step.skill_id in completed_skill_ids
        if done:
            state = 'completed'
        elif not found_current:
            state = 'current'
            found_current = True
        else:
            state = 'locked'
        result.append({'step': step, 'state': state})
    return result


def get_track_progress_pct(student_id, track):
    """Rough completion percentage for a track, used for the 'Your Learning Paths' cards
    on the Skills home — how many of its skills the student has actually completed."""
    steps = track.steps.all() if track else []
    if not steps:
        return 0
    completed_skill_ids = {
        s.skill_id for s in StudentSkill.query.filter_by(student_id=student_id, status='completed').all()
    }
    done = sum(1 for s in steps if s.skill_id in completed_skill_ids)
    return round((done / len(steps)) * 100)


def student_has_track_activity(student_id, track):
    """Whether the student has touched ANY skill in this track — used to decide whether a
    track shows in 'Continue' vs 'Explore' on the Skills home."""
    skill_ids = [s.skill_id for s in track.steps.all()]
    if not skill_ids:
        return False
    return StudentSkill.query.filter(
        StudentSkill.student_id == student_id, StudentSkill.skill_id.in_(skill_ids)
    ).first() is not None


def recompute_student_skill(student_id, skill_id):
    """Recalculates and persists a student's overall progress on one skill, from every
    published course's lesson completions. Called after any lesson/challenge/project
    activity so the skill profile and dashboard never show stale numbers."""
    skill = Skill.query.get(skill_id)
    if not skill:
        return None

    courses = skill.courses.filter_by(is_published=True).all()
    total_lessons = 0
    completed_lessons = 0
    for course in courses:
        c, t, _ = get_course_progress(student_id, course)
        completed_lessons += c
        total_lessons += t

    pct = round((completed_lessons / total_lessons) * 100) if total_lessons else 0

    record = StudentSkill.query.filter_by(student_id=student_id, skill_id=skill_id).first()
    if not record:
        if completed_lessons == 0:
            return None  # don't create a tracking row until the student has actually started
        record = StudentSkill(student_id=student_id, skill_id=skill_id, started_at=datetime.utcnow())
        db.session.add(record)

    record.progress_pct = pct
    record.last_activity_at = datetime.utcnow()
    if pct >= 100 and total_lessons > 0:
        record.status = 'completed'
        if not record.completed_at:
            record.completed_at = datetime.utcnow()
    else:
        record.status = 'in_progress'
        record.completed_at = None
    db.session.commit()
    return record


def mark_lesson_complete(student_id, lesson):
    """Idempotent — completing an already-completed lesson is a no-op besides refreshing
    last_activity_at on the skill."""
    existing = StudentLessonProgress.query.filter_by(student_id=student_id, lesson_id=lesson.id).first()
    if not existing:
        db.session.add(StudentLessonProgress(student_id=student_id, lesson_id=lesson.id))
        db.session.commit()
    skill_id = lesson.module.course.skill_id
    return recompute_student_skill(student_id, skill_id)


def touch_skill_activity(student_id, skill_id):
    """Bumps last_activity_at (and creates the tracking row if needed) for actions that
    aren't lesson completions — starting a challenge or project — so 'Continue where you
    left off' reflects all practice, not just lessons watched."""
    return recompute_student_skill(student_id, skill_id)


def compute_streak(student_id):
    """Consecutive days (ending today or yesterday) with at least one lesson completion,
    challenge submission, or project update. Computed on the fly — no separate counter
    table to keep in sync, per the 'don't overload with vanity metrics' brief."""
    dates = set()
    for row in StudentLessonProgress.query.filter_by(student_id=student_id).all():
        if row.completed_at:
            dates.add(row.completed_at.date())
    for row in ChallengeSubmission.query.filter_by(student_id=student_id).all():
        if row.created_at:
            dates.add(row.created_at.date())
    for row in StudentProject.query.filter_by(student_id=student_id).all():
        if row.updated_at:
            dates.add(row.updated_at.date())

    if not dates:
        return 0

    today = datetime.utcnow().date()
    cursor = today if today in dates else today - timedelta(days=1)
    if cursor not in dates:
        return 0
    streak = 0
    while cursor in dates:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def get_dashboard_data(student_id):
    """Everything the Skills home page needs, computed fresh each visit."""
    in_progress = (
        StudentSkill.query.filter_by(student_id=student_id, status='in_progress')
        .order_by(StudentSkill.last_activity_at.desc()).all()
    )
    completed = StudentSkill.query.filter_by(student_id=student_id, status='completed').all()

    active_projects = (
        StudentProject.query.filter_by(student_id=student_id)
        .filter(StudentProject.status != 'completed')
        .order_by(StudentProject.updated_at.desc()).limit(5).all()
    )
    challenges_done = ChallengeSubmission.query.filter_by(student_id=student_id).count()
    projects_done = StudentProject.query.filter_by(student_id=student_id, status='completed').count()

    started_skill_ids = {s.skill_id for s in in_progress} | {s.skill_id for s in completed}
    recommended = (
        Skill.query.filter(Skill.is_published.is_(True), ~Skill.id.in_(started_skill_ids) if started_skill_ids else True)
        .order_by(Skill.order).limit(4).all()
    )

    return {
        'continue_learning': in_progress[:1],
        'in_progress_skills': in_progress,
        'completed_skills': completed,
        'active_projects': active_projects,
        'recommended': recommended,
        'stats': {
            'skills_in_progress': len(in_progress),
            'skills_completed': len(completed),
            'challenges_completed': challenges_done,
            'projects_completed': projects_done,
            'streak': compute_streak(student_id),
        },
    }
