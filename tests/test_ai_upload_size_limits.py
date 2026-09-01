"""Regression tests for P0-5 of the stabilization pass: /generate-test's image branch and
/ask_with_files had no size cap at all, unlike /analyze and /generate-test's PDF branch
(both bounded by MAX_ANALYZE_PDF_BYTES). A large enough upload could block the single
eventlet worker on synchronous parsing and/or balloon the OpenRouter request payload.
"""
import io
from routes.ai_routes import MAX_ANALYZE_PDF_BYTES, MAX_IMAGE_BYTES


def test_generate_test_rejects_oversized_image(client, make_user, login_as):
    user = make_user('upload_tester2')
    login_as(client, user)

    oversized = io.BytesIO(b'\x89PNG\r\n\x1a\n' + b'0' * (MAX_IMAGE_BYTES + 1))
    res = client.post('/generate-test', data={
        'file': (oversized, 'huge.png'),
        'test_type': 'cbt',
    }, content_type='multipart/form-data')

    assert res.status_code == 413
    body = res.get_json()
    assert body['success'] is False
    assert 'too large' in body['error'].lower()


def test_generate_test_rejects_oversized_pdf(client, make_user, login_as):
    user = make_user('upload_tester3')
    login_as(client, user)

    oversized = io.BytesIO(b'%PDF-1.4\n' + b'0' * (MAX_ANALYZE_PDF_BYTES + 1))
    res = client.post('/generate-test', data={
        'file': (oversized, 'huge.pdf'),
        'test_type': 'cbt',
    }, content_type='multipart/form-data')

    assert res.status_code == 413


def test_ask_with_files_skips_oversized_pdf_instead_of_processing_it(client, make_user, login_as):
    """An oversized attachment with no message and no other valid content should hit the
    'nothing to analyze' fallback -- proof the file was skipped by the size guard before
    ever reaching extract_text_from_pdf(), not silently processed anyway."""
    user = make_user('upload_tester4')
    login_as(client, user)

    oversized = io.BytesIO(b'%PDF-1.4\n' + b'0' * (MAX_ANALYZE_PDF_BYTES + 1))
    res = client.post('/ask_with_files', data={
        'files': (oversized, 'huge.pdf'),
    }, content_type='multipart/form-data')

    assert res.status_code == 200
    body = res.get_json()
    assert body['success'] is True
    assert 'provide a message or upload files' in body['answer'].lower()
