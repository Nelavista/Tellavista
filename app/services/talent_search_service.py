"""Talent search for the employer Discover page, extended for language-data talent.

Builds on the existing discovery rule: a student appears only if they opted in
(StudentPrivacySettings.profile_visibility in 'employers'/'public'). Two levels of detail,
matching what V1 already shows on every visible Talent Profile:
- Profile level (shown and filterable once a student opts in): which skills they've
  started or verified, skill level, and self-reported languages -- V1's Discover and Talent
  Profile always showed verified-skill badges, independent of the transcript toggle.
- Transcript level (assessment results, measured scores, practical-task and quality-review
  status): only when the student's "show Skill Transcript" toggle is on. A student who hid
  it is never matched by, or described with, those details.

Every value comes from get_skill_verification_record() / get_language_profile(), the same
functions behind the student's own Skill Transcript and Talent Profile, so an employer
never sees a richer or different view than the student does.
"""
from app.extensions import db
from app.models import User, StudentPrivacySettings, StudentSkill, Skill, StudentLanguage
from app.services.skills_service import get_skill_verification_record, get_talent_stats
from app.services.language_profile_service import get_language_profile

STATUS_FILTERS = {
    'verified': 'Verified',
    'assessment_passed': 'Assessment passed',
    'in_progress': 'In progress',
}


def search_talent(q='', skill_id=None, language='', level='', status='', practical_done=False,
                  background='', min_rating=None, verified_only=False):
    query = (
        db.session.query(StudentPrivacySettings, User)
        .join(User, StudentPrivacySettings.student_id == User.id)
        .filter(StudentPrivacySettings.profile_visibility.in_(['employers', 'public']), User.is_deleted.is_(False))
    )
    if q:
        like = f'%{q}%'
        query = query.filter(db.or_(User.name.ilike(like), User.username.ilike(like), User.university.ilike(like)))
    if background:
        like = f'%{background}%'
        query = query.filter(db.or_(User.department.ilike(like), User.language_background.ilike(like),
                                    User.faculty.ilike(like)))

    skill_filters = bool(skill_id or level or status or practical_done or verified_only)
    # Filters that can only be answered from transcript-level detail.
    transcript_filters = status == 'assessment_passed' or practical_done
    results = []
    for privacy, student in query.order_by(User.name).all():
        shows_evidence = privacy.show_skill_transcript is not False
        if transcript_filters and not shows_evidence:
            continue

        # Languages are profile-level: the self-reported claims plus which language skills
        # are verified (the same verified badges a visible Talent Profile already shows).
        languages = get_language_profile(student.id)
        if language and not any(lp['row'].language == language for lp in languages):
            # Also match students with progress in a skill of that language.
            has_lang_skill = StudentSkill.query.join(Skill, StudentSkill.skill_id == Skill.id).filter(
                StudentSkill.student_id == student.id, Skill.language == language).first() is not None
            if not has_lang_skill:
                continue

        matches = []
        # Skill rows are profile-level; their transcript detail is hidden in the template.
        rows = StudentSkill.query.filter_by(student_id=student.id)
        if skill_id:
            rows = rows.filter_by(skill_id=skill_id)
        for ss in rows.all():
            skill = ss.skill
            if not skill or not skill.is_published:
                continue
            if language and skill.language not in (None, language):
                continue
            if level and skill.level != level:
                continue
            rec = get_skill_verification_record(student.id, skill)
            if (status == 'verified' or verified_only) and not rec['verified']:
                continue
            if status == 'assessment_passed' and rec['assessment_status'] != 'passed':
                continue
            if status == 'in_progress' and rec['verified']:
                continue
            if practical_done and rec['project_status'] not in ('completed', 'reviewed'):
                continue
            matches.append(rec)
        if skill_filters and not matches:
            continue

        stats = get_talent_stats(student)
        if min_rating and (not stats['avg_rating'] or stats['avg_rating'] < min_rating):
            continue
        matches.sort(key=lambda r: (not r['verified'], r['assessment_status'] != 'passed', r['skill'].name))
        results.append({
            'student': student, 'privacy': privacy, 'stats': stats, 'languages': languages,
            'matches': matches[:5], 'shows_evidence': shows_evidence,
        })
    results.sort(key=lambda r: (-sum(1 for m in r['matches'] if m['verified']), (r['student'].name or '').lower()))
    return results


def language_options():
    """Languages that actually appear on opted-in profiles or language skills."""
    from app.services.language_profile_service import language_label
    keys = {row[0] for row in db.session.query(StudentLanguage.language).distinct().all()}
    keys |= {row[0] for row in db.session.query(Skill.language).filter(Skill.language.isnot(None)).distinct().all()}
    return sorted(((k, language_label(k)) for k in keys), key=lambda kv: kv[1])
