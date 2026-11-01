"""Seeds the African Languages Lab (ALL) skills into the existing Skills data model —
no parallel system. Reads seed_data/all_skills (see that package) and upserts:

    SkillCategory (program='all') -> Skill (language, tags)
      -> SkillCourse "<name> Essentials" -> CourseModule x2 -> Lesson x3 (+ Quiz)
      -> Challenge 'practice'   (scored task, Challenge.task_spec)
      -> Challenge 'assessment' (scored task, is_assessment=True, pass_score)
      -> ProjectTemplate (writer/developer workspace, reviewed via "Request Review")
      -> LearningPath: course -> practice -> assessment -> project
    CareerTrack (multi-skill ALL tracks) -> CareerTrackStep

Idempotent: upserts by slug and can be re-run after editing the curriculum. Lesson,
challenge and template rows are updated in place (so existing student progress and
submissions keep pointing at the same rows); path and track steps are rebuilt. It never
touches a skill whose slug already belongs to a non-ALL category.

Run (after `flask db upgrade`):
    python -m scripts.seed.seed_all_skills
Validate the curriculum without touching any database:
    python -m scripts.seed.seed_all_skills --check
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def _slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', (text or '').lower()).strip('-') or 'item'


def _rotate_quiz(quiz):
    """Curriculum quizzes list the correct option first; rotate each question's options by
    its position so the answer isn't always option A. Deterministic, so re-runs are stable."""
    result = []
    for qi, item in enumerate(quiz):
        opts = list(item['options'])
        shift = (qi + 1) % len(opts)
        rotated = opts[shift:] + opts[:shift]
        result.append({**item, 'options': rotated, 'correct_index': (item['correct_index'] - shift) % len(opts)})
    return result


def check():
    import seed_data.all_skills as curriculum
    from app.services.language_task_service import validate_task_spec
    errors = curriculum.validate(validate_task_spec)
    for e in errors:
        print(f'  - {e}')
    print(f'{len(curriculum.SKILLS)} skills, {len(curriculum.CATEGORIES)} categories, {len(curriculum.TRACKS)} tracks: '
          + ('INVALID' if errors else 'OK'))
    return not errors


def seed(db_session=None, verbose=True, only=None):
    """Upserts everything (or just the skill slugs in `only`). Must run inside an app
    context. Returns {'skills': n, ...}."""
    import seed_data.all_skills as curriculum
    from app.extensions import db
    from app.models import (
        SkillCategory, Skill, SkillCourse, CourseModule, Lesson, Quiz, Challenge, ProjectTemplate,
        LearningPath, LearningPathStep, CareerTrack, CareerTrackStep,
    )
    from app.services.language_task_service import validate_task_spec

    errors = curriculum.validate(validate_task_spec)
    if errors:
        raise RuntimeError('Curriculum is invalid:\n' + '\n'.join(errors))

    session = db_session or db.session
    log = print if verbose else (lambda *a, **k: None)

    categories = {}
    for c in curriculum.CATEGORIES:
        cat = SkillCategory.query.filter_by(slug=c['slug']).first()
        if not cat:
            cat = SkillCategory(slug=c['slug'])
            session.add(cat)
        cat.name, cat.icon, cat.description, cat.order = c['name'], c['icon'], c['description'], c['order']
        cat.program, cat.is_active = curriculum.PROGRAM, True
        session.flush()
        categories[c['slug']] = cat

    seeded = skipped = 0
    for data in curriculum.SKILLS:
        if only is not None and data['slug'] not in only:
            continue
        category = categories[data['category']]
        skill = Skill.query.filter_by(slug=data['slug']).first()
        if skill and skill.category_id not in {c.id for c in categories.values()}:
            log(f"skip: {data['slug']} already exists outside the ALL categories")
            skipped += 1
            continue
        if not skill:
            skill = Skill(slug=data['slug'], category_id=category.id, name=data['name'])
            session.add(skill)
        skill.category_id = category.id
        skill.name, skill.tagline, skill.description = data['name'], data['tagline'], data['description']
        skill.level, skill.icon, skill.color = data['level'], data['icon'], data['color']
        skill.estimated_hours, skill.order, skill.is_published = data['estimated_hours'], data['order'], True
        skill.language = data.get('language')
        skill.tags = data['tags']
        session.flush()

        # ---- courses -> modules -> lessons (+ quiz) ----
        # Most skills have one "<name> Essentials" course (Foundations + Doing the work);
        # a skill may instead define 'courses' (the beginner path's seven short courses),
        # each becoming its own SkillCourse and its own LearningPath step.
        if data.get('courses'):
            course_plans = [{'slug': _slugify(c['title']), 'title': c['title'], 'modules': [(c['title'], c['lessons'])]}
                            for c in data['courses']]
        else:
            course_plans = [{'slug': f"{data['slug']}-essentials", 'title': f"{data['name']} Essentials",
                             'modules': [('Foundations', data['lessons'][:2]), ('Doing the work', data['lessons'][2:])]}]
        courses = []
        for c_index, plan in enumerate(course_plans, 1):
            course = SkillCourse.query.filter_by(skill_id=skill.id, slug=plan['slug']).first()
            if not course:
                course = SkillCourse(skill_id=skill.id, slug=plan['slug'], title=plan['title'])
                session.add(course)
            course.title = plan['title']
            course.description = data['description'] if len(course_plans) == 1 else f"Step {c_index} of the {data['name']} path."
            course.level, course.estimated_hours, course.order, course.is_published = data['level'], data['estimated_hours'], c_index, True
            session.flush()
            courses.append(course)

            lesson_order = 0
            for m_order, (m_title, lessons) in enumerate(plan['modules'], 1):
                module = CourseModule.query.filter_by(course_id=course.id, order=m_order).first()
                if not module:
                    module = CourseModule(course_id=course.id, order=m_order, title=m_title)
                    session.add(module)
                module.title = m_title
                session.flush()
                for ld in lessons:
                    lesson_order += 1
                    lesson_slug = _slugify(ld['title'])
                    lesson = Lesson.query.filter_by(module_id=module.id, slug=lesson_slug).first()
                    if not lesson:
                        lesson = Lesson(module_id=module.id, slug=lesson_slug, title=ld['title'])
                        session.add(lesson)
                    lesson.title, lesson.content, lesson.order = ld['title'], ld['content'], lesson_order
                    lesson.duration_minutes, lesson.learning_objective, lesson.is_published = ld['minutes'], ld['objective'], True
                    session.flush()
                    if ld['quiz']:
                        quiz = Quiz.query.filter_by(lesson_id=lesson.id).first()
                        if not quiz:
                            quiz = Quiz(lesson_id=lesson.id, title='Quick check')
                            session.add(quiz)
                        quiz.questions = _rotate_quiz(ld['quiz'])

        # ---- practice + assessment challenges ----
        challenges = {}
        for c_order, key in enumerate(('practice', 'assessment'), 1):
            td = data[key]
            ch = Challenge.query.filter_by(skill_id=skill.id, slug=key).first()
            if not ch:
                ch = Challenge(skill_id=skill.id, slug=key, title=td['title'])
                session.add(ch)
            ch.title, ch.description, ch.instructions = td['title'], td['description'], td['instructions']
            ch.challenge_type = 'assessment' if key == 'assessment' else 'practical'
            ch.difficulty, ch.estimated_minutes, ch.order, ch.is_published = data['level'], td['minutes'], c_order, True
            # Practice data is prepared by Nelavista, not drawn from a client project.
            ch.task_spec = {**td['spec'], 'simulation': True}
            ch.is_assessment = key == 'assessment'
            ch.pass_score = td['pass_score'] if key == 'assessment' else None
            session.flush()
            challenges[key] = ch

        # ---- practical project ----
        pd = data['project']
        template_slug = f"{data['slug']}-project"
        template = ProjectTemplate.query.filter_by(skill_id=skill.id, slug=template_slug).first()
        if not template:
            template = ProjectTemplate(skill_id=skill.id, slug=template_slug, title=pd['title'])
            session.add(template)
        template.title, template.description = pd['title'], pd['description']
        template.difficulty, template.estimated_hours, template.order = pd['difficulty'], pd['hours'], 1
        template.is_published, template.is_final_project = True, False
        template.workspace_type = pd.get('workspace') or 'writer'
        template.skills_demonstrated = pd['skills_demonstrated']
        session.flush()

        # ---- learning path (rebuilt so it always mirrors the curriculum) ----
        path = skill.path
        if not path:
            path = LearningPath(skill_id=skill.id, title=f"{data['name']} Path")
            session.add(path)
            session.flush()
        path.title = f"{data['name']} Path"
        path.description = 'Learn → practise → pass the assessment → complete a reviewed project → verified.'
        for step in path.steps.all():
            session.delete(step)
        session.flush()
        steps = [('course', c.title if len(courses) == 1 else f'{i}. {c.title}', 'Lessons with a quick check on each.',
                  {'course_id': c.id}) for i, c in enumerate(courses, 1)]
        n = len(courses)
        if n > 1:  # numbered path, e.g. the beginner path's steps 8-10
            titles = (f"{n + 1}. {challenges['practice'].title}", f"{n + 2}. {challenges['assessment'].title}",
                      f"{n + 3}. Final Skill Verification — {template.title}")
        else:
            titles = (f"Practice: {challenges['practice'].title}", f"Assessment: {challenges['assessment'].title}", template.title)
        steps += [
            ('challenge', titles[0], 'Scored practical task — answers shown after you submit.',
             {'challenge_id': challenges['practice'].id}),
            ('challenge', titles[1], f"Pass mark {challenges['assessment'].pass_score}%.",
             {'challenge_id': challenges['assessment'].id}),
            ('project', titles[2], 'Complete it, then use "Request Review" — a quality review of 60%+ verifies the skill.',
             {'project_template_id': template.id}),
        ]
        for order, (step_type, title, desc, fk) in enumerate(steps, 1):
            session.add(LearningPathStep(path_id=path.id, order=order, step_type=step_type, title=title[:150], description=desc, **fk))
        seeded += 1
        log(f"seeded: {skill.slug}")

    session.flush()
    for order, t in enumerate(curriculum.TRACKS, 1):
        track = CareerTrack.query.filter_by(slug=t['slug']).first()
        if not track:
            track = CareerTrack(slug=t['slug'], title=t['title'])
            session.add(track)
        track.title, track.tagline, track.icon, track.color = t['title'], t['tagline'], t['icon'], t['color']
        track.description = t['tagline']
        track.is_published, track.order = True, 100 + order
        session.flush()
        for step in track.steps.all():
            session.delete(step)
        session.flush()
        for s_order, skill_slug in enumerate(t['skills'], 1):
            skill = Skill.query.filter_by(slug=skill_slug).first()
            if skill:
                session.add(CareerTrackStep(track_id=track.id, skill_id=skill.id, order=s_order))

    session.commit()
    log(f'\nDone. {seeded} skills seeded, {skipped} skipped, {len(curriculum.TRACKS)} tracks.')
    return {'skills': seeded, 'skipped': skipped, 'tracks': len(curriculum.TRACKS)}


if __name__ == '__main__':
    if '--check' in sys.argv:
        os.environ.setdefault('SKIP_DB_INIT', '1')
        sys.exit(0 if check() else 1)
    from app import app
    with app.app_context():
        seed()
