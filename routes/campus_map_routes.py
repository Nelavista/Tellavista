"""University-aware campus map: University -> Campus -> CampusLocation.

Replaces the old single-tenant /campus-map (templates/static_pages_routes.py used to
render templates/campus-map.html with a hardcoded, LASU-only JS `locations` array baked
into the template). The page now fetches its data from /api/campus-map, which is always
scoped to the logged-in student's own university/campus -- never a client-supplied id --
so a frontend dropdown can't be used to pull another school's data (there isn't really
anything sensitive in a campus map, but the whole point of this feature is that it
follows the student automatically, not that it's browsable by id).

Admin CRUD below follows the exact pattern already used by routes/admin_academia_routes.py
(form-encoded POST, JSON response, @login_required + @admin_required, duplicate/validation
checks) so this doesn't introduce a second convention for the same kind of task.
"""
from flask import Blueprint, render_template, request, session, jsonify
from utils.helpers import login_required, admin_required
from models import User, University, Campus, CampusLocation
from extensions import db

campus_map_bp = Blueprint('campus_map', __name__)


def _current_user():
    username = session.get('user', {}).get('username')
    return User.query.filter_by(username=username).first() if username else None


@campus_map_bp.route('/campus-map')
@login_required
def campus_map_page():
    user = _current_user()
    university = user.university_ref if user else None
    return render_template(
        'campus-map.html',
        university_name=(university.name if university else 'Your Campus'),
        university_slug=((university and university.slug) or 'campus'),
    )


@campus_map_bp.route('/api/campus-map')
@login_required
def api_campus_map():
    """Server-derived from the logged-in user's own university/campus -- see module
    docstring. Returns an explicit empty-state flag when no location data exists yet for
    that school, so the frontend can show a clean message instead of a blank map."""
    user = _current_user()
    if not user or not user.university_id:
        return jsonify({
            'success': True, 'university': None, 'campus': None,
            'locations': [], 'has_data': False,
        })

    university = user.university_ref
    campus = user.campus_ref or Campus.query.filter_by(university_id=university.id, is_main=True).first()
    locations = []
    if campus:
        locations = [loc.to_dict() for loc in campus.locations.filter_by(is_active=True).order_by(CampusLocation.name)]

    return jsonify({
        'success': True,
        'university': university.to_dict(),
        'campus': campus.to_dict() if campus else None,
        'locations': locations,
        'has_data': bool(locations),
    })


# ===== Admin CRUD (mirrors routes/admin_academia_routes.py's conventions) =====

@campus_map_bp.route('/admin/campus-map')
@login_required
@admin_required
def admin_campus_map_home():
    universities = University.query.order_by(University.name).all()
    return render_template('admin_campus_map.html', universities=universities, active_page='campus_map')


@campus_map_bp.route('/admin/campus-map/locations/new', methods=['POST'])
@login_required
@admin_required
def new_campus_location():
    campus_id = request.form.get('campus_id', type=int)
    name = (request.form.get('name') or '').strip()
    category = (request.form.get('category') or '').strip() or None
    description = (request.form.get('description') or '').strip() or None
    try:
        latitude = float(request.form.get('latitude'))
        longitude = float(request.form.get('longitude'))
    except (TypeError, ValueError):
        return jsonify({'success': False, 'error': 'Valid latitude and longitude are required'}), 400

    if not campus_id or not name:
        return jsonify({'success': False, 'error': 'Campus and location name are required'}), 400
    if not Campus.query.get(campus_id):
        return jsonify({'success': False, 'error': 'Unknown campus'}), 404
    if CampusLocation.query.filter_by(campus_id=campus_id, name=name).first():
        return jsonify({'success': False, 'error': 'That location already exists on this campus'}), 409

    admin = _current_user()
    loc = CampusLocation(
        campus_id=campus_id, name=name, category=category, description=description,
        latitude=latitude, longitude=longitude, created_by=(admin.id if admin else None),
    )
    db.session.add(loc)
    db.session.commit()
    return jsonify({'success': True, 'location': loc.to_dict()})


@campus_map_bp.route('/admin/campus-map/locations/<int:location_id>/edit', methods=['POST'])
@login_required
@admin_required
def edit_campus_location(location_id):
    loc = CampusLocation.query.get_or_404(location_id)
    name = (request.form.get('name') or '').strip()
    if name:
        loc.name = name
    if 'category' in request.form:
        loc.category = (request.form.get('category') or '').strip() or None
    if 'description' in request.form:
        loc.description = (request.form.get('description') or '').strip() or None
    if request.form.get('latitude'):
        try:
            loc.latitude = float(request.form['latitude'])
        except ValueError:
            return jsonify({'success': False, 'error': 'Invalid latitude'}), 400
    if request.form.get('longitude'):
        try:
            loc.longitude = float(request.form['longitude'])
        except ValueError:
            return jsonify({'success': False, 'error': 'Invalid longitude'}), 400
    db.session.commit()
    return jsonify({'success': True, 'location': loc.to_dict()})


@campus_map_bp.route('/admin/campus-map/locations/<int:location_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_campus_location(location_id):
    loc = CampusLocation.query.get_or_404(location_id)
    db.session.delete(loc)
    db.session.commit()
    return jsonify({'success': True})


@campus_map_bp.route('/admin/campus-map/campuses/new', methods=['POST'])
@login_required
@admin_required
def new_campus():
    university_id = request.form.get('university_id', type=int)
    name = (request.form.get('name') or '').strip() or 'Main Campus'
    try:
        latitude = float(request.form['latitude']) if request.form.get('latitude') else None
        longitude = float(request.form['longitude']) if request.form.get('longitude') else None
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid latitude/longitude'}), 400

    if not university_id:
        return jsonify({'success': False, 'error': 'University is required'}), 400
    if not University.query.get(university_id):
        return jsonify({'success': False, 'error': 'Unknown university'}), 404

    campus = Campus(university_id=university_id, name=name, latitude=latitude, longitude=longitude, is_main=False)
    db.session.add(campus)
    db.session.commit()
    return jsonify({'success': True, 'campus': campus.to_dict()})
