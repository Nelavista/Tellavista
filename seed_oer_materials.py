"""One-off bulk run of Nelavista's existing OER discovery (the same logic behind
POST /api/fetch-google-materials-batch in routes/google_search_routes.py) across every
distinct course code now in the database, for all 7 universities at once.

Does NOT duplicate that route's logic in spirit -- reuses the exact same service
functions (OPENSTAX_MATERIALS dict lookup, search_open_textbook_library,
search_google_pdfs) and the exact same Material caching/dedup rules, just driven from
a script instead of a per-student HTTP request, since a bulk backfill across ~600
distinct codes isn't something a logged-in student session should trigger.

Sources, in order, matching the existing route:
1. OpenStax (free, no API key, no quota -- open-license textbooks keyed by course code)
2. Open Textbook Library (free, no API key, no quota -- open-license textbooks keyed by
   department; only departments with a verified-good OTL subject slug get results, see
   services/open_textbook_library_service.py's DEPARTMENT_TO_SLUG)
3. Tavily web search (has a monthly quota) -- runs for every code that doesn't already
   have a google_auto material, REGARDLESS of whether OpenStax/OTL found something.
   OTL's department-level textbooks are the same for every level in a department (a
   300-level course gets the same generic OTL result as a 100-level one), so skipping
   Tavily just because OTL found *something* was leaving genuinely course/level-specific
   content undiscovered. A consecutive-failure circuit breaker (not a raw call cap) stops
   Tavily calls once the API itself starts failing (bad key/quota/network), since that's
   the real constraint -- OpenStax/OTL keep running for remaining codes either way.

Materials created here are universal (university=None) since OpenStax/OTL/web-search
results aren't school-specific -- the same textbook applies regardless of which of the
7 universities teaches that course code, matching how Material.university scoping
already works.

Usage:
    python seed_oer_materials.py [--tavily-cap N]
"""
import sys
import time
from app import app, db
from models import Course, Department
from models import Material
from services.google_search_service import OPENSTAX_MATERIALS, search_google_pdfs
from services.open_textbook_library_service import search_open_textbook_library

TAVILY_CAP = 5000  # effectively unbounded -- the real stop condition is the consecutive-
                   # failure circuit breaker below, once Tavily's own API signals it's done
CONSECUTIVE_FAILURE_LIMIT = 6
for arg in sys.argv[1:]:
    if arg.startswith('--tavily-cap'):
        TAVILY_CAP = int(arg.split('=')[1]) if '=' in arg else int(sys.argv[sys.argv.index(arg) + 1])


def seed_oer_materials():
    with app.app_context():
        # {code: department_name} -- one representative department per code (a code
        # shared across departments, e.g. GST111, just needs one department for the
        # OTL department-level lookup; OpenStax/Tavily lookups are code-only anyway).
        rows = db.session.query(Course.code, Department.name).join(
            Department, Course.department_id == Department.id
        ).all()
        code_to_department = {}
        for code, dept_name in rows:
            code_to_department.setdefault(code, dept_name)

        codes = sorted(code_to_department.keys())
        print(f"Distinct course codes to process: {len(codes)}")

        openstax_added = otl_added = tavily_added = skipped_existing = 0
        tavily_used = 0
        tavily_exhausted = False
        consecutive_tavily_failures = 0

        for i, code in enumerate(codes):
            department = code_to_department[code]
            found_anything = False

            # --- 1. OpenStax (free, instant) ---
            for resource in OPENSTAX_MATERIALS.get(code, []):
                existing = Material.query.filter_by(external_url=resource['url'], source='openstax').first()
                if existing:
                    skipped_existing += 1
                    found_anything = True
                    continue
                db.session.add(Material(
                    title=resource['title'], course_code=code, external_url=resource['url'],
                    source='openstax', is_approved=True, uploaded_by='OpenStax',
                    department=department, level='100', semester='First Semester',
                    next_topic=resource.get('description', ''),
                ))
                openstax_added += 1
                found_anything = True

            # --- 2. Open Textbook Library (free, department-keyed) ---
            already_cached_otl = Material.query.filter_by(course_code=code, source='oer_library').first()
            if already_cached_otl:
                skipped_existing += 1
                found_anything = True
            else:
                otl_results, otl_ok = search_open_textbook_library(department, max_results=3)
                for r in otl_results:
                    db.session.add(Material(
                        title=r['title'][:200], course_code=code, external_url=r['url'],
                        source='oer_library', is_approved=True, uploaded_by='Open Textbook Library',
                        department=department, level='100', semester='First Semester',
                        next_topic=r.get('snippet', '')[:190],
                    ))
                    otl_added += 1
                    found_anything = True

            db.session.commit()  # commit per course code -- same rationale as seed_ccmas_core.py:
                                  # this hits a remote DB and outbound HTTP APIs; a dropped
                                  # connection should only cost one code's progress, not the batch.

            # --- 3. Tavily (quota-limited) -- runs for every code lacking google_auto
            # material, regardless of whether OpenStax/OTL already found something, so
            # every level gets real course-specific content instead of a department-
            # generic freebie. Stops once the API itself starts failing repeatedly. ---
            if not tavily_exhausted and tavily_used < TAVILY_CAP:
                already_cached_google = Material.query.filter_by(course_code=code, source='google_auto').first()
                if not already_cached_google:
                    tavily_used += 1
                    results, api_ok = search_google_pdfs(code, max_results=5)
                    if not api_ok:
                        consecutive_tavily_failures += 1
                        if consecutive_tavily_failures >= CONSECUTIVE_FAILURE_LIMIT:
                            tavily_exhausted = True
                            print(f"\n[TAVILY EXHAUSTED] {consecutive_tavily_failures} consecutive API "
                                  f"failures at code {code} ({i+1}/{len(codes)}) -- stopping Tavily calls "
                                  "for the rest of this run. OpenStax/OTL continue for remaining codes.")
                    else:
                        consecutive_tavily_failures = 0
                    for r in results:
                        existing = Material.query.filter_by(external_url=r['url'], source='google_auto').first()
                        if existing:
                            continue
                        db.session.add(Material(
                            title=r['title'][:200], course_code=code, external_url=r['url'],
                            source='google_auto', is_approved=True, uploaded_by='Web Search',
                            department=department, level='100', semester='First Semester',
                        ))
                        tavily_added += 1
                    db.session.commit()

            if (i + 1) % 25 == 0:
                print(f"[{i+1}/{len(codes)}] openstax+={openstax_added} otl+={otl_added} "
                      f"tavily+={tavily_added} (tavily calls used: {tavily_used}/{TAVILY_CAP}) "
                      f"skipped(existing)={skipped_existing}")

            time.sleep(0.2)  # be polite to open.umn.edu / api.tavily.com

        print(f"\nDONE. openstax added: {openstax_added}, otl added: {otl_added}, "
              f"tavily added: {tavily_added} (tavily calls used: {tavily_used}/{TAVILY_CAP}"
              f"{', EXHAUSTED' if tavily_exhausted else ''}), "
              f"skipped (already existed): {skipped_existing}")


if __name__ == '__main__':
    seed_oer_materials()
