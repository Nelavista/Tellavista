"""Seed data for the Software Engineering 30-Day Skill Class."""

SKILL = {
    "slug": "software-engineering",
    "name": "Software Engineering",
    "tagline": "Learn how professional teams design, build, test, and ship real software, not just write code that runs once.",
    "description": "Software engineering is the discipline of building software that is reliable, maintainable, and safe to change, using practices like version control, automated testing, and documentation that separate professional developers from hobbyist coders. For a Nigerian student aiming at a junior developer role, a backend internship, or freelance contract work, these practices are exactly what technical interviews and code reviews test for. This track takes you from writing your first structured program to designing, building, testing, and deploying a complete backend application the way a real engineering team would.",
    "level": "beginner",
    "estimated_hours": 62,
    "course_title": "30-Day Software Engineering Career Track",
    "course_description": "After 30 days you will be able to design a backend application's architecture, write clean and tested Python code, manage a codebase with Git, build and document a REST API backed by a real database, and deploy a working application using basic CI practices.",
    "final_project": {
        "title": "Design, Build, Test, and Deploy a Production-Style Backend Application",
        "description": "Design, build, test, and deploy a real backend or full-stack application, such as a student attendance tracker, a campus lost-and-found system, a small inventory manager, or a bookings API for a local business. The project must use Git with a clean commit history, include automated tests covering the core logic, run a basic CI pipeline that executes those tests on every push, and ship a README documenting the architecture, setup steps, and API endpoints. The application must be deployed somewhere publicly reachable, such as Render, Railway, or Fly.io, with a working database connection. This is the exact combination of skills a hiring manager checks for when deciding whether a junior candidate can be trusted with real production code.",
        "difficulty": "advanced",
        "estimated_hours": 14,
        "skills_demonstrated": ["system design", "REST API development", "automated testing", "Git workflow", "CI basics", "database design", "technical documentation", "deployment"],
        "rubric": [
            {"name": "Architecture and code quality", "max_points": 30},
            {"name": "Automated tests and CI pipeline", "max_points": 25},
            {"name": "API functionality and database design", "max_points": 25},
            {"name": "Deployment, Git history, and documentation", "max_points": 20}
        ]
    },
    "days": [
        {
            "day_number": 1,
            "week_number": 1,
            "week_title": "Thinking Like an Engineer",
            "title": "What Software Engineers Actually Do on the Job",
            "learning_objective": "By the end of this class, you will be able to describe the full lifecycle of a professional software project from requirements to maintenance.",
            "duration_minutes": 20,
            "content_html": """<p>Writing code that runs on your machine once is not software engineering. Software engineering is the discipline of building software that keeps working correctly as requirements change, as other people touch the code, and as the number of users grows. This distinction is exactly what separates someone who can follow a coding tutorial from someone a company will actually hire and trust with production systems.</p><h2>The Software Development Lifecycle</h2><p>A real project moves through stages: gathering requirements from stakeholders, designing the system's structure, implementing it in code, testing it before release, deploying it somewhere users can reach it, and maintaining it as bugs surface and needs change. Skipping design or testing to \"just start coding\" is the most common mistake beginners make, and it is why their projects become impossible to change later.</p><pre><code>Requirements -> Design -> Implementation -> Testing -> Deployment -> Maintenance</code></pre><h2>Why This Track Is Structured This Way</h2><p>Over the next 30 days you will practice every one of these stages, not just the implementation step most tutorials focus on. By day 30 you will design, build, test, and deploy a real backend application, following the same lifecycle a junior developer follows in their first job. Nigerian tech employers increasingly ask interview questions specifically about this lifecycle, because it signals whether a candidate can operate on a team, not just solve isolated coding puzzles.</p>""",
            "key_concepts": ["software development lifecycle", "requirements gathering", "system design", "testing and maintenance"],
            "practical_exercise": {
                "title": "Map a Lifecycle to a Real App",
                "instructions": "Pick an app you use daily (e.g. a banking app or food delivery app) and write a half-page document listing one concrete example of what each lifecycle stage (requirements, design, implementation, testing, deployment, maintenance) might have looked like for that app's login feature. Submit the document as a short text file."
            },
            "quiz": [
                {"question": "What mainly separates professional software engineering from writing a script that runs once?", "options": ["Using a faster programming language", "Building software that stays correct and maintainable as it changes and grows", "Writing more lines of code", "Using more advanced hardware"], "correct_index": 1, "explanation": "Software engineering focuses on building maintainable, reliable systems that survive change, not just code that works once."},
                {"question": "Which stage of the software development lifecycle comes immediately before implementation?", "options": ["Deployment", "Maintenance", "Design", "Testing"], "correct_index": 2, "explanation": "Design happens after requirements are gathered and before code is implemented, defining the system's structure."},
                {"question": "Why do many beginner projects become hard to change later?", "options": ["They use too many comments", "They skip design and testing and jump straight to coding", "They are written in Python", "They are deployed too early"], "correct_index": 1, "explanation": "Skipping design and testing leads to unstructured code that is difficult to safely modify as requirements evolve."}
            ],
            "resources": [
                {"label": "MDN: Understanding Client-Side Web Development Tools", "url": "https://developer.mozilla.org/en-US/docs/Learn"}
            ]
        },
        {
            "day_number": 2,
            "week_number": 1,
            "week_title": "Thinking Like an Engineer",
            "title": "Setting Up a Professional Development Environment",
            "learning_objective": "By the end of this class, you will be able to set up a code editor, terminal, and Python environment configured the way professional developers work.",
            "duration_minutes": 25,
            "content_html": """<p>Every professional developer works inside the same basic toolkit: a code editor, a terminal, and a properly isolated language environment. Setting this up correctly on day one avoids the broken-dependency headaches that waste beginners' time for weeks, and it is the first thing a technical mentor checks when reviewing a new hire's setup.</p><h2>Editor, Terminal, and Virtual Environments</h2><p>Install VS Code and get comfortable with its integrated terminal. For Python projects, always work inside a virtual environment so each project's dependencies stay isolated from your system and from other projects.</p><pre><code>python -m venv venv
source venv/bin/activate
pip install requests</code></pre><h2>Why Isolation Matters</h2><p>Without virtual environments, installing one project's dependencies can silently break another project on the same machine, which is a real problem professional teams avoid by isolating every project. Getting into this habit now means your future projects, including your day-30 final project, will run reliably on any machine, including a grader's or an employer's.</p>""",
            "key_concepts": ["code editor setup", "terminal basics", "virtual environments", "dependency isolation"],
            "practical_exercise": {
                "title": "Create Your First Isolated Project",
                "instructions": "Create a project folder, set up a Python virtual environment inside it, activate it, and install the requests package. Write a one-line Python script that imports requests and prints its version. Submit a screenshot of your terminal showing the environment activated and the script's output."
            },
            "quiz": [
                {"question": "What is the main purpose of a Python virtual environment?", "options": ["To make code run faster", "To isolate a project's dependencies from the system and other projects", "To connect to a database", "To automatically write tests"], "correct_index": 1, "explanation": "Virtual environments isolate each project's installed packages, preventing conflicts between projects on the same machine."},
                {"question": "Which command activates a virtual environment on most Unix-based systems?", "options": ["python -m venv venv", "pip install venv", "source venv/bin/activate", "venv --start"], "correct_index": 2, "explanation": "After creating a virtual environment with venv, it must be activated using the activate script before installing packages into it."},
                {"question": "Why should every project use its own virtual environment instead of a shared global setup?", "options": ["It is required by Python's license", "It prevents one project's dependency versions from breaking another project", "It makes the code open source automatically", "It is only needed for web projects"], "correct_index": 1, "explanation": "Isolated environments prevent version conflicts between projects that require different versions of the same package."}
            ],
            "resources": [
                {"label": "Python venv Documentation", "url": "https://docs.python.org/3/library/venv.html"}
            ]
        },
        {
            "day_number": 3,
            "week_number": 1,
            "week_title": "Thinking Like an Engineer",
            "title": "Version Control Fundamentals: Git Init, Add, Commit",
            "learning_objective": "By the end of this class, you will be able to initialize a Git repository and record a clean history of changes using commits.",
            "duration_minutes": 25,
            "content_html": """<p>Version control is non-negotiable in professional software engineering. Every serious company uses Git to track exactly who changed what and why, and being unable to use Git confidently is an instant red flag in a technical interview.</p><h2>The Core Git Workflow</h2><p>Git tracks changes in three stages: your working directory, the staging area, and the committed history. You add changes to staging, then commit them with a message describing what changed and why.</p><pre><code>git init
git add app.py
git commit -m "Add initial Flask app skeleton"
git log --oneline</code></pre><h2>Writing Commits That Matter</h2><p>A good commit message describes the intent of a change, not just what files changed, for example \"Fix off-by-one error in pagination\" rather than \"update code.\" Engineering teams read commit history to understand why a bug was introduced or when a feature was added, so a clean, descriptive history is a skill graders and employers explicitly look for in your final project's Git log.</p>""",
            "key_concepts": ["git init", "staging area", "commits", "commit messages", "git log"],
            "practical_exercise": {
                "title": "Build a Clean Commit History",
                "instructions": "Create a new folder, initialize a Git repository, and make three separate commits, each adding one small piece of a simple Python script (e.g. one commit for a function definition, one for adding a print statement, one for a comment/docstring). Each commit message must describe the change in under 10 words. Submit the output of git log --oneline."
            },
            "quiz": [
                {"question": "What does 'git add' do?", "options": ["Permanently deletes a file", "Stages a change so it will be included in the next commit", "Uploads code to GitHub", "Creates a new branch"], "correct_index": 1, "explanation": "git add moves changes into the staging area, marking them to be included in the next commit."},
                {"question": "Why do engineering teams care about commit message quality?", "options": ["Longer messages make the repository larger and more valuable", "Clear messages help others understand why a change was made when reviewing history later", "Git requires a minimum message length", "Commit messages affect code execution speed"], "correct_index": 1, "explanation": "Descriptive commit messages make a project's history useful for debugging and understanding past decisions."},
                {"question": "Which command shows a compact history of commits?", "options": ["git status", "git diff", "git log --oneline", "git branch"], "correct_index": 2, "explanation": "git log --oneline displays a condensed, one-line-per-commit view of the repository's history."}
            ],
            "resources": [
                {"label": "Git Documentation", "url": "https://git-scm.com/doc"},
                {"label": "GitHub Docs", "url": "https://docs.github.com/"}
            ]
        },
        {
            "day_number": 4,
            "week_number": 1,
            "week_title": "Thinking Like an Engineer",
            "title": "Branching and Collaborating with Git and GitHub",
            "learning_objective": "By the end of this class, you will be able to create branches, open a pull request, and merge changes on GitHub.",
            "duration_minutes": 30,
            "content_html": """<p>Real engineering teams almost never write code directly on the main branch. They use feature branches and pull requests so changes can be reviewed before they reach production, and this workflow is exactly what you will be expected to follow from your first day at any engineering job or open-source contribution.</p><h2>Branch, Push, Pull Request</h2><p>A branch is an isolated line of development. You create a branch for a feature or fix, commit your work there, push it to GitHub, and open a pull request (PR) so someone (or you, reviewing your own work) can check the changes before merging into main.</p><pre><code>git checkout -b add-login-endpoint
git push -u origin add-login-endpoint
# then open a Pull Request on GitHub and merge after review</code></pre><h2>Why Branching Protects Real Projects</h2><p>Working on main directly means a half-finished or broken feature can break the whole project for everyone. Branches let multiple features be developed in parallel without interfering, and pull requests create a review checkpoint that catches bugs before they reach users, exactly the safety net production systems depend on.</p>""",
            "key_concepts": ["Git branches", "pull requests", "code review", "merging", "main branch protection"],
            "practical_exercise": {
                "title": "Create a Branch and Open a Pull Request",
                "instructions": "In a GitHub repository you own, create a new branch, add a small change (such as a new function in a Python file), push the branch, and open a pull request describing the change. Merge the pull request into main. Submit the URL of the merged pull request."
            },
            "quiz": [
                {"question": 'What is the main risk of committing directly to the main branch on a real project?', "options": ['A half-finished or broken change can affect everyone immediately', 'It uses more disk space', 'It disables Git entirely', 'It requires a paid GitHub plan'], "correct_index": 0, "explanation": 'Working directly on main means unreviewed, possibly broken changes go straight into the branch everyone else builds from.'},
                {"question": 'What is the purpose of a pull request?', "options": ['To delete a branch permanently', 'To download a repository', 'To request that proposed changes on a branch be reviewed before merging into main', 'To install project dependencies'], "correct_index": 2, "explanation": "A pull request proposes merging one branch's changes into another and gives a checkpoint for review before that happens."},
                {"question": 'Which command creates and switches to a new branch in one step?', "options": ['git branch new-feature', 'git merge new-feature', 'git push new-feature', 'git checkout -b new-feature'], "correct_index": 3, "explanation": 'git checkout -b creates a new branch and switches to it immediately, combining both actions.'}
            ],
            "resources": [
                {"label": "GitHub Docs: About Pull Requests", "url": "https://docs.github.com/"}
            ]
        },
        {
            "day_number": 5,
            "week_number": 1,
            "week_title": "Thinking Like an Engineer",
            "title": "Writing Clean, Readable Python Functions",
            "learning_objective": "By the end of this class, you will be able to write small, well-named Python functions that follow clean-code principles.",
            "duration_minutes": 25,
            "content_html": """<p>Code is read far more often than it is written. A function that works but is confusing to read will slow down every teammate who touches it later, and code reviews at real companies frequently reject working code purely for being unclear.</p><h2>Small Functions, Clear Names</h2><p>Each function should do one thing and its name should describe exactly what that thing is. Compare a vague function to a clear one.</p><pre><code># Unclear
def calc(x, y):
    return x * y * 0.075

# Clear
def calculate_vat(price, quantity):
    VAT_RATE = 0.075
    return price * quantity * VAT_RATE</code></pre><h2>Avoiding Duplication and Magic Numbers</h2><p>Repeating the same logic in multiple places, or using unexplained numbers like 0.075 directly in code, makes bugs easy to introduce and hard to fix consistently. Naming constants and extracting repeated logic into functions is one of the most common things senior engineers flag in code review, and it is exactly what graders will look for in your final project's code quality.</p>""",
            "key_concepts": ["function naming", "single responsibility", "avoiding magic numbers", "avoiding duplication", "readability"],
            "practical_exercise": {
                "title": "Refactor a Messy Function",
                "instructions": "Write a poorly named function with a magic number that calculates a student's final grade from three scores, then refactor it into a clearly named function with a named constant and a docstring explaining what it does. Submit both the before and after versions of the code."
            },
            "quiz": [
                {"question": "What is a 'magic number' in code?", "options": ['A number that changes randomly at runtime', 'Any number greater than 1000', 'A number used only in mathematical libraries', 'An unexplained numeric literal used directly in code instead of a named constant'], "correct_index": 3, "explanation": 'A magic number is a hardcoded value with no explanation, making code harder to understand and maintain.'},
                {"question": 'Why do code reviews often reject working code for being unclear?', "options": ['Working code is never rejected', 'Unclear code slows down every future developer who has to read and maintain it', 'Reviewers prefer shorter code regardless of clarity', 'Clarity has no effect on long-term maintenance'], "correct_index": 1, "explanation": 'Code is read far more than it is written, so unclear code creates ongoing costs for the whole team.'},
                {"question": "What does 'single responsibility' mean for a function?", "options": ['A function should do one clearly defined thing', 'A function should only be called once in the program', 'A function should have only one parameter', 'A function should never return a value'], "correct_index": 0, "explanation": 'A function following single responsibility focuses on one task, making it easier to test, name, and reuse.'}
            ],
            "resources": [
                {"label": "Python Style Guide (PEP 8)", "url": "https://docs.python.org/3/"}
            ]
        },
        {
            "day_number": 6,
            "week_number": 2,
            "week_title": "Building Blocks of Real Applications",
            "title": "Structuring a Python Project into Modules and Packages",
            "learning_objective": "By the end of this class, you will be able to organize a Python codebase into logical modules and packages instead of one large file.",
            "duration_minutes": 25,
            "content_html": """<p>A 500-line single file becomes unmanageable fast. Real backend applications split logic into modules by responsibility, for example separating routes, database models, and business logic, so any developer joining the project can find things quickly.</p><h2>Modules and Packages</h2><p>A module is a single Python file; a package is a folder of modules with an <code>__init__.py</code> file. A typical small backend project might look like this.</p><pre><code>myapp/
  __init__.py
  models.py
  routes.py
  services.py
  utils.py</code></pre><h2>Importing Across Modules</h2><p>Once split, modules import from each other using Python's import system.</p><pre><code># in routes.py
from myapp.services import calculate_total
from myapp.models import Order</code></pre><p>This structure is exactly what you will use in your final project: separating routes from business logic from database models makes the codebase testable and lets multiple people work on different files without constant merge conflicts, which is precisely how real engineering teams divide work.</p>""",
            "key_concepts": ["Python modules", "packages", "__init__.py", "project structure", "imports"],
            "practical_exercise": {
                "title": "Split a Monolithic Script into Modules",
                "instructions": "Take a single Python script that has a function for input validation, a function for a calculation, and a main block that runs it, and split it into a package with at least two separate module files, importing correctly across them. Submit the resulting folder structure and the code."
            },
            "quiz": [
                {"question": 'What is a Python package?', "options": ['A single function', 'A third-party library only', 'A folder of modules containing an __init__.py file', 'A compiled executable'], "correct_index": 2, "explanation": 'A Python package is a directory containing multiple modules along with an __init__.py file that marks it as importable.'},
                {"question": 'Why do real backend projects split code into multiple modules instead of one large file?', "options": ['It makes the codebase easier to navigate, test, and work on across a team', 'Python requires it to run', 'It makes the program run faster', 'Single files are not allowed by Git'], "correct_index": 0, "explanation": 'Splitting code by responsibility improves readability, testability, and lets multiple developers work without constant conflicts.'},
                {"question": "What does the following import statement do: 'from myapp.services import calculate_total'?", "options": ['Deletes the calculate_total function', 'Imports the calculate_total function from the services module inside the myapp package', 'Creates a new module called services', 'Runs the entire myapp package'], "correct_index": 1, "explanation": 'This statement imports a specific function from another module within the same package, a common pattern in structured projects.'}
            ],
            "resources": [
                {"label": "Python Modules Documentation", "url": "https://docs.python.org/3/tutorial/modules.html"}
            ]
        },
        {
            "day_number": 7,
            "week_number": 2,
            "week_title": "Building Blocks of Real Applications",
            "title": "Handling Errors Gracefully with Exceptions",
            "learning_objective": "By the end of this class, you will be able to anticipate failure points in code and handle them using try/except blocks appropriately.",
            "duration_minutes": 20,
            "content_html": """<p>Real users send bad input, networks fail, and files go missing. Software that crashes on the first unexpected input is not production-ready, and handling failure gracefully is one of the clearest signals of engineering maturity in a code review.</p><h2>Try, Except, and Specific Exceptions</h2><p>Python lets you catch specific error types and respond appropriately instead of crashing the whole program.</p><pre><code>def get_user_age(data):
    try:
        return int(data["age"])
    except KeyError:
        raise ValueError("Missing 'age' field in input")
    except ValueError:
        raise ValueError("Age must be a valid number")</code></pre><h2>Avoiding the Bare Except Trap</h2><p>Catching every possible exception with a bare <code>except:</code> hides real bugs and makes debugging painful, because you lose information about what actually failed. Always catch specific exception types, and only handle an error where you can meaningfully respond to it, otherwise let it propagate up with useful context, exactly the discipline your final project's API will need when handling bad requests.</p>""",
            "key_concepts": ["try/except", "specific exception handling", "raising exceptions", "avoiding bare except"],
            "practical_exercise": {
                "title": "Handle Bad Input Safely",
                "instructions": "Write a function that divides two numbers provided by a user as strings, and handle both the case where the input is not a valid number and the case where the division is by zero, returning a clear error message for each instead of crashing. Submit the function and three test calls showing each outcome."
            },
            "quiz": [
                {"question": "Why is a bare 'except:' considered bad practice?", "options": ['It runs slower than specific exceptions', 'It silently catches every error type, hiding real bugs and losing useful information', 'Python does not allow it', 'It only works with numeric errors'], "correct_index": 1, "explanation": 'A bare except swallows all exceptions indiscriminately, making it hard to know what actually went wrong.'},
                {"question": 'What should you do if a function cannot meaningfully handle an error it catches?', "options": ['Ignore the error silently', 'Always crash the entire program immediately', 'Print nothing and return None always', 'Let it propagate up with useful context rather than swallowing it'], "correct_index": 3, "explanation": "If a function can't meaningfully resolve an error, it should re-raise it with context so a higher-level caller can handle it properly."},
                {"question": "In the example function, what exception is raised if the 'age' key is missing from the input dictionary?", "options": ['TypeError, caught first', 'IndexError', 'ValueError, raised directly from a KeyError catch', 'No exception is raised'], "correct_index": 2, "explanation": 'The except KeyError block catches the missing key and raises a ValueError with a clear message instead of letting a raw KeyError surface.'}
            ],
            "resources": [
                {"label": "Python Errors and Exceptions Documentation", "url": "https://docs.python.org/3/tutorial/errors.html"}
            ]
        },
        {
            "day_number": 8,
            "week_number": 2,
            "week_title": "Building Blocks of Real Applications",
            "title": "Writing Your First Automated Tests with pytest",
            "learning_objective": "By the end of this class, you will be able to write and run automated unit tests for a Python function using pytest.",
            "duration_minutes": 30,
            "content_html": """<p>Manually re-running your program and eyeballing the output does not scale, and it does not catch regressions when you change code weeks later. Automated tests are code that checks your code, and every serious engineering team requires them before merging changes.</p><h2>Writing a Test with pytest</h2><p>pytest is the standard Python testing framework. A test function starts with <code>test_</code> and uses <code>assert</code> to check expected outcomes.</p><pre><code># test_calculator.py
from calculator import add

def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-2, -3) == -5</code></pre><p>Run tests from the terminal with <code>pytest</code>, and it reports exactly which tests passed or failed.</p><h2>Why Tests Change How You Code</h2><p>Once you have tests, you can change code confidently, because the test suite immediately tells you if you broke something. This is why job postings for backend roles list \"experience with automated testing\" as a requirement, not a nice-to-have, and why your final project must include tests covering its core logic.</p>""",
            "key_concepts": ["pytest", "unit tests", "assert statements", "test functions", "regression detection"],
            "practical_exercise": {
                "title": "Write Unit Tests for a Function",
                "instructions": "Write a function that checks whether a given year is a leap year, then write at least four pytest test functions covering a normal leap year, a normal non-leap year, a century year that is not a leap year (like 1900), and a century year that is a leap year (like 2000). Submit the code and a screenshot of pytest passing all tests."
            },
            "quiz": [
                {"question": "What must a pytest test function's name start with by convention?", "options": ["check_", "test_", "verify_", "run_"], "correct_index": 1, "explanation": "pytest automatically discovers and runs functions whose names start with test_."},
                {"question": "Why are automated tests valuable when changing existing code later?", "options": ["They make the code run faster", "They immediately reveal whether a change broke existing behavior", "They replace the need for Git", "They automatically fix bugs"], "correct_index": 1, "explanation": "Automated tests act as a safety net, catching regressions the moment a change breaks expected behavior."},
                {"question": "What keyword do pytest tests typically use to check an expected outcome?", "options": ["check", "verify", "assert", "expect"], "correct_index": 2, "explanation": "pytest tests use Python's built-in assert statement to state the expected result of the code under test."}
            ],
            "resources": [
                {"label": "pytest Documentation", "url": "https://docs.pytest.org/"}
            ]
        },
        {
            "day_number": 9,
            "week_number": 2,
            "week_title": "Building Blocks of Real Applications",
            "title": "Reading and Writing Data with Files and JSON",
            "learning_objective": "By the end of this class, you will be able to read from and write to files and structured JSON data in Python.",
            "duration_minutes": 20,
            "content_html": """<p>Before connecting to a real database, every backend developer needs to be comfortable persisting data to disk. JSON is the format APIs speak almost universally, so this is a direct stepping stone to building real backend endpoints.</p><h2>Reading and Writing JSON</h2><p>Python's built-in json module converts between Python dictionaries and JSON text.</p><pre><code>import json

data = {"name": "Amaka", "score": 87}
with open("student.json", "w") as f:
    json.dump(data, f)

with open("student.json") as f:
    loaded = json.load(f)
print(loaded["name"])</code></pre><h2>Why This Matters for Backend Work</h2><p>Every REST API request and response you will build later in this track is JSON under the hood. Understanding how to safely read, write, and validate JSON data now, including handling a missing or malformed file, is what makes the jump to building real API endpoints in week three straightforward instead of confusing.</p>""",
            "key_concepts": ["file I/O", "JSON serialization", "json.dump/json.load", "data persistence"],
            "practical_exercise": {
                "title": "Build a Simple JSON Data Store",
                "instructions": "Write a Python script that stores a list of student records (name and score) as a JSON file, then write a function to load the file, add a new student, and save it back, handling the case where the file does not exist yet. Submit the script and the resulting JSON file after adding two students."
            },
            "quiz": [
                {"question": "What does 'json.dump' do in Python?", "options": ['Writes a Python object to a file as JSON text', 'Deletes a JSON file', 'Reads JSON from a file into a Python object', 'Converts JSON to XML'], "correct_index": 0, "explanation": 'json.dump serializes a Python object (like a dict) and writes it to a file as JSON-formatted text.'},
                {"question": 'Why is JSON especially relevant for backend development?', "options": ['It is the only format Python can read', 'JSON files run faster than Python scripts', 'It replaces the need for databases entirely', 'It is the standard format most REST APIs use for requests and responses'], "correct_index": 3, "explanation": 'JSON is the near-universal data format for API communication, making it essential for backend developers.'},
                {"question": 'What should a script do if it tries to load a JSON file that does not exist yet?', "options": ['Crash with no explanation', 'Handle the missing file case explicitly, such as starting with an empty data structure', 'Automatically convert to XML', 'Ignore the error and continue with corrupted data'], "correct_index": 1, "explanation": 'Robust code anticipates a missing file and handles it gracefully instead of crashing unexpectedly.'}
            ],
            "resources": [
                {"label": "Python json Module Documentation", "url": "https://docs.python.org/3/library/json.html"}
            ]
        },
        {
            "day_number": 10,
            "week_number": 2,
            "week_title": "Building Blocks of Real Applications",
            "title": "Designing a Simple Relational Database Schema",
            "learning_objective": "By the end of this class, you will be able to design a normalized relational database schema with tables, keys, and relationships.",
            "duration_minutes": 30,
            "content_html": """<p>Nearly every real backend application stores its data in a relational database. Designing the schema well up front, before writing a single line of API code, prevents painful rewrites later and is a skill technical interviewers frequently probe with whiteboard questions.</p><h2>Tables, Primary Keys, and Foreign Keys</h2><p>A table represents one type of entity, a primary key uniquely identifies each row, and a foreign key links rows in one table to rows in another. A simple bookings system might look like this.</p><pre><code>users(id PK, name, email)
bookings(id PK, user_id FK -> users.id, date, status)</code></pre><h2>Avoiding Duplicate Data</h2><p>If you stored a user's name and email directly on every booking row instead of linking by user_id, updating a user's email would require updating every booking row too, and the data could easily become inconsistent. This is called normalization, and designing schemas this way from the start is exactly what you will do when planning your final project's database before writing any code.</p>""",
            "key_concepts": ["relational tables", "primary keys", "foreign keys", "normalization", "schema design"],
            "practical_exercise": {
                "title": "Design a Schema on Paper",
                "instructions": "Design a database schema for a simple library book-lending system with at least three tables (such as books, members, and loans), specifying each table's columns, primary keys, and foreign key relationships. Submit the schema as text or a diagram, along with one sentence explaining why you structured it that way."
            },
            "quiz": [
                {"question": 'What is the purpose of a foreign key?', "options": ["To encrypt a table's data", 'To make a table read-only', 'To link a row in one table to a row in another table', 'To speed up all queries automatically'], "correct_index": 2, "explanation": 'A foreign key creates a relationship by referencing the primary key of another table, connecting related data.'},
                {"question": 'What problem does normalizing a database schema solve?', "options": ['It makes queries impossible to write', 'It prevents duplicate, inconsistent data by storing each fact in one place', 'It removes the need for primary keys', 'It only applies to NoSQL databases'], "correct_index": 1, "explanation": 'Normalization avoids storing the same data redundantly across rows, preventing inconsistencies when that data changes.'},
                {"question": "In the example schema, what does 'user_id FK -> users.id' mean in the bookings table?", "options": ['It is an unrelated column with no connection to users', 'It automatically deletes users', 'It is the primary key of the bookings table', 'It is a foreign key linking each booking to a specific user in the users table'], "correct_index": 3, "explanation": 'This notation shows that user_id in bookings references the id primary key in the users table, forming a relationship.'}
            ],
            "resources": [
                {"label": "MDN: Database Design Basics", "url": "https://developer.mozilla.org/en-US/docs/Learn"}
            ]
        },
        {
            "day_number": 11,
            "week_number": 3,
            "week_title": "Building a Real Backend API",
            "title": "Building Your First REST API Endpoint with Flask",
            "learning_objective": "By the end of this class, you will be able to build and run a basic REST API endpoint that returns JSON data using Flask.",
            "duration_minutes": 30,
            "content_html": """<p>Flask is one of the most widely used Python web frameworks for building backend APIs, and it is popular precisely because it lets you build a working endpoint in minutes without heavy boilerplate. This is where your database and Python skills start turning into an actual application other software can talk to.</p><h2>Your First Endpoint</h2><p>A route maps a URL path and HTTP method to a Python function that returns a response.</p><pre><code>from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/students", methods=["GET"])
def get_students():
    return jsonify([{"id": 1, "name": "Amaka"}])

if __name__ == "__main__":
    app.run(debug=True)</code></pre><h2>Testing Your Endpoint</h2><p>Run the app and visit <code>http://localhost:5000/api/students</code> in a browser or use a tool like curl or Postman to send requests. Every backend job posting expects comfort building and testing REST endpoints like this one, and this exact pattern, routes returning JSON, is what your final project's API will be built from.</p>""",
            "key_concepts": ["Flask", "REST routes", "HTTP methods", "jsonify", "local development server"],
            "practical_exercise": {
                "title": "Build a Two-Endpoint Flask API",
                "instructions": "Build a Flask application with two GET endpoints: one that returns a list of at least three fictional products as JSON, and one that returns a single product by id from the URL path, returning a 404 JSON error if the id is not found. Submit the code and a screenshot of both endpoints working in a browser or Postman."
            },
            "quiz": [
                {"question": "What does the @app.route decorator do in Flask?", "options": ["Deletes a route from the app", "Maps a URL path and HTTP method to a specific Python function", "Connects the app to a database", "Installs Flask automatically"], "correct_index": 1, "explanation": "The @app.route decorator registers a function to handle requests to a specific URL path and HTTP method."},
                {"question": "What does jsonify() do in a Flask route?", "options": ["Converts a Python object into a proper JSON HTTP response", "Deletes JSON data", "Connects to an external API", "Renders an HTML template"], "correct_index": 0, "explanation": "jsonify() converts Python data structures into a JSON-formatted Flask response with the correct headers."},
                {"question": "Which HTTP method is typically used to retrieve data without changing anything on the server?", "options": ["DELETE", "POST", "GET", "PUT"], "correct_index": 2, "explanation": "GET requests are used to retrieve data and should not modify server-side state."}
            ],
            "resources": [
                {"label": "Flask Documentation", "url": "https://flask.palletsprojects.com/"}
            ]
        },
        {
            "day_number": 12,
            "week_number": 3,
            "week_title": "Building a Real Backend API",
            "title": "Handling POST Requests and Validating Input",
            "learning_objective": "By the end of this class, you will be able to build a POST endpoint that accepts and validates JSON input from a client.",
            "duration_minutes": 30,
            "content_html": """<p>Any API that only reads data is half an application. Real systems need to accept data from users, and every endpoint accepting outside input must validate it, because trusting client-supplied data blindly is one of the most common sources of bugs and security issues in production backends.</p><h2>Accepting JSON Input</h2><p>Flask's request object gives access to the JSON body of an incoming POST request.</p><pre><code>from flask import request, jsonify

@app.route("/api/students", methods=["POST"])
def create_student():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "name is required"}), 400
    new_student = {"id": 2, "name": data["name"]}
    return jsonify(new_student), 201</code></pre><h2>Why Validation Is Not Optional</h2><p>Without checking that required fields exist and have sensible types, a missing field can crash your endpoint or, worse, silently corrupt your data. Returning clear 400 error responses for bad input, instead of a generic server crash, is exactly the defensive coding style graders and interviewers expect from a competent backend developer.</p>""",
            "key_concepts": ["POST requests", "request.get_json()", "input validation", "HTTP status codes 201/400"],
            "practical_exercise": {
                "title": "Build a Validated POST Endpoint",
                "instructions": "Add a POST endpoint to your Flask app from Day 11 that creates a new product, requiring both a name and a price field, returning a 400 error with a clear message if either is missing or if price is not a positive number, and a 201 response with the created product otherwise. Submit the code and three example requests: one valid, one missing a field, and one with an invalid price."
            },
            "quiz": [
                {"question": 'What HTTP status code should a successful resource-creation POST request typically return?', "options": ['200', '404', '500', '201'], "correct_index": 3, "explanation": '201 Created is the standard status code for a request that successfully created a new resource.'},
                {"question": 'Why must an API validate incoming POST data instead of trusting it directly?', "options": ['Untrusted client input can crash the endpoint or corrupt stored data if not checked', 'Validation is only needed for GET requests', 'Flask automatically validates all input', 'Validation makes responses load faster'], "correct_index": 0, "explanation": 'Client-supplied data can be missing, malformed, or malicious, so servers must validate it before using it.'},
                {"question": 'What does request.get_json() do in a Flask route?', "options": ['Sends a JSON response to the client', 'Deletes the request', 'Parses the JSON body of the incoming request into a Python object', 'Connects to a JSON file on disk'], "correct_index": 2, "explanation": 'request.get_json() reads and parses the JSON payload sent in the body of an incoming request.'}
            ],
            "resources": [
                {"label": "Flask Documentation", "url": "https://flask.palletsprojects.com/"}
            ]
        },
        {
            "day_number": 13,
            "week_number": 3,
            "week_title": "Building a Real Backend API",
            "title": "Connecting Flask to a Real Database with SQLAlchemy",
            "learning_objective": "By the end of this class, you will be able to connect a Flask application to a database and define models using SQLAlchemy.",
            "duration_minutes": 35,
            "content_html": """<p>JSON files and in-memory lists disappear the moment your app restarts, which is unacceptable for a real product. Connecting your API to an actual database, using an ORM (Object-Relational Mapper) like SQLAlchemy, is the step that turns a toy demo into a real backend.</p><h2>Defining a Model</h2><p>SQLAlchemy lets you define database tables as Python classes.</p><pre><code>from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, default=0)</code></pre><h2>Querying the Database</h2><p>Once configured, you query and save data through Python objects instead of raw SQL strings.</p><pre><code>new_student = Student(name="Chidi", score=75)
db.session.add(new_student)
db.session.commit()

all_students = Student.query.all()</code></pre><p>This ORM pattern, models mapped to Python classes and queried through session objects, is the standard approach used in production Flask and Django applications across the industry, and it is exactly what your final project's data layer will be built on.</p>""",
            "key_concepts": ["SQLAlchemy ORM", "db.Model", "db.session", "querying with .query", "database persistence"],
            "practical_exercise": {
                "title": "Connect a Flask App to SQLite with SQLAlchemy",
                "instructions": "Set up Flask-SQLAlchemy with a SQLite database, define a Product model with name and price fields, write a script that adds three products to the database, and query and print all products back out. Submit the code and the printed query output."
            },
            "quiz": [
                {"question": 'What is the purpose of an ORM like SQLAlchemy?', "options": ['To design HTML templates', 'To let developers interact with a database using Python objects instead of raw SQL', 'To replace Git for version control', 'To handle only JSON files'], "correct_index": 1, "explanation": 'An ORM maps database tables to Python classes, letting developers query and modify data using Python syntax.'},
                {"question": "In the Student model example, what does 'nullable=False' on the name column enforce?", "options": ['The name column must always have a value when a row is saved', 'The name column can be left empty', 'The name column stores numbers only', 'The name column is automatically generated'], "correct_index": 0, "explanation": "nullable=False means the database will reject any row where that column's value is missing."},
                {"question": 'What does db.session.commit() do?', "options": ['Deletes all records in a table', 'Creates a new database from scratch', 'Rolls back the last change', 'Saves pending changes (like new or updated rows) permanently to the database'], "correct_index": 3, "explanation": 'commit() persists all pending changes in the current session to the actual database.'}
            ],
            "resources": [
                {"label": "Flask-SQLAlchemy Documentation", "url": "https://flask.palletsprojects.com/"}
            ]
        },
        {
            "day_number": 14,
            "week_number": 3,
            "week_title": "Building a Real Backend API",
            "title": "Building Full CRUD Endpoints for a Resource",
            "learning_objective": "By the end of this class, you will be able to build complete Create, Read, Update, and Delete endpoints for a single database-backed resource.",
            "duration_minutes": 35,
            "content_html": """<p>Almost every backend feature you will ever build reduces to CRUD: Create, Read, Update, Delete. Mastering this pattern for one resource means you can apply it to any resource, which is exactly how real APIs scale to dozens of endpoints.</p><h2>The Four Operations</h2><p>Each CRUD operation maps to an HTTP method and typically a specific URL pattern.</p><pre><code>GET    /api/products       -> list all
GET    /api/products/&lt;id&gt;  -> get one
POST   /api/products       -> create
PUT    /api/products/&lt;id&gt;  -> update
DELETE /api/products/&lt;id&gt;  -> delete</code></pre><h2>Implementing Update and Delete</h2><p>Update and delete both need to look up the record first and handle the case where it does not exist.</p><pre><code>@app.route("/api/products/&lt;int:id&gt;", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "not found"}), 404
    db.session.delete(product)
    db.session.commit()
    return "", 204</code></pre><p>By the end of today you can build a complete, database-backed resource end to end, which is the core building block your final project's entire API will be assembled from.</p>""",
            "key_concepts": ["CRUD operations", "RESTful URL patterns", "PUT vs DELETE", "404 handling"],
            "practical_exercise": {
                "title": "Build Full CRUD for a Resource",
                "instructions": "Extend your Product API to support all four CRUD operations: list all products, get one by id, create a new one, update an existing one's price, and delete one, with correct HTTP status codes and 404 handling when a product does not exist. Submit the code and a short log showing all five operations tested successfully."
            },
            "quiz": [
                {"question": "Which HTTP method is conventionally used to fully update an existing resource?", "options": ["GET", "POST", "PUT", "DELETE"], "correct_index": 2, "explanation": "PUT is the conventional HTTP method for updating an existing resource identified by its URL."},
                {"question": "What should a DELETE or update endpoint do if the requested resource id does not exist?", "options": ["Crash the server", "Return a 404 error indicating the resource was not found", "Silently create a new resource instead", "Always return 200 regardless"], "correct_index": 1, "explanation": "A well-designed API returns a 404 status when a client references a resource that does not exist."},
                {"question": "What does CRUD stand for?", "options": ["Create, Retrieve, Update, Destroy", "Create, Read, Update, Delete", "Connect, Read, Upload, Deploy", "Copy, Read, Undo, Delete"], "correct_index": 1, "explanation": "CRUD stands for Create, Read, Update, and Delete, the four fundamental data operations most APIs support."}
            ],
            "resources": [
                {"label": "MDN: HTTP Request Methods", "url": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods"}
            ]
        },
        {
            "day_number": 15,
            "week_number": 3,
            "week_title": "Building a Real Backend API",
            "title": "Testing API Endpoints with pytest and Flask's Test Client",
            "learning_objective": "By the end of this class, you will be able to write automated tests for Flask API endpoints using Flask's test client.",
            "duration_minutes": 30,
            "content_html": """<p>Manually clicking through Postman to check every endpoint after every change does not scale, and it is easy to forget to recheck something you broke. Flask ships a built-in test client specifically so you can automate exactly this kind of endpoint verification.</p><h2>Using Flask's Test Client</h2><p>The test client simulates HTTP requests against your app without needing a running server.</p><pre><code>import pytest
from app import app, db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_products_empty(client):
    response = client.get("/api/products")
    assert response.status_code == 200
    assert response.get_json() == []</code></pre><h2>Testing Create and Error Cases</h2><p>Good API tests cover both the happy path and failure cases, such as sending invalid data and checking for a 400 response. This is precisely the kind of automated test suite your final project's CI pipeline will run on every push, catching regressions before they ever reach a reviewer or a user.</p>""",
            "key_concepts": ["Flask test client", "pytest fixtures", "testing status codes", "happy path vs error path testing"],
            "practical_exercise": {
                "title": "Write an API Test Suite",
                "instructions": "Write at least five pytest tests for your CRUD Product API from Day 14, covering: listing products, creating a valid product, creating an invalid product (missing field), getting a product that does not exist, and deleting an existing product. Submit the test file and a screenshot of all tests passing."
            },
            "quiz": [
                {"question": "What is the main advantage of Flask's test client over manually testing with Postman?", "options": ['It lets tests simulate HTTP requests and be run repeatedly and automatically', 'It deploys the app automatically', 'It replaces the need for a database', 'It only works for GET requests'], "correct_index": 0, "explanation": 'The test client allows automated, repeatable testing of endpoints without manual clicking or a running server.'},
                {"question": 'Why should API tests cover error cases, not just successful requests?', "options": ['Error cases are not actually important', 'pytest cannot test error responses', 'Error handling is part of correct behavior and regressions there are just as harmful as broken success paths', 'Error cases always pass automatically'], "correct_index": 2, "explanation": 'Robust APIs must handle bad input correctly, so tests should verify error responses behave as expected too.'},
                {"question": 'What is a pytest fixture used for, as shown in the client() example?', "options": ['To permanently delete test data', 'To slow down test execution intentionally', 'To replace assert statements', 'To set up reusable resources, like a configured test client, for multiple tests'], "correct_index": 3, "explanation": 'Fixtures provide reusable setup logic, like an initialized test client, that multiple test functions can share.'}
            ],
            "resources": [
                {"label": "pytest Documentation", "url": "https://docs.pytest.org/"},
                {"label": "Flask Testing Documentation", "url": "https://flask.palletsprojects.com/"}
            ]
        },
        {
            "day_number": 16,
            "week_number": 4,
            "week_title": "Engineering Practices That Scale",
            "title": "Automating Tests on Every Push with GitHub Actions CI",
            "learning_objective": "By the end of this class, you will be able to configure a basic GitHub Actions workflow that runs your test suite automatically on every push.",
            "duration_minutes": 30,
            "content_html": """<p>Even a great test suite is only useful if it actually gets run consistently. Continuous Integration (CI) automatically runs your tests every time code is pushed, catching broken code before it reaches a teammate or production, and every professional engineering team relies on this.</p><h2>A Basic GitHub Actions Workflow</h2><p>GitHub Actions runs workflows defined in YAML files inside a <code>.github/workflows</code> folder.</p><pre><code># .github/workflows/tests.yml
name: Run Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest</code></pre><h2>Why CI Changes How Teams Work</h2><p>With CI configured, every pull request shows a pass/fail check automatically, so nobody has to remember to run tests manually before merging. This is exactly the CI pipeline your final project must include, and listing \"CI/CD experience\" on your resume backed by a real example is a strong signal to employers.</p>""",
            "key_concepts": ["Continuous Integration", "GitHub Actions", "workflow YAML", "automated test runs on push"],
            "practical_exercise": {
                "title": "Set Up a CI Pipeline for Your Tests",
                "instructions": "Add a .github/workflows/tests.yml file to one of your existing Flask projects that installs dependencies and runs pytest on every push, push a small code change to trigger it, and confirm it runs successfully in the Actions tab. Submit a screenshot of the passing workflow run."
            },
            "quiz": [
                {"question": "What is the main purpose of Continuous Integration?", "options": ["To deploy code to production without any review", "To automatically run tests (and other checks) every time code is pushed", "To replace the need for Git entirely", "To write code automatically"], "correct_index": 1, "explanation": "CI automates running checks like tests on every code change, catching problems early and consistently."},
                {"question": "Where does GitHub Actions expect workflow configuration files to live in a repository?", "options": [".github/workflows/", "workflows/", "ci/", ".actions/"], "correct_index": 0, "explanation": "GitHub Actions looks for YAML workflow files inside the .github/workflows directory of a repository."},
                {"question": "What does the 'on: [push, pull_request]' line in a workflow file control?", "options": ["Which programming language is used", "Which events trigger the workflow to run", "The name of the repository", "The Python version installed"], "correct_index": 1, "explanation": "The 'on' key specifies which GitHub events, like pushes or pull requests, will trigger the workflow to execute."}
            ],
            "resources": [
                {"label": "GitHub Actions Documentation", "url": "https://docs.github.com/"}
            ]
        },
        {
            "day_number": 17,
            "week_number": 4,
            "week_title": "Engineering Practices That Scale",
            "title": "Writing Documentation That Actually Gets Read: READMEs and API Docs",
            "learning_objective": "By the end of this class, you will be able to write a clear README and basic API documentation for a backend project.",
            "duration_minutes": 25,
            "content_html": """<p>A brilliant project with no documentation is often unusable to anyone but its author, including a hiring manager skimming your GitHub in under two minutes. Good documentation is what turns your code into something other people, including future you, can actually use.</p><h2>What a Good README Includes</h2><p>A strong README explains what the project does, how to set it up locally, and how to run it, at minimum.</p><pre><code># Student Attendance API

A REST API for tracking student attendance.

## Setup
1. python -m venv venv && source venv/bin/activate
2. pip install -r requirements.txt
3. flask run

## Endpoints
GET /api/students - list all students
POST /api/students - create a student</code></pre><h2>Documenting API Endpoints</h2><p>Listing each endpoint's method, path, required fields, and example response saves anyone integrating with your API significant guesswork. A recruiter or technical interviewer reading your final project's README in the first 90 seconds is often deciding whether to look any further, so this document carries real weight.</p>""",
            "key_concepts": ["README structure", "setup instructions", "API endpoint documentation", "developer-facing writing"],
            "practical_exercise": {
                "title": "Write a README for an Existing Project",
                "instructions": "Write a complete README.md for one of your Flask projects from this track, including a project description, setup instructions from a clean clone, and a documented list of every endpoint with its method, path, and an example request/response. Submit the README file."
            },
            "quiz": [
                {"question": 'Why does documentation quality matter for a job search, not just for other developers?', "options": ['It has no real hiring impact', 'READMEs are only read by the original author', 'Documentation is optional in every hiring process', 'Recruiters and interviewers often judge a portfolio project quickly based on its README'], "correct_index": 3, "explanation": "A clear README is often the first thing a reviewer reads and shapes their first impression of a candidate's project."},
                {"question": 'What should setup instructions in a README allow someone to do?', "options": ["Understand the project's marketing copy", 'Get the project running locally from a clean clone of the repository', 'Deploy the code without reading any code', 'Skip installing dependencies'], "correct_index": 1, "explanation": 'Good setup instructions let any developer clone the repo and get it running without guessing steps.'},
                {"question": 'What should API endpoint documentation include at minimum?', "options": ['The HTTP method, URL path, and expected request/response format', "Only the endpoint's color scheme", "The developer's personal biography", "The server's IP address only"], "correct_index": 0, "explanation": 'Useful API docs specify how to call each endpoint and what to expect back, covering method, path, and data shape.'}
            ],
            "resources": [
                {"label": "GitHub Docs: About READMEs", "url": "https://docs.github.com/"}
            ]
        },
        {
            "day_number": 18,
            "week_number": 4,
            "week_title": "Engineering Practices That Scale",
            "title": "Managing Secrets and Configuration with Environment Variables",
            "learning_objective": "By the end of this class, you will be able to manage sensitive configuration like API keys and database URLs using environment variables instead of hardcoding them.",
            "duration_minutes": 20,
            "content_html": """<p>Hardcoding a database password or API key directly in your code is one of the most common and most damaging mistakes junior developers make, because it usually ends up committed to a public GitHub repository for anyone to find and abuse.</p><h2>Using Environment Variables</h2><p>Environment variables keep secrets outside your codebase, loaded at runtime instead.</p><pre><code># .env (never committed to Git)
DATABASE_URL=postgresql://user:pass@localhost/mydb
SECRET_KEY=super-secret-value</code></pre><pre><code>import os
from dotenv import load_dotenv

load_dotenv()
database_url = os.environ.get("DATABASE_URL")</code></pre><h2>Keeping Secrets Out of Git</h2><p>Add a <code>.gitignore</code> entry for <code>.env</code> so it never gets committed, and commit a <code>.env.example</code> file with placeholder values instead so teammates know what variables are needed. This pattern, real secrets in environment variables, placeholders in Git, is mandatory for your final project's deployment and is one of the first things a security-conscious reviewer checks.</p>""",
            "key_concepts": ["environment variables", ".env files", "python-dotenv", ".gitignore", "secrets management"],
            "practical_exercise": {
                "title": "Move Hardcoded Secrets to Environment Variables",
                "instructions": "Take one of your Flask projects and move its database URL or secret key out of the source code into a .env file, load it using python-dotenv, add .env to .gitignore, and create a .env.example with placeholder values. Submit the updated code, the .gitignore, and the .env.example file (not your real .env)."
            },
            "quiz": [
                {"question": 'Why is hardcoding a database password directly in source code dangerous?', "options": ['It makes the code run slower', 'Python does not allow string literals for passwords', 'If the code is pushed to a public repository, the password becomes visible to anyone', 'It has no real security impact'], "correct_index": 2, "explanation": 'Hardcoded secrets committed to version control, especially public repos, can be discovered and abused by anyone.'},
                {"question": 'What is the purpose of adding .env to .gitignore?', "options": ['To prevent the file containing real secrets from being committed to version control', 'To delete the .env file automatically', 'To make the app run faster', 'To share secrets publicly on purpose'], "correct_index": 0, "explanation": '.gitignore prevents Git from tracking and committing the .env file, keeping real secrets out of the repository history.'},
                {"question": 'What is the purpose of a .env.example file?', "options": ['To store real production secrets', 'To show teammates which environment variables are needed, using placeholder values', 'To replace the .gitignore file', 'To automatically deploy the application'], "correct_index": 1, "explanation": '.env.example documents required configuration variables with safe placeholder values, without exposing real secrets.'}
            ],
            "resources": [
                {"label": "python-dotenv on PyPI", "url": "https://pypi.org/"}
            ]
        },
        {
            "day_number": 19,
            "week_number": 4,
            "week_title": "Engineering Practices That Scale",
            "title": "Debugging Systematically with Logs and a Debugger",
            "learning_objective": "By the end of this class, you will be able to debug a failing application systematically using logging and a step-through debugger instead of guesswork.",
            "duration_minutes": 25,
            "content_html": """<p>Randomly inserting print statements and hoping to spot the bug does not scale to real applications with hundreds of files. Professional developers debug systematically, using logs to understand what happened and a debugger to inspect exactly what is happening at the moment something goes wrong.</p><h2>Structured Logging Over Print Statements</h2><p>Python's logging module lets you record events with severity levels, and unlike print, logs can be filtered and kept in production.</p><pre><code>import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Processing order %s", order_id)
logger.error("Payment failed for order %s: %s", order_id, error)</code></pre><h2>Using a Debugger to Inspect State</h2><p>VS Code's built-in debugger lets you set breakpoints and inspect variable values at the exact line where something goes wrong, rather than guessing from scattered print output. Learning to read a stack trace and reproduce a bug with a breakpoint, instead of randomly editing code until it works, is what separates efficient debugging from hours of frustration, on this track and in a real job.</p>""",
            "key_concepts": ["logging levels", "structured logging", "breakpoints", "stack traces", "systematic debugging"],
            "practical_exercise": {
                "title": "Add Logging and Debug a Broken Function",
                "instructions": "Take a function with a deliberately introduced bug (such as an off-by-one error in a loop), add logging statements to trace its execution, use a debugger or print-based trace to identify the exact line causing the wrong result, and fix it. Submit the buggy version, your debugging notes explaining how you found the issue, and the fixed version."
            },
            "quiz": [
                {"question": 'What is a key advantage of using the logging module over scattered print statements?', "options": ['Logging cannot be turned off', 'Logs support severity levels and can be filtered or kept in production without editing code', 'print statements run faster than logging', 'Logging only works with Flask'], "correct_index": 1, "explanation": 'The logging module supports severity levels and configuration, making it far more suitable for production use than print.'},
                {"question": 'What does a breakpoint let a developer do while debugging?', "options": ['Permanently stop the program', 'Automatically fix the bug', 'Delete the current function', 'Pause execution at a specific line to inspect variable values at that moment'], "correct_index": 3, "explanation": "A breakpoint pauses execution so the developer can inspect the program's exact state at that point."},
                {"question": 'Why is systematic debugging (using logs and breakpoints) preferred over randomly editing code until it works?', "options": ['Random editing is always faster', 'Systematic debugging is only for large teams', 'It identifies the actual cause of a bug instead of guessing, saving time and avoiding new bugs', 'It removes the need for testing'], "correct_index": 2, "explanation": 'Systematic debugging locates the real root cause, avoiding wasted time and the risk of introducing new bugs through guesswork.'}
            ],
            "resources": [
                {"label": "Python logging Documentation", "url": "https://docs.python.org/3/library/logging.html"}
            ]
        },
        {
            "day_number": 20,
            "week_number": 4,
            "week_title": "Engineering Practices That Scale",
            "title": "Deploying a Flask API to a Live Server",
            "learning_objective": "By the end of this class, you will be able to deploy a Flask application to a live public URL using a modern hosting platform.",
            "duration_minutes": 30,
            "content_html": """<p>Code sitting on your laptop helps nobody. Deployment is the step that turns your project into something a client, employer, or real user can actually reach and use, and it is the single most convincing proof that you can ship, not just code.</p><h2>Preparing an App for Deployment</h2><p>Production deployments need a production-grade server (not Flask's built-in dev server), a requirements file, and configuration through environment variables.</p><pre><code># requirements.txt
flask
flask-sqlalchemy
gunicorn
python-dotenv</code></pre><pre><code># Procfile (for platforms like Render/Railway)
web: gunicorn app:app</code></pre><h2>Deploying and Verifying</h2><p>Platforms like Render, Railway, or Fly.io connect directly to your GitHub repository and redeploy automatically on every push once configured. After deploying, always test every endpoint against the live URL, not just locally, because differences in environment variables or database connections often only surface once deployed, exactly the checklist your final project's deployment must pass.</p>""",
            "key_concepts": ["gunicorn", "Procfile", "environment-based deployment", "production hosting platforms", "post-deploy verification"],
            "practical_exercise": {
                "title": "Deploy Your Flask API Live",
                "instructions": "Deploy one of your Flask CRUD APIs to a free tier of Render, Railway, or Fly.io, configuring any required environment variables on the platform, and verify at least two endpoints work against the live URL using curl or Postman. Submit the live URL and a screenshot of a successful request against it."
            },
            "quiz": [
                {"question": "Why shouldn't Flask's built-in development server be used in production?", "options": ["It is not designed to handle production traffic reliably and securely", "It cannot run Python code", "It only works locally and never elsewhere", "Flask has no development server"], "correct_index": 0, "explanation": "Flask's built-in server is meant for local development, not for handling real production traffic; a WSGI server like gunicorn is used instead."},
                {"question": "What is the purpose of a Procfile on platforms like Render or Railway?", "options": ["To store the app's HTML templates", "To tell the platform what command to run to start the application", "To define the database schema", "To list Python dependencies"], "correct_index": 1, "explanation": "A Procfile specifies the command (e.g. running gunicorn) that the hosting platform uses to start the application."},
                {"question": "Why should you test endpoints against the live deployed URL, not just locally, after deployment?", "options": ["Local testing is always sufficient", "Environment or configuration differences in production can cause issues that don't appear locally", "Live testing is required by law", "It has no real purpose"], "correct_index": 1, "explanation": "Differences in environment variables, database connections, or configuration can cause production-only bugs that local testing misses."}
            ],
            "resources": [
                {"label": "Render Documentation", "url": "https://render.com/docs"}
            ]
        },
        {
            "day_number": 21,
            "week_number": 5,
            "week_title": "Designing Real Systems",
            "title": "Designing a System's Architecture Before Writing Code",
            "learning_objective": "By the end of this class, you will be able to sketch a basic system architecture diagram for a backend application before implementing it.",
            "duration_minutes": 25,
            "content_html": """<p>Senior engineers spend real time designing before typing a single line of code, because a bad architectural decision made on day one can cost weeks to fix later. This is also exactly what system design interview rounds test, even for junior roles, at an appropriately simpler level.</p><h2>What a Basic Architecture Diagram Shows</h2><p>A simple backend architecture diagram shows the client, the API server, the database, and any external services, along with how data flows between them.</p><pre><code>[Mobile/Web Client] --HTTP--> [Flask API]  --SQL--> [PostgreSQL DB]
                                    |
                                    v
                          [Email/Payment Service]</code></pre><h2>Making Deliberate Trade-offs</h2><p>Every design decision, like choosing SQLite for a small project versus PostgreSQL for a scaling one, or a monolith versus separate services, is a trade-off between simplicity and future flexibility. Documenting these decisions and why you made them, even briefly, is exactly what you will be expected to do when planning your final project's architecture before day 30.</p>""",
            "key_concepts": ["system architecture", "architecture diagrams", "client-server-database flow", "design trade-offs"],
            "practical_exercise": {
                "title": "Sketch an Architecture Diagram",
                "instructions": "Choose a realistic backend idea (such as a campus food ordering system) and sketch a simple architecture diagram showing the client, API server, database, and at least one external service, then write three sentences justifying your key design choices (database type, monolith vs separate services). Submit the diagram and justification."
            },
            "quiz": [
                {"question": "Why do experienced engineers design a system's architecture before writing code?", "options": ['Poor early architectural decisions are often expensive to fix once significant code is written', 'Design has no impact on later development', 'It is required by every programming language', 'Architecture diagrams replace the need for code entirely'], "correct_index": 0, "explanation": 'Architecture decisions made early can be costly to change later, so thinking them through upfront saves significant rework.'},
                {"question": 'What does a basic backend architecture diagram typically show?', "options": ['Only the visual design of the user interface', "The company's org chart", 'Only the programming language used', 'The client, API server, database, and how data flows between them'], "correct_index": 3, "explanation": 'A basic architecture diagram illustrates the major components of a system and how data moves between them.'},
                {"question": 'Why does choosing SQLite versus PostgreSQL count as a design trade-off?', "options": ['There is no real difference between them', 'SQLite is simpler for small projects but PostgreSQL better supports scaling and concurrent access', 'SQLite cannot store any data', 'PostgreSQL cannot be used with Flask'], "correct_index": 1, "explanation": 'SQLite is lightweight and simple, ideal for small projects, while PostgreSQL handles concurrency and scale better for larger systems — a genuine trade-off.'}
            ],
            "resources": [
                {"label": "Martin Fowler: Software Architecture Guide", "url": "https://martinfowler.com/architecture/"}
            ]
        },
        {
            "day_number": 22,
            "week_number": 5,
            "week_title": "Designing Real Systems",
            "title": "Refactoring Legacy Code Without Breaking It",
            "learning_objective": "By the end of this class, you will be able to safely refactor an existing piece of working code while relying on tests to confirm behavior did not change.",
            "duration_minutes": 25,
            "content_html": """<p>Most professional software engineering work is not building something new; it is improving or extending code someone else already wrote. Refactoring, changing code's internal structure without changing its external behavior, is a daily task in real jobs, and doing it safely is a skill tested directly in take-home interview assignments.</p><h2>Refactoring Safely with Tests as a Safety Net</h2><p>Before refactoring, make sure tests exist and pass. After refactoring, run them again; if they still pass, behavior is preserved.</p><pre><code># Before: duplicated, hard to extend
def calculate_price(item, is_vip):
    if is_vip:
        return item["price"] * 0.9
    return item["price"]

# After: same behavior, clearer and extensible
DISCOUNT_RATES = {"vip": 0.9, "regular": 1.0}

def calculate_price(item, customer_type="regular"):
    return item["price"] * DISCOUNT_RATES[customer_type]</code></pre><h2>Small Steps, Constant Verification</h2><p>Refactor in small, verifiable steps rather than one giant rewrite, running your test suite after each step. This discipline is exactly what will let you confidently extend your own final project's code as requirements evolve, without accidentally breaking features that already worked.</p>""",
            "key_concepts": ["refactoring", "behavior preservation", "test-driven safety net", "incremental changes"],
            "practical_exercise": {
                "title": "Refactor Code Backed by Tests",
                "instructions": "Take a working function with duplicated or awkward logic (write one if you do not already have one), write tests that pass against the current version, refactor the internal implementation to be cleaner without changing its inputs or outputs, and confirm all tests still pass. Submit the before code, the tests, and the refactored code."
            },
            "quiz": [
                {"question": "What does 'refactoring' mean in software engineering?", "options": ['Adding new features to an application', 'Deleting unused files from a repository', "Changing code's internal structure without changing its external behavior", 'Rewriting an app in a different language'], "correct_index": 2, "explanation": "Refactoring improves code's internal design and readability while preserving its observable behavior."},
                {"question": 'Why should tests exist before refactoring a piece of code?', "options": ['Tests are not actually necessary for refactoring', 'Passing tests before and after refactoring confirm that behavior was preserved', 'Tests make the refactored code run faster', 'Tests replace the need for code review'], "correct_index": 1, "explanation": "Tests act as a safety net, confirming that a refactor did not accidentally change the code's behavior."},
                {"question": 'Why is refactoring in small, verifiable steps preferred over one large rewrite?', "options": ['Small steps take longer with no benefit', 'Large rewrites are always safer', 'Step size has no effect on safety', 'Small steps make it easier to catch and isolate any accidental behavior change immediately'], "correct_index": 3, "explanation": 'Small incremental changes, each verified with tests, make it much easier to pinpoint exactly what broke if something does.'}
            ],
            "resources": [
                {"label": "Refactoring Guru", "url": "https://refactoring.guru/"}
            ]
        },
        {
            "day_number": 23,
            "week_number": 5,
            "week_title": "Designing Real Systems",
            "title": "Securing an API: Authentication and Common Vulnerabilities",
            "learning_objective": "By the end of this class, you will be able to implement basic token-based authentication and identify common API security vulnerabilities.",
            "duration_minutes": 30,
            "content_html": """<p>An API with no authentication lets anyone read or modify your data, which is unacceptable for anything beyond a toy project. Understanding basic authentication and common vulnerabilities is expected knowledge for any backend role, and it is one of the first things a security-conscious reviewer checks in a portfolio project.</p><h2>Token-Based Authentication</h2><p>A common pattern issues a token on login that the client sends with every subsequent request.</p><pre><code>@app.route("/api/protected")
def protected_route():
    token = request.headers.get("Authorization")
    if not token or not is_valid_token(token):
        return jsonify({"error": "unauthorized"}), 401
    return jsonify({"message": "You are authenticated"})</code></pre><h2>Common Vulnerabilities to Avoid</h2><p>Never build raw SQL queries by concatenating user input, which enables SQL injection; always use parameterized queries or an ORM, which SQLAlchemy already handles safely. Never store passwords in plain text; always hash them with a library like bcrypt or Werkzeug's security helpers. These are the exact basics an interviewer expects any backend candidate to know, and your final project's authentication must follow them.</p>""",
            "key_concepts": ["token-based authentication", "401 Unauthorized", "SQL injection", "password hashing"],
            "practical_exercise": {
                "title": "Add Basic Authentication to an Endpoint",
                "instructions": "Add a simple token-check to one endpoint in your Flask API, requiring an Authorization header with a specific hardcoded token value for this exercise, returning 401 if it is missing or wrong. Then write one paragraph explaining, in your own words, what SQL injection is and how using SQLAlchemy's ORM protects against it. Submit the code and the paragraph."
            },
            "quiz": [
                {"question": 'What HTTP status code should an API return when a request is missing valid authentication?', "options": ['200', '201', '404', '401'], "correct_index": 3, "explanation": '401 Unauthorized is the standard status code indicating a request lacks valid authentication credentials.'},
                {"question": 'Why is building SQL queries by directly concatenating user input dangerous?', "options": ['It enables SQL injection, letting attackers manipulate the query itself', 'It makes queries run faster', 'It is not actually dangerous if using Flask', 'Concatenation is required for all databases'], "correct_index": 0, "explanation": 'Concatenating raw user input into SQL queries allows attackers to inject malicious SQL, a classic and serious vulnerability.'},
                {"question": 'Why should passwords never be stored in plain text?', "options": ['Plain text passwords take up more storage space', 'Plain text storage is not supported by any database', "If the database is ever breached, plain text passwords expose every user's real password directly", 'Hashing is only needed for email addresses'], "correct_index": 2, "explanation": "Storing passwords in plain text means a database breach immediately exposes every user's actual password; hashing protects against this."}
            ],
            "resources": [
                {"label": "MDN: Web Security", "url": "https://developer.mozilla.org/en-US/docs/Web/Security"}
            ]
        },
        {
            "day_number": 24,
            "week_number": 5,
            "week_title": "Designing Real Systems",
            "title": "Working with Third-Party APIs and External Services",
            "learning_objective": "By the end of this class, you will be able to integrate a third-party API into a backend application and handle its failures gracefully.",
            "duration_minutes": 25,
            "content_html": """<p>Real applications rarely work in isolation; they call payment providers, SMS gateways, weather services, or maps APIs. Knowing how to integrate a third-party API reliably, including when it fails, is a routine backend engineering task.</p><h2>Calling an External API</h2><p>The requests library is the standard way to call external APIs from Python.</p><pre><code>import requests

response = requests.get("https://api.exchangerate.host/latest", params={"base": "NGN"}, timeout=5)
if response.status_code == 200:
    rates = response.json()
else:
    rates = None</code></pre><h2>Handling External Failures Gracefully</h2><p>External services go down, time out, or rate-limit you, and your application must not crash when that happens. Always set a timeout, check the status code, and handle exceptions like connection errors, returning a sensible fallback or clear error to your own API's caller instead of letting the failure crash your whole app, exactly the resilience real production backends need.</p>""",
            "key_concepts": ["requests library", "third-party API integration", "timeouts", "graceful failure handling"],
            "practical_exercise": {
                "title": "Integrate a Public API with Failure Handling",
                "instructions": "Build a Flask endpoint that calls a free public API (such as a currency exchange or weather API) and returns a simplified JSON response to the caller, with a timeout set and proper handling if the external API is slow, down, or returns an error, returning a clear error message instead of crashing. Submit the code and a demonstration of both a successful call and a simulated failure (e.g. by using an invalid URL) handled gracefully."
            },
            "quiz": [
                {"question": 'Why is it important to set a timeout when calling an external API?', "options": ['Timeouts are not necessary for external calls', 'Without a timeout, a slow or unresponsive external service can hang your entire application', 'Timeouts make external APIs respond faster', 'Timeouts are only relevant for database queries'], "correct_index": 1, "explanation": 'A timeout prevents your application from hanging indefinitely if an external service is slow or unresponsive.'},
                {"question": 'What should a backend do if a third-party API it depends on returns an error or is down?', "options": ['Handle the failure gracefully, returning a clear error or fallback instead of crashing', 'Crash immediately with no explanation', 'Ignore the error and return random data', 'Automatically retry forever with no limit'], "correct_index": 0, "explanation": 'Well-engineered backends handle external failures gracefully, giving callers clear feedback instead of crashing.'},
                {"question": 'What Python library is most commonly used to call external HTTP APIs?', "options": ['flask', 'sqlalchemy', 'pytest', 'requests'], "correct_index": 3, "explanation": 'The requests library is the standard, widely used tool for making HTTP calls to external APIs from Python.'}
            ],
            "resources": [
                {"label": "Requests Library Documentation", "url": "https://requests.readthedocs.io/"}
            ]
        },
        {
            "day_number": 25,
            "week_number": 5,
            "week_title": "Designing Real Systems",
            "title": "Optimizing a Slow Application: Profiling and Query Performance",
            "learning_objective": "By the end of this class, you will be able to identify a performance bottleneck in an application and apply a targeted fix.",
            "duration_minutes": 25,
            "content_html": """<p>An application that works correctly but takes ten seconds to respond will still lose users and fail technical interviews focused on performance. Knowing how to find and fix the actual bottleneck, rather than guessing, is what separates competent engineers from those who optimize the wrong thing.</p><h2>Finding the Real Bottleneck</h2><p>Never optimize based on a guess. Time different parts of your code or use profiling tools to see exactly where time is spent, which is very often a database query, not your Python logic.</p><pre><code>import time
start = time.time()
students = Student.query.all()
print(f"Query took {time.time() - start:.3f}s")</code></pre><h2>A Common Fix: The N+1 Query Problem</h2><p>A frequent backend performance bug is running one query per item in a loop instead of one combined query, known as the N+1 problem.</p><pre><code># Slow: N+1 queries
for order in Order.query.all():
    print(order.customer.name)  # separate query per order

# Fast: one query with a join
orders = Order.query.join(Customer).all()</code></pre><p>Recognizing and fixing N+1 queries is one of the most common backend performance issues in real production systems, and exactly the kind of optimization interviewers ask candidates to spot.</p>""",
            "key_concepts": ["performance profiling", "N+1 query problem", "database joins", "measuring before optimizing"],
            "practical_exercise": {
                "title": "Find and Fix an N+1 Query",
                "instructions": "Write a small SQLAlchemy example with two related models (like Order and Customer) that deliberately triggers an N+1 query pattern in a loop, measure or count the number of queries executed, then rewrite it using a join to fix the problem. Submit both versions and a short explanation of the performance difference."
            },
            "quiz": [
                {"question": 'What is the N+1 query problem?', "options": ['Running one separate query per item in a loop instead of a single combined query', 'A database error that only happens with more than one user', 'A bug that only affects NoSQL databases', 'An error that occurs when N is negative'], "correct_index": 0, "explanation": 'The N+1 problem occurs when a loop triggers a separate database query for each item instead of fetching related data in one combined query.'},
                {"question": 'Why should you measure before optimizing code?', "options": ['Measuring wastes time and should be skipped', 'Measurement always slows down the final code', 'Optimizing without measuring risks fixing something that was never actually the bottleneck', 'Optimization does not require any evidence'], "correct_index": 2, "explanation": "Without measuring first, developers risk spending effort optimizing code that isn't actually the performance bottleneck."},
                {"question": 'How does using a join typically fix an N+1 query problem?', "options": ['It deletes unnecessary data', 'It disables the database temporarily', 'It only works for write operations', 'It retrieves related data in a single combined query instead of one query per row'], "correct_index": 3, "explanation": 'A join combines related tables in a single query, avoiding the repeated per-row queries that cause the N+1 problem.'}
            ],
            "resources": [
                {"label": "SQLAlchemy Documentation", "url": "https://docs.sqlalchemy.org/"}
            ]
        },
        {
            "day_number": 26,
            "week_number": 6,
            "week_title": "Portfolio and Career Readiness",
            "title": "What Hiring Managers Actually Look for in a Junior Developer's Portfolio",
            "learning_objective": "By the end of this class, you will be able to evaluate your own project portfolio the way a hiring manager would and identify gaps to fix.",
            "duration_minutes": 25,
            "content_html": """<p>Most junior developer applications from Nigerian students look similar: a to-do list app, a calculator, maybe a weather app clone. Hiring managers reviewing dozens of portfolios in a day are looking for signals that separate a candidate who followed tutorials from one who can actually build and ship.</p><h2>What Actually Stands Out</h2><p>A live, working deployed URL beats a project that only runs locally. Clean, readable commit history beats one giant \"final version\" commit. A README that lets a stranger set the project up in five minutes beats no documentation. Tests that pass beat no tests at all.</p><pre><code>Weak signal:  "index.html, style.css, script.js" with no README, no tests, no deployment
Strong signal: Live URL, tested backend, clean commits, clear README, documented API</code></pre><h2>Auditing Your Own Work</h2><p>Go through your existing projects from this track and score each one honestly against these signals. This exercise directly previews what you must nail in your final project on day 30, because it is the single piece of work most likely to sit at the top of your portfolio when you apply for real roles.</p>""",
            "key_concepts": ["portfolio signals", "hiring manager perspective", "deployment as proof of skill", "self-audit"],
            "practical_exercise": {
                "title": "Audit Your Portfolio Against Hiring Signals",
                "instructions": "List your three strongest projects from this track so far, and for each one, score it 0-2 on four signals: live deployment, test coverage, commit history quality, and documentation quality, for a possible 8 points per project. Submit the scores and one specific fix you will make to your weakest-scoring project."
            },
            "quiz": [
                {"question": 'Why does a live deployed URL matter more to a hiring manager than a project that only runs locally?', "options": ['Deployment has no real effect on hiring decisions', 'Local projects are always better quality', 'Hiring managers cannot access GitHub', 'It proves the candidate can ship working software that a real user can access, not just code that runs on their own machine'], "correct_index": 3, "explanation": 'A live deployment is direct proof a candidate can take a project all the way to something usable, a stronger signal than local-only code.'},
                {"question": 'What does a clean, incremental commit history signal to a reviewer?', "options": ['That the candidate is inexperienced', 'That the candidate worked through the problem in organized, understandable steps', 'Commit history is never reviewed by anyone', 'It signals nothing useful'], "correct_index": 1, "explanation": 'A clear commit history shows organized, professional working habits, similar to how real engineering teams operate.'},
                {"question": 'According to the lesson, what is a common weakness in typical junior developer portfolios?', "options": ['Projects with no README, no tests, and no deployment, only local code', 'Too much documentation', 'Too many deployed projects', 'Overly detailed commit messages'], "correct_index": 0, "explanation": 'Many beginner portfolios lack documentation, tests, and deployment, making them look like tutorials rather than real, finished work.'}
            ],
            "resources": []
        },
        {
            "day_number": 27,
            "week_number": 6,
            "week_title": "Portfolio and Career Readiness",
            "title": "Answering Common Technical Interview Questions with Confidence",
            "learning_objective": "By the end of this class, you will be able to answer common junior software engineering interview questions clearly, using examples from your own projects.",
            "duration_minutes": 25,
            "content_html": """<p>Technical interviews for junior roles rarely start with a hard algorithm question. They usually start with questions about your projects and fundamentals, and how clearly you explain your own decisions matters as much as the decisions themselves.</p><h2>Common Junior-Level Questions</h2><p>Expect questions like: \"Walk me through a project you built and why you made the design choices you did,\" \"What is the difference between a GET and POST request?,\" and \"How do you handle errors in your code?\" Practice answering these out loud, not just silently in your head.</p><pre><code>Q: "How would you find a bug in an API that's returning wrong data?"
A: "I'd start by checking logs, reproduce it with a minimal test case,
   use a debugger to inspect the actual values at each step,
   then write a test that fails until the bug is fixed."</code></pre><h2>Using Your Own Projects as Evidence</h2><p>Every answer becomes stronger when tied to a specific project from this track: \"I actually handled this exact situation in my Flask API when I...\" turns an abstract answer into concrete proof of skill. Building this habit now means you walk into interviews with real stories, not rehearsed theory.</p>""",
            "key_concepts": ["technical interview basics", "explaining design decisions", "using project evidence", "debugging interview questions"],
            "practical_exercise": {
                "title": "Draft Answers to Common Interview Questions",
                "instructions": "Write out your spoken answers (as if talking to an interviewer) to three questions: 'Walk me through a project you built,' 'How do you handle errors in your code?,' and 'How would you debug an API returning the wrong data?' Each answer must reference a specific project or code example from this track. Submit the three written answers."
            },
            "quiz": [
                {"question": 'What kind of questions do junior software engineering interviews typically start with?', "options": ['Only extremely difficult algorithm puzzles', 'Only questions about salary expectations', 'Questions about your own projects and fundamental concepts', 'Trick questions with no correct answer'], "correct_index": 2, "explanation": "Junior interviews commonly focus on a candidate's own project experience and core fundamentals before, if ever, moving to harder problems."},
                {"question": 'Why does referencing a specific project strengthen an interview answer?', "options": ['It turns an abstract claim into concrete, verifiable evidence of real skill', 'It makes the answer longer, which is always better', 'Interviewers ignore project references', 'Specific examples are considered unprofessional'], "correct_index": 0, "explanation": "Concrete examples from real projects give interviewers tangible proof of a candidate's skills rather than abstract claims."},
                {"question": 'According to the lesson, what should you practice besides just knowing the answer mentally?', "options": ['Memorizing answers word for word without understanding them', 'Saying answers out loud to build comfort explaining them clearly', 'Avoiding any preparation before interviews', 'Only writing code, never speaking about it'], "correct_index": 1, "explanation": 'Practicing answers out loud builds the verbal fluency needed to explain technical decisions clearly under interview pressure.'}
            ],
            "resources": []
        },
        {
            "day_number": 28,
            "week_number": 6,
            "week_title": "Portfolio and Career Readiness",
            "title": "Writing Clear Pull Request Descriptions and Giving Code Review Feedback",
            "learning_objective": "By the end of this class, you will be able to write a clear pull request description and give constructive code review feedback.",
            "duration_minutes": 20,
            "content_html": """<p>On a real engineering team, most of your daily communication with other developers happens through pull requests and code review comments, not meetings. Writing clearly here is a skill that directly affects how quickly your code gets merged and how much teammates trust your work.</p><h2>A Strong Pull Request Description</h2><p>A good PR description explains what changed, why, and how to verify it, not just \"fixed bug.\"</p><pre><code>## What
Fixes incorrect VAT calculation on orders over 10 items.

## Why
Bug reported in issue #42; the discount was applied before VAT
instead of after, undercharging customers.

## How to verify
Run the new test in test_orders.py::test_vat_after_discount</code></pre><h2>Giving Constructive Review Feedback</h2><p>Good review comments are specific, kind, and explain the reasoning: \"Consider extracting this into a helper function since it's duplicated in three places\" beats \"this is bad.\" Practicing this now, even reviewing your own past code, builds a habit that makes you someone teams want to collaborate with from day one.</p>""",
            "key_concepts": ["pull request descriptions", "code review etiquette", "constructive feedback", "team communication"],
            "practical_exercise": {
                "title": "Write a PR Description and Review Comments",
                "instructions": "Pick a real change from one of your projects this track, write a full pull request description for it following the What/Why/How to verify structure, and then write three constructive code review comments (as if reviewing a teammate's code) pointing out specific, actionable improvements on a piece of your own past code. Submit both the PR description and the three review comments."
            },
            "quiz": [
                {"question": 'What should a good pull request description explain, beyond just what changed?', "options": ['Nothing more is needed beyond the code diff itself', 'Why the change was made and how a reviewer can verify it works', "The developer's personal opinions unrelated to the change", 'Only the file names that were modified'], "correct_index": 1, "explanation": 'A strong PR description gives context (why) and verification steps, not just a list of changed files.'},
                {"question": 'Which of these is an example of constructive code review feedback?', "options": ['"This is bad code."', 'No comment at all, just an approval', '"Rewrite this entirely, I don\'t like it."', '"Consider extracting this into a helper function since it\'s duplicated in three places."'], "correct_index": 3, "explanation": 'Constructive feedback is specific and actionable, explaining the reasoning behind a suggested change.'},
                {"question": 'Why does communication through pull requests matter so much on real engineering teams?', "options": ['It has no real impact on team collaboration', 'Pull requests are rarely used by professional teams', 'Most day-to-day developer communication happens through PRs and review comments, not meetings', 'Only senior engineers write pull requests'], "correct_index": 2, "explanation": 'Pull requests and code review comments are a primary communication channel on engineering teams, making clarity there essential.'}
            ],
            "resources": [
                {"label": "GitHub Docs: About Pull Requests", "url": "https://docs.github.com/"}
            ]
        },
        {
            "day_number": 29,
            "week_number": 6,
            "week_title": "Portfolio and Career Readiness",
            "title": "Planning Your Final Project: Scope, Architecture, and Milestones",
            "learning_objective": "By the end of this class, you will be able to scope a backend project into a realistic architecture and a day-by-day build plan.",
            "duration_minutes": 30,
            "content_html": """<p>Jumping straight into coding a big project without a plan is how final projects end up half-finished. Real engineering teams break large work into milestones before writing code, and doing this today sets you up to actually finish a polished final project instead of an ambitious but incomplete one.</p><h2>Scoping Realistically</h2><p>Pick a project idea you can realistically finish: a student attendance tracker, a lost-and-found system, or a small inventory manager are all appropriately sized. List the core features first, and explicitly cut anything not essential to a working v1.</p><pre><code>Must-have: create/list/update attendance records, basic auth, tests, deployment
Nice-to-have (cut for v1): email notifications, admin analytics dashboard</code></pre><h2>Breaking It into Milestones</h2><p>Split the remaining work into a short build plan, for example: Day 1 - schema and models, Day 2 - CRUD endpoints and tests, Day 3 - auth and CI, Day 4 - deployment and README. Writing this plan today, before day 30, is exactly the project-planning skill that keeps real engineering work on schedule instead of sprawling indefinitely.</p>""",
            "key_concepts": ["project scoping", "MVP thinking", "build milestones", "planning before coding"],
            "practical_exercise": {
                "title": "Write Your Final Project Plan",
                "instructions": "Choose your final project idea (a real backend or full-stack application), write a one-paragraph description of what it does, list its must-have v1 features versus nice-to-have features you are cutting, sketch its basic database schema, and write a milestone plan for how you will build it. Submit this plan; it will be the direct starting point for Day 30."
            },
            "quiz": [
                {"question": 'Why is scoping a project into must-have versus nice-to-have features important before starting to build?', "options": ['It focuses effort on a realistic, finishable v1 instead of an overly ambitious, incomplete project', 'Scoping has no effect on whether a project gets finished', 'Nice-to-have features should always be built first', 'Scoping is only relevant for very large teams'], "correct_index": 0, "explanation": 'Clear scoping prevents scope creep and increases the chance of finishing a working version of the project.'},
                {"question": 'What is the main benefit of breaking a project into build milestones before coding?', "options": ['Milestones make the project take longer overall', 'Milestones are only useful for teams larger than one person', 'Milestones replace the need for testing', 'It keeps the work organized and on schedule instead of sprawling indefinitely'], "correct_index": 3, "explanation": 'Milestones break large work into manageable, trackable pieces, helping keep a project on schedule.'},
                {"question": 'According to the lesson, what should you do with features that are not essential to a working first version?', "options": ['Build them first before anything else', 'Explicitly cut them from v1 scope and note them as nice-to-have', 'Ignore the concept of scope entirely', 'Delete the entire project idea'], "correct_index": 1, "explanation": 'Non-essential features should be deliberately deferred from the initial scope so the core, must-have functionality ships first.'}
            ],
            "resources": []
        },
        {
            "day_number": 30,
            "week_number": 6,
            "week_title": "Portfolio and Career Readiness",
            "title": "Final Project: Kick Off Designing, Building, Testing, and Deploying Your Application",
            "learning_objective": "By the end of this class, you will be able to begin executing your final project plan by setting up its repository, schema, and first working endpoint.",
            "duration_minutes": 35,
            "content_html": """<p>Today you begin \"Design, Build, Test, and Deploy a Production-Style Backend Application,\" the capstone of this entire track. Every skill from the last 29 days, Git workflow, clean code, testing, database design, REST APIs, CI, security, documentation, and deployment, comes together in this one project, and it is the piece of work most likely to open doors when you apply for your first developer role or freelance contract.</p><h2>Turning Your Day 29 Plan into Working Code</h2><p>Start executing exactly what you scoped yesterday: initialize a fresh Git repository, set up your virtual environment and requirements.txt, and implement your database schema as SQLAlchemy models first, since every other piece of your API depends on it.</p><pre><code>git init
python -m venv venv && source venv/bin/activate
pip install flask flask-sqlalchemy pytest python-dotenv gunicorn
git add . && git commit -m "Initial project scaffold and models"</code></pre><h2>What Full Completion Looks Like</h2><p>Over the coming days of independent work, build out your CRUD endpoints, write pytest tests covering the core logic, add a GitHub Actions workflow that runs those tests on every push, secure sensitive config with environment variables, write a complete README documenting setup and endpoints, and deploy the finished application to a live URL. Each of these is a skill you already practiced this track; today's job is simply to start, with a real commit in a real repository.</p>""",
            "key_concepts": ["final project kickoff", "project scaffolding", "applying the full engineering lifecycle", "milestone execution"],
            "practical_exercise": {
                "title": "Start Building Your Final Project",
                "instructions": "This IS the start of your final project: initialize a new Git repository for your chosen application, set up a virtual environment with a requirements.txt, implement your planned database schema as SQLAlchemy models, and make your first commit. Submit the GitHub repository URL showing your initial scaffold and models commit as the beginning of your Design, Build, Test, and Deploy a Production-Style Backend Application project."
            },
            "quiz": [
                {"question": "What should today's work be directly based on?", "options": ['A completely new idea, unrelated to previous planning', 'A randomly chosen tutorial project', 'The project plan, schema, and milestones scoped on Day 29', "Someone else's finished GitHub repository"], "correct_index": 2, "explanation": 'Day 30 begins executing the specific plan, schema, and milestones the student already scoped out on Day 29.'},
                {"question": 'Why are database models implemented first, before building CRUD endpoints?', "options": ['Models have no relationship to the rest of the API', 'The API endpoints and business logic depend on the data structures defined in the models', 'Endpoints must always be built before models', 'Testing requires models to be built last'], "correct_index": 1, "explanation": 'Since endpoints read and write data through the models, defining the schema first gives the rest of the API something concrete to build against.'},
                {"question": 'Which of these is explicitly part of what full completion of the final project requires?', "options": ['Only a working local script with no deployment', 'A single Python file with no version control', 'Skipping tests since the project already works locally', 'A live deployment, automated tests, a CI pipeline, and documentation, in addition to working endpoints'], "correct_index": 3, "explanation": 'The final project requires the full engineering lifecycle: tests, CI, security practices, documentation, and live deployment, not just working code.'}
            ],
            "resources": [
                {"label": "GitHub Docs", "url": "https://docs.github.com/"},
                {"label": "Render Documentation", "url": "https://render.com/docs"}
            ]
        }
    ]
}
