"""
Real PDF/image extraction backing the "Analyze Materials" feature (routes/ai_routes.py's
/analyze and /understand endpoints). This used to be all stub functions that made the
feature entirely non-functional — every upload failed with "PDF is unreadable" because
extract_text_from_pdf_turbo() always returned the literal string "PDF text extraction not
implemented.".

- Text + tables: pdfplumber (pure Python, no system binary required)
- Embedded images: PyMuPDF/fitz (pure Python wheel, no system binary required)

Deliberately NOT using pytesseract/Tesseract OCR here — that needs a system binary that
isn't guaranteed to exist in every deployment environment (e.g. Render's default Python
buildpack doesn't include it). extract_text_from_image() below degrades gracefully instead
of crashing if Tesseract isn't installed; if OCR turns out to matter, install Tesseract in
the deploy environment and this will pick it up automatically without further code changes.
"""
import os
import re
import time
import uuid

import pdfplumber
import fitz  # PyMuPDF

from config import DEBUG_MODE


def debug_print(*args, **kwargs):
    if DEBUG_MODE:
        print(*args, **kwargs)


def extract_text_from_pdf(file):
    """Extract all text from a PDF, page by page, in reading order."""
    try:
        file.seek(0)
        pages_text = []
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                if text.strip():
                    pages_text.append(text)
        return "\n\n".join(pages_text)
    except Exception as e:
        debug_print(f"❌ PDF text extraction failed: {e}")
        return ""


def extract_text_from_pdf_turbo(file):
    """Same extraction as extract_text_from_pdf — kept as a separate name because
    routes/ai_routes.py calls this one specifically for the main analyzer flow."""
    return extract_text_from_pdf(file)


def extract_images_from_pdf(file, session_id):
    """
    Extract embedded raster images from a PDF, save them under IMAGE_FOLDER/<session_id>/,
    and return metadata routes/ai_routes.py's /understand endpoint expects: a list of dicts
    with 'path' (local filesystem path, checked with os.path.exists), 'url' (served via
    ai_bp's /static/extracted_images/<path:filename> route), 'alt', and 'page'.
    """
    try:
        file.seek(0)
        file_bytes = file.read()
        if not file_bytes:
            return []

        image_folder = os.path.join(os.getcwd(), 'extracted_images', session_id)
        os.makedirs(image_folder, exist_ok=True)

        results = []
        doc = fitz.open(stream=file_bytes, filetype='pdf')
        try:
            for page_index in range(len(doc)):
                page = doc[page_index]
                for img_index, img in enumerate(page.get_images(full=True)):
                    xref = img[0]
                    try:
                        base_image = doc.extract_image(xref)
                    except Exception as e:
                        debug_print(f"⚠️ Skipping image xref {xref}: {e}")
                        continue

                    ext = base_image.get('ext', 'png')
                    # Skip tiny images — these are almost always icons/bullets/rules embedded
                    # in the page background, not real diagrams worth surfacing.
                    if base_image.get('width', 0) < 80 or base_image.get('height', 0) < 80:
                        continue

                    filename = f"p{page_index + 1}_{img_index}_{uuid.uuid4().hex[:8]}.{ext}"
                    filepath = os.path.join(image_folder, filename)
                    with open(filepath, 'wb') as f:
                        f.write(base_image['image'])

                    results.append({
                        'path': filepath,
                        'url': f"/static/extracted_images/{session_id}/{filename}",
                        'alt': f"Diagram from page {page_index + 1}",
                        'page': page_index + 1,
                    })

                    if len(results) >= 20:  # sane cap — don't extract hundreds of images
                        return results
        finally:
            doc.close()

        return results
    except Exception as e:
        debug_print(f"❌ Image extraction failed: {e}")
        return []


def extract_tables_from_pdf(file):
    """
    Extract tables via pdfplumber and return a list of dicts with 'page', 'text' (plain
    preview), and 'markdown' (rendered as a Markdown table) — the exact shape
    services/ai_service.py's generate_structured_fallback()/enhance_notes_with_extractions()
    already expect.
    """
    try:
        file.seek(0)
        results = []
        with pdfplumber.open(file) as pdf:
            for page_index, page in enumerate(pdf.pages):
                try:
                    tables = page.extract_tables()
                except Exception as e:
                    debug_print(f"⚠️ Table extraction failed on page {page_index + 1}: {e}")
                    continue

                for table in tables:
                    # Drop fully-empty rows/cells noise
                    rows = [row for row in table if any((cell or '').strip() for cell in row)]
                    if len(rows) < 2:  # need at least a header + one data row to be useful
                        continue

                    markdown = _table_to_markdown(rows)
                    preview = " | ".join(cell or '' for cell in rows[0])

                    results.append({
                        'page': page_index + 1,
                        'text': preview,
                        'markdown': markdown,
                    })

                    if len(results) >= 15:  # sane cap
                        return results
        return results
    except Exception as e:
        debug_print(f"❌ Table extraction failed: {e}")
        return []


def _table_to_markdown(rows):
    header, *data_rows = rows
    header_cells = [(cell or '').strip() or ' ' for cell in header]
    lines = [
        "| " + " | ".join(header_cells) + " |",
        "| " + " | ".join(['---'] * len(header_cells)) + " |",
    ]
    for row in data_rows:
        cells = [(cell or '').strip().replace('\n', ' ') or ' ' for cell in row]
        # Pad/truncate to header width so ragged rows don't break the table
        if len(cells) < len(header_cells):
            cells += [' '] * (len(header_cells) - len(cells))
        elif len(cells) > len(header_cells):
            cells = cells[:len(header_cells)]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


# Heuristic-only — patterns commonly seen in headings/section titles across lecture notes
# and textbook chapters. Not a substitute for an NLP model, but doesn't cost an extra AI
# call, and services/ai_service.py's AI-generated notes are the primary output anyway —
# this only backs the structured fallback path when the AI call itself fails.
_HEADING_RE = re.compile(r'^(chapter|unit|section|part|topic)\s+\d+', re.IGNORECASE)
_NUMBERED_RE = re.compile(r'^\d+(\.\d+)*[\.\)]\s+\S')
_DEFINITION_RE = re.compile(
    r'([A-Z][A-Za-z0-9 ,\-]{2,60}?)\s+(?:is|are|refers to|means|can be defined as)\s+([^.]{10,200}\.)'
)


def analyze_document_structure(text):
    """
    Lightweight heuristic pass over extracted text — no extra AI call. Returns
    document_title / main_topics / definitions, matching what routes/ai_routes.py and
    services/ai_service.py's fallback notes path expect.
    """
    if not text or not text.strip():
        return {'document_title': '', 'main_topics': [], 'definitions': []}

    lines = [l.strip() for l in text.split('\n') if l.strip()]

    # Title: first substantial line that isn't just a page number/header fragment
    title = ''
    for line in lines[:15]:
        if 8 <= len(line) <= 120 and not line.isdigit():
            title = line
            break

    # Topics: short lines that look like headings (numbered, "Chapter N", or short Title Case)
    topics = []
    seen = set()
    for line in lines:
        if len(line) > 90:
            continue
        is_heading = bool(_HEADING_RE.match(line) or _NUMBERED_RE.match(line))
        is_title_case = line == line.title() and 3 <= len(line.split()) <= 10 and line[0].isupper()
        if (is_heading or is_title_case) and line not in seen:
            topics.append(line)
            seen.add(line)
        if len(topics) >= 12:
            break

    # Definitions: sentences matching "X is/are/means Y" patterns
    definitions = []
    for match in _DEFINITION_RE.finditer(text):
        term, definition = match.group(1).strip(), match.group(2).strip()
        sentence = f"{term} — {definition}"
        if sentence not in definitions:
            definitions.append(sentence)
        if len(definitions) >= 10:
            break

    return {
        'document_title': title,
        'main_topics': topics,
        'definitions': definitions,
    }


def is_diagram_or_visual(text):
    """Heuristic: does this caption/alt text suggest a diagram/chart rather than a photo."""
    if not text:
        return False
    keywords = ('diagram', 'chart', 'graph', 'figure', 'flowchart', 'schematic', 'illustration', 'plot')
    return any(k in text.lower() for k in keywords)


def extract_text_from_image(file):
    """
    OCR on a standalone image upload. Requires pytesseract + a system Tesseract install,
    neither of which is guaranteed present in every deploy environment. Degrades gracefully
    (returns a clear placeholder instead of crashing) if unavailable — the primary image
    understanding path in routes/ai_routes.py's ask_with_files() already sends images
    straight to a vision-capable model instead of relying on this function.
    """
    try:
        import pytesseract
        from PIL import Image
        file.seek(0)
        image = Image.open(file)
        text = pytesseract.image_to_string(image)
        return text.strip() or "DIAGRAM_OR_VISUAL_CONTENT"
    except ImportError:
        debug_print("⚠️ pytesseract/Tesseract not installed — OCR unavailable, skipping")
        return "DIAGRAM_OR_VISUAL_CONTENT"
    except Exception as e:
        debug_print(f"❌ OCR failed: {e}")
        return "DIAGRAM_OR_VISUAL_CONTENT"
