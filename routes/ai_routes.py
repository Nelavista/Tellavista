import os
import json
import uuid
import base64
import shutil
import time
import traceback
from datetime import datetime
from models import User
from flask import Blueprint, render_template, request, session, jsonify, send_from_directory, current_app
from utils.helpers import login_required, debug_print, get_session_memory, add_to_session_memory, cleanup_old_files, allowed_file
from services.material_service import extract_text_from_pdf, extract_text_from_pdf_turbo, extract_images_from_pdf, extract_tables_from_pdf, analyze_document_structure, extract_text_from_image, is_diagram_or_visual
from services.ai_service import generate_turbo_style_notes, safe_markdown_to_html, generate_test_questions
from models import UserQuestions
from extensions import db
import requests
from config import OPENROUTER_API_KEY

ai_bp = Blueprint('ai', __name__)


# ===== SERVER-SIDE ANALYZER CONTENT STORE =====
# Extracted PDF text/tables/images/notes are too large for Flask's default client-side
# cookie session (capped at ~4KB by browser/RFC limits — a single lecture-notes PDF's
# extracted text alone routinely exceeds that, and the browser just silently drops or
# truncates an oversized cookie). Only a small pointer lives in session['analyzer_content'];
# the actual payload is written to a JSON file under IMAGE_FOLDER/<session_id>/, reusing the
# same per-session folder extract_images_from_pdf() already writes images into.
def _content_path(session_id):
    return os.path.join(current_app.config['IMAGE_FOLDER'], session_id, 'content.json')


def _save_content(session_id, content):
    path = _content_path(session_id)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(content, f)


def _load_content(session_id):
    path = _content_path(session_id)
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        debug_print(f"⚠️ Failed to load analyzer content for {session_id}: {e}")
        return None


@ai_bp.route('/analyze')
@login_required
def analyze_page():
    user = session.get('user')
    return render_template('analyze.html', user=user)

@ai_bp.route('/analyze', methods=['POST'])
@login_required
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
        user_department = user.department if user and user.department else "not specified"
        user_level = user.level if user and user.level else "not specified"
        user_university = user.university if user and user.university else "not specified"
        user_faculty = user.faculty if user and user.faculty else "not specified"

        session_memory = get_session_memory()
        system_prompt = f"""You are Nelavista, an advanced AI tutor created by Afeez Adewale Tella for Nigerian university students (100–400 level).

## STUDENT CONTEXT
- Name: {user_name}
- Department: {user_department}
- Academic Level: {user_level}
- University: {user_university}
- Faculty: {user_faculty}

Use this information to personalise your responses. Address the student by their name occasionally, and tailor examples to their department or level when relevant.

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
        for mem in session_memory:
            messages.append({"role": mem["role"], "content": mem["content"]})
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

@ai_bp.route('/teach-me-ai')
@login_required
def teach_me_ai():
    return render_template('teach-me-ai.html')


@ai_bp.route('/api/ai-teach')
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
