from flask import Blueprint, render_template

from app.routes.dashboard_routes import _landing_stats

pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/about')
def about():
    return render_template('about.html')


@pages_bp.route('/impact')
def impact():
    # Same live skill/university counts as the landing page, so the two pages can't disagree.
    # The student and AI-training figures are fixed, verified numbers set in impact.html.
    return render_template('impact.html', stats=_landing_stats())


@pages_bp.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')


@pages_bp.route('/terms-of-service')
def terms_of_service():
    return render_template('terms-of-service.html')


@pages_bp.route("/mat101")
def math101():
    return render_template("mat101.html")
