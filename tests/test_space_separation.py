"""Academia, Skills, Opportunities and Campus are four separate spaces.

They were separated in the Choose Your Path picker but their content still leaked:
Skills' dashboard showed matched opportunities and earnings, Opportunities rendered
with the Skills sidebar, and Campus Map sat in Academia's sidebar. These tests pin the
content boundary so a page from one space cannot quietly reappear inside another.
"""
from app.extensions import db
from app.models import (
    SkillCategory, Skill, StudentOnboarding, Opportunity,
)


def _start_skills(app, user_id):
    """A student who has finished Skills onboarding, so /skills renders instead of
    redirecting to /skills/onboarding."""
    with app.app_context():
        db.session.add(StudentOnboarding(
            student_id=user_id, interest_text='Web Development', experience_level='new',
        ))
        db.session.commit()


def _make_opportunity(app, title='Space gig'):
    with app.app_context():
        cat = SkillCategory.query.filter_by(slug='space-cat').first()
        if not cat:
            cat = SkillCategory(name='Tech', slug='space-cat')
            db.session.add(cat)
            db.session.flush()
        skill = Skill(category_id=cat.id, name='Space Skill', slug='space-skill', is_published=True)
        db.session.add(skill)
        db.session.flush()
        opp = Opportunity(skill_id=skill.id, title=title, is_published=True)
        db.session.add(opp)
        db.session.commit()
        return opp.id


def test_skills_dashboard_has_no_earning_surface(app, client, login_as, make_user):
    user = make_user('space_skills')
    _start_skills(app, user.id)
    _make_opportunity(app)

    login_as(client, user)
    res = client.get('/skills')
    assert res.status_code == 200
    body = res.get_data(as_text=True)

    assert 'Opportunities matching your skills' not in body
    assert 'Your earnings' not in body
    assert '/skills/opportunities' not in body
    assert '/skills/gigs' not in body
    assert '/skills/earnings' not in body


def test_opportunities_page_uses_its_own_shell(app, client, login_as, make_user):
    user = make_user('space_opps')
    _make_opportunity(app, title='Space-only gig')

    login_as(client, user)
    res = client.get('/opportunities')
    assert res.status_code == 200
    body = res.get_data(as_text=True)

    assert 'Space-only gig' in body
    assert '/opportunities/gigs' in body
    # Nothing from the Skills IA (Learn / My Learning / Projects / Talent) or Academia.
    assert '/skills/catalog' not in body
    assert '/skills/my-learning' not in body
    assert '/skills/projects' not in body
    assert '/skills/talent' not in body
    assert '/dashboard' not in body


def test_academia_sidebar_does_not_host_campus(app, client, login_as, make_user):
    user = make_user('space_academia')
    login_as(client, user)

    res = client.get('/dashboard')
    assert res.status_code == 200
    assert '/campus-map' not in res.get_data(as_text=True)


def test_campus_is_reachable_as_its_own_space(app, client, login_as, make_user):
    user = make_user('space_campus')
    login_as(client, user)

    res = client.get('/campus-map')
    assert res.status_code == 200
    body = res.get_data(as_text=True)
    assert 'Switch space' in body
    # Campus does not render another space's navigation.
    assert '/skills/catalog' not in body
    assert '/dashboard' not in body


def test_legacy_skills_earning_urls_redirect_to_the_opportunities_space(app, client, login_as, make_user):
    user = make_user('space_legacy')
    opp_id = _make_opportunity(app)
    login_as(client, user)

    for old, new in (
        ('/skills/opportunities', '/opportunities'),
        ('/skills/gigs', '/opportunities/gigs'),
        ('/skills/earnings', '/opportunities/earnings'),
    ):
        res = client.get(old)
        assert res.status_code == 301
        assert res.headers['Location'] == new

    # Applying is a POST; the redirect must keep the method (308) so no application is lost.
    res = client.post(f'/skills/opportunities/{opp_id}/apply')
    assert res.status_code == 308
    assert res.headers['Location'] == f'/opportunities/{opp_id}/apply'
