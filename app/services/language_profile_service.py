"""The student language profile for language-data work (African Languages Lab skills).

What a student SAYS they can do lives on StudentLanguage rows and is always shown as
self-reported. What they've PROVEN is derived here, at read time, from verified
language-specific Skills (Skill.language + is_skill_verified) -- selecting a language
never verifies it, and there is no stored 'verified' flag that could drift out of sync.
"""
from app.models import Skill, SkillCategory, StudentLanguage, StudentSkill
from app.services.skills_service import is_skill_verified

# key -> display name. Keys are what Skill.language and StudentLanguage.language store.
LANGUAGES = {
    'yoruba': 'Yoruba', 'igbo': 'Igbo', 'hausa': 'Hausa', 'pidgin': 'Nigerian Pidgin',
    'nigerian-english': 'Nigerian English', 'english': 'English',
    'edo': 'Edo (Bini)', 'efik': 'Efik', 'ibibio': 'Ibibio', 'tiv': 'Tiv', 'nupe': 'Nupe',
    'fulfulde': 'Fulfulde', 'kanuri': 'Kanuri', 'ijaw': 'Ijaw', 'urhobo': 'Urhobo',
    'igala': 'Igala', 'idoma': 'Idoma', 'ebira': 'Ebira',
    'swahili': 'Swahili', 'amharic': 'Amharic', 'akan': 'Akan (Twi)', 'ewe': 'Ewe',
    'wolof': 'Wolof', 'zulu': 'isiZulu', 'xhosa': 'isiXhosa', 'somali': 'Somali',
    'french': 'French', 'arabic': 'Arabic', 'portuguese': 'Portuguese',
}

PROFICIENCY_LABELS = {
    'basic': 'Basic', 'conversational': 'Conversational', 'fluent': 'Fluent', 'native': 'Native / first language',
}

CAPABILITIES = [
    ('can_speak', 'Speak'), ('can_read', 'Read'), ('can_write', 'Write'),
    ('can_transcribe', 'Transcribe'), ('can_translate', 'Translate'),
]

# Which self-reported capability a verified skill in each ALL category backs up.
_CATEGORY_CAPABILITY = {
    'transcription': 'can_transcribe',
    'translation': 'can_translate',
    'speech-voice-data': 'can_speak',
}


def language_label(key):
    if not key:
        return None
    return LANGUAGES.get(key, key.replace('-', ' ').title())


def normalize_language_key(raw):
    raw = (raw or '').strip().lower()
    if not raw:
        return None
    for key, label in LANGUAGES.items():
        if raw in (key, label.lower()):
            return key
    return '-'.join(raw.split())[:40]


def get_language_profile(student_id):
    """One entry per StudentLanguage row: the self-reported claims plus the skills that
    actually verify work in that language, and which claimed capabilities those back."""
    rows = StudentLanguage.query.filter_by(student_id=student_id).order_by(StudentLanguage.created_at).all()
    if not rows:
        return []
    language_keys = [r.language for r in rows]
    started = (
        StudentSkill.query.join(Skill, StudentSkill.skill_id == Skill.id)
        .filter(StudentSkill.student_id == student_id, StudentSkill.status == 'completed',
                Skill.language.in_(language_keys))
        .all()
    )
    verified_by_language = {}
    for row in started:
        if is_skill_verified(student_id, row.skill_id):
            verified_by_language.setdefault(row.skill.language, []).append(row.skill)

    profile = []
    for r in rows:
        verified_skills = verified_by_language.get(r.language, [])
        verified_caps = set()
        for skill in verified_skills:
            cap = _CATEGORY_CAPABILITY.get(skill.category.slug if skill.category else None)
            if cap:
                verified_caps.add(cap)
        profile.append({
            'row': r, 'label': language_label(r.language),
            'proficiency_label': PROFICIENCY_LABELS.get(r.proficiency, r.proficiency),
            'claimed': [label for attr, label in CAPABILITIES if getattr(r, attr)],
            'verified_capabilities': [label for attr, label in CAPABILITIES if attr in verified_caps],
            'verified_skills': verified_skills,
        })
    return profile


def recommended_language_skills(student_id, limit=6):
    """Published language-specific skills matching languages on the student's profile --
    so a Yoruba speaker sees Yoruba Transcription first on the ALL hub."""
    keys = [r.language for r in StudentLanguage.query.filter_by(student_id=student_id).all()]
    if not keys:
        return []
    return (
        Skill.query.join(SkillCategory, Skill.category_id == SkillCategory.id)
        .filter(Skill.is_published.is_(True), Skill.language.in_(keys))
        .order_by(SkillCategory.order, Skill.order).limit(limit).all()
    )
