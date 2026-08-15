"""Seeds the Skills system with one fully-built path (Python Developer) plus a handful
of published-but-empty skills across other categories, so the catalog shows real breadth
from day one. Safe to re-run — it upserts by slug instead of duplicating.

Run with: venv/Scripts/python.exe seed_skills.py
"""
from app import app
from extensions import db
from models import (
    SkillCategory, Skill, LearningPath, LearningPathStep, SkillCourse, CourseModule,
    Lesson, Quiz, Challenge, ProjectTemplate, CareerTrack, CareerTrackStep,
)


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


def run():
    with app.app_context():
        tech, _ = get_or_create(SkillCategory, slug='tech', defaults={
            'name': 'Tech', 'icon': '💻', 'order': 1,
            'description': 'Software development, data, AI, and infrastructure skills.',
        })
        design, _ = get_or_create(SkillCategory, slug='design', defaults={
            'name': 'Design', 'icon': '🎨', 'order': 2,
            'description': 'UI/UX, product, and visual design.',
        })
        business, _ = get_or_create(SkillCategory, slug='business', defaults={
            'name': 'Business', 'icon': '💼', 'order': 3,
            'description': 'Entrepreneurship, marketing, sales, and strategy.',
        })
        creative, _ = get_or_create(SkillCategory, slug='creative', defaults={
            'name': 'Creative', 'icon': '🎬', 'order': 4,
            'description': 'Content, video, writing, and personal brand.',
        })
        career, _ = get_or_create(SkillCategory, slug='career', defaults={
            'name': 'Career', 'icon': '🚀', 'order': 5,
            'description': 'Getting opportunity-ready — CVs, interviews, and remote work.',
        })

        # ============== PYTHON (fully built path) ==============
        python, _ = get_or_create(Skill, slug='python', defaults={
            'category_id': tech.id, 'name': 'Python', 'level': 'beginner', 'icon': '🐍',
            'color': '#3b82f6', 'estimated_hours': 20, 'is_published': True, 'order': 1,
            'tagline': "Build the foundation you need to start developing real software.",
            'description': (
                "Python is the most versatile starting point in software development — used in "
                "web apps, automation, data analysis, and AI. This path takes you from your first "
                "line of code to shipping a real, working project."
            ),
        })
        path, _ = get_or_create(LearningPath, skill_id=python.id, defaults={'title': 'Python Developer Path'})

        course, _ = get_or_create(SkillCourse, skill_id=python.id, slug='python-fundamentals', defaults={
            'title': 'Python Fundamentals', 'level': 'beginner', 'estimated_hours': 6, 'order': 1,
            'is_published': True,
            'description': 'The core building blocks — variables, control flow, functions, and data structures.',
        })

        m1, _ = get_or_create(CourseModule, course_id=course.id, title='Getting Started', defaults={'order': 1})
        l1, created = get_or_create(Lesson, module_id=m1.id, slug='what-is-python', defaults={
            'title': 'What Is Python, and Why Start Here?', 'order': 1, 'duration_minutes': 8, 'is_published': True,
            'content': (
                "<p>Python is a general-purpose programming language known for being readable and "
                "quick to learn — which is exactly why it's a strong first language.</p>"
                "<h2>Where Python is used</h2>"
                "<ul><li>Web backends (Django, Flask — this very platform is built in Flask)</li>"
                "<li>Data analysis and AI/ML</li><li>Automating repetitive tasks</li></ul>"
                "<h2>How this course works</h2>"
                "<p>Each lesson builds on the last. You'll read a short explanation, then a code example. "
                "By the end of this course, you'll be comfortable writing real Python programs — not just "
                "reading about them.</p>"
            ),
        })
        if created:
            quiz, _ = get_or_create(Quiz, lesson_id=l1.id, defaults={'title': 'Quick check'})
            quiz.questions = [{
                'question': 'Which of these is Python commonly used for?',
                'options': ['Web backends', 'Data analysis', 'Automating tasks', 'All of the above'],
                'correct_index': 3,
                'explanation': "Python's versatility is exactly why it's such a strong first language.",
            }]

        l2, _ = get_or_create(Lesson, module_id=m1.id, slug='variables-and-types', defaults={
            'title': 'Variables and Data Types', 'order': 2, 'duration_minutes': 12, 'is_published': True,
            'content': (
                "<p>A variable stores a value so you can use it later.</p>"
                "<pre><code>name = \"Ada\"\nage = 24\nis_student = True</code></pre>"
                "<h2>Core types</h2>"
                "<ul><li><code>str</code> — text, like <code>\"Ada\"</code></li>"
                "<li><code>int</code> / <code>float</code> — whole and decimal numbers</li>"
                "<li><code>bool</code> — <code>True</code> or <code>False</code></li>"
                "<li><code>list</code> — an ordered collection, like <code>[1, 2, 3]</code></li></ul>"
                "<p>Python figures out the type automatically — you never have to declare it.</p>"
            ),
        })

        m2, _ = get_or_create(CourseModule, course_id=course.id, title='Control Flow & Functions', defaults={'order': 2})
        l3, _ = get_or_create(Lesson, module_id=m2.id, slug='if-statements', defaults={
            'title': 'Making Decisions with if/else', 'order': 1, 'duration_minutes': 10, 'is_published': True,
            'content': (
                "<p>Programs need to make decisions. That's what <code>if</code> statements are for.</p>"
                "<pre><code>score = 85\nif score >= 70:\n    print(\"Pass\")\nelse:\n    print(\"Try again\")</code></pre>"
                "<p>Indentation isn't just style in Python — it's how the language knows what belongs "
                "inside the <code>if</code> block.</p>"
            ),
        })
        l4, _ = get_or_create(Lesson, module_id=m2.id, slug='functions', defaults={
            'title': 'Writing Reusable Code with Functions', 'order': 2, 'duration_minutes': 14, 'is_published': True,
            'content': (
                "<p>A function packages up code so you can reuse it without copy-pasting.</p>"
                "<pre><code>def greet(name):\n    return f\"Hello, {name}!\"\n\nprint(greet(\"Ada\"))</code></pre>"
                "<p>Once you start repeating yourself in code, that's usually a sign you need a function.</p>"
            ),
        })

        challenge, _ = get_or_create(Challenge, skill_id=python.id, slug='fizzbuzz', defaults={
            'title': 'Classic: FizzBuzz', 'challenge_type': 'coding', 'difficulty': 'beginner',
            'estimated_minutes': 20, 'order': 1, 'is_published': True,
            'description': 'A classic warm-up that tests if/else and loops.',
            'instructions': (
                "Write a Python program that prints the numbers from 1 to 30.\n\n"
                "But: for multiples of 3, print \"Fizz\" instead of the number. For multiples of 5, "
                "print \"Buzz\". For multiples of both 3 and 5, print \"FizzBuzz\".\n\n"
                "Paste your code (or a link to it) as your submission."
            ),
        })

        project_template, _ = get_or_create(ProjectTemplate, skill_id=python.id, slug='cli-budget-tracker', defaults={
            'title': 'Command-Line Budget Tracker', 'difficulty': 'beginner', 'estimated_hours': 4, 'order': 1,
            'is_published': True,
            'description': (
                "Build a simple command-line app that lets a user log expenses, categorize them, and "
                "see a running total. It's small enough to finish in an afternoon, but it forces you to "
                "combine everything from this course: variables, functions, control flow, and lists."
            ),
        })
        project_template.skills_demonstrated = ['Python', 'Functions', 'Control Flow', 'Data Structures']

        if not path.steps.count():
            db.session.add(LearningPathStep(path_id=path.id, order=1, step_type='course', course_id=course.id,
                                             title='Python Fundamentals', description='Learn the core language.'))
            db.session.add(LearningPathStep(path_id=path.id, order=2, step_type='challenge', challenge_id=challenge.id,
                                             title='Practice: FizzBuzz', description='Put control flow to the test.'))
            db.session.add(LearningPathStep(path_id=path.id, order=3, step_type='project', project_template_id=project_template.id,
                                             title='Build: Budget Tracker', description='Ship your first real program.'))

        # ============== WEB DEVELOPMENT (fully built path) ==============
        webdev, _ = get_or_create(Skill, slug='web-development', defaults={
            'category_id': tech.id, 'name': 'Web Development', 'level': 'beginner', 'icon': '🌐',
            'color': '#06b6d4', 'estimated_hours': 18, 'is_published': True, 'order': 2,
            'tagline': "Learn to build and ship real websites, from your first tag to a live page.",
            'description': (
                "Web development is how you turn an idea into something anyone can open in a browser. "
                "This path starts with HTML and CSS — the two things every website is built from — and "
                "takes you to a real, deployed page of your own."
            ),
        })
        wd_path, _ = get_or_create(LearningPath, skill_id=webdev.id, defaults={'title': 'Web Developer Path'})

        wd_course, _ = get_or_create(SkillCourse, skill_id=webdev.id, slug='web-fundamentals', defaults={
            'title': 'Web Fundamentals', 'level': 'beginner', 'estimated_hours': 5, 'order': 1,
            'is_published': True,
            'description': 'How the web actually works, then HTML structure and CSS styling from scratch.',
        })

        wd_m1, _ = get_or_create(CourseModule, course_id=wd_course.id, title='How the Web Works', defaults={'order': 1})
        wd_l1, created = get_or_create(Lesson, module_id=wd_m1.id, slug='how-the-web-works', defaults={
            'title': 'What Happens When You Open a Website', 'order': 1, 'duration_minutes': 8, 'is_published': True,
            'content': (
                "<p>Every website is really just three things working together: <strong>HTML</strong> "
                "(structure), <strong>CSS</strong> (style), and <strong>JavaScript</strong> (behavior).</p>"
                "<h2>The request</h2>"
                "<p>When you type a web address, your browser asks a server for a file — usually an HTML "
                "file — and the server sends it back. Your browser then reads that file top to bottom and "
                "draws it on your screen.</p>"
                "<h2>Where this course is headed</h2>"
                "<p>You'll write real HTML and CSS starting in the next lesson, then build and deploy an "
                "actual page of your own by the end of this path.</p>"
            ),
        })
        if created:
            quiz, _ = get_or_create(Quiz, lesson_id=wd_l1.id, defaults={'title': 'Quick check'})
            quiz.questions = [{
                'question': 'What does HTML control on a webpage?',
                'options': ['Structure/content', 'Visual styling', 'Interactive behavior', 'Server storage'],
                'correct_index': 0,
                'explanation': 'HTML is the structure — CSS handles styling, JavaScript handles behavior.',
            }]

        wd_m2, _ = get_or_create(CourseModule, course_id=wd_course.id, title='HTML & CSS Basics', defaults={'order': 2})
        wd_l2, _ = get_or_create(Lesson, module_id=wd_m2.id, slug='your-first-html-page', defaults={
            'title': 'Your First HTML Page', 'order': 1, 'duration_minutes': 12, 'is_published': True,
            'content': (
                "<p>HTML is made of <strong>tags</strong> that describe each piece of content.</p>"
                "<pre><code>&lt;h1&gt;Hello, world&lt;/h1&gt;\n&lt;p&gt;This is my first page.&lt;/p&gt;</code></pre>"
                "<h2>Common tags</h2>"
                "<ul><li><code>&lt;h1&gt;</code>–<code>&lt;h6&gt;</code> — headings</li>"
                "<li><code>&lt;p&gt;</code> — paragraphs</li>"
                "<li><code>&lt;a href=\"...\"&gt;</code> — links</li>"
                "<li><code>&lt;img src=\"...\"&gt;</code> — images</li></ul>"
                "<p>Every tag you open, you close — that pairing is what gives HTML its structure.</p>"
            ),
        })
        wd_l3, _ = get_or_create(Lesson, module_id=wd_m2.id, slug='styling-with-css', defaults={
            'title': 'Styling With CSS', 'order': 2, 'duration_minutes': 14, 'is_published': True,
            'content': (
                "<p>CSS says how HTML should look. You target an element, then set properties on it.</p>"
                "<pre><code>h1 {\n  color: #3b82f6;\n  font-size: 2rem;\n}</code></pre>"
                "<h2>Three ways to target elements</h2>"
                "<ul><li>By tag: <code>p { ... }</code></li>"
                "<li>By class: <code>.card { ... }</code> matches <code>class=\"card\"</code></li>"
                "<li>By id: <code>#header { ... }</code> matches <code>id=\"header\"</code></li></ul>"
                "<p>Classes are what you'll reach for most — they're reusable across many elements.</p>"
            ),
        })

        wd_challenge, _ = get_or_create(Challenge, skill_id=webdev.id, slug='build-a-bio-page', defaults={
            'title': 'Build a Personal Bio Page', 'challenge_type': 'coding', 'difficulty': 'beginner',
            'estimated_minutes': 45, 'order': 1, 'is_published': True,
            'description': 'Put your HTML and CSS together into one real page about you.',
            'instructions': (
                "Build a single HTML page with:\n"
                "- A heading with your name\n"
                "- A short paragraph about yourself\n"
                "- At least one image\n"
                "- At least one link (to anything — a social profile, a project, anything)\n"
                "- Some CSS styling (colors, fonts, or spacing) — inline, in a <style> tag, or a separate file\n\n"
                "Paste your HTML (and CSS) as your submission."
            ),
        })

        wd_project_template, _ = get_or_create(ProjectTemplate, skill_id=webdev.id, slug='personal-portfolio-site', defaults={
            'title': 'Personal Portfolio Website', 'difficulty': 'beginner', 'estimated_hours': 6, 'order': 1,
            'is_published': True,
            'description': (
                "Build a small multi-section portfolio page: an intro, a section listing things you've "
                "made or are learning, and a way to contact you. This is the project most students end up "
                "sharing first — treat it like something you'd actually put your name on."
            ),
        })
        wd_project_template.skills_demonstrated = ['HTML', 'CSS', 'Web Development']

        if not wd_path.steps.count():
            db.session.add(LearningPathStep(path_id=wd_path.id, order=1, step_type='course', course_id=wd_course.id,
                                             title='Web Fundamentals', description='HTML and CSS from scratch.'))
            db.session.add(LearningPathStep(path_id=wd_path.id, order=2, step_type='challenge', challenge_id=wd_challenge.id,
                                             title='Practice: Bio Page', description='Put HTML and CSS together.'))
            db.session.add(LearningPathStep(path_id=wd_path.id, order=3, step_type='project', project_template_id=wd_project_template.id,
                                             title='Build: Portfolio Website', description='Ship a real page of your own.'))

        # ============== A FEW MORE SKILLS (breadth, content coming soon) ==============
        get_or_create(Skill, slug='ui-ux-design', defaults={
            'category_id': design.id, 'name': 'UI/UX Design', 'level': 'beginner', 'icon': '🎨',
            'color': '#a855f7', 'estimated_hours': 15, 'is_published': True, 'order': 1,
            'tagline': 'Design products people actually enjoy using.',
            'description': 'Learn how to research, wireframe, and design interfaces that solve real problems.',
        })
        get_or_create(Skill, slug='digital-marketing', defaults={
            'category_id': business.id, 'name': 'Digital Marketing', 'level': 'beginner', 'icon': '📈',
            'color': '#f59e0b', 'estimated_hours': 12, 'is_published': True, 'order': 1,
            'tagline': 'Get products and ideas in front of the right people.',
            'description': 'The fundamentals of reaching an audience — content, social, and basic analytics.',
        })
        get_or_create(Skill, slug='content-creation', defaults={
            'category_id': creative.id, 'name': 'Content Creation', 'level': 'beginner', 'icon': '🎬',
            'color': '#ec4899', 'estimated_hours': 10, 'is_published': True, 'order': 1,
            'tagline': 'Turn what you know into content people want to watch or read.',
            'description': 'Planning, writing, and producing content that holds attention.',
        })
        get_or_create(Skill, slug='cv-interview-prep', defaults={
            'category_id': career.id, 'name': 'CV & Interview Prep', 'level': 'beginner', 'icon': '📄',
            'color': '#22c55e', 'estimated_hours': 5, 'is_published': True, 'order': 1,
            'tagline': 'Get opportunity-ready.',
            'description': 'Build a CV that gets read, and prepare for the interviews that follow.',
        })

        # ============== A CAREER TRACK (chains real, published skills) ==============
        # Only combines skills that actually have real content — no placeholder skills
        # invented just to pad out the track.
        track, _ = get_or_create(CareerTrack, slug='full-stack-foundations', defaults={
            'title': 'Full-Stack Foundations', 'icon': '🧭', 'color': '#3b82f6', 'is_published': True,
            'tagline': 'Learn to build the logic and the interface — backend thinking meets a real website.',
            'description': (
                "A short, focused track for students who want both sides of the picture: how "
                "Python teaches you to think in logic and structure, and how Web Development "
                "turns that into something anyone can open in a browser."
            ),
        })
        if not track.steps.count():
            db.session.add(CareerTrackStep(track_id=track.id, skill_id=python.id, order=1,
                                            note='Start here — the logic every other skill builds on.'))
            db.session.add(CareerTrackStep(track_id=track.id, skill_id=webdev.id, order=2,
                                            note='Now put that logic in front of real users.'))

        db.session.commit()
        print(f"Seeded. Python skill id={python.id}, Web Development skill id={webdev.id}, track id={track.id}")


if __name__ == '__main__':
    run()
