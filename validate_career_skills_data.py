"""Standalone validator for seed_data/career_skills/<slug>.py curriculum files — no Flask
app / DB needed, so it can be run the moment each authoring batch lands. Checks structural
correctness (30 days, quiz shape, rubric sum) and flags likely placeholder/generic titles.
Content quality itself still needs a human/LLM read-through — this only catches mechanical
schema violations that would break the DB seed.

Run with: venv/Scripts/python.exe validate_career_skills_data.py
"""
import importlib
import pathlib
import re

BANNED_TITLE_PATTERNS = [
    r'^introduction$', r'^overview$', r'^advanced topic$', r'^lesson \d+$',
    r'^day \d+$', r'^getting started$', r'^wrap[\s-]?up$', r'^review$',
    r'^miscellaneous topics?$', r'^coming soon$', r'^tbd$', r'^more about',
]
BANNED_RE = re.compile('|'.join(BANNED_TITLE_PATTERNS), re.IGNORECASE)

EXPECTED_SLUGS = [
    'ai-machine-learning', 'generative-ai-engineering', 'software-engineering',
    'data-analysis-bi', 'data-engineering', 'web-development', 'mobile-app-development',
    'cloud-computing-devops', 'cybersecurity', 'ui-ux-design', 'digital-marketing',
    'sales-business-development', 'content-creation', 'video-production-motion-design',
    'product-management', 'project-operations-management', 'fintech-financial-analysis',
    'advanced-excel-automation', 'renewable-energy-sustainability', 'professional-workplace-skills',
]


def validate(slug, data):
    errors = []
    warnings = []

    for key in ('slug', 'name', 'tagline', 'description', 'level', 'estimated_hours',
                'course_title', 'course_description', 'final_project', 'days'):
        if key not in data:
            errors.append(f"missing top-level key: {key}")
    if errors:
        return errors, warnings

    if data['slug'] != slug:
        errors.append(f"slug mismatch: file says {data['slug']!r}, expected {slug!r}")

    days = data['days']
    if len(days) != 30:
        errors.append(f"expected exactly 30 days, got {len(days)}")

    day_numbers = [d.get('day_number') for d in days]
    if sorted(day_numbers) != list(range(1, 31)):
        errors.append(f"day_number set is not exactly 1..30: {sorted(set(day_numbers))} (count={len(day_numbers)})")

    seen_titles = set()
    for d in days:
        dn = d.get('day_number')
        title = (d.get('title') or '').strip()
        if not title:
            errors.append(f"day {dn}: missing title")
        elif BANNED_RE.match(title.strip()):
            errors.append(f"day {dn}: banned generic title: {title!r}")
        norm = title.lower().strip()
        if norm in seen_titles:
            errors.append(f"day {dn}: duplicate title also used by another day: {title!r}")
        seen_titles.add(norm)

        wn = d.get('week_number')
        expected_week = ((dn - 1) // 5) + 1 if isinstance(dn, int) else None
        if wn != expected_week:
            warnings.append(f"day {dn}: week_number={wn}, expected {expected_week} for 5-day weeks")

        if not d.get('learning_objective', '').startswith('By the end of this class'):
            warnings.append(f"day {dn}: learning_objective doesn't start with the expected phrasing")

        content = d.get('content_html') or ''
        word_count = len(re.sub('<[^<]+?>', ' ', content).split())
        if word_count < 100:
            errors.append(f"day {dn}: content_html looks too thin ({word_count} words)")

        quiz = d.get('quiz') or []
        if len(quiz) != 3:
            errors.append(f"day {dn}: expected 3 quiz questions, got {len(quiz)}")
        correct_indices = []
        for qi, q in enumerate(quiz):
            opts = q.get('options') or []
            if len(opts) != 4:
                errors.append(f"day {dn} quiz {qi}: expected 4 options, got {len(opts)}")
            ci = q.get('correct_index')
            if not isinstance(ci, int) or not (0 <= ci <= 3):
                errors.append(f"day {dn} quiz {qi}: correct_index invalid: {ci!r}")
            else:
                correct_indices.append(ci)
        if quiz and len(set(correct_indices)) == 1 and len(correct_indices) == len(quiz):
            warnings.append(f"day {dn}: all quiz correct_index values are the same ({correct_indices[0]}) — vary them")

        exercise = d.get('practical_exercise') or {}
        if not exercise.get('title') or not exercise.get('instructions'):
            errors.append(f"day {dn}: practical_exercise missing title/instructions")

        for r in (d.get('resources') or []):
            if not r.get('url', '').startswith('https://'):
                warnings.append(f"day {dn}: resource url doesn't look like a real https link: {r}")

    fp = data.get('final_project') or {}
    for key in ('title', 'description', 'difficulty', 'estimated_hours', 'skills_demonstrated', 'rubric'):
        if key not in fp:
            errors.append(f"final_project missing key: {key}")
    rubric = fp.get('rubric') or []
    total = sum(r.get('max_points', 0) for r in rubric)
    if total != 100:
        errors.append(f"final_project rubric sums to {total}, expected 100")

    if days:
        last_day = sorted(days, key=lambda d: d.get('day_number') or 0)[-1]
        if fp.get('title', '').lower()[:10] not in (last_day.get('content_html') or '').lower() and \
           fp.get('title', '') not in (last_day.get('content_html') or ''):
            warnings.append("day 30 content_html doesn't obviously reference the final_project title — double-check it's connected")

    return errors, warnings


def main():
    base = pathlib.Path(__file__).parent / 'seed_data' / 'career_skills'
    found = sorted(p.stem for p in base.glob('*.py') if p.stem != '__init__')
    print(f"Found {len(found)}/20 curriculum files: {found}\n")

    missing = [s for s in EXPECTED_SLUGS if s not in found]
    if missing:
        print(f"Still missing: {missing}\n")

    total_errors = 0
    for slug in found:
        module = importlib.import_module(f'seed_data.career_skills.{slug}')
        data = getattr(module, 'SKILL', None)
        if data is None:
            print(f"[{slug}] FAIL — no SKILL dict found in module")
            total_errors += 1
            continue
        errors, warnings = validate(slug, data)
        status = 'OK' if not errors else 'FAIL'
        print(f"[{slug}] {status} — {len(errors)} errors, {len(warnings)} warnings")
        for e in errors:
            print(f"    ERROR: {e}")
        for w in warnings:
            print(f"    warn:  {w}")
        total_errors += len(errors)

    print(f"\n{'='*60}\nTotal files: {len(found)}/20, total errors: {total_errors}")


if __name__ == '__main__':
    main()
