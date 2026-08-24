from flask import Blueprint, render_template, request, jsonify
from utils.helpers import login_required, admin_required
from models import University, Faculty, Department, Course
from extensions import db

admin_academia_bp = Blueprint('admin_academia', __name__)


@admin_academia_bp.route('/admin/academia')
@login_required
@admin_required
def admin_academia_home():
    universities = University.query.order_by(University.name).all()
    return render_template('admin_academia.html', universities=universities, active_page='academia')


@admin_academia_bp.route('/admin/academia/universities/new', methods=['POST'])
@login_required
@admin_required
def new_university():
    name = (request.form.get('name') or '').strip()
    short_name = (request.form.get('short_name') or '').strip() or None
    if not name:
        return jsonify({'success': False, 'error': 'University name is required'}), 400
    if University.query.filter_by(name=name).first():
        return jsonify({'success': False, 'error': 'That university already exists'}), 409
    uni = University(name=name, short_name=short_name)
    db.session.add(uni)
    db.session.commit()
    return jsonify({'success': True, 'university': uni.to_dict()})


@admin_academia_bp.route('/admin/academia/faculties/new', methods=['POST'])
@login_required
@admin_required
def new_faculty():
    university_id = request.form.get('university_id', type=int)
    name = (request.form.get('name') or '').strip()
    if not university_id or not name:
        return jsonify({'success': False, 'error': 'University and faculty name are required'}), 400
    if Faculty.query.filter_by(university_id=university_id, name=name).first():
        return jsonify({'success': False, 'error': 'That faculty already exists at this university'}), 409
    fac = Faculty(university_id=university_id, name=name)
    db.session.add(fac)
    db.session.commit()
    return jsonify({'success': True, 'faculty': fac.to_dict()})


@admin_academia_bp.route('/admin/academia/departments/new', methods=['POST'])
@login_required
@admin_required
def new_department():
    faculty_id = request.form.get('faculty_id', type=int)
    name = (request.form.get('name') or '').strip()
    if not faculty_id or not name:
        return jsonify({'success': False, 'error': 'Faculty and department name are required'}), 400
    if Department.query.filter_by(faculty_id=faculty_id, name=name).first():
        return jsonify({'success': False, 'error': 'That department already exists in this faculty'}), 409
    dept = Department(faculty_id=faculty_id, name=name)
    db.session.add(dept)
    db.session.commit()
    return jsonify({'success': True, 'department': dept.to_dict()})


@admin_academia_bp.route('/admin/academia/departments/<int:department_id>')
@login_required
@admin_required
def admin_academia_department(department_id):
    department = Department.query.get_or_404(department_id)
    courses = Course.query.filter_by(department_id=department.id).order_by(Course.level, Course.code).all()
    return render_template(
        'admin_academia_department.html', department=department, courses=courses, active_page='academia'
    )


@admin_academia_bp.route('/admin/academia/courses/new', methods=['POST'])
@login_required
@admin_required
def new_course():
    department_id = request.form.get('department_id', type=int)
    code = (request.form.get('code') or '').strip().upper()
    title = (request.form.get('title') or '').strip()
    level = (request.form.get('level') or '').strip()
    semester = (request.form.get('semester') or '').strip() or None
    course_type = (request.form.get('course_type') or '').strip() or None
    description = (request.form.get('description') or '').strip() or None
    if not (department_id and code and title and level):
        return jsonify({'success': False, 'error': 'Department, code, title and level are required'}), 400
    if Course.query.filter_by(department_id=department_id, level=level, code=code).first():
        return jsonify({'success': False, 'error': 'That course code already exists at this level/department'}), 409
    course = Course(
        department_id=department_id, code=code, title=title, level=level,
        semester=semester, course_type=course_type, description=description,
    )
    db.session.add(course)
    db.session.commit()
    return jsonify({'success': True, 'course': course.to_dict()})


@admin_academia_bp.route('/admin/academia/courses/<int:course_id>/edit', methods=['POST'])
@login_required
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    for field in ('code', 'title', 'level', 'semester', 'course_type', 'description'):
        if field in request.form:
            value = request.form[field].strip()
            if field == 'code':
                value = value.upper()
            setattr(course, field, value or None if field in ('semester', 'course_type', 'description') else value)
    db.session.commit()
    return jsonify({'success': True, 'course': course.to_dict()})


@admin_academia_bp.route('/admin/academia/courses/<int:course_id>/delete', methods=['DELETE'])
@login_required
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({'success': True})
