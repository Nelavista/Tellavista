"""Nelavista AI Tutor -- the Academia-native conversational tutor (routes/tutor_routes.py).

Deliberately separate from services/ai_service.py's older single-shot helpers (ask(),
ask_with_files(), material_ai_action, topic_ai_action) -- those stay untouched for
backward compatibility. This module is the new streaming, threaded-conversation surface:
it builds the tutor's system prompt from live academic context, streams OpenRouter's
response token-by-token over SSE, and derives conversation titles/quick-prompts from
real course/topic data instead of anything hardcoded.
"""
import json
import re
import requests
from config import OPENROUTER_API_KEY
from models import Topic

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
TUTOR_MODEL = "openai/gpt-4o-mini"

# Mirrors _MATERIAL_AI_MODES' honesty rule in routes/ai_routes.py: never claim to have
# read something the platform hasn't actually extracted text from.
MAX_MATERIAL_CHARS = 6000

# Settings > AI Tutor -- same instruction set routes/ai_routes.py's /ask uses for the
# legacy single-shot tutor, kept in sync per concept rather than duplicated ad hoc.
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


def _headers():
    return {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://nelavista.com",
        "X-Title": "Nelavista AI Tutor",
    }


def build_tutor_system_prompt(user, course=None, topic=None, material=None, material_text=None, prefs=None):
    """Builds the system prompt for one tutor turn. Recomputed fresh on every request
    (never cached/stored) so it always reflects the student's current academic profile,
    not whatever it was when the conversation started.

    course/topic/material are the live-resolved models.Course/Topic/Material rows for
    this conversation (or None) -- see routes/tutor_routes.py. material_text is the
    already-extracted text of `material`, or None if extraction failed/wasn't attempted;
    callers must pass None rather than fabricate text so the prompt below can be honest
    about what it has and hasn't actually read. prefs is the student's
    models.UserPreferences row (or None, treated as all defaults) -- see Settings > AI
    Tutor; every field it has is read somewhere below, nothing is accepted and ignored.
    """
    name = user.name or (user.username if user else "there")
    use_academic_context = prefs.ai_use_academic_context if prefs else True

    if use_academic_context:
        context_lines = [
            f"- Name: {name}",
            f"- University: {user.university if user and user.university else 'not specified'}",
            f"- Faculty: {user.faculty if user and user.faculty else 'not specified'}",
            f"- Department: {user.department if user and user.department else 'not specified'}",
            f"- Academic level: {user.level if user and user.level else 'not specified'}",
        ]
    else:
        # Settings > AI Tutor > Personalization > "Use my academic context" is OFF --
        # don't share or assume university/faculty/department/level.
        context_lines = [f"- Name: {name}", "- Academic-context personalization is turned off for this student -- do not guess or assume their department, level, or university."]

    focus_block = ""
    if topic and course:
        focus_block = (
            f"\n## CURRENT FOCUS\nThe student opened the tutor from the topic "
            f"\"{topic.title}\" inside {course.code} — {course.title}. Assume every "
            f"question is about this topic unless they clearly ask about something else. "
            f"If the platform has a written explanation for this topic, it is included "
            f"below as ground truth -- prefer it over your own general knowledge when "
            f"they conflict, and don't contradict it.\n"
        )
        if topic.explanation:
            plain = re.sub(r'<[^>]+>', ' ', topic.explanation)
            focus_block += f"\nTOPIC EXPLANATION (platform content, treat as authoritative):\n{plain[:3000]}\n"
    elif course:
        focus_block = (
            f"\n## CURRENT FOCUS\nThe student opened the tutor from the course "
            f"{course.code} — {course.title}. Assume questions are about this course "
            f"unless they clearly ask about something else.\n"
        )
        if course.description:
            focus_block += f"\nCourse description on file: {course.description}\n"

    if material:
        if material_text:
            focus_block += (
                f"\n## SELECTED MATERIAL: \"{material.title}\"\nThe student selected this "
                f"study material. Its actual extracted text follows -- base answers about "
                f"it ONLY on this text; if something isn't covered here, say so honestly "
                f"instead of inventing it.\n\nMATERIAL TEXT:\n{material_text[:MAX_MATERIAL_CHARS]}\n"
            )
        else:
            focus_block += (
                f"\n## SELECTED MATERIAL: \"{material.title}\"\nThe student selected this "
                f"material, but Nelavista could not extract readable text from it. Do not "
                f"claim to have read it -- say so if asked, and answer from general "
                f"subject knowledge instead.\n"
            )

    style = prefs.ai_response_style if prefs else 'balanced'
    approach = prefs.ai_teaching_approach if prefs else 'step_by_step'
    difficulty = prefs.ai_difficulty if prefs else 'university'
    personal_context = ((prefs.ai_personal_context if prefs else None) or '').strip()
    personalization_lines = [
        f"- Response depth: {_RESPONSE_STYLE_INSTRUCTIONS.get(style, _RESPONSE_STYLE_INSTRUCTIONS['balanced'])}",
        f"- Teaching approach: {_TEACHING_APPROACH_INSTRUCTIONS.get(approach, _TEACHING_APPROACH_INSTRUCTIONS['step_by_step'])}",
        f"- Difficulty level: {_DIFFICULTY_INSTRUCTIONS.get(difficulty, _DIFFICULTY_INSTRUCTIONS['university'])}",
    ]
    if personal_context:
        personalization_lines.append(f"- Additional context this student shared about themselves: {personal_context}")

    return f"""You are the AI Tutor inside Nelavista Academia -- a university's own study companion, not a general-purpose chatbot. You exist specifically to help this student learn their courses, understand difficult topics, and prepare for exams.

## STUDENT
{chr(10).join(context_lines)}
{focus_block}
## HOW YOU TEACH
- Teach like an excellent, direct university lecturer -- clear, warm, and precise, never childish, never gimmicky.
- Match depth to what was actually asked: a quick question gets a focused answer, not a forced essay. Only build out a full explanation when the question genuinely calls for one.
- When it helps, structure a fuller explanation loosely as: the core concept, then a concrete example, then (when the topic supports practice) a short "try it yourself" prompt, then a one-line key takeaway. Never force this shape onto a simple answer -- skip sections that would just be filler.
- For "quiz me" or "practice" requests: ask ONE question at a time and wait for the student's answer before giving the next question or revealing the solution. Never dump a whole question bank at once.
- Be honest about the limits of what you actually know or have been given (see CURRENT FOCUS / SELECTED MATERIAL above) -- never invent specific facts about a course, lecturer, or material you have not actually been shown.
- Address the student by name occasionally, not every message.

## PERSONALIZATION (from this student's Settings)
{chr(10).join(personalization_lines)}

## FORMAT
Respond in clean Markdown (this renders in a real markdown viewer with math support):
- `#`/`##`/`###` headings only for genuinely multi-part answers -- skip them for short answers.
- **bold** / *italics* for emphasis, never overused.
- Numbered lists for steps/procedures, bullet lists for unordered points.
- Markdown tables for comparisons.
- Fenced code blocks with a language tag for any code.
- LaTeX for math: inline as \\( ... \\), display as $$ ... $$. Never split one expression across multiple delimiters.
- No emojis except, at most, one per response, and only if it genuinely fits.

Never mention that you are built on any particular AI provider or model -- you are Nelavista's AI Tutor."""


def stream_chat_completion(messages, model=TUTOR_MODEL, temperature=0.5, max_tokens=1800):
    """Generator yielding incremental text deltas from OpenRouter's streaming chat
    completions endpoint. Yields a single fallback string and returns if the request
    fails outright (mirrors the GRACEFUL_FALLBACK convention in routes/ai_routes.py) --
    callers should treat every yielded chunk as literal text to append, not JSON.
    """
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": True,
    }
    try:
        response = requests.post(OPENROUTER_URL, headers=_headers(), json=payload, stream=True, timeout=120)
    except requests.exceptions.RequestException:
        yield "I'm having trouble reaching the tutor right now — please try again in a moment."
        return

    if response.status_code != 200:
        yield "I'm having trouble reaching the tutor right now — please try again in a moment."
        return

    # OpenRouter's SSE stream has no charset in its Content-Type, and requests falls back
    # to ISO-8859-1 (the HTTP default for text/*) whenever a response doesn't declare one --
    # decode_unicode=True below would then mis-decode every multi-byte UTF-8 character (curly
    # quotes, em dashes, accented letters) into 2-3 garbled/invisible-control-char codepoints,
    # silently corrupting stored conversation history. Force the correct encoding explicitly.
    response.encoding = 'utf-8'

    got_any = False
    try:
        for raw_line in response.iter_lines(decode_unicode=True):
            if not raw_line or not raw_line.startswith('data: '):
                continue
            data = raw_line[len('data: '):].strip()
            if data == '[DONE]':
                break
            try:
                obj = json.loads(data)
            except ValueError:
                continue
            choices = obj.get('choices') or []
            if not choices:
                continue
            delta = (choices[0].get('delta') or {}).get('content')
            if delta:
                got_any = True
                yield delta
    finally:
        response.close()

    if not got_any:
        yield "I'm having trouble responding right now — please try again."


def generate_conversation_title(first_user_message, course=None):
    """One cheap, non-streamed AI call to summarize the opening exchange into a short
    title (3-6 words) -- run once, after the first assistant reply, from
    routes/tutor_routes.py. Falls back to a heuristic truncation of the student's own
    message if the AI call fails, so a title is always produced without ever inventing
    conversation content that didn't happen.
    """
    snippet = first_user_message.strip()
    fallback = ' '.join(snippet.split()[:7]).rstrip('.,!?') or "New chat"
    if len(fallback) > 60:
        fallback = fallback[:57].rstrip() + '...'
    if course:
        fallback = f"{course.code} — {fallback}"

    try:
        payload = {
            "model": TUTOR_MODEL,
            "messages": [
                {"role": "system", "content": (
                    "Summarize the student's question below into a short conversation "
                    "title: 3-6 words, no trailing punctuation, no quotes, title case. "
                    "Output ONLY the title, nothing else."
                )},
                {"role": "user", "content": snippet[:500]},
            ],
            "temperature": 0.3,
            "max_tokens": 20,
        }
        resp = requests.post(OPENROUTER_URL, headers=_headers(), json=payload, timeout=15)
        if resp.status_code == 200:
            title = resp.json()["choices"][0]["message"]["content"].strip().strip('"').strip("'")
            if title:
                return f"{course.code} — {title}" if course else title
    except Exception:
        pass
    return fallback


def build_quick_prompts(course=None, topic=None, department=None):
    """Contextual starter prompts for the composer/empty-state -- built from real
    course/topic data (never a hardcoded example course/topic), per the product
    requirement that suggestions must reflect the student's actual academic context.
    Returns a list of {"label": short chip text, "prompt": full message to send}.
    """
    if topic and course:
        return [
            {"label": "Teach me this from the beginning",
             "prompt": f"Teach me \"{topic.title}\" from {course.code} from the beginning, as if I'm seeing it for the first time."},
            {"label": "Give me an example",
             "prompt": f"Give me a concrete worked example of \"{topic.title}\"."},
            {"label": "Quiz me",
             "prompt": f"Quiz me on \"{topic.title}\". Ask one question at a time and wait for my answer before the next one."},
            {"label": "Common mistakes",
             "prompt": f"What mistakes do students usually make with \"{topic.title}\"?"},
        ]
    if course:
        first_topic = course.topics.filter_by(is_active=True).order_by(Topic.order).first()
        teach_prompt = (
            f"Teach me \"{first_topic.title}\", the first topic in {course.code}."
            if first_topic else f"Teach me the basics of {course.code} — {course.title}."
        )
        return [
            {"label": "Teach me the first topic", "prompt": teach_prompt},
            {"label": "What should I know for my exam?",
             "prompt": f"What are the most important things I should know for my {course.code} exam?"},
            {"label": "Quiz me on this course",
             "prompt": f"Quiz me on {course.code} — {course.title}. Ask one question at a time."},
            {"label": "Explain the hardest topics",
             "prompt": f"What are usually the hardest topics in {course.code}, and can you explain them simply?"},
        ]
    dept = f" in {department}" if department else ""
    return [
        {"label": "Explain a topic", "prompt": f"Explain a topic to me{dept} — ask me which one first."},
        {"label": "Help me solve a question", "prompt": "Help me solve a question step by step. I'll paste it now."},
        {"label": "Summarize my material", "prompt": "Help me summarize a study material into concise notes. I'll tell you what it's about."},
        {"label": "Prepare me for an exam", "prompt": f"Help me prepare for an exam{dept}. Ask me which course first."},
    ]


TUTOR_ACTIONS = {
    'explain': lambda target: f"Explain {target} in simple, easy-to-understand language, as if I'm seeing it for the first time.",
    'steps': lambda target: f"Break down how to solve problems on {target} into clear step-by-step processes, with a worked example.",
    'quiz': lambda target: f"Quiz me on {target}. Ask one question at a time, wait for my answer, then tell me if I'm right before giving the next question.",
    'practice': lambda target: f"Give me a practice question on {target}, then wait for my answer before showing me the solution.",
    'summarize': lambda target: f"Summarize the key points of {target} into concise study notes I can revise from.",
    'exam_prep': lambda target: f"Help me prepare for my exam on {target}. Cover the most important concepts and likely exam questions.",
}
