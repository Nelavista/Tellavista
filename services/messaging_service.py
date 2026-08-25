"""Simple DB-backed threaded messaging between one employer and one student — polled, not
real-time. One thread per (employer, student) pair regardless of how many gigs they've
worked together, so a conversation doesn't fragment across applications.
"""
from datetime import datetime
from extensions import db
from models import MessageThread, Message
from services.notification_service import notify


def get_or_create_thread(employer_id, student_id, application_id=None):
    thread = MessageThread.query.filter_by(employer_id=employer_id, student_id=student_id).first()
    if thread:
        if application_id and not thread.opportunity_application_id:
            thread.opportunity_application_id = application_id
            db.session.commit()
        return thread
    thread = MessageThread(employer_id=employer_id, student_id=student_id, opportunity_application_id=application_id)
    db.session.add(thread)
    db.session.commit()
    return thread


def send_message(thread, sender_id, content):
    message = Message(thread_id=thread.id, sender_id=sender_id, content=content)
    db.session.add(message)
    thread.last_message_at = datetime.utcnow()
    db.session.commit()

    recipient_id = thread.student_id if sender_id == thread.employer_id else thread.employer_id
    sender_name = thread.employer.employer_profile.company_name if sender_id == thread.employer_id and thread.employer.employer_profile else (thread.student.name or thread.student.username)
    notify(recipient_id, 'message', f'New message from {sender_name}', content[:150], '/skills/messages')
    return message


def mark_thread_read(thread, reader_id):
    # Query Message directly rather than through thread.messages — that relationship
    # carries an order_by (for display), and SQLAlchemy refuses a bulk .update() on an
    # ordered query (InvalidRequestError: "Can't call Query.update() ... when order_by()
    # has been called").
    Message.query.filter(
        Message.thread_id == thread.id, Message.sender_id != reader_id, Message.is_read.is_(False)
    ).update({'is_read': True})
    db.session.commit()
