"""End-to-end checks for the African Languages Lab (ALL) skills, on the real Skills routes:
seeding into the existing tables, catalog filters and the hub, a full
learn -> practise -> assessment -> project -> verified flow, the Skill Transcript, and the
self-reported-vs-verified language profile."""
import io
import json

import pytest

from app.extensions import db
from app.models import (
    Skill, SkillCategory, Challenge, ChallengeSubmission, ProjectTemplate, StudentProject, Lesson, CourseModule,
    SkillCourse, CareerTrack, StudentLanguage,
)


# Seeding all ~93 skills per test is slow on SQLite; most tests only need these.
SUBSET = {'yoruba-transcription', 'igbo-transcription', 'yoruba-english-translation', 'sentiment-annotation',
          'voice-recording', 'inter-annotator-agreement', 'transcription-qa'}


def _seed(app, monkeypatch, only):
    # Coach feedback is an AI call -- never make a network request from tests.
    import app.routes.skills_routes as routes
    monkeypatch.setattr(routes, 'generate_challenge_feedback', lambda *a, **k: (_ for _ in ()).throw(RuntimeError('no AI in tests')))
    from scripts.seed.seed_all_skills import seed
    with app.app_context():
        seed(verbose=False, only=only)
    return app


@pytest.fixture
def seeded(app, monkeypatch):
    return _seed(app, monkeypatch, SUBSET)


@pytest.fixture
def seeded_full(app, monkeypatch):
    return _seed(app, monkeypatch, None)


def _correct_form(spec):
    form = {}
    if spec['kind'] == 'transcription':
        for s in spec['segments']:
            form[f"seg-{s['id']}-text"] = s['reference']
            if s.get('speaker'):
                form[f"seg-{s['id']}-speaker"] = s['speaker']
            if s.get('start') is not None:
                form[f"seg-{s['id']}-start"] = str(s['start'])
    elif spec['kind'] == 'translation':
        for it in spec['items']:
            form[f"item-{it['id']}-translation"] = it['references'][0]
    elif spec['kind'] == 'labeling':
        for it in spec['items']:
            for f in it['fields']:
                expected = f['expected'] if isinstance(f['expected'], list) else [f['expected']]
                form[f"item-{it['id']}-{f['name']}"] = str(expected[0])
    elif spec['kind'] == 'recording':
        for p in spec['prompts']:
            form[f"rec-{p['id']}-metrics"] = json.dumps({'duration': 5, 'clip_pct': 0, 'rms_db': -24, 'silence_pct': 30})
            form[f"rec-{p['id']}-audio"] = (io.BytesIO(b'' * 20000), f"{p['id']}.webm", 'audio/webm')
        for f in spec.get('metadata_fields', []):
            form[f"meta-{f['name']}"] = (f.get('options') or ['Lagos'])[0]
    if spec.get('report'):
        form['report'] = ' '.join(['detail'] * (spec['report'].get('min_words', 15) + 5))
    return form


def _wrong_form(spec):
    form = _correct_form(spec)
    return {k: ('zzz' if not k.startswith('rec-') else '{"duration": 0.1}') for k in form if not k.endswith('-audio')}


def test_seed_populates_existing_tables_and_is_idempotent(seeded_full):
    seeded = seeded_full
    from scripts.seed.seed_all_skills import seed
    with seeded.app_context():
        counts = (SkillCategory.query.filter_by(program='all').count(),
                  Skill.query.join(SkillCategory).filter(SkillCategory.program == 'all').count(),
                  Challenge.query.count(), ProjectTemplate.query.count(), Lesson.query.count())
        assert counts[0] == 9 and counts[1] >= 90
        seed(verbose=False)
        assert counts == (SkillCategory.query.filter_by(program='all').count(),
                          Skill.query.join(SkillCategory).filter(SkillCategory.program == 'all').count(),
                          Challenge.query.count(), ProjectTemplate.query.count(), Lesson.query.count())
        yoruba = Skill.query.filter_by(slug='yoruba-transcription').one()
        assert yoruba.language == 'yoruba' and 'transcription' in yoruba.tags and yoruba.is_published
        steps = yoruba.path.steps.all()
        assert [s.step_type for s in steps] == ['course', 'challenge', 'challenge', 'project']
        assert steps[2].challenge.is_assessment and steps[2].challenge.pass_score == 70
        assert CareerTrack.query.filter_by(slug='all-nlp-builder').one().steps.count() == 5


def test_catalog_filters_and_hub(seeded_full, client, make_user, login_as):
    user = make_user('all_browser')
    login_as(client, user)
    r = client.get('/skills/catalog?language=yoruba')
    assert r.status_code == 200
    assert b'Yoruba Transcription' in r.data and b'Igbo Transcription' not in r.data
    r = client.get('/skills/catalog?program=all&tag=qa&level=advanced')
    assert b'Inter-Annotator Agreement' in r.data and b'Yoruba Transcription' not in r.data
    hub = client.get('/skills/african-languages')
    assert hub.status_code == 200
    for name in (b'Transcription', b'Translation', b'Speech &amp; Voice Data', b'Language Annotation', b'AI Data Work',
                 b'Linguistics', b'Language Technology', b'Quality Assurance', b'Project &amp; Work Skills'):
        assert name in hub.data
    assert b"doesn't guarantee" in hub.data  # honest framing, no placement claims
    assert client.get('/skills/african-languages?language=hausa&level=beginner').status_code == 200


def test_skill_page_shows_how_to_prove_it(seeded, client, make_user, login_as):
    login_as(client, make_user('all_viewer'))
    r = client.get('/skills/yoruba-transcription')
    assert r.status_code == 200
    assert b'How you prove this skill' in r.data and b'Pass the assessment' in r.data and b'Yoruba' in r.data
    task = client.get('/skills/yoruba-transcription/challenge/assessment')
    # Fresh student: the assessment is locked behind the lessons and practice, server-side.
    assert task.status_code == 200 and b'This assessment opens after you finish' in task.data
    assert b'seg-s1-text' not in task.data
    practice = client.get('/skills/yoruba-transcription/challenge/practice')
    assert b'seg-s1-text' in practice.data and b'Simulation' in practice.data
    # The reference answer must never be in the page before submission.
    with seeded.app_context():
        ref = Challenge.query.join(Skill).filter(Skill.slug == 'yoruba-transcription', Challenge.slug == 'assessment').one().task_spec['segments'][0]['reference']
    assert ref.encode() not in task.data


def test_every_task_kind_renders_and_scores(seeded, client, make_user, login_as):
    login_as(client, make_user('all_kinds'))
    for skill_slug in ('yoruba-english-translation', 'sentiment-annotation', 'voice-recording', 'inter-annotator-agreement'):
        page = client.get(f'/skills/{skill_slug}/challenge/practice')
        assert page.status_code == 200, skill_slug
        with seeded.app_context():
            ch = Challenge.query.join(Skill).filter(Skill.slug == skill_slug, Challenge.slug == 'practice').one()
            spec, ch_id = ch.task_spec, ch.id
        r = client.post(f'/skills/{skill_slug}/challenge/practice', data=_correct_form(spec))
        assert r.status_code == 302
        with seeded.app_context():
            sub = ChallengeSubmission.query.filter_by(challenge_id=ch_id).order_by(ChallengeSubmission.id.desc()).first()
            assert sub.score == 100, (skill_slug, sub.result)
        assert client.get(f'/skills/{skill_slug}/challenge/practice').status_code == 200  # result breakdown renders


def test_empty_structured_submission_is_rejected(seeded, client, make_user, login_as):
    login_as(client, make_user('all_empty'))
    r = client.post('/skills/sentiment-annotation/challenge/practice', data={})
    assert r.status_code == 302
    with seeded.app_context():
        assert ChallengeSubmission.query.count() == 0


def test_full_flow_to_verified_skill_transcript_and_language(seeded, client, make_user, login_as):
    user = make_user('all_learner')
    login_as(client, user)
    slug = 'yoruba-transcription'
    with seeded.app_context():
        skill = Skill.query.filter_by(slug=slug).one()
        lesson_ids = [l.id for l in Lesson.query.join(CourseModule).join(SkillCourse).filter(SkillCourse.skill_id == skill.id).all()]
        practice = Challenge.query.filter_by(skill_id=skill.id, slug='practice').one()
        assessment = Challenge.query.filter_by(skill_id=skill.id, slug='assessment').one()
        p_spec, a_spec, a_id = practice.task_spec, assessment.task_spec, assessment.id
        template_id = ProjectTemplate.query.filter_by(skill_id=skill.id).one().id

    client.post('/skills/languages', data={'language': 'yoruba', 'proficiency': 'native', 'dialect': 'Ijebu',
                                           'can_speak': '1', 'can_transcribe': '1'})
    assert b'self-reported' in client.get('/skills/languages').data

    from app.services.skills_service import is_skill_verified, get_skill_verification_record, get_path_step_states
    from app.services.language_profile_service import get_language_profile

    for lid in lesson_ids:
        assert client.post(f'/skills/lesson/{lid}/complete').get_json()['success']
    client.post(f'/skills/{slug}/challenge/practice', data=_correct_form(p_spec))

    # A failed assessment attempt does not complete its path step.
    client.post(f'/skills/{slug}/challenge/assessment', data=_wrong_form(a_spec))
    with seeded.app_context():
        skill = Skill.query.filter_by(slug=slug).one()
        states = [s['state'] for s in get_path_step_states(user.id, skill.path)]
        assert states == ['completed', 'completed', 'current', 'locked']
        failed = ChallengeSubmission.query.filter_by(challenge_id=a_id).one()
        assert failed.score < 70 and 'reference' not in json.dumps(failed.result)  # no answers leaked

    client.post(f'/skills/{slug}/challenge/assessment', data=_correct_form(a_spec))
    client.post(f'/skills/projects/start/{template_id}')
    with seeded.app_context():
        skill = Skill.query.filter_by(slug=slug).one()
        project = StudentProject.query.filter_by(student_id=user.id, project_template_id=template_id).one()
        assert project.workspace_type == 'writer'
        project.status = 'completed'
        db.session.commit()
        # Completed but unreviewed: still not verified, and the language stays self-reported.
        assert not is_skill_verified(user.id, skill.id)
        assert get_language_profile(user.id)[0]['verified_capabilities'] == []
        project.verification_status = 'reviewed'
        project.ai_feedback = {'score': 82}
        db.session.commit()
        assert is_skill_verified(user.id, skill.id)
        record = get_skill_verification_record(user.id, skill)
        assert record['assessment_status'] == 'passed' and record['project_status'] == 'reviewed' and record['verified']
        assert get_language_profile(user.id)[0]['verified_capabilities'] == ['Transcribe']

    transcript = client.get('/skills/transcript')
    assert transcript.status_code == 200
    assert b'Yoruba Transcription' in transcript.data and b'Verified' in transcript.data and b'Passed' in transcript.data
    assert client.get('/skills/talent').status_code == 200
    assert b'Yoruba' in client.get('/skills/talent').data


def test_language_profile_update_delete_and_ownership(seeded, client, make_user, login_as):
    owner = make_user('lang_owner')
    other = make_user('lang_other')
    login_as(client, owner)
    client.post('/skills/languages', data={'language': 'hausa', 'proficiency': 'fluent'})
    client.post('/skills/languages', data={'language': 'hausa', 'proficiency': 'native', 'dialect': 'Kano', 'can_read': '1'})
    client.post('/skills/languages', data={'language': 'other', 'other_language': 'Isoko', 'proficiency': 'basic'})
    client.post('/skills/languages', data={'action': 'background', 'language_background': '300L Linguistics, LASU'})
    with seeded.app_context():
        rows = StudentLanguage.query.filter_by(student_id=owner.id).order_by(StudentLanguage.id).all()
        assert [(r.language, r.proficiency, r.dialect) for r in rows] == [('hausa', 'native', 'Kano'), ('isoko', 'basic', None)]
        row_id = rows[0].id
    login_as(client, other)
    assert client.post(f'/skills/languages/{row_id}/delete').status_code == 404
    login_as(client, owner)
    client.post(f'/skills/languages/{row_id}/delete')
    with seeded.app_context():
        assert StudentLanguage.query.filter_by(student_id=owner.id).count() == 1


def test_existing_free_text_challenges_still_work(seeded, client, make_user, login_as, monkeypatch):
    """A challenge without task_spec keeps the original free-text + AI-feedback flow."""
    with seeded.app_context():
        cat = SkillCategory(name='Tech', slug='tech-x', order=0)
        db.session.add(cat)
        db.session.flush()
        s = Skill(category_id=cat.id, name='Old Skill', slug='old-skill', is_published=True)
        db.session.add(s)
        db.session.flush()
        db.session.add(Challenge(skill_id=s.id, title='Old', slug='old', instructions='Do it', is_published=True))
        db.session.commit()
    login_as(client, make_user('old_flow'))
    assert client.get('/skills/old-skill/challenge/old').status_code == 200
    client.post('/skills/old-skill/challenge/old', data={'content': 'my answer'})
    with seeded.app_context():
        sub = ChallengeSubmission.query.filter_by(content='my answer').one()
        assert sub.score is None and sub.result is None
