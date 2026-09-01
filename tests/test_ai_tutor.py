"""Tests for the AI Tutor (routes/tutor_routes.py, services/tutor_service.py).

OpenRouter is never called here -- stream_chat_completion / generate_conversation_title
are monkeypatched at their routes.tutor_routes import site (not the defining module,
since routes.tutor_routes already bound its own reference at import time).
"""
import json
from datetime import datetime
import pytest
from extensions import db
from models import TutorConversation, TutorMessage


@pytest.fixture
def client(app):
    # tests/conftest.py's shared `app` fixture now registers tutor_bp itself (see
    # "Fix AI Tutor cross-university/department content leak") -- registering it again
    # here raises "already registered for this blueprint".
    return app.test_client()


def _fake_stream(messages, **kwargs):
    yield "Hello "
    yield "world."


def _stub_ai(monkeypatch, title="A Test Title", stream=_fake_stream):
    monkeypatch.setattr('routes.tutor_routes.stream_chat_completion', stream)
    monkeypatch.setattr('routes.tutor_routes.generate_conversation_title', lambda *a, **k: title)


def _read_sse_events(response):
    text = response.get_data(as_text=True)
    events = []
    for chunk in text.split('\n\n'):
        chunk = chunk.strip()
        if chunk.startswith('data: '):
            events.append(json.loads(chunk[len('data: '):]))
    return events


class TestPageAuth:
    def test_ai_tutor_page_requires_login(self, client):
        resp = client.get('/ai-tutor')
        assert resp.status_code == 302
        assert '/login' in resp.headers['Location']


class TestConversationCrud:
    def test_create_list_get_delete_conversation(self, client, make_user, login_as):
        user = make_user(username='tutor_a')
        login_as(client, user)

        resp = client.post('/api/tutor/conversations')
        assert resp.status_code == 200
        conv = resp.get_json()['conversation']
        assert conv['title'] == 'New chat'

        resp = client.get('/api/tutor/conversations')
        ids = [c['id'] for c in resp.get_json()['conversations']]
        assert conv['id'] in ids

        resp = client.get(f"/api/tutor/conversations/{conv['id']}")
        assert resp.status_code == 200
        assert resp.get_json()['messages'] == []

        resp = client.delete(f"/api/tutor/conversations/{conv['id']}")
        assert resp.status_code == 200
        resp = client.get(f"/api/tutor/conversations/{conv['id']}")
        assert resp.status_code == 404

    def test_cannot_access_another_users_conversation(self, client, make_user, login_as):
        owner = make_user(username='owner')
        intruder = make_user(username='intruder')

        login_as(client, owner)
        conv_id = client.post('/api/tutor/conversations').get_json()['conversation']['id']

        login_as(client, intruder)
        assert client.get(f'/api/tutor/conversations/{conv_id}').status_code == 404
        assert client.delete(f'/api/tutor/conversations/{conv_id}').status_code == 404
        assert client.patch(f'/api/tutor/conversations/{conv_id}',
                             json={'title': 'hijacked'}).status_code == 404

    def test_conversation_scoped_to_course_and_topic(self, client, make_user, login_as, make_course, app):
        from models import Topic
        user = make_user(username='tutor_ctx')
        course = make_course(code='CSC201', title='Computer Programming I', level='200')
        with app.app_context():
            topic = Topic(course_id=course.id, title='Variables & Data Types', order=1)
            db.session.add(topic)
            db.session.commit()
            topic_id = topic.id
        login_as(client, user)

        resp = client.post(f'/api/tutor/conversations?course=CSC201&topic={topic_id}')
        conv = resp.get_json()['conversation']
        assert conv['course_code'] == 'CSC201'
        assert conv['topic_title'] == 'Variables & Data Types'


class TestMessaging:
    def test_send_message_persists_user_and_assistant_turns(self, client, make_user, login_as, monkeypatch):
        user = make_user(username='tutor_send')
        login_as(client, user)
        _stub_ai(monkeypatch)

        conv_id = client.post('/api/tutor/conversations').get_json()['conversation']['id']
        resp = client.post(f'/api/tutor/conversations/{conv_id}/messages',
                            json={'content': 'What is a variable?'})
        assert resp.status_code == 200
        assert resp.mimetype == 'text/event-stream'
        events = _read_sse_events(resp)
        assert ''.join(e['delta'] for e in events if 'delta' in e) == 'Hello world.'
        done = [e for e in events if e.get('done')][0]
        assert done['title'] == 'A Test Title'

        detail = client.get(f'/api/tutor/conversations/{conv_id}').get_json()
        assert [m['role'] for m in detail['messages']] == ['user', 'assistant']
        assert detail['messages'][0]['content'] == 'What is a variable?'
        assert detail['messages'][1]['content'] == 'Hello world.'
        assert detail['conversation']['title'] == 'A Test Title'

    def test_regenerate_replaces_last_assistant_message_without_duplicating(self, client, make_user, login_as, monkeypatch):
        """Regression test: regenerate must delete the previous assistant turn before
        adding the new one, leaving exactly one user + one assistant message -- never
        two assistant rows for the same question."""
        user = make_user(username='tutor_regen')
        login_as(client, user)
        _stub_ai(monkeypatch)

        conv_id = client.post('/api/tutor/conversations').get_json()['conversation']['id']
        first = client.post(f'/api/tutor/conversations/{conv_id}/messages', json={'content': 'Explain recursion'})
        # A streaming Response's generator only actually runs as it's read -- a real
        # browser always reads the body to completion, so the test must too (Werkzeug's
        # test client does NOT eagerly drain an unread streaming response, unlike a real
        # WSGI server, which always fully iterates + closes the app_iter per the spec).
        first.get_data()

        def _second_answer(messages, **kwargs):
            yield "A different "
            yield "answer."
        monkeypatch.setattr('routes.tutor_routes.stream_chat_completion', _second_answer)

        resp = client.post(f'/api/tutor/conversations/{conv_id}/messages', json={'regenerate': True})
        assert resp.status_code == 200
        events = _read_sse_events(resp)
        assert ''.join(e['delta'] for e in events if 'delta' in e) == 'A different answer.'

        detail = client.get(f'/api/tutor/conversations/{conv_id}').get_json()
        roles = [m['role'] for m in detail['messages']]
        assert roles == ['user', 'assistant'], f"expected exactly one user + one assistant message, got {roles}"
        assert detail['messages'][1]['content'] == 'A different answer.'

    def test_regenerate_with_no_prior_message_fails_cleanly(self, client, make_user, login_as, monkeypatch):
        user = make_user(username='tutor_regen_empty')
        login_as(client, user)
        _stub_ai(monkeypatch)
        conv_id = client.post('/api/tutor/conversations').get_json()['conversation']['id']
        resp = client.post(f'/api/tutor/conversations/{conv_id}/messages', json={'regenerate': True})
        assert resp.status_code == 400

    def test_empty_message_rejected(self, client, make_user, login_as, monkeypatch):
        user = make_user(username='tutor_empty_msg')
        login_as(client, user)
        _stub_ai(monkeypatch)
        conv_id = client.post('/api/tutor/conversations').get_json()['conversation']['id']
        resp = client.post(f'/api/tutor/conversations/{conv_id}/messages', json={'content': '   '})
        assert resp.status_code == 400

    def test_message_to_missing_conversation_404s(self, client, make_user, login_as, monkeypatch):
        user = make_user(username='tutor_missing_conv')
        login_as(client, user)
        _stub_ai(monkeypatch)
        resp = client.post('/api/tutor/conversations/999999/messages', json={'content': 'hi'})
        assert resp.status_code == 404


class TestActionPrompt:
    def test_action_prompt_uses_course_context(self, client, make_user, login_as, make_course):
        user = make_user(username='tutor_action')
        make_course(code='CSC201', title='Computer Programming I', level='200')
        login_as(client, user)
        resp = client.post('/api/tutor/action-prompt?course=CSC201', json={'mode': 'quiz'})
        assert resp.status_code == 200
        assert 'CSC201' in resp.get_json()['prompt']

    def test_action_prompt_rejects_unknown_mode(self, client, make_user, login_as):
        user = make_user(username='tutor_action_bad')
        login_as(client, user)
        resp = client.post('/api/tutor/action-prompt', json={'mode': 'not_a_real_mode'})
        assert resp.status_code == 400


class TestTutorServiceUnits:
    def test_build_quick_prompts_generic_when_no_context(self):
        from services.tutor_service import build_quick_prompts
        prompts = build_quick_prompts()
        assert len(prompts) == 4
        assert all('prompt' in p and 'label' in p for p in prompts)

    def test_build_quick_prompts_topic_scoped(self, app, make_course):
        from models import Topic
        from services.tutor_service import build_quick_prompts
        course = make_course(code='CSC201', level='200')
        with app.app_context():
            from models import Course
            course_row = Course.query.get(course.id)
            topic = Topic(course_id=course.id, title='Variables & Data Types', order=1)
            db.session.add(topic)
            db.session.commit()
            prompts = build_quick_prompts(course=course_row, topic=topic)
        labels = [p['label'] for p in prompts]
        assert 'Quiz me' in labels
        assert any('Variables & Data Types' in p['prompt'] for p in prompts)

    def test_system_prompt_grounds_in_topic_explanation_and_is_honest_without_one(self, app, make_course, make_user):
        from models import Topic, Course, User
        from services.tutor_service import build_tutor_system_prompt
        course = make_course(code='CSC201', level='200')
        user = make_user(username='promptuser')
        with app.app_context():
            course_row = Course.query.get(course.id)
            user_row = User.query.get(user.id)
            topic_with_explanation = Topic(course_id=course.id, title='Loops', explanation='<p>A loop repeats code.</p>')
            topic_without = Topic(course_id=course.id, title='Recursion')
            db.session.add_all([topic_with_explanation, topic_without])
            db.session.commit()

            grounded = build_tutor_system_prompt(user_row, course=course_row, topic=topic_with_explanation)
            assert 'A loop repeats code.' in grounded

            ungrounded = build_tutor_system_prompt(user_row, course=course_row, topic=topic_without)
            assert 'A loop repeats code.' not in ungrounded
            assert 'Recursion' in ungrounded

    def test_lookup_finds_course_and_materials_mentioned_by_code(self, app, make_course, make_user):
        from models import Material, User
        from services.tutor_service import lookup_mentioned_course_materials
        make_course(code='MAT207', title='Real Analysis', level='200')
        user = make_user(username='lookupuser', university='Lagos State University', department='Computer Science')
        with app.app_context():
            db.session.add(Material(title='MAT207 Handout', department='Computer Science', level='200',
                                     semester='First Semester', course_code='MAT207', is_approved=True))
            db.session.commit()
            user_row = User.query.get(user.id)
            results = lookup_mentioned_course_materials(user_row, "check my material, there is mat207")
        assert len(results) == 1
        assert results[0]['code'] == 'MAT207'
        assert results[0]['course'] is not None
        assert results[0]['course'].title == 'Real Analysis'
        assert [m.title for m in results[0]['materials']] == ['MAT207 Handout']

    def test_lookup_is_honest_about_unknown_course_code(self, app, make_user):
        from models import User
        from services.tutor_service import lookup_mentioned_course_materials
        user = make_user(username='lookupuser2')
        with app.app_context():
            user_row = User.query.get(user.id)
            results = lookup_mentioned_course_materials(user_row, "what about zzz999")
        assert len(results) == 1
        assert results[0]['course'] is None
        assert results[0]['materials'] == []

    def test_lookup_ignores_messages_with_no_course_code(self, make_user, app):
        from models import User
        from services.tutor_service import lookup_mentioned_course_materials
        user = make_user(username='lookupuser3')
        with app.app_context():
            user_row = User.query.get(user.id)
            assert lookup_mentioned_course_materials(user_row, "what is nelavista about?") == []

    def test_system_prompt_lists_materials_honestly_without_claiming_to_have_read_them(self, app, make_course, make_user):
        from models import Material, Course, User
        from services.tutor_service import build_tutor_system_prompt, lookup_mentioned_course_materials
        make_course(code='MAT207', title='Real Analysis', level='200')
        user = make_user(username='promptuser2', university='Lagos State University', department='Computer Science')
        with app.app_context():
            db.session.add(Material(title='MAT207 Handout', department='Computer Science', level='200',
                                     semester='First Semester', course_code='MAT207', is_approved=True))
            db.session.commit()
            user_row = User.query.get(user.id)
            lookups = lookup_mentioned_course_materials(user_row, "check my material for mat207")
            prompt = build_tutor_system_prompt(user_row, course_lookups=lookups)
        assert 'MAT207 Handout' in prompt
        assert 'Real Analysis' in prompt
        assert 'have NOT read their contents' in prompt

    def test_message_wants_material_content_detects_intent(self):
        from services.tutor_service import message_wants_material_content
        assert message_wants_material_content("check my material, there is mat207") is True
        assert message_wants_material_content("please summarize this") is True
        assert message_wants_material_content("hey what's up") is False


class TestMessagingCourseMaterialLookup:
    def test_mentioning_single_matching_material_auto_grounds_the_answer(self, client, make_user, make_course, login_as, monkeypatch):
        """Regression coverage for the reported UX failure: a student mid-conversation
        says "check my material, there is mat207" and the tutor used to reply "I don't
        have access to your materials" even though Nelavista has exactly that material
        on file. It should now be auto-selected and its real text grounded into the
        system prompt sent to the model."""
        from models import Material
        make_course(code='MAT207', title='Real Analysis', level='200')
        user = make_user(username='tutor_lookup', university='Lagos State University', department='Computer Science')
        with client.application.app_context():
            db.session.add(Material(title='MAT207 Handout', department='Computer Science', level='200',
                                     semester='First Semester', course_code='MAT207', is_approved=True,
                                     extracted_text='Limits are defined using epsilon-delta.', extracted_at=datetime.utcnow()))
            db.session.commit()
        login_as(client, user)

        captured = {}

        def _capturing_stream(messages, **kwargs):
            captured['system'] = messages[0]['content']
            yield "Found it."
        monkeypatch.setattr('routes.tutor_routes.stream_chat_completion', _capturing_stream)
        monkeypatch.setattr('routes.tutor_routes.generate_conversation_title', lambda *a, **k: 'title')

        conv_id = client.post('/api/tutor/conversations').get_json()['conversation']['id']
        resp = client.post(f'/api/tutor/conversations/{conv_id}/messages',
                            json={'content': 'check my material, there is mat207'})
        resp.get_data()

        assert 'SELECTED MATERIAL: "MAT207 Handout"' in captured['system']
        assert 'Limits are defined using epsilon-delta.' in captured['system']

    def test_mentioning_course_with_multiple_materials_lists_instead_of_guessing(self, client, make_user, make_course, login_as, monkeypatch):
        from models import Material
        make_course(code='MAT207', title='Real Analysis', level='200')
        user = make_user(username='tutor_lookup2', university='Lagos State University', department='Computer Science')
        with client.application.app_context():
            db.session.add_all([
                Material(title='MAT207 Handout A', department='Computer Science', level='200',
                         semester='First Semester', course_code='MAT207', is_approved=True),
                Material(title='MAT207 Past Questions', department='Computer Science', level='200',
                         semester='First Semester', course_code='MAT207', is_approved=True),
            ])
            db.session.commit()
        login_as(client, user)

        captured = {}

        def _capturing_stream(messages, **kwargs):
            captured['system'] = messages[0]['content']
            yield "Which one?"
        monkeypatch.setattr('routes.tutor_routes.stream_chat_completion', _capturing_stream)
        monkeypatch.setattr('routes.tutor_routes.generate_conversation_title', lambda *a, **k: 'title')

        conv_id = client.post('/api/tutor/conversations').get_json()['conversation']['id']
        resp = client.post(f'/api/tutor/conversations/{conv_id}/messages',
                            json={'content': 'check my material for mat207'})
        resp.get_data()

        # The static instructions always reference "SELECTED MATERIAL" by name (as a
        # cross-reference to the section that appears only when one IS selected) -- the
        # real assertion is that the heading itself (and therefore the section) doesn't
        # render, since two candidates must be listed for the student to pick, never
        # silently guessed at.
        assert '## SELECTED MATERIAL:' not in captured['system']
        assert 'MAT207 Handout A' in captured['system']
        assert 'MAT207 Past Questions' in captured['system']
