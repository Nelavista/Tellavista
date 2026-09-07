"""Server-authoritative state machine for OpportunityApplication.status.

Before this existed, routes/admin_skills_routes.py's update_opportunity_application()
accepted any status in _APPLICATION_STATUSES as a legal next value for ANY current
status -- meaning a single PUT could take a brand-new 'applied' row straight to 'paid',
with payout_amount taken from the request body with no bound on it, and a rating could
then be posted against that fabricated 'paid' state. transition_application() below is
now the one place OpportunityApplication.status is ever written; every route that used
to assign `application.status = ...` directly calls this instead.
"""
from datetime import datetime
from extensions import db
from models import OpportunityStatusEvent

# Every legal (from_status -> {legal next statuses}) edge. A new OpportunityApplication
# is only ever created with status='applied' (routes/skills_routes.py's
# apply_opportunity) -- there is deliberately no edge back INTO 'applied' from anywhere,
# and rejected/cancelled/refunded are terminal (no further money or status movement).
#
# The one thing this table exists to make impossible is skipping 'accepted' -- that's
# the actual exploit this closes (an admin PUT taking a brand-new 'applied' row straight
# to 'paid', or to 'completed'/'disputed', with no acceptance step ever happening).
# Everything AFTER 'accepted' stays deliberately flexible (accepted can go straight to
# 'paid', 'completed', or 'disputed' in any order an admin's real workflow needs --
# "the gig is done and I already paid them" is one click, not two) since that
# flexibility isn't what let the original bug happen.
LEGAL_TRANSITIONS = {
    'applied': {'accepted', 'rejected'},
    'accepted': {'completed', 'paid', 'disputed', 'cancelled'},
    'completed': {'paid', 'disputed'},
    'paid': {'refunded', 'disputed'},
    'disputed': {'completed', 'paid', 'refunded', 'cancelled'},
    'rejected': set(),
    'cancelled': set(),
    'refunded': set(),
}


class InvalidTransition(ValueError):
    """Raised for any status change not present in LEGAL_TRANSITIONS, or a 'paid'
    transition whose payout_amount fails validation. Callers (admin routes) catch this
    and return a 400 -- it must never surface as an unhandled 500, and a rejected
    transition must never be mistaken for a silently-applied one."""


def transition_application(application, to_status, actor, note=None, payout_amount=None,
                            payment_reference=None, dispute_reason=None):
    """Validates and applies one status transition, staging an OpportunityStatusEvent
    audit row in the same session. Does NOT call db.session.commit() -- the caller
    commits once it's also finished anything else (e.g. a notification) so a failure
    partway through never leaves a half-applied change. Raises InvalidTransition (a
    ValueError) rather than returning False, so a caller can't accidentally ignore a
    rejected transition."""
    from_status = application.status
    legal_next = LEGAL_TRANSITIONS.get(from_status, set())
    if to_status not in legal_next:
        raise InvalidTransition(f"Can't move an application from '{from_status}' to '{to_status}'.")

    if to_status == 'paid':
        amount = payout_amount if payout_amount is not None else application.opportunity.payment_amount
        try:
            amount = int(amount)
        except (TypeError, ValueError):
            raise InvalidTransition('payout_amount must be a whole number')
        # Never negative, never more than the gig's own listed amount -- this platform
        # doesn't renegotiate rates after the fact, so the listing is a hard ceiling on
        # what an admin can record as paid, not just a form default they can override.
        if amount < 0 or amount > application.opportunity.payment_amount:
            raise InvalidTransition(
                f'payout_amount must be between 0 and the listed amount (₦{application.opportunity.payment_amount:,})'
            )
        application.payout_amount = amount
        application.paid_at = datetime.utcnow()
        application.payment_reference = (payment_reference or '').strip() or None
        application.paid_by_admin_id = actor.id if actor else None
    elif to_status == 'completed' and not application.completed_at:
        application.completed_at = datetime.utcnow()
    elif to_status == 'disputed':
        application.disputed_at = datetime.utcnow()
        application.dispute_reason = (dispute_reason or '').strip() or None
    elif to_status == 'refunded':
        application.refunded_at = datetime.utcnow()

    application.status = to_status
    db.session.add(OpportunityStatusEvent(
        application_id=application.id, actor_user_id=(actor.id if actor else None),
        from_status=from_status, to_status=to_status, note=(note or '').strip() or None,
    ))
    return application
