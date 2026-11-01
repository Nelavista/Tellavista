"""The ALL talent pipeline end to end: the first-cohort beginner path (order, progress,
gates, verification), Talent discovery filters on top of the existing employer Discover
page, privacy rules, and the evidence the Skill Transcript shows. Everything runs on the
real routes/services against a throwaway SQLite app (see conftest.py)."""
import pytest

from app.extensions import db
from app.models import (
    Skill, Challenge, ChallengeSubmission, ProjectTemplate, StudentProject, Lesson, CourseModule, SkillCourse,
    StudentLanguage, StudentPrivacySettings, StudentLessonProgress, User,
)
from app.services.skills_service import recompute_student_skill, is_skill_verified, get_path_step_states

SUBSET = {'african-language-data-beginner', 'yoruba-transcription', 'sentiment-annotation', 'inter-annotator-agreement'}
BEGINNER = 'african-language-data-beginner'


@pytest.fixture
def seeded(app, monkeypatch):
    import app.routes.skills_routes as routes
    monkeypatch.setattr(routes, 'generate_challenge_feedback', lambda *a, **k: (_ for _ in ()).throw(RuntimeError('no AI in tests')))
    from app.routes.employer_routes import employer_bp  # conftest doesn't register it
    if 'employer' not in app.blueprints:
        app.register_blueprint(employer_bp, url_prefix='/')
    from scripts.seed.seed_all_skills import seed
    with app.app_context():
        seed(verbose=False, only=SUBSET)
    return app


# ---------------------------------------------------------------- helpers (direct DB state)

def _lesson_ids(slug, course_index=None):
    skill = Skill.query.filter_by(slug=slug).one()
    q = Lesson.query.join(CourseModule).join(SkillCourse).filter(SkillCourse.skill_id == skill.id)
    if course_index is not None:
        q = q.filter(SkillCourse.order == course_index)
    return [l.id for l in q.order_by(SkillCourse.order, CourseModule.order, Lesson.order).all()]


def _complete_lessons(user_id, slug, only=None):
    ids = _lesson_ids(slug)
    for lid in (ids if only is None else ids[:only]):
        db.session.add(StudentLessonProgress(student_id=user_id, lesson_id=lid))
    db.session.commit()
    recompute_student_skill(user_id, Skill.query.filter_by(slug=slug).one().id)


def _submit(user_id, slug, which, score, summary=None, kind='transcription'):
    skill = Skill.query.filter_by(slug=slug).one()
    ch = Challenge.query.filter_by(skill_id=skill.id, slug=which).one()
    sub = ChallengeSubmission(challenge_id=ch.id, student_id=user_id, content='x', status='reviewed', score=score)
    sub.result = {'kind': kind, 'score': score, 'items': [], 'summary': summary or {}}
    db.session.add(sub)
    db.session.commit()


def _project(user_id, slug, status='completed', review=None):
    skill = Skill.query.filter_by(slug=slug).one()
    t = ProjectTemplate.query.filter_by(skill_id=skill.id).one()
    p = StudentProject(student_id=user_id, project_template_id=t.id, title=t.title, status=status, source='template')
    if review is not None:
        p.verification_status = 'reviewed'
        p.ai_feedback = {'score': review}
    db.session.add(p)
    db.session.commit()


def _verified(user_id, slug):
    _complete_lessons(user_id, slug)
    _submit(user_id, slug, 'practice', 55)
    _submit(user_id, slug, 'assessment', 92, {'word_accuracy': 96, 'word_error_rate': 0.04,
                                               'word_accuracy_no_diacritics': 98, 'speaker_accuracy': 100})
    _project(user_id, slug, 'completed', 82)


def _opt_in(user_id, visibility='employers', show_transcript=True):
    db.session.add(StudentPrivacySettings(student_id=user_id, profile_visibility=visibility, show_skill_transcript=show_transcript))
    db.session.commit()


def _language(user_id, key, **caps):
    db.session.add(StudentLanguage(student_id=user_id, language=key, proficiency=caps.pop('proficiency', 'native'), **caps))
    db.session.commit()


# ---------------------------------------------------------------- A. beginner path

def test_fresh_student_sees_the_beginner_path_first(seeded, client, make_user, login_as):
    login_as(client, make_user('fresh1'))
    hub = client.get('/skills/african-languages')
    assert hub.status_code == 200
    body = hub.data.decode()
    assert 'Learn African Language AI Skills' in body and 'African Language Data Beginner' in body
    assert 'Start the beginner path' in body
    assert body.index('African Language Data Beginner') < body.index('Then choose a direction')


def test_beginner_path_order_seven_courses_then_practice_assessment_project(seeded):
    with seeded.app_context():
        skill = Skill.query.filter_by(slug=BEGINNER).one()
        steps = skill.path.steps.all()
        assert [s.step_type for s in steps] == ['course'] * 7 + ['challenge', 'challenge', 'project']
        assert [s.course.title for s in steps[:7]] == [
            'Introduction to Language Data', 'Data Privacy & Confidentiality', 'Following Annotation Guidelines',
            'Transcription Fundamentals', 'Audio Quality', 'Basic Annotation', 'AI Data Fundamentals']
        assert not steps[7].challenge.is_assessment and steps[8].challenge.is_assessment
        assert steps[8].title.startswith('9. Practical Assessment')
        assert steps[9].title.startswith('10. Final Skill Verification') and 'Practice Project' in steps[9].title


def test_course_progress_is_preserved_and_shown_on_the_hub(seeded, client, make_user, login_as):
    user = make_user('fresh2')
    login_as(client, user)
    with seeded.app_context():
        first_course = _lesson_ids(BEGINNER, course_index=1)
    for lid in first_course:
        assert client.post(f'/skills/lesson/{lid}/complete').get_json()['success']
    with seeded.app_context():
        skill = Skill.query.filter_by(slug=BEGINNER).one()
        states = [s['state'] for s in get_path_step_states(user.id, skill.path)]
        assert states[:2] == ['completed', 'current'] and set(states[2:]) == {'locked'}
    hub = client.get('/skills/african-languages').data.decode()
    assert 'Continue the beginner path' in hub and '% of lessons done' in hub
    i = hub.index('Data Privacy &amp; Confidentiality')
    assert '← you are here' in hub[i:i + 200]


def test_assessment_requires_lessons_and_practice_server_side(seeded, client, make_user, login_as):
    user = make_user('fresh3')
    login_as(client, user)
    url = f'/skills/{BEGINNER}/challenge/assessment'
    with seeded.app_context():
        a_id = Challenge.query.join(Skill).filter(Skill.slug == BEGINNER, Challenge.slug == 'assessment').one().id
    # Direct POST before any work: rejected, nothing stored.
    client.post(url, data={'item-p1-a': 'Acceptable'})
    assert b'This assessment opens after you finish' in client.get(url).data
    with seeded.app_context():
        assert ChallengeSubmission.query.filter_by(challenge_id=a_id).count() == 0
        _complete_lessons(user.id, BEGINNER)
    # Lessons alone are not enough -- the practice round must be attempted.
    assert b'Attempt the practice task' in client.get(url).data
    client.post(f'/skills/{BEGINNER}/challenge/practice', data={'item-a1-a': 'Positive'})
    page = client.get(url)
    assert b'This assessment opens after you finish' not in page.data and b'Submit assessment' in page.data
    fetch = client.post('/skills/yoruba-transcription/challenge/assessment', data={'seg-s1-text': 'x'},
                        headers={'X-Requested-With': 'fetch'})
    assert fetch.status_code == 403  # another skill's assessment stays locked for this student


def test_project_opens_only_after_assessment_and_verification_cannot_happen_early(seeded, client, make_user, login_as):
    user = make_user('fresh4')
    login_as(client, user)
    with seeded.app_context():
        template_id = ProjectTemplate.query.join(Skill).filter(Skill.slug == BEGINNER).one().id
        skill_id = Skill.query.filter_by(slug=BEGINNER).one().id
        _complete_lessons(user.id, BEGINNER)
        _submit(user.id, BEGINNER, 'practice', 40)
    client.post(f'/skills/projects/start/{template_id}')
    with seeded.app_context():
        assert StudentProject.query.filter_by(student_id=user.id).count() == 0  # locked before the assessment
        assert not is_skill_verified(user.id, skill_id)
        _submit(user.id, BEGINNER, 'assessment', 60, kind='labeling')  # below the 70% pass mark
    client.post(f'/skills/projects/start/{template_id}')
    with seeded.app_context():
        assert StudentProject.query.filter_by(student_id=user.id).count() == 0
        _submit(user.id, BEGINNER, 'assessment', 85, kind='labeling')
    client.post(f'/skills/projects/start/{template_id}')
    with seeded.app_context():
        project = StudentProject.query.filter_by(student_id=user.id).one()
        assert not is_skill_verified(user.id, skill_id)          # started only
        project.status = 'completed'
        db.session.commit()
        assert not is_skill_verified(user.id, skill_id)          # completed, never reviewed
        project.verification_status, project.ai_feedback = 'reviewed', {'score': 55}
        db.session.commit()
        assert not is_skill_verified(user.id, skill_id)          # reviewed below 60
        project.ai_feedback = {'score': 74}
        db.session.commit()
        assert is_skill_verified(user.id, skill_id)
    hub = client.get('/skills/african-languages').data.decode()
    start = hub.index('id="start-here"')
    assert 'Verified' in hub[start:start + 1500]


def test_practice_is_required_for_verification(seeded):
    with seeded.app_context():
        u = User(username='nopractice', email='np@example.com')
        db.session.add(u)
        db.session.commit()
        _complete_lessons(u.id, 'yoruba-transcription')
        _submit(u.id, 'yoruba-transcription', 'assessment', 95)
        _project(u.id, 'yoruba-transcription', 'completed', 90)
        skill_id = Skill.query.filter_by(slug='yoruba-transcription').one().id
        assert not is_skill_verified(u.id, skill_id)
        _submit(u.id, 'yoruba-transcription', 'practice', 10)  # any genuine attempt counts as "attempted"
        assert is_skill_verified(u.id, skill_id)


# ---------------------------------------------------------------- B/C. talent discovery + privacy

@pytest.fixture
def talent_pool(seeded, make_user):
    ids = {}
    for name in ('verified_ada', 'assessed_bisi', 'learning_chidi', 'private_dayo', 'hidden_emeka'):
        ids[name] = make_user(name).id
    with seeded.app_context():
        users = {k: User.query.get(v) for k, v in ids.items()}
        users['verified_ada'].department = 'Linguistics'
        users['assessed_bisi'].department = 'English'
        users['learning_chidi'].department = 'Computer Science'
        users['learning_chidi'].language_background = 'Minor in Hausa linguistics'
        db.session.commit()

        _verified(ids['verified_ada'], 'yoruba-transcription')
        _language(ids['verified_ada'], 'yoruba', can_speak=True, can_transcribe=True)
        _opt_in(ids['verified_ada'])

        _complete_lessons(ids['assessed_bisi'], 'yoruba-transcription')
        _submit(ids['assessed_bisi'], 'yoruba-transcription', 'practice', 70)
        _submit(ids['assessed_bisi'], 'yoruba-transcription', 'assessment', 78, {'word_accuracy': 81, 'word_error_rate': 0.19,
                                                                                 'word_accuracy_no_diacritics': 90})
        _project(ids['assessed_bisi'], 'yoruba-transcription', 'completed')
        _language(ids['assessed_bisi'], 'yoruba', can_speak=True)
        _opt_in(ids['assessed_bisi'], 'public')

        _complete_lessons(ids['learning_chidi'], 'sentiment-annotation', only=1)
        _complete_lessons(ids['learning_chidi'], 'inter-annotator-agreement', only=1)
        _language(ids['learning_chidi'], 'hausa', proficiency='fluent', can_read=True)
        _opt_in(ids['learning_chidi'], 'public')

        _verified(ids['private_dayo'], 'yoruba-transcription')       # never opted in
        _language(ids['private_dayo'], 'yoruba', can_transcribe=True)

        _verified(ids['hidden_emeka'], 'yoruba-transcription')
        _language(ids['hidden_emeka'], 'yoruba', can_transcribe=True)
        _opt_in(ids['hidden_emeka'], 'employers', show_transcript=False)
    return ids


def _names(results):
    return sorted(r['student'].username for r in results)


def test_talent_filters(seeded, talent_pool):
    from app.services.talent_search_service import search_talent
    with seeded.app_context():
        yoruba_id = Skill.query.filter_by(slug='yoruba-transcription').one().id
        everyone = ['assessed_bisi', 'hidden_emeka', 'learning_chidi', 'verified_ada']
        assert _names(search_talent()) == everyone                                   # private_dayo never appears
        assert _names(search_talent(language='yoruba')) == ['assessed_bisi', 'hidden_emeka', 'verified_ada']
        assert _names(search_talent(language='hausa')) == ['learning_chidi']
        # Profile-level filters (skill, level, verified/in-progress): hidden_emeka's verified
        # badge counts, exactly as on V1's Discover and Talent Profile.
        assert _names(search_talent(skill_id=yoruba_id)) == ['assessed_bisi', 'hidden_emeka', 'verified_ada']
        assert _names(search_talent(level='advanced')) == ['learning_chidi']
        assert _names(search_talent(status='verified')) == ['hidden_emeka', 'verified_ada']
        assert _names(search_talent(status='in_progress')) == ['assessed_bisi', 'learning_chidi']
        assert _names(search_talent(language='yoruba', status='verified', level='beginner')) == ['hidden_emeka', 'verified_ada']
        # Transcript-level filters never match a student whose transcript is private.
        assert _names(search_talent(status='assessment_passed')) == ['assessed_bisi', 'verified_ada']
        assert _names(search_talent(practical_done=True)) == ['assessed_bisi', 'verified_ada']
        assert _names(search_talent(background='linguistics')) == ['learning_chidi', 'verified_ada']


def test_privacy_hidden_transcript_and_language_claims(seeded, talent_pool):
    from app.services.talent_search_service import search_talent
    with seeded.app_context():
        by_name = {r['student'].username: r for r in search_talent()}
        emeka = by_name['hidden_emeka']
        # Transcript private: the template shows only skill name/verified/level for his
        # matches -- no assessment, practical or QA detail (asserted on the page below).
        assert not emeka['shows_evidence']
        assert [m['skill'].slug for m in emeka['matches']] == ['yoruba-transcription']
        assert emeka['languages'][0]['claimed'] == ['Transcribe']       # self-reported claim
        assert [s.slug for s in emeka['languages'][0]['verified_skills']] == ['yoruba-transcription']  # badge-level
        ada, bisi = by_name['verified_ada'], by_name['assessed_bisi']
        assert [s.slug for s in ada['languages'][0]['verified_skills']] == ['yoruba-transcription']
        assert bisi['languages'][0]['verified_skills'] == []            # claims Yoruba, not verified
        assert by_name['learning_chidi']['languages'][0]['verified_skills'] == []


def test_discover_route_access_and_privacy(seeded, talent_pool, client, make_user, login_as):
    login_as(client, make_user('plain_student'))
    assert client.get('/employer/discover').status_code == 302             # students can't browse talent
    login_as(client, make_user('ops_admin', is_admin=True))
    page = client.get('/employer/discover?language=yoruba&status=verified').data.decode()
    assert 'Verified_Ada' in page and 'Private_Dayo' not in page
    assert 'Yoruba Transcription' in page and 'Assessment passed (92%)' in page and 'QA passed (82%)' in page
    # Emeka appears (verified badge is profile-level) but none of his transcript detail does.
    emeka_row = page[page.index('Hidden_Emeka'):]
    emeka_row = emeka_row[:emeka_row.index('View Profile')]
    assert 'Verified' in emeka_row and 'Assessment' not in emeka_row and 'QA passed' not in emeka_row
    assert 'Practical:' not in emeka_row and 'keeps their Skill Transcript details' in emeka_row
    assert 'Hidden_Emeka' not in client.get('/employer/discover?status=assessment_passed').data.decode()
    everyone = client.get('/employer/discover').data.decode()
    assert 'Private_Dayo' not in everyone
    assert '(self-reported)' in everyone                                   # Bisi's unverified Yoruba claim
    for word in ('African Languages Lab project', 'hired by', 'worked for African Languages Lab'):
        assert word not in everyone


def test_talent_profile_evidence_respects_transcript_privacy(seeded, talent_pool, client, make_user, login_as):
    login_as(client, make_user('viewer_admin', is_admin=True))
    ada = client.get('/skills/talent/verified_ada').data.decode()
    assert 'Skill evidence' in ada and 'Word accuracy 96%' in ada and 'Linguistics' in ada
    emeka = client.get('/skills/talent/hidden_emeka').data.decode()
    assert 'Skill evidence' not in emeka and 'Word accuracy' not in emeka
    assert client.get('/skills/talent/private_dayo').status_code == 302    # private profile


# ---------------------------------------------------------------- D. skill transcript

def test_transcript_shows_each_stage_with_real_scores(seeded, talent_pool, client, login_as):
    with seeded.app_context():
        ada = User.query.get(talent_pool['verified_ada'])
        bisi = User.query.get(talent_pool['assessed_bisi'])
        chidi = User.query.get(talent_pool['learning_chidi'])
    login_as(client, ada)
    page = client.get('/skills/transcript').data.decode()
    i = page.index('Yoruba Transcription')
    block = page[i:i + 4000]
    for text in ('Verified', 'Learning completed', 'Yes', '1 / 1 attempted', 'Passed · best 92%',
                 'Word accuracy 96%', 'Speakers 100%', 'Practical task (practice project)', 'Quality review', 'Passed · 82%'):
        assert text in block, text

    login_as(client, bisi)
    block = client.get('/skills/transcript').data.decode()
    assert 'Not verified yet' in block and 'Word accuracy 81%' in block and 'Pending' in block

    login_as(client, chidi)
    page = client.get('/skills/transcript').data.decode()
    assert 'Not taken' in page and 'Measured in the assessment' not in page and 'Word accuracy' not in page


def test_onboarding_offers_only_the_beginner_path_from_all(seeded, client, make_user, login_as):
    """Regression: seeding ~94 ALL skills flooded the first-visit onboarding grid (100 chips,
    beginner path at #90). Onboarding must show the existing skills plus the one ALL entry."""
    login_as(client, make_user('onboard_new'))
    page = client.get('/skills/onboarding').data.decode()
    assert 'African Language Data Beginner' in page
    for other in ('Yoruba Transcription', 'Sentiment Annotation', 'Inter-Annotator Agreement'):
        assert other not in page


def test_lesson_quiz_radios_are_grouped_per_question(seeded, client, make_user, login_as):
    """Regression: the options loop's loop.index0 shadowed the question index, so radio
    names were q0..q3 per OPTION; no question could ever register as answered and lesson
    quizzes were impossible to submit (lesson_view.html and day_view.html)."""
    import re
    login_as(client, make_user('quiz_taker'))
    page = client.get(f'/skills/{BEGINNER}/learn/introduction-to-language-data/what-language-data-is-and-who-makes-it').data.decode()
    names = re.findall(r'<input type="radio" name="(q\d+)" value="(\d+)"', page)
    assert len(names) == 12  # 3 questions x 4 options
    assert [n for n, _ in names] == ['q0'] * 4 + ['q1'] * 4 + ['q2'] * 4
    assert [v for _, v in names] == ['0', '1', '2', '3'] * 3


def test_discover_keeps_the_existing_min_rating_filter(seeded, talent_pool, client, make_user, login_as):
    """Regression: the extended Discover form briefly dropped the pre-existing
    'Min rating' input. Nobody in the pool has a rating, so any min_rating excludes all."""
    login_as(client, make_user('rating_admin', is_admin=True))
    page = client.get('/employer/discover').data.decode()
    assert 'name="min_rating"' in page and 'Verified_Ada' in page
    filtered = client.get('/employer/discover?min_rating=1').data.decode()
    assert 'Verified_Ada' not in filtered and 'No matching students' in filtered
