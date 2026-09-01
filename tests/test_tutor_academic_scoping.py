"""Regression tests for the AI Tutor cross-university/department content leak: routes/
tutor_routes.py's _resolve_context_from_args() resolved a topic_id/material_id straight
off the query string with no check that it belonged to the requesting student's own
university/department -- unlike course_code resolution in the same function (already
scoped via find_course(ctx.department, ...)), and unlike every other Material/Topic read
path in the app (materials_routes.py's fetch_materials(), academia_routes.py's
topic_detail(), and the sibling fix already applied to ai_routes.py's material_ai_action()/
topic_ai_action() -- see tests/test_academic_scoping_ai_actions.py).

This mattered more than a metadata leak: send_message() injects the resolved material's
actual extracted text into the tutor's system prompt, so an unscoped material_id was a
real cross-university content leak, not just a title/id disclosure.
"""
from extensions import db
from models import Material, Topic


def test_create_conversation_blocks_other_university_material(app, client, make_user, login_as):
    with app.app_context():
        m = Material(title='LASU Past Question', department='Computer Science', level='100',
                      semester='First Semester', university='Test University A', is_approved=True)
        db.session.add(m)
        db.session.commit()
        material_id = m.id

    student = make_user('tutor_other_uni_student', university='Test University B', department='Computer Science', level='100')
    login_as(client, student)

    res = client.post(f'/api/tutor/conversations?material={material_id}')
    assert res.status_code == 200
    assert res.get_json()['conversation']['material_id'] is None


def test_create_conversation_allows_universal_material(app, client, make_user, login_as):
    """university=NULL is the app's own convention for 'shown to everyone' -- must stay
    reachable regardless of the requester's university."""
    with app.app_context():
        m = Material(title='Universal Note', department='Computer Science', level='100',
                      semester='First Semester', university=None, is_approved=True)
        db.session.add(m)
        db.session.commit()
        material_id = m.id

    student = make_user('tutor_any_uni_student', university='Test University B', department='Computer Science', level='100')
    login_as(client, student)

    res = client.post(f'/api/tutor/conversations?material={material_id}')
    assert res.status_code == 200
    assert res.get_json()['conversation']['material_id'] == material_id


def test_create_conversation_blocks_other_department_topic(app, client, make_user, make_course, login_as):
    course_a = make_course(university='Test University A', faculty='Science',
                            department='Tutor Dept A', code='CSC101', level='100')
    with app.app_context():
        topic = Topic(course_id=course_a.id, title='Intro', explanation='<p>hello</p>', is_active=True)
        db.session.add(topic)
        db.session.commit()
        topic_id = topic.id

    student = make_user('tutor_other_dept_student', university='Test University B',
                         department='Unrelated Department', level='100')
    login_as(client, student)

    res = client.post(f'/api/tutor/conversations?topic={topic_id}')
    assert res.status_code == 200
    assert res.get_json()['conversation']['topic_id'] is None


def test_create_conversation_allows_own_department_topic(app, client, make_user, make_course, login_as):
    course_c = make_course(university='Test University C', faculty='Science',
                            department='Tutor Dept C', code='CSC101', level='100')
    with app.app_context():
        topic = Topic(course_id=course_c.id, title='Intro', explanation='<p>hello</p>', is_active=True)
        db.session.add(topic)
        db.session.commit()
        topic_id = topic.id

    student = make_user('tutor_own_dept_student', university='Test University C',
                         department='Tutor Dept C', level='100')
    login_as(client, student)

    res = client.post(f'/api/tutor/conversations?topic={topic_id}')
    assert res.status_code == 200
    assert res.get_json()['conversation']['topic_id'] == topic_id
