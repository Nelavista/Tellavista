"""One-off seed: FUTA's (Federal University of Technology, Akure) schools, departments and
Surveying & GeoInformatics courses, taken only from FUTA's own websites -- see
docs/drive_import/futa_official_structure.md for the page each item was read from (2026-11-01).

Only verified data is seeded:
- Schools are added only when at least one of their departments was read from the school's own
  page (SEET listed no departments; the College of Health Sciences schools were blocked; the
  Postgraduate and Professional Development schools aren't undergraduate) -- an empty school
  would only clutter the faculty picker.
- Department names are FUTA's published link text; only casing and two obvious typos
  ("Computer science", "Cyberecurity") are normalised. Abbreviations ("Mangt.") are kept.
- Courses: only Surveying & GeoInformatics, from svg.futa.edu.ng's course-synopsis pages, with the
  semester FUTA lists. Tagged source='futa_official' (see Course.source) so they're never
  mistaken for NUC CCMAS rows.

seed_ccmas_core.py may already have given FUTA departments under Nelavista's generic faculty
names ("Science", "Faculty of Computing and Information Technology", ...). A FUTA department
that already exists there under the same name is MOVED into its official school (its CCMAS
courses come with it) instead of being duplicated, since Department.name is what students
resolve against. Faculties left empty by that move, and CCMAS departments FUTA's pages don't
list, are reported -- never deleted.

Idempotent. Default is a DRY RUN; pass --apply to write.

Usage:
    python -m scripts.seed.seed_futa_official
    python -m scripts.seed.seed_futa_official --apply
"""
import sys

from app import app, db
from app.models import University, Faculty, Department, Course

FUTA = 'Federal University of Technology, Akure'
COURSE_SOURCE = 'futa_official'

# {school: [department, ...]} -- schools.futa.edu.ng + each school's "Featured Links".
SCHOOLS = {
    'School of Agriculture and Agricultural Technology': [
        'Agricultural & Resource Economics', 'Agricultural Extension & Comm. Tech.',
        'Animal Production and Health', 'Crop, Soil & Pest Mangt.', 'Ecotourism & Wildlife Management',
        'Fisheries & Aquaculture', 'Food Science & Technology', 'Forestry & Wood Technology',
        'Nutrition and Dietetics',
    ],
    'School of Computing': [
        'Computer Science', 'Information Technology', 'Cybersecurity', 'Information Systems',
        'Data Science', 'Software Engineering',
    ],
    'School of Earth and Mineral Sciences': [
        'Applied Geophysics', 'Applied Geology', 'Meteorology', 'Marine Science & Technology',
        'Remote Sensing & GIS',
    ],
    'School of Environmental Technology': [
        'Architecture', 'Building', 'Estate Management', 'Industrial Design', 'Quantity Surveying',
        'Surveying and Geoinformatics', 'Urban & Regional Planning',
    ],
    'School of Physical Sciences': ['Chemistry', 'Mathematics', 'Physics', 'Statistics'],
    'School of Life Sciences': [
        'Biology', 'Biochemistry', 'Microbiology', 'Plant Biology', 'Animal and Environmental Biology',
        'Biotechnology',
    ],
    'School of Logistic and Innovation Technology': [
        'Entrepreneurship Management Tech.', 'Project Management Technology', 'Business Administration',
        'Logistics and Transport Technology', 'Securities and Investment Management Technology',
    ],
}

# svg.futa.edu.ng/home/courses/{100..500} -- (level, semester, code, title), titles verbatim.
# The 500-level page lists no courses.
SVG_DEPARTMENT = 'Surveying and Geoinformatics'
SVG_COURSES = [
    ('100', 'First Semester', 'SVG101', 'Introduction to Surveying and Geoinformatics'),
    ('100', 'First Semester', 'SVG103', 'MAP READINGAND INTERPRETATION'),
    ('100', 'Second Semester', 'SVG102', 'Surveying Instrumentation 1'),
    ('200', 'First Semester', 'SVG201', 'Basic Surveying 1'),
    ('200', 'First Semester', 'SVG203', 'Cadastral Surveying 1'),
    ('200', 'First Semester', 'SVG205', 'Photogrammetry I'),
    ('200', 'First Semester', 'SVG207', 'Field Astronomy'),
    ('200', 'First Semester', 'SVG209', 'Survey Computation'),
    ('200', 'First Semester', 'SVG211', 'Computer Application in Surveying 1'),
    ('200', 'Second Semester', 'SVG202', 'Basic Surveying II'),
    ('200', 'Second Semester', 'SVG204', 'Cadastral Surveying 2'),
    ('200', 'Second Semester', 'SVG206', 'Geodetic Astronomy'),
    ('200', 'Second Semester', 'SVG208', 'SURVEYING CARTOGRAPHY'),
    ('200', 'Second Semester', 'SVG210', 'Computer Application in Surveying 2'),
    ('200', 'Second Semester', 'SVG212', 'Surveying Instrumentation 11'),
    ('300', 'First Semester', 'MTS315', 'Engineering Mathematics'),
    ('300', 'First Semester', 'RSG301', 'Satellite Remote Sensing'),
    ('300', 'First Semester', 'SVG303', 'Photogrammetry II'),
    ('300', 'First Semester', 'SVG305', 'topographic surveying'),
    ('300', 'First Semester', 'SVG307', 'Adjustment Computation I'),
    ('300', 'First Semester', 'SVG309', 'Geodetic Surveying'),
    ('300', 'Second Semester', 'SVG302', 'Engineering Surveying II'),
    ('300', 'Second Semester', 'SVG304', 'Electronic Surveying'),
    ('300', 'Second Semester', 'SVG306', 'Mining and underground Surveying'),
    ('300', 'Second Semester', 'SVG308', 'Adjustment computation II'),
    ('300', 'Second Semester', 'SVG310', 'Spatial Statistics'),
    ('300', 'Second Semester', 'SVG314', 'Safety and swimming in Surveying'),
    ('300', 'Second Semester', 'SVG316', 'DATA QUALITY AND STRUCTURE'),
    ('400', 'First Semester', 'RSG401', 'Geographic Information Systems II'),
    ('400', 'First Semester', 'SVG401', 'Map Projection'),
    ('400', 'First Semester', 'SVG403', 'Hydrographic Surveying 1'),
    ('400', 'First Semester', 'SVG405', 'Digital Photogrammetry'),
    ('400', 'First Semester', 'SVG407', 'Digital Mapping'),
    ('400', 'First Semester', 'SVG409', 'Introduction to Geodesy'),
    ('400', 'First Semester', 'SVG411', 'Potential Theory and Spherical Harmonics'),
]


def seed_futa_official(apply):
    with app.app_context():
        uni = University.query.filter_by(name=FUTA).first()
        if not uni:
            uni = University(name=FUTA, short_name='FUTA')
            db.session.add(uni)
            db.session.flush()
            print(f'University added: {FUTA}')

        existing_depts = {d.name.lower(): d for d in
                          Department.query.join(Faculty).filter(Faculty.university_id == uni.id)}
        official = {name.lower() for depts in SCHOOLS.values() for name in depts}
        schools_added = depts_added = depts_moved = 0
        svg_dept = None

        for school_name, dept_names in SCHOOLS.items():
            school = Faculty.query.filter_by(university_id=uni.id, name=school_name).first()
            if not school:
                school = Faculty(university_id=uni.id, name=school_name)
                db.session.add(school)
                db.session.flush()
                schools_added += 1
            for dept_name in dept_names:
                dept = existing_depts.get(dept_name.lower())
                if dept is None:
                    dept = Department(faculty_id=school.id, name=dept_name)
                    db.session.add(dept)
                    db.session.flush()
                    existing_depts[dept_name.lower()] = dept
                    depts_added += 1
                elif dept.faculty_id != school.id:
                    print(f'  move: {dept.name}  ({dept.faculty.name} -> {school_name})')
                    dept.faculty_id = school.id
                    depts_moved += 1
                if dept_name == SVG_DEPARTMENT:
                    svg_dept = dept

        courses_added = courses_present = 0
        for level, semester, code, title in SVG_COURSES:
            if Course.query.filter_by(department_id=svg_dept.id, level=level, code=code).first():
                courses_present += 1
                continue
            db.session.add(Course(department_id=svg_dept.id, level=level, code=code, title=title,
                                  semester=semester, source=COURSE_SOURCE))
            courses_added += 1
        db.session.flush()

        unlisted = sorted(d.name for key, d in existing_depts.items() if key not in official)
        empty = sorted(f.name for f in Faculty.query.filter_by(university_id=uni.id)
                       if f.name not in SCHOOLS and not Department.query.filter_by(faculty_id=f.id).count())

        print(f'{"APPLY" if apply else "DRY RUN"}: schools +{schools_added}, departments +{depts_added} '
              f'(moved {depts_moved} existing into their official school), '
              f'Surveying courses +{courses_added} ({courses_present} already present)')
        if unlisted:
            print('FUTA departments not on FUTA\'s official school pages (left as-is, review): '
                  + ', '.join(unlisted))
        if empty:
            print('FUTA faculties now empty (left as-is, review): ' + ', '.join(empty))

        if apply:
            db.session.commit()
        else:
            db.session.rollback()


if __name__ == '__main__':
    seed_futa_official('--apply' in sys.argv)
