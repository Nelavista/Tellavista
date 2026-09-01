"""Regression test for the P2 performance fix: catalog() (routes/skills_routes.py)
previously ran 4 separate .count() queries per skill card (projects/students/
opportunities/has_content) -- a published catalog of N skills cost 4N queries on one
page load. Now 4 grouped-count queries total, covering every skill on the page. Proves
the counts rendered are still correct after the refactor, including that unpublished
rows are still excluded from each count exactly as before.
"""
from extensions import db
from models import SkillCategory, Skill, ProjectTemplate, StudentSkill, Opportunity, SkillCourse


def test_catalog_counts_are_correct_after_batching(app, client, make_user, login_as):
    user = make_user('catalog_perf_student')
    # make_user() opens and commits its own app context internally -- both calls must
    # happen before the block below opens a second, uncommitted one, or SQLite's
    # single-writer lock deadlocks the two against each other.
    s1 = make_user('catalog_learner_1')
    s2 = make_user('catalog_learner_2')
    with app.app_context():
        cat = SkillCategory(name='Tech', slug='catalog-perf-cat')
        db.session.add(cat)
        db.session.flush()
        skill = Skill(category_id=cat.id, name='Design', slug='design-catalog-perf', is_published=True)
        db.session.add(skill)
        db.session.flush()

        # 2 published course -> has_content True; 1 unpublished project template must
        # NOT count.
        db.session.add(SkillCourse(skill_id=skill.id, title='Intro', slug='intro-catalog-perf', is_published=True))
        db.session.add(ProjectTemplate(skill_id=skill.id, title='P1', slug='p1-catalog-perf', is_published=True))
        db.session.add(ProjectTemplate(skill_id=skill.id, title='P2', slug='p2-catalog-perf', is_published=True))
        db.session.add(ProjectTemplate(skill_id=skill.id, title='P3 (draft)', slug='p3-catalog-perf', is_published=False))

        db.session.add(StudentSkill(student_id=s1.id, skill_id=skill.id))
        db.session.add(StudentSkill(student_id=s2.id, skill_id=skill.id))

        db.session.add(Opportunity(skill_id=skill.id, title='Gig 1', is_published=True))
        db.session.add(Opportunity(skill_id=skill.id, title='Gig 2 (unpublished)', is_published=False))
        db.session.commit()

    login_as(client, user)
    res = client.get('/skills/catalog')
    assert res.status_code == 200
    body = res.get_data(as_text=True)

    # Each label is tied to its value in the template
    # (<span class="...meta-label">Label</span><span>N</span>), so match both together
    # rather than a bare number that could coincidentally match a different field.
    assert 'Projects</span><span>2</span>' in body  # 2 published, the draft excluded
    assert 'Learning it</span><span>2</span>' in body
    assert 'Gigs open</span><span>1</span>' in body  # 1 published, the other excluded
