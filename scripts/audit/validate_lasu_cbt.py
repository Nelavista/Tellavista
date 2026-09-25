"""Data-integrity validation for the LASU CBT rebuild -- runs the full checklist the
task itself specified, against the live DB, and prints a pass/fail report. Safe to run
any time (read-only); intended to be run before and after
scripts/seed/seed_lasu_cbt_questions.py.

Usage:
    python -m scripts.audit.validate_lasu_cbt
"""
import csv
import os
import sys
from collections import Counter, defaultdict

from app import app, db
from app.models import University, Department, Course, CBTQuestion

CSV_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'Nelavista_Course_Codes.csv')


def load_lasu_catalogue_codes():
    codes = set()
    with open(CSV_PATH, encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            if row['University'].strip() == 'Lagos State University':
                codes.add(row['Course Code'].strip().upper())
    return codes


def validate():
    with app.app_context():
        problems = []
        info = []

        lasu = University.query.filter_by(name='Lagos State University').first()
        if not lasu:
            print('[FAIL] Lagos State University not found in the database.')
            sys.exit(1)

        catalogue_codes = load_lasu_catalogue_codes()
        info.append(f'LASU catalogue: {len(catalogue_codes)} unique course codes (source CSV).')

        # 1. Every catalogue code is recognized (a real Course row exists for it).
        lasu_dept_ids = [d.id for d in Department.query.join(Department.faculty).filter_by(university_id=lasu.id).all()]
        db_codes = {c.code.upper() for c in Course.query.filter(Course.department_id.in_(lasu_dept_ids)).all()}
        missing_from_db = catalogue_codes - db_codes
        if missing_from_db:
            problems.append(f'{len(missing_from_db)} catalogue codes have no Course row: {sorted(missing_from_db)[:20]}')
        else:
            info.append('OK: every LASU catalogue course code has a Course row.')

        # 2. Duplicate Course rows post-normalization: same (department_id, level, code) twice.
        dupe_check = Counter()
        for c in Course.query.filter(Course.department_id.in_(lasu_dept_ids)).all():
            dupe_check[(c.department_id, c.level, c.code.upper())] += 1
        dupes = [k for k, v in dupe_check.items() if v > 1]
        if dupes:
            problems.append(f'{len(dupes)} duplicate (department, level, code) Course rows: {dupes[:10]}')
        else:
            info.append('OK: no duplicate Course rows within any department/level.')

        # 3. Orphaned courses: department_id doesn't resolve.
        orphan_courses = Course.query.filter(
            Course.department_id.in_(lasu_dept_ids), ~Course.department_id.in_(db.session.query(Department.id))
        ).count()
        if orphan_courses:
            problems.append(f'{orphan_courses} Course rows reference a missing department.')
        else:
            info.append('OK: no orphaned Course rows.')

        # --- CBTQuestion checks (LASU-scoped: university_id == lasu.id) ---
        questions = CBTQuestion.query.filter_by(university_id=lasu.id).all()
        info.append(f'CBTQuestion rows tagged to LASU: {len(questions)}')

        codes_with_bank = defaultdict(lambda: {'cbt': 0, 'written': 0})
        for q in questions:
            # 4. Every question has a course code, and it's a real catalogue code.
            if not q.course_code:
                problems.append(f'CBTQuestion id={q.id} has no course_code.')
                continue
            if q.course_code.upper() not in catalogue_codes:
                problems.append(f'CBTQuestion id={q.id} course_code={q.course_code} is not a real LASU catalogue code.')
            codes_with_bank[q.course_code.upper()][q.question_type] += 1

            # 5. No null/broken question text.
            if not q.question_text or not q.question_text.strip():
                problems.append(f'CBTQuestion id={q.id} ({q.course_code}) has null/blank question_text.')

            if q.question_type == 'cbt':
                opts = q.options
                # 6. Valid options; 7. exactly one correct answer that exists among them; 8. no duplicate options.
                if not opts or len(opts) < 2:
                    problems.append(f'CBTQuestion id={q.id} ({q.course_code}) has <2 options.')
                elif len(set(opts)) != len(opts):
                    problems.append(f'CBTQuestion id={q.id} ({q.course_code}) has duplicate options.')
                if q.correct_index is None or not opts or not (0 <= q.correct_index < len(opts)):
                    problems.append(f'CBTQuestion id={q.id} ({q.course_code}) correct_index out of range/null.')
            else:
                if not q.mark_scheme or not q.mark_scheme.strip():
                    problems.append(f'CBTQuestion id={q.id} ({q.course_code}) written question has no mark_scheme.')

        # 9. No obvious duplicate questions within a course.
        text_seen = defaultdict(list)
        for q in questions:
            key = (q.course_code, ' '.join((q.question_text or '').split()).lower())
            text_seen[key].append(q.id)
        for (code, text), ids in text_seen.items():
            if len(ids) > 1:
                problems.append(f'{code}: {len(ids)} duplicate questions (ids={ids}) for "{text[:60]}"')

        # 10. Orphaned questions: course_code doesn't correspond to anything in the catalogue (already checked above).

        # Coverage summary.
        covered = sorted(codes_with_bank.keys())
        info.append(f'Course codes with at least one active question: {len(covered)} / {len(catalogue_codes)}')
        pending = sorted(catalogue_codes - set(covered))
        if pending:
            info.append(f'Pending (no question bank yet): {len(pending)} codes')

        print('=== LASU CBT Data Integrity Report ===\n')
        for line in info:
            print('[INFO]', line)
        print()
        if problems:
            print(f'[FAIL] {len(problems)} problem(s) found:\n')
            for p in problems[:200]:
                print('  -', p)
            if len(problems) > 200:
                print(f'  ... and {len(problems) - 200} more')
        else:
            print('[PASS] No integrity problems found.')

        return problems, pending, covered


if __name__ == '__main__':
    problems, pending, covered = validate()
    sys.exit(1 if problems else 0)
