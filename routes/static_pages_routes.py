from flask import Blueprint, render_template

pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/about')
def about():
    return render_template('about.html')


@pages_bp.route('/campus-map')
def campus_map():
    return render_template('campus-map.html')


@pages_bp.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')


@pages_bp.route('/terms-of-service')
def terms_of_service():
    return render_template('terms-of-service.html')


@pages_bp.route("/mat101")
def math101():
    return render_template("mat101.html")
