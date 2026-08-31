import os
import json
import uuid
import base64
import shutil
import time
import traceback
from datetime import datetime
from models import User, Material, AnalyzerSession, Topic
from flask import Blueprint, render_template, request, session, jsonify, send_from_directory, current_app
from utils.helpers import login_required, debug_print, get_session_memory, add_to_session_memory, cleanup_old_files, allowed_file
from services.material_service import extract_text_from_pdf, extract_text_from_pdf_turbo, extract_images_from_pdf, extract_tables_from_pdf, analyze_document_structure, extract_text_from_image, is_diagram_or_visual
from services.ai_service import generate_turbo_style_notes, safe_markdown_to_html, generate_test_questions
from services.academic_context import resolve_academic_context, find_course
from models import UserQuestions, UserPreferences
from extensions import db, limiter
import requests
from config import OPENROUTER_API_KEY

ai_bp = Blueprint('ai', __name__)


# ===== SERVER-SIDE ANALYZER CONTENT STORE =====
# Extracted PDF text/tables/images/notes are too large for Flask's default client-side
# cookie session (capped at ~4KB by browser/RFC limits — a single lecture-notes PDF's
# extracted text alone routinely exceeds that, and the browser just silently drops or
# truncates an oversized cookie). Only a small pointer lives in session['analyzer_content'];
# the actual payload lives in the AnalyzerSession table (see models.py) -- previously a
# JSON file under IMAGE_FOLDER/<session_id>/content.json, which Render's ephemeral
# filesystem silently destroyed on every redeploy/restart.
def _save_content(session_id, content):
    username = session.get('user', {}).get('username')
    user = User.query.filter_by(username=username).first() if username else None
    row = AnalyzerSession.query.filter_by(session_id=session_id).first()
    if not row:
        row = AnalyzerSession(session_id=session_id)
        db.session.add(row)
    row.user_id = user.id if user else None
    row.content_json = json.dumps(content)
    db.session.commit()


def _load_content(session_id):
    row = AnalyzerSession.query.filter_by(session_id=session_id).first()
    if not row:
        return None
    try:
        return json.loads(row.content_json)
    except Exception as e:
        debug_print(f"⚠️ Failed to load analyzer content for {session_id}: {e}")
        return None


def _build_course_materials_block(user, course_code):
    """When the student is asking from within a specific course's context, tell the
    tutor exactly what's available for that course -- titles/descriptions only, never
    claimed as full text the model has read -- so it can decline honestly instead of
    inventing course-specific facts (exact lecture content, past-question answers,
    claims about 'what the course covers') when the real material doesn't back it up.
    Returns '' when course_code is absent, so every existing caller (which never sends
    one today) gets byte-identical behavior to before this was added."""
    if not course_code:
        return ""
    ctx = resolve_academic_context(user)
    course = find_course(ctx.department, course_code) if ctx.department else None
    if not course:
        return ""
    materials = Material.query.filter(
        Material.course_code.ilike(course.code), Material.is_approved == True  # noqa: E712
    ).limit(8).all()
    if materials:
        lines = [f"- {m.title}" + (f": {m.description}" if m.description else "") for m in materials]
        return (
            f"\n\n## AVAILABLE COURSE MATERIALS for {course.code} — {course.title}\n"
            + "\n".join(lines)
            + "\n\nThese are titles/descriptions only -- you have not read their full text. "
            "If the student asks something these titles don't clearly cover, say so honestly "
            "and answer from general subject knowledge instead of inventing course-specific "
            "facts (exact lecture content, past-question answers, or claims about what this "
            "course covers beyond these titles)."
        )
    return (
        f"\n\n## COURSE CONTEXT\nThe student is asking about {course.code} — {course.title}, but no "
        "study materials have been uploaded for it on Nelavista yet. Do not claim to have or "
        "reference any course materials for it; answer from general subject knowledge."
    )


_RESPONSE_STYLE_INSTRUCTIONS = {
    'concise': "Keep answers tight -- the shortest response that actually answers the question, minimal elaboration.",
    'balanced': "Match length to the question -- a quick question gets a focused answer, a genuinely complex one gets a fuller explanation.",
    'detailed': "Prefer thorough, fully worked-through explanations, even for questions that could technically be answered briefly.",
}
_TEACHING_APPROACH_INSTRUCTIONS = {
    'step_by_step': "Teach by breaking everything into clear, numbered steps the student can follow in order.",
    'concept_first': "Lead with the underlying concept/intuition before any steps or formulas -- make sure the 'why' lands before the 'how'.",
    'example_first': "Lead with a concrete worked example, then generalize into the underlying concept/rule.",
    'exam_focused': "Frame explanations around what's likely to be tested -- key definitions, common exam question patterns, and typical mistakes to avoid.",
}
_DIFFICULTY_INSTRUCTIONS = {
    'beginner': "Assume no prior background -- define terms before using them, avoid jargon, favor simple language.",
    'university': "Assume standard Nigerian university-level background for this student's level -- normal course terminology is fine.",
    'advanced': "Assume strong prior background -- move quickly past basics, use precise technical language, go deeper than a standard lecture would.",
}


def _get_user_preferences(user):
    if not user:
        return None
    return UserPreferences.query.filter_by(user_id=user.id).first()


def _build_personalization_block(prefs):
    """Settings > AI Tutor -- turns response depth / teaching approach / difficulty /
    personal context into explicit instructions in the system prompt. Falls back to the
    same defaults models.UserPreferences.DEFAULTS uses when the student has no row yet
    (prefs is None), so /ask behaves identically to before this existed until someone
    actually visits Settings and changes something."""
    style = prefs.ai_response_style if prefs else 'balanced'
    approach = prefs.ai_teaching_approach if prefs else 'step_by_step'
    difficulty = prefs.ai_difficulty if prefs else 'university'

    lines = [
        "\n## PERSONALIZATION (from this student's Settings)",
        f"- Response depth: {_RESPONSE_STYLE_INSTRUCTIONS.get(style, _RESPONSE_STYLE_INSTRUCTIONS['balanced'])}",
        f"- Teaching approach: {_TEACHING_APPROACH_INSTRUCTIONS.get(approach, _TEACHING_APPROACH_INSTRUCTIONS['step_by_step'])}",
        f"- Difficulty level: {_DIFFICULTY_INSTRUCTIONS.get(difficulty, _DIFFICULTY_INSTRUCTIONS['university'])}",
    ]
    personal_context = (prefs.ai_personal_context if prefs else None) or ''
    personal_context = personal_context.strip()
    if personal_context:
        lines.append(f"- Additional context this student shared about themselves: {personal_context}")
    return "\n".join(lines)


def _build_history_messages(user, prefs):
    """Settings > AI Tutor > 'Use my previous conversations for continuity'. ON (default):
    pulls the student's real, persistent AI Tutor history from UserQuestions -- carries
    over across logins/devices, not just the current Flask session. OFF: no prior turns at
    all, every message starts a fresh conversation. Only applies to this single-shot /ask
    endpoint -- the newer /ai-tutor (services/tutor_service.py) has real conversation
    threads instead, where continuity is just the thread itself."""
    use_history = prefs.ai_use_conversation_history if prefs else True
    if not use_history or not user:
        return []
    recent = (UserQuestions.query.filter_by(username=user.username)
              .order_by(UserQuestions.timestamp.desc()).limit(5).all())
    recent.reverse()
    messages = []
    for q in recent:
        messages.append({"role": "user", "content": q.question})
        messages.append({"role": "assistant", "content": q.answer})
    return messages


# The Flask-wide MAX_CONTENT_LENGTH (100MB, config.py) exists to reject absurd uploads
# outright, but a 100MB PDF is still well within that limit and would tie up the single
# eventlet worker handling it for a long time -- pdfplumber/PyMuPDF extraction is
# CPU-bound C-extension work that does NOT yield to eventlet's cooperative scheduler, so
# a huge/complex PDF here blocks every other concurrent student's request too, not just
# the uploader's. This caps synchronous PDF-analysis uploads specifically, well below the
# app-wide ceiling, independent of the general upload limit used elsewhere (materials,
# videos). A real fix (background job queue) is out of scope for this pass -- see the
# Level 1 audit's scale findings -- this bounds the worst case in the meantime.
MAX_ANALYZE_PDF_BYTES = 20 * 1024 * 1024  # 20MB


def _reject_if_too_large(file_content_or_size, max_bytes=MAX_ANALYZE_PDF_BYTES):
    size = file_content_or_size if isinstance(file_content_or_size, int) else len(file_content_or_size)
    if size > max_bytes:
        return jsonify({
            "success": False,
            "error": f"That PDF is too large to analyze ({size // (1024*1024)}MB). "
                     f"Please upload a file under {max_bytes // (1024*1024)}MB.",
        }), 413
    return None


@ai_bp.route('/analyze')
@login_required
def analyze_page():
    user = session.get('user')
    return render_template('analyze.html', user=user)

@ai_bp.route('/analyze', methods=['POST'])
@login_required
@limiter.limit('15 per hour')
def analyze_pdf():
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "No file uploaded"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "error": "No file selected"}), 400
        if not allowed_file(file.filename):
            return jsonify({"success": False, "error": "Only PDF files are supported"}), 400
        session_id = str(uuid.uuid4())
        file_content = file.read()
        if len(file_content) == 0:
            return jsonify({"success": False, "error": "Uploaded file is empty"}), 400
        too_large = _reject_if_too_large(file_content)
        if too_large:
            return too_large
        from io import BytesIO
        file_streams = [BytesIO(file_content) for _ in range(3)]
        text = extract_text_from_pdf_turbo(file_streams[0])
        if not text or len(text.strip()) < 100:
            return jsonify({"success": False, "error": "PDF is unreadable or contains too little text"}), 400
        images = extract_images_from_pdf(file_streams[1], session_id)
        tables = extract_tables_from_pdf(file_streams[2])
        document_analysis = analyze_document_structure(text)
        content = {
            "type": "pdf", "text": text, "images": images, "tables": tables,
            "document_analysis": document_analysis, "filename": file.filename,
            "session_id": session_id, "timestamp": datetime.utcnow().isoformat(),
            "text_length": len(text), "image_count": len(images), "table_count": len(tables)
        }
        _save_content(session_id, content)
        session['analyzer_content'] = {"session_id": session_id, "type": "pdf", "filename": file.filename}
        return jsonify({"success": True, "filename": file.filename, "text_length": len(text),
                        "image_count": len(images), "table_count": len(tables),
                        "preview": text[:500] + "..." if len(text) > 500 else text,
                        "session_id": session_id, "main_topics": document_analysis.get('main_topics', [])[:3]})
    except Exception as e:
        debug_print(f"❌ Analyze error: {str(e)}")
        traceback.print_exc()
        return jsonify({"success": False, "error": f"Processing failed: {str(e)}"}), 500

@ai_bp.route('/understand', methods=['POST'])
@login_required
@limiter.limit('20 per hour')
def understand_content():
    try:
        pointer = session.get('analyzer_content')
        if not pointer:
            return jsonify({"success": False, "error": "No PDF uploaded. Please upload a PDF first."}), 400
        content = _load_content(pointer.get('session_id', ''))
        if not content:
            return jsonify({"success": False, "error": "Session expired. Please upload the PDF again."}), 400
        text = content.get("text", "")
        images = content.get("images", [])
        tables = content.get("tables", [])
        document_analysis = content.get("document_analysis", {})
        filename = content.get("filename", "Study Material")
        if not text or len(text.strip()) < 100:
            return jsonify({"success": False, "error": "Uploaded PDF content is insufficient for analysis."}), 400
        notes = generate_turbo_style_notes(text, tables, images, filename, document_analysis)
        content["generated_notes"] = notes
        content["notes_timestamp"] = datetime.utcnow().isoformat()
        content["markdown"] = notes
        _save_content(content["session_id"], content)
        image_urls = []
        for img in images[:5]:
            if os.path.exists(img.get("path", "")):
                image_urls.append({"url": img.get("url", ""), "alt": img.get("alt", "Diagram"), "page": img.get("page", 1)})
        table_data = []
        for table in tables[:5]:
            table_data.append({"markdown": table.get("markdown", ""), "page": table.get("page", 1), "preview": table.get("text", "")[:150] + "..."})
        return jsonify({"success": True, "mode": "turbo_comprehensive", "markdown": notes, "filename": filename,
                        "images": image_urls, "tables": table_data, "note_type": "lecture_textbook_style",
                        "word_count": len(notes.split()), "has_tables": len(tables) > 0, "has_images": len(images) > 0})
    except Exception as e:
        debug_print(f"[UNDERSTAND] Error: {e}")
        traceback.print_exc()
        return jsonify({"success": False, "error": f"Failed to generate comprehensive notes: {str(e)}"}), 500

@ai_bp.route('/generate-test', methods=['POST'])
@login_required
@limiter.limit('15 per hour')
def generate_test():
    """Backs the "Test Yourself" option on /analyze — templates/analyze.html's
    generateTest() posts a PDF or image plus test_type ('cbt' or 'written') here and
    expects {"success": true, "filename": ..., "questions": [...]} back. This endpoint
    never existed before; the button called it and always 404'd."""
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "No file uploaded"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "error": "No file selected"}), 400

        test_type = request.form.get('test_type', 'cbt')
        if test_type not in ('cbt', 'written'):
            test_type = 'cbt'

        filename_lower = file.filename.lower()
        source_text = ""

        if filename_lower.endswith('.pdf'):
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            too_large = _reject_if_too_large(file_size)
            if too_large:
                return too_large
            source_text = extract_text_from_pdf_turbo(file)
        elif filename_lower.endswith(('.png', '.jpg', '.jpeg')):
            # No reliable OCR available (see services/material_service.py) — send the
            # image straight to a vision model to describe/transcribe its content, same
            # pattern already used by ask_with_files() for image attachments.
            file.seek(0)
            image_bytes = file.read()
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            mime_type = 'image/png' if filename_lower.endswith('.png') else 'image/jpeg'
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://nelavista.com",
                "X-Title": "Nelavista Test Generator"
            }
            payload = {
                "model": "openai/gpt-4o",
                "messages": [{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Transcribe all readable text and describe the academic content of this image in detail, so it can be used as source material for writing exam questions."},
                        {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{image_base64}"}}
                    ]
                }],
                "temperature": 0.2,
                "max_tokens": 1500
            }
            vision_resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=60)
            if vision_resp.status_code == 200:
                source_text = vision_resp.json()["choices"][0]["message"]["content"]
        else:
            return jsonify({"success": False, "error": "Please upload a PDF or image file (PDF, JPG, PNG)"}), 400

        if not source_text or len(source_text.strip()) < 100:
            return jsonify({"success": False, "error": "Could not read enough content from this file to generate a test"}), 400

        questions = generate_test_questions(source_text, test_type=test_type, filename=file.filename)
        return jsonify({"success": True, "filename": file.filename, "test_type": test_type, "questions": questions})
    except Exception as e:
        debug_print(f"[GENERATE-TEST] Error: {e}")
        traceback.print_exc()
        return jsonify({"success": False, "error": f"Test generation failed: {str(e)}"}), 500

@ai_bp.route('/analyzer/clear', methods=['POST'])
@login_required
def clear_analyzer_content():
    try:
        pointer = session.get('analyzer_content', {})
        session_id = pointer.get('session_id')
        if session_id:
            session_folder = os.path.join(current_app.config['IMAGE_FOLDER'], session_id)
            if os.path.exists(session_folder):
                shutil.rmtree(session_folder)
        if 'analyzer_content' in session:
            session.pop('analyzer_content')
        return jsonify({"success": True, "message": "Content cleared successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": f"Error clearing content: {str(e)}"}), 500

@ai_bp.route('/analyzer/status', methods=['GET'])
@login_required
def get_analyzer_status():
    try:
        pointer = session.get('analyzer_content')
        content = _load_content(pointer.get('session_id', '')) if pointer else None
        if content and content.get('type') == 'pdf':
            has_notes = 'generated_notes' in content
            return jsonify({"success": True, "has_content": True, "has_notes": has_notes,
                            "content_type": 'pdf', "filename": content.get('filename'),
                            "image_count": len(content.get('images', [])), "table_count": len(content.get('tables', [])),
                            "text_length": len(content.get('text', '')), "notes_length": len(content.get('generated_notes', '')) if has_notes else 0,
                            "session_id": content.get('session_id', 'unknown')})
        else:
            return jsonify({"success": True, "has_content": False, "has_notes": False, "message": "No PDF content uploaded"})
    except Exception as e:
        return jsonify({"success": False, "error": f"Error getting status: {str(e)}"}), 500

@ai_bp.route('/static/extracted_images/<path:filename>')
@login_required
def serve_extracted_image(filename):
    try:
        return send_from_directory(current_app.config['IMAGE_FOLDER'], filename)
    except Exception as e:
        debug_print(f"Error serving image {filename}: {e}")
        return "Image not found", 404

@ai_bp.route('/talk-to-nelavista')
@login_required
def talk_to_nelavista():
    return render_template('talk-to-nelavista.html')

@ai_bp.route('/ask_with_files', methods=['POST'])
@login_required
@limiter.limit('20 per hour')
def ask_with_files():
    GRACEFUL_FALLBACK = "I'm having a little trouble answering right now, but please try again."
    try:
        username = session['user']['username']
        # Fetch user profile from database
        user = User.query.filter_by(username=username).first()
        user_name = user.name if user and user.name else username
        user_department = user.department if user and user.department else "not specified"
        user_level = user.level if user and user.level else "not specified"
        user_university = user.university if user and user.university else "not specified"
        user_faculty = user.faculty if user and user.faculty else "not specified"

        message = request.form.get('message', '').strip()
        course_materials_block = _build_course_materials_block(user, request.form.get('course_code', '').strip())
        session_memory = get_session_memory()
        file_texts = []
        vision_images = []
        if 'files' in request.files:
            files = request.files.getlist('files')
            for file in files:
                if file and file.filename:
                    filename = file.filename.lower()
                    if filename.endswith('.pdf'):
                        text = extract_text_from_pdf(file)
                        if text:
                            file_texts.append(f"[PDF: {file.filename}]\n{text}")
                    elif filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        file.seek(0)
                        image_bytes = file.read()
                        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                        mime_type = 'image/png' if filename.endswith('.png') else 'image/gif' if filename.endswith('.gif') else 'image/jpeg'
                        vision_images.append({'base64': image_base64, 'mime_type': mime_type, 'filename': file.filename})
        user_content_parts = []
        if message:
            user_content_parts.append(message)
        if file_texts:
            user_content_parts.append("DOCUMENT CONTENT:\n" + "\n\n".join(file_texts))
        if not user_content_parts and not vision_images:
            return jsonify({"success": True, "answer": "Please provide a message or upload files for analysis."})
        user_content = "\n\n".join(user_content_parts) if user_content_parts else "Please analyze the uploaded image(s)."

        system_prompt = f"""You are Nelavista, an advanced AI tutor created by Afeez Adewale Tella for Nigerian university students (100–400 level).

## STUDENT CONTEXT
- Name: {user_name}
- Department: {user_department}
- Academic Level: {user_level}
- University: {user_university}
- Faculty: {user_faculty}
{course_materials_block}

Use this information to personalise your responses. Address the student by their name occasionally, and tailor examples to their department or level when relevant.

## YOUR ROLE
You are a professional, friendly university‑level tutor who makes learning enjoyable. Your answers should feel like a conversation with a brilliant, approachable lecturer.

## YOUR GOAL
Teach clearly, patiently, and in a way students love to read and keep using. Every response should be a mini‑lesson that is both informative and inviting.

## TEACHING STYLE
- **Start with a warm, encouraging opening** – e.g., "Great question!", "Let's dive into that together.", "That's an excellent topic to explore."
- **Use headings (`<h2>`, `<h3>`) to structure longer explanations** – for multi‑part answers, use headings to guide the reader. For simple or introductory responses (e.g., "What can you teach me?"), you may start directly with a warm opening paragraph **without** a heading. Avoid headings that merely repeat the user's question.
- **Use short paragraphs** – no more than 3–4 sentences each. Keep each paragraph focused on one idea.
- **Use bullet points** (`<ul>`) for lists of key points, examples, or summaries.
- **Use numbered lists** (`<ol>`) for step‑by‑step processes.
- **Emphasise important terms** with `<strong>` or `<em>`.
- **Explain each step in words** when solving problems, before or after showing the math.
- **Use simple, relatable language**, but never sacrifice accuracy. Include real‑world examples or analogies when helpful.
- **End with a short, encouraging conclusion** or a “next steps” suggestion to keep the student engaged.

## STRUCTURE (HTML)
- `<h2>` for main sections.
- `<h3>` for subsections if needed.
- `<p>` for explanatory text.
- `<ul>` / `<li>` for unordered lists.
- `<ol>` / `<li>` for ordered lists.
- Use `<strong>` for bold, `<em>` for italics.
- Present ideas in a logical order: introduction → explanation → steps (if applicable) → conclusion/summary.

## FORMAT RULES (STRICT)
- **Output pure HTML** – no Markdown syntax whatsoever.
- Do **not** wrap the whole answer in `<html>` or `<body>` tags.
- Do **not** include code blocks.
- Use only valid HTML tags as listed above.
- **Emojis are allowed occasionally** in headings to make them visually inviting (e.g., 📘 **Core Concepts**, 💡 **Tip**, ✅ **Key Takeaway**). Use at most one emoji per section; do not overdo it.
- If you include mathematics, use LaTeX:
- Inline math: `\\( ... \\)`
- Display math: `$$ ... $$`

## LATEX RULES
- Every mathematical expression must be **complete** inside a single `\\( ... \\)` or `$$ ... $$` block.
- **Never split** one formula across multiple lines or tags.
- **Never break** fractions, powers, roots, or equations into pieces.
- Do **not** mix normal text inside math expressions.
- Prefer `$$ ... $$` for important equations or multi‑step derivations.

## TONE
- Warm, supportive, and enthusiastic.
- Avoid being robotic or too formal.
- Use phrases like “Let’s break this down”, “Think of it this way”, “You’ll often see this in…”.
- Sound like a real teacher who genuinely wants the student to understand.

## EXAMPLES
**For a detailed topic (use heading):**
> <h2>📘 Understanding Cellular Respiration</h2>
> <p>That's an excellent question! Cellular respiration is how your cells turn food into energy – think of it as the cell's power plant. Let’s explore it step by step.</p>

**For a simple introductory question (no heading):**
> <p>Great question! I can help you with a wide range of university subjects – from Mathematics and Sciences to Computer Science, Social Sciences, Literature, and more. Just tell me what topic you'd like to explore, and we'll dive right in!</p>

Your final answer should be so clear and pleasant that a student would *want* to read it and come back for more."""

        messages = [{"role": "system", "content": system_prompt}]
        for mem in session_memory:
            messages.append({"role": mem["role"], "content": mem["content"]})
        openrouter_model = "openai/gpt-4o-mini"
        if vision_images:
            content_parts = [{"type": "text", "text": user_content}]
            for image_data in vision_images:
                content_parts.append({"type": "image_url", "image_url": {"url": f"data:{image_data['mime_type']};base64,{image_data['base64']}"}})
            messages.append({"role": "user", "content": content_parts})
            openrouter_model = "openai/gpt-4o"
        else:
            messages.append({"role": "user", "content": user_content})

        headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json", "HTTP-Referer": "https://nelavista.com", "X-Title": "Nelavista AI Tutor"}
        payload = {"model": openrouter_model, "messages": messages, "temperature": 0.5, "max_tokens": 1500}

        # Retry logic with increased timeout
        max_retries = 2
        retry_delay = 2
        ai_response = None
        for attempt in range(max_retries + 1):
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                if response.status_code == 200:
                    response_json = response.json()
                    ai_response = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")
                    if ai_response and ai_response.strip():
                        break
                    else:
                        ai_response = None
                else:
                    debug_print(f"API returned {response.status_code}, retry {attempt+1}/{max_retries}")
            except requests.exceptions.Timeout:
                debug_print(f"Timeout on attempt {attempt+1}/{max_retries}")
                if attempt == max_retries:
                    ai_response = None
                else:
                    time.sleep(retry_delay)
            except Exception as e:
                debug_print(f"API error: {e}")
                if attempt == max_retries:
                    ai_response = None
                else:
                    time.sleep(retry_delay)

        if not ai_response:
            final_answer = GRACEFUL_FALLBACK
        else:
            final_answer = ai_response

        try:
            question_record = UserQuestions(username=username, question=user_content, answer=final_answer, memory_layer='chat')
            db.session.add(question_record)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            debug_print(f"Failed to save message: {e}")
        add_to_session_memory("user", user_content)
        add_to_session_memory("assistant", final_answer)
        cleanup_old_files()
        return jsonify({"success": True, "answer": final_answer})
    except Exception as e:
        debug_print(f"Unhandled error in /ask_with_files: {e}")
        traceback.print_exc()
        return jsonify({"success": True, "answer": GRACEFUL_FALLBACK})

@ai_bp.route('/ask', methods=['POST'])
@login_required
@limiter.limit('40 per hour')
def ask():
    GRACEFUL_FALLBACK = "I'm having a little trouble answering right now, but please try again."
    try:
        data = request.get_json() or {}
        message = data.get('message', '').strip()
        if not message:
            return jsonify({'error': 'No question provided'}), 400
        username = session['user']['username']
        # Fetch user profile from database
        user = User.query.filter_by(username=username).first()
        user_name = user.name if user and user.name else username
        prefs = _get_user_preferences(user)
        use_academic_context = prefs.ai_use_academic_context if prefs else True

        if use_academic_context:
            student_context_block = f"""## STUDENT CONTEXT
- Name: {user_name}
- Department: {user.department if user and user.department else "not specified"}
- Academic Level: {user.level if user and user.level else "not specified"}
- University: {user.university if user and user.university else "not specified"}
- Faculty: {user.faculty if user and user.faculty else "not specified"}"""
            personalise_line = "Use this information to personalise your responses. Address the student by their name occasionally, and tailor examples to their department or level when relevant."
        else:
            # "Use my academic context" is OFF (Settings > AI Tutor > Personalization) --
            # the student chose not to have their university/faculty/department/level
            # shared with the tutor, so only their display name is used.
            student_context_block = f"## STUDENT CONTEXT\n- Name: {user_name}"
            personalise_line = "The student has turned off academic-context personalization -- do not guess or assume their department, level, or university."
        course_materials_block = _build_course_materials_block(user, (data.get('course_code') or '').strip()) if use_academic_context else ""
        personalization_block = _build_personalization_block(prefs)

        system_prompt = f"""You are Nelavista, an advanced AI tutor created by Afeez Adewale Tella for Nigerian university students (100–400 level).

{student_context_block}
{course_materials_block}
{personalization_block}

{personalise_line}

## YOUR ROLE
You are a professional, friendly university‑level tutor who makes learning enjoyable. Your answers should feel like a conversation with a brilliant, approachable lecturer.

## YOUR GOAL
Teach clearly, patiently, and in a way students love to read and keep using. Every response should be a mini‑lesson that is both informative and inviting.

## TEACHING STYLE
- **Start with a warm, encouraging opening** – e.g., "Great question!", "Let's dive into that together.", "That's an excellent topic to explore."
- **Break the explanation into clear sections** with descriptive headings (`<h2>`, `<h3>`). Use headings to guide the reader through the logic.
- **Use short paragraphs** – no more than 3–4 sentences each. Keep each paragraph focused on one idea.
- **Use bullet points** (`<ul>`) for lists of key points, examples, or summaries.
- **Use numbered lists** (`<ol>`) for step‑by‑step processes.
- **Emphasise important terms** with `<strong>` or `<em>`.
- **Explain each step in words** when solving problems, before or after showing the math.
- **Use simple, relatable language**, but never sacrifice accuracy. Include real‑world examples or analogies when helpful.
- **End with a short, encouraging conclusion** or a “next steps” suggestion to keep the student engaged.

## STRUCTURE (HTML)
- `<h2>` for main sections.
- `<h3>` for subsections if needed.
- `<p>` for explanatory text.
- `<ul>` / `<li>` for unordered lists.
- `<ol>` / `<li>` for ordered lists.
- Use `<strong>` for bold, `<em>` for italics.
- Present ideas in a logical order: introduction → explanation → steps (if applicable) → conclusion/summary.

## FORMAT RULES (STRICT)
- **Output pure HTML** – no Markdown syntax whatsoever.
- Do **not** wrap the whole answer in `<html>` or `<body>` tags.
- Do **not** include code blocks.
- Use only valid HTML tags as listed above.
- **Emojis are allowed occasionally** in headings to make them visually inviting (e.g., 📘 **Core Concepts**, 💡 **Tip**, ✅ **Key Takeaway**). Use at most one emoji per section; do not overdo it.
- If you include mathematics, use LaTeX:
- Inline math: `\\( ... \\)`
- Display math: `$$ ... $$`

## LATEX RULES
- Every mathematical expression must be **complete** inside a single `\\( ... \\)` or `$$ ... $$` block.
- **Never split** one formula across multiple lines or tags.
- **Never break** fractions, powers, roots, or equations into pieces.
- Do **not** mix normal text inside math expressions.
- Prefer `$$ ... $$` for important equations or multi‑step derivations.

## TONE
- Warm, supportive, and enthusiastic.
- Avoid being robotic or too formal.
- Use phrases like “Let’s break this down”, “Think of it this way”, “You’ll often see this in…”.
- Sound like a real teacher who genuinely wants the student to understand.

## EXAMPLE OPENING
> **<h2>📘 Understanding Cellular Respiration</h2>**
> <p>That's an excellent question! Cellular respiration is how your cells turn food into energy – think of it as the cell's power plant. Let’s explore it step by step.</p>

Your final answer should be so clear and pleasant that a student would *want* to read it and come back for more."""

        messages = [{"role": "system", "content": system_prompt}]
        messages += _build_history_messages(user, prefs)
        messages.append({"role": "user", "content": message})

        headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json", "HTTP-Referer": "https://nelavista.com", "X-Title": "Nelavista AI Tutor"}
        payload = {"model": "openai/gpt-4o-mini", "messages": messages, "temperature": 0.5, "max_tokens": 1500}

        # Retry logic with increased timeout
        max_retries = 2
        retry_delay = 2
        ai_response = None
        for attempt in range(max_retries + 1):
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                if response.status_code == 200:
                    response_json = response.json()
                    ai_response = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")
                    if ai_response and ai_response.strip():
                        break
                    else:
                        ai_response = None
                else:
                    debug_print(f"API returned {response.status_code}, retry {attempt+1}/{max_retries}")
            except requests.exceptions.Timeout:
                debug_print(f"Timeout on attempt {attempt+1}/{max_retries}")
                if attempt == max_retries:
                    ai_response = None
                else:
                    time.sleep(retry_delay)
            except Exception as e:
                debug_print(f"API error: {e}")
                if attempt == max_retries:
                    ai_response = None
                else:
                    time.sleep(retry_delay)

        if not ai_response:
            final_answer = GRACEFUL_FALLBACK
        else:
            final_answer = ai_response

        try:
            question_record = UserQuestions(username=username, question=message, answer=final_answer, memory_layer='chat')
            db.session.add(question_record)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            debug_print(f"Failed to save message: {e}")
        add_to_session_memory("user", message)
        add_to_session_memory("assistant", final_answer)
        return jsonify({"success": True, "answer": final_answer})
    except Exception as e:
        debug_print(f"Unhandled error in /ask: {e}")
        traceback.print_exc()
        return jsonify({"success": True, "answer": GRACEFUL_FALLBACK})

_MATERIAL_AI_MODES = {
    'explain': "Explain this material's content clearly, in plain language, as if teaching a "
               "university student who hasn't read it yet. Break it into a few key ideas.",
    'summarize': "Summarize this material's content into a concise study summary covering its "
                 "main points, organized with short headings or bullet points.",
    'quiz': "Based on this material's content, write 5 short practice questions (with answers) "
            "a student could use to test themselves. Only ask about things actually covered in the text.",
}


@ai_bp.route('/api/materials/<int:material_id>/ai-action', methods=['POST'])
@login_required
@limiter.limit('30 per hour')
def material_ai_action(material_id):
    """Ask Nelavista about ONE specific material, grounded in its real extracted text
    (not just its title) -- this is genuine retrieval, not a title-only guess. If the
    file can't be downloaded/read, says so honestly instead of answering as if it had."""
    from services.material_service import get_or_extract_material_text

    material = Material.query.get(material_id)
    if not material or not material.is_approved:
        return jsonify({'success': False, 'error': 'Material not found'}), 404

    mode = (request.get_json(silent=True) or {}).get('mode', 'explain')
    if mode not in _MATERIAL_AI_MODES:
        mode = 'explain'

    text = get_or_extract_material_text(material)
    if not text:
        return jsonify({
            'success': True,
            'answer': f"Nelavista couldn't read \"{material.title}\" to {mode} it (the file may not be a "
                      "readable PDF, or couldn't be downloaded right now). Try opening it directly instead.",
            'grounded': False,
        })

    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    prefs = _get_user_preferences(user)
    system_prompt = (
        "You are Nelavista, an AI tutor for Nigerian university students. You have been given the actual "
        f"extracted text of a study material titled \"{material.title}\"" +
        (f" for course {material.course_code}" if material.course_code else "") + ". "
        "Base your answer ONLY on this text -- if something isn't covered in it, say so rather than "
        "inventing it. Use simple HTML (<h3>, <p>, <ul>/<li>, <strong>) for structure, no Markdown.\n\n"
        f"{_build_personalization_block(prefs)}\n\n"
        f"TASK: {_MATERIAL_AI_MODES[mode]}\n\n"
        f"MATERIAL CONTENT:\n{text}"
    )

    try:
        headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json",
                   "HTTP-Referer": "https://nelavista.com", "X-Title": "Nelavista Material AI"}
        payload = {"model": "openai/gpt-4o-mini",
                   "messages": [{"role": "system", "content": system_prompt},
                                {"role": "user", "content": _MATERIAL_AI_MODES[mode]}],
                   "temperature": 0.4, "max_tokens": 900}
        resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=45)
        if resp.status_code == 200:
            answer = resp.json()["choices"][0]["message"]["content"]
            return jsonify({'success': True, 'answer': answer, 'grounded': True})
        debug_print(f"Material AI action returned {resp.status_code}")
    except Exception as e:
        debug_print(f"Material AI action failed: {e}")
        traceback.print_exc()

    return jsonify({'success': True, 'answer': "Nelavista is having trouble responding right now — please try again.", 'grounded': False})


@ai_bp.route('/api/topics/<int:topic_id>/ai-action', methods=['POST'])
@login_required
@limiter.limit('30 per hour')
def topic_ai_action(topic_id):
    """Same idea as material_ai_action above, grounded in a Topic's own written
    explanation instead of a PDF's extracted text -- the 'AI Tutor' entry point on a
    topic page. A topic with no explanation yet is answered honestly rather than
    guessing content that was never written."""
    topic = Topic.query.get_or_404(topic_id)
    if not topic.is_active:
        return jsonify({'success': False, 'error': 'Topic not found'}), 404

    mode = (request.get_json(silent=True) or {}).get('mode', 'explain')
    if mode not in _MATERIAL_AI_MODES:
        mode = 'explain'

    if not topic.explanation:
        return jsonify({
            'success': True,
            'answer': f"Nelavista doesn't have a written explanation for \"{topic.title}\" yet to {mode} it. "
                      "Try the reference video above, or check back once an admin has added one.",
            'grounded': False,
        })

    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    prefs = _get_user_preferences(user)
    course = topic.course
    system_prompt = (
        "You are Nelavista, an AI tutor for Nigerian university students. You have been given the actual "
        f"written explanation of the topic \"{topic.title}\" from the course {course.code} — {course.title}. "
        "Base your answer ONLY on this text -- if something isn't covered in it, say so rather than "
        "inventing it. Use simple HTML (<h3>, <p>, <ul>/<li>, <strong>) for structure, no Markdown.\n\n"
        f"{_build_personalization_block(prefs)}\n\n"
        f"TASK: {_MATERIAL_AI_MODES[mode]}\n\n"
        f"TOPIC CONTENT:\n{topic.explanation}"
    )

    try:
        headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json",
                   "HTTP-Referer": "https://nelavista.com", "X-Title": "Nelavista Topic AI"}
        payload = {"model": "openai/gpt-4o-mini",
                   "messages": [{"role": "system", "content": system_prompt},
                                {"role": "user", "content": _MATERIAL_AI_MODES[mode]}],
                   "temperature": 0.4, "max_tokens": 900}
        resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=45)
        if resp.status_code == 200:
            answer = resp.json()["choices"][0]["message"]["content"]
            return jsonify({'success': True, 'answer': answer, 'grounded': True})
        debug_print(f"Topic AI action returned {resp.status_code}")
    except Exception as e:
        debug_print(f"Topic AI action failed: {e}")
        traceback.print_exc()

    return jsonify({'success': True, 'answer': "Nelavista is having trouble responding right now — please try again.", 'grounded': False})


@ai_bp.route('/teach-me-ai')
@login_required
def teach_me_ai():
    return render_template('teach-me-ai.html')


@ai_bp.route('/api/ai-teach')
@login_required
@limiter.limit('20 per hour')
def ai_teach():
    course = request.args.get("course")
    level = request.args.get("level")
    if not course or not level:
        return jsonify({"error": "Missing course or level"}), 400
    prompt = f"You're a tutor. Teach a {level} student the basics of {course} in a friendly and easy-to-understand way."
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://nelavista.com",
            "X-Title": "Nelavista AI Tutor"
        }
        payload = {
            "model": "openai/gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are an educational AI assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7, "max_tokens": 800
        }
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            summary = response.json()["choices"][0]["message"]["content"]
        else:
            summary = f"Let me teach you the basics of {course}. We'll start with fundamental concepts and build up from there. This is perfect for {level} students!"
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)})
