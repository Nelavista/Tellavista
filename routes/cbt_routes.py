import random
import re
import traceback
from datetime import datetime
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from utils.helpers import login_required, debug_print
from models import User, CBTQuestion, CBTAttempt, CBTAnswer
from extensions import db, limiter
from config import OPENROUTER_API_KEY
from services.academic_context import resolve_academic_context, find_course
from services.progress_service import get_cbt_summary
import requests

cbt_bp = Blueprint('cbt', __name__)

# Matches CBT.html's own subject-prefix extraction (course.match(/[A-Z]+/)) -- the
# leading letters of a course code, e.g. "MAT101" -> "MAT". Kept in exact sync so a
# course that resolves to a question bank client-side resolves to the same bank here.
_SUBJECT_PREFIX_RE = re.compile(r'[A-Za-z]+')

MAX_CBT_QUESTIONS = 50
MAX_WRITTEN_QUESTIONS = 10


def _subject_code_for(course_code):
    m = _SUBJECT_PREFIX_RE.match(course_code or '')
    return m.group(0).upper() if m else None


@cbt_bp.route('/CBT', methods=['GET'])
@login_required
def CBT():
    """Mock Exam / CBT Practice page"""

    # Get username from session (custom auth)
    username = session.get('user', {}).get('username')
    if not username:
        flash('Please log in to continue.', 'error')
        return redirect(url_for('auth.login'))

    # Query the user from database
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('User not found. Please log in again.', 'error')
        return redirect(url_for('auth.login'))

    return render_template(
        "CBT.html",
        user_dept=user.department or '',
        user_level=user.level or '',
        user_name=user.name or 'Student'
    )


@cbt_bp.route('/api/cbt/counts')
@login_required
def cbt_counts():
    """How many CBT/written questions exist for one course -- used by the exam-type
    screen to show real counts and honestly disable a card with no content, without ever
    shipping the questions (or answers) themselves before the student actually starts."""
    course_code = (request.args.get('course_code') or '').strip().upper()
    subject_code = _subject_code_for(course_code)
    if not subject_code:
        return jsonify({'success': True, 'cbt_count': 0, 'written_count': 0})
    cbt_count = CBTQuestion.query.filter_by(subject_code=subject_code, question_type='cbt', is_active=True).count()
    written_count = CBTQuestion.query.filter_by(subject_code=subject_code, question_type='written', is_active=True).count()
    return jsonify({'success': True, 'cbt_count': min(cbt_count, MAX_CBT_QUESTIONS),
                     'written_count': min(written_count, MAX_WRITTEN_QUESTIONS)})


@cbt_bp.route('/api/cbt/mark-scheme')
@login_required
def cbt_mark_scheme():
    """Reveals one written question's mark scheme mid-attempt -- the 'Check Answer' study
    aid in the exam UI. Written questions were never auto-scored (the student self-marks
    honestly or not, same as before this change), so there's no score-forging risk here
    the way there was for CBT correct_index; this endpoint still scopes to a real,
    in-progress attempt the student owns so it can't be used to scrape the whole written
    bank's mark schemes without ever starting a practice attempt."""
    try:
        attempt_id = int(request.args.get('attempt_id'))
        question_id = int(request.args.get('question_id'))
    except (TypeError, ValueError):
        return jsonify({'success': False, 'error': 'Invalid attempt_id/question_id'}), 400

    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    attempt = CBTAttempt.query.filter_by(id=attempt_id, user_id=user.id).first()
    if not attempt or question_id not in attempt.issued_question_ids:
        return jsonify({'success': False, 'error': 'Not found'}), 404

    question = CBTQuestion.query.get(question_id)
    return jsonify({'success': True, 'mark_scheme': (question.mark_scheme if question else None) or 'Mark scheme not available.'})


@cbt_bp.route('/api/cbt/start', methods=['POST'])
@login_required
@limiter.limit('30 per hour')
def start_cbt_attempt():
    """Issues a fresh set of questions for one course/type WITHOUT correct answers --
    the server picks and shuffles the questions from CBTQuestion (never the client), and
    snapshots exactly which question ids were issued onto the new CBTAttempt row
    (issued_question_ids) so /CBT/submit/<id> can later verify every submitted answer
    belongs to a question that was actually handed out for this specific attempt, and
    can never be substituted, duplicated, or invented by the client. Mirrors CBT.html's
    own course-code -> subject-prefix mapping exactly (see _subject_code_for above) so
    the same course always resolves to the same bank."""
    data = request.get_json(silent=True) or {}
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 401

    course_code = (data.get('course_code') or '').strip().upper()
    question_type = data.get('question_type')
    if not course_code or question_type not in ('cbt', 'written'):
        return jsonify({'success': False, 'error': 'Missing/invalid course_code or question_type'}), 400

    subject_code = _subject_code_for(course_code)
    bank = CBTQuestion.query.filter_by(
        subject_code=subject_code, question_type=question_type, is_active=True
    ).all() if subject_code else []

    if not bank:
        return jsonify({'success': False, 'error': 'no_questions',
                         'message': f'No {question_type} questions available for {course_code} yet.'}), 200

    limit = MAX_CBT_QUESTIONS if question_type == 'cbt' else MAX_WRITTEN_QUESTIONS
    selected = random.sample(bank, min(limit, len(bank)))

    attempt = CBTAttempt(
        user_id=user.id, course_code=course_code, question_type=question_type,
        total_questions=len(selected), correct_count=0, score_pct=0,
        started_at=datetime.utcnow(),
    )
    attempt.issued_question_ids = [q.id for q in selected]
    db.session.add(attempt)
    db.session.commit()

    return jsonify({
        'success': True,
        'attempt_id': attempt.id,
        'course_code': course_code,
        'question_type': question_type,
        # include_answer defaults to False -- correct_index/explanation/mark_scheme are
        # never sent here, only after the student submits (see /CBT/submit/<id> below).
        'questions': [q.to_dict() for q in selected],
    })


@cbt_bp.route('/CBT/submit/<int:attempt_id>', methods=['POST'])
@login_required
@limiter.limit('60 per hour')
def submit_cbt_attempt(attempt_id):
    """Grades one attempt server-side and persists the authoritative result. The client
    sends only {answers: {question_id: selected_index_or_written_text}, duration_seconds}
    -- never a correct_index or a score. Every question actually graded/counted comes
    from attempt.issued_question_ids (set at /api/cbt/start time), not from whatever ids
    the client happens to submit, so a request can't invent extra questions, replay a
    different attempt's questions, or submit the same question twice to inflate a score.
    Rejects a second submission against an already-graded attempt outright."""
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 401

    attempt = CBTAttempt.query.filter_by(id=attempt_id, user_id=user.id).first()
    if not attempt:
        return jsonify({'success': False, 'error': 'Attempt not found'}), 404
    if attempt.submitted_at is not None:
        return jsonify({'success': False, 'error': 'This attempt was already submitted'}), 409

    issued_ids = attempt.issued_question_ids
    if not issued_ids:
        # Only possible for attempts created before this endpoint existed -- nothing to
        # grade against; refuse rather than guess.
        return jsonify({'success': False, 'error': 'This attempt has no issued questions to grade'}), 400

    data = request.get_json(silent=True) or {}
    raw_answers = data.get('answers') or {}
    # Client keys are strings (JSON object keys always are) -- normalize to int and drop
    # anything not in issued_ids so a submitted id that was never issued to THIS attempt
    # (a different attempt's question, or a made-up id) is silently ignored, not graded.
    answers_by_id = {}
    for k, v in raw_answers.items():
        try:
            qid = int(k)
        except (TypeError, ValueError):
            continue
        if qid in issued_ids:
            answers_by_id[qid] = v

    questions = {q.id: q for q in CBTQuestion.query.filter(CBTQuestion.id.in_(issued_ids)).all()}

    correct_count = 0
    results = []
    for qid in issued_ids:  # iterate the server's issued order, not the client's payload
        question = questions.get(qid)
        if not question:
            continue  # question was deleted/deactivated between issue and submit
        answer_value = answers_by_id.get(qid)
        is_correct = None
        selected_index, written_answer = None, None

        if attempt.question_type == 'cbt':
            try:
                selected_index = int(answer_value) if answer_value is not None else None
            except (TypeError, ValueError):
                selected_index = None
            is_correct = (selected_index is not None and selected_index == question.correct_index)
            if is_correct:
                correct_count += 1
        else:
            written_answer = str(answer_value) if answer_value is not None else None
            # Written answers stay self-marked (never auto-scored) -- unchanged from
            # before; is_correct stays None, correct_count/score_pct stay 0 for these.

        db.session.add(CBTAnswer(
            attempt_id=attempt.id, question_id=question.id, question_text=question.question_text,
            selected_index=selected_index, written_answer=written_answer, is_correct=is_correct,
        ))
        results.append({
            'question_id': question.id, 'question_text': question.question_text,
            'options': question.options, 'selected_index': selected_index,
            'written_answer': written_answer, 'correct_index': question.correct_index,
            'is_correct': is_correct, 'explanation': question.explanation,
            'mark_scheme': question.mark_scheme,
        })

    total = len(issued_ids)
    attempt.correct_count = correct_count
    attempt.score_pct = round(correct_count / total * 100) if total and attempt.question_type == 'cbt' else 0
    attempt.duration_seconds = data.get('duration_seconds')
    attempt.submitted_at = datetime.utcnow()
    db.session.commit()

    return jsonify({
        'success': True, 'attempt_id': attempt.id, 'course_code': attempt.course_code,
        'question_type': attempt.question_type, 'total_questions': total,
        'correct_count': correct_count, 'score_pct': attempt.score_pct,
        'duration_seconds': attempt.duration_seconds, 'results': results,
    })


@cbt_bp.route('/CBT/history')
@login_required
def cbt_history():
    """List the current user's past CBT practice attempts, newest first."""
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    attempts = CBTAttempt.query.filter_by(user_id=user.id).order_by(CBTAttempt.submitted_at.desc()).all()
    return render_template('cbt_history.html', attempts=attempts, user=user)


@cbt_bp.route('/CBT/attempts/<int:attempt_id>')
@login_required
def cbt_attempt_review(attempt_id):
    """Review one past attempt's questions/answers -- ownership-checked so a student
    can only ever review their own attempts."""
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    attempt = CBTAttempt.query.filter_by(id=attempt_id, user_id=user.id).first_or_404()
    answers = attempt.answers.all()

    # "Study this topic" -- only shown when the attempt's course_code actually
    # resolves to a real Course for this student; never a fabricated/dead link.
    ctx = resolve_academic_context(user)
    course = find_course(ctx.department, attempt.course_code) if ctx.department else None
    study_link = f"/courses/{course.code}" if course else None

    return render_template('cbt_attempt_review.html', attempt=attempt, answers=answers, study_link=study_link)


@cbt_bp.route('/api/cbt-summary')
@login_required
def cbt_summary():
    """{attempts_count, average_score, last_attempt} for the dashboard's Practice card
    and the course page's Progress section (pass ?course=CODE to scope to one course)."""
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    course_code = request.args.get('course', '').strip() or None
    return jsonify(get_cbt_summary(user, course_code))


@cbt_bp.route('/CBT/attempts/<int:attempt_id>/explain/<int:answer_id>', methods=['POST'])
@login_required
@limiter.limit('30 per hour')
def explain_cbt_answer(attempt_id, answer_id):
    """Closes the CBT learning loop: 'why was I wrong?' answered by the AI using only
    the exact question/answer/mark-scheme already captured on this attempt -- no
    fabricated context, no re-fetching unrelated material."""
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    attempt = CBTAttempt.query.filter_by(id=attempt_id, user_id=user.id).first_or_404()
    answer = CBTAnswer.query.filter_by(id=answer_id, attempt_id=attempt.id).first_or_404()

    if attempt.question_type == 'cbt':
        correct_text = ''
        if answer.question and answer.question.options:
            opts = answer.question.options
            if answer.question.correct_index is not None and 0 <= answer.question.correct_index < len(opts):
                correct_text = opts[answer.question.correct_index]
        selected_text = ''
        if answer.question and answer.question.options and answer.selected_index is not None:
            opts = answer.question.options
            if 0 <= answer.selected_index < len(opts):
                selected_text = opts[answer.selected_index]
        explanation_hint = (answer.question.explanation if answer.question else '') or ''
        prompt = (
            f"A Nigerian university student practicing {attempt.course_code} answered a multiple-choice "
            f"question wrong.\nQuestion: {answer.question_text}\n"
            f"Their answer: {selected_text or '(skipped)'}\nCorrect answer: {correct_text}\n"
            f"{f'Known explanation: {explanation_hint}' if explanation_hint else ''}\n\n"
            "In 2-4 short sentences, explain simply why the correct answer is right and why a student "
            "might have picked the wrong one. Be encouraging, not condescending."
        )
    else:
        prompt = (
            f"A Nigerian university student practicing {attempt.course_code} wrote this answer to a "
            f"written/essay question.\nQuestion: {answer.question_text}\n"
            f"Their answer: {answer.written_answer or '(no answer written)'}\n"
            f"{f'Mark scheme: {answer.question.mark_scheme}' if answer.question and answer.question.mark_scheme else ''}\n\n"
            "In 3-5 short sentences, give constructive feedback: what's good, what's missing, and one "
            "concrete tip to improve the answer."
        )

    try:
        headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json",
                   "HTTP-Referer": "https://nelavista.com", "X-Title": "Nelavista CBT Explain"}
        payload = {"model": "openai/gpt-4o-mini",
                   "messages": [{"role": "system", "content": "You are a concise, encouraging university tutor."},
                                {"role": "user", "content": prompt}],
                   "temperature": 0.4, "max_tokens": 300}
        resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            explanation = resp.json()["choices"][0]["message"]["content"]
            return jsonify({'success': True, 'explanation': explanation})
        debug_print(f"CBT explain API returned {resp.status_code}")
    except Exception as e:
        debug_print(f"CBT explain failed: {e}")
        traceback.print_exc()

    return jsonify({'success': False, 'explanation': "Nelavista couldn't generate an explanation right now — please try again."})
