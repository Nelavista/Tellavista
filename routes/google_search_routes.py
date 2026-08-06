from flask import Blueprint, request, jsonify
from utils.helpers import login_required
from models import Material
from extensions import db
from services.google_search_service import OPENSTAX_MATERIALS, search_google_pdfs
from services.open_textbook_library_service import search_open_textbook_library

google_search_bp = Blueprint('google_search', __name__)


# ===== FETCH OPENSTAX MATERIALS FOR MULTIPLE COURSES =====
@google_search_bp.route('/api/fetch-google-materials-batch', methods=['POST'])
@login_required
def fetch_google_materials_batch():
    """
    Fetch materials from OpenStax database AND Google Custom Search for multiple course codes.
    Prioritizes OpenStax materials (free, high-quality textbooks).
    Falls back to Google Custom Search for additional resources.
    Expects JSON: {'course_codes': ['MAT101', 'CSC111', ...], 'department': ..., 'level': ..., 'semester': ...}
    """
    try:
        data = request.get_json()
        course_codes = data.get('course_codes', [])
        department = (data.get('department') or '').strip() or 'General'
        level = (data.get('level') or '').strip() or '100'
        semester = (data.get('semester') or '').strip() or 'First Semester'

        if not course_codes:
            return jsonify({'error': 'No course codes provided'}), 400

        all_materials = []
        seen_urls = set()
        google_unavailable = False

        for code in course_codes[:10]:  # Process up to 10 courses
            code = code.upper().strip()

            # === STEP 1: Check OpenStax database first ===
            openstax_resources = OPENSTAX_MATERIALS.get(code, [])

            if openstax_resources:
                for resource in openstax_resources:
                    # Check if this URL already exists in database
                    existing = Material.query.filter_by(
                        external_url=resource['url'],
                        source='openstax'
                    ).first()

                    if existing:
                        if existing.external_url not in seen_urls:
                            seen_urls.add(existing.external_url)
                            all_materials.append(existing.to_dict())
                    else:
                        # Create new material entry for OpenStax, tagged with the
                        # student's real department/level/semester so it actually shows
                        # up again later when the library is filtered by those fields —
                        # previously these were hardcoded to 'General'/'100'/'First
                        # Semester' regardless of the real course, which made them
                        # invisible to semester-based filtering after the first fetch.
                        new_material = Material(
                            title=resource['title'],
                            course_code=code,
                            external_url=resource['url'],
                            source='openstax',
                            is_approved=True,  # Auto-approve OpenStax materials
                            uploaded_by='OpenStax',
                            department=department,
                            level=level,
                            semester=semester,
                            next_topic=resource.get('description', '')
                        )
                        db.session.add(new_material)
                        all_materials.append(new_material.to_dict())
                        seen_urls.add(resource['url'])

            # === STEP 2: Check cached Google materials ===
            cached = Material.query.filter_by(
                course_code=code,
                source='google_auto',
                is_approved=True
            ).all()

            if cached:
                for material in cached:
                    if material.external_url and material.external_url not in seen_urls:
                        seen_urls.add(material.external_url)
                        all_materials.append(material.to_dict())

            # === STEP 2.5: Check cached Open Textbook Library materials ===
            cached_otl = Material.query.filter_by(
                course_code=code,
                source='oer_library',
                is_approved=True
            ).all()

            if cached_otl:
                for material in cached_otl:
                    if material.external_url and material.external_url not in seen_urls:
                        seen_urls.add(material.external_url)
                        all_materials.append(material.to_dict())

            # === STEP 3: Nothing cached anywhere for this course — try live sources ===
            if not openstax_resources and not cached and not cached_otl:
                # Open Textbook Library first — real textbooks, keyed by department
                # rather than course code, so it works even for course codes Tavily's
                # keyword search wouldn't match well.
                otl_results, otl_ok = search_open_textbook_library(department, max_results=3)
                for r in otl_results:
                    if r['url'] not in seen_urls:
                        seen_urls.add(r['url'])
                        new_material = Material(
                            title=r['title'][:200],
                            course_code=code,
                            external_url=r['url'],
                            source='oer_library',
                            is_approved=True,
                            uploaded_by='Open Textbook Library',
                            department=department,
                            level=level,
                            semester=semester,
                            next_topic=r.get('snippet', '')[:190]
                        )
                        db.session.add(new_material)
                        all_materials.append(new_material.to_dict())

                results, api_ok = search_google_pdfs(code, max_results=5)
                if not api_ok:
                    google_unavailable = True
                for r in results:
                    if r['url'] not in seen_urls:
                        seen_urls.add(r['url'])

                        existing = Material.query.filter_by(
                            external_url=r['url'],
                            source='google_auto'
                        ).first()

                        if not existing:
                            new_material = Material(
                                title=r['title'][:200],
                                course_code=code,
                                external_url=r['url'],
                                source='google_auto',
                                is_approved=True,
                                uploaded_by='Google Search',
                                department=department,
                                level=level,
                                semester=semester
                            )
                            db.session.add(new_material)
                            all_materials.append(new_material.to_dict())
                        else:
                            all_materials.append(existing.to_dict())

        db.session.commit()

        return jsonify({
            'success': True,
            'materials': all_materials,
            'count': len(all_materials),
            'search_unavailable': google_unavailable,
        })

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] fetch_google_materials_batch: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ===== FETCH MATERIALS FOR A SINGLE COURSE (OpenStax + Google fallback) =====
@google_search_bp.route('/api/fetch-google-materials/<course_code>')
@login_required
def fetch_google_materials(course_code):
    """
    Fetch materials for a specific course code.
    Tries OpenStax first, then Google Custom Search as fallback.
    Caches results in database to avoid repeated lookups.
    """
    try:
        course_code = course_code.upper().strip()
        department = (request.args.get('department') or '').strip() or 'General'
        level = (request.args.get('level') or '').strip() or '100'
        semester = (request.args.get('semester') or '').strip() or 'First Semester'
        all_materials = []
        google_unavailable = False

        # Check OpenStax first
        openstax_resources = OPENSTAX_MATERIALS.get(course_code, [])

        if openstax_resources:
            for resource in openstax_resources:
                existing = Material.query.filter_by(
                    external_url=resource['url'],
                    source='openstax'
                ).first()

                if existing:
                    all_materials.append(existing.to_dict())
                else:
                    new_material = Material(
                        title=resource['title'],
                        course_code=course_code,
                        external_url=resource['url'],
                        source='openstax',
                        is_approved=True,
                        uploaded_by='OpenStax',
                        department=department,
                        level=level,
                        semester=semester,
                        next_topic=resource.get('description', '')
                    )
                    db.session.add(new_material)
                    all_materials.append(new_material.to_dict())

        # Check cached Google materials
        cached = Material.query.filter_by(
            course_code=course_code,
            source='google_auto',
            is_approved=True
        ).all()

        if cached:
            for material in cached:
                all_materials.append(material.to_dict())

        # Check cached Open Textbook Library materials
        cached_otl = Material.query.filter_by(
            course_code=course_code,
            source='oer_library',
            is_approved=True
        ).all()

        if cached_otl:
            for material in cached_otl:
                all_materials.append(material.to_dict())

        # Nothing cached anywhere for this course — try live sources
        if not openstax_resources and not cached and not cached_otl:
            otl_results, otl_ok = search_open_textbook_library(department, max_results=3)
            for r in otl_results:
                new_material = Material(
                    title=r['title'][:200],
                    course_code=course_code,
                    external_url=r['url'],
                    source='oer_library',
                    is_approved=True,
                    uploaded_by='Open Textbook Library',
                    department=department,
                    level=level,
                    semester=semester,
                    next_topic=r.get('snippet', '')[:190]
                )
                db.session.add(new_material)
                all_materials.append(new_material.to_dict())

            results, api_ok = search_google_pdfs(course_code, max_results=8)
            if not api_ok:
                google_unavailable = True
            for r in results:
                existing = Material.query.filter_by(
                    external_url=r['url'],
                    source='google_auto'
                ).first()

                if not existing:
                    new_material = Material(
                        title=r['title'][:200],
                        course_code=course_code,
                        external_url=r['url'],
                        source='google_auto',
                        is_approved=True,
                        uploaded_by='Google Search',
                        department=department,
                        level=level,
                        semester=semester
                    )
                    db.session.add(new_material)
                    all_materials.append(new_material.to_dict())
                else:
                    all_materials.append(existing.to_dict())

        db.session.commit()

        return jsonify({
            'success': True,
            'materials': all_materials,
            'count': len(all_materials),
            'search_unavailable': google_unavailable,
        })

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] fetch_google_materials: {str(e)}")
        return jsonify({'error': str(e)}), 500
