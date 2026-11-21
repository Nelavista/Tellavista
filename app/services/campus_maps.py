"""Campus Map: the multi-university map system behind /campus-map.

Three layers, kept separate on purpose:

1. Content lives in the database (models.py): University -> Campus -> CampusLocation.
   Admins add and edit campuses and places at /admin/campus-map. Adding a university's
   map is a data task, not a code change.

2. Presentation defaults live here: the category taxonomy (labels, icons, colours) and
   an optional per-university MAP_PROFILES entry (display location, default zoom, campus
   boundary). A university with no profile still works. The map centres on its campus
   coordinates and fits its places.

3. Campus plans: a campus with no verified coordinates can be mapped from its official
   plan instead. data/campus_maps/<university-slug>.json names the plan image (straightened)
   and lists places in the plan's own pixel frame (x right, y down). The map page then
   draws the plan as the base layer instead of satellite tiles (campus-map.js,
   map.kind == 'plan'), and GPS directions are switched off because the plan has no
   coordinates. For a campus listed in such a file, the file is the source of its places.
   University of Abuja is the first.

To add a university's map:
  - make sure its University row exists (seed_academia.py or /admin/academia),
  - either give its Campus row real latitude/longitude and add places at
    /admin/campus-map, or add a campus-plan file under data/campus_maps/,
  - optionally add a MAP_PROFILES entry below for its town, zoom and boundary.

Nothing here invents data. Boundaries stay None until a verified outline exists, and a
place's description is only shown when one was actually written for it.
"""
import json
import os
import re
from functools import lru_cache

from sqlalchemy import func

from app.extensions import db
from app.models import University, Campus, CampusLocation


# ── Categories ──────────────────────────────────────────────────────────────────────
# Order is the order chips appear in on the map. `color` is the marker fill; every one
# carries white icons at >= 4.5:1.
CATEGORIES = [
    {'key': 'faculty', 'label': 'Faculties', 'singular': 'Faculty', 'icon': 'ri-building-4-line', 'color': '#2f5bd3'},
    {'key': 'department', 'label': 'Departments & centres', 'singular': 'Department or centre', 'icon': 'ri-community-line', 'color': '#6342c9'},
    {'key': 'lecture_hall', 'label': 'Lecture halls & venues', 'singular': 'Lecture hall or venue', 'icon': 'ri-presentation-line', 'color': '#0f7f86'},
    {'key': 'library', 'label': 'Libraries', 'singular': 'Library', 'icon': 'ri-book-2-line', 'color': '#9a4b12'},
    {'key': 'laboratory', 'label': 'Laboratories', 'singular': 'Laboratory', 'icon': 'ri-flask-line', 'color': '#7a3f9e'},
    {'key': 'ict', 'label': 'ICT & CBT centres', 'singular': 'ICT or CBT centre', 'icon': 'ri-computer-line', 'color': '#126b6b'},
    {'key': 'admin', 'label': 'Administration', 'singular': 'Administrative building', 'icon': 'ri-government-line', 'color': '#8a5a0b'},
    {'key': 'student_centre', 'label': 'Student spaces', 'singular': 'Student space', 'icon': 'ri-team-line', 'color': '#b0306a'},
    {'key': 'hostel', 'label': 'Hostels', 'singular': 'Hostel', 'icon': 'ri-hotel-bed-line', 'color': '#4b5a8a'},
    {'key': 'health', 'label': 'Health', 'singular': 'Health centre', 'icon': 'ri-first-aid-kit-line', 'color': '#c0322b'},
    {'key': 'food', 'label': 'Food', 'singular': 'Cafeteria or eatery', 'icon': 'ri-restaurant-line', 'color': '#b4470f'},
    {'key': 'shopping', 'label': 'Shops & markets', 'singular': 'Shop or market', 'icon': 'ri-store-2-line', 'color': '#7c4a1e'},
    {'key': 'bank', 'label': 'Banks & ATMs', 'singular': 'Bank or ATM', 'icon': 'ri-bank-line', 'color': '#0c7a4b'},
    {'key': 'religious', 'label': 'Worship', 'singular': 'Place of worship', 'icon': 'ri-hand-heart-line', 'color': '#3c4a5e'},
    {'key': 'sports', 'label': 'Sports', 'singular': 'Sports facility', 'icon': 'ri-football-line', 'color': '#2e7d32'},
    {'key': 'parking', 'label': 'Parking', 'singular': 'Car park', 'icon': 'ri-parking-box-line', 'color': '#3b5b8c'},
    {'key': 'gate', 'label': 'Gates & entrances', 'singular': 'Gate or entrance', 'icon': 'ri-door-open-line', 'color': '#5b616e'},
    {'key': 'landmark', 'label': 'Other places', 'singular': 'Campus place', 'icon': 'ri-map-pin-2-line', 'color': '#4a5160'},
]
CATEGORY_INDEX = {c['key']: c for c in CATEGORIES}
DEFAULT_CATEGORY = 'landmark'

# Values written by the original LASU seed (seed_campus_map.py's _category_for) and other
# early spellings. Mapped rather than migrated so existing rows display correctly with
# no data change.
LEGACY_CATEGORY_ALIASES = {
    'lecture': 'lecture_hall', 'healthcare': 'health', 'medical': 'health',
    'commercial': 'shopping', 'market': 'shopping', 'general': DEFAULT_CATEGORY,
    'utility': 'admin', 'administrative': 'admin', 'administration': 'admin',
    'cafeteria': 'food', 'restaurant': 'food', 'lab': 'laboratory', 'labs': 'laboratory',
    'student_center': 'student_centre', 'gates': 'gate', 'entrance': 'gate', 'atm': 'bank',
    'sport': 'sports', 'worship': 'religious', 'hostels': 'hostel', 'other': DEFAULT_CATEGORY,
}

# Stored categories that were assigned by a loose name heuristic and are allowed to be
# refined by a clearer one. Any other explicit category an admin picks always wins.
_REFINABLE = {None, '', 'general', 'department', 'lecture', 'commercial', 'utility',
              'landmark', 'other'}

# Checked in order; first match wins. Word-boundary patterns so "lab" does not match
# "Collaboration" and "school of" beats "library" for "School of Library ... Science".
_NAME_RULES = [
    ('gate', r'\bgate\b|\bentrance\b'),
    ('parking', r'car ?park|\bparking\b'),
    ('hostel', r'\bhostel|hall of residence|\blodge\b'),
    ('religious', r'mosque|chapel|church|\bcathedral\b'),
    ('bank', r'\bbank\b|\batm\b'),
    ('food', r'cafeteria|canteen|restaurant|eatery|\bbuka\b|food court'),
    ('health', r'health|medical|\bhospital\b|\bpharmacy\b'),
    ('sports', r'sport|\bcourt\b|\bpitch\b|stadium|\bgym\b'),
    ('ict', r'\bict\b|\bcbt\b|computer cent|e-library'),
    ('admin', r'senate|registry|bursary|directorate|post ?graduate school|works and physical|liaison|liason|\bsiwes\b|vice.?chancellor'),
    ('faculty', r'^faculty\b|\bfaculty of\b|\bcollege of\b'),
    ('department', r'^department\b|\bdepartment of\b|\bschool of\b|\bcent(re|er) (for|of)\b|institut'),
    ('library', r'librar'),
    ('laboratory', r'\blab\b|laborator'),
    ('lecture_hall', r'lecture|theatre|auditorium|conference|\bhall\b'),
    ('shopping', r'arcade|market|\bshop|\bmall\b'),
    ('student_centre', r'\bhub\b|garden|student union|\bsug\b'),
]
_NAME_RULES = [(key, re.compile(pattern, re.I)) for key, pattern in _NAME_RULES]


def category_from_name(name):
    for key, pattern in _NAME_RULES:
        if pattern.search(name or ''):
            return key
    return None


def resolve_category(stored, name):
    """The category a place is shown under. An explicit, specific category set by an
    admin is respected. Blank or loosely-guessed legacy values get refined from the
    place's name, then fall back to their alias, then to 'Other places'."""
    raw = (stored or '').strip().lower()
    if raw not in _REFINABLE:
        key = LEGACY_CATEGORY_ALIASES.get(raw, raw)
        if key in CATEGORY_INDEX:
            return key
    from_name = category_from_name(name)
    if from_name:
        return from_name
    key = LEGACY_CATEGORY_ALIASES.get(raw, raw)
    return key if key in CATEGORY_INDEX else DEFAULT_CATEGORY


# ── Per-university presentation profiles (optional) ─────────────────────────────────
# Keyed by University.name, the stable identifier used across the codebase.
#   location  shown under the university's name when University.location is blank
#   zoom      opening zoom when a campus has coordinates but no places yet
#   campuses  per-campus-name overrides: {'boundary': GeoJSON Polygon coordinates | None}
# Towns are the universities' official locations. No boundary is filled in until a
# verified campus outline exists.
MAP_PROFILES = {
    'Lagos State University': {'location': 'Ojo, Lagos', 'zoom': 16},
    'University of Lagos': {'location': 'Akoka, Lagos'},
    'University of Ibadan': {'location': 'Ibadan, Oyo'},
    'Federal University Dutsin-Ma': {'location': 'Dutsin-Ma, Katsina'},
    'University of Abuja': {'location': 'Gwagwalada, FCT Abuja'},
    'University of Ilorin': {'location': 'Ilorin, Kwara'},
    'Kwara State University': {'location': 'Malete, Kwara'},
    'University of Port Harcourt': {'location': 'Choba, Rivers'},
    'Federal University of Technology, Akure': {'location': 'Akure, Ondo'},
    'Federal University of Technology, Minna': {'location': 'Minna, Niger'},
    'University of Nigeria, Nsukka': {'location': 'Nsukka, Enugu'},
    'University of Benin': {'location': 'Benin City, Edo'},
    'Modibbo Adama University': {'location': 'Yola, Adamawa'},
    'Obafemi Awolowo University': {'location': 'Ile-Ife, Osun'},
}
DEFAULT_ZOOM = 16


def _profile(university):
    return MAP_PROFILES.get(university.name, {})


def display_location(university):
    return university.location or _profile(university).get('location')


def monogram(university):
    if university.short_name:
        # "FUT Minna" -> "FUT"; long single words (UNIABUJA) shrink in CSS, not truncate.
        return university.short_name.split()[0][:8]
    words = [w for w in re.split(r'[\s,]+', university.name) if w and w.lower() not in {'of', 'the', 'and'}]
    return ''.join(w[0] for w in words[:4]).upper()


DATASET_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'campus_maps'))


@lru_cache(maxsize=64)
def _read_dataset(path, mtime):
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def load_dataset(university):
    """This university's campus-plan file (data/campus_maps/<slug>.json), or None."""
    if not university.slug:
        return None
    path = os.path.join(DATASET_DIR, university.slug + '.json')
    if not os.path.isfile(path):
        return None
    data = _read_dataset(path, os.path.getmtime(path))
    if data.get('university') and data['university'] != university.name:
        return None   # the file names a different school than the one holding this slug
    return data


def _dataset_campus(dataset, campus_name):
    if not dataset:
        return None
    return next((c for c in dataset.get('campuses') or [] if c.get('name') == campus_name), None)


def _db_counts_by_campus_name(university):
    rows = (
        db.session.query(Campus.name, func.count(CampusLocation.id))
        .join(CampusLocation, CampusLocation.campus_id == Campus.id)
        .filter(Campus.university_id == university.id, CampusLocation.is_active.is_(True))
        .group_by(Campus.name).all()
    )
    return dict(rows)


def _image_url(path):
    if not path:
        return None
    if path.startswith(('http://', 'https://', '/')):
        return path
    return '/' + path


def _location_counts():
    """{university_id: active place count}, one grouped query for the whole picker."""
    rows = (
        db.session.query(Campus.university_id, func.count(CampusLocation.id))
        .join(CampusLocation, CampusLocation.campus_id == Campus.id)
        .filter(CampusLocation.is_active.is_(True))
        .group_by(Campus.university_id)
        .all()
    )
    return {uid: n for uid, n in rows}


def university_card(university, place_count=0, kind='geo'):
    return {
        'map_kind': kind,
        'id': university.id,
        'slug': university.slug,
        'name': university.name,
        'short_name': university.short_name,
        'monogram': monogram(university),
        'location': display_location(university),
        'logo_url': university.logo_url,
        'place_count': place_count,
        'has_map': place_count > 0,
    }


def list_universities():
    """Every active university for the picker: mapped ones first, then A-Z."""
    counts = _location_counts()
    unis = University.query.filter(University.active.is_(True)).order_by(University.name).all()
    cards = []
    for u in unis:
        dataset = load_dataset(u)
        n = counts.get(u.id, 0)
        if dataset:
            # A plan campus's places come from its file, not from DB rows for that campus.
            plan_names = {c.get('name') for c in dataset.get('campuses') or []}
            n = sum(len(c.get('places') or []) for c in dataset.get('campuses') or [])
            n += sum(cnt for name, cnt in _db_counts_by_campus_name(u).items() if name not in plan_names)
        cards.append(university_card(u, n, kind=('plan' if dataset else 'geo')))
    cards.sort(key=lambda c: (not c['has_map'], c['name'].lower()))
    return cards


def find_university(key):
    """Resolve a URL key: the slug first, then the short name (so /campus-map/lasu works)."""
    key = (key or '').strip().lower()
    if not key:
        return None
    uni = University.query.filter(University.slug == key, University.active.is_(True)).first()
    if uni:
        return uni
    return University.query.filter(
        func.lower(University.short_name) == key, University.active.is_(True)
    ).first()


def _campuses(university):
    return university.campuses.order_by(Campus.is_main.desc(), Campus.name).all()


def place_dict(loc, campus):
    key = resolve_category(loc.category, loc.name)
    return {
        'id': str(loc.id),
        'name': loc.name,
        'category': key,
        'description': (loc.description or '').strip() or None,
        'lat': loc.latitude,
        'lng': loc.longitude,
        'image': _image_url(loc.image_path),
        'campus': campus.name,
    }


def plan_place_dict(raw, campus_name, height):
    """A place from a campus-plan file. Plan pixels (x right, y down) become Leaflet
    CRS.Simple coordinates, where lat grows upward, so y is flipped."""
    fp = raw.get('footprint')
    return {
        'id': str(raw['id']),
        'name': raw['name'],
        'category': resolve_category(raw.get('category'), raw.get('name')),
        'description': (raw.get('description') or '').strip() or None,
        'lat': height - raw['y'],
        'lng': raw['x'],
        'footprint': ([[height - fp[1][1], fp[0][0]], [height - fp[0][1], fp[1][0]]] if fp else None),
        'aliases': raw.get('aliases') or [],
        'verify': bool(raw.get('verify')),
        'image': _image_url(raw.get('image')),
        'campus': campus_name,
    }


def build_map_payload(university, campus_id=None):
    """Everything the map page needs for one university and one of its campuses."""
    dataset = load_dataset(university)
    campuses = _campuses(university)
    campus_list = [{'id': c.id, 'name': c.name, 'is_main': c.is_main} for c in campuses]
    if dataset:
        # A plan campus with no DB row still appears (id None: it is the only way to open it).
        known = {c['name'] for c in campus_list}
        for dc in dataset.get('campuses') or []:
            if dc.get('name') not in known:
                campus_list.append({'id': None, 'name': dc['name'], 'is_main': not campus_list})
    campus = None
    if campus_id:
        campus = next((c for c in campus_list if c['id'] == campus_id), None)
    if campus is None and campus_list:
        campus = campus_list[0]

    plan_campus = _dataset_campus(dataset, campus['name']) if campus else None
    db_campus = next((c for c in campuses if campus and c.id == campus['id']), None)

    places = []
    plan = None
    if plan_campus:
        frame = (dataset.get('source') or {}).get('frame') or {}
        width, height = frame['width'], frame['height']
        places = sorted(
            (plan_place_dict(p, campus['name'], height) for p in plan_campus.get('places') or []),
            key=lambda p: p['name'].lower(),
        )
        plan = {
            'image': _image_url(plan_campus['plan']['image']),
            'credit': plan_campus['plan'].get('credit'),
            'bounds': [[0, 0], [height, width]],
        }
    elif db_campus:
        rows = db_campus.locations.filter_by(is_active=True).order_by(CampusLocation.name).all()
        places = [place_dict(loc, db_campus) for loc in rows]

    counts = {}
    for p in places:
        counts[p['category']] = counts.get(p['category'], 0) + 1
    categories = [dict(c, count=counts[c['key']]) for c in CATEGORIES if c['key'] in counts]

    profile = _profile(university)
    campus_profile = (profile.get('campuses') or {}).get(campus['name'], {}) if campus else {}
    bounds = None
    if places:
        lats = [p['lat'] for p in places]
        lngs = [p['lng'] for p in places]
        bounds = [[min(lats), min(lngs)], [max(lats), max(lngs)]]
    center = None
    if plan:
        bounds = plan['bounds']   # open on the whole plan, not just the pins
        center = [bounds[1][0] / 2, bounds[1][1] / 2]
    elif db_campus and db_campus.latitude is not None and db_campus.longitude is not None:
        center = [db_campus.latitude, db_campus.longitude]
    elif bounds:
        center = [(bounds[0][0] + bounds[1][0]) / 2, (bounds[0][1] + bounds[1][1]) / 2]

    campus_counts = dict(
        db.session.query(CampusLocation.campus_id, func.count(CampusLocation.id))
        .filter(CampusLocation.campus_id.in_([c.id for c in campuses] or [0]),
                CampusLocation.is_active.is_(True))
        .group_by(CampusLocation.campus_id).all()
    )
    for c in campus_list:
        dc = _dataset_campus(dataset, c['name'])
        c['place_count'] = len(dc.get('places') or []) if dc else campus_counts.get(c['id'], 0)
        c['kind'] = 'plan' if dc else 'geo'

    return {
        'university': university_card(
            university, sum(c['place_count'] for c in campus_list), kind=('plan' if dataset else 'geo')),
        'campuses': campus_list,
        'campus': ({'id': campus['id'], 'name': campus['name']} if campus else None),
        'map': {
            'kind': 'plan' if plan else 'geo',
            'plan': plan,
            'center': center,
            'zoom': profile.get('zoom', DEFAULT_ZOOM),
            'bounds': bounds,
            'boundary': campus_profile.get('boundary'),
        },
        'categories': categories,
        'places': places,
        'has_data': bool(places),
    }
