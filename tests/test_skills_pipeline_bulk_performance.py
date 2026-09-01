"""Regression tests for the P2 performance fix: get_pipeline_state() (services/
skills_service.py) does 5-6 queries per skill, and the Skills dashboard/My Learning
pages previously called it once per started skill in a loop -- an 8-skill student cost
40-50+ queries for that one section alone. get_pipeline_states_bulk() computes the same
result for every skill in a fixed, small number of queries. This proves both that the
batched result is identical to the per-skill result, and that query count no longer
scales with the number of skills.
"""
from sqlalchemy import event
from extensions import db
from models import (
    SkillCategory, Skill, StudentSkill, Challenge, ChallengeSubmission,
    ProjectTemplate, StudentProject, Opportunity, OpportunityApplication,
)
from services.skills_service import get_pipeline_state, get_pipeline_states_bulk


def _make_skill(name, slug):
    cat = SkillCategory.query.filter_by(slug='bulk-perf-cat').first()
    if not cat:
        cat = SkillCategory(name='Tech', slug='bulk-perf-cat')
        db.session.add(cat)
        db.session.flush()
    skill = Skill(category_id=cat.id, name=name, slug=slug, is_published=True)
    db.session.add(skill)
    db.session.flush()
    return skill


def test_bulk_result_matches_individual_calls_for_mixed_progress_states(app, make_user):
    user = make_user('pipeline_bulk_student')
    with app.app_context():
        # Skill A: fully verified and earned.
        skill_a = _make_skill('Skill A', 'skill-a-bulk')
        db.session.add(StudentSkill(student_id=user.id, skill_id=skill_a.id, status='completed'))
        challenge = Challenge(skill_id=skill_a.id, title='Drill', slug='drill-a', is_published=True)
        db.session.add(challenge)
        db.session.flush()
        db.session.add(ChallengeSubmission(student_id=user.id, challenge_id=challenge.id, content='my answer'))
        template = ProjectTemplate(skill_id=skill_a.id, title='Build it', slug='build-it-a', is_published=True)
        db.session.add(template)
        db.session.flush()
        project = StudentProject(student_id=user.id, project_template_id=template.id, title='My build',
                                  source='template', status='completed', verification_status='reviewed')
        project.ai_feedback = {'score': 85}
        db.session.add(project)
        opp = Opportunity(skill_id=skill_a.id, title='Gig A', is_published=True)
        db.session.add(opp)
        db.session.flush()
        db.session.add(OpportunityApplication(opportunity_id=opp.id, student_id=user.id, status='paid'))

        # Skill B: just started, nothing else.
        skill_b = _make_skill('Skill B', 'skill-b-bulk')
        db.session.add(StudentSkill(student_id=user.id, skill_id=skill_b.id, status='in_progress'))

        # Skill C: completed project but never reviewed -- must NOT count as verified.
        skill_c = _make_skill('Skill C', 'skill-c-bulk')
        db.session.add(StudentSkill(student_id=user.id, skill_id=skill_c.id, status='completed'))
        template_c = ProjectTemplate(skill_id=skill_c.id, title='Build C', slug='build-it-c', is_published=True)
        db.session.add(template_c)
        db.session.flush()
        db.session.add(StudentProject(student_id=user.id, project_template_id=template_c.id, title='Unreviewed',
                                       source='template', status='completed'))
        db.session.commit()

        skill_ids = [skill_a.id, skill_b.id, skill_c.id]
        individual = {sid: get_pipeline_state(user.id, sid) for sid in skill_ids}
        bulk = get_pipeline_states_bulk(user.id, skill_ids)

        for sid in skill_ids:
            assert bulk[sid] == individual[sid], f'mismatch for skill {sid}'

        # Sanity: skill A really is fully done, C's verify phase is NOT done despite
        # having a "completed" project (unreviewed), proving _project_counts_as_verified
        # logic survived the refactor intact.
        assert individual[skill_a.id][1] == 'earn'
        assert all(step['state'] == 'done' for step in individual[skill_a.id][0])
        c_steps = individual[skill_c.id][0]
        assert c_steps[3]['state'] != 'done'  # verify phase


def test_bulk_query_count_does_not_scale_with_skill_count(app, make_user):
    user = make_user('pipeline_bulk_query_count_student')
    with app.app_context():
        skill_ids = []
        for i in range(6):
            skill = _make_skill(f'Scale Skill {i}', f'scale-skill-{i}-bulk')
            db.session.add(StudentSkill(student_id=user.id, skill_id=skill.id, status='in_progress'))
            skill_ids.append(skill.id)
        db.session.commit()

        queries = []

        def _count(conn, cursor, statement, parameters, context, executemany):
            queries.append(statement)

        event.listen(db.engine, 'before_cursor_execute', _count)
        try:
            get_pipeline_states_bulk(user.id, skill_ids)
        finally:
            event.remove(db.engine, 'before_cursor_execute', _count)
        bulk_query_count = len(queries)

        queries.clear()
        event.listen(db.engine, 'before_cursor_execute', _count)
        try:
            for sid in skill_ids:
                get_pipeline_state(user.id, sid)
        finally:
            event.remove(db.engine, 'before_cursor_execute', _count)
        individual_query_count = len(queries)

        # The old per-skill path does ~5-6 queries PER skill (30-36 for 6 skills); the
        # bulk path does a fixed handful regardless of how many skills are passed in.
        assert bulk_query_count <= 6
        assert individual_query_count > bulk_query_count * 3
