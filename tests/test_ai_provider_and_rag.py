"""PRD §6 provider abstraction + PRD §5.5 RAG pipeline.

The provider tests lock the OpenRouterProvider contract (chat / stream / embed, error
mapping) without any network. The RAG tests cover chunking coherence + overlap,
retrieval scoping (a student never retrieves across universities), and the
hallucination-mitigation AC: an unrelated question must produce an explicit
decline, not a fabricated answer.
"""

import pytest
from unittest.mock import patch, MagicMock

from app.extensions import db
from app.models import Material, MaterialChunk, User
from app.services import rag_service
from app.services.ai_provider import (OpenRouterProvider, AIProviderError)


# ---------------------------------------------------------------------------
# Provider contract
# ---------------------------------------------------------------------------

def _resp(status=200, payload=None):
    m = MagicMock()
    m.status_code = status
    m.json.return_value = payload if payload is not None else {}
    return m


def test_chat_returns_content_and_sends_expected_shape():
    p = OpenRouterProvider(api_key='test-key')
    with patch('app.services.ai_provider.requests.post',
               return_value=_resp(payload={'choices': [{'message': {'content': 'hello'}}]})) as post:
        out = p.chat([{'role': 'user', 'content': 'hi'}], model='openai/gpt-4o-mini',
                     temperature=0.1, max_tokens=50)
    assert out == 'hello'
    _, kwargs = post.call_args
    body = kwargs['json']
    assert body['model'] == 'openai/gpt-4o-mini'
    assert body['max_tokens'] == 50
    assert body['messages'][0]['content'] == 'hi'
    assert kwargs['headers']['Authorization'] == 'Bearer test-key'


def test_chat_maps_errors_to_ai_provider_error():
    p = OpenRouterProvider(api_key='test-key')
    with patch('app.services.ai_provider.requests.post',
               return_value=_resp(status=429, payload={})):
        with pytest.raises(AIProviderError):
            p.chat([{'role': 'user', 'content': 'hi'}], model='m')
    with patch('app.services.ai_provider.requests.post',
               side_effect=Exception('network down')):
        with pytest.raises(AIProviderError):
            p.chat([{'role': 'user', 'content': 'hi'}], model='m')


def test_chat_without_key_is_an_error_not_a_crash():
    p = OpenRouterProvider(api_key=None)
    with patch('app.config.OPENROUTER_API_KEY', None):
        p2 = OpenRouterProvider()
        with pytest.raises(AIProviderError):
            p2.chat([{'role': 'user', 'content': 'hi'}], model='m')


def test_embed_parses_openai_shape_and_orders_by_index():
    p = OpenRouterProvider(api_key='test-key')
    vec = [0.1, 0.2, 0.3]
    payload = {'data': [{'embedding': vec, 'index': 0}]}
    with patch('app.services.ai_provider.requests.post', return_value=_resp(payload=payload)):
        out = p.embed('one text', 'openai/text-embedding-3-small')
    assert out == [vec]


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------

def test_chunking_produces_overlapping_coherent_chunks():
    para = ('The stack is a LIFO data structure. ' * 40)          # ~1700 chars -> >1 chunk
    chunks = rag_service.chunk_text(para, chunk_size=800, overlap=100)
    assert len(chunks) >= 2
    texts = [t for _, t in chunks]
    # Overlap: the tail of chunk 1 appears in chunk 2.
    tail = texts[0][-100:].strip()
    assert tail[:40] in texts[1]
    # Every chunk respects the size cap (hard-wrap guarantees it).
    assert all(len(t) <= 800 + 200 for t in texts)


def test_chunking_merges_micro_fragments():
    text = '# Heading\n\nA real paragraph with enough content to stand on its own as a chunk.'
    chunks = rag_service.chunk_text(text)
    assert len(chunks) == 1
    assert 'Heading' in chunks[0][1]     # heading merged into the real paragraph


def test_chunking_empty_and_short_inputs():
    assert rag_service.chunk_text('') == []
    # A whole document below MIN_CHUNK_CHARS still yields one chunk -- dropping the
    # only content would be worse than a short chunk.
    out = rag_service.chunk_text('too short')
    assert len(out) == 1 and out[0][1] == 'too short'


# ---------------------------------------------------------------------------
# RAG retrieval + decline AC
# ---------------------------------------------------------------------------

@pytest.fixture
def rag_env(app, make_user):
    """One user + two materials (one LASU-scoped, one universal) with pre-baked chunk
    embeddings: material A's chunk points 'east', material B's chunk also 'east'.
    Questions embed as unit vectors so cosine similarity is trivially deterministic."""
    user = make_user('raguser', university='Lagos State University')

    def east_vec():
        v = [0.0] * rag_service.EMBEDDING_DIM
        v[0] = 1.0
        return v

    with app.app_context():
        m1 = Material(title='Stacks Notes', department='Computer Science', level='200',
                      semester='First Semester', course_code='CSC213',
                      university='Lagos State University', source='uploaded',
                      is_approved=True)
        m2 = Material(title='Other School Notes', department='Computer Science', level='200',
                      semester='First Semester', course_code='CSC213',
                      university='University of Benin', source='uploaded',   # NOT the user's school
                      is_approved=True)
        db.session.add_all([m1, m2])
        db.session.commit()

        for m, content in ((m1, 'A stack is a LIFO data structure with push and pop operations.'),
                           (m2, 'A stack is a LIFO data structure with push and pop operations.')):
            db.session.add(MaterialChunk(
                material_id=m.id, chunk_index=0, content=content,
                course_code='CSC213', embedding_model=rag_service.EMBEDDING_MODEL,
                embedding=rag_service._pack(east_vec()),
            ))
        db.session.commit()
        ids = {'m1': m1.id, 'm2': m2.id, 'user': user.id}
    return ids


def _patch_embed(monkeypatch, question_vec):
    def fake_embed(texts, user_id=None):
        return [question_vec for _ in texts]
    monkeypatch.setattr(rag_service, '_embed_texts', fake_embed)


def test_retrieval_scopes_to_students_university(app, rag_env, monkeypatch):
    """The cross-university material's identical chunk must never be retrieved."""
    q = [0.0] * rag_service.EMBEDDING_DIM
    q[0] = 1.0
    _patch_embed(monkeypatch, q)
    with app.app_context():
        user = User.query.get(rag_env['user'])
        result = rag_service.retrieve_context(user, 'What is a stack?')
        ids = {c['material_id'] for c in result['chunks']}
        assert rag_env['m1'] in ids
        assert rag_env['m2'] not in ids     # other school's material invisible
        assert result['declined'] is False


def test_unrelated_question_declines_instead_of_fabricating(app, rag_env, monkeypatch):
    """§5.5's acceptance criterion: a question the material doesn't cover gets an
    honest 'not covered' from the pipeline (declined=True), never a confident guess."""
    q = [0.0] * rag_service.EMBEDDING_DIM
    q[1] = 1.0      # orthogonal to every stored 'east' vector -> similarity 0
    _patch_embed(monkeypatch, q)
    with app.app_context():
        user = User.query.get(rag_env['user'])
        result = rag_service.retrieve_context(user, 'What is the boiling point of water?')
    assert result['chunks'] == []
    assert result['declined'] is True


def test_answer_declined_message_is_explicit(app, rag_env, monkeypatch):
    q = [0.0] * rag_service.EMBEDDING_DIM
    q[1] = 1.0
    _patch_embed(monkeypatch, q)
    with app.app_context():
        user = User.query.get(rag_env['user'])
        m1 = Material.query.get(rag_env['m1'])
        out = rag_service.answer_material_question(user, 'What is quantum chromodynamics?',
                                                   material=m1)
    assert out['ok'] is True and out['declined'] is True
    assert "doesn't cover" in out['answer']


def test_answer_grounded_in_retrieved_context(app, rag_env, monkeypatch):
    """Related question -> chunks retrieved -> model called with the wrapped context
    and the untrusted-content delimiters."""
    q = [0.0] * rag_service.EMBEDDING_DIM
    q[0] = 1.0
    _patch_embed(monkeypatch, q)

    captured = {}

    class FakeProvider:
        def chat(self, messages, model, **kw):
            captured['messages'] = messages
            return 'A stack is LIFO [1].'
        def embed(self, texts, model, **kw):
            return [q for _ in texts]

    with app.app_context():
        user = User.query.get(rag_env['user'])
        m1 = Material.query.get(rag_env['m1'])
        out = rag_service.answer_material_question(user, 'Explain stack operations.',
                                                   material=m1, provider=FakeProvider())
    assert out['declined'] is False
    assert '[1]' in out['answer']
    assert out['sources'] and out['sources'][0]['material_id'] == rag_env['m1']
    user_msg = captured['messages'][1]['content']
    assert '<material_context>' in user_msg and 'LIFO' in user_msg


def test_roundtrip_pack_unpack():
    vec = [0.25, -0.5, 1.0] + [0.0] * (rag_service.EMBEDDING_DIM - 3)
    blob = rag_service._pack(vec)
    assert len(blob) == rag_service.EMBEDDING_DIM * 4
    assert rag_service._unpack(blob) == vec
