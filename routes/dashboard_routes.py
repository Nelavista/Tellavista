from flask import Blueprint, render_template, redirect, url_for, session, flash, jsonify, request
from utils.helpers import login_required
from models import User, Material
from extensions import db
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

# ===== STATIC MATERIALS (mirrored from materials.html) =====
STATIC_MATERIALS = [
    { "title": "BCH 101 - Lipids of Biological Importance", "course": "Biochemistry", "level": "100", "semester": "First Semester" },
    { "title": "BCH 101 – Carbohydrates", "course": "Biochemistry", "level": "100", "semester": "First Semester" },
    { "title": "BCH 101 – Amino Acids and Proteins", "course": "Biochemistry", "level": "100", "semester": "First Semester" },
    { "title": "BCH 101 – Macromolecules", "course": "Biochemistry", "level": "100", "semester": "First Semester" },
    { "title": "BCH 101 OER – Past Questions", "course": "Biochemistry", "level": "100", "semester": "First Semester" },
    { "title": "BCH 101 – Brief History of Biochemistry", "course": "Biochemistry", "level": "100", "semester": "First Semester" },
    { "title": "BCH 101 – Multiple Choice Questions", "course": "Biochemistry", "level": "100", "semester": "First Semester" },
    { "title": "History of Biochemistry", "course": "Biochemistry", "level": "100", "semester": "First Semester" },
    { "title": "MAT 101 OER – Likely Exam Questions", "course": "Mathematics", "level": "100", "semester": "First Semester" },
    { "title": "MAT 101 – Questions (DML & Adebanjo)", "course": "Mathematics", "level": "100", "semester": "First Semester" },
    { "title": "MAT 101 – Elementary Mathematics I (Lecture 1)", "course": "Mathematics", "level": "100", "semester": "First Semester" },
    { "title": "MAT 101 – Lecture 2: Theory of Quadratic Equations", "course": "Mathematics", "level": "100", "semester": "First Semester" },
    { "title": "MAT 101 – Lecture 3: Indices and Logarithms", "course": "Mathematics", "level": "100", "semester": "First Semester" },
    { "title": "PHY 101 OER", "course": "Physics", "level": "100", "semester": "First Semester" },
    { "title": "CSC 102 – Introduction to Computing Concepts", "course": "Computer Science", "level": "100", "semester": "Second Semester" },
    { "title": "Types of Documents and Their Structures in LaTeX", "course": "Computer Science", "level": "100", "semester": "Second Semester" },
    { "title": "BIO 101 – Levels of Biological Organization", "course": "Biology", "level": "100", "semester": "First Semester" },
    { "title": "BIO 101 – Meiosis, Gametogenesis, Inheritance and Variation", "course": "Biology", "level": "100", "semester": "First Semester" },
    { "title": "BIO 101 – Biomolecules: Carbohydrates and Lipids", "course": "Biology", "level": "100", "semester": "First Semester" },
    { "title": "BIO 101 – Biomolecules: Proteins and Nucleic Acids", "course": "Biology", "level": "100", "semester": "First Semester" },
    { "title": "BIO 101 – Gametogenesis", "course": "Biology", "level": "100", "semester": "First Semester" },
    { "title": "BIO 101 – Basic Principles of Reproduction and Growth", "course": "Biology", "level": "100", "semester": "First Semester" },
    { "title": "BIO 101 – Proteins and Nucleic Acids", "course": "Biology", "level": "100", "semester": "First Semester" },
    { "title": "BIO 101 – Evolutionary Trends", "course": "Biology", "level": "100", "semester": "First Semester" },
    { "title": "BIO 101 – Diversity of Animals", "course": "Biology", "level": "100", "semester": "First Semester" },
    { "title": "BIO 101 – Microscopy", "course": "Biology", "level": "100", "semester": "First Semester" },
    { "title": "BIO 101 – Cell Structure and Function of Organelles", "course": "Biology", "level": "100", "semester": "First Semester" },
    { "title": "CHM 102 – Homework Practice Questions", "course": "Chemistry", "level": "100", "semester": "Second Semester" },
    { "title": "CHM 101 – Oxidation and Reduction", "course": "Chemistry", "level": "100", "semester": "First Semester" },
    { "title": "CHM 101 – Acids and Bases", "course": "Chemistry", "level": "100", "semester": "First Semester" },
    { "title": "CHM 101 – Atomic Theory Timeline", "course": "Chemistry", "level": "100", "semester": "First Semester" },
    { "title": "CHM 101 – Redox Reactions and Introduction to Electrochemistry", "course": "Chemistry", "level": "100", "semester": "First Semester" },
    { "title": "CHM 101 – Periodicity", "course": "Chemistry", "level": "100", "semester": "First Semester" },
    { "title": "CHM 101 – Rates of Reactions and Equilibrium", "course": "Chemistry", "level": "100", "semester": "First Semester" },
    { "title": "CHM 101 – Modern Electronic Theory of Atoms", "course": "Chemistry", "level": "100", "semester": "First Semester" },
    { "title": "CHM 101 – Atomic and Molecular Structure", "course": "Chemistry", "level": "100", "semester": "First Semester" },
    { "title": "CHM 101 – Hybridization and Shapes of Molecules", "course": "Chemistry", "level": "100", "semester": "First Semester" },
    { "title": "PHY 104 – Electricity and Magnetism", "course": "Physics", "level": "100", "semester": "Second Semester" },
    { "title": "PHY 104 – Oscillation", "course": "Physics", "level": "100", "semester": "Second Semester" },
    { "title": "Trigonometry", "course": "Mathematics", "level": "100", "semester": "First Semester" },
    { "title": "Indices, Surds and Logarithms", "course": "Mathematics", "level": "100", "semester": "First Semester" },
    { "title": "Inequalities", "course": "Mathematics", "level": "100", "semester": "First Semester" },
    { "title": "Theory of Quadratic Equation", "course": "Mathematics", "level": "100", "semester": "First Semester" },
    { "title": "Sequence and Series", "course": "Mathematics", "level": "100", "semester": "First Semester" },
    { "title": "Binomial Expansion", "course": "Mathematics", "level": "100", "semester": "First Semester" },
    { "title": "MAT 161 – Descriptive Statistics (Lecture 1)", "course": "Mathematics", "level": "100", "semester": "First Semester" },
    { "title": "Financial Accounting", "course": "Accounting", "level": "100", "semester": "First Semester" },
    { "title": "A Business Perspective (Managerial Accounting)", "course": "Accounting", "level": "100", "semester": "First Semester" },
    { "title": "Principles Of Accounting Vol 1", "course": "Accounting", "level": "100", "semester": "First Semester" },
    { "title": "Principles of Accounting Vol 2", "course": "Accounting", "level": "100", "semester": "Second Semester" },
    { "title": "Zoology Test", "course": "Zoology", "level": "100", "semester": "First Semester" },
    { "title": "ZOO 102 – Digestive System of Mammals", "course": "Zoology", "level": "100", "semester": "Second Semester" },
    { "title": "PHY 101 OER", "course": "Physics", "level": "100", "semester": "First Semester" },
    { "title": "PHY 101 – General Physics I", "course": "Physics", "level": "100", "semester": "First Semester" },
    { "title": "PHY 101 – Circular Motion", "course": "Physics", "level": "100", "semester": "First Semester" },
    { "title": "PHY 101 – Mechanics and Properties of Matter", "course": "Physics", "level": "100", "semester": "First Semester" },
    { "title": "PHY 101 – Circular and Oscillatory Motion", "course": "Physics", "level": "100", "semester": "First Semester" },
    { "title": "MAT 141 – Mathematics", "course": "Mathematics", "level": "100", "semester": "First Semester" },
    { "title": "MAT 101 – Practice Questions", "course": "Mathematics", "level": "100", "semester": "First Semester" },
    { "title": "MAT 101 – Questions", "course": "Mathematics", "level": "100", "semester": "First Semester" },
    { "title": "Computer Questions and Answers – Basic to Advanced", "course": "Computer Science", "level": "100", "semester": "First Semester" },
    { "title": "CSC 120 OER", "course": "Computer Science", "level": "100", "semester": "First Semester" },
    { "title": "CSC 111 – Possible Questions", "course": "Computer Science", "level": "100", "semester": "First Semester" },
    { "title": "CSC 111 – Past Questions", "course": "Computer Science", "level": "100", "semester": "First Semester" },
    { "title": "CSC 101 – Introduction to Computing", "course": "Computer Science", "level": "100", "semester": "First Semester" },
    { "title": "CSC 111 – Introduction to Internet", "course": "Computer Science", "level": "100", "semester": "First Semester" },
    { "title": "CSC 111 – Introduction to Computer Science", "course": "Computer Science", "level": "100", "semester": "First Semester" },
    { "title": "CSC 111 – Computer Hardware and Software", "course": "Computer Science", "level": "100", "semester": "First Semester" },
    { "title": "CHM 102 – Thermochemistry", "course": "Chemistry", "level": "100", "semester": "Second Semester" },
    { "title": "CHM 101 – Rates of Reactions", "course": "Chemistry", "level": "100", "semester": "First Semester" },
    { "title": "CHM 101 – Radioactivity", "course": "Chemistry", "level": "100", "semester": "First Semester" },
    { "title": "Principles of Financial Accounting", "course": "Accounting", "level": "100", "semester": "First Semester" },
    { "title": "Training Manual for Organic Agriculture", "course": "Agriculture", "level": "100", "semester": "First Semester" },
    { "title": "Introduction to Business Administration", "course": "Business Administration", "level": "100", "semester": "First Semester" },
    { "title": "Business Fundamentals – 1st Edition", "course": "Business Administration", "level": "100", "semester": "First Semester" },
    { "title": "Material II", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "CISC and RISC", "course": "Information Technology", "level": "200", "semester": "First Semester" },
    { "title": "CSC 207 Test 2", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "ENT 211 Compilation", "course": "Entrepreneurship", "level": "200", "semester": "First Semester" },
    { "title": "CSC 221 Course Content", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "Data Structure I", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "Data Structure II", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "CSC217 Lecture 1", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "CSC217 Lecture 2", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "CSC217 Lecture 3", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "Compiler Construction Note II", "course": "Computer Science", "level": "300", "semester": "First Semester" },
    { "title": "CSC217 Lecture 4", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "CSC217 Key Points & Practice Questions", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "Compiler Note II", "course": "Computer Science", "level": "300", "semester": "First Semester" },
    { "title": "Lecture 1: Real-Valued Functions of a Real Variable", "course": "Mathematics", "level": "200", "semester": "First Semester" },
    { "title": "Lecture: Multiple Integrals", "course": "Mathematics", "level": "200", "semester": "First Semester" },
    { "title": "Lecture: Evaluation of Line Integrals", "course": "Mathematics", "level": "200", "semester": "First Semester" },
    { "title": "Lecture 8: Increments, Differentials and Linear Approximations", "course": "Mathematics", "level": "200", "semester": "First Semester" },
    { "title": "Lecture 7: Partial Derivatives and Applications", "course": "Mathematics", "level": "200", "semester": "First Semester" },
    { "title": "Lecture 6: Real-Valued Functions of Two or Three Variables", "course": "Mathematics", "level": "200", "semester": "First Semester" },
    { "title": "Lecture 5: Taylor Series", "course": "Mathematics", "level": "200", "semester": "First Semester" },
    { "title": "Lecture 4: Mean Value Theorem", "course": "Mathematics", "level": "200", "semester": "First Semester" },
    { "title": "Lecture 3: Applications of Differentiation and Integration", "course": "Mathematics", "level": "200", "semester": "First Semester" },
    { "title": "Lecture 2: Review of Differentiation and Integration", "course": "Mathematics", "level": "200", "semester": "First Semester" },
    { "title": "Operating System Note I", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "Operating System", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "CSC 207 Note 1", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "IFT 219 Note I", "course": "Information Technology", "level": "200", "semester": "First Semester" },
    { "title": "Digital Logic Circuit Analysis and Design", "course": "Information Technology", "level": "200", "semester": "First Semester" },
    { "title": "Hashing", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "Queues", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "Stacks", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "Complexity Analysis of Algorithms", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "GLT 201 – Instrument Maintenance", "course": "Science Laboratory Technology", "level": "200", "semester": "First Semester" },
    { "title": "Trees I", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "Trees III", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "Tree II", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "CSC 213 Note 1", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "Complexity IV", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "Complexity III", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "Algorithm Design Techniques and Analysis", "course": "Computer Science", "level": "200", "semester": "First Semester" },
    { "title": "Genetics, Agriculture, and Biotechnology", "course": "Agriculture", "level": "100", "semester": "First Semester" },
    { "title": "Plant Breeding Methods", "course": "Agriculture", "level": "100", "semester": "First Semester" },
    { "title": "DBMS II – Transaction Processing", "course": "Computer Science", "level": "200", "semester": "First Semester" },
]


@dashboard_bp.route('/')
def landing():
    user = session.get('user')
    if user:
        return redirect(url_for('dashboard.dashboard'))
    return render_template('landing.html')


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    user_data = session.get('user')
    if not user_data:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(username=user_data['username']).first()
    if user and not user.department:
        flash('Please complete your academic profile to continue.', 'warning')
        return redirect(url_for('profile.profile'))

    if user and user.name:
        first_name = user.name.strip().split()[0]
    else:
        first_name = user_data.get('username', 'Student')

    exam_key = f"exams_{user_data.get('username')}"
    exams_list = session.get(exam_key, [])
    upcoming = [
        e for e in exams_list
        if e.get('date') and e['date'] >= datetime.now().strftime('%Y-%m-%d')
    ]
    exam_count = len(upcoming)

    return render_template('index.html',
                           user=user_data,
                           first_name=first_name,
                           exam_count=exam_count)


@dashboard_bp.route('/api/track-session', methods=['POST'])
@login_required
def track_session():
    user_data = session.get('user')
    username = user_data.get('username')
    data = request.get_json()
    seconds = data.get('seconds', 0)
    week_key = f"study_time_{username}_{datetime.now().strftime('%Y_W%U')}"
    current = session.get(week_key, {})
    today = datetime.now().strftime('%A')[:3]
    current[today] = current.get(today, 0) + seconds
    session[week_key] = current
    session.modified = True
    return jsonify({'status': 'ok', 'tracked': seconds})


@dashboard_bp.route('/api/study-stats')
@login_required
def study_stats():
    user_data = session.get('user')
    username = user_data.get('username')
    week_key = f"study_time_{username}_{datetime.now().strftime('%Y_W%U')}"
    raw = session.get(week_key, {})
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    hours = {day: round(raw.get(day, 0) / 3600, 1) for day in days}
    total = round(sum(hours.values()), 1)
    return jsonify({'days': hours, 'total': total})


@dashboard_bp.route('/api/exams', methods=['GET', 'POST'])
@login_required
def exams():
    user_data = session.get('user')
    username = user_data.get('username')
    exam_key = f"exams_{username}"
    if request.method == 'POST':
        data = request.get_json()
        exams_list = session.get(exam_key, [])
        exams_list.append({
            'id': str(datetime.now().timestamp()),
            'course': data.get('course'),
            'date': data.get('date'),
            'duration': data.get('duration', '')
        })
        session[exam_key] = exams_list
        session.modified = True
        return jsonify({'status': 'ok'})
    exams_list = session.get(exam_key, [])
    return jsonify({'exams': exams_list})


@dashboard_bp.route('/api/user-courses')
@login_required
def user_courses():
    user_data = session.get('user')
    username = user_data.get('username')
    user = User.query.filter_by(username=username).first()

    if not user or not user.level:
        return jsonify({
            'courses': [],
            'message': 'Set your level in profile to see your courses'
        })

    if not user.semester:
        return jsonify({
            'courses': [],
            'message': 'Set your semester in profile to see your courses'
        })

    level = user.level.strip()
    semester = user.semester.strip()
    department = (user.department or '').strip()

    # Step 1 — Filter static materials by level + semester + department
    matched = [
        m for m in STATIC_MATERIALS
        if m['level'] == level
        and m['semester'] == semester
        and m['course'].lower() == department.lower()
    ]

    # Step 2 — If no exact department match, fall back to all materials
    # for that level + semester so dashboard always shows something
    if not matched:
        matched = [
            m for m in STATIC_MATERIALS
            if m['level'] == level
            and m['semester'] == semester
        ]

    # Step 3 — Also check database Material table and merge
    try:
        db_courses = Material.query.filter_by(
            level=level,
            semester=semester,
            is_approved=True
        ).limit(6).all()

        for c in db_courses:
            matched.append({
                'title': c.course,
                'course': c.course,
                'level': c.level,
                'semester': c.semester
            })
    except Exception:
        pass

    # Deduplicate by title and limit to 6
    seen = set()
    unique = []
    for m in matched:
        title = m.get('title', m.get('course', ''))
        if title not in seen:
            seen.add(title)
            unique.append(m)

    unique = unique[:6]

    courses_data = [{
        'name': m.get('title', m.get('course', 'Unknown')),
        'type': 'CORE',
        'next_topic': '',
        'progress': 0
    } for m in unique]

    return jsonify({
        'courses': courses_data,
        'level': level,
        'semester': semester,
        'department': department,
        'count': len(courses_data)
    })


@dashboard_bp.route('/api/debug-courses')
@login_required
def debug_courses():
    user_data = session.get('user')
    user = User.query.filter_by(username=user_data.get('username')).first()
    user_info = {
        'level': user.level,
        'semester': user.semester,
        'department': user.department
    }
    all_materials = Material.query.limit(10).all()
    materials_info = [{
        'course': c.course,
        'level': c.level,
        'semester': c.semester,
        'is_approved': c.is_approved
    } for c in all_materials]
    return jsonify({
        'user': user_info,
        'all_materials_in_db': materials_info,
        'total_materials': len(materials_info)
    })


@dashboard_bp.route('/api/debug-all')
@login_required
def debug_all():
    from models import Video, Material
    all_videos = Video.query.limit(10).all()
    videos_info = [{
        'course': v.course,
        'level': v.level,
        'semester': v.semester,
        'department': v.department,
        'is_approved': v.is_approved
    } for v in all_videos]
    all_materials = Material.query.limit(10).all()
    materials_info = [{
        'course': c.course,
        'level': c.level,
        'semester': c.semester,
        'is_approved': c.is_approved
    } for c in all_materials]
    return jsonify({
        'videos_in_db': videos_info,
        'total_videos': len(videos_info),
        'materials_in_db': materials_info,
        'total_materials': len(materials_info)
    })


@dashboard_bp.route('/api/debug-tables')
@login_required
def debug_tables():
    from sqlalchemy import inspect, text
    with db.engine.connect() as conn:
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        table_counts = {}
        for table in tables:
            try:
                result = conn.execute(text(f'SELECT COUNT(*) FROM "{table}"'))
                count = result.scalar()
                table_counts[table] = count
            except Exception:
                table_counts[table] = 'error'
    return jsonify({
        'all_tables': tables,
        'row_counts': table_counts
    })
