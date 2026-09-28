"""PRD §5.8/§5.9: deterministic insights -- performance rollup, weak/strong topics,
recommendations, and the mastery write-back (G9).

All numbers here must come from real rows; the thresholds follow the PRD's rules
(weak below 50%, strong at 80%+, course >=80% progressed -> point at next topic).
"Never measured" must stay distinct from "measured at zero" in every output.
"""
import json

import pytest

from app.extensions import db
from app.models import (CBTAnswer, CBTAttempt, CBTQuestion, Material,
                        MaterialView, Topic, TopicProgress, User)
from app.services.insights_service import (get_insights, get_performance_summary,
                                           get_weak_strong_topics, get_recommendations,
                                           update_topic_mastery_from_attempt)


def _seed_topic_questions(app, course_code='CSC213', topic='Linked Lists', count=4, correct_index=1):
    """Returns the created question ids. `topic=None` rows simulate untagged banks."""
    with app.app_context():
        qs = []
        for i in range(count):
            q = CBTQuestion(
                subject_code='CSC', course_code=course_code, question_type='cbt',
                question_text=f'{topic or "General"} Q{i}?',
                options_json=json.dumps(['a', 'b', 'c', 'd']),
                correct_index=correct_index, explanation='because',
                topic=topic,
            )
            db.session.add(q)
            qs.append(q)
        db.session.commit()
        return [q.id for q in qs]


def _run_attempt(app, user_id, question_ids, correct_ids, course_code='CSC213'):
    """Drives the real submit path's grading effects: a submitted CBTAttempt with one
    CBTAnswer row per issued question, then the mastery write-back."""
    with app.app_context():
        attempt = CBTAttempt(
            user_id=user_id, course_code=course_code, question_type='cbt',
            total_questions=len(question_ids), correct_count=0, score_pct=0,
            started_at=__import__('datetime').datetime.utcnow(),
            submitted_at=__import__('datetime').datetime.utcnow(),
        )
        attempt.issued_question_ids = question_ids
        db.session.add(attempt)
        db.session.flush()

        questions = {q.id: q for q in CBTQuestion.query.filter(
            CBTQuestion.id.in_(question_ids)).all()}
        for qid in question_ids:
            db.session.add(CBTAnswer(
                attempt_id=attempt.id, question_id=qid,
                question_text=questions[qid].question_text,
                selected_index=questions[qid].correct_index if qid in correct_ids else 0,
                is_correct=qid in correct_ids,
            ))
        attempt.correct_count = len(correct_ids)
        attempt.score_pct = round(len(correct_ids) / len(question_ids) * 100)
        db.session.commit()

        user = User.query.get(user_id)
        update_topic_mastery_from_attempt(attempt, user)
        return attempt.id


def test_performance_summary_only_counts_submitted_attempts(app, make_user):
    user = make_user('insight1')
    ids = _seed_topic_questions(app)
    # Submitted attempt via the real grading path (4 answered questions, 3 correct).
    _run_attempt(app, user.id, ids, correct_ids=ids[:3])
    with app.app_context():
        from datetime import datetime
        # Plus one abandoned attempt (submitted_at=None must be invisible).
        a2 = CBTAttempt(user_id=user.id, course_code='CSC213', question_type='cbt',
                        total_questions=4, correct_count=0, score_pct=0,
                        started_at=datetime.utcnow(), submitted_at=None)
        a2.issued_question_ids = ids
        db.session.add(a2)
        db.session.commit()

        summary = get_performance_summary(User.query.get(user.id))
    assert summary['cbt_attempts'] == 1          # abandoned attempt invisible
    assert summary['quiz_average'] == 75
    assert summary['questions_answered'] == 4


def test_weak_and_strong_topics_with_thresholds(app, make_user):
    user = make_user('insight2')
    weak_ids = _seed_topic_questions(app, topic='Pointers', count=4)
    strong_ids = _seed_topic_questions(app, topic='Sorting', count=4)
    _run_attempt(app, user.id, weak_ids, correct_ids=weak_ids[:1])     # 25% -> weak
    _run_attempt(app, user.id, strong_ids, correct_ids=strong_ids)     # 100% -> strong

    with app.app_context():
        result = get_weak_strong_topics(User.query.get(user.id))
    weak = {e['topic']: e for e in result['weak']}
    strong = {e['topic']: e for e in result['strong']}
    assert weak['Pointers']['score_pct'] == 25
    assert strong['Sorting']['score_pct'] == 100
    # The middle band (50-79%) appears in neither list.
    assert 'Pointers' not in strong and 'Sorting' not in weak


def test_sparse_topics_never_classified(app, make_user):
    """1-2 answered questions can't put a weak-topic warning on the dashboard."""
    user = make_user('insight3')
    ids = _seed_topic_questions(app, topic='Recursion', count=2)
    _run_attempt(app, user.id, ids, correct_ids=[])   # 0% but only 2 answers

    with app.app_context():
        result = get_weak_strong_topics(User.query.get(user.id))
    assert result['weak'] == []
    assert result['strong'] == []


def test_untagged_questions_excluded_from_topic_rollups(app, make_user):
    user = make_user('insight4')
    ids = _seed_topic_questions(app, topic=None, count=5)
    _run_attempt(app, user.id, ids, correct_ids=[])

    with app.app_context():
        result = get_weak_strong_topics(User.query.get(user.id))
    assert result['weak'] == []   # unattributable -> honest absence, not a zero


def test_revision_recommendation_names_topic_and_links(app, make_user, make_course):
    course = make_course(code='CSC213')
    user = make_user('insight5', university='Lagos State University')
    # Make the topic real in the taxonomy so the link can resolve.
    with app.app_context():
        from app.models import Course as CourseModel
        t = Topic(course_id=course.id, title='Linked Lists', order=1)
        db.session.add(t)
        db.session.commit()

    ids = _seed_topic_questions(app, course_code='CSC213', topic='Linked Lists', count=4)
    _run_attempt(app, user.id, ids, correct_ids=ids[:1])   # 25%

    with app.app_context():
        result = get_weak_strong_topics(User.query.get(user.id))
        recs = get_recommendations(User.query.get(user.id), result['weak'])
    rev = [r for r in recs if r['kind'] == 'revision']
    assert rev, 'a 25% topic must produce a revision recommendation'
    assert rev[0]['topic'] == 'Linked Lists'
    assert 'struggling with Linked Lists' in rev[0]['message']
    assert rev[0]['link'] and rev[0]['link'].startswith('/courses/CSC213/topics/')


def test_next_topic_recommendation_at_progress_threshold(app, make_user, make_course):
    course = make_course(code='CSC213')
    user = make_user('insight6', university='Lagos State University')
    with app.app_context():
        t1 = Topic(course_id=course.id, title='Arrays', order=1)
        t2 = Topic(course_id=course.id, title='Linked Lists', order=2)
        db.session.add_all([t1, t2])
        db.session.commit()
        material_ids = []
        for i in range(4):
            m = Material(title=f'note{i}.pdf', department='Computer Science', level='200',
                         semester='First Semester', course_code='CSC213', course_id=course.id,
                         university='Lagos State University', source='uploaded')
            db.session.add(m)
            material_ids.append(m)
        db.session.commit()
        material_ids = [m.id for m in material_ids]
        uid = user.id

    # View 4/4 materials -> 100% >= 80% threshold -> "move on to" the unfinished topic.
    with app.app_context():
        u = User.query.get(uid)
        for mid in material_ids:
            db.session.add(MaterialView(user_id=uid, material_id=mid))
        db.session.commit()

    with app.app_context():
        recs = get_recommendations(User.query.get(uid), [])
    nxt = [r for r in recs if r['kind'] == 'next_topic']
    assert nxt, '>=80% course progress must produce a next-topic recommendation'
    assert nxt[0]['topic'] == 'Arrays'   # first not-yet-completed topic in order
    assert '/courses/CSC213/topics/' in nxt[0]['link']


def test_get_insights_starter_state(app, make_user):
    user = make_user('insight7')
    with app.app_context():
        data = get_insights(User.query.get(user.id))
    assert data['starter'] is True
    assert data['performance']['quiz_average'] is None
    assert data['weak'] == [] and data['strong'] == [] and data['recommendations'] == []


def test_mastery_writeback_measures_only_taxonomized_topics(app, make_user, make_course):
    course = make_course(code='CSC213')
    user = make_user('insight8', university='Lagos State University')
    with app.app_context():
        t = Topic(course_id=course.id, title='Stacks', order=1)
        db.session.add(t)
        db.session.commit()

    # Same bank questions also cover an unseeded course's code: only the taxonomized
    # course's topic gets a mastery row.
    ids = _seed_topic_questions(app, course_code='CSC213', topic='Stacks', count=4)
    _run_attempt(app, user.id, ids, correct_ids=ids[:3])   # 75%

    with app.app_context():
        row = TopicProgress.query.filter_by(user_id=user.id).first()
        assert row is not None
        assert row.mastery_score == 0.75
        assert row.completed_at is None, 'measurement must not masquerade as completion'
        assert row.last_activity_at is not None


def test_mastery_writeback_unseeded_taxonomy_stays_null(app, make_user):
    """No Course/Topic rows exist for this student's department -> nothing measured,
    no zero invented."""
    user = make_user('insight9', university='University of Nowhere')
    ids = _seed_topic_questions(app, course_code='ZZZ101', topic='Mystery', count=4)
    _run_attempt(app, user.id, ids, correct_ids=[], course_code='ZZZ101')

    with app.app_context():
        assert TopicProgress.query.filter_by(user_id=user.id).count() == 0
