"""Read-only view models for the redesigned Skills learning screens (Learn, skill page,
syllabus, lesson, My Learning, Projects, Paths, Transcript).

Nothing here writes. Progress, unlocking and verification rules stay in
services/skills_service.py and services/daily_class_service.py; this module only
gathers what those rules already decided into the shapes the templates render, with
batched queries so a catalog of 100+ skills costs a fixed number of queries.
"""
import re

from flask import url_for
from sqlalchemy import func

from app.extensions import db
from app.models import (
    SkillCourse, CourseModule, Lesson, ProjectTemplate, StudentSkill,
    StudentLessonProgress, ChallengeSubmission, Cohort, CohortEnrollment,
)

_WEEK_PREFIX = re.compile(r'^\s*(week|day|module|part|unit)\s*\d+\s*[:\-–—.]\s*', re.I)
_NUM_PREFIX = re.compile(r'^\s*\d+\s*[.)]\s*')


_KIND_PREFIX = re.compile(r'^\s*(practice|build|assessment|course|project)\s*:\s*', re.I)


def clean_step_title(title):
    """Path step titles often repeat their kind ('Practice: Bio Page'); the kind is shown
    separately, so drop it. 'Practice Project: ...' is a title, not a prefix, and stays."""
    return _KIND_PREFIX.sub('', clean_title(title)).strip() or clean_title(title)


def clean_title(title):
    """'Week 2: Bringing Pages to Life' -> 'Bringing Pages to Life'; '3. Audio' -> 'Audio'."""
    t = _WEEK_PREFIX.sub('', title or '')
    return _NUM_PREFIX.sub('', t).strip() or (title or '').strip()


# ── URLs ────────────────────────────────────────────────────────────────────────
def lesson_url(skill, course, lesson):
    if course.is_daily_class and lesson.day_number:
        return url_for('skills.day_view', skill_slug=skill.slug, course_slug=course.slug, day_number=lesson.day_number)
    return url_for('skills.lesson_view', skill_slug=skill.slug, course_slug=course.slug, lesson_slug=lesson.slug)


def course_url(skill, course):
    if course.is_daily_class:
        return url_for('skills.class_overview', skill_slug=skill.slug, course_slug=course.slug)
    return url_for('skills.course_view', skill_slug=skill.slug, course_slug=course.slug)


# ── Catalog cards ───────────────────────────────────────────────────────────────
def card_stats(skill_ids):
    """{skill_id: {'lessons', 'minutes', 'projects', 'has_content'}} for published content
    only, in three grouped queries regardless of how many skills are on the page."""
    if not skill_ids:
        return {}
    lesson_rows = (
        db.session.query(SkillCourse.skill_id, func.count(Lesson.id), func.coalesce(func.sum(Lesson.duration_minutes), 0))
        .join(CourseModule, CourseModule.course_id == SkillCourse.id)
        .join(Lesson, Lesson.module_id == CourseModule.id)
        .filter(SkillCourse.skill_id.in_(skill_ids), SkillCourse.is_published.is_(True), Lesson.is_published.is_(True))
        .group_by(SkillCourse.skill_id).all()
    )
    project_rows = dict(
        db.session.query(ProjectTemplate.skill_id, func.count(ProjectTemplate.id))
        .filter(ProjectTemplate.skill_id.in_(skill_ids), ProjectTemplate.is_published.is_(True))
        .group_by(ProjectTemplate.skill_id).all()
    )
    course_ids = {
        row[0] for row in db.session.query(SkillCourse.skill_id)
        .filter(SkillCourse.skill_id.in_(skill_ids), SkillCourse.is_published.is_(True)).distinct().all()
    }
    stats = {sid: {'lessons': 0, 'minutes': 0, 'projects': project_rows.get(sid, 0), 'has_content': sid in course_ids}
             for sid in skill_ids}
    for sid, count, minutes in lesson_rows:
        stats[sid]['lessons'] = count
        stats[sid]['minutes'] = int(minutes or 0)
    for sid in skill_ids:
        stats[sid]['has_content'] = stats[sid]['has_content'] and stats[sid]['lessons'] > 0
    return stats


def skill_hours(skill, stats):
    """The skill's own published estimate when set, otherwise the real sum of lesson
    durations (rounded). None when there is nothing to estimate from."""
    if skill.estimated_hours:
        return skill.estimated_hours
    minutes = (stats or {}).get('minutes') or 0
    return max(1, round(minutes / 60)) if minutes else None


def build_cards(skills, student_id):
    stats = card_stats([s.id for s in skills])
    progress = {
        row.skill_id: row for row in StudentSkill.query.filter(
            StudentSkill.student_id == student_id, StudentSkill.skill_id.in_([s.id for s in skills])
        ).all()
    } if skills else {}
    cards = []
    for skill in skills:
        st = stats.get(skill.id, {})
        ss = progress.get(skill.id)
        cards.append({
            'skill': skill, 'lessons': st.get('lessons', 0), 'hours': skill_hours(skill, st),
            'projects': st.get('projects', 0), 'has_content': st.get('has_content', False),
            'progress': ss.progress_pct if ss else None,
            'completed': bool(ss and ss.status == 'completed'),
        })
    return cards


def card_json(card):
    s = card['skill']
    return {
        'n': s.name, 's': s.slug, 't': s.tagline or '', 'c': s.category.name if s.category else '',
        'l': (s.level or '').title(), 'k': ' '.join(s.tags), 'i': s.icon or 'ri-book-3-line', 'co': s.color or '',
        'ls': card['lessons'], 'h': card['hours'], 'p': card['projects'], 'ok': card['has_content'],
        'pr': card['progress'], 'd': card['completed'],
    }


# ── Course outlines ─────────────────────────────────────────────────────────────
def _existing_enrollment(student_id, course):
    """The student's enrollment in a daily class, WITHOUT creating one -- browsing a
    syllabus must not enrol anyone."""
    return (
        CohortEnrollment.query.join(Cohort, CohortEnrollment.cohort_id == Cohort.id)
        .filter(Cohort.course_id == course.id, CohortEnrollment.student_id == student_id).first()
    )


def course_outline(student_id, course, completed_ids=None):
    """Modules -> lessons with a per-lesson state: 'done', 'current' (the next one to
    take), 'open' (available, not next) or 'locked' (a daily-class day not reached yet).
    Same unlocking rule as daily_class_service.get_day_states."""
    modules = course.modules.order_by(CourseModule.order).all()
    lessons_by_module = []
    all_lessons = []
    for m in modules:
        ls = m.lessons.filter_by(is_published=True).order_by(Lesson.order).all()
        if course.is_daily_class:
            ls = sorted(ls, key=lambda l: (l.day_number or 0, l.order or 0))
        if ls:
            lessons_by_module.append((m, ls))
            all_lessons.extend(ls)
    if completed_ids is None:
        completed_ids = {
            p.lesson_id for p in StudentLessonProgress.query.filter(
                StudentLessonProgress.student_id == student_id,
                StudentLessonProgress.lesson_id.in_([l.id for l in all_lessons]),
            ).all()
        } if all_lessons else set()

    frontier = None
    if course.is_daily_class:
        enrollment = _existing_enrollment(student_id, course)
        frontier = enrollment.current_day if enrollment else 1

    next_lesson = None
    out_modules = []
    minutes = 0
    for m, ls in lessons_by_module:
        rows = []
        for l in ls:
            minutes += l.duration_minutes or 0
            if l.id in completed_ids:
                state = 'done'
            elif frontier is not None and l.day_number and l.day_number > frontier:
                state = 'locked'
            elif next_lesson is None:
                state = 'current'
                next_lesson = l
            else:
                state = 'open'
            rows.append({'lesson': l, 'state': state})
        out_modules.append({'module': m, 'title': m.title, 'rows': rows})

    total = len(all_lessons)
    done = sum(1 for l in all_lessons if l.id in completed_ids)
    return {
        'course': course, 'modules': out_modules, 'lessons': all_lessons, 'total': total, 'done': done,
        'pct': round(done / total * 100) if total else 0, 'next_lesson': next_lesson,
        'first_lesson': all_lessons[0] if all_lessons else None, 'minutes': minutes,
    }


def skill_outlines(student_id, skill):
    """course_outline() for every published course of a skill, sharing one progress query."""
    courses = skill.courses.filter_by(is_published=True).order_by(SkillCourse.order).all()
    lesson_ids = [
        l.id for c in courses for m in c.modules.all() for l in m.lessons.filter_by(is_published=True).all()
    ]
    completed_ids = {
        p.lesson_id for p in StudentLessonProgress.query.filter(
            StudentLessonProgress.student_id == student_id, StudentLessonProgress.lesson_id.in_(lesson_ids),
        ).all()
    } if lesson_ids else set()
    return [course_outline(student_id, c, completed_ids) for c in courses]


def resume_point(outlines):
    """(course, lesson, is_start) -- where the student should go next in a skill: the
    first course that still has an unfinished, unlocked lesson. None when there is no
    content or everything is done."""
    any_done = any(o['done'] for o in outlines)
    for o in outlines:
        if o['next_lesson']:
            return {'course': o['course'], 'lesson': o['next_lesson'], 'is_start': not any_done}
    return None


def learning_outcomes(outlines, limit=8):
    """'What you'll learn', taken from the curriculum itself: module titles when they
    are specific enough (four or more distinct ones), otherwise lesson titles."""
    seen, modules = set(), []
    for o in outlines:
        for m in o['modules']:
            t = clean_title(m['title'])
            if t.lower() not in seen:
                seen.add(t.lower())
                modules.append(t)
    if len(modules) >= 4:
        return modules[:limit]
    seen, lessons = set(), []
    for o in outlines:
        for l in o['lessons']:
            t = clean_title(l.title)
            if t.lower() not in seen:
                seen.add(t.lower())
                lessons.append(t)
    return lessons[:limit]


def demonstrated_skills(templates, limit=12):
    seen, tags = set(), []
    for t in templates:
        for tag in t.skills_demonstrated:
            key = (tag or '').strip().lower()
            if key and key not in seen:
                seen.add(key)
                tags.append(tag.strip())
    return tags[:limit]


# ── Student work ────────────────────────────────────────────────────────────────
def project_skill(project):
    """The Skill a StudentProject belongs to, when it came from a template."""
    t = getattr(project, 'template', None)
    return t.skill if t is not None and t.skill is not None else None


def project_status(project):
    """('In progress' | 'Submitted' | 'In review' | 'Reviewed' | 'Completed', css-modifier)."""
    if project.verification_status == 'requested':
        return 'In review', 'is-review'
    if project.status == 'completed':
        return 'Completed', 'is-done'
    if project.status == 'submitted':
        return 'Submitted', 'is-review'
    return 'In progress', 'is-progress'


def project_score(project):
    if project.ai_overall_score is not None:
        return project.ai_overall_score
    fb = project.ai_feedback or {}
    try:
        return int(fb.get('score')) if fb.get('score') is not None else None
    except (TypeError, ValueError):
        return None


def challenge_done_ids(student_id, challenge_ids):
    if not challenge_ids:
        return set()
    return {
        row[0] for row in db.session.query(ChallengeSubmission.challenge_id).filter(
            ChallengeSubmission.student_id == student_id, ChallengeSubmission.challenge_id.in_(challenge_ids),
        ).distinct().all()
    }


def step_kind(step):
    if step.step_type == 'course':
        return 'Course'
    if step.step_type == 'project':
        return 'Project'
    if step.challenge is not None and step.challenge.is_assessment:
        return 'Assessment'
    return 'Practice'


PHASES = [('learn', 'Learn'), ('practice', 'Practice'), ('build', 'Build'), ('verify', 'Demonstrate')]


def phase_row(pipeline_steps):
    """Learn -> Practice -> Build -> Demonstrate states from skills_service's pipeline,
    without its 'earn' phase (earning lives in Opportunities, not Skills)."""
    by_phase = {s['phase']: s['state'] for s in pipeline_steps}
    out, found = [], False
    for key, label in PHASES:
        state = by_phase.get(key, 'locked')
        if state == 'done':
            out.append({'label': label, 'state': 'done'})
        elif not found:
            out.append({'label': label, 'state': 'now'})
            found = True
        else:
            out.append({'label': label, 'state': 'later'})
    return out
