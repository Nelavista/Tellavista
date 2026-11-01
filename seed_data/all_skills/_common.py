"""Builders shared by every African Languages Lab (ALL) skill file.

Each category module calls skill(...) once per skill, which returns the SKILL dict the
seeder (scripts/seed/seed_all_skills.py) upserts as:
    Skill -> SkillCourse "<name> Essentials" -> 2 CourseModules -> 3 Lessons (+ Quizzes)
          -> practice Challenge (scored task) -> assessment Challenge (must pass)
          -> ProjectTemplate (writer workspace, AI quality review)
          -> LearningPath: course -> practice -> assessment -> project
Keeping the shape in one place means every ALL skill gets the same, complete
Learn -> Practice -> Assessment -> Project -> Verify structure.
"""
from html import escape


def q(question, correct, *wrong, why=''):
    """A quiz question with the correct option first; the seeder rotates option order so
    the right answer isn't always in the same position."""
    return {'question': question, 'options': [correct, *wrong], 'correct_index': 0, 'explanation': why}


def _ul(items):
    return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


def lesson(title, objective, paragraphs, points=None, example=None, quiz=None, minutes=12):
    html = ''.join(f'<p>{p}</p>' for p in paragraphs)
    if points:
        html += '<h2>Key points</h2>' + _ul(points)
    if example:
        html += f'<h2>Example</h2><pre>{escape(example)}</pre>'
    return {'title': title, 'objective': objective, 'content': html, 'quiz': quiz or [], 'minutes': minutes}


def workflow_lesson(name, steps, mistakes, quality_bar, minutes=10):
    html = (f'<p>This is how {name} work is actually done on a real project, step by step. '
            'Follow the same order in the practice task and the assessment.</p>'
            '<h2>Workflow</h2><ol>' + ''.join(f'<li>{s}</li>' for s in steps) + '</ol>'
            '<h2>Common mistakes reviewers flag</h2>' + _ul(mistakes) +
            f'<h2>What "good" looks like</h2><p>{quality_bar}</p>')
    return {'title': f'Doing {name} on a real project', 'objective': f'Apply a reliable workflow for {name}.',
            'content': html, 'quiz': [], 'minutes': minutes}


def choice_items(field, label, options, rows, context_key=None):
    """Labeling items that each ask one multiple-choice question.
    rows: [(text, expected)] or [(text, expected, context)]."""
    items = []
    for i, row in enumerate(rows, 1):
        text, expected = row[0], row[1]
        item = {'id': f'{field}{i}', 'text': text,
                'fields': [{'name': field, 'label': label, 'type': 'choice', 'options': options, 'expected': expected}]}
        if len(row) > 2 and row[2]:
            item['context'] = row[2]
        items.append(item)
    return items


def number_item(iid, text, label, expected, tolerance=0, context=None):
    item = {'id': iid, 'text': text,
            'fields': [{'name': 'value', 'label': label, 'type': 'number', 'expected': expected, 'tolerance': tolerance}]}
    if context:
        item['context'] = context
    return item


def labeling(items, guidelines, brief=None, report=None, ai_feedback=False):
    spec = {'kind': 'labeling', 'items': items, 'guidelines': guidelines}
    if brief:
        spec['brief'] = brief
    if report:
        spec['report'] = report
    if ai_feedback:
        spec['ai_feedback'] = True
    return spec


def task(title, description, spec, minutes=25, instructions=None):
    return {'title': title, 'description': description, 'spec': spec, 'minutes': minutes,
            'instructions': instructions or description}


def project(title, brief, deliverables, criteria, skills_demonstrated, difficulty='beginner', hours=3, workspace='writer'):
    """workspace: which existing StudentProject workspace the project opens with --
    'writer' (document) for most language work, 'developer' for code projects.

    Every ALL project is a Nelavista simulation unless it is genuinely connected to an
    external project -- labelled as such in its title and in the first line of its brief."""
    if not title.startswith('Practice Project'):
        title = f'Practice Project: {title}'
    if not brief.startswith('Simulation'):
        brief = ('Simulation — a Nelavista practice project modelled on real language-data work. It is not an '
                 'African Languages Lab project or paid client work.\n\n' + brief)
    description = (
        f'{brief}\n\nDeliverables:\n' + '\n'.join(f'- {d}' for d in deliverables) +
        '\n\nWhat the quality review looks for:\n' + '\n'.join(f'- {c}' for c in criteria) +
        '\n\nWrite your work in the project document, then use "Request Review". '
        'A review score of 60% or more counts toward verifying this skill.'
    )
    return {'title': title, 'description': description, 'skills_demonstrated': skills_demonstrated,
            'difficulty': difficulty, 'hours': hours, 'workspace': workspace}


def skill(slug, name, *, level, tags, icon, color, tagline, description, foundation, core, workflow,
          practice, assessment, project_brief, language=None, hours=6, pass_score=70):
    return {
        'slug': slug, 'name': name, 'level': level, 'language': language, 'tags': tags,
        'icon': icon, 'color': color, 'tagline': tagline, 'description': description,
        'estimated_hours': hours,
        'lessons': [foundation, core, workflow],
        'practice': practice, 'assessment': {**assessment, 'pass_score': pass_score},
        'project': project_brief,
    }
