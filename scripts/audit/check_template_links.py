"""Cross-check every href/action/fetch() in templates against the real Flask URL map.

Finding: nav items (and dashboard JS) pointing at routes that don't exist is the
class of bug this catches -- a link that looks fine in HTML but 404s for the user.
Static targets are checked against files under app/static instead.

Usage (repo root):
    SKIP_DB_INIT=1 python -m scripts.audit.check_template_links

Exit code 0 = all links resolve; 1 = at least one dead link (printed with template
and line number). Jinja-templated URLs (containing '{{') are skipped -- they can't
be resolved statically -- as are external/anchor/mailto targets.
"""
import os
import re
import sys

if os.environ.get('SKIP_DB_INIT') != '1':  # must precede any app import; see tests/conftest.py
    os.environ['SKIP_DB_INIT'] = '1'

TEMPLATES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), 'app', 'templates')

# href="...", action="...", fetch('...' / fetch("..."  (single call style used across JS)
PATTERNS = [
    re.compile(r'''(?:href|action)=["'](/[^"']*)["']'''),
    re.compile(r'''fetch\(\s*["'](/[^"']*)["']'''),
]

# fetch('/x/' + id) -- the literal is a route *prefix*; matched by rule-prefix below.
CONCAT_PATTERN = re.compile(r'''["'](/[^"']*)["']\s*\+''')


def collect_template_urls():
    hits = []
    for root, _dirs, files in os.walk(TEMPLATES):
        for name in files:
            if not name.endswith('.html'):
                continue
            path = os.path.join(root, name)
            rel = os.path.relpath(path, TEMPLATES)
            with open(path, encoding='utf-8', errors='replace') as fh:
                for lineno, line in enumerate(fh, 1):
                    concat_prefixes = set(m.group(1) for m in CONCAT_PATTERN.finditer(line))
                    for pat in PATTERNS:
                        for m in pat.finditer(line):
                            hits.append((rel, lineno, m.group(1), concat_prefixes))
    return hits


def main():
    from app import app

    rules = [r.rule for r in app.url_map.iter_rules()]

    # Convert Flask rule syntax (<int:x>) to a matcher for the literal path segments.
    def matches(url):
        path = url.split('?')[0].split('#')[0]
        for rule in rules:
            if '<' not in rule:
                if rule == path:
                    return True
                continue
            rx = re.escape(rule)
            rx = re.sub(r'\\<[^>]+\\>', r'[^/]+', rx)  # any converter: <int:id>, <path:x>...
            if re.fullmatch(rx, path):
                return True
        return False

    static_prefix = '/static/'
    dead = []
    skipped = 0
    for rel, lineno, url, concat_prefixes in collect_template_urls():
        if '{{' in url or '{%' in url:
            skipped += 1
            continue
        if url.startswith(static_prefix):
            local = os.path.join(os.path.dirname(TEMPLATES), 'static',
                                 url[len(static_prefix):])
            if not os.path.exists(local):
                dead.append((rel, lineno, url, 'static file missing'))
            continue
        if not matches(url):
            # fetch('/x/' + id) style: the literal both ends at a segment boundary
            # and is concatenated onto in the source, so a rule-prefix match counts.
            if (url in concat_prefixes and url.endswith('/')
                    and any(r.startswith(url) for r in rules)):
                continue
            dead.append((rel, lineno, url, 'no route'))

    total = len(collect_template_urls())
    print(f'{total} internal URL references across templates '
          f'({skipped} Jinja-templated skipped)')
    if not dead:
        print('OK: every resolvable internal link targets a real route or file.')
        return 0
    print(f'{len(dead)} DEAD link(s):')
    for rel, lineno, url, why in dead:
        print(f'  {rel}:{lineno}  {url}  ({why})')
    return 1


if __name__ == '__main__':
    sys.exit(main())
