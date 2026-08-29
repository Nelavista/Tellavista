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
    CareerTrackStep, Challenge, ProjectTemplate, Opportunity, OpportunityApplication,
    Rating,
)

# What Nelavista keeps of a paid gig — shown openly everywhere a payout is shown (Earnings,
# an application's status, a Talent Profile) so "trusted intermediary" is never just a
# claim. A single constant, not per-opportunity, so a student can trust it's consistent.
PLATFORM_FEE_PCT = 10

# Minimum review score (percent) for a project to count toward skill verification. Applies
# to both review paths a StudentProject can go through: the ordinary "Request Review" AI
# feedback (ai_feedback['score'], 0-100) and a daily-class final project's rubric score
# (ai_overall_score, which by ProjectTemplate.rubric's own convention sums to 100 -- see
# models.py). A completed project that was never reviewed, or that scored below this bar,
# does not count -- see _project_counts_as_verified below.
PROJECT_VERIFICATION_MIN_SCORE = 60

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


# ============================================================
# ===== DASHBOARD V2: Learn -> Practice -> Build -> Verify -> Earn =====
# ============================================================

PIPELINE_PHASES = ['learn', 'practice', 'build', 'verify', 'earn']
PIPELINE_LABELS = {'learn': 'Learn', 'practice': 'Practice', 'build': 'Build', 'verify': 'Verify', 'earn': 'Earn'}


def has_practiced(student_id, skill_id):
    return ChallengeSubmission.query.join(Challenge, ChallengeSubmission.challenge_id == Challenge.id) \
        .filter(Challenge.skill_id == skill_id, ChallengeSubmission.student_id == student_id).first() is not None


def has_built(student_id, skill_id):
    return StudentProject.query.join(ProjectTemplate, StudentProject.project_template_id == ProjectTemplate.id) \
        .filter(ProjectTemplate.skill_id == skill_id, StudentProject.student_id == student_id).first() is not None


def _project_counts_as_verified(project):
    """Whether one StudentProject clears the bar for skill verification. Being marked
    `status == 'completed'` is the student's OWN claim (see routes/skills_routes.py's
    update_project -- a plain student-triggered status flip) and is NOT sufficient by
    itself; this additionally requires a real, Nelavista-triggered review that actually
    scored the work at or above PROJECT_VERIFICATION_MIN_SCORE, via either review path:
    - `verification_status == 'reviewed'` with a numeric ai_feedback['score'] (the
      "Request Review" AI evaluation, routes/skills_routes.py's request_project_review), or
    - a rubric-graded final project's `ai_overall_score` (evaluate_final_project, only set
      once a daily-class final-project submission has actually been evaluated).
    A project that is merely 'completed' with neither signal present returns False."""
    if project.status != 'completed':
        return False

    if project.verification_status == 'reviewed':
        feedback = project.ai_feedback or {}
        score = feedback.get('score')
        try:
            if score is not None and int(score) >= PROJECT_VERIFICATION_MIN_SCORE:
                return True
        except (TypeError, ValueError):
            pass

    if project.ai_overall_score is not None:
        try:
            if int(project.ai_overall_score) >= PROJECT_VERIFICATION_MIN_SCORE:
                return True
        except (TypeError, ValueError):
            pass

    return False


def is_skill_verified(student_id, skill_id):
    """A skill counts as 'verified' once the student has finished its course content AND
    shipped at least one project in it that was actually reviewed and scored well enough
    (see _project_counts_as_verified) — a course alone only proves you watched something,
    and an unreviewed 'completed' project is only the student's own say-so, neither of
    which is a claim Nelavista makes to an employer on the student's behalf."""
    student_skill = StudentSkill.query.filter_by(student_id=student_id, skill_id=skill_id).first()
    if not student_skill or student_skill.status != 'completed':
        return False
    projects = StudentProject.query.join(ProjectTemplate, StudentProject.project_template_id == ProjectTemplate.id) \
        .filter(ProjectTemplate.skill_id == skill_id, StudentProject.student_id == student_id).all()
    return any(_project_counts_as_verified(p) for p in projects)


def has_earned(student_id, skill_id):
    return OpportunityApplication.query.join(Opportunity, OpportunityApplication.opportunity_id == Opportunity.id) \
        .filter(Opportunity.skill_id == skill_id, OpportunityApplication.student_id == student_id,
                OpportunityApplication.status.in_(['accepted', 'completed', 'paid'])).first() is not None


def get_pipeline_state(student_id, skill_id):
    """Returns the Learn->Practice->Build->Verify->Earn state for one skill: an ordered
    list of {phase, label, state} ('done'|'current'|'locked') plus the current phase key.
    Same completed/current/locked vocabulary used everywhere else in Skills."""
    done_map = {
        'learn': (StudentSkill.query.filter_by(student_id=student_id, skill_id=skill_id, status='completed').first() is not None),
        'practice': has_practiced(student_id, skill_id),
        'build': has_built(student_id, skill_id),
        'verify': is_skill_verified(student_id, skill_id),
        'earn': has_earned(student_id, skill_id),
    }
    steps = []
    found_current = False
    current_phase = None
    for phase in PIPELINE_PHASES:
        done = done_map[phase]
        if done:
            state = 'done'
        elif not found_current:
            state = 'current'
            found_current = True
            current_phase = phase
        else:
            state = 'locked'
        steps.append({'phase': phase, 'label': PIPELINE_LABELS[phase], 'state': state})
    if current_phase is None:
        current_phase = 'earn'  # every phase done
    return steps, current_phase


def opportunity_match_pct(student_id, skill_id):
    """How well-matched a student is to an opportunity in this skill — always derived
    from real progress (StudentSkill.progress_pct), never a fabricated number."""
    row = StudentSkill.query.filter_by(student_id=student_id, skill_id=skill_id).first()
    return row.progress_pct if row else 0


def profile_completeness(user):
    """The 'Profile strength' checklist on the Skills dashboard — every item here is a
    real, checkable fact, not a static UI decoration."""
    items = [
        {'key': 'photo', 'label': 'Profile photo', 'done': bool(user.profile_photo_url)},
        {'key': 'bio', 'label': 'Bio', 'done': bool(user.bio and user.bio.strip())},
        {'key': 'portfolio', 'label': 'Portfolio link', 'done': bool(user.portfolio_url)},
        {'key': 'verification', 'label': 'Skill verification', 'done': _any_skill_verified(user.id)},
        {'key': 'academic', 'label': 'Academic information', 'done': all([
            user.university, user.faculty, user.department, user.level,
        ])},
    ]
    done_count = sum(1 for i in items if i['done'])
    pct = round((done_count / len(items)) * 100)
    # Named 'checklist', not 'items' — Jinja resolves `dict.items` to the built-in
    # dict.items() method via attribute lookup before it ever checks dict keys, so a key
    # literally named 'items' silently becomes uniterable in a template.
    return {'pct': pct, 'checklist': items}


def _any_skill_verified(student_id):
    for row in StudentSkill.query.filter_by(student_id=student_id, status='completed').all():
        if is_skill_verified(student_id, row.skill_id):
            return True
    return False


def get_continue_learning_card(student_id, student_skill):
    """Everything the 'Continue Learning' card needs for one in-progress skill: the next
    lesson to take, real remaining time (summed from actual lesson durations, not a
    guess), and how many of the skill's project templates the student has started."""
    skill = student_skill.skill
    course = skill.courses.filter_by(is_published=True).order_by(SkillCourse.order).first()
    if not course:
        return None

    modules = course.modules.order_by(CourseModule.order).all()
    all_lessons = []
    for m in modules:
        all_lessons.extend(m.lessons.filter_by(is_published=True).order_by(Lesson.order).all())
    completed_ids = {
        p.lesson_id for p in StudentLessonProgress.query.filter(
            StudentLessonProgress.student_id == student_id,
            StudentLessonProgress.lesson_id.in_([l.id for l in all_lessons]),
        ).all()
    } if all_lessons else set()

    next_lesson, next_module = None, None
    remaining_minutes = 0
    for m in modules:
        for l in m.lessons.filter_by(is_published=True).order_by(Lesson.order).all():
            if l.id not in completed_ids:
                if next_lesson is None:
                    next_lesson, next_module = l, m
                remaining_minutes += l.duration_minutes or 0

    total_templates = ProjectTemplate.query.filter_by(skill_id=skill.id, is_published=True).count()
    started_templates = StudentProject.query.filter(
        StudentProject.student_id == student_id, StudentProject.project_template_id.in_(
            [t.id for t in ProjectTemplate.query.filter_by(skill_id=skill.id, is_published=True).all()]
        )
    ).count() if total_templates else 0

    steps, current_phase = get_pipeline_state(student_id, skill.id)
    next_phase = None
    for i, s in enumerate(steps):
        if s['phase'] == current_phase and i + 1 < len(steps):
            next_phase = steps[i + 1]['label']
            break

    return {
        'skill': skill, 'course': course, 'pct': student_skill.progress_pct,
        'next_lesson': next_lesson, 'next_module': next_module,
        'time_left_hours': round(remaining_minutes / 60, 1) if remaining_minutes else 0,
        'projects_started': started_templates, 'projects_total': total_templates,
        'next_phase_label': next_phase or 'Complete',
        'pipeline_steps': steps, 'current_phase': current_phase,
    }


def compute_payout_breakdown(payment_amount):
    """Gross/fee/net for one gig — the same formula everywhere a payout is shown, so a
    number on the Earnings page always matches what was quoted on the Opportunity."""
    payment_amount = payment_amount or 0
    fee = round(payment_amount * PLATFORM_FEE_PCT / 100)
    return {'gross': payment_amount, 'fee': fee, 'fee_pct': PLATFORM_FEE_PCT, 'net': payment_amount - fee}


def get_verified_skills(student_id):
    """Every Skill this student has actually verified (Learn+Practice+Build+Verify all
    done) — the badge list shown on a Talent Profile. Always recomputed, never cached,
    same as the rest of this module."""
    verified = []
    for row in StudentSkill.query.filter_by(student_id=student_id, status='completed').all():
        if is_skill_verified(student_id, row.skill_id):
            verified.append(row.skill)
    return verified


def get_skill_scores(student_id, public_only=False):
    """Per-skill score + project evidence, computed at query time from reviewed
    StudentProjects — same 'derive, don't persist' convention get_cohort_rank uses for
    cohort ranking (services/gpa_service.py). No new table, no caching.

    Only scores projects that have actually been graded (rubric-based or the ordinary
    AI review) — reuses the exact numbers _project_counts_as_verified already trusts,
    never recomputes or re-derives a score of its own. A project stuck at 'in_progress'
    or merely self-marked 'completed' with no review contributes nothing here, same
    gating spirit as is_skill_verified.

    `public_only=True` (for a Talent Profile a viewer other than the student themself is
    looking at) additionally requires each project's own is_public flag — the same
    per-project toggle that already gates the adjacent Projects grid on that page. Without
    this, a project the student explicitly marked private could still leak its title and
    score into the evidence list.

    Returns a list of {skill, score, evidence: [{project_id, title, score}, ...]},
    sorted by score desc, skill name used as the grouping key so custom/AI-generated
    projects (no project_template_id) still count toward the skill they declared via
    skills_demonstrated.
    """
    query = StudentProject.query.filter_by(student_id=student_id)
    if public_only:
        query = query.filter_by(is_public=True)
    projects = query.all()
    by_skill = {}
    for p in projects:
        if p.ai_overall_score is not None:
            score = p.ai_overall_score
        elif p.ai_feedback and p.ai_feedback.get('score') is not None:
            score = p.ai_feedback['score']
        else:
            continue
        try:
            score = int(score)
        except (TypeError, ValueError):
            continue

        skill = p.template.skill if p.template and p.template.skill else None
        skill_name = skill.name if skill else (p.skills_demonstrated[0] if p.skills_demonstrated else None)
        if not skill_name:
            continue

        entry = by_skill.setdefault(skill_name, {'skill': skill, 'skill_name': skill_name, 'scores': [], 'evidence': []})
        entry['scores'].append(score)
        entry['evidence'].append({'project_id': p.id, 'title': p.title, 'score': score})

    results = []
    for entry in by_skill.values():
        entry['evidence'].sort(key=lambda e: e['score'], reverse=True)
        results.append({
            'skill': entry['skill'], 'skill_name': entry['skill_name'],
            'score': round(sum(entry['scores']) / len(entry['scores'])),
            'evidence': entry['evidence'],
        })
    results.sort(key=lambda r: r['score'], reverse=True)
    return results


def get_talent_stats(user):
    """Everything a Talent Profile (public or the student's own preview) needs in one
    call: verified skills, real project count, real completed-gig count with a real
    average rating (never a placeholder), and total earned. Every number here is derived
    from the same rows Earnings/Transcript/Dashboard already use — a Talent Profile is a
    view of that data, not a separate source of truth."""
    verified_skills = get_verified_skills(user.id)
    completed_projects = StudentProject.query.filter_by(student_id=user.id, status='completed').count()

    completed_apps = OpportunityApplication.query.filter(
        OpportunityApplication.student_id == user.id, OpportunityApplication.status.in_(['completed', 'paid'])
    ).all()
    ratings = Rating.query.filter_by(student_id=user.id).all()
    avg_rating = round(sum(r.stars for r in ratings) / len(ratings), 1) if ratings else None

    total_earned = sum(a.payout_amount or 0 for a in
                        OpportunityApplication.query.filter_by(student_id=user.id, status='paid').all())

    headline_skill = verified_skills[0] if verified_skills else None
    if not headline_skill:
        top = StudentSkill.query.filter_by(student_id=user.id).order_by(StudentSkill.progress_pct.desc()).first()
        headline_skill = top.skill if top else None

    return {
        'verified_skills': verified_skills,
        'completed_projects': completed_projects,
        'completed_gigs': len(completed_apps),
        'avg_rating': avg_rating,
        'rating_count': len(ratings),
        'total_earned': total_earned,
        'headline_skill': headline_skill,
    }
