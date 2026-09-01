"""Regression tests for the P2 performance fix: opportunities()/gigs() (routes/
skills_routes.py) called opportunity_match_pct() -- itself a StudentSkill query -- once
per opportunity on the page, even though both routes already fetched every one of the
student's StudentSkill rows a line earlier just to check skill-id membership. earnings()
accessed a.opportunity per application, a separate lazy-loaded query each time with no
eager-load. All three now do one query for the data they need regardless of row count.
"""
from extensions import db
from models import SkillCategory, Skill, StudentSkill, Opportunity, OpportunityApplication


def _make_skill_with_progress(user_id, progress_pct, slug):
    cat = SkillCategory.query.filter_by(slug='opp-perf-cat').first()
    if not cat:
        cat = SkillCategory(name='Tech', slug='opp-perf-cat')
        db.session.add(cat)
        db.session.flush()
    skill = Skill(category_id=cat.id, name=f'Skill {slug}', slug=slug, is_published=True)
    db.session.add(skill)
    db.session.flush()
    db.session.add(StudentSkill(student_id=user_id, skill_id=skill.id, progress_pct=progress_pct))
    return skill


def test_opportunities_page_shows_correct_match_pct(app, client, make_user, login_as):
    user = make_user('opp_match_student')
    with app.app_context():
        skill = _make_skill_with_progress(user.id, 65, 'opp-match-skill')
        db.session.add(Opportunity(skill_id=skill.id, title='Freelance gig', is_published=True))
        db.session.commit()

    login_as(client, user)
    res = client.get('/skills/opportunities')
    assert res.status_code == 200
    assert '65% match' in res.get_data(as_text=True)


def test_gigs_page_shows_correct_match_pct(app, client, make_user, login_as):
    user = make_user('gigs_match_student')
    with app.app_context():
        skill = _make_skill_with_progress(user.id, 40, 'gigs-match-skill')
        db.session.add(Opportunity(skill_id=skill.id, title='Open gig', is_published=True))
        db.session.commit()

    login_as(client, user)
    res = client.get('/skills/gigs')
    assert res.status_code == 200
    assert '40% match' in res.get_data(as_text=True)


def test_unstarted_skill_has_no_match_badge(app, client, make_user, login_as):
    """A skill the student never started must show 0/no match, not crash and not
    accidentally pick up another student's progress row."""
    user = make_user('opp_nomatch_student')
    with app.app_context():
        cat = SkillCategory(name='Tech', slug='opp-nomatch-cat')
        db.session.add(cat)
        db.session.flush()
        skill = Skill(category_id=cat.id, name='Untouched Skill', slug='untouched-skill-opp', is_published=True)
        db.session.add(skill)
        db.session.flush()
        db.session.add(Opportunity(skill_id=skill.id, title='Gig nobody matches', is_published=True))
        db.session.commit()

    login_as(client, user)
    res = client.get('/skills/opportunities')
    assert res.status_code == 200
    # match_pct=0 is falsy in the template's {% if row.match_pct %} -- no badge at all,
    # not a "0% match" badge, and definitely not another student's leftover progress.
    assert '% match' not in res.get_data(as_text=True)


def test_earnings_totals_correct_with_eager_loaded_opportunity(app, client, make_user, login_as):
    user = make_user('earnings_student')
    with app.app_context():
        cat = SkillCategory(name='Tech', slug='earnings-perf-cat')
        db.session.add(cat)
        db.session.flush()
        skill = Skill(category_id=cat.id, name='Earnings Skill', slug='earnings-skill', is_published=True)
        db.session.add(skill)
        db.session.flush()
        opp = Opportunity(skill_id=skill.id, title='Paid gig', payment_amount=50000, is_published=True)
        db.session.add(opp)
        db.session.flush()
        db.session.add(OpportunityApplication(
            opportunity_id=opp.id, student_id=user.id, status='paid', payout_amount=45000,
        ))
        db.session.commit()

    login_as(client, user)
    res = client.get('/skills/earnings')
    assert res.status_code == 200
    assert '45,000' in res.get_data(as_text=True)
