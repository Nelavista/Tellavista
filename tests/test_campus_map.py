"""Campus Map space: Map -> choose a university -> that university's map."""
import json
import re

import pytest

from app.extensions import db
from app.models import University, Campus, CampusLocation, User
from app.services import campus_maps


@pytest.fixture
def campus_data(app):
    """LASU with a mapped main campus, UNILAG with an empty campus, one inactive school."""
    with app.app_context():
        lasu = University(name='Lagos State University', short_name='LASU')
        unilag = University(name='University of Lagos', short_name='UNILAG')
        hidden = University(name='Retired University', short_name='RU', active=False)
        db.session.add_all([lasu, unilag, hidden])
        db.session.flush()
        main = Campus(university_id=lasu.id, name='Main Campus', latitude=6.47, longitude=3.2, is_main=True)
        db.session.add_all([main, Campus(university_id=unilag.id, name='Main Campus', is_main=True)])
        db.session.flush()
        db.session.add_all([
            CampusLocation(campus_id=main.id, name='Faculty of Sciences', category='faculty', latitude=6.4678, longitude=3.2008),
            CampusLocation(campus_id=main.id, name='School of Library, Archival and information Science', category='department', latitude=6.4644, longitude=3.2002),
            CampusLocation(campus_id=main.id, name='Physics Lab', category='department', latitude=6.4651, longitude=3.2011, image_path='images/physicslab.jpeg'),
            CampusLocation(campus_id=main.id, name='Senate Building', category='general', latitude=6.4712, longitude=3.1999,
                           description='Registry and the Vice-Chancellor\'s office.'),
            CampusLocation(campus_id=main.id, name='Old Kiosk', category='general', latitude=6.466, longitude=3.201, is_active=False),
        ])
        db.session.commit()
        return {'lasu_slug': lasu.slug, 'unilag_slug': unilag.slug, 'lasu_id': lasu.id, 'hidden_slug': hidden.slug}


def _payload(html):
    m = re.search(r'<script id="cm-data" type="application/json">(.*?)</script>', html, re.S)
    assert m, 'map page must embed its data'
    return json.loads(m.group(1))


def test_picker_lists_universities_mapped_first(client, login_as, make_user, campus_data):
    login_as(client, make_user('cm_pick'))
    res = client.get('/campus-map')
    assert res.status_code == 200
    body = res.get_data(as_text=True)
    assert 'Choose your university' in body
    assert 'Switch space' in body
    assert body.index('Lagos State University') < body.index('University of Lagos')
    assert '4 places mapped' in body            # inactive place not counted
    assert 'Map coming soon' in body             # UNILAG has no places yet
    assert 'Ojo, Lagos' in body and 'Akoka, Lagos' in body
    assert 'Retired University' not in body
    assert f'/campus-map/{campus_data["lasu_slug"]}' in body


def test_picker_puts_the_students_own_university_first(app, client, login_as, make_user, campus_data):
    ref = make_user('cm_own')
    with app.app_context():
        u = db.session.get(User, ref.id)
        u.university_id = campus_data['lasu_id']
        db.session.commit()
    login_as(client, ref)
    body = client.get('/campus-map').get_data(as_text=True)
    assert 'Your university' in body
    assert body.index('Your university') < body.index('All universities')


def test_short_name_redirects_to_slug_and_keeps_query(client, login_as, make_user, campus_data):
    login_as(client, make_user('cm_short'))
    res = client.get('/campus-map/LASU?place=1')
    assert res.status_code == 302
    assert res.headers['Location'].endswith(f'/campus-map/{campus_data["lasu_slug"]}?place=1')


def test_lasu_map_page_embeds_places_and_categories(client, login_as, make_user, campus_data):
    login_as(client, make_user('cm_map'))
    res = client.get(f'/campus-map/{campus_data["lasu_slug"]}')
    assert res.status_code == 200
    body = res.get_data(as_text=True)
    assert 'Change university' in body and 'href="/campus-map"' in body
    assert 'Lagos State University' in body and 'Campus Map' in body
    assert 'leaflet@1.9.4' in body and 'js/campus-map.js' in body
    data = _payload(body)
    assert data['has_data'] is True
    names = {p['name']: p for p in data['places']}
    assert 'Old Kiosk' not in names
    # Legacy loose categories are refined from the place's name.
    assert names['School of Library, Archival and information Science']['category'] == 'department'
    assert names['Physics Lab']['category'] == 'laboratory'
    assert names['Senate Building']['category'] == 'admin'
    assert names['Physics Lab']['image'] == '/images/physicslab.jpeg'
    assert names['Senate Building']['description'].startswith('Registry')
    assert {c['key'] for c in data['categories']} == {'faculty', 'department', 'laboratory', 'admin'}
    assert data['map']['bounds'][0][0] <= 6.4644 and data['map']['center'] == [6.47, 3.2]


def test_api_matches_page_payload(client, login_as, make_user, campus_data):
    login_as(client, make_user('cm_api'))
    res = client.get(f'/api/campus-map/{campus_data["lasu_slug"]}')
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert data['university']['short_name'] == 'LASU'
    assert len(data['places']) == 4


def test_unmapped_university_shows_empty_state(client, login_as, make_user, campus_data):
    login_as(client, make_user('cm_empty'))
    body = client.get(f'/campus-map/{campus_data["unilag_slug"]}').get_data(as_text=True)
    assert "isn't mapped yet" in body
    assert 'Choose another university' in body
    assert _payload(body)['has_data'] is False


def test_unknown_and_inactive_universities_404(client, login_as, make_user, campus_data):
    login_as(client, make_user('cm_404'))
    assert client.get('/campus-map/no-such-school').status_code == 404
    assert client.get(f'/campus-map/{campus_data["hidden_slug"]}').status_code == 404


def test_map_requires_login(client, campus_data):
    assert client.get('/campus-map').status_code == 302
    assert client.get(f'/campus-map/{campus_data["lasu_slug"]}').status_code == 302


def test_legacy_own_university_api_still_works(app, client, login_as, make_user, campus_data):
    ref = make_user('cm_legacy')
    with app.app_context():
        u = db.session.get(User, ref.id)
        u.university_id = campus_data['lasu_id']
        db.session.commit()
    login_as(client, ref)
    data = client.get('/api/campus-map').get_json()
    assert data['has_data'] is True
    assert data['university']['short_name'] == 'LASU'
    assert len(data['locations']) == 4


@pytest.mark.parametrize('stored,name,expected', [
    ('department', 'School of Library, Archival and information Science', 'department'),
    ('department', 'Lasu Centre Library', 'library'),
    ('department', 'Sciences Laboratory', 'laboratory'),
    ('general', 'LASU Central Mosque', 'religious'),
    ('commercial', 'Arcade (Student Commercial Hub)', 'shopping'),
    ('lecture', 'Main Auditorium', 'lecture_hall'),
    ('healthcare', 'Primary Health Center', 'health'),
    ('general', 'Law Clinic', 'landmark'),         # a law clinic is not a health centre
    ('general', 'Collaboration Space', 'landmark'), # "lab" must not match inside a word
    ('hostel', 'Senate Building', 'hostel'),       # an explicit admin choice always wins
    (None, 'Main Gate', 'gate'),
    ('nonsense', 'Somewhere', 'landmark'),
])
def test_resolve_category(stored, name, expected):
    assert campus_maps.resolve_category(stored, name) == expected


def test_every_category_has_display_fields():
    for c in campus_maps.CATEGORIES:
        assert c['label'] and c['singular'] and c['icon'].startswith('ri-')
        assert re.fullmatch(r'#[0-9a-f]{6}', c['color'])


# ── Dataset-file universities (University of Abuja) ───────────────────────────────
import os  # noqa: E402

ABUJA_FILE = os.path.join(campus_maps.DATASET_DIR, 'university-of-abuja.json')
# University of Abuja's campus outline in OpenStreetMap (way 1133000152), padded a little.
ABUJA_BBOX = (8.970, 7.166, 8.987, 7.188)


@pytest.fixture
def abuja(app):
    with app.app_context():
        uni = University(name='University of Abuja', short_name='UNIABUJA')
        db.session.add(uni)
        db.session.flush()
        db.session.add(Campus(university_id=uni.id, name='Main Campus', is_main=True))
        db.session.commit()
        return uni.slug


def _abuja_places():
    with open(ABUJA_FILE, encoding='utf-8') as fh:
        return json.load(fh)['campuses'][0]['places']


def test_abuja_dataset_has_real_coordinates_on_campus():
    places = _abuja_places()
    ids = [p['id'] for p in places]
    assert len(ids) == len(set(ids))
    s, w, n, e = ABUJA_BBOX
    for p in places:
        assert s <= p['lat'] <= n and w <= p['lng'] <= e, p['id']
        assert campus_maps.resolve_category(p['category'], p['name']) == p['category'], p['id']
        for lat, lng in p.get('outline') or []:
            assert s <= lat <= n and w <= lng <= e, p['id']
    names = {p['name'] for p in places}
    # Faculties that are not on the reference plan must not be invented.
    for missing in ('Faculty of Medicine', 'Faculty of Pharmaceutical Sciences'):
        assert missing not in names


def test_abuja_layout_matches_reference_plan():
    """Relative positions read off the plan survive the move onto real coordinates."""
    p = {x['id']: x for x in _abuja_places()}
    # The access road reaches Central Administration from the north-east.
    assert p['main-road']['lat'] > p['central-admin']['lat']
    assert p['main-road']['lng'] > p['central-admin']['lng']
    # Agriculture and Science sit on the north-west side of the campus, Arts and
    # Education on the south-east side, the Female Hostel beyond the southern ring road.
    assert p['faculty-of-agriculture']['lat'] > p['faculty-of-arts']['lat']
    assert p['faculty-of-agriculture']['lng'] < p['faculty-of-arts']['lng']
    assert p['faculty-of-engineering']['lat'] > p['female-hostel']['lat'] or \
        p['faculty-of-engineering']['lng'] < p['female-hostel']['lng']
    assert p['garden']['lat'] < p['central-admin']['lat']


def test_abuja_appears_in_picker_as_mapped(client, login_as, make_user, abuja):
    login_as(client, make_user('ua_pick'))
    body = client.get('/campus-map').get_data(as_text=True)
    assert 'University of Abuja' in body
    assert 'Airport Road, Abuja (FCT)' in body
    assert f'{len(_abuja_places())} places mapped' in body


def test_abuja_uses_the_same_live_map_as_lasu(client, login_as, make_user, abuja):
    login_as(client, make_user('ua_map'))
    res = client.get('/campus-map/uniabuja')
    assert res.status_code == 302 and res.headers['Location'].endswith('/campus-map/university-of-abuja')
    body = client.get('/campus-map/university-of-abuja').get_data(as_text=True)
    assert 'University of Abuja' in body and 'Change university' in body
    assert 'Directions' in body and 'leaflet@1.9.4' in body
    assert 'imageOverlay' not in body and '.webp' not in body
    data = _payload(body)
    assert data['has_data'] is True
    assert 'kind' not in data['map'] and 'plan' not in data['map']
    assert data['map']['default_layer'] == 'street'
    assert data['map']['center'] == pytest.approx([8.9785, 7.1792], abs=0.002)
    places = {p['id']: p for p in data['places']}
    sci = places['faculty-of-science']
    assert sci['category'] == 'faculty' and sci['label_tier'] == 1 and sci['campus'] == 'Main Campus'
    assert len(sci['outline']) == 4
    assert places['central-admin']['name'] == 'Central Administration'
    assert places['garden']['label_tier'] == 2
    assert places['park']['verify'] is True and places['faculty-of-law']['verify'] is False
    keys = [c['key'] for c in data['categories']]
    assert 'faculty' in keys and 'hostel' in keys and 'health' not in keys


def test_dataset_campus_without_db_row_still_opens(app, client, login_as, make_user):
    with app.app_context():
        db.session.add(University(name='University of Abuja', short_name='UNIABUJA'))
        db.session.commit()
    login_as(client, make_user('ua_nocampus'))
    data = client.get('/api/campus-map/university-of-abuja').get_json()
    assert data['campus'] == {'id': None, 'name': 'Main Campus'}
    assert len(data['places']) > 20


def test_lasu_payload_is_unchanged_in_shape(client, login_as, make_user, campus_data):
    login_as(client, make_user('ua_lasu'))
    data = client.get(f'/api/campus-map/{campus_data["lasu_slug"]}').get_json()
    assert data['map']['default_layer'] == 'satellite'
    assert all(p['label_tier'] in (1, 2) for p in data['places'])
