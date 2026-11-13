"""The Opportunities space: the student's own earning home, separate from Skills.

These pages used to live inside the Skills blueprint at /skills/opportunities,
/skills/gigs and /skills/earnings, rendered with the Skills sidebar. That meant
Skills content appeared in Opportunities and Opportunities appeared in Skills even
though the four-space picker treats them as different products. They now have their
own blueprint, their own shell (components/opportunities_sidebar.html) and their own
URLs; the old Skills URLs redirect here so existing links keep working.

Content boundary: this space lists work (opportunities, gigs) and money (earnings).
It never shows the Skills catalog, learning paths, projects or the skill dashboard.

Two rules keep that boundary from being "fixed" back into a leak later:

1. Competitions and challenges stay in Skills even though Competition.prize_amount is
   money. They are the Showcase step of the Skills journey (Learn -> Practice -> Build ->
   Verify -> Showcase), a prize for demonstrating a skill, not paid work for a client.
   Only the Get Discovered -> Earn end of that journey lives here.
2. Message threads are the single deliberate cross-space link, from this space's
   sidebar back to skills.messages. Hiring starts on a Talent Profile (a Skills page),
   and an application-status notification points here, so a student accepting work
   needs one click to reply. Do not add a second such link; everything else goes
   through the /choose-path switcher.
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.utils.helpers import login_required
from app.models import User, Skill, StudentSkill, Opportunity, OpportunityApplication
from app.extensions import db
from sqlalchemy.exc import IntegrityError
from app.services.skills_service import compute_payout_breakdown

opportunities_bp = Blueprint('opportunities', __name__)


def _current_user():
    return User.query.filter_by(username=session['user']['username']).first()


@opportunities_bp.before_request
def _ensure_session_user_exists():
    """Same narrow guard as skills_routes: a session can outlive its user row (an admin
    deleted the account, a dev DB reset). Without this the routes below 500 inside
    _current_user() instead of sending the student back to login."""
    if 'user' not in session:
        return None
    if not User.query.filter_by(username=session['user']['username']).first():
        session.clear()
        flash('Your session has expired. Please log in again.')
        return redirect(url_for('auth.login'))


# ===== OPPORTUNITIES (matched to the skills the student has started) =====
@opportunities_bp.route('/opportunities')
@login_required
def index():
    user = _current_user()
    # progress_by_skill replaces a call to opportunity_match_pct() per opportunity below
    # -- that function's whole body is this same StudentSkill lookup, run again for every
    # row even though every row's answer was already sitting in one query's results.
    progress_by_skill = {s.skill_id: s.progress_pct for s in StudentSkill.query.filter_by(student_id=user.id).all()}
    all_opps = Opportunity.query.filter_by(is_published=True).order_by(Opportunity.order).all()
    my_applications = {a.opportunity_id: a for a in OpportunityApplication.query.filter_by(student_id=user.id).all()}

    rows = []
    for o in all_opps:
        rows.append({
            'opportunity': o,
            'match_pct': progress_by_skill.get(o.skill_id, 0),
            'application': my_applications.get(o.id),
        })
    rows.sort(key=lambda r: -r['match_pct'])
    return render_template('opportunities_home.html', rows=rows, active_page='home')


@opportunities_bp.route('/opportunities/<int:opportunity_id>/apply', methods=['POST'])
@login_required
def apply(opportunity_id):
    opportunity = Opportunity.query.filter_by(id=opportunity_id, is_published=True).first_or_404()
    user = _current_user()
    existing = OpportunityApplication.query.filter_by(opportunity_id=opportunity.id, student_id=user.id).first()
    if not existing:
        db.session.add(OpportunityApplication(opportunity_id=opportunity.id, student_id=user.id))
        try:
            db.session.commit()
            flash(f'Applied to "{opportunity.title}"!')
        except IntegrityError:
            # OpportunityApplication already has a DB-level unique constraint on
            # (opportunity_id, student_id) -- data can't actually duplicate -- but the
            # check-then-act above has no isolation of its own, so a double-click/retry
            # race previously hit an unhandled IntegrityError -> 500 instead of the same
            # "you're in" outcome the winner of the race gets.
            db.session.rollback()
            flash(f'You already applied to "{opportunity.title}".')
    else:
        flash(f'You already applied to "{opportunity.title}".')
    return redirect(request.referrer or url_for('opportunities.index'))


@opportunities_bp.route('/opportunities/gigs')
@login_required
def gigs():
    """The full open marketplace — every published gig, filterable, not just the ones
    matched to skills the student has already started. Opportunities (the personalized
    feed) is 'best matches'; Gigs is 'browse everything', same distinction Upwork/Fiverr
    draw between a matched feed and open browse."""
    user = _current_user()
    skill_id = request.args.get('skill_id', type=int)
    location = request.args.get('location', '').strip()
    min_pay = request.args.get('min_pay', type=int)

    query = Opportunity.query.filter_by(is_published=True)
    if skill_id:
        query = query.filter_by(skill_id=skill_id)
    if location:
        query = query.filter(Opportunity.location.ilike(f'%{location}%'))
    if min_pay:
        query = query.filter(Opportunity.payment_amount >= min_pay)
    all_opps = query.order_by(Opportunity.created_at.desc()).all()

    # Same batching as index() above -- one query for every skill's progress instead of
    # one opportunity_match_pct() call (itself a query) per gig on the page.
    progress_by_skill = {s.skill_id: s.progress_pct for s in StudentSkill.query.filter_by(student_id=user.id).all()}
    my_applications = {a.opportunity_id: a for a in OpportunityApplication.query.filter_by(student_id=user.id).all()}
    rows = [{
        'opportunity': o, 'application': my_applications.get(o.id),
        'match_pct': progress_by_skill.get(o.skill_id, 0),
    } for o in all_opps]

    skills = Skill.query.filter_by(is_published=True).order_by(Skill.name).all()
    return render_template('opportunities_gigs.html', rows=rows, skills=skills, active_page='gigs',
                            skill_id=skill_id, location=location, min_pay=min_pay)


@opportunities_bp.route('/opportunities/earnings')
@login_required
def earnings():
    user = _current_user()
    # joinedload: a.opportunity below is otherwise a separate lazy-loaded query per
    # application (OpportunityApplication.opportunity has no lazy= override, so it
    # defaults to lazy='select') -- one JOIN here instead of N queries for N applications.
    applications = (
        OpportunityApplication.query.filter_by(student_id=user.id)
        .options(db.joinedload(OpportunityApplication.opportunity))
        .order_by(OpportunityApplication.applied_at.desc()).all()
    )
    for a in applications:
        a.breakdown = compute_payout_breakdown(a.payout_amount if a.status == 'paid' else a.opportunity.payment_amount)
    summary = {
        'total_paid': sum(a.payout_amount or 0 for a in applications if a.status == 'paid'),
        'pending': sum((a.opportunity.payment_amount or 0) for a in applications if a.status in ('applied', 'accepted')),
        'completed_count': sum(1 for a in applications if a.status == 'paid'),
        'active_count': sum(1 for a in applications if a.status in ('applied', 'accepted', 'completed')),
    }
    return render_template('opportunities_earnings.html', applications=applications, summary=summary, active_page='earnings')
