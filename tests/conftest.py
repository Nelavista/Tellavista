"""Shared pytest fixtures for the Level 1 production-readiness test suite.

IMPORTANT: this deliberately does NOT `import app` (the real app.py module). app.py runs
`init_database(app)` at import time against whatever DATABASE_URL happens to be
configured in the local .env -- which, in this environment, is a real Postgres instance,
not a disposable local one. Importing app.py from a test would attempt a real network
connection to that database and (via db.create_all()) could create tables/columns
against it. Instead, every fixture here builds its own throwaway Flask app bound to a
temporary SQLite file, registers only the blueprints a given test needs, and calls
db.create_all() directly -- never touching the real configured database at all.
"""
import os
import sys
import tempfile
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('SECRET_KEY', 'test-secret-key-for-pytest-only')
os.environ.setdefault('FLASK_DEBUG', 'True')

from flask import Flask
from extensions import db, csrf, limiter, mail
import models  # noqa: F401 -- registers all models onto db.metadata


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)

    flask_app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
                       static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'))
    flask_app.config.update(
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{db_path}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY='test-secret-key-for-pytest-only',
        TESTING=True,
        WTF_CSRF_ENABLED=False,  # tests exercise route/business logic, not the CSRF layer itself
        MAIL_SUPPRESS_SEND=True,
    )

    db.init_app(flask_app)
    csrf.init_app(flask_app)
    limiter.init_app(flask_app)
    mail.init_app(flask_app)

    # Only import blueprints inside the fixture, after config is set, so a route module's
    # top-level imports (which may pull in config.py) see the test config.
    from routes.auth_routes import auth_bp
    from routes.cbt_routes import cbt_bp
    from routes.skills_routes import skills_bp
    from routes.materials_routes import materials_bp
    from routes.live_meeting_routes import live_bp
    from routes.dashboard_routes import dashboard_bp
    from routes.admin_skills_routes import admin_skills_bp
    from routes.admin_routes import admin_bp
    from routes.academia_routes import academia_bp
    from routes.admin_academia_routes import admin_academia_bp
    from routes.ai_routes import ai_bp
    from routes.tutor_routes import tutor_bp

    for bp in (auth_bp, cbt_bp, skills_bp, materials_bp, live_bp, dashboard_bp, admin_skills_bp, admin_bp,
               academia_bp, admin_academia_bp, ai_bp, tutor_bp):
        flask_app.register_blueprint(bp, url_prefix='/')

    with flask_app.app_context():
        db.create_all()

    yield flask_app

    with flask_app.app_context():
        db.session.remove()
        db.drop_all()
        db.engine.dispose()  # release SQLite's file handle -- otherwise os.remove()
        # below intermittently fails with PermissionError on Windows (file still "in
        # use" from the connection pool's point of view even after drop_all()).
    try:
        os.remove(db_path)
    except OSError:
        pass  # best-effort cleanup; a leftover temp file never affects test correctness


@pytest.fixture
def client(app):
    return app.test_client()


def _login_as(client, user):
    """Populate the test client's session exactly like routes/auth_routes.py's login()
    does, without going through the real /login route (keeps tests focused on the
    behavior under test, not re-proving login works every time)."""
    with client.session_transaction() as sess:
        sess['user'] = {
            'username': user.username,
            'email': user.email,
            'joined_on': '2026-01-01',
            'last_login': '2026-01-01 00:00:00',
            'is_admin': user.is_admin,
            'preferred_path': user.preferred_path,
        }


@pytest.fixture
def login_as():
    return _login_as


class _UserRef:
    """A plain snapshot of a created user's fields -- deliberately NOT the live ORM
    instance, which would be detached the moment its creating app-context block exits.
    Tests that need the live row back should re-query User.query.get(ref.id) inside
    their own `with app.app_context()` block."""
    def __init__(self, u):
        self.id = u.id
        self.username = u.username
        self.email = u.email
        self.is_admin = u.is_admin
        self.department = u.department
        self.level = u.level
        self.university = u.university
        self.preferred_path = u.preferred_path


class _CourseRef:
    """Same plain-snapshot convention as _UserRef -- avoids handing back a detached ORM
    instance once the creating app-context block exits."""
    def __init__(self, c):
        self.id = c.id
        self.code = c.code
        self.title = c.title
        self.level = c.level
        self.department_id = c.department_id


@pytest.fixture
def make_course(app):
    """Builds a full University -> Faculty -> Department -> Course chain in one call --
    every taxonomy-linked Material/Topic test needs this same setup, so it lives here
    rather than being copy-pasted per test file."""
    from models import University, Faculty, Department, Course

    def _make(university='Lagos State University', faculty='Science', department='Computer Science',
              code='CSC213', title='Data Structures & Algorithm Analysis', level='200'):
        with app.app_context():
            uni = University.query.filter_by(name=university).first()
            if not uni:
                uni = University(name=university)
                db.session.add(uni)
                db.session.flush()
            fac = Faculty.query.filter_by(university_id=uni.id, name=faculty).first()
            if not fac:
                fac = Faculty(university_id=uni.id, name=faculty)
                db.session.add(fac)
                db.session.flush()
            dept = Department.query.filter_by(faculty_id=fac.id, name=department).first()
            if not dept:
                dept = Department(faculty_id=fac.id, name=department)
                db.session.add(dept)
                db.session.flush()
            course = Course.query.filter_by(department_id=dept.id, code=code, level=level).first()
            if not course:
                course = Course(department_id=dept.id, code=code, title=title, level=level)
                db.session.add(course)
                db.session.commit()
            return _CourseRef(course)
    return _make


@pytest.fixture
def make_user(app):
    from models import User

    def _make(username='student1', email=None, is_admin=False, department='Computer Science', level='200',
              university=None, complete_profile=True):
        with app.app_context():
            u = User(
                username=username, email=email or f'{username}@example.com',
                is_admin=is_admin, department=department, level=level, university=university,
            )
            if complete_profile:
                # A real, complete Academia profile by default -- routes/materials_routes.py's
                # site-wide before_app_request hook (enforce_profile_completion) HTML-redirects
                # any non-exempt route for an incomplete profile, which would otherwise silently
                # break JSON-endpoint tests with a non-JSON response. Pass complete_profile=False
                # to deliberately test that incomplete-profile behavior itself.
                u.name = username.title()
                u.university = university or 'Lagos State University'
                u.faculty = 'Science'
                u.semester = 'First Semester'
            u.set_password('TestPass123!')
            db.session.add(u)
            db.session.commit()
            return _UserRef(u)
    return _make
