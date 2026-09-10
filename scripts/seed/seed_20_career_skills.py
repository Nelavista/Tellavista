"""Seeds the 20 career-oriented Skill tracks (each a 30-Day Skill Class) required by the
Skills-section expansion. Reads one curriculum data file per skill from
seed_data/career_skills/<slug>.py (each exporting a module-level SKILL dict — see that
package for the schema) and upserts it into the existing Skills data model:

    Skill -> SkillCourse (is_daily_class=True, duration_days=30) -> CourseModule (1 per
    week) -> Lesson (1 per day, day_number 1-30) -> Quiz + Assignment (per lesson)
    Skill -> ProjectTemplate (is_final_project=True, tied to the course, rubric-graded)
    SkillCourse -> GradeScale + GradeWeight (defaults) + Cohort (one active intake)
    Skill -> LearningPath -> LearningPathStep (points at the 30-day course)

No new tables or migrations — everything fits the schema the 30-Day Skill Class system
already ships with. Idempotent: safe to re-run (upserts by slug), matching the pattern
already established by seed_skills.py.

Four of the 20 slugs (web-development, ui-ux-design, digital-marketing, content-creation)
already exist as published Skills with their own earlier, smaller course — this script
attaches the new 30-day course alongside that existing content rather than replacing it,
and refreshes the Skill's name/tagline/description to the broader, more specific 30-skill
scope.

Run with: venv/Scripts/python.exe seed_20_career_skills.py
"""
import importlib
import re

from app import app
from app.extensions import db
from app.models import (
    SkillCategory, Skill, LearningPath, LearningPathStep, SkillCourse, CourseModule,
    Lesson, Quiz, Assignment, ProjectTemplate, GradeScale, GradeWeight,
)
from app.services.daily_class_service import get_or_create_active_cohort
from app.services.gpa_service import DEFAULT_GRADE_SCALE, DEFAULT_GRADE_WEIGHTS

# slug -> (category_slug, icon, color, order_within_category)
SKILL_META = {
    'ai-machine-learning':              ('tech', 'ri-brain-line', '#6366f1', 10),
    'generative-ai-engineering':        ('tech', 'ri-magic-line', '#8b5cf6', 11),
    'software-engineering':             ('tech', 'ri-code-box-line', '#0ea5e9', 12),
    'data-analysis-bi':                 ('tech', 'ri-bar-chart-box-line', '#14b8a6', 13),
    'data-engineering':                 ('tech', 'ri-database-2-line', '#0891b2', 14),
    'web-development':                  ('tech', 'ri-global-line', '#06b6d4', 2),   # existing skill
    'mobile-app-development':           ('tech', 'ri-smartphone-line', '#f97316', 15),
    'cloud-computing-devops':           ('tech', 'ri-cloud-line', '#3b82f6', 16),
    'cybersecurity':                    ('tech', 'ri-shield-keyhole-line', '#ef4444', 17),
    'ui-ux-design':                     ('design', 'ri-palette-line', '#a855f7', 1),  # existing skill
    'digital-marketing':                ('business', 'ri-line-chart-line', '#f59e0b', 1),  # existing skill
    'sales-business-development':       ('business', 'ri-handshake-line', '#22c55e', 2),
    'content-creation':                 ('creative', 'ri-movie-2-line', '#ec4899', 1),  # existing skill
    'video-production-motion-design':   ('creative', 'ri-film-line', '#d946ef', 2),
    'product-management':               ('business', 'ri-flag-line', '#2563eb', 3),
    'project-operations-management':    ('business', 'ri-flow-chart', '#0d9488', 4),
    'fintech-financial-analysis':       ('business', 'ri-money-dollar-circle-line', '#16a34a', 5),
    'advanced-excel-automation':        ('business', 'ri-file-excel-2-line', '#15803d', 6),
    'renewable-energy-sustainability':  ('sustainability', 'ri-leaf-line', '#059669', 1),
    'professional-workplace-skills':    ('career', 'ri-user-star-line', '#7c3aed', 2),
}

EXISTING_SKILL_SLUGS = {'web-development', 'ui-ux-design', 'digital-marketing', 'content-creation'}


def _slugify(text):
    slug = re.sub(r'[^a-z0-9]+', '-', (text or '').lower()).strip('-')
    return slug or 'item'


def _unique_slug(model, base_slug, scope_filters=None):
    slug = base_slug
    n = 2
    while True:
        query = model.query.filter_by(slug=slug)
        if scope_filters:
            query = query.filter_by(**scope_filters)
        if not query.first():
            return slug
        slug = f'{base_slug}-{n}'
        n += 1


def _diversify_quiz(quiz):
    """Several batches of AI-authored quizzes defaulted every question's correct answer to
    the same option position (e.g. always index 1) — mechanically fixed here by rotating
    each question's options by its position in the quiz, rather than re-generating content.
    Deterministic (safe to re-run) and never changes which option's TEXT is correct."""
    result = []
    for qi, q in enumerate(quiz):
        opts = list(q['options'])
        n = len(opts)
        shift = qi % n
        rotated = opts[shift:] + opts[:shift]
        new_correct = (q['correct_index'] - shift) % n
        result.append({**q, 'options': rotated, 'correct_index': new_correct})
    return result


def get_or_create(model, defaults=None, **lookup):
    instance = model.query.filter_by(**lookup).first()
    if instance:
        return instance, False
    params = dict(lookup)
    params.update(defaults or {})
    instance = model(**params)
    db.session.add(instance)
    db.session.flush()
    return instance, True


def load_skill_data(slug):
    module = importlib.import_module(f'seed_data.career_skills.{slug}')
    return module.SKILL


def validate_skill_data(slug, data):
    errors = []
    if data.get('slug') != slug:
        errors.append(f"slug mismatch: file says {data.get('slug')!r}, expected {slug!r}")
    days = data.get('days') or []
    if len(days) != 30:
        errors.append(f"expected exactly 30 days, got {len(days)}")
    day_numbers = [d.get('day_number') for d in days]
    if sorted(day_numbers) != list(range(1, 31)):
        errors.append(f"day_number set is not exactly 1..30: {sorted(day_numbers)}")
    for d in days:
        quiz = d.get('quiz') or []
        if len(quiz) != 3:
            errors.append(f"day {d.get('day_number')}: expected 3 quiz questions, got {len(quiz)}")
        for q in quiz:
            if len(q.get('options') or []) != 4:
                errors.append(f"day {d.get('day_number')}: a quiz question doesn't have 4 options")
            if not (0 <= (q.get('correct_index') if q.get('correct_index') is not None else -1) <= 3):
                errors.append(f"day {d.get('day_number')}: correct_index out of range")
        if not d.get('practical_exercise', {}).get('instructions'):
            errors.append(f"day {d.get('day_number')}: missing practical_exercise instructions")
    rubric = (data.get('final_project') or {}).get('rubric') or []
    total_points = sum(r.get('max_points', 0) for r in rubric)
    if total_points != 100:
        errors.append(f"final_project rubric sums to {total_points}, expected 100")
    return errors


def seed_one_skill(slug, meta, data):
    category_slug, icon, color, order = meta
    category = SkillCategory.query.filter_by(slug=category_slug).first()
    if not category:
        raise RuntimeError(f"category {category_slug!r} does not exist — create it before running")

    is_existing = slug in EXISTING_SKILL_SLUGS
    skill, created = get_or_create(Skill, slug=slug, defaults={
        'category_id': category.id, 'name': data['name'], 'level': 'beginner',
        'icon': icon, 'color': color, 'estimated_hours': data['estimated_hours'],
        'is_published': True, 'order': order,
        'tagline': data['tagline'], 'description': data['description'],
    })
    if not created:
        # Refresh copy to the broader 30-skill-track scope; never touch icon/color/order/
        # category for a skill that already existed (avoid disturbing its established look).
        skill.name = data['name']
        skill.tagline = data['tagline']
        skill.description = data['description']
        skill.estimated_hours = max(skill.estimated_hours or 0, data['estimated_hours'])
        skill.is_published = True

    # ---- 30-day course ----
    course_base_slug = _slugify(data['course_title'])
    existing_course = SkillCourse.query.filter_by(skill_id=skill.id, is_daily_class=True).first()
    if existing_course:
        course = existing_course
        course.title = data['course_title']
        course.description = data['course_description']
        course.duration_days = 30
        course.is_published = True
    else:
        max_order = db.session.query(db.func.max(SkillCourse.order)).filter_by(skill_id=skill.id).scalar() or 0
        course = SkillCourse(
            skill_id=skill.id, title=data['course_title'],
            slug=_unique_slug(SkillCourse, course_base_slug, {'skill_id': skill.id}),
            description=data['course_description'], level='beginner',
            estimated_hours=data['estimated_hours'], order=max_order + 1,
            is_published=True, is_daily_class=True, duration_days=30,
        )
        db.session.add(course)
        db.session.flush()

    days = sorted(data['days'], key=lambda d: d['day_number'])
    modules_by_week = {}
    for day in days:
        week_number = day['week_number']
        if week_number not in modules_by_week:
            module = CourseModule.query.filter_by(course_id=course.id, order=week_number).first()
            if not module:
                module = CourseModule(course_id=course.id, title=f"Week {week_number}: {day['week_title']}", order=week_number)
                db.session.add(module)
                db.session.flush()
            else:
                module.title = f"Week {week_number}: {day['week_title']}"
            modules_by_week[week_number] = module
        module = modules_by_week[week_number]

        content = day['content_html']
        key_concepts = day.get('key_concepts') or []
        if key_concepts:
            content += '<h2>Key Concepts</h2><ul>' + ''.join(f'<li>{kc}</li>' for kc in key_concepts) + '</ul>'

        lesson = Lesson.query.filter_by(module_id=module.id, day_number=day['day_number']).first()
        lesson_title = day['title']
        if not lesson:
            lesson = Lesson(
                module_id=module.id, title=lesson_title,
                slug=_unique_slug(Lesson, _slugify(f"day-{day['day_number']}-{lesson_title}"), {'module_id': module.id}),
                order=day['day_number'], content=content,
                duration_minutes=day['duration_minutes'], is_published=True,
                day_number=day['day_number'], week_number=week_number,
                week_title=day['week_title'], learning_objective=day['learning_objective'],
            )
            db.session.add(lesson)
            db.session.flush()
        else:
            lesson.title = lesson_title
            lesson.content = content
            lesson.duration_minutes = day['duration_minutes']
            lesson.week_title = day['week_title']
            lesson.learning_objective = day['learning_objective']
            lesson.is_published = True

        resources = day.get('resources') or []
        if resources:
            lesson.resources = resources

        quiz = Quiz.query.filter_by(lesson_id=lesson.id).first()
        if not quiz:
            quiz = Quiz(lesson_id=lesson.id, title='Quick check')
            db.session.add(quiz)
        quiz.questions = _diversify_quiz(day['quiz'])

        assignment = Assignment.query.filter_by(lesson_id=lesson.id).first()
        exercise = day['practical_exercise']
        if not assignment:
            assignment = Assignment(lesson_id=lesson.id, title=exercise['title'], instructions=exercise['instructions'], due_offset_hours=48)
            db.session.add(assignment)
        else:
            assignment.title = exercise['title']
            assignment.instructions = exercise['instructions']

    # ---- final project ----
    fp = data['final_project']
    template = ProjectTemplate.query.filter_by(course_id=course.id, is_final_project=True).first()
    if not template:
        template = ProjectTemplate(
            skill_id=skill.id, course_id=course.id, is_final_project=True,
            title=fp['title'], slug=_unique_slug(ProjectTemplate, _slugify(fp['title']), {'skill_id': skill.id}),
            description=fp['description'], difficulty=fp['difficulty'],
            estimated_hours=fp['estimated_hours'], is_published=True, order=1,
        )
        db.session.add(template)
        db.session.flush()
    else:
        template.title = fp['title']
        template.description = fp['description']
        template.difficulty = fp['difficulty']
        template.estimated_hours = fp['estimated_hours']
        template.is_published = True
    template.skills_demonstrated = fp['skills_demonstrated']
    template.rubric = fp['rubric']

    # ---- grading defaults ----
    if not course.grade_scale.count():
        for row in DEFAULT_GRADE_SCALE:
            db.session.add(GradeScale(course_id=course.id, **row))
    existing_weights = {w.component for w in course.grade_weights}
    for component, pct in DEFAULT_GRADE_WEIGHTS.items():
        if component not in existing_weights:
            db.session.add(GradeWeight(course_id=course.id, component=component, weight_pct=pct))

    db.session.flush()
    get_or_create_active_cohort(course)

    # ---- learning path ----
    path = skill.path
    if not path:
        path = LearningPath(skill_id=skill.id, title=f"{skill.name} Path")
        db.session.add(path)
        db.session.flush()
    has_course_step = any(s.course_id == course.id for s in path.steps)
    if not has_course_step:
        max_order = db.session.query(db.func.max(LearningPathStep.order)).filter_by(path_id=path.id).scalar() or 0
        db.session.add(LearningPathStep(
            path_id=path.id, order=max_order + 1, step_type='course', course_id=course.id,
            title=course.title, description='Your 30-day, job-ready curriculum for this skill.',
        ))

    return skill, course


def run():
    with app.app_context():
        sustainability, _ = get_or_create(SkillCategory, slug='sustainability', defaults={
            'name': 'Sustainability', 'icon': 'ri-leaf-line', 'order': 6,
            'description': 'Renewable energy, climate, and sustainable-impact skills.',
        })
        db.session.commit()

        all_errors = {}
        for slug in SKILL_META:
            data = load_skill_data(slug)
            errors = validate_skill_data(slug, data)
            if errors:
                all_errors[slug] = errors

        if all_errors:
            print("VALIDATION FAILED — fix these before seeding:")
            for slug, errors in all_errors.items():
                print(f"\n  {slug}:")
                for e in errors:
                    print(f"    - {e}")
            return

        results = []
        for slug, meta in SKILL_META.items():
            data = load_skill_data(slug)
            skill, course = seed_one_skill(slug, meta, data)
            results.append((skill.slug, skill.id, course.id))
            print(f"seeded: {skill.slug} (skill_id={skill.id}, course_id={course.id})")

        db.session.commit()
        print(f"\nDone. Seeded {len(results)} skills.")


if __name__ == '__main__':
    run()
