import traceback
from datetime import datetime
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from utils.helpers import login_required, debug_print
from models import User, CBTAttempt, CBTAnswer
from extensions import db
from config import OPENROUTER_API_KEY
from services.academic_context import resolve_academic_context, find_course
from services.progress_service import get_cbt_summary
import requests

cbt_bp = Blueprint('cbt', __name__)


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


@cbt_bp.route('/CBT/submit', methods=['POST'])
@login_required
def submit_cbt_attempt():
    """Persists one completed exam's score/answers. The client (CBT.html's
    submitExam()) already has everything it needs to score itself for the results
    screen the student sees immediately -- this just saves a copy of that so it's
    not lost the moment the tab closes. Called fire-and-forget from the client; a
    failure here must never block or alter the results the student already sees."""
    data = request.get_json(silent=True) or {}
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 401

    course_code = (data.get('course_code') or '').strip().upper()
    question_type = data.get('question_type')
    questions = data.get('questions') or []
    if not course_code or question_type not in ('cbt', 'written') or not questions:
        return jsonify({'success': False, 'error': 'Missing/invalid attempt data'}), 400

    if question_type == 'cbt':
        correct = sum(1 for q in questions if q.get('selected_index') == q.get('correct_index'))
    else:
        correct = 0  # written answers are self-marked client-side only, never auto-scored here
    total = len(questions)

    attempt = CBTAttempt(
        user_id=user.id, course_code=course_code, question_type=question_type,
        total_questions=total, correct_count=correct,
        score_pct=round(correct / total * 100) if total and question_type == 'cbt' else 0,
        duration_seconds=data.get('duration_seconds'), submitted_at=datetime.utcnow(),
    )
    db.session.add(attempt)
    db.session.flush()

    for q in questions:
        db.session.add(CBTAnswer(
            attempt_id=attempt.id,
            question_text=q.get('question_text', ''),
            selected_index=q.get('selected_index'),
            written_answer=q.get('written_answer'),
            is_correct=(q.get('selected_index') == q.get('correct_index')) if question_type == 'cbt' else None,
        ))
    db.session.commit()
    return jsonify({'success': True, 'attempt_id': attempt.id})


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
