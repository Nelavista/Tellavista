"""Deterministic student insights: performance rollups, weak/strong topics, and
next-action recommendations -- the engine behind the dashboard's Performance and
AI Insights sections (PRD §5.8/§5.9).

Deliberately NO machine learning. The PRD pins the recommendation rules:

    IF quiz_performance(topic) < threshold: RECOMMEND revision_material(topic)
    IF course_progress >= X%:               RECOMMEND next_topic(course)

...as pure functions over real activity. Every number here is computed from actual
rows (CBTAttempt/CBTAnswer/MaterialView/TopicProgress) -- nothing is estimated, and
"never measured" stays distinct from "measured at zero" throughout (see the NULL
mastery_score convention on models.TopicProgress).

Thresholds live here as named constants so they're tunable in one place and testable.
"""
from datetime import datetime

from sqlalchemy import case, func

from app.extensions import db
from app.models import (CBTAnswer, CBTAttempt, CBTQuestion, Topic, TopicProgress)
from app.services.academic_context import resolve_academic_context, find_course
from app.services.progress_service import get_courses_materials_progress_bulk

# A topic is only eligible for weak/strong classification once enough of it has been
# answered for the percentage to mean anything -- a single unlucky question must not
# put "You are struggling with X" on a student's dashboard.
MIN_TOPIC_ANSWERS = 3
# Weak = below 50% correct; strong = 80% or above. Between the two = "on track"
# (surfaced as neither, per §5.9's actionable-insight-not-raw-numbers principle).
WEAK_THRESHOLD = 0.5
STRONG_THRESHOLD = 0.8
# The §5.8 course rule: at 80%+ material progress, point at the next unfinished topic.
COURSE_PROGRESS_NEXT_TOPIC = 0.8
MAX_RECOMMENDATIONS = 3
MAX_LISTED_TOPICS = 3


def get_performance_summary(user):
    """Assessment rollup for the Performance section: quiz average, CBT attempts,
    questions answered. Only submitted attempts count (an abandoned attempt has no
    real result -- see progress_service.get_cbt_summary for the phantom-zero trap)."""
    attempts = (
        CBTAttempt.query.filter(
            CBTAttempt.user_id == user.id,
            CBTAttempt.submitted_at.isnot(None),
        ).all()
    )
    # Both auto-scored formats feed the average: 'cbt' MCQs and 'truefalse' (§5.6).
    # Written practice stays out -- self-marked, never auto-scored.
    scored = [a for a in attempts if a.question_type in ('cbt', 'truefalse')]
    quiz_average = round(sum(a.score_pct for a in scored) / len(scored)) if scored else None

    questions_answered = (
        db.session.query(func.count(CBTAnswer.id))
        .join(CBTAttempt, CBTAnswer.attempt_id == CBTAttempt.id)
        .filter(CBTAttempt.user_id == user.id, CBTAttempt.submitted_at.isnot(None))
        .scalar()
    ) or 0

    return {
        'quiz_average': quiz_average,
        'cbt_attempts': len(attempts),
        'questions_answered': questions_answered,
    }


def _topic_rows(user):
    """Per-(topic, course-code) correctness over this student's submitted CBT
    attempts -- one grouped query, not per-topic loops.

    Only MCQ ('cbt') attempts are aggregated: written answers are self-marked, never
    auto-scored (is_correct is NULL there), so mixing them in would fake a score.
    Questions without a topic tag can't be attributed and are excluded -- honest
    absence, not a zero."""
    return (
        db.session.query(
            func.upper(CBTAttempt.course_code).label('course_code'),
            CBTQuestion.topic.label('topic'),
            func.count(CBTAnswer.id).label('answered'),
            func.sum(case((CBTAnswer.is_correct == True, 1), else_=0)).label('correct'),  # noqa: E712
        )
        .join(CBTAttempt, CBTAnswer.attempt_id == CBTAttempt.id)
        .join(CBTQuestion, CBTAnswer.question_id == CBTQuestion.id)
        .filter(
            CBTAttempt.user_id == user.id,
            CBTAttempt.submitted_at.isnot(None),
            CBTAttempt.question_type.in_(('cbt', 'truefalse')),
            CBTQuestion.topic.isnot(None),
            CBTQuestion.topic != '',
        )
        .group_by(func.upper(CBTAttempt.course_code), CBTQuestion.topic)
        .all()
    )


def _topic_link(ctx, course_code, topic_title):
    """Real /courses/<code>/topics/<id> link when the topic resolves against this
    student's own department's taxonomy -- never a fabricated URL for unseeded data."""
    if not ctx.department:
        return None
    course = find_course(ctx.department, course_code)
    if not course:
        return None
    topic = Topic.query.filter(
        Topic.course_id == course.id,
        func.lower(Topic.title) == (topic_title or '').strip().lower(),
    ).first()
    return f"/courses/{course.code}/topics/{topic.id}" if topic else f"/courses/{course.code}"


def get_weak_strong_topics(user):
    """Weak/strong topic lists under the §5.8 thresholds. Weak sorts worst-first (the
    thing to fix is the first thing you see); strong sorts best-first."""
    weak, strong = [], []
    ctx = resolve_academic_context(user)
    for row in _topic_rows(user):
        answered = row.answered or 0
        if answered < MIN_TOPIC_ANSWERS:
            continue
        score = round((row.correct or 0) / answered, 2)
        entry = {
            'course_code': row.course_code,
            'topic': row.topic,
            'score_pct': round(score * 100),
            'answered': answered,
            'link': _topic_link(ctx, row.course_code, row.topic),
        }
        if score < WEAK_THRESHOLD:
            weak.append(entry)
        elif score >= STRONG_THRESHOLD:
            strong.append(entry)
    weak.sort(key=lambda e: (e['score_pct'], -e['answered']))
    strong.sort(key=lambda e: (-e['score_pct'], -e['answered']))
    return {'weak': weak[:MAX_LISTED_TOPICS], 'strong': strong[:MAX_LISTED_TOPICS]}


def _next_topic_recommendations(user, ctx):
    """The §5.8 progression rule: a course the student is >=80% through gets a pointer
    at its next unfinished topic. Bounded by the student's own level's course list."""
    if not ctx.department or not ctx.courses:
        return []
    codes = [c.code for c in ctx.courses]
    progress = get_courses_materials_progress_bulk(user, codes)

    recs = []
    for course in ctx.courses:
        viewed, total = progress.get(course.code, (0, 0))
        if not total or viewed / total < COURSE_PROGRESS_NEXT_TOPIC:
            continue
        topics = course.topics.filter_by(is_active=True).order_by(Topic.order).all()
        if not topics:
            continue
        done_ids = {
            row.topic_id
            for row in TopicProgress.query.filter(
                TopicProgress.user_id == user.id,
                TopicProgress.topic_id.in_([t.id for t in topics]),
            ).all()
        }
        nxt = next((t for t in topics if t.id not in done_ids), None)
        if not nxt:
            continue
        recs.append({
            'kind': 'next_topic',
            'course_code': course.code,
            'topic': nxt.title,
            'progress_pct': round(viewed / total * 100),
            'message': f"You're {round(viewed / total * 100)}% through {course.code}. "
                       f"Move on to {nxt.title}.",
            'link': f"/courses/{course.code}/topics/{nxt.id}",
        })
        if len(recs) >= MAX_RECOMMENDATIONS:
            break
    return recs


def get_recommendations(user, weak_topics):
    """Actionable next steps, weakest topic first (§5.9: "you are struggling with X"
    must name X and link somewhere real)."""
    recs = []
    for entry in weak_topics[:MAX_RECOMMENDATIONS]:
        recs.append({
            'kind': 'revision',
            'course_code': entry['course_code'],
            'topic': entry['topic'],
            'score_pct': entry['score_pct'],
            'message': f"You are struggling with {entry['topic']} in {entry['course_code']} "
                       f"({entry['score_pct']}% correct). Review this topic before continuing.",
            'link': entry['link'] or f"/courses/{entry['course_code']}",
        })
    recs.extend(_next_topic_recommendations(user, resolve_academic_context(user)))
    return recs[:MAX_RECOMMENDATIONS]


def get_insights(user):
    """Everything the dashboard's Performance + AI Insights sections need, in one
    response. `starter` marks the no-activity state so the UI can show a sensible
    empty state instead of zeros (§5.9's "populate even pre-activity" AC)."""
    performance = get_performance_summary(user)
    topics = get_weak_strong_topics(user)
    recommendations = get_recommendations(user, topics['weak'])
    return {
        'performance': performance,
        'weak': topics['weak'],
        'strong': topics['strong'],
        'recommendations': recommendations,
        'starter': performance['cbt_attempts'] == 0 and performance['questions_answered'] == 0,
    }


# ---------------------------------------------------------------
# Mastery write-back (G9): the PRD's Progress entity wants a measured per-topic
# strength signal. CBT results are the only authoritative scorer today, so a
# submitted attempt writes TopicProgress.mastery_score for every topic it actually
# measured, plus last_activity_at. Unseeded taxonomy (no Course/Topic rows) stays
# NULL -- "not measured", never "scored zero".
# ---------------------------------------------------------------

def update_topic_mastery_from_attempt(attempt, user):
    """Called from /CBT/submit after grading. Computes each topic's % correct from
    the attempt's own CBTAnswer rows (same source the grader used) and upserts
    TopicProgress. Never raises into the submit path -- a mastery-update failure must
    not fail a submission that already graded fine."""
    try:
        if attempt.question_type not in ('cbt', 'truefalse'):
            return
        topic_names = [
            q.topic for q in CBTQuestion.query.filter(
                CBTQuestion.id.in_(attempt.issued_question_ids),
                CBTQuestion.topic.isnot(None), CBTQuestion.topic != '',
            ).all() if q.topic
        ]
        if not topic_names:
            return
        ctx = resolve_academic_context(user)
        course = find_course(ctx.department, attempt.course_code) if ctx.department else None
        if not course:
            return

        answers = CBTAnswer.query.filter(CBTAnswer.attempt_id == attempt.id).all()
        stats = {}
        for a in answers:
            t = a.question.topic if a.question else None
            if not t:
                continue
            s = stats.setdefault(t, {'answered': 0, 'correct': 0})
            s['answered'] += 1
            if a.is_correct:
                s['correct'] += 1

        for title, s in stats.items():
            topic = Topic.query.filter(
                Topic.course_id == course.id,
                func.lower(Topic.title) == title.strip().lower(),
            ).first()
            if not topic:
                continue
            row = TopicProgress.query.filter_by(user_id=user.id, topic_id=topic.id).first()
            if not row:
                # A row created here is measurement, not completion -- completed_at
                # stays NULL (set only by the explicit toggle in academia_routes) so
                # "measured" never masquerades as "marked complete".
                row = TopicProgress(user_id=user.id, topic_id=topic.id, completed_at=None)
                db.session.add(row)
            row.mastery_score = round(s['correct'] / s['answered'], 2) if s['answered'] else None
            row.last_activity_at = datetime.utcnow()
        db.session.commit()
    except Exception:
        db.session.rollback()


def touch_topic_activity(user, topic_id):
    """Bump last_activity_at on an existing TopicProgress row when its topic's
    material is viewed. Never creates a row (a view is not completion) and never
    touches mastery_score -- activity and measurement stay separate signals."""
    if not topic_id:
        return
    row = TopicProgress.query.filter_by(user_id=user.id, topic_id=topic_id).first()
    if row:
        row.last_activity_at = datetime.utcnow()
        db.session.commit()
