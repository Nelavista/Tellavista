"""PRD §5.2 sequential onboarding: per-step filtering, multi-select enrollment saved
as real Enrollment rows, validation against the student's own department/level (no
forged cross-faculty enrollment), waitlist capture, and hook exemptions.

The taxonomy chain comes from conftest's make_course fixture
(University -> Faculty -> Department -> Course); sessions/semesters are created here
because the product never seeds them on its own.
"""
import pytest

from app.extensions import db
from app.models import AcademicSession, Enrollment, Notification, Semester, User
from app.services import onboarding_service as svc


@pytest.fixture
def lasu_chain(app, make_course):
    """University -> Faculty -> Department -> two courses at two levels."""
    c1 = make_course(code='CSC213', level='200')
    c2 = make_course(code='CSC315', level='300')
    with app.app_context():
        from app.models import University, Faculty, Department, Course
        uni = University.query.filter_by(name='Lagos State University').first()
        dept = Department.query.join(Faculty).filter(Department.name == 'Computer Science').first()
        session_row = AcademicSession(university_id=uni.id, label='2025/2026')
        db.session.add(session_row)
        db.session.flush()
        sem = Semester(session_id=session_row.id, label='First Semester')
        db.session.add(sem)
        db.session.commit()
        return {
            'university': uni.name, 'faculty': 'Science', 'department': 'Computer Science',
            'session_id': session_row.id, 'semester_id': sem.id,
            'courses': {lvl: Course.query.filter_by(department_id=dept.id, level=lvl).all()
                        for lvl in ('200', '300')},
        }


def test_step_filtering_faculties_departments(app, lasu_chain):
    assert [f['name'] for f in svc.faculties_for(lasu_chain['university'])] == ['Science']
    # Wrong/unknown university filters to nothing (per-step filtering, not global lists).
    assert svc.faculties_for('University of Nowhere') == []
    assert [d['name'] for d in svc.departments_for(lasu_chain['university'], lasu_chain['faculty'])] == ['Computer Science']
    assert svc.departments_for(lasu_chain['university'], 'Law') == []
    # Level filtering on the final step.
    codes_200 = [c['code'] for c in svc.courses_for(lasu_chain['university'], lasu_chain['department'], '200')]
    assert codes_200 == ['CSC213']
    assert 'CSC315' in [c['code'] for c in svc.courses_for(lasu_chain['university'], lasu_chain['department'], '300')]


def test_sessions_only_those_recorded(app, lasu_chain):
    rows = svc.sessions_for(lasu_chain['university'])
    assert [s['label'] for s in rows] == ['2025/2026']
    assert rows[0]['semesters'][0]['label'] == 'First Semester'
    # Unrecorded schools get an honest empty list, not invented labels.
    assert svc.sessions_for('University of Nowhere') == []


def test_save_creates_enrollments_and_profile(app, make_user, lasu_chain):
    user = make_user('onb1', university=None, complete_profile=False)
    target_ids = [c.id for c in lasu_chain['courses']['200']]
    ok, err = svc.save_onboarding(User.query.get(user.id), {
        'university': lasu_chain['university'], 'faculty': lasu_chain['faculty'],
        'department': lasu_chain['department'], 'level': '200', 'semester': 'First Semester',
        'session_id': lasu_chain['session_id'], 'semester_id': lasu_chain['semester_id'],
        'course_ids': target_ids,
    })
    assert (ok, err) == (True, None)
    with app.app_context():
        u = User.query.get(user.id)
        rows = Enrollment.query.filter_by(user_id=u.id).all()
        assert {r.course_id for r in rows} == set(target_ids)
        assert all(r.session_id == lasu_chain['session_id'] for r in rows)
        assert all(r.semester_id == lasu_chain['semester_id'] for r in rows)
        # Legacy profile strings stay written for every existing reader.
        assert u.university == lasu_chain['university']
        assert u.level == '200'
        assert u.semester == 'First Semester'


def test_save_rejects_cross_department_course_ids(app, make_user, make_course, lasu_chain):
    make_course(code='LAW101', level='200', faculty='Law', department='Law')
    user = make_user('onb2', university=None, complete_profile=False)
    with app.app_context():
        from app.models import Course
        law_id = Course.query.filter_by(code='LAW101').first().id
    ok, _ = svc.save_onboarding(User.query.get(user.id), {
        'university': lasu_chain['university'], 'faculty': lasu_chain['faculty'],
        'department': lasu_chain['department'], 'level': '200',
        'course_ids': [law_id],   # forged: not in CS/200 scope
    })
    assert ok is True   # save proceeds with the valid (empty) subset...
    with app.app_context():
        assert Enrollment.query.filter_by(user_id=user.id).count() == 0   # ...but enrolls nothing


def test_save_is_idempotent_on_re_enrollment(app, make_user, lasu_chain):
    user = make_user('onb3', university=None, complete_profile=False)
    payload = {
        'university': lasu_chain['university'], 'faculty': lasu_chain['faculty'],
        'department': lasu_chain['department'], 'level': '200',
        'course_ids': [c.id for c in lasu_chain['courses']['200']],
    }
    svc.save_onboarding(User.query.get(user.id), payload)
    svc.save_onboarding(User.query.get(user.id), payload)
    with app.app_context():
        assert Enrollment.query.filter_by(user_id=user.id).count() == 1


def test_save_validates_session_semester_pairing(app, make_user, lasu_chain):
    user = make_user('onb4', university=None, complete_profile=False)
    ok, err = svc.save_onboarding(User.query.get(user.id), {
        'university': lasu_chain['university'], 'faculty': lasu_chain['faculty'],
        'department': lasu_chain['department'], 'level': '200',
        'session_id': lasu_chain['session_id'], 'semester_id': 999999,
    })
    assert ok is False and 'semester' in err.lower()


def test_waitlist_captures_unknown_department(app, make_user, lasu_chain):
    user = make_user('onb5')
    with app.app_context():
        result = svc.save_waitlist(
            User.query.get(user.id), lasu_chain['university'], 'Marine Sciences', level='100')
    assert result['status'] == 'waitlisted'
    assert result['department_known'] is False
    with app.app_context():
        n = Notification.query.filter_by(user_id=user.id, type='onboarding_waitlist').first()
        assert n is not None and 'Marine Sciences' in n.body


def test_waitlist_reports_existing_department(app, make_user, lasu_chain):
    user = make_user('onb6')
    with app.app_context():
        result = svc.save_waitlist(
            User.query.get(user.id), lasu_chain['university'], 'Computer Science')
    assert result == {'status': 'exists', 'university_known': True, 'department_known': True}


def test_wizard_endpoints_live(app, client, make_user, login_as, lasu_chain):
    user = make_user('onb7', university=None, complete_profile=False)
    login_as(client, user)
    assert client.get('/onboarding').status_code == 200
    assert client.get('/api/onboarding/faculties?university=Lagos%20State%20University').status_code == 200
    assert client.get('/api/onboarding/departments?university=Lagos%20State%20University&faculty=Science').status_code == 200
    assert client.get('/api/onboarding/sessions?university=Lagos%20State%20University').status_code == 200
    assert client.get('/api/onboarding/courses?university=Lagos%20State%20University&department=Computer%20Science&level=200').status_code == 200

    res = client.post('/api/onboarding/save', json={
        'university': lasu_chain['university'], 'faculty': lasu_chain['faculty'],
        'department': lasu_chain['department'], 'level': '200',
        'course_ids': [c.id for c in lasu_chain['courses']['200']],
    })
    assert res.status_code == 200 and res.get_json()['success'] is True
    with app.app_context():
        assert Enrollment.query.filter_by(user_id=user.id).count() >= 1
