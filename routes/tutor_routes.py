"""Nelavista AI Tutor -- the Academia-native, ChatGPT-quality conversational tutor.

Separate blueprint from routes/ai_routes.py's older single-shot endpoints (/ask,
/ask_with_files, the per-material/per-topic ai-action boxes) -- those stay exactly as
they are for backward compatibility. This is the new primary surface: persistent
threaded conversations, streamed responses, and live academic-context grounding.
"""
import json
import traceback
from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, session, jsonify, Response, stream_with_context

from extensions import db, limiter
from models import User, Course, Topic, Material, TutorConversation, TutorMessage, UserPreferences
from utils.helpers import login_required, debug_print
from services.academic_context import resolve_academic_context, find_course
from services.material_service import get_or_extract_material_text
from services.tutor_service import (
    build_tutor_system_prompt, stream_chat_completion, generate_conversation_title,
    build_quick_prompts, TUTOR_ACTIONS, lookup_mentioned_course_materials, message_wants_material_content,
)

tutor_bp = Blueprint('tutor', __name__)


def _current_user():
    username = session['user']['username']
    return User.query.filter_by(username=username).first()


def _resolve_context_from_args(user, ctx):
    """Shared by the page route and the create-conversation API -- resolves course/topic/
    material from query-string-style params, never inventing a course/topic that doesn't
    exist in the taxonomy (falls back to None, same as the rest of Academia)."""
    course_code = (request.values.get('course') or '').strip()
    topic_id = request.values.get('topic', type=int)
    material_id = request.values.get('material', type=int)

    topic = None
    course = None
    material = None

    if topic_id:
        topic = Topic.query.filter_by(id=topic_id, is_active=True).first()
        # Mirrors academia_routes.py's topic_detail() and ai_routes.py's
        # topic_ai_action() -- a topic whose course isn't in the requesting student's
        # own resolved department must never ground the tutor. Previously unchecked
        # here: passing another department's/university's real topic_id let the tutor
        # be grounded on content that topic's course_lookups/system-prompt building
        # would then treat as legitimately "the student's own topic".
        if topic and (not ctx.department or topic.course.department_id != ctx.department.id):
            topic = None
        if topic:
            course = topic.course
    if not course and course_code:
        course = find_course(ctx.department, course_code) if ctx.department else None
    if material_id:
        material = Material.query.filter_by(id=material_id, is_approved=True).first()
        # Mirrors ai_routes.py's material_ai_action() -- same university boundary every
        # other Material read path in the app already enforces (Material.university=NULL
        # is universal; a school-specific material is only for that school's own
        # students). Previously unchecked here: material_text below sends the file's
        # actual extracted content into the tutor's system prompt, so an unscoped
        # material_id was a real cross-university content leak, not just metadata.
        if material and material.university and user and user.university and material.university != user.university:
            material = None

    return course, topic, material


@tutor_bp.route('/ai-tutor')
@login_required
def ai_tutor_page():
    user = _current_user()
    ctx = resolve_academic_context(user)

    course, topic, material = _resolve_context_from_args(user, ctx)

    active_conversation = None
    conversation_id = request.args.get('conversation', type=int)
    if conversation_id:
        active_conversation = TutorConversation.query.filter_by(id=conversation_id, user_id=user.id).first()
        if active_conversation:
            course, topic, material = active_conversation.course, active_conversation.topic, active_conversation.material

    quick_prompts = build_quick_prompts(course=course, topic=topic, department=user.department)
    conversations = (TutorConversation.query.filter_by(user_id=user.id)
                      .order_by(TutorConversation.updated_at.desc()).limit(150).all())

    return render_template(
        'ai_tutor.html',
        user=user, course=course, topic=topic, material=material,
        active_conversation=active_conversation,
        quick_prompts=quick_prompts,
        conversations=[c.to_dict() for c in conversations],
        active_messages=[m.to_dict() for m in active_conversation.messages] if active_conversation else [],
        course_dict={'code': course.code, 'title': course.title} if course else None,
        topic_dict={'id': topic.id, 'title': topic.title} if topic else None,
        material_dict={'id': material.id, 'title': material.title} if material else None,
    )


@tutor_bp.route('/api/tutor/conversations', methods=['GET'])
@login_required
def list_conversations():
    user = _current_user()
    conversations = (TutorConversation.query.filter_by(user_id=user.id)
                      .order_by(TutorConversation.updated_at.desc()).limit(150).all())
    return jsonify({'success': True, 'conversations': [c.to_dict() for c in conversations]})


@tutor_bp.route('/api/tutor/conversations', methods=['POST'])
@login_required
def create_conversation():
    user = _current_user()
    ctx = resolve_academic_context(user)
    course, topic, material = _resolve_context_from_args(user, ctx)

    conversation = TutorConversation(
        user_id=user.id,
        course_id=course.id if course else None,
        topic_id=topic.id if topic else None,
        material_id=material.id if material else None,
    )
    db.session.add(conversation)
    db.session.commit()
    return jsonify({'success': True, 'conversation': conversation.to_dict()})


def _get_owned_conversation(conversation_id, user):
    return TutorConversation.query.filter_by(id=conversation_id, user_id=user.id).first()


@tutor_bp.route('/api/tutor/conversations/<int:conversation_id>', methods=['GET'])
@login_required
def get_conversation(conversation_id):
    user = _current_user()
    conversation = _get_owned_conversation(conversation_id, user)
    if not conversation:
        return jsonify({'success': False, 'error': 'Conversation not found'}), 404
    quick_prompts = build_quick_prompts(course=conversation.course, topic=conversation.topic, department=user.department)
    return jsonify({
        'success': True,
        'conversation': conversation.to_dict(),
        'messages': [m.to_dict() for m in conversation.messages],
        'quick_prompts': quick_prompts,
    })


@tutor_bp.route('/api/tutor/conversations/<int:conversation_id>', methods=['PATCH'])
@login_required
def rename_conversation(conversation_id):
    user = _current_user()
    conversation = _get_owned_conversation(conversation_id, user)
    if not conversation:
        return jsonify({'success': False, 'error': 'Conversation not found'}), 404
    title = (request.get_json(silent=True) or {}).get('title', '').strip()
    if not title:
        return jsonify({'success': False, 'error': 'Title cannot be empty'}), 400
    conversation.title = title[:200]
    db.session.commit()
    return jsonify({'success': True, 'conversation': conversation.to_dict()})


@tutor_bp.route('/api/tutor/conversations/<int:conversation_id>', methods=['DELETE'])
@login_required
def delete_conversation(conversation_id):
    user = _current_user()
    conversation = _get_owned_conversation(conversation_id, user)
    if not conversation:
        return jsonify({'success': False, 'error': 'Conversation not found'}), 404
    db.session.delete(conversation)
    db.session.commit()
    return jsonify({'success': True})


@tutor_bp.route('/api/tutor/conversations/<int:conversation_id>/messages', methods=['POST'])
@login_required
@limiter.limit('60 per hour')
def send_message(conversation_id):
    user = _current_user()
    conversation = _get_owned_conversation(conversation_id, user)
    if not conversation:
        return jsonify({'success': False, 'error': 'Conversation not found'}), 404

    body = request.get_json(silent=True) or {}
    content = (body.get('content') or '').strip()
    regenerate = bool(body.get('regenerate'))

    if not regenerate:
        if not content:
            return jsonify({'success': False, 'error': 'Message cannot be empty'}), 400
        db.session.add(TutorMessage(conversation_id=conversation.id, role='user', content=content))
        conversation.updated_at = datetime.utcnow()
        db.session.commit()
    else:
        # Query TutorMessage directly rather than through conversation.messages --
        # that relationship carries its own baked-in `order_by='TutorMessage.created_at'`
        # (ascending), and SQLAlchemy's .order_by() is ADDITIVE, not a replacement: chaining
        # .order_by(created_at.desc()) on the relationship produces
        # `ORDER BY created_at, created_at DESC`, where the relationship's ascending clause
        # wins first and the .desc() has no effect. That silently made "last_message" resolve
        # to the OLDEST message (the student's own first question) instead of the most recent
        # one, so a "role == assistant" check here never matched and regenerate never deleted
        # the previous answer -- it just appended a second one alongside it.
        last_message = (TutorMessage.query.filter_by(conversation_id=conversation.id)
                         .order_by(TutorMessage.created_at.desc()).first())
        if not last_message:
            return jsonify({'success': False, 'error': 'Nothing to regenerate yet'}), 400
        if last_message.role == 'assistant':
            db.session.delete(last_message)
            db.session.commit()
        last_user_message = (TutorMessage.query.filter_by(conversation_id=conversation.id, role='user')
                              .order_by(TutorMessage.created_at.desc()).first())
        if not last_user_message:
            return jsonify({'success': False, 'error': 'Nothing to regenerate yet'}), 400

    # The message actually driving this turn -- the student's fresh `content` for a new
    # message, or whichever user message is being re-answered on regenerate. Used below
    # to look up any course code the student mentioned, independent of whatever
    # course/topic/material the conversation happened to be opened with.
    turn_text = content if not regenerate else last_user_message.content
    course_lookups = lookup_mentioned_course_materials(user, turn_text)

    material_for_prompt = conversation.material
    if not material_for_prompt and course_lookups and message_wants_material_content(turn_text):
        # Only auto-select when exactly one course was mentioned and it has exactly one
        # material on file -- multiple candidates get listed (not guessed at) via
        # course_lookups below instead, so the student picks rather than the tutor
        # silently grounding on the wrong file.
        single_candidates = [entry for entry in course_lookups if len(entry['materials']) == 1]
        if len(single_candidates) == 1:
            material_for_prompt = single_candidates[0]['materials'][0]
            course_lookups = [entry for entry in course_lookups if entry is not single_candidates[0]]

    material_text = None
    if material_for_prompt:
        material_text = get_or_extract_material_text(material_for_prompt)

    prefs = UserPreferences.query.filter_by(user_id=user.id).first()
    system_prompt = build_tutor_system_prompt(
        user, course=conversation.course, topic=conversation.topic,
        material=material_for_prompt, material_text=material_text, prefs=prefs,
        course_lookups=course_lookups,
    )
    # Same additive-order_by pitfall as last_message above -- query TutorMessage directly
    # so .desc() actually takes effect and this grabs the most recent 30 turns (not the
    # oldest 30, which conversation.messages.order_by(...desc()) silently returned instead).
    history = (TutorMessage.query.filter_by(conversation_id=conversation.id)
               .order_by(TutorMessage.created_at.desc()).limit(30).all())
    history.reverse()
    messages = [{"role": "system", "content": system_prompt}]
    messages += [{"role": m.role, "content": m.content} for m in history]

    conversation_id_ = conversation.id
    course_ref = conversation.course

    def generate():
        chunks = []
        disconnected = False
        try:
            for delta in stream_chat_completion(messages):
                chunks.append(delta)
                yield f"data: {json.dumps({'delta': delta})}\n\n"
        except GeneratorExit:
            disconnected = True
            raise
        except Exception as e:
            debug_print(f"[tutor] stream error: {e}")
            traceback.print_exc()
        finally:
            text = ''.join(chunks).strip()
            new_title = None
            message_id = None
            if text:
                try:
                    convo = TutorConversation.query.get(conversation_id_)
                    msg = TutorMessage(conversation_id=conversation_id_, role='assistant', content=text)
                    db.session.add(msg)
                    convo.updated_at = datetime.utcnow()
                    db.session.commit()
                    message_id = msg.id
                    if convo.title is None:
                        first_user_msg = convo.messages.filter_by(role='user').order_by(TutorMessage.created_at).first()
                        if first_user_msg:
                            convo.title = generate_conversation_title(first_user_msg.content, course_ref)
                            db.session.commit()
                    new_title = convo.title
                except Exception as e:
                    db.session.rollback()
                    debug_print(f"[tutor] failed to persist assistant message: {e}")
            if not disconnected:
                yield f"data: {json.dumps({'done': True, 'message_id': message_id, 'title': new_title})}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'},
    )


@tutor_bp.route('/api/tutor/action-prompt', methods=['POST'])
@login_required
def action_prompt():
    """Backs the composer's capability menu (Explain / Step-by-step / Quiz / Practice /
    Summarize / Exam prep) -- turns a mode + the active course/topic/material into the
    actual message text to send, so the crafting logic lives in one place (services/
    tutor_service.TUTOR_ACTIONS) instead of being duplicated in the client."""
    user = _current_user()
    ctx = resolve_academic_context(user)
    body = request.get_json(silent=True) or {}
    mode = body.get('mode')
    if mode not in TUTOR_ACTIONS:
        return jsonify({'success': False, 'error': 'Unknown action'}), 400

    course, topic, material = _resolve_context_from_args(user, ctx)
    if topic:
        target = f"\"{topic.title}\" from {course.code}" if course else f"\"{topic.title}\""
    elif course:
        target = f"{course.code} — {course.title}"
    elif material:
        target = f"the material \"{material.title}\""
    else:
        target = "what I'm currently studying (ask me which course/topic first)"

    return jsonify({'success': True, 'prompt': TUTOR_ACTIONS[mode](target)})
