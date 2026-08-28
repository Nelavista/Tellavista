import os
import json
import requests
import re
from datetime import datetime
from config import OPENROUTER_API_KEY

def debug_print(*args, **kwargs):
    from config import DEBUG_MODE
    if DEBUG_MODE:
        print(*args, **kwargs)

def safe_markdown_to_html(text):
    """
    Convert common Markdown patterns to HTML while preserving LaTeX math.
    """
    if not text:
        return text

    math_placeholders = {}
    def replace_inline_math(match):
        placeholder = f"__INLINE_MATH_{len(math_placeholders)}__"
        math_placeholders[placeholder] = match.group(0)
        return placeholder
    def replace_display_math(match):
        placeholder = f"__DISPLAY_MATH_{len(math_placeholders)}__"
        math_placeholders[placeholder] = match.group(0)
        return placeholder

    text = re.sub(r'\\\(.*?\\\)', replace_inline_math, text, flags=re.DOTALL)
    text = re.sub(r'\$[^\$]*?\$', replace_inline_math, text, flags=re.DOTALL)
    text = re.sub(r'\$\$.*?\$\$', replace_display_math, text, flags=re.DOTALL)
    text = re.sub(r'\\\[.*?\\\]', replace_display_math, text, flags=re.DOTALL)

    # Headings
    text = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.*?)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)

    # Bold & italic
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text, flags=re.DOTALL)
    text = re.sub(r'__(.*?)__', r'<strong>\1</strong>', text, flags=re.DOTALL)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text, flags=re.DOTALL)
    text = re.sub(r'_(.*?)_', r'<em>\1</em>', text, flags=re.DOTALL)

    # Unordered lists
    lines = text.split('\n')
    in_list = False
    new_lines = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith(('- ', '* ', '+ ')):
            if not in_list:
                new_lines.append('<ul>')
                in_list = True
            item = stripped[2:].strip()
            new_lines.append(f'<li>{item}</li>')
        else:
            if in_list:
                new_lines.append('</ul>')
                in_list = False
            new_lines.append(line)
    if in_list:
        new_lines.append('</ul>')
    text = '\n'.join(new_lines)

    # Numbered lists
    lines = text.split('\n')
    in_ol = False
    new_lines = []
    for line in lines:
        stripped = line.lstrip()
        match = re.match(r'^(\d+)\.\s+(.*)$', stripped)
        if match:
            if not in_ol:
                new_lines.append('<ol>')
                in_ol = True
            item = match.group(2).strip()
            new_lines.append(f'<li>{item}</li>')
        else:
            if in_ol:
                new_lines.append('</ol>')
                in_ol = False
            new_lines.append(line)
    if in_ol:
        new_lines.append('</ol>')
    text = '\n'.join(new_lines)

    # Simple tables
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        if '|' in lines[i]:
            header_line = lines[i].strip()
            if i+1 < len(lines) and re.match(r'^[\s\|:-]+$', lines[i+1]):
                headers = [h.strip() for h in header_line.split('|') if h.strip()]
                data_rows = []
                j = i+2
                while j < len(lines) and '|' in lines[j] and not re.match(r'^[\s\|:-]+$', lines[j]):
                    row = [c.strip() for c in lines[j].split('|') if c.strip()]
                    data_rows.append(row)
                    j += 1
                table_html = '<table>\n<thead>\n<tr>\n'
                for h in headers:
                    table_html += f'<th>{h}</th>\n'
                table_html += '</tr>\n</thead>\n<tbody>\n'
                for row in data_rows:
                    table_html += '<tr>\n'
                    for cell in row:
                        table_html += f'<td>{cell}</td>\n'
                    table_html += '</tr>\n'
                table_html += '</tbody>\n</table>'
                lines[i:j] = [table_html]
                i = j
                continue
        i += 1
    text = '\n'.join(lines)

    for placeholder, math in math_placeholders.items():
        text = text.replace(placeholder, math)

    text = re.sub(r'\*\*', '', text)
    text = re.sub(r'__', '', text)
    text = re.sub(r'\*', '', text)
    text = re.sub(r'\_', '', text)
    return text

def generate_turbo_style_notes(text, tables, images, filename, document_analysis):
    """Generate comprehensive lecture-style notes using AI."""
    try:
        tables_summary = f"Found {len(tables)} table(s)."
        for i, table in enumerate(tables[:3], 1):
            tables_summary += f"\nTable {i} (page {table.get('page', '?')}): {table.get('text', '')[:200]}"
        images_summary = f"Found {len(images)} image(s)."

        PDF_ANALYSIS_PROMPT = """
You are an expert academic tutor and textbook author. Transform raw extracted content into ULTIMATE LECTURE-STYLE NOTES that are clear, comprehensive, and exam-focused.

Your output must:
1. Turn all bullet points into flowing textbook explanations.
2. Create comprehensive comparison tables from any comparable data.
3. Explain EVERY concept in student-friendly language.
4. Add structure with clear headings and logical flow.
5. Include practical examples and real-world applications.
6. Prepare for exams with must-know facts and common questions.

Serve both slow learners (clear explanations) and fast learners (advanced insights).
"""
        enhanced_prompt = f"""
EXTRACTED TABLES SUMMARY:
{tables_summary}

EXTRACTED IMAGES: {images_summary}

YOUR TASK:
Transform this raw material into ULTIMATE LECTURE-STYLE NOTES following the instructions above.
"""
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://nelavista.com",
            "X-Title": "Nelavista Turbo-Style Notes Generator"
        }
        payload = {
            "model": "openai/gpt-4-turbo",
            "messages": [
                {"role": "system", "content": PDF_ANALYSIS_PROMPT},
                {"role": "user", "content": enhanced_prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 7000
        }
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=180)
        if response.status_code == 200:
            data = response.json()
            notes = data["choices"][0]["message"]["content"]
            return enhance_notes_with_extractions(notes, tables, images)
        else:
            raise Exception(f"AI API error: {response.status_code}")
    except Exception as e:
        debug_print(f"❌ AI note generation failed: {e}")
        return generate_structured_fallback(text, tables, images, filename, document_analysis)

def enhance_notes_with_extractions(notes, tables, images):
    enhanced = notes
    if tables:
        table_section = "\n\n---\n\n## 📊 EXTRACTED DATA TABLES FROM DOCUMENT\n\n"
        table_section += "*Below are the actual tables extracted from the original document:*\n\n"
        for i, table in enumerate(tables[:5], 1):
            table_section += f"### 📋 Table {i} (Page {table.get('page', '?')})\n\n"
            table_section += table.get("markdown", "Table format not available") + "\n\n"
            if i < min(5, len(tables)):
                table_section += "---\n\n"
        enhanced += table_section
    if images:
        image_section = "\n\n---\n\n## 🖼️ EXTRACTED DIAGRAMS & ILLUSTRATIONS\n\n"
        image_section += f"*The original document contains {len(images)} image(s) that supplement the text:*\n\n"
        for i, img in enumerate(images[:3], 1):
            image_section += f"### Image {i} (Page {img.get('page', '?')})\n\n"
            image_section += f"![{img.get('alt', 'Diagram')}]({img.get('url', '')})\n"
            image_section += f"*{img.get('alt', 'Document diagram')}*\n\n"
        enhanced += image_section
    enhanced += f"\n\n---\n*Generated by Nelavista Academic Document Analyzer | {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"
    return enhanced

def generate_structured_fallback(text, tables, images, filename, document_analysis):
    notes = f"# 📚 {filename} - Comprehensive Study Guide\n\n"
    notes += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
    if document_analysis.get('document_title'):
        notes += f"**Main Topic**: {document_analysis['document_title']}\n\n"
    if document_analysis.get('main_topics'):
        notes += "## 🎯 Key Concepts\n\n"
        for i, topic in enumerate(document_analysis['main_topics'][:10], 1):
            notes += f"{i}. **{topic}**\n"
        notes += "\n"
    if document_analysis.get('definitions'):
        notes += "## 🔍 Key Definitions\n\n"
        for i, definition in enumerate(document_analysis['definitions'][:8], 1):
            notes += f"**Definition {i}**: {definition}\n\n"
    if tables:
        notes += f"## 📊 Extracted Tables ({len(tables)} found)\n\n"
        for i, table in enumerate(tables[:3], 1):
            notes += f"### Table {i} (Page {table.get('page', '?')})\n\n"
            notes += table.get("markdown", "Table not available") + "\n\n"
    if images:
        notes += f"## 🖼️ Extracted Images ({len(images)} found)\n\n"
        for img in images[:2]:
            notes += f"![{img.get('alt', 'Diagram')}]({img.get('url', '')})\n"
            notes += f"*{img.get('alt', 'Document image')}*\n\n"
    notes += "## 📝 Document Content Preview\n\n"
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    for i, para in enumerate(paragraphs[:6]):
        notes += f"{para}\n\n"
        if i == 2:
            notes += "---\n\n"
    notes += "\n---\n*Note: AI-powered comprehensive analysis was unavailable. Showing structured extraction.*\n"
    return notes

def generate_test_questions(text, test_type='cbt', num_questions=10, filename='Study Material'):
    """
    Generate practice test questions from extracted document text — backs the "Test
    Yourself" feature on /analyze. test_type is 'cbt' (multiple choice) or 'written'
    (open-ended). Returns a list of question dicts matching what templates/analyze.html's
    renderTestQuestions()/submitTest() expect:
      cbt:     {"question": str, "options": [str, str, str, str], "correctAnswer": int, "explanation": str}
      written: {"question": str, "explanation": str}
    Raises on failure — the caller decides the HTTP-level fallback.
    """
    # Cap the source text so a huge document doesn't blow the prompt token budget —
    # a representative slice is enough to generate a solid question set.
    source_text = text[:12000]

    if test_type == 'cbt':
        format_instructions = (
            "Return a JSON array of exactly %d multiple-choice questions. Each item must be an "
            "object with these exact keys: \"question\" (string), \"options\" (array of exactly "
            "4 strings), \"correctAnswer\" (integer index 0-3 into options), \"explanation\" "
            "(string, briefly explains why the answer is correct)." % num_questions
        )
    else:
        format_instructions = (
            "Return a JSON array of exactly %d open-ended written/theory questions testing deep "
            "understanding. Each item must be an object with these exact keys: \"question\" "
            "(string), \"explanation\" (string — a model answer / key points a student should "
            "cover)." % num_questions
        )

    system_prompt = (
        "You are an exam-question writer for Nigerian university students. Write exam-quality "
        "questions strictly from the material provided — do not invent facts not supported by it. "
        f"{format_instructions} "
        "Output ONLY the JSON array, no surrounding prose, no Markdown code fences."
    )
    user_prompt = f"Source material ({filename}):\n\n{source_text}"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://nelavista.com",
        "X-Title": "Nelavista Test Generator"
    }
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.4,
        "max_tokens": 3000
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers, json=payload, timeout=60
    )
    if response.status_code != 200:
        raise Exception(f"AI API error: {response.status_code}")

    raw = response.json()["choices"][0]["message"]["content"].strip()
    return _parse_question_json(raw)


def generate_lesson_content_from_video(skill_name, lesson_title, video):
    """Drafts a Skills lesson's written explanation anchored to a specific reference video,
    so the text and the video actually teach the same material in the same order — not two
    unrelated things sharing a page. Returns a draft for an admin to review/edit in the
    lesson editor; nothing here writes to the database. Raises on failure, same convention
    as generate_test_questions — the caller (an admin API route) decides the HTTP response.
    """
    system_prompt = (
        "You are an instructional content writer for Nelavista, a student skills platform. "
        "Write a lesson's written explanation to directly complement a specific reference "
        "video students will watch alongside it — cover the same core ideas, in the same "
        "order, so a student reading the text recognizes what they just watched. Do not "
        "describe or refer to the video itself (no 'in this video...', 'as shown above') — "
        "just teach the material the way the video teaches it, in your own words.\n\n"
        "Output clean HTML only: <h2>/<h3> for structure, <p> for explanation, <ul>/<ol> for "
        "lists, <code> for inline code, <pre><code> for code blocks, <strong> for emphasis. "
        "No Markdown, no <html>/<body> wrapper, no surrounding code fences. Aim for 150-350 "
        "words — a focused lesson, not an essay."
    )
    user_prompt = (
        f"Skill: {skill_name}\n"
        f"Lesson title: {lesson_title}\n"
        f"Reference video: \"{video['title']}\" by {video['channel']}\n\n"
        "Write the lesson content now."
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://nelavista.com",
        "X-Title": "Nelavista Skills Lesson Drafter"
    }
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 1200
    }
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers, json=payload, timeout=60
    )
    if response.status_code != 200:
        raise Exception(f"AI API error: {response.status_code}")

    content = response.json()["choices"][0]["message"]["content"].strip()
    # Strip accidental code fences despite instructions not to include them (same defensive
    # habit as _parse_question_json below).
    content = re.sub(r'^```(?:html)?\s*', '', content)
    content = re.sub(r'\s*```$', '', content)
    return content


def generate_challenge_feedback(challenge_title, challenge_instructions, submission_content):
    """Evaluates a student's practice submission against the challenge's own instructions
    and returns structured feedback — not a bare 'Correct ✓'. Works across challenge types
    (coding, design, business, content, general) since the prompt reasons from whatever
    the instructions actually asked for, rather than assuming code. Raises on failure; the
    caller (challenge submission route) treats missing feedback as non-fatal — the
    submission itself is saved either way.
    """
    system_prompt = (
        "You are a practical, encouraging skills coach reviewing a student's attempt at a "
        "practice challenge. Evaluate their submission strictly against what the challenge "
        "instructions actually asked for. Be specific and honest — do not just say "
        "'Correct' or 'Great job' without substance, and do not invent praise or issues "
        "that don't apply.\n\n"
        "Return ONLY a single JSON object with this exact shape, no surrounding prose:\n"
        "{\n"
        '  "score": integer 0-100 (how completely the submission meets the challenge),\n'
        '  "strengths": [string, ...] (1-3 specific things done well — omit filler if there '
        "genuinely isn't much),\n"
        '  "improvements": [string, ...] (1-3 specific, actionable issues or gaps),\n'
        '  "explanation": string (2-4 sentences: why the score is what it is, in plain terms),\n'
        '  "next_step": string (one concrete suggestion for what to do next — revise this, '
        "move on, try a harder variant, etc.)\n"
        "}"
    )
    user_prompt = (
        f"Challenge: {challenge_title}\n\n"
        f"Instructions given to the student:\n{challenge_instructions or '(no detailed instructions were provided)'}\n\n"
        f"Student's submission:\n{submission_content}"
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://nelavista.com",
        "X-Title": "Nelavista Skills Challenge Feedback"
    }
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.4,
        "max_tokens": 800
    }
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers, json=payload, timeout=45
    )
    if response.status_code != 200:
        raise Exception(f"AI API error: {response.status_code}")

    raw = response.json()["choices"][0]["message"]["content"].strip()
    return _parse_json_object(raw)


PROJECT_REVIEW_DIMENSIONS = ('functionality', 'craft_quality', 'problem_solving', 'documentation', 'originality')


def evaluate_project_submission(project_title, project_description, submission_details, skills_demonstrated,
                                 reflections=None):
    """Reviews an ordinary (non-final-project) StudentProject submission — the 'Request
    Review' action in the project workspace. Same structured-feedback spirit as
    generate_challenge_feedback (real strengths/improvements, not a bare score), but for
    a whole project rather than one exercise. No rubric here (ordinary projects don't have
    one — only a daily-class's formal final project does; see evaluate_final_project),
    so this reasons from the project's own stated brief and what was actually submitted.

    The AI scores PROJECT_REVIEW_DIMENSIONS individually (0-100 each); the overall score
    returned as 'score' is then computed HERE as their rounded mean — never taken from an
    AI-reported total — same "AI proposes, Python computes ground truth" discipline
    evaluate_final_project already uses for rubric criteria. 'score' stays the top-level key
    services/skills_service.py's _project_counts_as_verified reads, so this change is
    backward-compatible with every existing caller.

    `reflections` (optional dict: problem_solved/challenges/improvements, all optional) is
    the student's own account of the work — given to the AI as grading context, not scored
    as its own dimension, so a vague reflection just makes the whole submission read as
    vague rather than being penalized in isolation.

    Raises on failure; the caller treats a failed review as non-fatal.
    """
    reflections = reflections or {}
    reflection_block = (
        f"What problem this solves (in the student's own words): {reflections.get('problem_solved') or '(not provided)'}\n"
        f"Challenges they faced: {reflections.get('challenges') or '(not provided)'}\n"
        f"What they'd improve: {reflections.get('improvements') or '(not provided)'}"
    )
    system_prompt = (
        "You are reviewing a student's project submission for a skills platform. Judge it "
        "against what the project brief actually asked for and what skills it claims to "
        "demonstrate. Be specific and honest — do not inflate scores or invent issues that "
        "aren't there. This becomes part of the student's public proof of work, so it needs "
        "to be defensible.\n\n"
        f"Score exactly these dimensions, 0-100 each: {', '.join(PROJECT_REVIEW_DIMENSIONS)} "
        "(functionality: does it do what it claims; craft_quality: how well-built/organized "
        "it is; problem_solving: depth of the approach; documentation: how clearly the "
        "student explained it; originality). Do not add, rename, or drop dimensions.\n\n"
        "Return ONLY a single JSON object with this exact shape, no surrounding prose:\n"
        "{\n"
        '  "dimension_scores": {"functionality": int, "craft_quality": int, "problem_solving": int, '
        '"documentation": int, "originality": int},\n'
        '  "strengths": [string, ...] (1-3 specific things done well),\n'
        '  "improvements": [string, ...] (1-3 specific, actionable gaps),\n'
        '  "explanation": string (2-4 sentences on why the scores are what they are),\n'
        '  "next_project": {"title": string, "description": string} (one concrete project, '
        'slightly harder, that builds on this one)\n'
        "}"
    )
    user_prompt = (
        f"Project: {project_title}\n"
        f"Brief: {project_description or '(no brief — a freeform project)'}\n"
        f"Skills claimed: {', '.join(skills_demonstrated) if skills_demonstrated else '(none listed)'}\n\n"
        f"Submission details:\n{submission_details}\n\n{reflection_block}"
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://nelavista.com",
        "X-Title": "Nelavista Project Review"
    }
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 900
    }
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers, json=payload, timeout=45
    )
    if response.status_code != 200:
        raise Exception(f"AI API error: {response.status_code}")

    raw = response.json()["choices"][0]["message"]["content"].strip()
    result = _parse_json_object(raw)

    # Ground truth: clamp each dimension into 0-100 (never trust the AI's own bounds), and
    # compute the overall score as their rounded mean rather than an AI-reported total.
    raw_dims = result.get('dimension_scores') or {}
    dims = {}
    for key in PROJECT_REVIEW_DIMENSIONS:
        try:
            dims[key] = max(0, min(100, int(raw_dims.get(key, 0))))
        except (TypeError, ValueError):
            dims[key] = 0
    overall = round(sum(dims.values()) / len(dims))

    next_project = result.get('next_project') or {}
    next_project_title = next_project.get('title') or ''

    return {
        'score': overall,
        'strengths': result.get('strengths') or [],
        'improvements': result.get('improvements') or [],
        'explanation': result.get('explanation') or '',
        'next_step': next_project_title,  # kept for backward-compat with older callers/UI
        'dimension_scores': dims,
        'next_project': {'title': next_project_title, 'description': next_project.get('description') or ''},
    }


def generate_project_brief(idea, experience_level):
    """Turns a student's free-text project idea into a full, structured project brief —
    the entry point for an AI-generated StudentProject (source='ai_generated'). Classifies
    the idea into exactly one of Nelavista's three workspace types — unlike a broader
    'data'/'other' category set, these three are the only in-browser workspaces this
    platform builds (see the project_workspace_* templates), so the AI is constrained to
    them rather than free-choosing a category with no matching workspace.
    Raises on failure; the caller must not create a project if this raises.
    """
    system_prompt = (
        "You are helping a student turn a rough idea into a concrete, buildable project "
        "brief for a student skills platform. Classify which kind of hands-on workspace "
        "this needs: 'developer' (a multi-file code project), 'writer' (a written "
        "document/report/plan), or 'designer' (a visual/UI moodboard-and-asset project) — "
        "choose the closest fit even if the idea is ambiguous; these are the only three "
        "options.\n\n"
        "Return ONLY a single JSON object with this exact shape, no surrounding prose:\n"
        "{\n"
        '  "title": string (concrete, specific — not a restatement of the idea),\n'
        '  "category": "developer" | "writer" | "designer",\n'
        '  "objectives": string (one clear paragraph),\n'
        '  "features": [string, ...] (4-8 concrete features/sections to build),\n'
        '  "difficulty": "beginner" | "intermediate" | "advanced",\n'
        '  "estimated_time": string (realistic, e.g. "6-8 hours"),\n'
        '  "deliverables": [string, ...] (3-6 concrete things handed in),\n'
        '  "milestones": [string, ...] (4-6 ordered build steps, short),\n'
        '  "tech_stack": [string, ...] (tools/frameworks/methods appropriate to the category),\n'
        '  "success_criteria": [string, ...] (3-5 concrete "this is genuinely done when..." checks)\n'
        "}"
    )
    user_prompt = f"Student's experience level: {experience_level}\nTheir idea: \"{idea}\""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://nelavista.com",
        "X-Title": "Nelavista AI Project Brief"
    }
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.4,
        "max_tokens": 1200
    }
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers, json=payload, timeout=45
    )
    if response.status_code != 200:
        raise Exception(f"AI API error: {response.status_code}")

    raw = response.json()["choices"][0]["message"]["content"].strip()
    result = _parse_json_object(raw)
    if result.get('category') not in ('developer', 'writer', 'designer'):
        result['category'] = 'developer'  # defensive only -- the prompt already constrains this
    return result


def project_mentor_reply(project_brief, history, user_message):
    """One turn of the AI mentor chat scoped to a single StudentProject (see models.py's
    ProjectMessage — deliberately separate from the site-wide, stateless 'Ask Nelavista'
    widget). Guides the student — explains concepts, points out mistakes, suggests
    approaches — without writing the project for them. `history` is a chronological list of
    {"role", "body"} dicts; only the most recent turns are sent, to keep the request small.
    Returns plain text, not JSON — this is a conversational reply. Raises on failure; the
    caller surfaces that as a chat-unavailable error rather than a broken reply.
    """
    brief_lines = [f"Project: {project_brief.get('title')} ({project_brief.get('workspace_type') or 'no workspace'})"]
    if project_brief.get('objectives'):
        brief_lines.append(f"Objectives: {project_brief['objectives']}")
    elif project_brief.get('description'):
        brief_lines.append(f"Description: {project_brief['description']}")
    if project_brief.get('features'):
        brief_lines.append(f"Features: {', '.join(project_brief['features'])}")
    if project_brief.get('tech_stack'):
        brief_lines.append(f"Tech/tools: {', '.join(project_brief['tech_stack'])}")
    if project_brief.get('success_criteria'):
        brief_lines.append(f"Success criteria: {', '.join(project_brief['success_criteria'])}")

    system_prompt = (
        "You are a mentor helping a student build their own project on Nelavista. Act like "
        "an experienced professional pairing with them: answer questions, point out "
        "mistakes, suggest better approaches, explain concepts, and give implementation "
        "ideas. Never just write the finished solution or complete the project for them — "
        "guide them to figure it out. Keep replies focused and practical, usually under 150 "
        "words unless the question genuinely needs more.\n\n" + "\n".join(brief_lines)
    )
    messages = [{"role": "system", "content": system_prompt}]
    messages += [{"role": m['role'], "content": m['body']} for m in history[-12:]]
    messages.append({"role": "user", "content": user_message})

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://nelavista.com",
        "X-Title": "Nelavista Project Mentor"
    }
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": messages,
        "temperature": 0.4,
        "max_tokens": 500
    }
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers, json=payload, timeout=45
    )
    if response.status_code != 200:
        raise Exception(f"AI API error: {response.status_code}")

    return response.json()["choices"][0]["message"]["content"].strip()


def generate_curriculum(skill_name, skill_description, level='beginner'):
    """Proposes a starter curriculum for a skill: two modules of two lessons each (real,
    complete HTML content — not just titles), one practice challenge, and one project
    brief. Everything comes back as a structured draft for an admin to review, edit, and
    individually publish through the normal Skills editor — nothing here is ever
    auto-published (see routes/admin_skills_routes.py's generate_curriculum route).
    Raises on failure; the caller decides the HTTP-level response.
    """
    system_prompt = (
        "You are a curriculum designer for Nelavista, a student skills platform. Given a "
        "skill, propose a focused starter curriculum: enough to genuinely teach the "
        "fundamentals, not an exhaustive course. An admin will review and expand on this "
        "before publishing, so prioritize getting the structure and first real lessons "
        "right over covering everything.\n\n"
        "Return ONLY a single JSON object with this exact shape, no surrounding prose:\n"
        "{\n"
        '  "course_title": string,\n'
        '  "course_description": string (1-2 sentences),\n'
        '  "modules": [\n'
        "    {\n"
        '      "title": string,\n'
        '      "lessons": [\n'
        '        {"title": string, "content": string (HTML: <h2>/<h3>/<p>/<ul>/<ol>/<code>/<pre><code>/<strong>, '
        "150-300 words, a complete real lesson, no Markdown, no code fences), "
        '"duration_minutes": integer}\n'
        "      ]\n"
        "    }\n"
        "  ],\n"
        '  "challenge": {"title": string, "description": string (1 sentence), '
        '"instructions": string (a full practical exercise the student can actually attempt), '
        '"difficulty": "beginner"|"intermediate"|"advanced", "estimated_minutes": integer},\n'
        '  "project": {"title": string, "description": string (a real project brief students would '
        'actually build, 2-4 sentences), "skills_demonstrated": [string, ...], '
        '"difficulty": "beginner"|"intermediate"|"advanced", "estimated_hours": integer}\n'
        "}\n\n"
        "Exactly 2 modules, exactly 2 lessons per module (4 lessons total)."
    )
    user_prompt = (
        f"Skill: {skill_name}\n"
        f"Level: {level}\n"
        f"Description: {skill_description or '(none given — infer a sensible scope from the skill name)'}"
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://nelavista.com",
        "X-Title": "Nelavista Skills Curriculum Generator"
    }
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 4000
    }
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers, json=payload, timeout=90
    )
    if response.status_code != 200:
        raise Exception(f"AI API error: {response.status_code}")

    raw = response.json()["choices"][0]["message"]["content"].strip()
    return _parse_json_object(raw)


def generate_course_topics(course_code, course_title, department_name, level, existing_description=None):
    """Drafts a course's student-facing description plus an ordered topic list -- the
    core Academia content pipeline (see routes/admin_academia_routes.py's
    generate_course_content). Mirrors generate_curriculum's structured-draft convention:
    everything comes back for an admin to review/edit before any Topic row is created,
    nothing is auto-published. Explicitly instructed to describe the SUBJECT MATTER a
    course with this code/title normally covers at Nigerian universities, never to
    invent a specific lecturer's own syllabus -- this is a reasonable starting draft,
    not a claim of official curriculum. Raises on failure; caller decides the HTTP
    response.
    """
    system_prompt = (
        "You are an experienced university lecturer writing a course description for "
        "Nelavista, an academic study platform for Nigerian university students. Given a "
        "course code and title, draft: (1) a course description, and (2) an ordered list "
        "of the core topics a course with this code and title normally covers, in a "
        "sensible teaching order from fundamentals onward. Base this on the well-established "
        "general subject matter such a course code/title conventionally covers -- do not "
        "invent a specific lecturer's own syllabus, exam pattern, or claim this is any "
        "particular university's official curriculum. This is a draft starting point for "
        "an admin to review and edit, not a final authoritative document.\n\n"
        "The description must read like a lecturer briefing a student, in 3-5 sentences "
        "covering: what the course is about, why it matters, the major concepts covered, "
        "and what a student should be able to do after studying it. Write clearly and "
        "directly -- no marketing language of any kind. Never use phrases like 'embark on "
        "a journey', 'unlock your potential', 'master the world of', 'dive into', or "
        "similar hype. State facts about the subject, plainly.\n\n"
        "Return ONLY a single JSON object with this exact shape, no surrounding prose:\n"
        "{\n"
        '  "description": string (3-5 sentences, lecturer tone as described above),\n'
        '  "topics": [string, ...] (8-14 topic titles, ordered, specific -- e.g. "Linked Lists", '
        'not vague filler like "More Concepts")\n'
        "}"
    )
    user_prompt = (
        f"Course code: {course_code}\nCourse title: {course_title}\n"
        f"Department: {department_name}\nLevel: {level}"
        + (f"\nExisting description (revise/improve, don't ignore): {existing_description}" if existing_description else "")
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://nelavista.com",
        "X-Title": "Nelavista Course Content Drafter"
    }
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.4,
        "max_tokens": 1500
    }
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers, json=payload, timeout=60
    )
    if response.status_code != 200:
        raise Exception(f"AI API error: {response.status_code}")

    raw = response.json()["choices"][0]["message"]["content"].strip()
    return _parse_json_object(raw)


def generate_topic_explanation(course_code, course_title, topic_title, video=None):
    """Drafts one Topic's written explanation -- same anchored-to-a-reference-video
    convention as generate_lesson_content_from_video when a video is already attached
    (so the text and the video teach the same material), otherwise a standalone
    explanation grounded only in the course/topic identity. Returns a draft for an admin
    to review/edit before it's saved as Topic.explanation; nothing here writes to the
    database. Raises on failure; caller decides the HTTP response."""
    system_prompt = (
        "You are an experienced university lecturer writing study material for Nelavista, "
        "an academic study platform for Nigerian university students. Write a clear, "
        "focused explanation of ONE topic within a specific university course, at a level "
        "appropriate for a student encountering it for the first time. Write like a "
        "lecturer explaining the topic to a student: clear, direct, academic, human. Do "
        "NOT use marketing language ('embark on a journey', 'unlock', 'master', 'dive "
        "into', or similar hype) -- state what the topic is and how it works, plainly. "
        + (
            "A reference video is provided below -- cover the same core ideas, in the same "
            "order, so a student reading the text recognizes what they just watched. Do not "
            "describe or refer to the video itself (no 'in this video...', 'as shown above')."
            if video else
            "No reference video is available yet -- write a self-contained explanation."
        )
        + "\n\nStructure the output as clean HTML in exactly this shape: "
        "an <h3>What you'll learn</h3> section with one or two <p> paragraphs explaining "
        "the topic itself, followed by an <h3>Key concepts</h3> section with a <ul> of "
        "3-6 <li> bullets, each a specific concept/term within this topic (not vague "
        "restatements of the topic name). <strong> for emphasis, <code> for inline "
        "technical terms. No Markdown, no <html>/<body> wrapper, no surrounding code "
        "fences. Aim for 150-350 words total -- a focused explanation, not an essay."
    )
    user_prompt = f"Course: {course_code} — {course_title}\nTopic: {topic_title}"
    if video:
        user_prompt += f"\nReference video: \"{video['title']}\" by {video.get('channel', '')}"
    user_prompt += "\n\nWrite the topic explanation now."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://nelavista.com",
        "X-Title": "Nelavista Topic Content Drafter"
    }
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 1000
    }
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers, json=payload, timeout=60
    )
    if response.status_code != 200:
        raise Exception(f"AI API error: {response.status_code}")

    content = response.json()["choices"][0]["message"]["content"].strip()
    content = re.sub(r'^```(?:html)?\s*', '', content)
    content = re.sub(r'\s*```$', '', content)
    return content


def generate_daily_class_outline(skill_name, class_title, total_days, level='beginner'):
    """Proposes just the week/day skeleton for a whole daily class — day titles, short
    topics, and learning objectives for all `total_days` days, grouped into weeks.
    Deliberately lightweight (no lesson content, video, assignment, or test yet) so a
    30-day request stays within one call's token budget; each day's full content is
    generated separately, on demand, once an admin reviews this outline (see
    generate_daily_class_day_content below) — nothing here is ever auto-published.
    Returns {"weeks": [{"week_number","week_title","days":[{"day_number","title","topic",
    "learning_objective"}]}]}. Raises on failure; the caller decides the HTTP response.
    """
    system_prompt = (
        "You are a curriculum designer for Nelavista, a student skills platform, planning "
        f"a structured {total_days}-day class. Propose a day-by-day skeleton: what each "
        "day covers, in a sensible teaching order building from fundamentals to more "
        "advanced material. Group days into weeks (roughly 5-7 days each) with a short "
        "theme per week. An admin will review this outline, then generate each day's full "
        "lesson individually — so titles and objectives must be specific and topically "
        "precise (e.g. 'CSS Flexbox: main-axis and cross-axis alignment', not vague "
        "filler like 'More CSS').\n\n"
        "Return ONLY a single JSON object with this exact shape, no surrounding prose:\n"
        "{\n"
        '  "weeks": [\n'
        "    {\n"
        '      "week_number": integer, "week_title": string,\n'
        '      "days": [\n'
        '        {"day_number": integer, "title": string, "topic": string (1 sentence, what this day teaches), '
        '"learning_objective": string (1 sentence, starts with a verb, e.g. "Explain how...", "Build a...")}\n'
        "      ]\n"
        "    }\n"
        "  ]\n"
        "}\n\n"
        f"Cover exactly {total_days} days total, day_number running 1 through {total_days} with no gaps or repeats."
    )
    user_prompt = f"Skill: {skill_name}\nClass title: {class_title}\nLevel: {level}\nTotal days: {total_days}"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://nelavista.com",
        "X-Title": "Nelavista Daily Class Outline Generator"
    }
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 4000
    }
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers, json=payload, timeout=90
    )
    if response.status_code != 200:
        raise Exception(f"AI API error: {response.status_code}")

    raw = response.json()["choices"][0]["message"]["content"].strip()
    return _parse_json_object(raw)


def generate_daily_class_day_content(skill_name, day_title, learning_objective, video):
    """Generates one day's full structured lesson content, anchored to a specific
    reference video (same video/text alignment principle as generate_lesson_content_from_video).
    Unlike a regular lesson, a daily-class day must explicitly walk through: a simple
    explanation, a real-world analogy, a step-by-step breakdown, common mistakes, and a
    practical application — the fixed teaching loop every day in the class follows.
    Returns clean HTML content. Raises on failure.
    """
    system_prompt = (
        "You are an instructional content writer for Nelavista, a student skills platform, "
        "writing ONE day of a structured daily class. Write content that directly "
        "complements a specific reference video the student watches alongside it — cover "
        "the same core ideas, in the same order. Do not describe or refer to the video "
        "itself (no 'in this video...').\n\n"
        "Structure the content with these sections, in this order, using <h3> headings "
        "exactly as named:\n"
        "<h3>Simple Explanation</h3> — the core idea in plain, beginner-friendly language.\n"
        "<h3>Real-World Analogy</h3> — one concrete analogy that makes the idea click.\n"
        "<h3>Step-by-Step Breakdown</h3> — an ordered list walking through how it actually works or is done.\n"
        "<h3>Common Mistakes</h3> — 2-4 specific mistakes beginners make with this topic.\n"
        "<h3>Practical Application</h3> — a short worked example showing the idea used for real.\n\n"
        "Output clean HTML only: <h3> for the section headings above, <p> for prose, "
        "<ul>/<ol> for lists, <code> for inline code, <pre><code> for code blocks, "
        "<strong> for emphasis. No Markdown, no <html>/<body> wrapper, no code fences. "
        "Aim for 350-600 words total across all sections."
    )
    user_prompt = (
        f"Skill: {skill_name}\n"
        f"Day topic: {day_title}\n"
        f"Learning objective: {learning_objective}\n"
        f"Reference video: \"{video['title']}\" by {video['channel']}\n\n"
        "Write the day's content now."
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://nelavista.com",
        "X-Title": "Nelavista Daily Class Content Generator"
    }
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 1800
    }
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers, json=payload, timeout=60
    )
    if response.status_code != 200:
        raise Exception(f"AI API error: {response.status_code}")

    content = response.json()["choices"][0]["message"]["content"].strip()
    content = re.sub(r'^```(?:html)?\s*', '', content)
    content = re.sub(r'\s*```$', '', content)
    return content


def generate_day_assignment(skill_name, day_title, learning_objective, lesson_content):
    """Proposes a graded assignment for one class day, scoped to what was actually taught
    (the day's lesson content), not a generic prompt. Returns {"title","instructions"}.
    Raises on failure."""
    system_prompt = (
        "You are a curriculum designer creating a graded assignment for one day of a "
        "structured skills class. The assignment must require applying what was just "
        "taught in the lesson content given — not something unrelated or too advanced "
        "for a single day's lesson.\n\n"
        "Return ONLY a single JSON object with this exact shape, no surrounding prose:\n"
        '{"title": string, "instructions": string (a complete, specific brief the student '
        'can act on directly — what to produce and what it should demonstrate)}'
    )
    # Strip HTML tags from the lesson content for a cleaner prompt — the AI needs the
    # substance, not the markup.
    plain_content = re.sub(r'<[^>]+>', ' ', lesson_content or '')[:2000]
    user_prompt = (
        f"Skill: {skill_name}\nDay topic: {day_title}\nLearning objective: {learning_objective}\n\n"
        f"Lesson content taught today:\n{plain_content}"
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://nelavista.com",
        "X-Title": "Nelavista Daily Class Assignment Generator"
    }
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 700
    }
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers, json=payload, timeout=45
    )
    if response.status_code != 200:
        raise Exception(f"AI API error: {response.status_code}")

    raw = response.json()["choices"][0]["message"]["content"].strip()
    return _parse_json_object(raw)


def generate_day_test(skill_name, day_title, learning_objective, lesson_content, num_questions=6):
    """Generates 5-10 MCQ questions for one day's test — reuses the existing Quiz
    infrastructure (same question shape as Quiz.questions) rather than a new test engine,
    since MCQ already satisfies 'various formats' for a first version. Raises on failure."""
    num_questions = max(5, min(10, int(num_questions or 6)))
    plain_content = re.sub(r'<[^>]+>', ' ', lesson_content or '')[:2500]
    system_prompt = (
        "You are writing a short test for one day of a structured skills class, checking "
        "understanding of exactly what was taught — do not test material outside the "
        f"lesson content given below. Return a JSON array of exactly {num_questions} "
        "multiple-choice questions. Each item must be an object with these exact keys: "
        '"question" (string), "options" (array of exactly 4 strings), "correct_index" '
        "(integer index 0-3), \"explanation\" (string, briefly explains why the answer is "
        "correct). Output ONLY the JSON array, no surrounding prose, no code fences."
    )
    user_prompt = (
        f"Skill: {skill_name}\nDay topic: {day_title}\nLearning objective: {learning_objective}\n\n"
        f"Lesson content:\n{plain_content}"
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://nelavista.com",
        "X-Title": "Nelavista Daily Class Test Generator"
    }
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.4,
        "max_tokens": 2200
    }
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers, json=payload, timeout=60
    )
    if response.status_code != 200:
        raise Exception(f"AI API error: {response.status_code}")

    raw = response.json()["choices"][0]["message"]["content"].strip()
    return _parse_question_json(raw)


def generate_assignment_feedback(assignment_title, assignment_instructions, submission_content):
    """Evaluates a graded assignment submission — same structured-feedback shape and
    intent as generate_challenge_feedback, but for graded work whose score feeds directly
    into Skill GPA, so the score must be defensible against the instructions actually
    given, not a vibe. Raises on failure; the caller treats a failed AI call as non-fatal
    (submission stands either way, review_status stays 'pending' until it succeeds)."""
    system_prompt = (
        "You are grading a student's assignment submission for a skills class. Evaluate "
        "strictly against what the assignment instructions actually asked for. Be "
        "specific and fair — this score contributes to the student's grade, so do not "
        "inflate or invent issues that aren't there.\n\n"
        "Return ONLY a single JSON object with this exact shape, no surrounding prose:\n"
        "{\n"
        '  "score": integer 0-100 (how completely the submission meets the assignment),\n'
        '  "strengths": [string, ...] (1-3 specific things done well),\n'
        '  "improvements": [string, ...] (1-3 specific, actionable issues or gaps),\n'
        '  "explanation": string (2-4 sentences: why the score is what it is),\n'
        '  "next_step": string (one concrete suggestion for what to do next)\n'
        "}"
    )
    user_prompt = (
        f"Assignment: {assignment_title}\n\n"
        f"Instructions given to the student:\n{assignment_instructions or '(no detailed instructions were provided)'}\n\n"
        f"Student's submission:\n{submission_content}"
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://nelavista.com",
        "X-Title": "Nelavista Assignment Grading"
    }
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 800
    }
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers, json=payload, timeout=45
    )
    if response.status_code != 200:
        raise Exception(f"AI API error: {response.status_code}")

    raw = response.json()["choices"][0]["message"]["content"].strip()
    return _parse_json_object(raw)


def evaluate_final_project(rubric, project_title, project_description, submission_details):
    """Evaluates a final-project submission STRICTLY against the admin-defined rubric —
    the AI never invents its own scale or criteria. `rubric` is
    [{"name": str, "max_points": int}, ...] as configured on the ProjectTemplate (see
    models.py ProjectTemplate.rubric). The AI scores each criterion individually, 0 to
    that criterion's max_points; the overall score is then computed here in Python as the
    literal sum of those per-criterion scores — never taken from an AI-reported total —
    so the number a student sees can always be traced back to the rubric line-by-line.
    Raises on failure.
    """
    rubric_lines = "\n".join(f"- {c['name']} (max {c['max_points']} points)" for c in rubric)
    system_prompt = (
        "You are evaluating a student's final project submission for a skills class, "
        "against a fixed grading rubric. You MUST score ONLY the criteria listed below — "
        "do not add, remove, rename, or reweight criteria, and do not exceed any "
        "criterion's max_points. Be specific: every score needs a one-sentence comment "
        "justifying it against what was actually submitted.\n\n"
        f"RUBRIC (fixed, do not deviate from this):\n{rubric_lines}\n\n"
        "Return ONLY a single JSON object with this exact shape, no surrounding prose:\n"
        "{\n"
        '  "criteria": [{"name": string (must exactly match a rubric name above), '
        '"score": integer (0 to that criterion\'s max_points), "comment": string}, ...],\n'
        '  "strengths": [string, ...] (1-3 things done well overall),\n'
        '  "improvements": [string, ...] (1-3 specific, actionable gaps)\n'
        "}\n"
        "Include exactly one entry in \"criteria\" for every rubric line above, in the same order."
    )
    user_prompt = (
        f"Project: {project_title}\n"
        f"Project brief: {project_description or '(no brief provided)'}\n\n"
        f"Student's submission details:\n{submission_details}"
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://nelavista.com",
        "X-Title": "Nelavista Final Project Evaluation"
    }
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 1500
    }
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers, json=payload, timeout=60
    )
    if response.status_code != 200:
        raise Exception(f"AI API error: {response.status_code}")

    raw = response.json()["choices"][0]["message"]["content"].strip()
    result = _parse_json_object(raw)

    # Ground truth: rebuild criteria strictly from the admin's rubric (name/max_points),
    # only pulling the AI's score/comment per name and clamping into range — an AI
    # hallucinating an extra criterion, a renamed one, or an out-of-range score can never
    # change what the student is actually scored against or the total they receive.
    ai_by_name = {c.get('name'): c for c in (result.get('criteria') or []) if isinstance(c, dict)}
    final_criteria = []
    overall_score = 0
    for c in rubric:
        name, max_points = c['name'], int(c['max_points'])
        ai_entry = ai_by_name.get(name, {})
        try:
            score = int(ai_entry.get('score', 0))
        except (TypeError, ValueError):
            score = 0
        score = max(0, min(max_points, score))
        overall_score += score
        final_criteria.append({
            'name': name, 'max_points': max_points, 'score': score,
            'comment': ai_entry.get('comment') or '',
        })

    return {
        'criteria': final_criteria,
        'overall_score': overall_score,
        'strengths': result.get('strengths') or [],
        'improvements': result.get('improvements') or [],
    }


def _parse_json_object(raw):
    """Same defensive unwrapping as _parse_question_json, for a JSON object instead of
    an array."""
    text = raw.strip()
    if text.startswith('```'):
        text = re.sub(r'^```(?:json)?\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
    start, end = text.find('{'), text.rfind('}')
    if start != -1 and end != -1 and end > start:
        text = text[start:end + 1]
    obj = json.loads(text)
    if not isinstance(obj, dict):
        raise ValueError("AI did not return a JSON object")
    return obj


def _parse_question_json(raw):
    """LLMs routinely wrap JSON in ```json fences or add stray prose despite instructions
    not to — strip those defensively rather than fail the whole request over formatting."""
    text = raw.strip()
    if text.startswith('```'):
        text = re.sub(r'^```(?:json)?\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
    # If there's leading/trailing prose around the array, extract just the [...] span.
    start, end = text.find('['), text.rfind(']')
    if start != -1 and end != -1 and end > start:
        text = text[start:end + 1]
    questions = json.loads(text)
    if not isinstance(questions, list) or not questions:
        raise ValueError("AI did not return a non-empty question list")
    return questions
