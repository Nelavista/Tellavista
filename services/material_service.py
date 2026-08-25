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
import io
import os
import re
import time
import uuid
from datetime import datetime

import pdfplumber
import fitz  # PyMuPDF
import requests
import cloudinary
import cloudinary.uploader

from config import DEBUG_MODE

# Configured independently here (same pattern as routes/materials_routes.py and
# routes/community_routes.py) rather than relying on another module having already
# configured the global cloudinary client first -- config() is idempotent, so this is
# safe to call from multiple modules.
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
    secure=True
)


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


# Matches the truncation convention already used in services/ai_service.py's
# generate_test_questions() ("cap the source text so a huge document doesn't blow the
# prompt token budget") -- reused here for the same reason.
MATERIAL_TEXT_CHAR_CAP = 12000


def get_or_extract_material_text(material):
    """Real per-material content retrieval for the AI tutor -- downloads the material's
    PDF and extracts its text on first use, then caches it on the Material row so a
    second question about the same material doesn't re-download/re-parse it. Returns
    None on ANY failure (no URL, download error, not a PDF, empty extraction) -- callers
    MUST treat None as 'could not read this file' and say so honestly, never silently
    fall back to answering as if the content were available."""
    if material.extracted_text and material.extracted_at:
        return material.extracted_text

    url = material.file_url or material.external_url
    if not url:
        return None

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        text = extract_text_from_pdf(io.BytesIO(response.content))
    except Exception as e:
        debug_print(f"⚠️ Material content fetch/extract failed for material {material.id}: {e}")
        return None

    if not text or len(text.strip()) < 50:  # too little to be a usable extraction
        return None

    text = text[:MATERIAL_TEXT_CHAR_CAP]

    # Cache on the row -- best-effort; a failed commit here shouldn't break the
    # in-flight AI response that already has the text in hand.
    try:
        from extensions import db
        material.extracted_text = text
        material.extracted_at = datetime.utcnow()
        db.session.commit()
    except Exception as e:
        debug_print(f"⚠️ Failed to cache extracted text for material {material.id}: {e}")
        from extensions import db
        db.session.rollback()

    return text


def extract_images_from_pdf(file, session_id):
    """
    Extract embedded raster images from a PDF and upload each to Cloudinary (folder
    nelavista_analyzer/<session_id>/), returning a list of dicts with 'url' (the
    Cloudinary secure_url), 'alt', and 'page'. Previously these were written to local
    disk under extracted_images/<session_id>/ and served back via a same-origin route --
    on Render's ephemeral filesystem, a redeploy or restart between a student generating
    notes and revisiting them silently broke every image (404s where a diagram used to
    be). Cloudinary is already how every other user-facing file in this app is stored
    (see routes/materials_routes.py, routes/community_routes.py) -- this brings the AI
    Analyzer's images in line with that, instead of being the one exception.
    """
    try:
        file.seek(0)
        file_bytes = file.read()
        if not file_bytes:
            return []

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

                    # Skip tiny images — these are almost always icons/bullets/rules embedded
                    # in the page background, not real diagrams worth surfacing.
                    if base_image.get('width', 0) < 80 or base_image.get('height', 0) < 80:
                        continue

                    public_id = f"nelavista_analyzer/{session_id}/p{page_index + 1}_{img_index}_{uuid.uuid4().hex[:8]}"
                    try:
                        upload_result = cloudinary.uploader.upload(
                            io.BytesIO(base_image['image']),
                            resource_type='image',
                            public_id=public_id,
                            overwrite=False,
                        )
                        image_url = upload_result.get('secure_url')
                    except Exception as e:
                        debug_print(f"⚠️ Cloudinary upload failed for {public_id}: {e}")
                        continue
                    if not image_url:
                        continue

                    results.append({
                        'url': image_url,
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
