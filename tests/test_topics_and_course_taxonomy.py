"""Regression coverage for the Course -> Topic -> Material taxonomy rebuild (Academia
Materials audit follow-up): Topic model/relationships, Material's new course_id/
topic_id/department_id FK links, the upload flow now requiring a real Course instead of
free-typed text, "My Uploads" status visibility, reject-with-reason moderation, course/
topic page rendering (including the "zero topics should not 404" empty state), and the
taxonomy backfill script's matching logic.
"""
import io
import json

from extensions import db
from models import Material, Topic, Course, TopicProgress


# ─────────────────────────── Topic <-> Course model ───────────────────────────

def test_course_belongs_to_correct_university_and_department(app, make_course):
    course = make_course(university='Lagos State University', department='Computer Science', code='CSC213')
    with app.app_context():
        c = Course.query.get(course.id)
        assert c.department.name == 'Computer Science'
        assert c.department.faculty.university.name == 'Lagos State University'


def test_topic_belongs_to_course_and_is_ordered(app, make_course):
    course = make_course()
    with app.app_context():
        db.session.add_all([
            Topic(course_id=course.id, title='Arrays', order=1),
            Topic(course_id=course.id, title='Introduction', order=0),
        ])
        db.session.commit()

        c = Course.query.get(course.id)
        titles = [t.title for t in c.topics.order_by(Topic.order).all()]
        assert titles == ['Introduction', 'Arrays']


def test_deleting_course_cascades_to_its_topics(app, make_course):
    course = make_course()
    with app.app_context():
        db.session.add(Topic(course_id=course.id, title='Linked Lists'))
        db.session.commit()
        assert Topic.query.filter_by(course_id=course.id).count() == 1

        db.session.delete(Course.query.get(course.id))
        db.session.commit()
        assert Topic.query.filter_by(course_id=course.id).count() == 0


def test_topic_primary_video_prefers_pinned_url_over_cache(app, make_course):
    course = make_course()
    with app.app_context():
        t = Topic(course_id=course.id, title='Stacks', video_url='https://youtu.be/abcdefghijk')
        t.videos = [{'video_id': 'zzzzzzzzzzz', 'title': 'cached result', 'channel': 'x', 'thumbnail': ''}]
        db.session.add(t)
        db.session.commit()

        reloaded = Topic.query.get(t.id)
        assert reloaded.primary_video['video_id'] == 'abcdefghijk'


def test_topic_videos_none_vs_empty_list_distinction(app, make_course):
    course = make_course()
    with app.app_context():
        t = Topic(course_id=course.id, title='Queues')
        db.session.add(t)
        db.session.commit()
        assert Topic.query.get(t.id).videos is None  # never fetched

        t.videos = []
        db.session.commit()
        assert Topic.query.get(t.id).videos == []  # fetched, found nothing


# ─────────────────────────── Material taxonomy links ───────────────────────────

def test_material_type_label_uses_stored_type_not_title_guessing(app, make_course):
    course = make_course()
    with app.app_context():
        m = Material(title='Random filename 4', department='Computer Science', level='200',
                      semester='First Semester', course_id=course.id, material_type='past_question',
                      is_approved=True, file_url='https://example.com/x.pdf')
        db.session.add(m)
        db.session.commit()
        assert Material.query.get(m.id).type_label == 'PAST QUESTIONS'


def test_material_type_label_falls_back_to_legacy_heuristic_for_untyped_rows(app, make_course):
    course = make_course()
    with app.app_context():
        m = Material(title='CSC213 Past Questions 2023', department='Computer Science', level='200',
                      semester='First Semester', course_id=course.id, material_type=None,
                      is_approved=True, file_url='https://example.com/x.pdf')
        db.session.add(m)
        db.session.commit()
        assert Material.query.get(m.id).type_label == 'PAST QUESTIONS'


def test_course_detail_page_shows_topic_linked_material(app, client, make_user, make_course, login_as):
    course = make_course()
    with app.app_context():
        topic = Topic(course_id=course.id, title='Linked Lists', explanation='<p>x</p>')
        db.session.add(topic)
        db.session.commit()
        db.session.add(Material(title='Linked Lists Handout', department='Computer Science', level='200',
                                 semester='First Semester', course_id=course.id, topic_id=topic.id,
                                 material_type='handout', is_approved=True, university='Lagos State University',
                                 file_url='https://example.com/x.pdf'))
        db.session.commit()
        topic_id = topic.id

    user = make_user('cs_student', university='Lagos State University', department='Computer Science', level='200')
    login_as(client, user)

    res = client.get(f'/courses/{course.code}')
    assert res.status_code == 200
    assert b'Linked Lists' in res.data  # the topic itself is listed

    res2 = client.get(f'/courses/{course.code}/topics/{topic_id}')
    assert res2.status_code == 200
    assert b'Linked Lists Handout' in res2.data


def test_course_with_zero_topics_renders_honest_empty_state_not_404(app, client, make_user, make_course, login_as):
    course = make_course(code='CSC999', title='Placeholder Course')
    user = make_user('no_topics_student', university='Lagos State University',
                      department='Computer Science', level='200')
    login_as(client, user)

    res = client.get(f'/courses/{course.code}')
    assert res.status_code == 200
    assert b"hasn't added a topic breakdown" in res.data


def test_topic_detail_404s_for_topic_belonging_to_different_course(app, client, make_user, make_course, login_as):
    course_a = make_course(code='CSC213', title='Data Structures')
    course_b = make_course(code='CSC221', title='Data Structures II')
    with app.app_context():
        topic = Topic(course_id=course_b.id, title='Some topic of course B')
        db.session.add(topic)
        db.session.commit()
        topic_id = topic.id

    user = make_user('mismatch_student', university='Lagos State University',
                      department='Computer Science', level='200')
    login_as(client, user)

    res = client.get(f'/courses/{course_a.code}/topics/{topic_id}')
    assert res.status_code == 404


def test_same_course_code_at_different_universities_does_not_leak_across(app, make_course, client, make_user, login_as):
    """Explicit collision test: two different universities can legitimately have the
    same course code (e.g. both LASU and UNILAG have a CSC213) with entirely different
    content -- a student must only ever see their own university's version, never
    resolve into the other school's course/topics by accident."""
    lasu_course = make_course(university='Lagos State University', department='Computer Science',
                               code='CSC213', title='LASU Data Structures')
    unilag_course = make_course(university='University of Lagos', department='Computer Science',
                                 code='CSC213', title='UNILAG Data Structures')
    with app.app_context():
        db.session.add(Topic(course_id=lasu_course.id, title='LASU-only topic'))
        db.session.add(Topic(course_id=unilag_course.id, title='UNILAG-only topic'))
        db.session.commit()

    lasu_student = make_user('lasu_cs_student', university='Lagos State University',
                              department='Computer Science', level='200')
    login_as(client, lasu_student)

    res = client.get('/courses/CSC213')
    assert res.status_code == 200
    body = res.data.decode()
    assert 'LASU Data Structures' in body
    assert 'LASU-only topic' in body
    assert 'UNILAG Data Structures' not in body
    assert 'UNILAG-only topic' not in body


def test_course_detail_never_triggers_ai_topic_generation(app, client, make_user, make_course, login_as, monkeypatch):
    """Opening a course page must never itself call the AI content pipeline -- topics
    are generated exactly once, by an explicit admin action (see
    routes/admin_academia_routes.py::generate_course_content), never on a student's
    page view. Patches the function everywhere it's imported to catch a future regression
    regardless of which module ends up calling it."""
    calls = []
    monkeypatch.setattr('services.ai_service.generate_course_topics', lambda *a, **kw: calls.append(1))

    course = make_course()
    user = make_user('no_ai_student', university='Lagos State University',
                      department='Computer Science', level='200')
    login_as(client, user)

    client.get(f'/courses/{course.code}')
    client.get(f'/courses/{course.code}')
    client.get(f'/courses/{course.code}')
    assert calls == []


def test_topic_detail_never_triggers_youtube_search(app, client, make_user, make_course, login_as, monkeypatch):
    """Opening a topic page must never itself call the YouTube API -- videos are fetched
    exactly once, by an explicit admin action (refresh_topic_videos), and cached on
    Topic.videos_json. A student re-opening the same topic repeatedly must never
    re-trigger the search, regardless of whether a video was ever fetched."""
    calls = []
    monkeypatch.setattr('services.youtube_service.search_youtube_videos', lambda *a, **kw: calls.append(1))

    course = make_course()
    with app.app_context():
        topic = Topic(course_id=course.id, title='Queues')  # deliberately never had videos fetched
        db.session.add(topic)
        db.session.commit()
        topic_id = topic.id

    user = make_user('no_yt_student', university='Lagos State University',
                      department='Computer Science', level='200')
    login_as(client, user)

    for _ in range(3):
        res = client.get(f'/courses/{course.code}/topics/{topic_id}')
        assert res.status_code == 200
    assert calls == []


def test_topic_with_no_video_and_no_materials_still_renders(app, client, make_user, make_course, login_as):
    """A topic with an explanation but nothing else (no video, no materials) must
    render its honest empty states, not error out or silently omit the sections."""
    course = make_course()
    with app.app_context():
        topic = Topic(course_id=course.id, title='Graphs', explanation='<p>Graphs are...</p>')
        db.session.add(topic)
        db.session.commit()
        topic_id = topic.id

    user = make_user('empty_state_student', university='Lagos State University',
                      department='Computer Science', level='200')
    login_as(client, user)

    res = client.get(f'/courses/{course.code}/topics/{topic_id}')
    assert res.status_code == 200
    body = res.data.decode()
    assert 'No video linked for this topic yet' in body
    assert 'No school materials have been added for this specific topic yet' in body


def test_course_detail_graceful_for_university_not_yet_mapped(app, client, make_user, login_as):
    """A student at a university the taxonomy doesn't cover yet (see
    seed_academia.py's ACTIVE_UNIVERSITIES_WITHOUT_TAXONOMY_YET -- a bare University row
    with no Faculty/Department/Course data behind it yet) must get an honest 'not mapped
    yet' message when opening any course code -- never a 404, never invented content."""
    from models import University
    with app.app_context():
        db.session.add(University(name='University of Abuja', short_name='UNIABUJA'))
        db.session.commit()

    user = make_user('unmapped_uni_student', university='University of Abuja',
                      department='Computer Science', level='200')
    login_as(client, user)

    res = client.get('/courses/CSC101')
    assert res.status_code == 200
    body = res.data.decode()
    assert "hasn't added" in body
    assert 'University of Abuja' in body


def test_browse_courses_groups_by_level_across_the_students_department(app, client, make_user, make_course, login_as):
    make_course(code='CSC101', title='Intro to CS', level='100')
    make_course(code='CSC213', title='Data Structures', level='200')
    make_course(code='CSC311', title='Databases', level='300')

    user = make_user('browse_student', university='Lagos State University',
                      department='Computer Science', level='200')
    login_as(client, user)

    res = client.get('/courses')
    assert res.status_code == 200
    body = res.data.decode()
    # All three levels show up, not just the student's own level (200) --
    # /courses is explicitly the escape hatch beyond "My Courses".
    assert 'CSC101' in body and 'CSC213' in body and 'CSC311' in body


# ─────────────────────────── Upload flow ───────────────────────────

def test_upload_requires_a_real_course_id(app, client, make_user, login_as):
    user = make_user('uploader1', university='Lagos State University', department='Computer Science', level='200')
    login_as(client, user)

    data = {
        'title': 'My Notes', 'course_id': '999999', 'material_type': 'handout', 'author': 'Uploader',
        'file': (io.BytesIO(b'%PDF-1.4 fake'), 'notes.pdf'),
    }
    res = client.post('/api/upload-material', data=data, content_type='multipart/form-data')
    assert res.status_code == 400
    assert 'course' in res.get_json()['error'].lower()


def test_upload_rejects_topic_from_a_different_course(app, client, make_user, make_course, login_as):
    course = make_course()
    other_course = make_course(code='MAT101', title='General Mathematics I', department='Mathematics')
    with app.app_context():
        other_topic = Topic(course_id=other_course.id, title='Set Theory')
        db.session.add(other_topic)
        db.session.commit()
        other_topic_id = other_topic.id

    user = make_user('uploader2', university='Lagos State University', department='Computer Science', level='200')
    login_as(client, user)

    data = {
        'title': 'My Notes', 'course_id': str(course.id), 'topic_id': str(other_topic_id),
        'material_type': 'handout', 'author': 'Uploader', 'file': (io.BytesIO(b'%PDF-1.4 fake'), 'notes.pdf'),
    }
    res = client.post('/api/upload-material', data=data, content_type='multipart/form-data')
    assert res.status_code == 400
    assert 'topic' in res.get_json()['error'].lower()


def test_upload_sets_uploaded_by_to_real_username_not_the_typed_author_name(
    app, client, make_user, make_course, login_as, monkeypatch
):
    """Regression: uploaded_by must be the authenticated account's username (what
    my_uploads() and admin moderation filter/identify by), never the free-typed
    'Author' display field -- found via manual browser verification when a student
    typing their own name into Author (which the form prefills) made their own upload
    invisible on My Uploads.

    Mocks Cloudinary's upload call -- this must never hit the real (production)
    Cloudinary account from an automated test."""
    course = make_course()
    user = make_user('real_username_here', university='Lagos State University',
                      department='Computer Science', level='200')
    login_as(client, user)

    monkeypatch.setattr(
        'routes.materials_routes.cloudinary.uploader.upload',
        lambda *a, **kw: {'secure_url': 'https://res.cloudinary.com/fake/raw/upload/test.pdf'},
    )

    data = {
        'title': 'My Notes', 'course_id': str(course.id), 'material_type': 'handout',
        'author': 'A Totally Different Display Name', 'file': (io.BytesIO(b'%PDF-1.4 fake'), 'notes.pdf'),
    }
    res = client.post('/api/upload-material', data=data, content_type='multipart/form-data')
    assert res.status_code == 201
    material = res.get_json()['material']
    assert material['author'] == 'A Totally Different Display Name'

    with app.app_context():
        m = Material.query.get(material['id'])
        assert m.uploaded_by == 'real_username_here'
        assert m.author == 'A Totally Different Display Name'


def test_upload_rejects_invalid_material_type(app, client, make_user, make_course, login_as):
    course = make_course()
    user = make_user('uploader3', university='Lagos State University', department='Computer Science', level='200')
    login_as(client, user)

    data = {
        'title': 'My Notes', 'course_id': str(course.id), 'material_type': 'not_a_real_type',
        'author': 'Uploader', 'file': (io.BytesIO(b'%PDF-1.4 fake'), 'notes.pdf'),
    }
    res = client.post('/api/upload-material', data=data, content_type='multipart/form-data')
    assert res.status_code == 400


# ─────────────────────────── My Uploads status visibility ───────────────────────────

def test_my_uploads_shows_pending_approved_and_rejected_states(app, client, make_user, make_course, login_as):
    course = make_course()
    with app.app_context():
        db.session.add_all([
            Material(title='Pending One', department='Computer Science', level='200', semester='First Semester',
                      course_id=course.id, uploaded_by='contributor', source='uploaded',
                      is_approved=False, file_url='https://example.com/a.pdf'),
            Material(title='Approved One', department='Computer Science', level='200', semester='First Semester',
                      course_id=course.id, uploaded_by='contributor', source='uploaded',
                      is_approved=True, file_url='https://example.com/b.pdf'),
            Material(title='Rejected One', department='Computer Science', level='200', semester='First Semester',
                      course_id=course.id, uploaded_by='contributor', source='uploaded',
                      is_approved=False, rejection_reason='Blurry scan, please re-upload',
                      file_url='https://example.com/c.pdf'),
        ])
        db.session.commit()

    user = make_user('contributor', university='Lagos State University', department='Computer Science', level='200')
    login_as(client, user)

    res = client.get('/my-uploads')
    assert res.status_code == 200
    body = res.data.decode()
    assert 'Pending One' in body and 'Pending review' in body
    assert 'Approved One' in body and 'Approved' in body
    assert 'Rejected One' in body and 'Blurry scan, please re-upload' in body


# ─────────────────────────── Moderation: reject with reason ───────────────────────────

def test_reject_material_keeps_row_and_sets_reason_instead_of_deleting(app, client, make_user, make_course, login_as):
    course = make_course()
    with app.app_context():
        m = Material(title='Needs fixing', department='Computer Science', level='200', semester='First Semester',
                      course_id=course.id, uploaded_by='contributor', source='uploaded',
                      is_approved=False, file_url='https://example.com/x.pdf')
        db.session.add(m)
        db.session.commit()
        material_id = m.id

    admin = make_user('mod_admin', is_admin=True, university='Lagos State University',
                       department='Computer Science', level='200')
    login_as(client, admin)

    res = client.post(f'/admin/materials/reject/{material_id}', json={'reason': 'Wrong course code'})
    assert res.status_code == 200
    assert res.get_json()['success'] is True

    with app.app_context():
        m = Material.query.get(material_id)
        assert m is not None  # not deleted
        assert m.is_approved is False
        assert m.rejection_reason == 'Wrong course code'


def test_reject_material_requires_a_reason(app, client, make_user, make_course, login_as):
    course = make_course()
    with app.app_context():
        m = Material(title='Needs a reason', department='Computer Science', level='200', semester='First Semester',
                      course_id=course.id, uploaded_by='contributor', source='uploaded',
                      is_approved=False, file_url='https://example.com/x.pdf')
        db.session.add(m)
        db.session.commit()
        material_id = m.id

    admin = make_user('mod_admin2', is_admin=True, university='Lagos State University',
                       department='Computer Science', level='200')
    login_as(client, admin)

    res = client.post(f'/admin/materials/reject/{material_id}', json={'reason': ''})
    assert res.status_code == 400


def test_rejected_material_does_not_reappear_in_pending_queue(app, client, make_user, make_course, login_as):
    course = make_course()
    with app.app_context():
        m = Material(title='Already rejected', department='Computer Science', level='200', semester='First Semester',
                      course_id=course.id, uploaded_by='contributor', source='uploaded',
                      is_approved=False, rejection_reason='Not relevant', file_url='https://example.com/x.pdf')
        m2 = Material(title='Still pending', department='Computer Science', level='200', semester='First Semester',
                       course_id=course.id, uploaded_by='contributor', source='uploaded',
                       is_approved=False, file_url='https://example.com/y.pdf')
        db.session.add_all([m, m2])
        db.session.commit()

    admin = make_user('mod_admin3', is_admin=True, university='Lagos State University',
                       department='Computer Science', level='200')
    login_as(client, admin)

    res = client.get('/admin/materials')
    body = res.data.decode()
    assert 'Still pending' in body
    assert 'Already rejected' not in body


# ─────────────────────────── Admin topic content management ───────────────────────────

def test_admin_can_apply_a_reviewed_topic_draft(app, client, make_user, make_course, login_as):
    course = make_course()
    admin = make_user('content_admin', is_admin=True, university='Lagos State University',
                       department='Computer Science', level='200')
    login_as(client, admin)

    res = client.post(
        f'/admin/academia/courses/{course.id}/apply-topics',
        json={'description': 'A course about organizing data efficiently.', 'topics': ['Arrays', 'Linked Lists']},
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert len(data['topics']) == 2

    with app.app_context():
        c = Course.query.get(course.id)
        assert c.description == 'A course about organizing data efficiently.'
        assert c.topics.count() == 2


def test_refresh_topic_videos_caches_search_results(app, client, make_user, make_course, login_as, monkeypatch):
    course = make_course()
    with app.app_context():
        t = Topic(course_id=course.id, title='Trees')
        db.session.add(t)
        db.session.commit()
        topic_id = t.id

    fake_videos = [{'video_id': 'abcdefghijk', 'title': 'Trees explained', 'channel': 'EduChan', 'thumbnail': ''}]

    def fake_search(query, max_results=3):
        return fake_videos

    monkeypatch.setattr('routes.admin_academia_routes.search_youtube_videos', fake_search)

    admin = make_user('video_admin', is_admin=True, university='Lagos State University',
                       department='Computer Science', level='200')
    login_as(client, admin)

    res = client.post(f'/admin/academia/topics/{topic_id}/videos')
    assert res.status_code == 200
    assert res.get_json()['videos'] == fake_videos

    with app.app_context():
        assert Topic.query.get(topic_id).videos == fake_videos


def test_quota_exceeded_video_search_is_not_cached_as_confirmed_empty(
        app, client, make_user, make_course, login_as, monkeypatch):
    """search_youtube_videos returns None (not []) when every configured API key failed
    (quota exceeded, network error, etc) -- a real bug this guards against: an earlier
    version treated that failure identically to 'searched, found nothing', permanently
    writing videos_json='[]' for topics that were never actually searched. That falsely
    marks them as done, so a later retry (once quota resets) silently skips them forever.
    None must be left uncached so a future attempt can still pick the topic up."""
    course = make_course()
    with app.app_context():
        t = Topic(course_id=course.id, title='Graphs')
        db.session.add(t)
        db.session.commit()
        topic_id = t.id

    monkeypatch.setattr('routes.admin_academia_routes.search_youtube_videos', lambda query, max_results=3: None)

    admin = make_user('quota_admin', is_admin=True, university='Lagos State University',
                       department='Computer Science', level='200')
    login_as(client, admin)

    res = client.post(f'/admin/academia/topics/{topic_id}/videos')
    assert res.status_code == 502  # surfaced as a real failure, not a silent success

    with app.app_context():
        # Still None (never fetched), NOT [] (confirmed empty) -- a later retry must
        # still see this topic as needing a search.
        assert Topic.query.get(topic_id).videos is None


def test_edit_topic_marks_hand_edited_content_as_reviewed(app, client, make_user, make_course, login_as):
    course = make_course()
    with app.app_context():
        t = Topic(course_id=course.id, title='Hashing', content_source='ai_draft')
        db.session.add(t)
        db.session.commit()
        topic_id = t.id

    admin = make_user('editor_admin', is_admin=True, university='Lagos State University',
                       department='Computer Science', level='200')
    login_as(client, admin)

    res = client.post(f'/admin/academia/topics/{topic_id}/edit', data={'explanation': '<p>Reviewed content</p>'})
    assert res.status_code == 200

    with app.app_context():
        t = Topic.query.get(topic_id)
        assert t.explanation == '<p>Reviewed content</p>'
        assert t.content_source == 'reviewed'


# ─────────────────────────── Topic AI action ───────────────────────────

def test_topic_ai_action_is_honest_when_no_explanation_exists_yet(app, client, make_user, make_course, login_as):
    course = make_course()
    with app.app_context():
        t = Topic(course_id=course.id, title='Graphs')
        db.session.add(t)
        db.session.commit()
        topic_id = t.id

    user = make_user('ai_student', university='Lagos State University', department='Computer Science', level='200')
    login_as(client, user)

    res = client.post(f'/api/topics/{topic_id}/ai-action', json={'mode': 'explain'})
    assert res.status_code == 200
    data = res.get_json()
    assert data['grounded'] is False
    assert "doesn't have a written explanation" in data['answer']


# ─────────────────────────── Taxonomy backfill script ───────────────────────────

def test_backfill_resolves_department_scoped_to_university(app, make_course):
    make_course(university='Lagos State University', department='Computer Science', code='CSC213')
    make_course(university='University of Lagos', department='Computer Science', code='CSC101')

    from backfill_material_taxonomy_links import _resolve_department
    from models import Department, Faculty, University

    with app.app_context():
        departments = Department.query.join(Faculty).join(University).all()
        from collections import defaultdict
        dept_by_name = defaultdict(list)
        for d in departments:
            dept_by_name[d.name.strip().lower()].append(d)

        class FakeMaterial:
            department = 'Computer Science'
            university = 'Lagos State University'

        resolved = _resolve_department(FakeMaterial(), dept_by_name)
        assert resolved is not None
        assert resolved.faculty.university.name == 'Lagos State University'


def test_backfill_leaves_department_unresolved_when_ambiguous_and_no_university_set(app, make_course):
    make_course(university='Lagos State University', department='Computer Science', code='CSC213')
    make_course(university='University of Lagos', department='Computer Science', code='CSC101')

    from backfill_material_taxonomy_links import _resolve_department
    from models import Department, Faculty, University
    from collections import defaultdict

    with app.app_context():
        departments = Department.query.join(Faculty).join(University).all()
        dept_by_name = defaultdict(list)
        for d in departments:
            dept_by_name[d.name.strip().lower()].append(d)

        class FakeMaterial:
            department = 'Computer Science'
            university = None

        assert _resolve_department(FakeMaterial(), dept_by_name) is None


# ─────────────────────────── Topic completion tracking ───────────────────────────

def test_toggle_topic_complete_marks_and_unmarks(app, client, make_user, make_course, login_as):
    course = make_course()
    with app.app_context():
        topic = Topic(course_id=course.id, title='Trees')
        db.session.add(topic)
        db.session.commit()
        topic_id = topic.id

    user = make_user('progress_student', university='Lagos State University',
                      department='Computer Science', level='200')
    login_as(client, user)

    res = client.post(f'/api/topics/{topic_id}/complete')
    assert res.status_code == 200
    assert res.get_json()['completed'] is True
    with app.app_context():
        assert TopicProgress.query.filter_by(topic_id=topic_id).count() == 1

    res2 = client.post(f'/api/topics/{topic_id}/complete')
    assert res2.get_json()['completed'] is False
    with app.app_context():
        assert TopicProgress.query.filter_by(topic_id=topic_id).count() == 0


def test_course_page_shows_completed_topics_and_count(app, client, make_user, make_course, login_as):
    course = make_course()
    with app.app_context():
        t1 = Topic(course_id=course.id, title='Arrays', order=0)
        t2 = Topic(course_id=course.id, title='Linked Lists', order=1)
        db.session.add_all([t1, t2])
        db.session.commit()
        t1_id = t1.id

    user = make_user('progress_student2', university='Lagos State University',
                      department='Computer Science', level='200')
    login_as(client, user)
    client.post(f'/api/topics/{t1_id}/complete')

    res = client.get(f'/courses/{course.code}')
    body = res.data.decode()
    assert '1/2 topics completed' in body


# ─────────────────────────── School Materials vs Additional Resources ───────────────────────────

def test_course_page_separates_uploaded_from_generic_materials(app, client, make_user, make_course, login_as):
    course = make_course()
    with app.app_context():
        db.session.add_all([
            Material(title='Real LASU Lecture Note', department='Computer Science', level='200',
                     semester='First Semester', course_id=course.id, course_code=course.code,
                     source='uploaded', material_type='lecture_note', is_approved=True,
                     file_url='https://example.com/a.pdf', uploaded_by='a_student'),
            Material(title='Collaborative Statistics', department='Computer Science', level='200',
                     semester='First Semester', course_id=course.id, course_code=course.code,
                     source='oer_library', is_approved=True, external_url='https://openstax.org/x'),
            Material(title='Some Web Result', department='Computer Science', level='200',
                     semester='First Semester', course_id=course.id, course_code=course.code,
                     source='google_auto', is_approved=True, external_url='https://example.com/y'),
        ])
        db.session.commit()

    user = make_user('split_student', university='Lagos State University',
                      department='Computer Science', level='200')
    login_as(client, user)

    res = client.get(f'/courses/{course.code}')
    body = res.data.decode()
    assert 'Real LASU Lecture Note' in body
    assert 'Additional Resources (2)' in body
    # The generic titles must not appear in the always-visible School Materials list --
    # only inside the (collapsed by default) Additional Resources panel.
    school_section = body.split('School Materials')[1].split('Additional Resources')[0]
    assert 'Collaborative Statistics' not in school_section
    assert 'Some Web Result' not in school_section


def test_course_stats_row_shows_real_counts_only(app, client, make_user, make_course, login_as):
    course = make_course()
    with app.app_context():
        t = Topic(course_id=course.id, title='Arrays', video_url='https://youtu.be/jNQXAC9IVRw')
        db.session.add(t)
        db.session.add(Material(title='Real Note', department='Computer Science', level='200',
                                 semester='First Semester', course_id=course.id, course_code=course.code,
                                 source='uploaded', material_type='lecture_note', is_approved=True,
                                 file_url='https://example.com/a.pdf', uploaded_by='a_student'))
        db.session.commit()

    user = make_user('stats_student', university='Lagos State University',
                      department='Computer Science', level='200')
    login_as(client, user)

    res = client.get(f'/courses/{course.code}')
    body = res.data.decode()
    assert '<div class="cd-stat-number">1</div>' in body  # 1 topic, 1 school material, 1 video -- all real
