"""Student opportunities: taxonomy, deadline status, search/filter, personalisation,
admin validation and analytics. Routes stay thin; every rule lives here so the student
feed, the detail page, My Opportunities and the admin dashboard can't disagree.

The listings are third-party programmes. Nelavista isn't a partner of these
organisations unless StudentOpportunity.is_partner says so (set by an admin for a real,
signed partnership). Nothing in this module claims an application was submitted or
accepted. "I applied" is the student's own record.
"""
import json
import re
from collections import Counter
from datetime import datetime, timedelta, date

from app.extensions import db
from app.models import (
    StudentOpportunity, StudentOpportunitySave, StudentOpportunityApplication,
    StudentOpportunityEvent, StudentOpportunityReport,
)
from app.utils.validation import safe_external_url

# ---------------------------------------------------------------- taxonomy

CATEGORIES = [
    ('scholarship', 'Scholarships', 'ri-graduation-cap-line'),
    ('fellowship', 'Fellowships', 'ri-team-line'),
    ('competition', 'Competitions', 'ri-trophy-line'),
    ('hackathon', 'Hackathons', 'ri-code-box-line'),
    ('internship', 'Internships', 'ri-briefcase-4-line'),
    ('campus_ambassador', 'Campus Ambassador', 'ri-megaphone-line'),
    ('bootcamp', 'Bootcamps', 'ri-rocket-line'),
    ('training', 'Training', 'ri-book-open-line'),
    ('leadership', 'Leadership', 'ri-flag-line'),
    ('entrepreneurship', 'Entrepreneurship', 'ri-lightbulb-flash-line'),
    ('volunteering', 'Volunteering', 'ri-heart-line'),
    ('exchange', 'Exchange', 'ri-earth-line'),
    ('grant', 'Grants & Prizes', 'ri-money-dollar-circle-line'),
    ('challenge', 'Challenges', 'ri-flashlight-line'),
    ('other', 'Other', 'ri-star-line'),
]
CATEGORY_KEYS = [c[0] for c in CATEGORIES]
CATEGORY_LABELS = {k: label for k, label, _ in CATEGORIES}
CATEGORY_ICONS = {k: icon for k, _, icon in CATEGORIES}
# Singular labels for the card's "Type:" line.
CATEGORY_SINGULAR = {
    'scholarship': 'Scholarship', 'fellowship': 'Fellowship', 'competition': 'Competition',
    'hackathon': 'Hackathon', 'internship': 'Internship', 'campus_ambassador': 'Campus Ambassador',
    'bootcamp': 'Bootcamp', 'training': 'Training programme', 'leadership': 'Leadership programme',
    'entrepreneurship': 'Entrepreneurship programme', 'volunteering': 'Volunteering',
    'exchange': 'Exchange programme', 'grant': 'Grant / Prize', 'challenge': 'Challenge', 'other': 'Opportunity',
}
# The chips row on the feed (the brief's minimum set); the rest are reachable via search.
FILTER_CHIP_CATEGORIES = [
    'scholarship', 'fellowship', 'competition', 'hackathon', 'internship', 'campus_ambassador',
    'bootcamp', 'leadership', 'entrepreneurship', 'volunteering',
]

DISCIPLINES = [
    ('all', 'All disciplines'),
    ('computer_science', 'Computer Science'),
    ('engineering', 'Engineering'),
    ('mathematics', 'Mathematics'),
    ('statistics', 'Statistics'),
    ('accounting', 'Accounting'),
    ('finance', 'Finance'),
    ('economics', 'Economics'),
    ('business', 'Business'),
    ('marketing', 'Marketing'),
    ('social_sciences', 'Social Sciences'),
    ('sciences', 'Sciences'),
    ('health', 'Health & Medicine'),
    ('law', 'Law'),
    ('arts_humanities', 'Arts & Humanities'),
    ('education', 'Education'),
    ('agriculture', 'Agriculture'),
]
DISCIPLINE_KEYS = [d[0] for d in DISCIPLINES]
DISCIPLINE_LABELS = dict(DISCIPLINES)

LEVELS = [
    ('100', '100 level'), ('200', '200 level'), ('300', '300 level'), ('400', '400 level'),
    ('500', '500 level+'), ('final_year', 'Final year'), ('postgraduate', 'Postgraduate'),
    ('graduate', 'Recent graduates'),
]
LEVEL_KEYS = [lv[0] for lv in LEVELS]
LEVEL_LABELS = dict(LEVELS)

LOCATION_SCOPES = [
    ('nigeria', 'Nigeria'), ('africa', 'Africa'), ('global', 'Global / International'),
    ('local', 'Specific state or campus'),
]
LOCATION_SCOPE_KEYS = [s[0] for s in LOCATION_SCOPES]
LOCATION_SCOPE_LABELS = dict(LOCATION_SCOPES)

DELIVERY_FORMATS = [('online', 'Online'), ('in_person', 'In person'), ('hybrid', 'Hybrid')]
DELIVERY_FORMAT_KEYS = [f[0] for f in DELIVERY_FORMATS]

DEADLINE_FILTERS = [
    ('week', 'Closes within 7 days'), ('month', 'Closes within 30 days'),
    ('later', 'Closes in 30+ days'), ('rolling', 'No closing date published'),
]

# EXTERNAL_WEBVIEW: no partnership; the student applies on the official site (opened
#   over Nelavista, in-app when the site allows framing and an admin enabled it).
# EMBEDDED_FORM: the organisation's own form, embedded because it permits embedding.
# NELAVISTA_APPLICATION: reserved for real partners. No partner workflow exists yet, so
#   students are still sent to the official URL (see effective_application_mode()).
APPLICATION_MODES = ['EXTERNAL_WEBVIEW', 'EMBEDDED_FORM', 'NELAVISTA_APPLICATION']
APPLICATION_MODE_LABELS = {
    'EXTERNAL_WEBVIEW': 'Official site (external)',
    'EMBEDDED_FORM': 'Embedded official form',
    'NELAVISTA_APPLICATION': 'Apply through Nelavista (partners only)',
}
# Partner workflows register here once one actually exists, e.g.
# PARTNER_WORKFLOWS['some-org'] = handler. Empty on purpose.
PARTNER_WORKFLOWS = {}

VERIFICATION_STATUSES = ['unverified', 'verified', 'rejected']
REPORT_REASONS = [
    ('closed', 'It has closed or expired'),
    ('broken_link', 'The application link is broken'),
    ('wrong_details', 'Details are wrong (deadline, eligibility...)'),
    ('scam', 'It looks like a scam or asks for payment'),
    ('other', 'Something else'),
]
REPORT_REASON_KEYS = [r[0] for r in REPORT_REASONS]
EVENT_TYPES = {'view', 'save', 'unsave', 'apply_click', 'applied', 'unapplied', 'share', 'report'}

CLOSING_SOON_DAYS = 7
RECHECK_AFTER_DAYS = 14
NEW_WITHIN_DAYS = 14

# ---------------------------------------------------------------- dates & status

WAT = timedelta(hours=1)  # Nigeria is UTC+1 all year (no DST)


def today_wat():
    return (datetime.utcnow() + WAT).date()


def compute_status(opp, today=None):
    """Returns a dict: key (open|closing_soon|closed|upcoming), label, tone, days_left.
    Purely date-driven (plus the admin's manual close/archive), so a programme can never
    keep showing as open after its deadline has passed. The deadline day itself still
    counts as open (WAT)."""
    today = today or today_wat()
    if opp.manually_closed or opp.is_archived:
        return {'key': 'closed', 'label': 'Closed', 'tone': 'closed', 'days_left': None}
    if opp.opens_at and today < opp.opens_at:
        days = (opp.opens_at - today).days
        return {'key': 'upcoming', 'label': f'Opens {_fmt_date(opp.opens_at, today)}', 'tone': 'upcoming',
                'days_left': None, 'opens_in': days}
    if opp.deadline:
        days_left = (opp.deadline - today).days
        if days_left < 0:
            return {'key': 'closed', 'label': 'Closed', 'tone': 'closed', 'days_left': None}
        if days_left <= CLOSING_SOON_DAYS:
            if days_left == 0:
                label = 'Closes today'
            elif days_left == 1:
                label = 'Closes tomorrow'
            else:
                label = f'Closing in {days_left} days'
            return {'key': 'closing_soon', 'label': label, 'tone': 'soon', 'days_left': days_left}
        return {'key': 'open', 'label': 'Open', 'tone': 'open', 'days_left': days_left}
    return {'key': 'open', 'label': 'Open', 'tone': 'open', 'days_left': None}


def _fmt_date(d, today=None):
    today = today or today_wat()
    s = f"{d.strftime('%b')} {d.day}"
    return s if d.year == today.year else f'{s}, {d.year}'


def format_deadline(opp):
    if opp.deadline:
        return f"{opp.deadline.strftime('%B')} {opp.deadline.day}, {opp.deadline.year}"
    if opp.is_rolling:
        return 'No closing date published'
    return 'Not stated by the organiser'


def is_active(opp, today=None):
    """Open or closing soon: what the main feed shows."""
    return compute_status(opp, today)['key'] in ('open', 'closing_soon')


def is_new(opp, now=None):
    """Published within the last NEW_WITHIN_DAYS. Shown as a quiet "New" on the card."""
    now = now or datetime.utcnow()
    return (opp.published_at or opp.created_at or datetime.min) >= now - timedelta(days=NEW_WITHIN_DAYS)


def needs_recheck(opp, now=None):
    now = now or datetime.utcnow()
    if not opp.last_checked_at:
        return True
    return (now - opp.last_checked_at) > timedelta(days=RECHECK_AFTER_DAYS)


# ---------------------------------------------------------------- visibility

def visible_query():
    """What students may ever see: published, verified, not archived."""
    return StudentOpportunity.query.filter(
        StudentOpportunity.is_published.is_(True),
        StudentOpportunity.is_archived.is_(False),
        StudentOpportunity.verification_status == 'verified',
    )


def can_view(opp, user):
    if user and user.is_admin:
        return True
    return bool(opp.is_published and not opp.is_archived and opp.is_verified)


def effective_application_mode(opp):
    """The mode the student UI actually uses. NELAVISTA_APPLICATION only applies to a real
    partner with a registered workflow. Without one, students go to the official URL."""
    mode = opp.application_mode or 'EXTERNAL_WEBVIEW'
    if mode == 'NELAVISTA_APPLICATION' and not (opp.is_partner and opp.slug in PARTNER_WORKFLOWS):
        return 'EXTERNAL_WEBVIEW'
    if mode == 'EMBEDDED_FORM' and not opp.embed_url:
        return 'EXTERNAL_WEBVIEW'
    return mode


# ---------------------------------------------------------------- profile mapping

_DISCIPLINE_KEYWORDS = [
    ('computer_science', ['computer', 'software', 'information tech', 'information system', 'cyber', 'computing', 'data science', 'artificial intel']),
    ('statistics', ['statistic', 'actuarial']),
    ('mathematics', ['math']),
    ('engineering', ['engineer', 'mechatronic', 'surveying', 'geoinformatic']),
    ('accounting', ['account', 'audit']),
    ('finance', ['finance', 'banking', 'insurance']),
    ('economics', ['economic']),
    ('marketing', ['marketing']),
    ('business', ['business', 'management', 'entrepreneur', 'commerce', 'administration', 'industrial relations']),
    ('law', ['law', 'jurisprudence']),
    ('health', ['medic', 'nursing', 'pharm', 'health', 'anatomy', 'physiology', 'dentist', 'radiograph', 'physiotherap', 'surgery']),
    ('social_sciences', ['sociology', 'political', 'psychology', 'mass comm', 'geography', 'international relations',
                         'social', 'criminology', 'public admin', 'demography', 'journalism']),
    ('education', ['education']),
    ('agriculture', ['agric', 'fisheries', 'forestry', 'animal sci', 'crop', 'soil', 'food sci']),
    ('arts_humanities', ['english', 'history', 'philosophy', 'language', 'linguistic', 'theatre', 'music', 'fine art',
                         'religio', 'literature', 'french', 'arabic', 'yoruba', 'igbo', 'hausa']),
    ('sciences', ['physics', 'chemistry', 'biology', 'biochem', 'microbio', 'botany', 'zoology', 'science', 'geology',
                  'biotech', 'environmental', 'marine']),
]

# Disciplines that usually also suit a student of discipline X. Used to widen "For You"
# so a maths student still sees data, AI and finance programmes.
RELATED_DISCIPLINES = {
    'mathematics': ['statistics', 'computer_science', 'finance', 'economics'],
    'statistics': ['mathematics', 'computer_science', 'finance', 'economics'],
    'computer_science': ['mathematics', 'statistics', 'engineering'],
    'engineering': ['computer_science', 'mathematics', 'sciences'],
    'accounting': ['finance', 'business', 'economics'],
    'finance': ['accounting', 'economics', 'business', 'mathematics'],
    'economics': ['finance', 'business', 'statistics', 'mathematics'],
    'business': ['marketing', 'finance', 'accounting', 'economics'],
    'marketing': ['business'],
    'social_sciences': ['law', 'education', 'arts_humanities'],
    'sciences': ['health', 'agriculture', 'engineering'],
    'health': ['sciences'],
    'law': ['social_sciences'],
    'arts_humanities': ['social_sciences', 'education'],
    'education': ['social_sciences', 'arts_humanities'],
    'agriculture': ['sciences'],
}

# Topic tags that make a listing relevant to a discipline even when the organiser didn't
# list that discipline (e.g. an "AI" hackathon open to all, for a CS or maths student).
DISCIPLINE_TAG_AFFINITY = {
    'computer_science': {'software', 'ai', 'data', 'developer', 'tech', 'coding', 'web', 'cloud', 'cybersecurity', 'machine learning'},
    'mathematics': {'data', 'ai', 'finance', 'quant', 'machine learning', 'analytics'},
    'statistics': {'data', 'ai', 'analytics', 'machine learning', 'finance'},
    'engineering': {'tech', 'hardware', 'energy', 'innovation'},
    'finance': {'finance', 'fintech', 'investment', 'banking'},
    'accounting': {'finance', 'fintech', 'banking'},
    'economics': {'finance', 'policy', 'fintech'},
    'business': {'business', 'startup', 'fintech', 'marketing', 'sales'},
    'marketing': {'marketing', 'brand', 'social media', 'sales'},
}
GENERALLY_USEFUL_CATEGORIES = {'scholarship', 'competition', 'leadership', 'fellowship'}


def discipline_for_department(department):
    text = (department or '').lower()
    if not text:
        return None
    for key, words in _DISCIPLINE_KEYWORDS:
        if any(w in text for w in words):
            return key
    return None


def level_key_for_user(level):
    m = re.search(r'(\d{3})', str(level or ''))
    if not m:
        low = str(level or '').lower()
        if 'post' in low or 'msc' in low or 'phd' in low:
            return 'postgraduate'
        return None
    n = int(m.group(1))
    if n >= 500:
        return '500'
    return str(n) if n in (100, 200, 300, 400) else None


def profile_for(user):
    if not user:
        return {'discipline': None, 'level': None, 'university': None}
    return {
        'discipline': discipline_for_department(user.department),
        'level': level_key_for_user(user.level),
        'university': (user.university or '').strip() or None,
    }


def level_matches(opp, level_key):
    levels = opp.levels
    if not levels or not level_key:
        return True
    if level_key in levels:
        return True
    # "Final year" covers a 400/500-level student even if the organiser didn't list numbers.
    return 'final_year' in levels and level_key in ('400', '500')


def relevance_score(opp, profile):
    """Higher = more relevant. Never negative, and general listings ("all disciplines")
    always score above zero, so personalisation re-orders the feed rather than hiding
    general opportunities."""
    disc = profile.get('discipline')
    level = profile.get('level')
    opp_disc = set(opp.disciplines)
    tags = {t.lower() for t in opp.tags}
    score = 1.0
    if disc:
        if disc in opp_disc:
            score += 6
        elif opp_disc & set(RELATED_DISCIPLINES.get(disc, [])):
            score += 3
        if tags & DISCIPLINE_TAG_AFFINITY.get(disc, set()):
            score += 2.5
    if not opp_disc or 'all' in opp_disc:
        score += 1.5
    if opp.category in GENERALLY_USEFUL_CATEGORIES:
        score += 0.5
    if level and opp.levels:
        score += 1.5 if level_matches(opp, level) else -2
    uni = (profile.get('university') or '').lower()
    if uni and any(t.lower() in uni or uni in t.lower() for t in opp.tags if len(t) >= 3):
        score += 2
    if opp.featured:
        score += 0.5
    return max(score, 0.1)


def is_for_you(opp, profile):
    """A listing counts as "for you" when it targets the student's field (directly, via a
    related field, or via topic tags), or when it's open to every discipline. In every
    case the student's level must not be excluded."""
    if not level_matches(opp, profile.get('level')):
        return False
    disc = profile.get('discipline')
    opp_disc = set(opp.disciplines)
    if not opp_disc or 'all' in opp_disc:
        return True
    if not disc:
        return False
    tags = {t.lower() for t in opp.tags}
    return bool(disc in opp_disc or opp_disc & set(RELATED_DISCIPLINES.get(disc, []))
                or tags & DISCIPLINE_TAG_AFFINITY.get(disc, set()))


# ---------------------------------------------------------------- search & filter

def _haystack(opp):
    parts = [
        opp.title, opp.organization, opp.summary, opp.description, opp.eligibility, opp.benefits,
        opp.eligible_summary, opp.location, LOCATION_SCOPE_LABELS.get(opp.location_scope, ''),
    ]
    parts += [CATEGORY_LABELS.get(c, c) for c in opp.categories] + [CATEGORY_SINGULAR.get(c, '') for c in opp.categories]
    parts += [DISCIPLINE_LABELS.get(d, d) for d in opp.disciplines]
    parts += opp.tags
    return ' '.join(p for p in parts if p).lower().replace('_', ' ')


def matches_search(opp, q):
    terms = [t for t in re.split(r'\s+', (q or '').lower().strip()) if t]
    if not terms:
        return True
    hay = _haystack(opp)
    # "scholarships" should still find "scholarship"
    return all(t in hay or (t.endswith('s') and t[:-1] in hay) for t in terms)


def apply_filters(opps, q=None, category=None, discipline=None, level=None, location=None, deadline=None, today=None):
    today = today or today_wat()
    out = []
    for o in opps:
        if category and category not in o.categories:
            continue
        if discipline and discipline != 'all':
            d = set(o.disciplines)
            if d and 'all' not in d and discipline not in d:
                continue
        if level and not level_matches(o, level):
            continue
        if location and o.location_scope != location:
            continue
        if deadline:
            days = (o.deadline - today).days if o.deadline else None
            if deadline == 'rolling' and o.deadline:
                continue
            if deadline == 'week' and (days is None or days > 7):
                continue
            if deadline == 'month' and (days is None or days > 30):
                continue
            if deadline == 'later' and (days is None or days <= 30):
                continue
        if q and not matches_search(o, q):
            continue
        out.append(o)
    return out


def _deadline_sort_key(o):
    return (o.deadline or date.max, o.title.lower())


def active_opportunities(today=None):
    today = today or today_wat()
    return [o for o in visible_query().all() if is_active(o, today)]


def build_feed(user, args=None, today=None):
    """Everything the Opportunities homepage needs, from one query."""
    args = args or {}
    today = today or today_wat()
    profile = profile_for(user)
    visible = visible_query().all()
    active = [o for o in visible if is_active(o, today)]
    upcoming = sorted([o for o in visible if compute_status(o, today)['key'] == 'upcoming'],
                      key=lambda o: o.opens_at or date.max)

    filters = {
        'q': (args.get('q') or '').strip()[:100],
        'category': args.get('category') if args.get('category') in CATEGORY_KEYS else None,
        'discipline': args.get('discipline') if args.get('discipline') in DISCIPLINE_KEYS else None,
        'level': args.get('level') if args.get('level') in LEVEL_KEYS else None,
        'location': args.get('location') if args.get('location') in LOCATION_SCOPE_KEYS else None,
        'deadline': args.get('deadline') if args.get('deadline') in dict(DEADLINE_FILTERS) else None,
    }
    filtering = any(filters.values())
    results = apply_filters(active, today=today, **filters)
    sort = args.get('sort') if args.get('sort') in ('relevance', 'deadline', 'newest') else 'relevance'
    if sort == 'deadline':
        results.sort(key=_deadline_sort_key)
    elif sort == 'newest':
        results.sort(key=lambda o: o.published_at or o.created_at or datetime.min, reverse=True)
    else:
        results.sort(key=lambda o: (-relevance_score(o, profile), _deadline_sort_key(o)))

    closing = sorted([o for o in active if compute_status(o, today)['key'] == 'closing_soon'], key=_deadline_sort_key)
    featured = sorted([o for o in active if o.featured], key=_deadline_sort_key)
    new_cutoff = datetime.utcnow() - timedelta(days=NEW_WITHIN_DAYS)
    new = sorted([o for o in active if (o.published_at or o.created_at or datetime.min) >= new_cutoff],
                 key=lambda o: o.published_at or o.created_at, reverse=True)
    for_you = sorted([o for o in active if is_for_you(o, profile)],
                     key=lambda o: (-relevance_score(o, profile), _deadline_sort_key(o)))

    return {
        'profile': profile, 'filters': filters, 'filtering': filtering, 'sort': sort,
        'results': results, 'total_active': len(active),
        'closing_soon': closing[:8], 'featured': featured[:8], 'new': new[:8], 'for_you': for_you[:8],
        'upcoming': upcoming[:6],
    }


# ---------------------------------------------------------------- per-user state

def user_state(user, opp_ids=None):
    """{opportunity_id: {'saved': bool, 'applied_at': datetime|None}} for one student."""
    if not user:
        return {}
    saves = StudentOpportunitySave.query.filter_by(user_id=user.id)
    apps = StudentOpportunityApplication.query.filter_by(user_id=user.id)
    if opp_ids is not None:
        ids = list(opp_ids)
        if not ids:
            return {}
        saves = saves.filter(StudentOpportunitySave.opportunity_id.in_(ids))
        apps = apps.filter(StudentOpportunityApplication.opportunity_id.in_(ids))
    state = {}
    for s in saves.all():
        state.setdefault(s.opportunity_id, {'saved': False, 'applied_at': None})['saved'] = True
    for a in apps.all():
        state.setdefault(a.opportunity_id, {'saved': False, 'applied_at': None})['applied_at'] = a.applied_at
    return state


def log_event(opp, user, event_type, channel=None):
    if event_type not in EVENT_TYPES:
        raise ValueError(f'Unknown event type: {event_type}')
    db.session.add(StudentOpportunityEvent(
        opportunity_id=opp.id, user_id=user.id if user else None, event_type=event_type,
        channel=(channel or '')[:30] or None,
    ))


def set_saved(opp, user, saved):
    existing = StudentOpportunitySave.query.filter_by(user_id=user.id, opportunity_id=opp.id).first()
    if saved and not existing:
        db.session.add(StudentOpportunitySave(user_id=user.id, opportunity_id=opp.id))
        log_event(opp, user, 'save')
    elif not saved and existing:
        db.session.delete(existing)
        log_event(opp, user, 'unsave')
    return saved


def set_applied(opp, user, applied):
    existing = StudentOpportunityApplication.query.filter_by(user_id=user.id, opportunity_id=opp.id).first()
    if applied and not existing:
        existing = StudentOpportunityApplication(user_id=user.id, opportunity_id=opp.id)
        db.session.add(existing)
        log_event(opp, user, 'applied')
    elif not applied and existing:
        db.session.delete(existing)
        log_event(opp, user, 'unapplied')
        existing = None
    return existing


def my_opportunities(user, today=None):
    today = today or today_wat()
    profile = profile_for(user)
    saves = (StudentOpportunitySave.query.filter_by(user_id=user.id)
             .order_by(StudentOpportunitySave.created_at.desc()).all())
    apps = (StudentOpportunityApplication.query.filter_by(user_id=user.id)
            .order_by(StudentOpportunityApplication.applied_at.desc()).all())
    applied_ids = {a.opportunity_id for a in apps}
    # Saved/applied lists keep showing an item even after it closes (it's the student's
    # own history), but never one an admin has unpublished as wrong or unverified.
    saved = [s.opportunity for s in saves if can_view(s.opportunity, None)]
    applied = [a for a in apps if can_view(a.opportunity, None)]
    closing = sorted([o for o in saved if compute_status(o, today)['key'] == 'closing_soon' and o.id not in applied_ids],
                     key=_deadline_sort_key)
    active = active_opportunities(today)
    recommended = sorted([o for o in active if is_for_you(o, profile) and o.id not in applied_ids],
                         key=lambda o: (-relevance_score(o, profile), _deadline_sort_key(o)))[:20]
    return {'saved': saved, 'applied': applied, 'closing': closing, 'recommended': recommended}


# ---------------------------------------------------------------- admin

def _clean(value, max_len=None):
    value = (value or '').strip()
    if max_len:
        value = value[:max_len]
    return value or None


def _parse_list(value, allowed=None, max_items=20):
    if isinstance(value, (list, tuple)):
        items = value
    else:
        items = re.split(r'[,\n]', value or '')
    out = []
    for item in items:
        item = str(item).strip()
        if not item:
            continue
        if allowed is not None and item not in allowed:
            continue
        if item not in out:
            out.append(item[:40])
    return out[:max_items]


def _parse_date(value, field, errors):
    value = (value or '').strip()
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        errors.append(f'{field} must be a date (YYYY-MM-DD).')
        return None


def slugify(text):
    slug = re.sub(r'[^a-z0-9]+', '-', (text or '').lower()).strip('-')
    return slug[:150] or 'opportunity'


def unique_slug(base, exclude_id=None):
    slug, n = base, 2
    while True:
        q = StudentOpportunity.query.filter_by(slug=slug)
        if exclude_id:
            q = q.filter(StudentOpportunity.id != exclude_id)
        if not q.first():
            return slug
        slug = f'{base}-{n}'
        n += 1


def apply_form(opp, form, getlist=None):
    """Copies an admin form onto `opp`. Returns a list of error strings (empty = valid).
    `getlist` is request.form.getlist for multi-value fields."""
    errors = []
    getlist = getlist or (lambda k: form.get(k) or [])
    opp.title = _clean(form.get('title'), 200) or ''
    opp.organization = _clean(form.get('organization'), 150) or ''
    if not opp.title:
        errors.append('Title is required.')
    if not opp.organization:
        errors.append('Organisation is required.')
    opp.summary = _clean(form.get('summary'), 300)
    opp.eligible_summary = _clean(form.get('eligible_summary'), 150)
    for field in ('description', 'eligibility', 'benefits', 'requirements', 'application_steps', 'verification_notes'):
        setattr(opp, field, _clean(form.get(field)))

    category = form.get('category') or 'other'
    opp.category = category if category in CATEGORY_KEYS else 'other'
    opp.categories_json = json.dumps([c for c in _parse_list(getlist('categories'), CATEGORY_KEYS) if c != opp.category])
    opp.disciplines_json = json.dumps(_parse_list(getlist('disciplines'), DISCIPLINE_KEYS))
    opp.levels_json = json.dumps(_parse_list(getlist('levels'), LEVEL_KEYS))
    opp.tags_json = json.dumps(_parse_list(form.get('tags'), None, 30))
    scope = form.get('location_scope') or 'nigeria'
    opp.location_scope = scope if scope in LOCATION_SCOPE_KEYS else 'nigeria'
    opp.location = _clean(form.get('location'), 150)
    fmt = form.get('delivery_format') or None
    opp.delivery_format = fmt if fmt in DELIVERY_FORMAT_KEYS else None

    opp.opens_at = _parse_date(form.get('opens_at'), 'Opening date', errors)
    opp.deadline = _parse_date(form.get('deadline'), 'Deadline', errors)
    opp.is_rolling = bool(form.get('is_rolling'))
    opp.deadline_note = _clean(form.get('deadline_note'), 200)
    if opp.opens_at and opp.deadline and opp.opens_at > opp.deadline:
        errors.append('Opening date is after the deadline.')

    for field in ('application_url', 'official_website', 'source_url', 'embed_url'):
        raw = (form.get(field) or '').strip()
        clean = safe_external_url(raw)
        if raw and not clean:
            errors.append(f'{field.replace("_", " ").capitalize()} must be a full http(s) link.')
        setattr(opp, field, clean)

    opp.is_partner = bool(form.get('is_partner'))
    opp.partner_note = _clean(form.get('partner_note'), 300)
    mode = form.get('application_mode') or 'EXTERNAL_WEBVIEW'
    if mode not in APPLICATION_MODES:
        mode = 'EXTERNAL_WEBVIEW'
    if mode == 'NELAVISTA_APPLICATION' and not opp.is_partner:
        errors.append('"Apply through Nelavista" is only for organisations that have actually partnered with Nelavista. '
                      'Tick "Signed partner" and record the agreement, or use the official site.')
    if mode == 'EMBEDDED_FORM' and not opp.embed_url:
        errors.append('Embedded form needs the embed URL the organisation provides.')
    opp.application_mode = mode
    if opp.is_partner and not opp.partner_note:
        errors.append('Record the partnership (agreement reference/contact) in the partner note.')
    opp.allows_in_app_view = bool(form.get('allows_in_app_view')) and bool(opp.framing_checked_at)
    opp.featured = bool(form.get('featured'))

    if not opp.slug or form.get('regenerate_slug'):
        opp.slug = unique_slug(slugify(f'{opp.organization} {opp.title}'), exclude_id=opp.id)
    # Edits to a verified listing keep it verified (an admin is making them), but a
    # published listing that no longer passes publish checks is unpublished, not left live.
    if opp.is_published and publish_problems(opp):
        opp.is_published = False
    return errors


def publish_problems(opp, today=None):
    """Why this listing can't be shown to students yet (empty list = publishable)."""
    problems = []
    if opp.verification_status != 'verified':
        problems.append('Mark it verified after checking the official source.')
    if not opp.source_url:
        problems.append('Add the source URL you verified it from.')
    if not opp.application_url and effective_application_mode(opp) != 'EMBEDDED_FORM':
        problems.append('Add the official application URL.')
    if not opp.deadline and not opp.is_rolling:
        problems.append('Set the deadline, or tick "No closing date published" if the official page gives none.')
    if compute_status(opp, today)['key'] == 'closed':
        problems.append('It is closed. Closed programmes are never published as open.')
    if opp.is_archived:
        problems.append('It is archived.')
    return problems


def verify_problems(opp):
    problems = []
    if not opp.source_url:
        problems.append('Add the source URL first. Nothing is marked verified without its source.')
    if not opp.application_url and not opp.embed_url:
        problems.append('Add the official application URL (or embed URL) first.')
    return problems


def admin_action(opp, action, admin):
    """Applies one admin action; returns (ok, message)."""
    now = datetime.utcnow()
    if action == 'verify':
        problems = verify_problems(opp)
        if problems:
            return False, ' '.join(problems)
        opp.verification_status = 'verified'
        opp.verified_at = now
        opp.verified_by_id = admin.id
        opp.last_checked_at = now
        return True, 'Marked verified.'
    if action == 'mark_checked':
        if opp.verification_status != 'verified':
            return False, 'Verify it first.'
        opp.last_checked_at = now
        return True, 'Re-check recorded.'
    if action == 'unverify':
        opp.verification_status = 'unverified'
        opp.verified_at = None
        opp.is_published = False
        return True, 'Marked unverified and unpublished.'
    if action == 'reject':
        opp.verification_status = 'rejected'
        opp.is_published = False
        return True, 'Rejected and unpublished.'
    if action == 'publish':
        problems = publish_problems(opp)
        if problems:
            return False, 'Not published: ' + ' '.join(problems)
        opp.is_published = True
        opp.published_at = opp.published_at or now
        return True, 'Published.'
    if action == 'unpublish':
        opp.is_published = False
        return True, 'Unpublished.'
    if action == 'close':
        opp.manually_closed = True
        return True, 'Marked closed. It has left the open feed.'
    if action == 'reopen':
        opp.manually_closed = False
        if opp.is_published and publish_problems(opp):
            opp.is_published = False
            return True, 'Reopened, but unpublished until the publish checks pass.'
        return True, 'Reopened.'
    if action == 'feature':
        opp.featured = True
        return True, 'Featured.'
    if action == 'unfeature':
        opp.featured = False
        return True, 'No longer featured.'
    if action == 'archive':
        opp.is_archived = True
        opp.is_published = False
        return True, 'Archived.'
    if action == 'unarchive':
        opp.is_archived = False
        return True, 'Restored from archive (unpublished).'
    return False, 'Unknown action.'


def check_framing(url):
    """Best-effort check of whether an official page allows being shown in an iframe:
    looks at X-Frame-Options and CSP frame-ancestors on the final response. Returns
    True/False, or None if the page couldn't be fetched. Even True isn't a guarantee
    (login cookies and script frame-busting can still break it), which is why the in-app
    view always keeps an "Open in browser" button."""
    from app.services.link_fetch_service import _is_safe_url, _get_with_safe_redirects
    if not url or not _is_safe_url(url):
        return None
    try:
        resp = _get_with_safe_redirects(url, timeout=6, stream=True)
    except Exception:
        return None
    if resp is None:
        return None
    try:
        headers = {k.lower(): v for k, v in resp.headers.items()}
    finally:
        try:
            resp.close()
        except Exception:
            pass
    xfo = (headers.get('x-frame-options') or '').lower()
    if 'deny' in xfo or 'sameorigin' in xfo:
        return False
    csp = (headers.get('content-security-policy') or '').lower()
    m = re.search(r'frame-ancestors([^;]*)', csp)
    if m:
        sources = m.group(1).split()
        if not sources or "'none'" in sources:
            return False
        if '*' not in sources and not any('nelavista' in s for s in sources):
            return False
    return True


def analytics_for(opp_ids=None):
    """{opportunity_id: Counter(event_type -> count)}, plus current saves/applied totals."""
    q = db.session.query(StudentOpportunityEvent.opportunity_id, StudentOpportunityEvent.event_type,
                         db.func.count(StudentOpportunityEvent.id))
    if opp_ids is not None:
        q = q.filter(StudentOpportunityEvent.opportunity_id.in_(list(opp_ids) or [-1]))
    out = {}
    for oid, etype, n in q.group_by(StudentOpportunityEvent.opportunity_id, StudentOpportunityEvent.event_type).all():
        out.setdefault(oid, Counter())[etype] = n
    viewers = db.session.query(StudentOpportunityEvent.opportunity_id,
                               db.func.count(db.distinct(StudentOpportunityEvent.user_id))) \
        .filter(StudentOpportunityEvent.event_type == 'view')
    if opp_ids is not None:
        viewers = viewers.filter(StudentOpportunityEvent.opportunity_id.in_(list(opp_ids) or [-1]))
    for oid, n in viewers.group_by(StudentOpportunityEvent.opportunity_id).all():
        out.setdefault(oid, Counter())['unique_viewers'] = n
    for model, key in ((StudentOpportunitySave, 'saved_now'), (StudentOpportunityApplication, 'applied_now')):
        rows = db.session.query(model.opportunity_id, db.func.count(model.id))
        if opp_ids is not None:
            rows = rows.filter(model.opportunity_id.in_(list(opp_ids) or [-1]))
        for oid, n in rows.group_by(model.opportunity_id).all():
            out.setdefault(oid, Counter())[key] = n
    return out


def create_report(opp, user, reason, details):
    if reason not in REPORT_REASON_KEYS:
        raise ValueError('Pick a reason.')
    db.session.add(StudentOpportunityReport(
        opportunity_id=opp.id, user_id=user.id if user else None, reason=reason,
        details=_clean(details, 1000),
    ))
    log_event(opp, user, 'report', channel=reason)
