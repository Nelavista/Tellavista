"""African Languages Lab (ALL) skills curriculum — data only, no app imports at module
level, so it can be validated offline (see validate()). Seeded into the existing Skills
tables by scripts/seed/seed_all_skills.py.

    CATEGORIES  the 9 ALL SkillCategory rows (program='all')
    SKILLS      every skill dict, each tagged with its category slug
    TRACKS      multi-skill CareerTracks built from ALL skills
"""
from . import transcription, translation, speech, annotation, ai_data, linguistics, language_tech, quality, work_skills
from .beginner import BEGINNER

PROGRAM = 'all'

# (slug, name, icon, description, module)
_CATEGORY_DEFS = [
    ('transcription', 'Transcription', 'ri-file-text-line',
     'Turn African-language speech into accurate, guideline-perfect text.', transcription),
    ('translation', 'Translation', 'ri-translate-2',
     'Translate, evaluate and localise between African languages and English.', translation),
    ('speech-voice-data', 'Speech & Voice Data', 'ri-mic-line',
     'Record, collect and quality-check the speech data voice AI is built on.', speech),
    ('language-annotation', 'Language Annotation', 'ri-price-tag-3-line',
     'Label text and speech for NLP datasets by following annotation guidelines.', annotation),
    ('ai-data-work', 'AI Data Work', 'ri-robot-line',
     'Evaluate, rank and safety-check AI output in real-world AI data workflows.', ai_data),
    ('linguistics', 'Linguistics', 'ri-book-open-line',
     'The linguistic foundations behind language-data work, applied to Nigerian languages.', linguistics),
    ('language-technology', 'Language Technology', 'ri-code-s-slash-line',
     'Python, NLP, speech and datasets — from beginner to advanced.', language_tech),
    ('quality-assurance', 'Quality Assurance', 'ri-checkbox-multiple-line',
     'Review others\' work, find errors, score quality and measure agreement.', quality),
    ('project-work-skills', 'Project & Work Skills', 'ri-briefcase-4-line',
     'Professional habits remote language-data projects check: guidelines, confidentiality, communication.', work_skills),
]

CATEGORIES = [
    {'slug': slug, 'name': name, 'icon': icon, 'description': desc, 'order': 20 + i}
    for i, (slug, name, icon, desc, _) in enumerate(_CATEGORY_DEFS)
]

# Skill.order is global across the whole catalog (the dashboard and "All Skills" sort by
# it), so ALL skills start at 100 to sit after the existing skills, grouped by category.
SKILLS = []
for _ci, (_slug, _name, _icon, _desc, _module) in enumerate(_CATEGORY_DEFS):
    for _order, _skill in enumerate(_module.SKILLS, 1):
        SKILLS.append({**_skill, 'category': _slug, 'order': 100 + _ci * 20 + _order})

# The first-cohort entry path sits first among the ALL skills (order 99).
BEGINNER_SLUG = BEGINNER['slug']
SKILLS.insert(0, {**BEGINNER, 'category': 'project-work-skills', 'order': 99})

TRACKS = [
    {'slug': 'all-yoruba-language-data-specialist', 'title': 'Yoruba Language Data Specialist', 'icon': 'ri-translate-2', 'color': '#2563eb',
     'tagline': 'Transcribe, translate, annotate and QA Yoruba data.',
     'skills': ['african-language-data-beginner', 'yoruba-transcription', 'yoruba-english-translation', 'text-annotation', 'transcription-qa']},
    {'slug': 'all-igbo-language-data-specialist', 'title': 'Igbo Language Data Specialist', 'icon': 'ri-translate-2', 'color': '#2563eb',
     'tagline': 'Transcribe, translate, annotate and QA Igbo data.',
     'skills': ['african-language-data-beginner', 'igbo-transcription', 'igbo-english-translation', 'sentiment-annotation', 'transcription-qa']},
    {'slug': 'all-hausa-language-data-specialist', 'title': 'Hausa Language Data Specialist', 'icon': 'ri-translate-2', 'color': '#2563eb',
     'tagline': 'Transcribe, translate, annotate and QA Hausa data.',
     'skills': ['african-language-data-beginner', 'hausa-transcription', 'hausa-english-translation', 'named-entity-annotation', 'transcription-qa']},
    {'slug': 'all-pidgin-language-data-specialist', 'title': 'Nigerian Pidgin Language Data Specialist', 'icon': 'ri-translate-2', 'color': '#2563eb',
     'tagline': 'Transcribe, translate, annotate and QA Naija data.',
     'skills': ['african-language-data-beginner', 'nigerian-pidgin-transcription', 'nigerian-pidgin-english-translation', 'intent-classification', 'transcription-qa']},
    {'slug': 'all-ai-data-evaluator', 'title': 'AI Data Evaluator', 'icon': 'ri-robot-line', 'color': '#4f46e5',
     'tagline': 'From annotation to safety evaluation of AI output.',
     'skills': ['african-language-data-beginner', 'ai-data-annotation', 'ai-response-evaluation', 'llm-evaluation', 'human-feedback-for-ai', 'ai-safety-evaluation']},
    {'slug': 'all-language-qa-reviewer', 'title': 'Language QA Reviewer', 'icon': 'ri-checkbox-multiple-line', 'color': '#16a34a',
     'tagline': 'Become the reviewer projects trust.',
     'skills': ['african-language-data-beginner', 'error-identification', 'quality-scoring', 'double-annotation', 'inter-annotator-agreement', 'reviewer-training']},
    {'slug': 'all-nlp-builder', 'title': 'NLP Builder', 'icon': 'ri-code-s-slash-line', 'color': '#1d4ed8',
     'tagline': 'Python for NLP → NLP Fundamentals → Dataset Creation → Corpus Creation → NLP.',
     'skills': ['python-for-nlp', 'nlp-fundamentals', 'dataset-creation', 'corpus-creation', 'natural-language-processing']},
    {'slug': 'all-speech-data-contributor', 'title': 'Speech Data Contributor', 'icon': 'ri-mic-line', 'color': '#7c3aed',
     'tagline': 'Record and validate speech data to dataset standard.',
     'skills': ['african-language-data-beginner', 'voice-recording', 'scripted-speech-recording', 'speech-quality-checking', 'audio-validation']},
    {'slug': 'all-computational-linguist', 'title': 'Computational Linguistics Foundations', 'icon': 'ri-node-tree', 'color': '#0d9488',
     'tagline': 'For Linguistics, English and language students moving into AI.',
     'skills': ['phonetics', 'phonology', 'morphology', 'syntax', 'corpus-linguistics', 'computational-linguistics']},
    {'slug': 'all-professional-data-contributor', 'title': 'Professional Data Contributor', 'icon': 'ri-briefcase-4-line', 'color': '#475569',
     'tagline': 'The professional habits every language-data project checks.',
     'skills': ['following-annotation-guidelines', 'nda-confidentiality', 'data-privacy', 'reporting-issues', 'meeting-project-requirements']},
]


def validate(validate_task_spec=None):
    """Returns a list of human-readable problems with the curriculum (empty = valid).
    Pass services.language_task_service.validate_task_spec to also check every task spec."""
    errors = []
    slugs = [s['slug'] for s in SKILLS]
    for dup in {s for s in slugs if slugs.count(s) > 1}:
        errors.append(f'duplicate skill slug: {dup}')
    for s in SKILLS:
        where = s['slug']
        if s['level'] not in ('beginner', 'intermediate', 'advanced'):
            errors.append(f'{where}: bad level {s["level"]!r}')
        if 'courses' not in s and len(s['lessons']) != 3:
            errors.append(f'{where}: expected 3 lessons')
        if not s['project']['title'].startswith('Practice Project'):
            errors.append(f'{where}: project must be labelled as a Practice Project')
        for lesson in s['lessons']:
            for qq in lesson['quiz']:
                if len(qq['options']) < 2 or not (0 <= qq['correct_index'] < len(qq['options'])):
                    errors.append(f'{where}: bad quiz question {qq["question"][:40]!r}')
        if not any(lesson['quiz'] for lesson in s['lessons']):
            errors.append(f'{where}: no quiz in any lesson')
        for key in ('practice', 'assessment'):
            spec = s[key]['spec']
            if validate_task_spec:
                errors.extend(f'{where} {key}: {e}' for e in validate_task_spec(spec))
        if not (0 < s['assessment']['pass_score'] <= 100):
            errors.append(f'{where}: bad pass_score')
        if not s['project'].get('title'):
            errors.append(f'{where}: project missing title')
    known = set(slugs)
    for t in TRACKS:
        for sk in t['skills']:
            if sk not in known:
                errors.append(f'track {t["slug"]}: unknown skill {sk}')
    return errors
