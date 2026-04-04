import os
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
            "X-Title": "Nellavista Turbo-Style Notes Generator"
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
    enhanced += f"\n\n---\n*Generated by Nellavista Academic Document Analyzer | {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"
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