"""In-app notifications — polled, not pushed. Every notification is written by the
specific event that caused it; there is no generic "something happened" path, so a
notification in the list always traces back to something real that occurred.
"""
from extensions import db
from models import Notification


def notify(user_id, type_, title, body=None, link_url=None):
    """Creates one Notification. Never raises on a bad user_id — a notification failing
    to send must never break the action that triggered it (an application status change,
    a message, etc.)."""
    try:
        n = Notification(user_id=user_id, type=type_, title=title, body=body, link_url=link_url)
        db.session.add(n)
        db.session.commit()
        return n
    except Exception:
        db.session.rollback()
        return None


def unread_count(user_id):
    return Notification.query.filter_by(user_id=user_id, is_read=False).count()


def mark_all_read(user_id):
    Notification.query.filter_by(user_id=user_id, is_read=False).update({'is_read': True})
    db.session.commit()
