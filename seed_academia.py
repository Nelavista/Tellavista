"""One-off seed: loads Nelavista_Course_Codes.csv (real curriculum data for Lagos
State University, University of Lagos, University of Ibadan -- 676 rows of
University/Department/Level/Course Code/Course Name) into the normalized
University -> Faculty -> Department -> Course tables (see models.py's "ACADEMIA
TAXONOMY" section). Idempotent -- safe to re-run after a CSV update or a partial run.

Usage:
    python seed_academia.py
"""
import csv
import os

from app import app, db
from models import University, Faculty, Department, Course

CSV_PATH = os.path.join(os.path.dirname(__file__), 'Nelavista_Course_Codes.csv')

# The CSV has no Faculty column, so this mapping is a deliberate product decision for
# LASU's 16 real departments -- derived from the faculty groupings already used for
# these exact department names in static/js/faculty-departments.js (its
# "hasCurriculum: true" departments are precisely LASU's real curriculum-backed ones).
# It is NOT verified against LASU's official faculty handbook -- if a department is
# later confirmed to sit under a different faculty, fix this dict and re-run this
# script (idempotent), don't hand-edit the database.
FACULTY_MAP = {
    'Biochemistry': 'Science',
    'Mathematics': 'Science',
    'Botany': 'Science',
    'Chemistry': 'Science',
    'Fisheries': 'Science',
    'Microbiology': 'Science',
    'Physics': 'Science',
    'Science Laboratory Technology': 'Science',
    'Biology': 'Science',
    'Computer Science': 'Science',
    'Zoology': 'Science',
    'Accounting': 'Management Sciences',
    'Business Administration': 'Management Sciences',
    'Entrepreneurship': 'Management Sciences',
    'Agriculture': 'Agriculture',
    'Information Technology': 'Computing',
}

# The CSV's "_general" department (UNILAG/UI's GST/GES-style general-studies courses)
# applies university-wide, not to one real faculty -- modeling it as a dedicated
# pseudo-faculty/department avoids pretending it belongs to "Science" or similar.
GENERAL_STUDIES_FACULTY = 'General Studies'
GENERAL_STUDIES_DEPT = 'General Studies (GST)'

UNIVERSITY_SHORT_NAMES = {
    'Lagos State University': 'LASU',
    'University of Lagos': 'UNILAG',
    'University of Ibadan': 'UI',
    'Federal University Dutsin-Ma': 'FUDMA',
    'University of Abuja': 'UNIABUJA',
    'University of Ilorin': 'UNILORIN',
    'Kwara State University': 'KWASU',
    'University of Port Harcourt': 'UNIPORT',
}

# Universities selectable in the student-facing university picker (see
# profile_completion_modal.html / profile.html) that have NO verified course-code
# data yet -- unlike Nelavista_Course_Codes.csv's rows below, these must not get
# invented Faculty/Department/Course rows. Ensured to exist as bare University rows
# only, so a student from one of these schools resolves to a real, correctly-named
# university and gets an honest "your courses aren't mapped yet" state (see
# services/academic_context.py) rather than an unresolved/blank one, while an admin
# can add their real faculties/departments/courses later via /admin/academia.
ACTIVE_UNIVERSITIES_WITHOUT_TAXONOMY_YET = [
    'Federal University Dutsin-Ma',
    'University of Abuja',
    'University of Ilorin',
    'Kwara State University',
    'University of Port Harcourt',
]


def ensure_active_universities():
    added = 0
    for uni_name in ACTIVE_UNIVERSITIES_WITHOUT_TAXONOMY_YET:
        if not University.query.filter_by(name=uni_name).first():
            db.session.add(University(name=uni_name, short_name=UNIVERSITY_SHORT_NAMES.get(uni_name)))
            added += 1
    if added:
        db.session.commit()
    return added


def seed_academia():
    with app.app_context():
        added = ensure_active_universities()
        if added:
            print(f"Universities added (no course data yet -- add via /admin/academia): {added}")

        with open(CSV_PATH, encoding='utf-8-sig') as f:
            rows = list(csv.DictReader(f))

        universities, faculties, departments = {}, {}, {}
        courses_added = skipped = 0
        unmapped = set()

        for row in rows:
            uni_name = row['University'].strip()
            dept_name = row['Department'].strip()
            level = row['Level'].strip()
            code = row['Course Code'].strip()
            title = row['Course Name'].strip()
            if not (uni_name and dept_name and level and code and title):
                continue

            if uni_name not in universities:
                uni = University.query.filter_by(name=uni_name).first()
                if not uni:
                    uni = University(name=uni_name, short_name=UNIVERSITY_SHORT_NAMES.get(uni_name))
                    db.session.add(uni)
                    db.session.flush()
                universities[uni_name] = uni
            uni = universities[uni_name]

            if dept_name == '_general':
                faculty_name, real_dept_name = GENERAL_STUDIES_FACULTY, GENERAL_STUDIES_DEPT
            else:
                faculty_name = FACULTY_MAP.get(dept_name)
                if not faculty_name:
                    unmapped.add((uni_name, dept_name))
                    continue
                real_dept_name = dept_name

            fac_key = (uni_name, faculty_name)
            if fac_key not in faculties:
                fac = Faculty.query.filter_by(university_id=uni.id, name=faculty_name).first()
                if not fac:
                    fac = Faculty(university_id=uni.id, name=faculty_name)
                    db.session.add(fac)
                    db.session.flush()
                faculties[fac_key] = fac
            fac = faculties[fac_key]

            dept_key = (uni_name, faculty_name, real_dept_name)
            if dept_key not in departments:
                dept = Department.query.filter_by(faculty_id=fac.id, name=real_dept_name).first()
                if not dept:
                    dept = Department(faculty_id=fac.id, name=real_dept_name)
                    db.session.add(dept)
                    db.session.flush()
                departments[dept_key] = dept
            dept = departments[dept_key]

            exists = Course.query.filter_by(department_id=dept.id, level=level, code=code).first()
            if exists:
                skipped += 1
                continue
            db.session.add(Course(department_id=dept.id, level=level, code=code, title=title))
            courses_added += 1

        db.session.commit()

        for uni_name, dept_name in sorted(unmapped):
            print(f"[WARN] Skipped unmapped department: {uni_name} / {dept_name} -- add it to FACULTY_MAP")

        print(f"Universities: {len(universities)}  Faculties: {len(faculties)}  Departments: {len(departments)}")
        print(f"Courses added: {courses_added}   Skipped (already exist): {skipped}")


if __name__ == '__main__':
    seed_academia()
