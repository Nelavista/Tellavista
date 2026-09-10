"""Regression tests for utils/validation.py's safe_external_url() and its use on
StudentProject.repo_url/live_url (routes/skills_routes.py's update_project).

Before this existed, repo_url/live_url were saved with only a .strip(), unlike
external_links (which already ran a scheme check) -- both fields render as a raw
<a href> on the project's own page AND the student's PUBLIC Talent Profile, so a
javascript:/data: URI here was stored XSS against any visitor who clicked it.
"""
from app.extensions import db
from app.models import Skill, SkillCategory, ProjectTemplate, StudentProject
from app.utils.validation import safe_external_url


def test_safe_external_url_rejects_dangerous_schemes():
    assert safe_external_url('javascript:alert(document.cookie)') is None
    assert safe_external_url('data:text/html,<script>alert(1)</script>') is None
    assert safe_external_url('vbscript:msgbox(1)') is None


def test_safe_external_url_accepts_http_and_https():
    assert safe_external_url('https://github.com/me/repo') == 'https://github.com/me/repo'
    assert safe_external_url('http://example.com') == 'http://example.com'


def test_safe_external_url_rejects_schemeless_and_empty():
    assert safe_external_url('') is None
    assert safe_external_url(None) is None
    assert safe_external_url('not-a-url-at-all') is None


def test_safe_external_url_truncates_to_max_length():
    long_url = 'https://example.com/' + ('a' * 600)
    result = safe_external_url(long_url, max_length=500)
    assert len(result) <= 500


def _make_student_project(student_id):
    category = SkillCategory(name='UrlCat', slug='url-cat', order=0)
    db.session.add(category)
    db.session.commit()
    skill = Skill(category_id=category.id, name='Url Skill', slug='url-skill', is_published=True)
    db.session.add(skill)
    db.session.commit()
    template = ProjectTemplate(skill_id=skill.id, title='Url Template', slug='url-template', is_published=True)
    db.session.add(template)
    db.session.commit()
    project = StudentProject(student_id=student_id, title='My Project', source='custom')
    db.session.add(project)
    db.session.commit()
    return project.id


def test_update_project_rejects_javascript_uri_in_repo_url(app, client, make_user, login_as):
    student = make_user('url_xss_student')
    with app.app_context():
        project_id = _make_student_project(student.id)
    login_as(client, student)

    res = client.post(f'/skills/projects/{project_id}/update',
                       json={'repo_url': 'javascript:alert(document.cookie)'})
    assert res.status_code == 200

    with app.app_context():
        project = StudentProject.query.get(project_id)
        assert project.repo_url is None  # dropped silently, never stored


def test_update_project_accepts_valid_https_repo_and_live_url(app, client, make_user, login_as):
    student = make_user('url_valid_student')
    with app.app_context():
        project_id = _make_student_project(student.id)
    login_as(client, student)

    res = client.post(f'/skills/projects/{project_id}/update',
                       json={'repo_url': 'https://github.com/me/repo', 'live_url': 'https://myapp.example.com'})
    assert res.status_code == 200

    with app.app_context():
        project = StudentProject.query.get(project_id)
        assert project.repo_url == 'https://github.com/me/repo'
        assert project.live_url == 'https://myapp.example.com'


def test_update_project_external_links_still_rejects_bad_scheme(app, client, make_user, login_as):
    student = make_user('url_extlinks_student')
    with app.app_context():
        project_id = _make_student_project(student.id)
    login_as(client, student)

    res = client.post(f'/skills/projects/{project_id}/update', json={
        'external_links': [
            {'label': 'Bad', 'url': 'javascript:alert(1)'},
            {'label': 'Good', 'url': 'https://figma.com/file/x'},
        ]
    })
    assert res.status_code == 200

    with app.app_context():
        project = StudentProject.query.get(project_id)
        links = project.external_links
        assert len(links) == 1
        assert links[0]['url'] == 'https://figma.com/file/x'


def test_edit_profile_rejects_javascript_uri_in_portfolio_url(app, client, make_user, login_as):
    student = make_user('url_profile_student')
    login_as(client, student)

    res = client.post('/skills/profile', data={
        'bio': 'hi', 'portfolio_url': 'javascript:alert(1)', 'profile_photo_url': '',
    }, follow_redirects=False)
    assert res.status_code in (302, 303)

    with app.app_context():
        from app.models import User
        user = User.query.get(student.id)
        assert user.portfolio_url is None
