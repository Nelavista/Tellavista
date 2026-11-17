"""Email alert for new Nelavista Talent requests.

Every request submitted at /talent/request is saved first (admin queue at
/admin/talent-requests), then announced by email to TALENT_REQUEST_NOTIFY_EMAIL
(default hello@nelavista.com). Reply-To is the employer's work email, so replying to the
alert answers the employer directly.

The email is best-effort: if SMTP is down or not configured, the failure is logged and the
request stays safely in the database. A submission never fails because of email.
"""
from html import escape
import logging

from flask import current_app, url_for
from flask_mail import Message

from app.services import talent_network as tn

log = logging.getLogger(__name__)
DEFAULT_RECIPIENT = 'hello@nelavista.com'


def _rows(req):
    category = tn.CATEGORY_BY_SLUG.get(req.category, {}).get('name') or ('Something else' if req.category == 'other' else None)
    return [
        ('Company', req.company_name),
        ('Contact', req.contact_name + (f', {req.job_title}' if req.job_title else '')),
        ('Work email', req.work_email),
        ('Website', req.company_website),
        ('Country', req.country),
        ('What they need', req.need_summary),
        ('Category', category),
        ('Number of people', tn.label_for(tn.HEADCOUNTS, req.headcount) or None),
        ('Skills', req.skills),
        ('Engagement', tn.label_for(tn.ENGAGEMENT_TYPES, req.engagement_type)),
        ('Start', tn.label_for(tn.START_WINDOWS, req.start_window) or None),
        ('Budget / person / month', tn.label_for(tn.BUDGET_RANGES, req.budget_range) or None),
        ('Working-hours overlap', tn.label_for(tn.TIMEZONES, req.timezone) or None),
        ('Started from profile', req.profile_ref),
        ('Anything else', req.details),
    ]


def build_request_alert(req):
    rows = [(k, v) for k, v in _rows(req) if v]
    admin_url = url_for('talent.admin_requests', _external=True)
    subject = f'New talent request: {req.company_name}'
    category = dict(rows).get('Category')
    if category:
        subject += f' ({category})'

    text = 'A new talent request came in through nelavista.com/talent.\n\n'
    text += '\n'.join(f'{k}: {v}' for k, v in rows)
    text += f'\n\nReply to this email to answer {req.contact_name} directly.\nAll requests: {admin_url}\n'

    cells = ''.join(
        f'<tr><td style="padding:8px 16px 8px 0;color:#69717f;vertical-align:top;white-space:nowrap">{escape(k)}</td>'
        f'<td style="padding:8px 0;color:#0c1322;white-space:pre-wrap">{escape(str(v))}</td></tr>'
        for k, v in rows
    )
    html = (
        '<div style="font-family:Arial,Helvetica,sans-serif;max-width:640px;margin:0 auto;font-size:14px;line-height:1.5">'
        '<p style="margin:0 0 4px;color:#1535a8;font-size:12px;letter-spacing:.08em;text-transform:uppercase">Nelavista Talent</p>'
        f'<h1 style="margin:0 0 16px;font-size:20px;color:#0c1322">New talent request from {escape(req.company_name)}</h1>'
        f'<table style="border-collapse:collapse;width:100%">{cells}</table>'
        f'<p style="margin:24px 0 0;color:#384357">Reply to this email to answer {escape(req.contact_name)} directly.</p>'
        f'<p style="margin:8px 0 0"><a href="{escape(admin_url)}" style="color:#1535a8">Open the talent request queue</a></p>'
        '</div>'
    )
    recipient = current_app.config.get('TALENT_REQUEST_NOTIFY_EMAIL') or DEFAULT_RECIPIENT
    return Message(subject=subject, recipients=[recipient], body=text, html=html, reply_to=req.work_email,
                   sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@nelavista.com'))


def send_request_alert(req) -> bool:
    """Returns True if the alert was handed to the mail server."""
    try:
        from app.routes.auth_routes import _send_mail_or_raise
        _send_mail_or_raise(build_request_alert(req))
        return True
    except Exception:
        log.exception('Talent request %s saved, but the email alert could not be sent', req.id)
        return False
