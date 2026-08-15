from flask import Blueprint, redirect, url_for
from utils.helpers import login_required

tech_bp = Blueprint('tech', __name__)


@tech_bp.route('/tech-skills')
@login_required
def hub():
    """Old URL for what is now the real Skills section (see routes/skills_routes.py).
    Kept as a redirect only for backward compatibility with anything already linking here."""
    return redirect(url_for('skills.home'))
