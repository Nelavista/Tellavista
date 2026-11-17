"""Gig rules: taxonomy, availability, display, matching, feed, student state, events,
admin checks. Routes and templates stay thin; everything they show comes from here."""
import hashlib
import html as html_lib
import json
import logging
import re
from collections import Counter
from datetime import datetime, timedelta, date
from html.parser import HTMLParser
from urllib.parse import urlparse, urlunparse

from app.extensions import db
from app.models import Gig, GigProvider, GigSave, GigApplication, GigEvent, StudentSkill, Skill
from app.utils.validation import safe_external_url

logger = logging.getLogger('nelavista.gigs')

# ---------------------------------------------------------------- taxonomy

CATEGORIES = [
    ('software', 'Software', 'ri-terminal-box-line'),
    ('web_development', 'Web Development', 'ri-code-s-slash-line'),
    ('design', 'Design', 'ri-palette-line'),
    ('data', 'Data', 'ri-bar-chart-box-line'),
    ('content', 'Content', 'ri-quill-pen-line'),
    ('marketing', 'Marketing', 'ri-megaphone-line'),
    ('social_media', 'Social Media', 'ri-instagram-line'),
    ('customer_support', 'Customer Support', 'ri-customer-service-2-line'),
    ('bpo', 'BPO', 'ri-building-4-line'),
    ('virtual_assistant', 'Virtual Assistant', 'ri-calendar-check-line'),
    ('research', 'Research', 'ri-search-eye-line'),
    ('other', 'Other', 'ri-briefcase-4-line'),
]
CATEGORY_KEYS = [c[0] for c in CATEGORIES]
CATEGORY_LABELS = {k: label for k, label, _ in CATEGORIES}
CATEGORY_ICONS = {k: icon for k, _, icon in CATEGORIES}

# Checked in order; the first hit wins. Used by adapters to map a provider's own
# category/title onto Nelavista's categories.
CATEGORY_KEYWORDS = [
    ('virtual_assistant', ['virtual assistant', 'executive assistant', 'personal assistant', 'admin assistant', 'administrative']),
    ('bpo', ['bpo', 'call center', 'call centre', 'outsourc', 'back office', 'data entry']),
    ('customer_support', ['customer support', 'customer service', 'customer success', 'support specialist', 'help desk', 'helpdesk', 'technical support', 'chat support']),
    ('social_media', ['social media', 'community manager', 'tiktok', 'instagram', 'influencer']),
    ('web_development', ['web develop', 'frontend', 'front-end', 'front end', 'wordpress', 'shopify', 'webflow', 'full stack', 'full-stack', 'fullstack', 'react', 'javascript', 'php']),
    ('software', ['software', 'developer', 'engineer', 'devops', 'backend', 'back-end', 'mobile', 'android', 'ios', 'python', 'qa ', 'quality assurance', 'programming', 'dev ']),
    ('data', ['data', 'analyst', 'analytics', 'machine learning', 'statistic', 'excel', 'spreadsheet', 'bi ', 'sql']),
    ('design', ['design', 'ui/ux', 'ux', 'graphic', 'illustrat', 'figma', 'video edit', 'motion', 'animation', 'photoshop', 'creative']),
    ('content', ['writ', 'copy', 'content', 'editor', 'editing', 'translat', 'transcri', 'proofread', 'blog', 'journalis']),
    ('marketing', ['marketing', 'seo', 'growth', 'sales', 'advertis', 'ppc', 'brand', 'email market', 'business develop', 'lead gen']),
    ('research', ['research', 'survey', 'user testing', 'annotat', 'evaluator', 'rater']),
]

PAY_TYPES = [
    ('fixed', 'Fixed price'), ('hourly', 'Per hour'), ('daily', 'Per day'), ('weekly', 'Per week'),
    ('monthly', 'Per month'), ('yearly', 'Per year'), ('per_task', 'Per task'), ('not_stated', 'Not stated'),
]
PAY_TYPE_KEYS = [p[0] for p in PAY_TYPES]
PAY_SUFFIX = {'hourly': '/hr', 'daily': '/day', 'weekly': '/week', 'monthly': '/month', 'yearly': '/year', 'per_task': '/task'}

WORK_TYPES = [
    ('project', 'Project-based'), ('freelance', 'Freelance'), ('contract', 'Contract'),
    ('part_time', 'Part-time'), ('full_time', 'Full-time'), ('internship', 'Paid internship'),
]
WORK_TYPE_KEYS = [w[0] for w in WORK_TYPES]
WORK_TYPE_LABELS = dict(WORK_TYPES)

LOCATION_TYPES = [('remote', 'Remote'), ('hybrid', 'Hybrid'), ('onsite', 'On-site')]
LOCATION_TYPE_KEYS = [lt[0] for lt in LOCATION_TYPES]
LOCATION_TYPE_LABELS = dict(LOCATION_TYPES)

CURRENCY_SYMBOLS = {'NGN': '₦', 'USD': '$', 'EUR': '€', 'GBP': '£', 'GHS': 'GH₵', 'KES': 'KSh ', 'ZAR': 'R', 'CAD': 'CA$', 'AUD': 'A$'}

STATUSES = ['OPEN', 'CLOSING_SOON', 'CLOSED', 'EXPIRED', 'UNKNOWN']
SOURCE_STATUSES = ['OPEN', 'CLOSED', 'UNKNOWN']
ORIGINS = ['external', 'manual', 'partner']
# Future: 'NELAVISTA' lets a signed partner's gig be applied to inside Nelavista. No
# partner workflow exists yet, so every gig uses the official application URL.
APPLICATION_MODES = ['EXTERNAL', 'NELAVISTA']
PARTNER_WORKFLOWS = {}

EVENT_VIEWED = 'gig_viewed'
EVENT_SAVED = 'gig_saved'
EVENT_UNSAVED = 'gig_unsaved'
EVENT_APPLY_CLICKED = 'apply_clicked'
EVENT_APPLICATION_MARKED = 'application_marked'
EVENT_APPLICATION_UNMARKED = 'application_unmarked'
EVENT_SHARED = 'gig_shared'
EVENT_TYPES = {EVENT_VIEWED, EVENT_SAVED, EVENT_UNSAVED, EVENT_APPLY_CLICKED, EVENT_APPLICATION_MARKED,
               EVENT_APPLICATION_UNMARKED, EVENT_SHARED}

CLOSING_SOON_DAYS = 3
NEW_WITHIN_DAYS = 7
# Manual and partner gigs have no feed re-confirming them, so an admin re-verifies them
# on this cadence. Past it they show as "Availability unknown", never as open.
MANUAL_RECHECK_DAYS = 14
DEFAULT_STALE_HOURS = 72
RESERVED_SLUGS = {'nelavista', 'new', 'mine'}

WAT = timedelta(hours=1)  # Nigeria is UTC+1 all year


def today_wat(now=None):
    return ((now or datetime.utcnow()) + WAT).date()


# ---------------------------------------------------------------- text helpers

class _TextExtractor(HTMLParser):
    BLOCK = {'p', 'div', 'br', 'li', 'ul', 'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'tr', 'section', 'blockquote'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self._skip += 1
        elif tag == 'li':
            self.parts.append('\n• ')
        elif tag in self.BLOCK:
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self._skip = max(0, self._skip - 1)
        elif tag in self.BLOCK:
            self.parts.append('\n')

    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)


def html_to_text(value, max_len=20000):
    """Provider descriptions arrive as HTML. Students get plain text (rendered with
    pre-line), so nothing from a provider is ever injected as markup."""
    if not value:
        return None
    value = str(value)
    if '<' in value and '>' in value:
        parser = _TextExtractor()
        try:
            parser.feed(value)
            parser.close()
            value = ''.join(parser.parts)
        except Exception:
            value = re.sub(r'<[^>]+>', ' ', value)
    value = html_lib.unescape(value).replace('\r', '')
    value = re.sub(r'[ \t\xa0]+', ' ', value)
    value = re.sub(r' *\n *', '\n', value)
    value = re.sub(r'\n{3,}', '\n\n', value).strip()
    return value[:max_len] or None


def summarize(text, max_len=220):
    text = re.sub(r'\s+', ' ', (text or '')).replace('•', '').strip()
    if len(text) <= max_len:
        return text or None
    cut = text[:max_len].rsplit(' ', 1)[0]
    return cut.rstrip('.,;:') + '…'


def _norm(text):
    return re.sub(r'[^a-z0-9]+', ' ', (text or '').lower()).strip()


def infer_category(*texts):
    hay = ' ' + ' '.join(t for t in texts if t).lower() + ' '
    for key, words in CATEGORY_KEYWORDS:
        if any(w in hay for w in words):
            return key
    return 'other'


# A vocabulary of skills worth showing on a card. Adapters pick skills only from what a
# listing actually names (title, tags, short excerpt). Nothing is guessed.
KNOWN_SKILLS = [
    'React', 'JavaScript', 'TypeScript', 'Node.js', 'Python', 'Django', 'Flask', 'PHP', 'Laravel', 'WordPress',
    'Shopify', 'Webflow', 'HTML', 'CSS', 'Tailwind', 'Vue', 'Angular', 'Next.js', 'Java', 'Kotlin', 'Swift',
    'Flutter', 'React Native', 'Go', 'Ruby', 'C#', '.NET', 'SQL', 'PostgreSQL', 'MongoDB', 'AWS', 'Docker',
    'Git', 'Excel', 'Google Sheets', 'Power BI', 'Tableau', 'Data Entry', 'Data Analysis', 'Machine Learning',
    'Figma', 'Photoshop', 'Illustrator', 'Canva', 'UI/UX', 'Graphic Design', 'Video Editing', 'Premiere Pro',
    'After Effects', 'CapCut', 'Copywriting', 'Content Writing', 'Blogging', 'Proofreading', 'Translation',
    'Transcription', 'SEO', 'Social Media', 'Email Marketing', 'Google Ads', 'Facebook Ads', 'Sales',
    'Customer Service', 'Zendesk', 'HubSpot', 'Salesforce', 'Virtual Assistance', 'Research', 'QA Testing',
]
SKILL_ALIASES = {
    'js': 'javascript', 'reactjs': 'react', 'react js': 'react', 'react.js': 'react', 'nodejs': 'node.js',
    'node': 'node.js', 'ts': 'typescript', 'ux': 'ui/ux', 'ui': 'ui/ux', 'ui ux': 'ui/ux', 'ui/ux design': 'ui/ux',
    'ux design': 'ui/ux', 'ui design': 'ui/ux', 'microsoft excel': 'excel', 'ms excel': 'excel', 'postgres': 'postgresql',
    'golang': 'go', 'nextjs': 'next.js', 'vuejs': 'vue', 'vue.js': 'vue', 'customer support': 'customer service',
    'virtual assistant': 'virtual assistance', 'data analytics': 'data analysis', 'writing': 'content writing',
}


def canonical_skill(name):
    """'React Development' -> 'react', 'UI/UX Design' -> 'ui/ux', 'JS' -> 'javascript'."""
    low = re.sub(r'\s+', ' ', (name or '').strip().lower())
    if low in SKILL_ALIASES:
        return SKILL_ALIASES[low]
    for suffix in (' development', ' developer', ' programming', ' fundamentals', ' basics', ' for beginners'):
        if low.endswith(suffix) and len(low) > len(suffix):
            low = low[: -len(suffix)].strip()
            break
    return SKILL_ALIASES.get(low, low)


def extract_skills(*texts, limit=8):
    hay = ' ' + ' '.join(t for t in texts if t) + ' '
    found = []
    for skill in KNOWN_SKILLS:
        pattern = r'(?<![A-Za-z0-9])' + re.escape(skill) + r'(?![A-Za-z0-9])'
        if re.search(pattern, hay, flags=re.IGNORECASE) and skill not in found:
            found.append(skill)
        if len(found) >= limit:
            break
    return found


def canonical_url(url):
    """Comparable form of an application URL for duplicate detection: lower-case host,
    no www, no fragment, no tracking parameters, no trailing slash."""
    if not url:
        return None
    try:
        p = urlparse(url.strip())
    except ValueError:
        return None
    if not p.hostname:
        return None
    host = p.hostname.lower()
    if host.startswith('www.'):
        host = host[4:]
    query = '&'.join(q for q in (p.query or '').split('&')
                     if q and not q.lower().startswith(('utm_', 'ref=', 'source=', 'u=', 'fbclid', 'gclid')))
    return urlunparse(('https', host, (p.path or '').rstrip('/'), '', query, ''))


def dedupe_key_for(title, organization):
    base = f'{_norm(title)}|{_norm(organization)}'
    return hashlib.sha1(base.encode('utf-8')).hexdigest()


def slugify(text):
    slug = re.sub(r'[^a-z0-9]+', '-', (text or '').lower()).strip('-')
    return slug[:150] or 'gig'


def unique_slug(base, exclude_id=None):
    if base in RESERVED_SLUGS:
        base = f'{base}-gig'
    slug, n = base, 2
    while True:
        q = Gig.query.filter_by(slug=slug)
        if exclude_id:
            q = q.filter(Gig.id != exclude_id)
        if not q.first():
            return slug
        slug = f'{base}-{n}'
        n += 1


# ---------------------------------------------------------------- availability

def stale_window(gig):
    if gig.origin == 'external':
        hours = (gig.provider.stale_after_hours if gig.provider and gig.provider.stale_after_hours else DEFAULT_STALE_HOURS)
        return timedelta(hours=hours)
    return timedelta(days=MANUAL_RECHECK_DAYS)


def is_fresh(gig, now=None):
    now = now or datetime.utcnow()
    return bool(gig.last_verified_at and now - gig.last_verified_at <= stale_window(gig))


def compute_status(gig, now=None):
    """{key, label, tone, emoji, days_left}. Order matters:
    archived/admin-closed/source-closed -> CLOSED; deadline passed -> EXPIRED; nobody has
    confirmed it is open within the freshness window -> UNKNOWN; deadline within
    CLOSING_SOON_DAYS -> CLOSING_SOON; else OPEN. An old import therefore can't stay
    "open" forever: once its source stops confirming it, it drops to UNKNOWN."""
    now = now or datetime.utcnow()
    today = today_wat(now)
    override = gig.status_override
    if gig.is_archived or override == 'CLOSED':
        return _status('CLOSED')
    if gig.deadline and gig.deadline < today:
        return _status('EXPIRED')
    if gig.source_status == 'CLOSED' and override != 'OPEN':
        return _status('CLOSED')
    if override == 'UNKNOWN':
        return _status('UNKNOWN')
    if override != 'OPEN' and gig.source_status != 'OPEN':
        return _status('UNKNOWN')
    if not is_fresh(gig, now):
        return _status('UNKNOWN')
    if gig.deadline:
        days = (gig.deadline - today).days
        if days <= CLOSING_SOON_DAYS:
            label = 'Closes today' if days == 0 else ('Closes tomorrow' if days == 1 else f'Closes in {days} days')
            return _status('CLOSING_SOON', label=label, days_left=days)
        return _status('OPEN', days_left=days)
    return _status('OPEN')


_STATUS_UI = {
    'OPEN': ('Open', 'open', '🟢'),
    'CLOSING_SOON': ('Closing soon', 'soon', '🟠'),
    'CLOSED': ('Closed', 'closed', '🔴'),
    'EXPIRED': ('Expired', 'closed', '🔴'),
    'UNKNOWN': ('Availability unknown', 'unknown', '⚪'),
}


def _status(key, label=None, days_left=None):
    default_label, tone, emoji = _STATUS_UI[key]
    return {'key': key, 'label': label or default_label, 'tone': tone, 'emoji': emoji, 'days_left': days_left,
            'accepting': key in ('OPEN', 'CLOSING_SOON')}


def is_active(gig, now=None):
    return compute_status(gig, now)['accepting']


def time_ago(dt, now=None):
    if not dt:
        return None
    now = now or datetime.utcnow()
    secs = max(0, int((now - dt).total_seconds()))
    if secs < 90:
        return 'just now'
    mins = secs // 60
    if mins < 60:
        return f'{mins} minutes ago'
    hours = mins // 60
    if hours < 24:
        return '1 hour ago' if hours == 1 else f'{hours} hours ago'
    days = hours // 24
    if days < 30:
        return 'yesterday' if days == 1 else f'{days} days ago'
    months = days // 30
    return '1 month ago' if months == 1 else f'{months} months ago'


# ---------------------------------------------------------------- display

def _money(amount, currency, compact):
    symbol = CURRENCY_SYMBOLS.get((currency or '').upper())
    if compact and amount >= 1000:
        if amount >= 1_000_000:
            num = f'{amount / 1_000_000:.1f}'.rstrip('0').rstrip('.') + 'M'
        else:
            num = f'{amount / 1000:.1f}'.rstrip('0').rstrip('.') + 'k'
    else:
        num = f'{amount:,}'
    return f'{symbol}{num}' if symbol else f'{(currency or "").upper()} {num}'.strip()


def format_pay(gig, compact=False):
    """'₦100,000–₦150,000', '$25/hr', or the provider's own wording. Never invents a
    number: no structured pay and no wording -> 'Pay not stated'."""
    lo, hi = gig.pay_min, gig.pay_max
    suffix = PAY_SUFFIX.get(gig.pay_type, '')
    if lo or hi:
        if lo and hi and lo != hi:
            text = f'{_money(lo, gig.currency, compact)}–{_money(hi, gig.currency, compact)}'
        elif lo and hi:
            text = _money(lo, gig.currency, compact)
        elif lo and gig.pay_type in ('fixed', 'per_task'):
            text = _money(lo, gig.currency, compact)  # one fixed amount, e.g. "₦50k"
        elif lo:
            text = f'From {_money(lo, gig.currency, compact)}'
        else:
            text = f'Up to {_money(hi, gig.currency, compact)}'
        return text + suffix
    if gig.pay_text:
        return gig.pay_text
    return 'Pay not stated'


def has_pay(gig):
    return bool(gig.pay_min or gig.pay_max or gig.pay_text)


def location_label(gig):
    kind = LOCATION_TYPE_LABELS.get(gig.location_type, 'Remote')
    if gig.location and gig.location.strip().lower() not in (kind.lower(), 'remote', 'anywhere'):
        return f'{kind} · {gig.location}'
    return kind


_NIGERIA_OK = ('worldwide', 'anywhere', 'global', 'international', 'africa', 'emea', 'nigeria', 'lagos', 'abuja',
               'west africa', 'remote', 'all countries', 'any location', 'europe, middle east')
_NIGERIA_HOSTILE = ('usa', 'united states', 'us only', 'us-only', 'canada', 'uk only', 'united kingdom', 'europe only',
                    'eu only', 'germany', 'australia', 'india', 'latam', 'latin america', 'philippines', 'apac', 'north america')


def open_to_nigeria(gig_or_location, location_type='remote'):
    """True/False/None (can't tell). Remote work is useless to a Nigerian student if the
    employer only hires in the US, so the feed can filter on this."""
    if isinstance(gig_or_location, Gig):
        location, location_type = gig_or_location.location, gig_or_location.location_type
    else:
        location = gig_or_location
    text = (location or '').lower()
    if not text:
        return True if location_type == 'remote' else None
    if any(w in text for w in ('nigeria', 'lagos', 'abuja', 'africa', 'worldwide', 'anywhere', 'global', 'emea')):
        return True
    if any(w in text for w in _NIGERIA_HOSTILE):
        return False
    if any(w in text for w in _NIGERIA_OK):
        return True
    return None


def source_name(gig):
    p = gig.provider
    if gig.origin in ('manual', 'partner') or not p:
        return 'Nelavista'
    return p.attribution_text or p.name


def application_handler(gig):
    """Who actually receives the application. External gigs: the provider's listing (it
    links on to the employer). Manual gigs: the organisation's own application."""
    if gig.origin == 'external':
        return source_name(gig)
    return gig.organization


def effective_application_mode(gig):
    if gig.application_mode == 'NELAVISTA' and gig.origin == 'partner' and gig.slug in PARTNER_WORKFLOWS:
        return 'NELAVISTA'
    return 'EXTERNAL'


def ui_helpers():
    return {
        'status': compute_status, 'pay': format_pay, 'location': location_label, 'ago': time_ago,
        'source': source_name, 'handler': application_handler, 'category_labels': CATEGORY_LABELS,
        'category_icons': CATEGORY_ICONS, 'work_types': WORK_TYPE_LABELS, 'nigeria': open_to_nigeria,
        'fresh': is_fresh,
    }


# ---------------------------------------------------------------- visibility

def visible_query():
    """What students may ever see: published, not archived, not a duplicate, from a
    provider that is still enabled (disabling a provider hides all its gigs at once)."""
    return (Gig.query.join(GigProvider, Gig.provider_id == GigProvider.id)
            .filter(Gig.is_published.is_(True), Gig.is_archived.is_(False), Gig.duplicate_of_id.is_(None),
                    GigProvider.enabled.is_(True)))


def can_view(gig, user):
    if user is not None and getattr(user, 'is_admin', False):
        return True
    return bool(gig.is_published and not gig.is_archived and gig.duplicate_of_id is None
                and gig.provider and gig.provider.enabled)


# ---------------------------------------------------------------- skill match

def user_skill_names(user):
    """Skills Nelavista actually knows the student is working on: their started or
    completed Skills (progress recorded). Nothing self-declared, nothing inferred."""
    if not user:
        return []
    rows = (db.session.query(Skill.name).join(StudentSkill, StudentSkill.skill_id == Skill.id)
            .filter(StudentSkill.student_id == user.id,
                    db.or_(StudentSkill.progress_pct > 0, StudentSkill.status == 'completed')).all())
    return sorted({r[0] for r in rows if r[0]})


def _skill_hits(gig_skill, user_skills_canon):
    g = canonical_skill(gig_skill)
    if not g:
        return False
    for u in user_skills_canon:
        if g == u:
            return True
        if len(g) >= 3 and re.search(r'(?<![a-z0-9])' + re.escape(g) + r'(?![a-z0-9])', u):
            return True
        if len(u) >= 3 and re.search(r'(?<![a-z0-9])' + re.escape(u) + r'(?![a-z0-9])', g):
            return True
    return False


def skill_match(gig, user_skills):
    """{'pct', 'matched'} or None when there isn't enough data (the student has no
    tracked skills, or the gig lists none). A 0% result is returned as None too: the
    card shows nothing rather than a discouraging, possibly wrong number."""
    if not user_skills or not gig.skills:
        return None
    canon = [canonical_skill(s) for s in user_skills]
    matched = [s for s in gig.skills if _skill_hits(s, canon)]
    if not matched:
        return None
    return {'pct': round(100 * len(matched) / len(gig.skills)), 'matched': matched}


# ---------------------------------------------------------------- search & feed

DEADLINE_FILTERS = [('week', 'Closes within 7 days'), ('month', 'Closes within 30 days'), ('none', 'No deadline given')]
POSTED_FILTERS = [('1', 'Last 24 hours'), ('7', 'Last 7 days'), ('30', 'Last 30 days')]
SORTS = [('best', 'Best for me'), ('newest', 'Newest'), ('pay', 'Highest pay'), ('deadline', 'Deadline (soonest)')]


def _haystack(gig):
    parts = [gig.title, gig.organization, gig.summary, gig.description, gig.location, gig.pay_text,
             CATEGORY_LABELS.get(gig.category, ''), WORK_TYPE_LABELS.get(gig.work_type or '', ''),
             LOCATION_TYPE_LABELS.get(gig.location_type, '')] + gig.skills
    return ' '.join(p for p in parts if p).lower()


def matches_search(gig, q):
    terms = [t for t in re.split(r'\s+', (q or '').lower().strip()) if t]
    if not terms:
        return True
    hay = _haystack(gig)
    return all(t in hay or (t.endswith('s') and t[:-1] in hay) for t in terms)


def parse_filters(args):
    args = args or {}

    def pick(name, allowed):
        v = args.get(name)
        return v if v in allowed else None

    min_pay = args.get('min_pay')
    try:
        min_pay = max(0, int(str(min_pay).replace(',', ''))) if min_pay not in (None, '') else None
    except ValueError:
        min_pay = None
    return {
        'q': (args.get('q') or '').strip()[:100],
        'category': pick('category', CATEGORY_KEYS),
        'location_type': pick('location_type', LOCATION_TYPE_KEYS),
        'nigeria': '1' if args.get('nigeria') in ('1', 'on', 'true') else None,
        'skill': (args.get('skill') or '').strip()[:40],
        'min_pay': min_pay or None,
        'pay_stated': '1' if args.get('pay_stated') in ('1', 'on', 'true') else None,
        'deadline': pick('deadline', dict(DEADLINE_FILTERS)),
        'posted': pick('posted', dict(POSTED_FILTERS)),
    }


def apply_filters(gigs, filters, now=None):
    now = now or datetime.utcnow()
    today = today_wat(now)
    out = []
    skill_canon = canonical_skill(filters.get('skill')) if filters.get('skill') else None
    for g in gigs:
        if filters.get('category') and g.category != filters['category']:
            continue
        if filters.get('location_type') and g.location_type != filters['location_type']:
            continue
        if filters.get('nigeria') and open_to_nigeria(g) is False:
            continue
        if skill_canon and not (_skill_hits(filters['skill'], [canonical_skill(s) for s in g.skills])
                                or skill_canon in _haystack(g)):
            continue
        if filters.get('pay_stated') and not has_pay(g):
            continue
        if filters.get('min_pay'):
            # Only naira amounts are compared. There is no exchange-rate guess.
            if (g.currency or '').upper() != 'NGN' or (g.pay_max or g.pay_min or 0) < filters['min_pay']:
                continue
        if filters.get('deadline'):
            days = (g.deadline - today).days if g.deadline else None
            if filters['deadline'] == 'none' and g.deadline:
                continue
            if filters['deadline'] == 'week' and (days is None or days > 7):
                continue
            if filters['deadline'] == 'month' and (days is None or days > 30):
                continue
        if filters.get('posted'):
            posted = g.posted_at or g.created_at
            if not posted or now - posted > timedelta(days=int(filters['posted'])):
                continue
        if filters.get('q') and not matches_search(g, filters['q']):
            continue
        out.append(g)
    return out


def _posted_key(g):
    return g.posted_at or g.created_at or datetime.min


def _pay_key(g):
    return ((g.currency or '').upper() == 'NGN', g.pay_max or g.pay_min or 0)


def sort_gigs(gigs, sort, matches):
    if sort == 'newest':
        return sorted(gigs, key=_posted_key, reverse=True)
    if sort == 'pay':
        return sorted(gigs, key=_pay_key, reverse=True)
    if sort == 'deadline':
        return sorted(gigs, key=lambda g: (g.deadline or date.max, -_posted_key(g).timestamp() if _posted_key(g) != datetime.min else 0))
    # best: featured, then skill match, then newest
    return sorted(gigs, key=lambda g: (not g.featured, -((matches.get(g.id) or {}).get('pct', 0)),
                                       -(_posted_key(g).timestamp() if _posted_key(g) != datetime.min else 0)))


def build_feed(user, args=None, now=None):
    now = now or datetime.utcnow()
    filters = parse_filters(args)
    sort = (args or {}).get('sort') if (args or {}).get('sort') in dict(SORTS) else 'best'
    visible = visible_query().all()
    statuses = {g.id: compute_status(g, now) for g in visible}
    active = [g for g in visible if statuses[g.id]['accepting']]
    unknown = [g for g in visible if statuses[g.id]['key'] == 'UNKNOWN']
    user_skills = user_skill_names(user)
    matches = {g.id: skill_match(g, user_skills) for g in active + unknown}
    filtering = any(v for v in filters.values())

    results = sort_gigs(apply_filters(active, filters, now), sort, matches)
    unknown_results = sort_gigs(apply_filters(unknown, filters, now), 'newest', matches)
    new_cutoff = now - timedelta(days=NEW_WITHIN_DAYS)
    open_gigs = sort_gigs(active, 'best', matches)
    new = [g for g in sort_gigs(active, 'newest', matches) if _posted_key(g) >= new_cutoff]
    closing = sorted([g for g in active if statuses[g.id]['key'] == 'CLOSING_SOON'], key=lambda g: g.deadline or date.max)
    recommended = sorted([g for g in active if matches.get(g.id)], key=lambda g: -matches[g.id]['pct'])
    return {
        'filters': filters, 'filtering': filtering, 'sort': sort, 'results': results,
        'unknown': unknown_results[:30], 'total_open': len(active), 'statuses': statuses, 'matches': matches,
        'open_gigs': open_gigs[:8], 'new': new[:8], 'closing_soon': closing[:8], 'recommended': recommended[:8],
        'user_skills': user_skills, 'has_skill_data': bool(user_skills),
    }


def related_gigs(gig, limit=3, now=None):
    pool = [g for g in visible_query().filter(Gig.id != gig.id, Gig.category == gig.category).all() if is_active(g, now)]
    return sorted(pool, key=_posted_key, reverse=True)[:limit]


# ---------------------------------------------------------------- per-student state & events

def user_state(user, gig_ids=None):
    if not user:
        return {}
    saves = GigSave.query.filter_by(user_id=user.id)
    apps = GigApplication.query.filter_by(user_id=user.id)
    if gig_ids is not None:
        ids = list(gig_ids)
        if not ids:
            return {}
        saves = saves.filter(GigSave.gig_id.in_(ids))
        apps = apps.filter(GigApplication.gig_id.in_(ids))
    state = {}
    for s in saves.all():
        state.setdefault(s.gig_id, {'saved': False, 'applied_at': None})['saved'] = True
    for a in apps.all():
        state.setdefault(a.gig_id, {'saved': False, 'applied_at': None})['applied_at'] = a.applied_at
    return state


def log_event(gig, user, event_type, channel=None):
    """Stages a GigEvent (caller commits) and mirrors it to PostHog when configured."""
    if event_type not in EVENT_TYPES:
        raise ValueError(f'Unknown gig event: {event_type}')
    db.session.add(GigEvent(gig_id=gig.id, user_id=user.id if user else None, event_type=event_type,
                            channel=(channel or '')[:30] or None))
    try:
        from app.services.analytics import capture_event_for_user
        capture_event_for_user(getattr(user, 'username', None), event_type, {
            'gig_id': gig.id, 'category': gig.category, 'origin': gig.origin,
            'provider': gig.provider.slug if gig.provider else None, 'channel': channel,
        })
    except Exception:
        logger.exception('gig analytics capture failed (ignored)')


def set_saved(gig, user, saved):
    existing = GigSave.query.filter_by(user_id=user.id, gig_id=gig.id).first()
    if saved and not existing:
        db.session.add(GigSave(user_id=user.id, gig_id=gig.id))
        log_event(gig, user, EVENT_SAVED)
    elif not saved and existing:
        db.session.delete(existing)
        log_event(gig, user, EVENT_UNSAVED)
    return saved


def set_applied(gig, user, applied):
    existing = GigApplication.query.filter_by(user_id=user.id, gig_id=gig.id).first()
    if applied and not existing:
        existing = GigApplication(user_id=user.id, gig_id=gig.id, source='self_reported')
        db.session.add(existing)
        log_event(gig, user, EVENT_APPLICATION_MARKED)
    elif not applied and existing:
        db.session.delete(existing)
        log_event(gig, user, EVENT_APPLICATION_UNMARKED)
        existing = None
    return existing


def my_gigs(user):
    """Saved and applied gigs for My Opportunities. Closed ones stay (it's the student's
    own history) but a gig an admin unpublished or removed does not."""
    saves = GigSave.query.filter_by(user_id=user.id).order_by(GigSave.created_at.desc()).all()
    apps = GigApplication.query.filter_by(user_id=user.id).order_by(GigApplication.applied_at.desc()).all()
    return {
        'saved': [s.gig for s in saves if can_view(s.gig, None)],
        'applied': [a for a in apps if can_view(a.gig, None)],
    }


# ---------------------------------------------------------------- admin

def _clean(value, max_len=None):
    value = (value or '').strip()
    if max_len:
        value = value[:max_len]
    return value or None


def _parse_int(value, field, errors):
    value = (value or '').strip().replace(',', '')
    if not value:
        return None
    try:
        n = int(float(value))
    except ValueError:
        errors.append(f'{field} must be a number.')
        return None
    if n < 0:
        errors.append(f'{field} can\'t be negative.')
        return None
    return n


# Fields an admin edit "locks" on an external gig so the next sync doesn't undo it.
LOCKABLE_FIELDS = ['title', 'organization', 'summary', 'description', 'requirements', 'eligibility', 'category',
                   'skills_json', 'pay_min', 'pay_max', 'currency', 'pay_type', 'pay_text', 'work_type',
                   'location_type', 'location', 'deadline', 'application_url']


def apply_form(gig, form):
    """Copies the admin form onto `gig`; returns error strings (empty = valid). On an
    external gig, every field whose value changes is added to locked_fields."""
    errors = []
    before = {f: getattr(gig, f) for f in LOCKABLE_FIELDS}
    gig.title = _clean(form.get('title'), 200) or ''
    gig.organization = _clean(form.get('organization'), 150) or ''
    if not gig.title:
        errors.append('Title is required.')
    if not gig.organization:
        errors.append('Organisation is required.')
    gig.summary = _clean(form.get('summary'), 300)
    for field in ('description', 'requirements', 'eligibility'):
        setattr(gig, field, _clean(form.get(field), 20000))
    category = form.get('category') or 'other'
    gig.category = category if category in CATEGORY_KEYS else 'other'
    skills = [s.strip()[:40] for s in re.split(r'[,\n]', form.get('skills') or '') if s.strip()]
    gig.skills_json = json.dumps(list(dict.fromkeys(skills))[:15])

    gig.pay_min = _parse_int(form.get('pay_min'), 'Minimum pay', errors)
    gig.pay_max = _parse_int(form.get('pay_max'), 'Maximum pay', errors)
    if gig.pay_min and gig.pay_max and gig.pay_min > gig.pay_max:
        errors.append('Minimum pay is more than maximum pay.')
    currency = (form.get('currency') or 'NGN').strip().upper()[:10]
    gig.currency = currency if re.fullmatch(r'[A-Z]{3}', currency) else 'NGN'
    pay_type = form.get('pay_type') or 'not_stated'
    gig.pay_type = pay_type if pay_type in PAY_TYPE_KEYS else 'not_stated'
    gig.pay_text = _clean(form.get('pay_text'), 120)
    work_type = form.get('work_type') or None
    gig.work_type = work_type if work_type in WORK_TYPE_KEYS else None
    lt = form.get('location_type') or 'remote'
    gig.location_type = lt if lt in LOCATION_TYPE_KEYS else 'remote'
    gig.location = _clean(form.get('location'), 200)

    raw_deadline = (form.get('deadline') or '').strip()
    gig.deadline = None
    if raw_deadline:
        try:
            gig.deadline = datetime.strptime(raw_deadline, '%Y-%m-%d').date()
        except ValueError:
            errors.append('Deadline must be a date (YYYY-MM-DD).')

    for field in ('application_url', 'source_url', 'organization_logo_url'):
        raw = (form.get(field) or '').strip()
        clean = safe_external_url(raw)
        if raw and not clean:
            errors.append(f'{field.replace("_", " ").capitalize()} must be a full http(s) link.')
        setattr(gig, field, clean)
    gig.external_reference = _clean(form.get('external_reference'), 200)
    gig.featured = bool(form.get('featured'))
    gig.allows_in_app_view = bool(form.get('allows_in_app_view'))

    if gig.origin == 'external' and gig.id:
        locked = gig.locked_fields | {f for f in LOCKABLE_FIELDS if getattr(gig, f) != before[f]}
        gig.locked_fields_json = json.dumps(sorted(locked))
    if form.get('unlock_fields') and gig.origin == 'external':
        gig.locked_fields_json = json.dumps([])
    if not gig.slug:
        gig.slug = unique_slug(slugify(f'{gig.title} {gig.organization}'), exclude_id=gig.id)
    if gig.is_published and publish_problems(gig):
        gig.is_published = False
    return errors


def publish_problems(gig, now=None):
    problems = []
    if not gig.title or not gig.organization:
        problems.append('Add the title and organisation.')
    if not gig.application_url and effective_application_mode(gig) != 'NELAVISTA':
        problems.append('Add the official application URL.')
    if gig.origin == 'external' and not gig.source_url:
        problems.append('External gigs need their source listing URL (for attribution).')
    if gig.origin != 'external' and not (gig.source_url or gig.external_reference):
        problems.append('Record where this gig came from (source URL, or the contact/agreement reference).')
    if not gig.provider or not gig.provider.enabled:
        problems.append('Its provider is disabled.')
    if gig.duplicate_of_id:
        problems.append('It is marked as a duplicate of another gig.')
    if gig.is_archived:
        problems.append('It is archived.')
    if compute_status(gig, now)['key'] in ('CLOSED', 'EXPIRED'):
        problems.append('It is closed or past its deadline.')
    return problems


def admin_action(gig, action, admin, value=None, now=None):
    """Applies one admin action; returns (ok, message). The caller commits."""
    now = now or datetime.utcnow()
    if action == 'publish':
        problems = publish_problems(gig, now)
        if problems:
            return False, 'Not published: ' + ' '.join(problems)
        gig.is_published = True
        gig.published_at = gig.published_at or now
        msg = 'Published.'
        if not compute_status(gig, now)['accepting']:
            msg += ' It shows as "Availability unknown" until it is verified open.'
        return True, msg
    if action == 'unpublish':
        gig.is_published = False
        return True, 'Unpublished.'
    if action == 'verify':
        # An admin checked the official listing and it is accepting applications.
        if not gig.application_url:
            return False, 'Add the application URL before verifying.'
        gig.source_status = 'OPEN'
        if gig.status_override in ('CLOSED', 'UNKNOWN'):
            gig.status_override = None
        gig.last_verified_at = now
        gig.verified_by_id = admin.id if admin else None
        gig.closed_at = None
        return True, 'Verified open just now.'
    if action == 'override':
        if value in ('OPEN', 'CLOSED', 'UNKNOWN'):
            gig.status_override = value
            if value == 'OPEN':
                gig.last_verified_at = now
                gig.verified_by_id = admin.id if admin else None
            if value == 'CLOSED':
                gig.closed_at = gig.closed_at or now
            return True, f'Status set to {value.title()} by an admin.'
        if value in ('', 'clear', None):
            gig.status_override = None
            return True, 'Status override cleared. The source decides again.'
        return False, 'Unknown status.'
    if action == 'feature':
        gig.featured = True
        return True, 'Featured.'
    if action == 'unfeature':
        gig.featured = False
        return True, 'No longer featured.'
    if action == 'archive':
        gig.is_archived = True
        gig.is_published = False
        gig.removed_reason = _clean(value, 200) or gig.removed_reason
        return True, 'Archived.'
    if action == 'unarchive':
        gig.is_archived = False
        return True, 'Restored (unpublished).'
    if action == 'not_duplicate':
        gig.duplicate_of_id = None
        locked = gig.locked_fields | {'duplicate_of_id'}
        gig.locked_fields_json = json.dumps(sorted(locked))
        return True, 'No longer treated as a duplicate.'
    return False, 'Unknown action.'


def gig_stats(gig_ids=None):
    """{gig_id: Counter(event_type -> n, unique_viewers, saved_now, applied_now)}."""
    q = db.session.query(GigEvent.gig_id, GigEvent.event_type, db.func.count(GigEvent.id))
    if gig_ids is not None:
        q = q.filter(GigEvent.gig_id.in_(list(gig_ids) or [-1]))
    out = {}
    for gid, etype, n in q.group_by(GigEvent.gig_id, GigEvent.event_type).all():
        out.setdefault(gid, Counter())[etype] = n
    viewers = (db.session.query(GigEvent.gig_id, db.func.count(db.distinct(GigEvent.user_id)))
               .filter(GigEvent.event_type == EVENT_VIEWED))
    if gig_ids is not None:
        viewers = viewers.filter(GigEvent.gig_id.in_(list(gig_ids) or [-1]))
    for gid, n in viewers.group_by(GigEvent.gig_id).all():
        out.setdefault(gid, Counter())['unique_viewers'] = n
    for model, key in ((GigSave, 'saved_now'), (GigApplication, 'applied_now')):
        rows = db.session.query(model.gig_id, db.func.count(model.id))
        if gig_ids is not None:
            rows = rows.filter(model.gig_id.in_(list(gig_ids) or [-1]))
        for gid, n in rows.group_by(model.gig_id).all():
            out.setdefault(gid, Counter())[key] = n
    return out


def dashboard_metrics(days=30, now=None):
    """The numbers for the admin dashboard and for pitching direct gig partners."""
    now = now or datetime.utcnow()
    since = now - timedelta(days=days)
    week = now - timedelta(days=7)
    visible = visible_query().all()
    active = [g for g in visible if is_active(g, now)]

    def distinct_users(event_type):
        return (db.session.query(db.func.count(db.distinct(GigEvent.user_id)))
                .filter(GigEvent.event_type == event_type, GigEvent.created_at >= since).scalar() or 0)

    totals = dict(db.session.query(GigEvent.event_type, db.func.count(GigEvent.id))
                  .filter(GigEvent.created_at >= since).group_by(GigEvent.event_type).all())
    # Demand = what students clicked Apply on (weighted 3) or viewed (1).
    weighted = Counter()
    cat_counts = Counter()
    rows = (db.session.query(GigEvent.gig_id, GigEvent.event_type, db.func.count(GigEvent.id))
            .filter(GigEvent.created_at >= since, GigEvent.event_type.in_([EVENT_VIEWED, EVENT_APPLY_CLICKED]))
            .group_by(GigEvent.gig_id, GigEvent.event_type).all())
    gigs_by_id = {g.id: g for g in Gig.query.filter(Gig.id.in_([r[0] for r in rows] or [-1])).all()}
    for gid, etype, n in rows:
        g = gigs_by_id.get(gid)
        if not g:
            continue
        w = n * (3 if etype == EVENT_APPLY_CLICKED else 1)
        cat_counts[g.category] += w
        for s in g.skills:
            weighted[s] += w
    return {
        'days': days,
        'total_active': len(active),
        'total_visible': len(visible),
        'new_this_week': sum(1 for g in active if (g.created_at or datetime.min) >= week),
        'views': totals.get(EVENT_VIEWED, 0),
        'apply_clicks': totals.get(EVENT_APPLY_CLICKED, 0),
        'saves': totals.get(EVENT_SAVED, 0),
        'marked_applied': totals.get(EVENT_APPLICATION_MARKED, 0),
        'shares': totals.get(EVENT_SHARED, 0),
        'students_viewing': distinct_users(EVENT_VIEWED),
        'students_clicking_apply': distinct_users(EVENT_APPLY_CLICKED),
        'students_applying': distinct_users(EVENT_APPLICATION_MARKED),
        'top_skills': weighted.most_common(10),
        'top_categories': [(CATEGORY_LABELS.get(k, k), n) for k, n in cat_counts.most_common(6)],
    }
