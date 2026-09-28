"""Product analytics via PostHog (PRD §21, migration-map gap G5) -- minimal, env-gated,
server-side only.

Design rules, matching how Sentry is wired in logging_config.py:

- Genuinely absent until POSTHOG_API_KEY is set. Every public call is a no-op without
  it -- no network client is ever constructed, so local dev and the test suite pay
  nothing and can never make a real call.
- Best-effort, always. Analytics must never break (or even slow the error path of) the
  user action it is measuring: every call swallows and logs. The posthog-python client
  also sends on a background thread with its own internal error handling, so a slow or
  down PostHog host never stalls a request.
- Server-side capture only. The app has no shared base template (every page is
  standalone HTML), so a JS snippet would mean editing dozens of templates and a CSP
  change; key funnel events are far cheaper and more reliable to emit from the routes
  that already own them (signup, onboarding complete, CBT submit, AI calls).
- Server events land under a distinct_id of `user:<username>` -- a stable join key that
  PostHog funnels can follow across events without needing autocapture cookies.

Events emitted (PRD §21 funnel): user_signup, onboarding_completed, cbt_submitted
(auto-scored attempts only -- the scored event is the signal), and ai_call for every
provider chat/embed (property `ok` distinguishes success/failure, so AI reliability is
queryable, not just volume).
"""
import logging

from app.config import POSTHOG_API_KEY, POSTHOG_HOST

logger = logging.getLogger('nelavista.posthog')

# Event names are constants so dashboards can't silently drift from code.
EVENT_SIGNUP = 'user_signup'
EVENT_ONBOARDING_COMPLETED = 'onboarding_completed'
EVENT_CBT_SUBMITTED = 'cbt_submitted'
EVENT_AI_CALL = 'ai_call'

_client = None
_initialized = False


def _get_client():
    """Lazily build the posthog client on first use, only when configured. Module-level
    lazy init (rather than import-time) keeps `import app.services.analytics` free of
    side effects for every test and for every deploy without a key."""
    global _client, _initialized
    if not _initialized:
        _initialized = True
        if POSTHOG_API_KEY:
            try:
                import posthog
                _client = posthog.Posthog(
                    POSTHOG_API_KEY, host=POSTHOG_HOST,
                    # Small + flush-fast: a single-worker deployment doesn't need a big
                    # queue, and flushing quickly keeps a crash from losing the queue.
                    sync_mode=False, flush_at=20, flush_interval=10,
                )
                logger.info('PostHog product analytics initialized (%s).', POSTHOG_HOST)
            except ImportError:
                logger.warning(
                    'POSTHOG_API_KEY is set but the posthog package is not installed -- '
                    'add posthog to requirements.txt to enable product analytics.'
                )
            except Exception:
                logger.exception('Failed to initialize PostHog client -- analytics disabled.')
    return _client


def capture(distinct_id, event, properties=None):
    """Send one event to PostHog. Best-effort by contract -- never raises, never logs
    anything sensitive (event names + countable properties only, never answer/prompt
    content). No-op without POSTHOG_API_KEY."""
    if not POSTHOG_API_KEY:
        return
    client = _get_client()
    if not client:
        return
    try:
        client.capture(distinct_id, event, properties or {})
    except Exception:
        logger.exception('PostHog capture failed for event %s (ignored).', event)


def user_distinct_id(username):
    """Stable server-side identity for funnels -- `user:<username>`. None-safe so
    callers can pass session lookups straight through."""
    return f'user:{username}' if username else None


def capture_event_for_user(username, event, properties=None):
    """Convenience wrapper for route code: resolve the session username to a distinct_id
    and capture. A missing username (shouldn't happen post-login) is skipped silently."""
    distinct_id = user_distinct_id(username)
    if not distinct_id:
        return
    capture(distinct_id, event, properties)
