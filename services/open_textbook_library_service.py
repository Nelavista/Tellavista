import requests

# Open Textbook Library (open.umn.edu) — a faculty-reviewed catalog of 600+
# real, open-license textbooks. Unlike Tavily (general web search) or OpenAlex
# (individual scholarly articles), this returns actual "Introduction to X"
# textbooks, which is what students searching materials actually want.
#
# It organizes by subject rather than by arbitrary course code, so lookups here
# are keyed by department name (mapped to an OTL subject slug) rather than by
# course code the way search_google_pdfs() works.

BASE_URL = "https://open.umn.edu/opentextbooks/subjects"

# Our department name -> OTL subject slug. Only departments with a real,
# verified-good match are listed; an unmapped department returns no results
# rather than guessing a slug that might 404 or return irrelevant subjects.
DEPARTMENT_TO_SLUG = {
    'Sociology': 'sociology',
    'Psychology': 'psychology',
    'Political Science': 'political-science',
    'Philosophy': 'philosophy',
    'Anthropology': 'anthropology',
    'Law': 'law',
    'Education': 'education',
    'Accounting': 'accounting',
    'Business Administration': 'management',
    'Business': 'management',
    'Marketing': 'marketing',
    'Mathematics': 'mathematics',
    # Verified live: 'computer-science' 404s (not a real OTL slug), the correct
    # slug is 'computer-science-information-systems' -- this bug meant every
    # Computer Science course silently got zero OTL results for as long as it
    # was wrong.
    'Computer Science': 'computer-science-information-systems',
    'Chemistry': 'chemistry',
    'Physics': 'physics',
    'Biology': 'biology',
}

FORMAT_PRIORITY = ['PDF', 'Online', 'eBook', 'XML', 'ODF', 'Print']


def _best_format_url(formats):
    by_type = {f['type']: f['url'] for f in formats if f.get('url')}
    for t in FORMAT_PRIORITY:
        if t in by_type:
            return by_type[t]
    if formats:
        return formats[0].get('url')
    return None


def _verify_url(url):
    try:
        r = requests.head(url, timeout=8, allow_redirects=True)
        if r.status_code in (405, 403):
            r = requests.get(url, timeout=8, stream=True, allow_redirects=True)
        return r.status_code < 400
    except Exception:
        return False


def search_open_textbook_library(department, max_results=5):
    """
    Look up real open textbooks for a department via the Open Textbook Library.

    Returns (results, api_ok) matching search_google_pdfs()'s contract:
      - results: list of dicts with title, url, snippet
      - api_ok: False only on an actual request failure — an unmapped
        department (no slug) legitimately returns ([], True), same as a
        real search with zero matches, not an API failure.

    Every URL is verified with a live HTTP check before being returned —
    this API's "PDF" format links are sometimes dead (third-party host
    removed the file, moved the book, etc.), and nothing gets served to
    students unverified after the phantom-materials incident.
    """
    slug = DEPARTMENT_TO_SLUG.get((department or '').strip())
    if not slug:
        return [], True

    try:
        resp = requests.get(f"{BASE_URL}/{slug}.json", timeout=12)
        resp.raise_for_status()
        books = resp.json().get('data', [])
    except Exception as e:
        print(f"[ERROR] Open Textbook Library request failed: {str(e)}")
        return [], False

    results = []
    for book in books:
        if len(results) >= max_results:
            break
        title = (book.get('title') or '').strip()
        url = _best_format_url(book.get('formats', []))
        if not url or not _verify_url(url):
            continue
        results.append({
            'title': title,
            'url': url,
            'snippet': (book.get('description') or '')[:250],
        })

    return results, True
