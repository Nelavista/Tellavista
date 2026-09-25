"""Idempotent loader: reads every course-code JSON file in
data/cbt_question_banks/lasu/ and upserts its questions into CBTQuestion, scoped to
Lagos State University (see app/models.py's "CBT PERSISTENCE" section and
app/services/cbt_bank.py, the single place that queries course_code).

Each JSON file is {course_code, title, level, source_note, questions: [...]}. A
question is either an MCQ (question/options/correct_answer/explanation/topic/difficulty)
or, for SIWES/Research-Project/Seminar codes, a written/self-marked item
(question/mark_scheme/topic). Every course_code is validated against the real LASU
catalogue (data/Nelavista_Course_Codes.csv) before anything is written -- a JSON file
naming a code that isn't actually a LASU course is refused, not silently imported. The
catalogue's own conflicting titles (the same code filed under two different titles by
different departments in the source CSV) are resolved here via CANONICAL_TITLE_OVERRIDES,
each with a one-line reason -- see the task's own "investigate before choosing a title"
requirement.

Usage:
    python -m scripts.seed.seed_lasu_cbt_questions [--dry-run]
"""
import argparse
import csv
import json
import os
import sys

from app import app, db
from app.models import University, CBTQuestion

CSV_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'Nelavista_Course_Codes.csv')
BANK_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'cbt_question_banks', 'lasu')

# The 26 LASU course codes the source CSV files under two different titles (different
# departments' own registrar submissions disagree). Resolved here rather than left
# ambiguous -- see the "COURSE CODE NORMALIZATION" section of the task and this repo's
# scripts/seed/seed_academia.py, which correctly keeps each department's own Course row
# untouched (this override only affects the CBT catalogue's single canonical display
# title/search result, never the per-department Course.title rows).
CANONICAL_TITLE_OVERRIDES = {
    # Wording-only variants -- majority/fuller phrasing wins.
    'BIO101': ('General Biology I', 'Majority of departments (9/10) use this title; Biochemistry\'s "Basic Biology I" is an outlier wording of the same course.'),
    'BIO102': ('General Biology II', 'Majority of departments (5/6) use this title; Biochemistry\'s "Basic Biology II" is an outlier wording.'),
    'CSC101': ('Introduction to Computer Science', 'Computer Science and Information Technology (the owning departments) both use this fuller wording over "Intro to Computer Science".'),
    'CSC213': ('Data Structures & Algorithm Analysis', 'Computer Science (owning department) uses this fuller title; Information Technology\'s "Data Structures" is a shortened variant.'),
    'MTH101': ('Elementary Mathematics I', 'Mathematics (owning department) plus 6 other departments use this title; Biochemistry/Biology\'s "General Mathematics I" is a local variant.'),
    'MTH102': ('Elementary Mathematics II', 'Mathematics (owning department) plus 6 other departments use this title; Biochemistry\'s "General Mathematics II" is a local variant.'),
    'PHY107': ('General Practical Physics I', 'Physics (owning department) plus 5 other departments use this title; Biochemistry/Biology\'s "Experimental Physics I" is a local variant.'),
    'PHY108': ('General Practical Physics II', 'Physics (owning department) plus 6 other departments use this title; Biochemistry\'s "Experimental Physics II" is a local variant.'),
    # Genuinely different subject matter under the same code at different departments --
    # the owning department's (i.e. the department the subject prefix names) own title
    # is kept as canonical; the alternate is a different department's local mapping of
    # the same code, not authored under this canonical title.
    'CHM201': ('Physical Chemistry I', 'Chemistry (owning department) files this code as Physical Chemistry I; Biology\'s "Organic Chemistry I" is that department\'s own local mapping of the same code.'),
    'CHM202': ('Physical Chemistry II', 'Chemistry (owning department) files this code as Physical Chemistry II.'),
    'CHM205': ('Organic Chemistry I', 'Chemistry (owning department) files this code as Organic Chemistry I; Biochemistry\'s "Physical Chemistry I" for this code (the inverse of CHM201) suggests a departmental cross-listing quirk, not an error to silently "fix".'),
    'CHM207': ('Analytical Chemistry I', 'Chemistry (owning department) files this code as Analytical Chemistry I.'),
    'CHM208': ('Analytical Chemistry II', 'Chemistry (owning department) files this code as Analytical Chemistry II.'),
    'CHM303': ('Inorganic Chemistry III', 'Chemistry (owning department) files this code as Inorganic Chemistry III.'),
    'CHM401': ('Advanced Physical Chemistry', 'Chemistry (owning department) files this code as Advanced Physical Chemistry.'),
    'CSC102': ('Introduction to Computing', 'Computer Science and Information Technology (owning departments) both use this title; Mathematics\' "Intro to Problem Solving" appears to be a different locally-mapped course under the same code.'),
    'CSC201': ('Computer Organization', 'Computer Science and Information Technology (owning departments) both use this title.'),
    'CSC401': ('Advanced Algorithms', 'Computer Science (owning department) files this code as Advanced Algorithms; Information Technology\'s "IT Project Management" is that department\'s own mapping of the same code.'),
    'CSC411': ('Distributed Systems', 'Computer Science (owning department) files this code as Distributed Systems; Information Technology\'s "Information Security" is that department\'s own mapping of the same code.'),
    'MCB201': ('General Microbiology I', 'Majority (Microbiology and Biology) use this numbered title, consistent with MCB202 "General Microbiology II" elsewhere in the catalogue.'),
    'MCB301': ('Bacteriology', 'Microbiology (owning department) files this code as Bacteriology.'),
    'MCB305': ('Mycology', 'Microbiology (owning department) files this code as Mycology.'),
    'MCB401': ('Advanced Microbial Genetics', 'Microbiology (owning department) files this code as Advanced Microbial Genetics.'),
    'MCB408': ('Advanced Immunology', 'Microbiology (owning department) files this code as Advanced Immunology.'),
    'PHY201': ('Electricity & Magnetism I', 'Physics (owning department) files this code as Electricity & Magnetism I.'),
    'PHY202': ('Electricity & Magnetism II', 'Physics (owning department) files this code as Electricity & Magnetism II.'),
}

# Codes whose real content is SIWES / a research project / a departmental seminar --
# never given fabricated subject-trivia MCQs (see the task's own instruction #10).
# Derived by scanning the source CSV for these exact title patterns, not guessed.
NON_EXAM_CODES = {
    'ACC499', 'AGR399', 'AGR499', 'BCH399', 'BCH409', 'BCH499', 'BIO399', 'BIO407',
    'BIO499', 'BOT399', 'BOT412', 'BOT413', 'BUS499', 'CHM399', 'CHM404', 'CHM411',
    'CSC499', 'ENT499', 'FIS399', 'FIS404', 'FIS409', 'MCB399', 'MCB404', 'MCB409',
    'MTH299', 'MTH399', 'MTH404', 'PHY399', 'PHY404', 'PHY409', 'SLT399', 'SLT404',
    'SLT407', 'ZOO399', 'ZOO499',
}


def load_catalogue():
    """code -> canonical title, for every unique LASU course code in the source CSV."""
    catalogue = {}
    with open(CSV_PATH, encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            if row['University'].strip() != 'Lagos State University':
                continue
            code = row['Course Code'].strip().upper()
            title = row['Course Name'].strip()
            if code not in catalogue:
                catalogue[code] = title
    for code, (title, _reason) in CANONICAL_TITLE_OVERRIDES.items():
        if code in catalogue:
            catalogue[code] = title
    return catalogue


def _validate_mcq(code, q, errors):
    required = ('question', 'options', 'correct_answer', 'explanation')
    for field in required:
        if not q.get(field):
            errors.append(f'{code}: MCQ missing "{field}": {q.get("question", "?")[:60]}')
            return False
    options = q['options']
    if not isinstance(options, list) or len(options) < 2:
        errors.append(f'{code}: MCQ needs >=2 options: {q["question"][:60]}')
        return False
    if len(set(options)) != len(options):
        errors.append(f'{code}: MCQ has duplicate options: {q["question"][:60]}')
        return False
    if q['correct_answer'] not in options:
        errors.append(f'{code}: correct_answer not among options: {q["question"][:60]}')
        return False
    return True


def _validate_written(code, q, errors):
    if not q.get('question') or not q.get('mark_scheme'):
        errors.append(f'{code}: written question missing question/mark_scheme: {q.get("question", "?")[:60]}')
        return False
    return True


def load_bank_files(catalogue, errors):
    """Reads every *.json in BANK_DIR, validates structurally, returns
    {course_code: [rows...]} of rows ready to upsert."""
    banks = {}
    if not os.path.isdir(BANK_DIR):
        return banks
    for fname in sorted(os.listdir(BANK_DIR)):
        if not fname.endswith('.json'):
            continue
        path = os.path.join(BANK_DIR, fname)
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        code = data['course_code'].strip().upper()
        if code not in catalogue:
            errors.append(f'{fname}: course_code {code} is not in the LASU catalogue -- skipped')
            continue
        rows = []
        for q in data.get('questions', []):
            is_written = 'mark_scheme' in q
            ok = _validate_written(code, q, errors) if is_written else _validate_mcq(code, q, errors)
            if not ok:
                continue
            rows.append({
                'course_code': code,
                'subject_code': ''.join(ch for ch in code if ch.isalpha()),
                'question_type': 'written' if is_written else 'cbt',
                'question_text': q['question'],
                'options': q.get('options'),
                'correct_index': q['options'].index(q['correct_answer']) if not is_written else None,
                'explanation': q.get('explanation'),
                'mark_scheme': q.get('mark_scheme'),
                'topic': q.get('topic'),
                'difficulty': q.get('difficulty'),
                'source_note': data.get('source_note'),
            })
        if rows:
            banks.setdefault(code, []).extend(rows)
    # Duplicate-question check across a course's own bank (case/whitespace-insensitive).
    for code, rows in banks.items():
        seen = {}
        for r in rows:
            key = ' '.join(r['question_text'].split()).lower()
            seen.setdefault(key, 0)
            seen[key] += 1
        for key, count in seen.items():
            if count > 1:
                errors.append(f'{code}: {count} duplicate/near-duplicate questions for "{key[:60]}"')
    return banks


def seed_lasu_cbt_questions(dry_run=False):
    with app.app_context():
        lasu = University.query.filter_by(name='Lagos State University').first()
        if not lasu:
            print('[ERROR] Lagos State University not found -- run scripts/seed/seed_academia.py first')
            sys.exit(1)

        catalogue = load_catalogue()
        errors = []
        banks = load_bank_files(catalogue, errors)

        if errors:
            print(f'[VALIDATION] {len(errors)} problem(s) found -- these rows were skipped:')
            for e in errors[:50]:
                print('  -', e)
            if len(errors) > 50:
                print(f'  ... and {len(errors) - 50} more')

        # One bulk fetch of every existing (course_code, question_type, question_text) ->
        # row for the courses we're about to touch, instead of a query per question --
        # the difference between ~10 queries and several thousand against the remote DB.
        codes = list(banks.keys())
        existing_rows = CBTQuestion.query.filter(CBTQuestion.course_code.in_(codes)).all() if codes else []
        existing_by_key = {(q.course_code, q.question_type, q.question_text): q for q in existing_rows}

        added = updated = skipped = 0
        new_objects = []
        for code, rows in banks.items():
            for r in rows:
                key = (r['course_code'], r['question_type'], r['question_text'])
                existing = existing_by_key.get(key)
                if existing:
                    if dry_run:
                        skipped += 1
                        continue
                    existing.explanation = r['explanation']
                    existing.mark_scheme = r['mark_scheme']
                    existing.topic = r['topic']
                    existing.difficulty = r['difficulty']
                    existing.source_note = r['source_note']
                    existing.is_active = True
                    if r['options'] is not None:
                        existing.options = r['options']
                        existing.correct_index = r['correct_index']
                    updated += 1
                    continue
                if dry_run:
                    added += 1
                    continue
                q = CBTQuestion(
                    subject_code=r['subject_code'], course_code=r['course_code'],
                    question_type=r['question_type'], question_text=r['question_text'],
                    correct_index=r['correct_index'], explanation=r['explanation'],
                    mark_scheme=r['mark_scheme'], topic=r['topic'], difficulty=r['difficulty'],
                    source_note=r['source_note'], university_id=lasu.id,
                )
                if r['options'] is not None:
                    q.options = r['options']
                new_objects.append(q)
                added += 1

        if not dry_run:
            if new_objects:
                db.session.bulk_save_objects(new_objects)
            db.session.commit()

        print(f"\nCourses with a bank on disk: {len(banks)}")
        print(f"Questions added: {added}   Updated: {updated}   Unchanged/skipped: {skipped}")
        if dry_run:
            print("[DRY RUN] Nothing was written to the database.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='Validate and report without writing to the DB')
    args = parser.parse_args()
    seed_lasu_cbt_questions(dry_run=args.dry_run)
