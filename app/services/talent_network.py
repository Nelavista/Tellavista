"""Content and data for Nelavista Talent (/talent).

Everything the Talent pages say about scale, process or people comes from this module, so
the honesty rules live in one place:

- FIGURES: only verified numbers, or numbers counted live from the database. A figure set
  to None is not rendered at all. Never put an estimate here.
- VERIFICATION_STANDARD: each step says whether it is live on Nelavista today ('live') or
  part of the standard we are building towards ('in_development'). The page shows that
  status to visitors. Change it only when the step actually ships.
- SAMPLE_PROFILES: illustrative profiles that show employers what a Nelavista Talent profile
  contains. They are NOT real people. Every surface that renders them labels them as
  samples, and their profile pages are noindex. Replace them with real, opted-in talent
  (StudentPrivacySettings.profile_visibility == 'public') once the network has consented
  profiles to show; see `featured_talent()`.
- CLIENT_LOGOS / STORIES: empty until an organisation or person agrees to be named. The
  sections that use them render nothing (logos) or an honest "being documented" state
  (stories) while they are empty. Never add placeholders that look real.
"""
from __future__ import annotations

# ── Figures ──────────────────────────────────────────────────────────────────────────────
# 'value' None = hidden. Live figures are filled in by the route from _landing_stats().
VERIFIED_FIGURES = [
    {'key': 'reached', 'value': '2,500+', 'label': 'Students and emerging professionals reached',
     'note': 'Across the Nelavista platform and programmes'},
    {'key': 'trained_ai', 'value': '500+', 'label': 'People trained in applied AI',
     'note': 'Through Nelavista AI training'},
    # Set these once the numbers are counted, e.g. {'value': '120', ...}. Until then they
    # stay hidden rather than showing an "X+" placeholder to the public.
    {'key': 'assessed', 'value': None, 'label': 'Talent assessed', 'note': ''},
    {'key': 'introductions', 'value': None, 'label': 'Employer introductions made', 'note': ''},
]


def build_figures(stats: dict | None) -> list[dict]:
    """Verified figures plus the live counts that already appear on the main landing page."""
    figures = [f for f in VERIFIED_FIGURES if f['value']]
    stats = stats or {}
    if stats.get('skill_count'):
        figures.append({'key': 'skills', 'value': str(stats['skill_count']),
                        'label': 'Structured skill tracks with assessments',
                        'note': 'Counted live from the Nelavista Skills catalogue'})
    if stats.get('university_count'):
        n = stats['university_count']
        figures.append({'key': 'universities', 'value': str(n),
                        'label': 'University live on Nelavista' if n == 1 else 'Universities live on Nelavista',
                        'note': 'Where our learners study'})
    return figures


# ── Categories ───────────────────────────────────────────────────────────────────────────
# Add a category by appending a dict. 'slug' is used by the directory filter and the
# request form; keep it stable once published.
CATEGORIES = [
    {'slug': 'customer-support', 'name': 'Customer Support', 'icon': 'ri-customer-service-2-line',
     'desc': 'Chat, email and phone support, ticket handling, CRM upkeep.',
     'roles': ['Support agent', 'Chat support', 'CRM administrator']},
    {'slug': 'data-operations', 'name': 'Data & Operations', 'icon': 'ri-database-2-line',
     'desc': 'Data entry and cleaning, processing, reporting, back-office operations.',
     'roles': ['Data entry', 'Operations assistant', 'Reporting analyst']},
    {'slug': 'virtual-assistance', 'name': 'Virtual Assistance', 'icon': 'ri-calendar-check-line',
     'desc': 'Inbox and calendar management, admin, scheduling, documentation.',
     'roles': ['Executive assistant', 'Admin support', 'Scheduler']},
    {'slug': 'marketing', 'name': 'Marketing', 'icon': 'ri-advertisement-line',
     'desc': 'Social media, content writing, campaign support, community management.',
     'roles': ['Social media manager', 'Content writer', 'Community manager']},
    {'slug': 'design-creative', 'name': 'Design & Creative', 'icon': 'ri-pen-nib-line',
     'desc': 'Graphic design, UI/UX, video editing, presentation design.',
     'roles': ['Graphic designer', 'UI/UX designer', 'Video editor']},
    {'slug': 'technology', 'name': 'Technology', 'icon': 'ri-code-s-slash-line',
     'desc': 'Web and software development, QA testing, data analysis.',
     'roles': ['Web developer', 'QA tester', 'Data analyst']},
    {'slug': 'finance-business', 'name': 'Finance & Business', 'icon': 'ri-line-chart-line',
     'desc': 'Bookkeeping support, financial analysis, business research.',
     'roles': ['Bookkeeping assistant', 'Financial analyst', 'Business analyst']},
    {'slug': 'research', 'name': 'Research', 'icon': 'ri-search-eye-line',
     'desc': 'Market research, data collection, literature reviews, AI data work.',
     'roles': ['Research assistant', 'Data collector', 'Annotator']},
]
CATEGORY_BY_SLUG = {c['slug']: c for c in CATEGORIES}


# ── Pipeline and verification ────────────────────────────────────────────────────────────
PIPELINE = [
    {'step': 'Learn', 'text': 'Structured skill tracks, built lesson by lesson.'},
    {'step': 'Practise', 'text': 'Practical tasks that mirror real work, not quizzes.'},
    {'step': 'Assess', 'text': 'Scored assessments with a fixed pass mark.'},
    {'step': 'Get discovered', 'text': 'An evidence-based profile, visible only with consent.'},
    {'step': 'Work', 'text': 'Introductions to organisations with a real need.'},
]

VERIFICATION_STANDARD = [
    {'key': 'identity', 'name': 'Identity', 'icon': 'ri-shield-user-line', 'status': 'in_development',
     'question': 'Is this person who they say they are?',
     'text': 'Verified email and account history today. Government ID checks before any introduction are being added to the standard.'},
    {'key': 'skills', 'name': 'Skills', 'icon': 'ri-medal-line', 'status': 'live',
     'question': 'Can they do what they claim?',
     'text': 'Scored assessments for each skill track, with a fixed pass mark. Scores are recorded, not self-reported.'},
    {'key': 'practical', 'name': 'Practical work', 'icon': 'ri-hammer-line', 'status': 'live',
     'question': 'Have they done the work, not just studied it?',
     'text': 'Practical tasks and projects reviewed against a quality bar before a skill counts as verified.'},
    {'key': 'communication', 'name': 'Communication', 'icon': 'ri-chat-check-line', 'status': 'in_development',
     'question': 'Can they work with your team?',
     'text': 'Written and spoken communication review for client-facing roles. Being added to the standard.'},
    {'key': 'profile', 'name': 'Evidence profile', 'icon': 'ri-profile-line', 'status': 'live',
     'question': 'Can you see the proof?',
     'text': 'One profile showing assessments passed, work reviewed and skills verified. Talent decide who can see it.'},
]
STATUS_LABELS = {'live': 'Live on Nelavista', 'in_development': 'Being added'}


EMPLOYER_STEPS = [
    {'n': '01', 'title': 'Tell us what you need', 'text': 'Role, skills, workload, timeline and how you want to engage. A few minutes, no account needed.'},
    {'n': '02', 'title': 'We look for suitable people', 'text': 'Our team searches the network against your brief and checks the evidence behind each candidate.'},
    {'n': '03', 'title': 'Review a short shortlist', 'text': 'A handful of relevant profiles with assessments, reviewed work and availability. Not a stack of CVs.'},
    {'n': '04', 'title': 'Engage the right people', 'text': 'Interview, then hire, contract or outsource on terms agreed with you.'},
]

USE_CASES = [
    {'title': 'Build a remote team', 'text': 'Start with two or three people and grow the team as the work proves out.', 'icon': 'ri-team-line'},
    {'title': 'Handle operational overflow', 'text': 'Extra hands for seasonal peaks, backlogs and one-off clean-ups.', 'icon': 'ri-stack-line'},
    {'title': 'Outsource a function', 'text': 'Hand over a defined function such as support, data or admin to a managed group.', 'icon': 'ri-git-branch-line'},
    {'title': 'Staff a project', 'text': 'People for a fixed scope and timeline, from research sprints to design work.', 'icon': 'ri-flag-2-line'},
    {'title': 'Scale customer support', 'text': 'Assessed support staff for chat, email and phone, across time zones.', 'icon': 'ri-customer-service-line'},
    {'title': 'Add digital skills', 'text': 'Design, data, development and marketing skills your team is missing.', 'icon': 'ri-cpu-line'},
]

EMPLOYER_SIGNALS = [
    {'name': 'Verification status', 'text': 'Which checks a person has passed, and which are still pending.'},
    {'name': 'Assessment results', 'text': 'Scores against a fixed pass mark, per skill.'},
    {'name': 'Reviewed work', 'text': 'Projects and practical tasks, with the reviewer’s verdict.'},
    {'name': 'Availability & time zone', 'text': 'Hours per week, start date, location and working-hours overlap.'},
    {'name': 'Skill match', 'text': 'How their verified skills line up with your brief.'},
    {'name': 'A person to talk to', 'text': 'Someone on our team handles your request, start to finish.'},
]

TALENT_JOURNEY = [
    {'title': 'Create your profile', 'text': 'Your background, the work you want and when you are available.'},
    {'title': 'Build skills', 'text': 'Structured tracks in support, data, design, development and more.'},
    {'title': 'Pass assessments', 'text': 'Scored tests with a fixed pass mark. Your result goes on your profile.'},
    {'title': 'Add real projects', 'text': 'Practical work reviewed against a quality bar.'},
    {'title': 'Become discoverable', 'text': 'Choose to make your profile visible to organisations.'},
    {'title': 'Receive opportunities', 'text': 'When your evidence matches a brief, we introduce you.'},
]

# Employer / partner logos. Add only with written permission to name the organisation:
# {'name': 'Company', 'logo': 'images/talent/logos/company.svg', 'url': 'https://...'}
CLIENT_LOGOS: list[dict] = []

# Published stories. Add only with the consent of everyone named, and only real outcomes.
# kind 'talent': before / skills / assessment / project / outcome
# kind 'employer': need / talent / work / result
STORIES: list[dict] = []

# Optional editorial photograph for the employer section. Use only licensed photography of
# real professionals (not AI-generated), e.g. {'src': 'images/talent/team.webp', 'alt': '...',
# 'credit': 'Photographer / Source'}. None hides the image and the layout adapts.
EDITORIAL_PHOTO: dict | None = None


# ── Request form options ─────────────────────────────────────────────────────────────────
ENGAGEMENT_TYPES = [
    ('full_time', 'Full-time hire'),
    ('part_time', 'Part-time'),
    ('contract', 'Fixed-term contract'),
    ('project', 'Project-based'),
    ('outsourced', 'Outsourced team or function'),
    ('unsure', 'Not sure yet'),
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


# ── Sample profiles ──────────────────────────────────────────────────────────────────────
# Illustrative only. Data shape matches what a real profile will carry, so the templates
# need no change when real talent replaces these.
# checks: identity | skills | practical | communication -> 'verified' | 'pending' | 'not_started'
SAMPLE_PROFILES = [
    {
        'slug': 'sample-adebayo-o', 'name': 'Adebayo O.', 'initials': 'AO', 'tone': 'blue',
        'role': 'Customer Support Specialist', 'category': 'customer-support',
        'location': 'Lagos, Nigeria', 'timezone': 'WAT (UTC+1)',
        'availability': 'available', 'availability_text': 'Available now', 'hours': '40 hrs / week',
        'engagements': ['Full-time', 'Contract'], 'level': 'Mid-level',
        'skills': ['Customer Support', 'Zendesk', 'Written Communication', 'Data Entry'],
        'languages': [('English', 'Fluent'), ('Yoruba', 'Native')],
        'summary': 'Handles high-volume chat and email support with a steady tone. Strongest on ticket triage, clear written replies and keeping CRM records clean.',
        'checks': {'identity': 'verified', 'skills': 'verified', 'practical': 'verified', 'communication': 'pending'},
        'assessments': [
            {'name': 'Customer Support Fundamentals', 'score': 86, 'pass': 70},
            {'name': 'Written Communication', 'score': 81, 'pass': 70},
        ],
        'projects': [
            {'title': 'Support macro library', 'text': 'Rewrote 30 reply templates for a simulated e-commerce helpdesk; reviewed for tone and accuracy.', 'status': 'Reviewed'},
            {'title': 'Ticket triage exercise', 'text': 'Categorised and prioritised 120 sample tickets against an SLA policy.', 'status': 'Reviewed'},
        ],
        'experience': [
            {'title': 'Support volunteer', 'org': 'University student union', 'period': '2024 – 2025'},
        ],
        'portfolio': True, 'completeness': 90,
    },
    {
        'slug': 'sample-amara-n', 'name': 'Amara N.', 'initials': 'AN', 'tone': 'green',
        'role': 'Data Operations Assistant', 'category': 'data-operations',
        'location': 'Enugu, Nigeria', 'timezone': 'WAT (UTC+1)',
        'availability': 'available', 'availability_text': 'Available in 2 weeks', 'hours': '30 hrs / week',
        'engagements': ['Part-time', 'Project-based'], 'level': 'Entry-level',
        'skills': ['Data Entry', 'Excel', 'Google Sheets', 'Data Cleaning'],
        'languages': [('English', 'Fluent'), ('Igbo', 'Native')],
        'summary': 'Accurate, methodical data work. Comfortable cleaning messy spreadsheets, building simple lookups and documenting each step.',
        'checks': {'identity': 'verified', 'skills': 'verified', 'practical': 'pending', 'communication': 'not_started'},
        'assessments': [{'name': 'Spreadsheet Skills', 'score': 92, 'pass': 70}],
        'projects': [
            {'title': 'Inventory clean-up', 'text': 'De-duplicated and standardised a 4,000-row product sheet.', 'status': 'In review'},
        ],
        'experience': [],
        'portfolio': True, 'completeness': 75,
    },
    {
        'slug': 'sample-kwame-a', 'name': 'Kwame A.', 'initials': 'KA', 'tone': 'amber',
        'role': 'Junior Web Developer', 'category': 'technology',
        'location': 'Accra, Ghana', 'timezone': 'GMT (UTC+0)',
        'availability': 'limited', 'availability_text': 'Part-time only', 'hours': '20 hrs / week',
        'engagements': ['Contract', 'Project-based'], 'level': 'Entry-level',
        'skills': ['HTML & CSS', 'JavaScript', 'React', 'Git'],
        'languages': [('English', 'Fluent'), ('Twi', 'Native')],
        'summary': 'Builds clean, responsive front ends. Most comfortable turning a design into working pages and fixing layout bugs across devices.',
        'checks': {'identity': 'verified', 'skills': 'verified', 'practical': 'verified', 'communication': 'verified'},
        'assessments': [
            {'name': 'Front-end Foundations', 'score': 78, 'pass': 70},
            {'name': 'JavaScript Essentials', 'score': 74, 'pass': 70},
        ],
        'projects': [
            {'title': 'Booking page rebuild', 'text': 'Rebuilt a salon booking page from a Figma file; tested on three screen sizes.', 'status': 'Reviewed'},
        ],
        'experience': [
            {'title': 'Freelance web projects', 'org': 'Independent', 'period': '2025 – present'},
        ],
        'portfolio': True, 'completeness': 95,
    },
    {
        'slug': 'sample-wanjiru-k', 'name': 'Wanjiru K.', 'initials': 'WK', 'tone': 'violet',
        'role': 'Virtual Assistant', 'category': 'virtual-assistance',
        'location': 'Nairobi, Kenya', 'timezone': 'EAT (UTC+3)',
        'availability': 'available', 'availability_text': 'Available now', 'hours': '40 hrs / week',
        'engagements': ['Full-time', 'Part-time'], 'level': 'Mid-level',
        'skills': ['Calendar Management', 'Google Workspace', 'Notion', 'Inbox Management'],
        'languages': [('English', 'Fluent'), ('Swahili', 'Native')],
        'summary': 'Keeps busy calendars and inboxes under control. Organised, quick to respond and careful with confidential information.',
        'checks': {'identity': 'verified', 'skills': 'verified', 'practical': 'verified', 'communication': 'pending'},
        'assessments': [{'name': 'Admin & Productivity Tools', 'score': 88, 'pass': 70}],
        'projects': [
            {'title': 'Executive week plan', 'text': 'Planned a week of meetings across three time zones from a messy request thread.', 'status': 'Reviewed'},
        ],
        'experience': [
            {'title': 'Office administrator', 'org': 'Small accounting practice', 'period': '2023 – 2025'},
        ],
        'portfolio': False, 'completeness': 85,
    },
    {
        'slug': 'sample-tobi-f', 'name': 'Tobi F.', 'initials': 'TF', 'tone': 'rose',
        'role': 'Graphic & UI Designer', 'category': 'design-creative',
        'location': 'Ibadan, Nigeria', 'timezone': 'WAT (UTC+1)',
        'availability': 'available', 'availability_text': 'Available now', 'hours': '25 hrs / week',
        'engagements': ['Project-based', 'Contract'], 'level': 'Mid-level',
        'skills': ['Figma', 'Brand Design', 'UI Design', 'Presentation Design'],
        'languages': [('English', 'Fluent')],
        'summary': 'Designs clear, restrained interfaces and brand material. Works from a brief, shows options early and documents decisions.',
        'checks': {'identity': 'pending', 'skills': 'verified', 'practical': 'verified', 'communication': 'not_started'},
        'assessments': [{'name': 'UI Design Principles', 'score': 83, 'pass': 70}],
        'projects': [
            {'title': 'Clinic appointment app', 'text': 'Designed five core screens and a small component set in Figma.', 'status': 'Reviewed'},
            {'title': 'Pitch deck redesign', 'text': 'Restructured and redesigned a 14-slide investor deck.', 'status': 'Reviewed'},
        ],
        'experience': [],
        'portfolio': True, 'completeness': 80,
    },
    {
        'slug': 'sample-fatima-b', 'name': 'Fatima B.', 'initials': 'FB', 'tone': 'teal',
        'role': 'Research Assistant', 'category': 'research',
        'location': 'Abuja, Nigeria', 'timezone': 'WAT (UTC+1)',
        'availability': 'limited', 'availability_text': 'From next month', 'hours': '20 hrs / week',
        'engagements': ['Project-based', 'Part-time'], 'level': 'Entry-level',
        'skills': ['Desk Research', 'Survey Design', 'Data Collection', 'Report Writing'],
        'languages': [('English', 'Fluent'), ('Hausa', 'Native')],
        'summary': 'Thorough desk researcher who writes concise summaries with sources. Has run small surveys and cleaned the results.',
        'checks': {'identity': 'verified', 'skills': 'pending', 'practical': 'verified', 'communication': 'verified'},
        'assessments': [],
        'projects': [
            {'title': 'Market scan: solar retail', 'text': 'Compiled a sourced overview of 20 solar retailers in two states.', 'status': 'Reviewed'},
        ],
        'experience': [
            {'title': 'Field enumerator', 'org': 'Household survey project', 'period': '2024'},
        ],
        'portfolio': True, 'completeness': 70,
    },
]
SAMPLE_BY_SLUG = {p['slug']: p for p in SAMPLE_PROFILES}

CHECK_LABELS = {
    'identity': 'Identity', 'skills': 'Skills assessed',
    'practical': 'Practical work reviewed', 'communication': 'Communication reviewed',
}
CHECK_STATE_LABELS = {'verified': 'Verified', 'pending': 'In progress', 'not_started': 'Not yet'}


def verified_count(profile: dict) -> int:
    return sum(1 for v in profile['checks'].values() if v == 'verified')


def featured_talent() -> list[dict]:
    """Profiles for the public directory. Today: the labelled samples. When real talent
    have opted in to public visibility, build their cards here from
    services/talent_search_service and set 'is_sample': False on them."""
    return [dict(p, is_sample=True) for p in SAMPLE_PROFILES]


def get_profile(slug: str) -> dict | None:
    p = SAMPLE_BY_SLUG.get(slug)
    return dict(p, is_sample=True) if p else None
