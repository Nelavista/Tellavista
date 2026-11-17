"""Content and data for Nelavista Talent (/talent).

Every claim the Talent pages make lives here, so the honesty rules live in one place.
Strong positioning is fine; invented evidence is not.

- METRICS: only real numbers. A metric whose value is None is not rendered, and the
  metrics band only appears once at least three real metrics exist.
- VETTING_LAYERS: each layer is 'live' (the product does it today) or 'rolling_out'.
  Only live layers become badges on profiles. Flip a layer to 'live' when it ships.
- PREVIEW_PROFILES: illustrative profiles that show the format of a Nelavista Talent
  profile. They are anonymous on purpose (role, not a person's name; no photo) and every
  surface labels them as previews; their pages are noindex. Real, consented profiles
  replace them through `featured_talent()`.
- CLIENT_LOGOS / TESTIMONIALS / CASE_STUDIES: empty until an organisation or person
  agrees to be named. Their sections render nothing while empty.
- PHOTOS: licensed stock photography (Unsplash License), served from Unsplash's CDN at
  responsive sizes. They depict professionals at work and are never attached to a
  profile, so no photographed person is presented as a candidate.
"""
from __future__ import annotations

from urllib.parse import quote

# ── Contact ──────────────────────────────────────────────────────────────────────────────
CONTACT_EMAIL = 'support@nelavista.com'
WHATSAPP_NUMBER = '2347087896654'          # international format, digits only
WHATSAPP_DISPLAY = '+234 708 789 6654'


def whatsapp_url(text: str = 'Hello Nelavista Talent, I would like to discuss hiring talent.') -> str:
    return f'https://wa.me/{WHATSAPP_NUMBER}?text={quote(text)}'


# ── Photography ──────────────────────────────────────────────────────────────────────────
_UNSPLASH = 'https://images.unsplash.com/'
PHOTOS = {
    'hero': {'id': 'photo-1635766828498-49dec8c0cc56', 'pos': '50% 40%',
             'alt': 'Two colleagues reviewing a design together on a laptop in an office',
             'credit': 'cutinamoment', 'url': 'https://unsplash.com/photos/k5Rltk9X1-U'},
    'engineers': {'id': 'photo-1528901166007-3784c7dd3653', 'pos': '50% 50%',
                  'alt': 'Software developers working through code together at a tech hub in Nairobi',
                  'credit': 'Disruptxn', 'url': 'https://unsplash.com/photos/kwzWjTnDPLk'},
    'meeting': {'id': 'photo-1739298061707-cefee19941b7', 'pos': '50% 50%',
                'alt': 'A team meeting around a conference table',
                'credit': 'ninthgrid', 'url': 'https://unsplash.com/photos/AekHsx1SxXQ'},
    'professional': {'id': 'photo-1638802126124-1b7598461d5c', 'pos': '50% 30%',
                     'alt': 'A professional reviewing work on a tablet in a modern office',
                     'credit': 'cutinamoment', 'url': 'https://unsplash.com/photos/AszfTJfly_U'},
    'at_work': {'id': 'photo-1635768229592-8c2532d33cb7', 'pos': '60% 40%',
                'alt': 'A professional working on a laptop at his desk',
                'credit': 'cutinamoment', 'url': 'https://unsplash.com/photos/u1QJm4o7cXk'},
    'data': {'id': 'photo-1532522953890-ccc87dfeb0b7', 'pos': '40% 50%',
             'alt': 'Analysing charts on a laptop',
             'credit': 'Disruptxn', 'url': 'https://unsplash.com/photos/xcUVwwdsWis'},
}
PHOTO_WIDTHS = (480, 768, 1080, 1440, 1920)


def photo_src(key: str, w: int = 1080, h: int | None = None) -> str:
    p = PHOTOS[key]
    crop = f'&h={h}&fit=crop&crop=faces,center' if h else ''
    return f'{_UNSPLASH}{p["id"]}?auto=format&q=70&w={w}{crop}'


def photo_srcset(key: str, ratio: float | None = None, widths=PHOTO_WIDTHS) -> str:
    """ratio = height / width; None keeps the original aspect."""
    return ', '.join(f'{photo_src(key, w, round(w * ratio) if ratio else None)} {w}w' for w in widths)


PHOTO_CREDITS = sorted({p['credit'] for p in PHOTOS.values()})


# ── Positioning ──────────────────────────────────────────────────────────────────────────
PRINCIPLES = [
    {'name': 'Vetted talent', 'icon': 'ri-shield-check-line', 'text': 'Screened against a clear standard before they reach you.'},
    {'name': 'Verified profiles', 'icon': 'ri-profile-line', 'text': 'Reviewed by our team against the evidence behind them.'},
    {'name': 'Skills assessed', 'icon': 'ri-medal-line', 'text': 'Role-based assessments, scored against a pass mark.'},
    {'name': 'Curated matching', 'icon': 'ri-team-line', 'text': 'A short list of people who fit your brief, picked by people.'},
    {'name': 'Remote ready', 'icon': 'ri-global-line', 'text': 'Professionals set up to work with distributed teams.'},
]

# status: 'live' = done by the product today; 'rolling_out' = part of the standard, shipping.
VETTING_LAYERS = [
    {'key': 'identity', 'name': 'Identity', 'lead': 'Know who you’re working with.',
     'text': 'Identity checks before a professional is introduced to an employer.',
     'icon': 'ri-fingerprint-line', 'status': 'rolling_out', 'badge': 'Identity verified'},
    {'key': 'skills', 'name': 'Skills', 'lead': 'Assess what the role actually needs.',
     'text': 'Role-based assessments with a fixed pass mark. Results are recorded, never self-reported.',
     'icon': 'ri-medal-line', 'status': 'live', 'badge': 'Skills assessed'},
    {'key': 'practical', 'name': 'Practical evidence', 'lead': 'Look past the CV.',
     'text': 'Real tasks and projects, reviewed against a quality bar before a skill counts.',
     'icon': 'ri-hammer-line', 'status': 'live', 'badge': 'Work reviewed'},
    {'key': 'readiness', 'name': 'Professional readiness', 'lead': 'Ready to work with your team.',
     'text': 'Communication and work-readiness review for client-facing and remote roles.',
     'icon': 'ri-chat-check-line', 'status': 'rolling_out', 'badge': 'Readiness reviewed'},
    {'key': 'profile', 'name': 'Profile quality', 'lead': 'Signals you can act on.',
     'text': 'A structured profile reviewed by our team, built on evidence rather than claims.',
     'icon': 'ri-profile-line', 'status': 'live', 'badge': 'Profile verified'},
]
LAYER_BY_KEY = {layer['key']: layer for layer in VETTING_LAYERS}
LIVE_BADGES = [layer for layer in VETTING_LAYERS if layer['status'] == 'live']
STATUS_LABELS = {'live': 'Live', 'rolling_out': 'Rolling out'}

CATEGORIES = [
    {'slug': 'technology', 'name': 'Technology', 'icon': 'ri-code-s-slash-line',
     'desc': 'Software development, web, QA and data.',
     'roles': ['Software developer', 'Web developer', 'QA tester', 'Data analyst'], 'photo': 'engineers'},
    {'slug': 'customer-experience', 'name': 'Customer Experience', 'icon': 'ri-customer-service-2-line',
     'desc': 'Customer support, chat support and CRM.',
     'roles': ['Support specialist', 'Chat agent', 'CRM administrator']},
    {'slug': 'operations', 'name': 'Operations', 'icon': 'ri-settings-4-line',
     'desc': 'Data operations, administration and research support.',
     'roles': ['Data operations', 'Operations associate', 'Admin specialist']},
    {'slug': 'marketing', 'name': 'Marketing', 'icon': 'ri-advertisement-line',
     'desc': 'Digital marketing, social media and content.',
     'roles': ['Digital marketer', 'Social media manager', 'Content writer']},
    {'slug': 'design', 'name': 'Design', 'icon': 'ri-pen-nib-line',
     'desc': 'Graphic design, UI/UX and creative.',
     'roles': ['UI/UX designer', 'Graphic designer', 'Motion designer']},
    {'slug': 'finance-business', 'name': 'Finance & Business', 'icon': 'ri-line-chart-line',
     'desc': 'Accounting support, analysis and business research.',
     'roles': ['Bookkeeper', 'Financial analyst', 'Business analyst']},
    {'slug': 'virtual-assistance', 'name': 'Virtual Assistance', 'icon': 'ri-calendar-check-line',
     'desc': 'Administrative and executive support.',
     'roles': ['Executive assistant', 'Virtual assistant', 'Project coordinator']},
    {'slug': 'research', 'name': 'Research', 'icon': 'ri-search-eye-line',
     'desc': 'Market research, data collection and analysis.',
     'roles': ['Research analyst', 'Data collector', 'AI data specialist']},
]
CATEGORY_BY_SLUG = {c['slug']: c for c in CATEGORIES}

EMPLOYER_STEPS = [
    {'n': '01', 'title': 'Tell us what you’re hiring for.', 'text': 'Role, skills, workload, timeline and how you want to engage. A few minutes, no account needed.'},
    {'n': '02', 'title': 'We identify relevant talent.', 'text': 'Our team searches the network against your brief and checks the evidence behind every candidate.'},
    {'n': '03', 'title': 'Review a curated shortlist.', 'text': 'A focused set of profiles with assessment results, reviewed work and availability.'},
    {'n': '04', 'title': 'Engage the professionals who fit.', 'text': 'Interview, then hire, contract or outsource on terms that suit your organisation.'},
]

USE_CASES = [
    {'title': 'Build remote teams', 'text': 'Assemble a dependable remote team and grow it as the work grows.', 'icon': 'ri-team-line'},
    {'title': 'Scale operations', 'text': 'Add trained people to operational work without slowing down.', 'icon': 'ri-stack-line'},
    {'title': 'Outsource business functions', 'text': 'Hand over support, data or admin to a managed group.', 'icon': 'ri-git-branch-line'},
    {'title': 'Find project-based talent', 'text': 'Specialists for a defined scope and timeline.', 'icon': 'ri-flag-2-line'},
    {'title': 'Strengthen customer support', 'text': 'Assessed support professionals for chat, email and phone.', 'icon': 'ri-customer-service-line'},
    {'title': 'Access specialist skills', 'text': 'Design, data, development and marketing expertise on demand.', 'icon': 'ri-cpu-line'},
    {'title': 'Handle temporary workload', 'text': 'Cover peaks, backlogs and seasonal demand.', 'icon': 'ri-time-line'},
    {'title': 'Add flexible capacity', 'text': 'Part-time and contract talent that flexes with your plans.', 'icon': 'ri-equalizer-line'},
]

# What an employer sees beyond a CV. 'status' mirrors the vetting layer that backs it.
EMPLOYER_SIGNALS = [
    {'name': 'Relevant skills', 'text': 'Skills mapped to your role, not a keyword list.', 'status': 'live'},
    {'name': 'Assessment results', 'text': 'Scores against a fixed pass mark, per skill.', 'status': 'live'},
    {'name': 'Portfolio evidence', 'text': 'Projects and practical work, with the reviewer’s verdict.', 'status': 'live'},
    {'name': 'Experience', 'text': 'Roles, responsibilities and the work delivered.', 'status': 'live'},
    {'name': 'Availability', 'text': 'Hours, start date, time zone and preferred engagement.', 'status': 'live'},
    {'name': 'Professional profile', 'text': 'A structured profile reviewed by our team.', 'status': 'live'},
    {'name': 'Verified identity', 'text': 'Identity checks before introduction.', 'status': 'rolling_out'},
]

ECOSYSTEM = [
    {'name': 'Skills', 'text': 'Structured skill tracks across technical and business roles.'},
    {'name': 'Assessment', 'text': 'Role-based tests with recorded, comparable results.'},
    {'name': 'Evidence', 'text': 'Practical work reviewed against a quality bar.'},
    {'name': 'Professional profiles', 'text': 'One profile that shows what someone can actually do.'},
    {'name': 'Opportunity', 'text': 'Introductions to organisations with real work.'},
]

TALENT_JOURNEY = [
    {'title': 'Build skills', 'text': 'Structured tracks in the skills employers hire for.'},
    {'title': 'Demonstrate ability', 'text': 'Practical tasks that mirror real work.'},
    {'title': 'Get assessed', 'text': 'Scored, role-based assessments.'},
    {'title': 'Build your profile', 'text': 'Evidence, not just claims.'},
    {'title': 'Get discovered', 'text': 'Visible to organisations, on your terms.'},
    {'title': 'Work', 'text': 'Introductions when your evidence fits a brief.'},
]

AFRICA_POINTS = [
    {'title': 'Capability', 'text': 'Professionals with skills that have been tested, not just listed.'},
    {'title': 'Access', 'text': 'A curated route to talent across the continent, with a team that knows the network.'},
    {'title': 'Working hours that overlap', 'text': 'West, Central and East African time zones sit within a few hours of Europe and the Middle East.'},
]

ABOUT = ('Nelavista Talent is part of Nelavista. It connects organisations with skilled professionals '
         'through a talent ecosystem built around learning, skills, assessment and opportunity.')

# ── Proof (real only) ────────────────────────────────────────────────────────────────────
# Add only with written permission:
# CLIENT_LOGOS: {'name', 'logo' (static path), 'url'}
# TESTIMONIALS: {'quote', 'name', 'role', 'company'}
# CASE_STUDIES: {'title', 'need', 'talent', 'work', 'result'}
CLIENT_LOGOS: list[dict] = []
TESTIMONIALS: list[dict] = []
CASE_STUDIES: list[dict] = []

# ── Metrics (real only) ──────────────────────────────────────────────────────────────────
# Fill these with counted numbers. None = hidden.
METRICS = [
    {'key': 'talent', 'label': 'Professionals in the network', 'value': None},
    {'key': 'assessed', 'label': 'Professionals assessed', 'value': None},
    {'key': 'companies', 'label': 'Companies served', 'value': None},
    {'key': 'engagements', 'label': 'Successful engagements', 'value': None},
    {'key': 'countries', 'label': 'Countries represented', 'value': None},
]
METRICS_MIN_TO_SHOW = 3


def build_metrics(assessment_tracks: int | None = None) -> list[dict]:
    metrics = [m for m in METRICS if m['value']]
    metrics.append({'key': 'categories', 'label': 'Talent categories', 'value': str(len(CATEGORIES))})
    if assessment_tracks:
        metrics.append({'key': 'tracks', 'label': 'Role-based assessment tracks', 'value': str(assessment_tracks)})
    return metrics if len(metrics) >= METRICS_MIN_TO_SHOW else []


# ── Request form options ─────────────────────────────────────────────────────────────────
ENGAGEMENT_TYPES = [
    ('full_time', 'Full-time hire'), ('part_time', 'Part-time'), ('contract', 'Fixed-term contract'),
    ('project', 'Project-based'), ('outsourced', 'Outsourced team or function'), ('unsure', 'Not sure yet'),
]
HEADCOUNTS = [('1', '1 person'), ('2-5', '2–5 people'), ('6-15', '6–15 people'), ('16+', '16 or more')]
START_WINDOWS = [
    ('asap', 'As soon as possible'), ('2_weeks', 'Within 2 weeks'), ('1_month', 'Within a month'),
    ('1_3_months', 'In 1–3 months'), ('exploring', 'Just exploring'),
]
BUDGET_RANGES = [
    ('lt_300', 'Under $300'), ('300_600', '$300–$600'), ('600_1200', '$600–$1,200'),
    ('1200_2500', '$1,200–$2,500'), ('gt_2500', 'Over $2,500'), ('discuss', 'Prefer to discuss'),
]
TIMEZONES = [
    ('any', 'No requirement'), ('wat', 'West Africa (WAT)'), ('eat', 'East Africa (EAT)'),
    ('europe', 'Europe'), ('north_america', 'North America'), ('other', 'Other'),
]
REQUEST_STATUSES = [('new', 'New'), ('contacted', 'Contacted'), ('shortlisting', 'Shortlisting'),
                    ('shortlist_sent', 'Shortlist sent'), ('closed', 'Closed')]


def label_for(options, value):
    return dict(options).get(value, value or '')


# ── Preview profiles ─────────────────────────────────────────────────────────────────────
# Anonymous by design: they show the profile format, not people. `checks` keys are
# VETTING_LAYERS keys -> 'verified' | 'pending'. Only live layers are shown as badges.
LEVELS = ['Entry', 'Mid-level', 'Senior']
WORK_TYPES = ['Full-time', 'Part-time', 'Contract', 'Project-based']

PREVIEW_PROFILES = [
    {
        'slug': 'preview-customer-support-specialist', 'role': 'Customer Support Specialist',
        'category': 'customer-experience', 'country': 'Nigeria', 'timezone': 'WAT · UTC+1',
        'level': 'Mid-level', 'years': '3 years', 'availability': 'available', 'availability_text': 'Available now',
        'hours': '40 hrs / week', 'work_types': ['Full-time', 'Contract'],
        'skills': ['Customer Support', 'Zendesk', 'CRM', 'Operations', 'Written Communication'],
        'languages': [('English', 'Professional'), ('Yoruba', 'Native')],
        'summary': 'Handles high-volume chat and email support with a calm, clear tone. Strongest on ticket triage, accurate written replies and keeping CRM records clean.',
        'checks': {'skills': 'verified', 'practical': 'verified', 'profile': 'verified'},
        'assessments': [{'name': 'Customer Support Fundamentals', 'score': 86, 'pass': 70},
                        {'name': 'Written Communication', 'score': 81, 'pass': 70}],
        'projects': [{'title': 'Support macro library', 'text': 'Rewrote 30 reply templates for an e-commerce helpdesk, reviewed for tone and accuracy.', 'status': 'Reviewed'},
                     {'title': 'Ticket triage exercise', 'text': 'Categorised and prioritised 120 tickets against an SLA policy.', 'status': 'Reviewed'}],
        'experience': [{'title': 'Customer support associate', 'org': 'E-commerce retailer', 'period': '2 years'},
                       {'title': 'Front desk & client service', 'org': 'Professional services firm', 'period': '1 year'}],
        'portfolio': 2, 'completeness': 92,
        'preferences': ['Remote', 'Customer-facing roles', 'Overlap with UK/EU hours'],
    },
    {
        'slug': 'preview-frontend-developer', 'role': 'Front-end Developer',
        'category': 'technology', 'country': 'Ghana', 'timezone': 'GMT · UTC+0',
        'level': 'Mid-level', 'years': '4 years', 'availability': 'limited', 'availability_text': 'From next month',
        'hours': '30 hrs / week', 'work_types': ['Contract', 'Project-based'],
        'skills': ['React', 'TypeScript', 'HTML & CSS', 'Accessibility', 'Git'],
        'languages': [('English', 'Professional'), ('Twi', 'Native')],
        'summary': 'Builds fast, accessible interfaces from design files. Comfortable owning a feature end to end and writing clear pull requests.',
        'checks': {'skills': 'verified', 'practical': 'verified', 'profile': 'verified'},
        'assessments': [{'name': 'Front-end Engineering', 'score': 84, 'pass': 70},
                        {'name': 'JavaScript & TypeScript', 'score': 79, 'pass': 70}],
        'projects': [{'title': 'Booking flow rebuild', 'text': 'Rebuilt a multi-step booking flow in React with form validation and tests.', 'status': 'Reviewed'}],
        'experience': [{'title': 'Front-end developer', 'org': 'Fintech product team', 'period': '2 years'},
                       {'title': 'Freelance web developer', 'org': 'Independent', 'period': '2 years'}],
        'portfolio': 3, 'completeness': 95,
        'preferences': ['Remote', 'Product teams', 'Async-friendly'],
    },
    {
        'slug': 'preview-data-operations-analyst', 'role': 'Data Operations Analyst',
        'category': 'operations', 'country': 'Kenya', 'timezone': 'EAT · UTC+3',
        'level': 'Mid-level', 'years': '3 years', 'availability': 'available', 'availability_text': 'Available now',
        'hours': '40 hrs / week', 'work_types': ['Full-time', 'Contract'],
        'skills': ['Excel', 'Google Sheets', 'SQL', 'Data Cleaning', 'Reporting'],
        'languages': [('English', 'Professional'), ('Swahili', 'Native')],
        'summary': 'Turns messy operational data into clean, reliable reports. Methodical, documents every step, and flags anomalies early.',
        'checks': {'skills': 'verified', 'practical': 'verified', 'profile': 'pending'},
        'assessments': [{'name': 'Spreadsheet & Data Operations', 'score': 91, 'pass': 70}],
        'projects': [{'title': 'Inventory reconciliation', 'text': 'De-duplicated and reconciled a 4,000-row product dataset against supplier records.', 'status': 'Reviewed'}],
        'experience': [{'title': 'Operations analyst', 'org': 'Logistics company', 'period': '3 years'}],
        'portfolio': 2, 'completeness': 84,
        'preferences': ['Remote or hybrid', 'Operations teams'],
    },
    {
        'slug': 'preview-product-designer', 'role': 'Product Designer (UI/UX)',
        'category': 'design', 'country': 'Nigeria', 'timezone': 'WAT · UTC+1',
        'level': 'Senior', 'years': '6 years', 'availability': 'available', 'availability_text': 'Available now',
        'hours': '25 hrs / week', 'work_types': ['Contract', 'Project-based'],
        'skills': ['Figma', 'UX Research', 'Design Systems', 'Prototyping'],
        'languages': [('English', 'Professional')],
        'summary': 'Designs clear, restrained products and the systems behind them. Works from research, shows options early and documents decisions.',
        'checks': {'skills': 'verified', 'practical': 'verified', 'profile': 'verified'},
        'assessments': [{'name': 'Product Design Principles', 'score': 88, 'pass': 70}],
        'projects': [{'title': 'Clinic appointment app', 'text': 'Research, flows and a small component library for a patient booking app.', 'status': 'Reviewed'},
                     {'title': 'Design system audit', 'text': 'Consolidated 60 inconsistent components into 18 documented ones.', 'status': 'Reviewed'}],
        'experience': [{'title': 'Senior product designer', 'org': 'SaaS company', 'period': '3 years'},
                       {'title': 'UI designer', 'org': 'Digital agency', 'period': '3 years'}],
        'portfolio': 5, 'completeness': 97,
        'preferences': ['Remote', 'Product teams', 'Design systems work'],
    },
    {
        'slug': 'preview-digital-marketing-specialist', 'role': 'Digital Marketing Specialist',
        'category': 'marketing', 'country': 'South Africa', 'timezone': 'SAST · UTC+2',
        'level': 'Mid-level', 'years': '4 years', 'availability': 'available', 'availability_text': 'Available in 2 weeks',
        'hours': '40 hrs / week', 'work_types': ['Full-time', 'Part-time'],
        'skills': ['Paid Social', 'Google Ads', 'Content Strategy', 'Analytics'],
        'languages': [('English', 'Professional'), ('isiZulu', 'Native')],
        'summary': 'Plans and runs paid and organic campaigns with a close eye on numbers. Writes sharp copy and reports results plainly.',
        'checks': {'skills': 'verified', 'practical': 'pending', 'profile': 'verified'},
        'assessments': [{'name': 'Digital Marketing', 'score': 82, 'pass': 70}],
        'projects': [{'title': 'Campaign teardown', 'text': 'Audited a paid social account and rebuilt the targeting and creative plan.', 'status': 'In review'}],
        'experience': [{'title': 'Marketing executive', 'org': 'Consumer brand', 'period': '4 years'}],
        'portfolio': 2, 'completeness': 86,
        'preferences': ['Remote', 'Growth teams'],
    },
    {
        'slug': 'preview-executive-assistant', 'role': 'Executive Assistant',
        'category': 'virtual-assistance', 'country': 'Kenya', 'timezone': 'EAT · UTC+3',
        'level': 'Senior', 'years': '7 years', 'availability': 'available', 'availability_text': 'Available now',
        'hours': '40 hrs / week', 'work_types': ['Full-time', 'Part-time'],
        'skills': ['Calendar Management', 'Google Workspace', 'Notion', 'Travel Planning'],
        'languages': [('English', 'Professional'), ('Swahili', 'Native')],
        'summary': 'Keeps busy executives organised across time zones. Discreet, quick to respond and careful with confidential information.',
        'checks': {'skills': 'verified', 'practical': 'verified', 'profile': 'verified'},
        'assessments': [{'name': 'Executive Support & Tools', 'score': 90, 'pass': 70}],
        'projects': [{'title': 'Executive week plan', 'text': 'Planned a week of meetings across three time zones from an unstructured request thread.', 'status': 'Reviewed'}],
        'experience': [{'title': 'Executive assistant', 'org': 'Regional consultancy', 'period': '5 years'},
                       {'title': 'Office administrator', 'org': 'Accounting practice', 'period': '2 years'}],
        'portfolio': 1, 'completeness': 90,
        'preferences': ['Remote', 'Executive support'],
    },
    {
        'slug': 'preview-financial-analyst', 'role': 'Financial Analyst',
        'category': 'finance-business', 'country': 'Nigeria', 'timezone': 'WAT · UTC+1',
        'level': 'Mid-level', 'years': '4 years', 'availability': 'limited', 'availability_text': 'Part-time only',
        'hours': '20 hrs / week', 'work_types': ['Part-time', 'Project-based'],
        'skills': ['Financial Modelling', 'Excel', 'Bookkeeping', 'Reporting'],
        'languages': [('English', 'Professional'), ('Igbo', 'Native')],
        'summary': 'Builds clean financial models and monthly reporting packs. Comfortable with bookkeeping support and variance analysis.',
        'checks': {'skills': 'verified', 'practical': 'verified', 'profile': 'verified'},
        'assessments': [{'name': 'Financial Analysis', 'score': 83, 'pass': 70}],
        'projects': [{'title': 'Three-statement model', 'text': 'Built a linked three-statement model for a small retail business.', 'status': 'Reviewed'}],
        'experience': [{'title': 'Finance associate', 'org': 'Advisory firm', 'period': '4 years'}],
        'portfolio': 2, 'completeness': 88,
        'preferences': ['Remote', 'Project work'],
    },
    {
        'slug': 'preview-research-analyst', 'role': 'Research Analyst',
        'category': 'research', 'country': 'Rwanda', 'timezone': 'CAT · UTC+2',
        'level': 'Entry', 'years': '2 years', 'availability': 'available', 'availability_text': 'Available now',
        'hours': '30 hrs / week', 'work_types': ['Contract', 'Project-based'],
        'skills': ['Desk Research', 'Survey Design', 'Data Collection', 'Report Writing'],
        'languages': [('English', 'Professional'), ('French', 'Professional'), ('Kinyarwanda', 'Native')],
        'summary': 'Thorough researcher who writes concise, sourced summaries. Has designed and run surveys and cleaned the results.',
        'checks': {'skills': 'verified', 'practical': 'verified', 'profile': 'pending'},
        'assessments': [{'name': 'Research Methods', 'score': 80, 'pass': 70}],
        'projects': [{'title': 'Market scan: solar retail', 'text': 'Compiled a sourced overview of 20 solar retailers across two markets.', 'status': 'Reviewed'}],
        'experience': [{'title': 'Research assistant', 'org': 'Policy research group', 'period': '2 years'}],
        'portfolio': 2, 'completeness': 80,
        'preferences': ['Remote', 'Research projects', 'French-speaking markets'],
    },
]
PREVIEW_BY_SLUG = {p['slug']: p for p in PREVIEW_PROFILES}
COUNTRIES = sorted({p['country'] for p in PREVIEW_PROFILES})


def badges(profile: dict) -> list[dict]:
    """Verified badges for a profile: only layers that are live and verified for them."""
    return [layer for layer in LIVE_BADGES if profile['checks'].get(layer['key']) == 'verified']


def is_vetted(profile: dict) -> bool:
    return all(profile['checks'].get(layer['key']) == 'verified' for layer in LIVE_BADGES)


def featured_talent() -> list[dict]:
    """Profiles for the public directory. Today: labelled previews. When real professionals
    have consented to a public profile, build their cards here and set is_preview False."""
    return [dict(p, is_preview=True) for p in PREVIEW_PROFILES]


def get_profile(slug: str) -> dict | None:
    p = PREVIEW_BY_SLUG.get(slug)
    return dict(p, is_preview=True) if p else None
