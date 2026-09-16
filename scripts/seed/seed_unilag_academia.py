"""One-off seed: adds University of Lagos's real, officially-verified Faculty/Department
structure that Nelavista_Course_Codes.csv doesn't cover (that CSV only has UNILAG's 6
"_general" GST rows -- see seed_academia.py). Sourced from official UNILAG subdomain
pages (mgtsci., sosc., engineering., env. .unilag.edu.ng) via web search, September
2026 -- direct fetch of unilag.edu.ng and its subdomains is network-blocked in this
environment, so this is search-snippet-sourced, not a full page read. Re-verify against
the live site before trusting this as final.

IMPORTANT -- what this data is and isn't:
- Faculty/Department names only, NO Course rows: no UNILAG course-code source (like
  LASU's registrar CSV) was found. Every department seeded here therefore resolves to
  an empty course list -- see services/academic_context.py; this is the same "no data
  yet" state materials/CBT already handle gracefully for any other under-populated
  department, not an error. Do not hand-invent course codes to fill this in.
- UNILAG underwent a major restructuring from 12 to 19 faculties effective 2025-08-01
  (unilag.edu.ng/when-the-future-calls-unilag-answers-with-new-faculties-and-a-new-vision/).
  Only faculties where BOTH the faculty name AND a specific, sourced department roster
  could be confirmed are seeded here. Faculties confirmed to exist post-restructuring
  but without a confirmed department roster -- Architecture, Art, Basic Clinical
  Sciences, Basic Medical Sciences, Clinical Sciences, Communication and Media Studies,
  Computing and Informatics, Creative Arts, Dental Sciences, Education, Health
  Professions, Law, Life Sciences, Pharmacy, Physical and Earth Sciences -- are
  deliberately NOT added here. Don't hand-guess their departments; extend
  UNILAG_STRUCTURE below once a real source is found.
- "Mass Communication" is kept under Social Sciences per the Faculty's own official page
  (sosc.unilag.edu.ng), despite the 2025 restructuring announcement implying it split
  off into the new Communication and Media Studies faculty -- the two sources conflict
  and this was not guessed either way. If a future source resolves this, move it here
  (idempotent re-run after editing UNILAG_STRUCTURE).
- "Architecture" is deliberately excluded from Environmental Sciences below (it appears
  to now be its own faculty per the 2025 restructuring) but isn't added as its own
  faculty since its post-split department roster isn't confirmed.

IMPORTANT -- resolution gap (flagged, not silently fixed): resolve_academic_context()
(services/academic_context.py) matches Department.name against User.department, which
in turn only ever gets set to a value the shared FACULTY_DEPARTMENTS picker
(static/js/faculty-departments.js) actually offers -- per this audit's explicit
instruction not to make that shared, non-university-specific picker the source of truth
for UNILAG, it was NOT edited to add UNILAG-only names. That leaves 4 of the 23
departments below unreachable by any student until the picker (or a future
UNILAG-specific picker) offers a matching value -- they're seeded anyway, using
UNILAG's real verified name, because the row itself is correct and future-proof; only
today's *reachability* is the gap:
  - "Actuarial Science and Insurance" (UNILAG's own combined department) -- the picker
    only offers "Actuarial Science" and "Insurance" as separate values.
  - "Building" -- the picker only offers "Building Technology".
  - "Civil and Environmental Engineering" -- the picker only offers "Civil Engineering".
  - "Electrical Engineering" -- the picker only offers "Electrical/Electronics
    Engineering".
"Industrial Relations and Personnel Management" is deliberately seeded here as
"Industrial Relations and Human Resources Management" instead (UNILAG's own site still
uses the old name, same as LASU's -- see faculty-departments.js's IRHRM_DEPARTMENT) so
that a student who searches any of its aliases and picks the one canonical chip in the
picker actually gets a User.department value this script's Department row can resolve.

Usage:
    python -m scripts.seed.seed_unilag_academia
"""
from app import app, db
from app.models import University, Faculty, Department

UNIVERSITY_NAME = 'University of Lagos'

# {faculty_name: [department_name, ...]} -- only faculties with a specific, sourced
# department roster are listed; see module docstring for what's deliberately excluded
# and why.
UNILAG_STRUCTURE = {
    'Management Sciences': [
        'Accounting',
        'Business Administration',
        'Banking and Finance',
        'Industrial Relations and Human Resources Management',
        'Actuarial Science and Insurance',
    ],
    'Social Sciences': [
        'Economics',
        'Geography',
        'Mass Communication',
        'Political Science',
        'Psychology',
        'Sociology',
        'Social Work',
    ],
    'Environmental Sciences': [
        'Building',
        'Estate Management',
        'Urban and Regional Planning',
        'Quantity Surveying',
    ],
    'Engineering': [
        'Civil and Environmental Engineering',
        'Electrical Engineering',
        'Mechanical Engineering',
        'Chemical Engineering',
        'Surveying and Geoinformatics',
        'Metallurgical and Materials Engineering',
        'Biomedical Engineering',
    ],
}


def seed_unilag_academia():
    with app.app_context():
        uni = University.query.filter_by(name=UNIVERSITY_NAME).first()
        if not uni:
            print(f"[WARN] {UNIVERSITY_NAME} not found -- run seed_academia.py first")
            return

        faculties_added = departments_added = skipped = 0
        for faculty_name, dept_names in UNILAG_STRUCTURE.items():
            fac = Faculty.query.filter_by(university_id=uni.id, name=faculty_name).first()
            if not fac:
                fac = Faculty(university_id=uni.id, name=faculty_name)
                db.session.add(fac)
                db.session.flush()
                faculties_added += 1

            for dept_name in dept_names:
                dept = Department.query.filter_by(faculty_id=fac.id, name=dept_name).first()
                if dept:
                    skipped += 1
                    continue
                db.session.add(Department(faculty_id=fac.id, name=dept_name))
                departments_added += 1

            # Commit per faculty, not once at the end -- same reasoning as
            # seed_ccmas_core.py: this runs against a remote DB over the internet, and
            # committing incrementally means a dropped connection only loses the
            # current faculty's progress, and re-running (idempotent via the
            # .filter_by().first() checks above) picks up where it left off.
            db.session.commit()
            print(f"  {faculty_name}: done (faculties added so far: {faculties_added}, departments added: {departments_added})")

        print(f"Faculties added: {faculties_added}   Departments added: {departments_added}   Skipped (already exist): {skipped}")
        print("No Course rows added -- no UNILAG course-code source was found; see module docstring.")


if __name__ == '__main__':
    seed_unilag_academia()
