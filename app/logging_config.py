"""Structured application logging.

Replaces ad-hoc print() debugging for the paths that actually matter operationally --
startup, database, auth, payments/transactions, AI calls, background processing -- with
real log records (level, timestamp, logger name) that a platform like Render's log
stream, or an external aggregator, can filter and alert on. This is deliberately NOT a
full rewrite of every print() in the codebase (~295 of them, mostly harmless debug
narration in routes/services) -- see the Level 1 audit report for why that's out of
scope for this pass. New/changed code from this pass (routes/cbt_routes.py,
events.py, routes/auth_routes.py, routes/admin_skills_routes.py, make_admin.py,
database.py) uses this logger; everything else keeps its existing debug_print()/print()
calls unchanged.

NEVER log: passwords, password hashes, session/reset/verification tokens, API keys, or
raw request bodies that might carry any of the above. Log identifiers (user id,
username, email) freely -- those are fine for correlating an incident, not secrets.

Deployment note: set SENTRY_DSN to also send ERROR-and-above records to Sentry (or any
Sentry-protocol-compatible service). Without it, logs still go to stdout, which Render
(and most PaaS platforms) captures automatically -- structured logging alone is useful
even with no external platform configured.
"""
import logging
import os
import sys


def configure_logging():
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    level = logging.DEBUG if debug_mode else logging.INFO

    root = logging.getLogger()
    root.setLevel(level)
    # Avoid duplicate handlers if this ever gets imported/called more than once
    # (e.g. by a test harness that imports app.py multiple times in-process).
    if not any(isinstance(h, logging.StreamHandler) for h in root.handlers):
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(
            fmt='%(asctime)s %(levelname)s [%(name)s] %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S%z',
        ))
        root.addHandler(handler)

    sentry_dsn = os.getenv('SENTRY_DSN')
    if sentry_dsn:
        try:
            import sentry_sdk
            from sentry_sdk.integrations.flask import FlaskIntegration
            from sentry_sdk.integrations.logging import LoggingIntegration
            sentry_sdk.init(
                dsn=sentry_dsn,
                integrations=[
                    FlaskIntegration(),
                    LoggingIntegration(level=logging.INFO, event_level=logging.ERROR),
                ],
                traces_sample_rate=float(os.getenv('SENTRY_TRACES_SAMPLE_RATE', '0.0')),
                environment=os.getenv('ENVIRONMENT', 'production'),
            )
            logging.getLogger('nelavista').info('Sentry error tracking initialized.')
        except ImportError:
            logging.getLogger('nelavista').warning(
                'SENTRY_DSN is set but the sentry-sdk package is not installed -- '
                'add sentry-sdk to requirements.txt to enable it.'
            )

    return logging.getLogger('nelavista')


logger = configure_logging()
