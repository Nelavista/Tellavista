"""Regression tests for P0-2 of the stabilization pass: material_ai_action() and
topic_ai_action() (routes/ai_routes.py) fetched their row by id and answered from its
real content with no check that it belonged to the requesting student's own
university/department -- unlike every other Material/Topic read path in the app
(materials_routes.py's fetch_materials(), academia_routes.py's topic_detail()), which
enforce that boundary. A student could pull another university's/department's content
through the AI action just by knowing or guessing an id.
"""
from extensions import db
from models import Material, Topic


def test_material_ai_action_blocks_other_university(app, client, make_user, login_as):
    with app.app_context():
        m = Material(title='LASU Past Question', department='Computer Science', level='100',
                      semester='First Semester', university='Test University A', is_approved=True)
        db.session.add(m)
        db.session.commit()
        material_id = m.id

    student = make_user('other_uni_student', university='Test University B', department='Computer Science', level='100')
    login_as(client, student)

    res = client.post(f'/api/materials/{material_id}/ai-action', json={'mode': 'explain'})
    assert res.status_code == 404


def test_material_ai_action_allows_universal_material(app, client, make_user, login_as):
    """university=NULL is the app's own convention for 'shown to everyone' -- must stay
    reachable regardless of the requester's university."""
    with app.app_context():
        m = Material(title='Universal Note', department='Computer Science', level='100',
                      semester='First Semester', university=None, is_approved=True)
        db.session.add(m)
        db.session.commit()
        material_id = m.id

    student = make_user('any_uni_student', university='Test University B', department='Computer Science', level='100')
    login_as(client, student)

    res = client.post(f'/api/materials/{material_id}/ai-action', json={'mode': 'explain'})
    assert res.status_code == 200
    assert res.get_json()['success'] is True


def test_topic_ai_action_blocks_other_department(app, client, make_user, make_course, login_as):
    course_a = make_course(university='Test University A', faculty='Science',
                            department='Computer Science A', code='CSC101', level='100')
    with app.app_context():
        topic = Topic(course_id=course_a.id, title='Intro', explanation='<p>hello</p>', is_active=True)
        db.session.add(topic)
        db.session.commit()
        topic_id = topic.id

    student = make_user('other_dept_student', university='Test University B',
                         department='Unrelated Department', level='100')
    login_as(client, student)

    res = client.post(f'/api/topics/{topic_id}/ai-action', json={'mode': 'explain'})
    assert res.status_code == 404


def test_topic_ai_action_allows_own_department(app, client, make_user, make_course, login_as):
    course_a = make_course(university='Test University C', faculty='Science',
                            department='Computer Science C', code='CSC101', level='100')
    with app.app_context():
        # No explanation set -- the route's own "nothing written yet" branch returns
        # before ever calling OpenRouter, same trick test_material_ai_action_allows_
        # universal_material() uses above, so this stays a fast, network-free unit test
        # while still proving the scoping check (which runs first) let the request through.
        topic = Topic(course_id=course_a.id, title='Intro', explanation=None, is_active=True)
        db.session.add(topic)
        db.session.commit()
        topic_id = topic.id

    student = make_user('own_dept_student', university='Test University C',
                         department='Computer Science C', level='100')
    login_as(client, student)

    res = client.post(f'/api/topics/{topic_id}/ai-action', json={'mode': 'explain'})
    assert res.status_code == 200
    assert res.get_json()['success'] is True
