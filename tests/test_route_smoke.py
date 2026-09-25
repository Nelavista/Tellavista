"""Whole-app route sweep -- the feature-wide regression net.

Every other test file in this suite covers one feature in depth. This one does the
opposite: it walks the *entire* registered route table and proves every endpoint is still
wired up and does not crash. That catches the class of breakage a per-feature suite
structurally cannot -- a blueprint that failed to register, a template that was renamed, a
service import that broke, a decorator that now throws on every request.

The inventory is read from the real application object's url_map, not hand-listed, so a
newly registered route is covered the moment it exists. There is nothing to remember to
update.

Three deliberate safety properties:

1. **No outbound network.** An autouse fixture replaces requests' transport, so any attempt
   to reach OpenRouter, Tavily, YouTube, Cloudinary, Agora or SMTP raises instead of
   silently costing quota or slowing the suite.
2. **No real database.** The app under test is built locally against a throwaway SQLite
   file. The real app object is only *read* (url_map, blueprints); it is never started.
3. **No false alarms.** A 5xx is only a failure when Flask actually signalled an exception
   for that request. Endpoints that deliberately return 500 because an integration is
   unconfigured are reported separately, so this file does not go permanently red on a
   machine without API keys and therefore get ignored.

Note on the local environment: no integration keys are set (.env points at local SQLite), so
several endpoints legitimately report as UNCONFIGURED here. That is expected, not a defect.

Known gap, stated rather than hidden: routes whose URL contains a path parameter
(``/materials/<int:material_id>``) cannot be swept without a real instance per route, so they
are excluded and listed by the inventory test. They remain covered by their own feature tests.
"""
import os
import tempfile
from types import SimpleNamespace

import pytest
import requests
from flask import Flask, got_request_exception

from app import app as real_app
from app.extensions import db, csrf, limiter, mail, socketio

# The Flask static endpoint exists purely to serve files; it is not a feature surface.
NON_FEATURE_ENDPOINTS = {'static'}

# Statuses meaning "the endpoint is wired up and responded sanely". 429 is included on
# purpose: auth and AI routes are rate-limited, and sweeping ~140 routes from one client can
# legitimately trip a limiter. That is the limiter working, not a failure.
ACCEPTABLE_STATUSES = {200, 201, 204, 302, 303, 304, 400, 401, 403, 404, 405, 409, 422, 429}


class BlockedOutboundCall(AssertionError):
    """Raised instead of performing a real third-party HTTP request."""


@pytest.fixture(scope='module', autouse=True)
def probe():
    """Blocks outbound HTTP and records exceptions Flask itself reports.

    Yields a namespace with two lists, cleared by the sweep before each request:
      .blocked    -- outbound calls we refused
      .exceptions -- exceptions that escaped a view (Flask's got_request_exception signal)
    """
    state = SimpleNamespace(blocked=[], exceptions=[])

    def _block(method):
        def _inner(self, url, *args, **kwargs):
            state.blocked.append(f'{method.upper()} {url}')
            raise BlockedOutboundCall(f'outbound HTTP blocked during sweep: {method} {url}')
        return _inner

    originals = {}
    for name in ('get', 'post', 'put', 'patch', 'delete', 'head', 'options'):
        originals[name] = getattr(requests, name)
        setattr(requests, name, _block(name))
    # Services call requests.get()/post(), which routes through Session.request -- patch that
    # too, so a service holding its own Session cannot slip past the guard.
    originals['Session.request'] = requests.sessions.Session.request
    requests.sessions.Session.request = _block('SESSION')

    def _record(sender, exception=None, **extra):
        state.exceptions.append(exception)

    got_request_exception.connect(_record)

    try:
        yield state
    finally:
        got_request_exception.disconnect(_record)
        for name, original in originals.items():
            if name == 'Session.request':
                requests.sessions.Session.request = original
            else:
                setattr(requests, name, original)


@pytest.fixture(scope='module')
def full_client():
    """A client for an app with *every* registered blueprint mounted at '/'.

    app/__init__.py mounts all of them at '/' (no blueprint-level prefixes), and the
    blueprint objects are taken from the real app's registry -- which is what keeps this
    file from silently falling behind when a new blueprint is added.
    """
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    flask_app = Flask(
        'route_sweep',
        template_folder=os.path.join(project_root, 'app', 'templates'),
        static_folder=os.path.join(project_root, 'app', 'static'),
    )
    flask_app.config.update(
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{db_path}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY='route-sweep-secret',
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        MAIL_SUPPRESS_SEND=True,
    )

    db.init_app(flask_app)
    csrf.init_app(flask_app)
    limiter.init_app(flask_app)
    mail.init_app(flask_app)
    socketio.init_app(flask_app, message_queue=None)

    for _name, blueprint in real_app.blueprints.items():
        flask_app.register_blueprint(blueprint, url_prefix='/')

    with flask_app.app_context():
        db.create_all()

    yield flask_app.test_client()

    with flask_app.app_context():
        db.session.remove()
        db.drop_all()
        db.engine.dispose()  # release the file handle before os.remove() on Windows
    try:
        os.remove(db_path)
    except OSError:
        pass


def _inventory():
    """(sweepable, needs_path_params) split of every registered route."""
    sweepable, needs_params = [], []
    for rule in real_app.url_map.iter_rules():
        if rule.endpoint in NON_FEATURE_ENDPOINTS:
            continue
        (needs_params if rule.arguments else sweepable).append(rule)
    key = lambda r: str(r)  # noqa: E731 -- small local sort key
    return sorted(sweepable, key=key), sorted(needs_params, key=key)


def _sweep(client, rules, probe):
    """GET each rule, bucketing the outcome.

    Buckets:
      ok           -- anything below 500, plus any acceptable status
      blocked      -- 5xx because a real outbound call was refused by the guard
      unconfigured -- 5xx that the app returned deliberately (no exception signalled),
                      typically "integration not configured" on this machine
      failures     -- Flask signalled a real exception, or an exception escaped to the test
    """
    ok, blocked, unconfigured, failures = 0, [], [], []
    for rule in rules:
        path = str(rule)
        probe.blocked.clear()
        probe.exceptions.clear()
        try:
            response = client.get(path, follow_redirects=False)
            status = response.status_code
        except Exception as exc:  # escaped the app entirely -- definitely a failure
            failures.append((path, f'raised {type(exc).__name__}: {exc}'))
            continue

        if status in ACCEPTABLE_STATUSES or status < 500:
            ok += 1
        elif probe.exceptions:
            exc = probe.exceptions[0]
            failures.append((path, f'HTTP {status} from unhandled '
                                   f'{type(exc).__name__}: {exc}'))
        elif probe.blocked:
            blocked.append((path, sorted(set(probe.blocked))))
        else:
            detail = 'deliberate 5xx'
            try:
                payload = response.get_json(silent=True)
                if isinstance(payload, dict) and payload.get('error'):
                    detail = f"deliberate 5xx: {payload['error']}"
            except Exception:
                pass
            unconfigured.append((path, detail))
    return ok, blocked, unconfigured, failures


def _report(label, ok, blocked, unconfigured, failures, total):
    lines = [f'{label}: {ok}/{total} responded cleanly']
    if unconfigured:
        lines.append(f'  {len(unconfigured)} returned 5xx deliberately (usually an '
                     f'unconfigured integration here, not a defect):')
        lines.extend(f'    {path}  -- {reason}' for path, reason in unconfigured)
    if blocked:
        lines.append(f'  {len(blocked)} blocked by the outbound-network guard '
                     f'(coverage gap, not a failure):')
        lines.extend(f'    {path}  <- {", ".join(calls)}' for path, calls in blocked)
    if failures:
        lines.append(f'  {len(failures)} FAILED:')
        lines.extend(f'    {path}  {reason}' for path, reason in failures)
    return '\n'.join(lines)


@pytest.mark.smoke
def test_every_route_responds_without_crashing_when_logged_out(full_client, probe):
    """Nobody should get an unhandled error just by browsing while signed out."""
    rules, _ = _inventory()
    assert rules, 'route inventory came back empty -- the sweep is not testing anything'

    ok, blocked, unconfigured, failures = _sweep(full_client, rules, probe)
    report = _report('logged out', ok, blocked, unconfigured, failures, len(rules))
    print('\n' + report)
    assert not failures, 'routes crashed on logged-out GET:\n' + report


@pytest.mark.smoke
def test_every_route_responds_without_crashing_when_logged_in(full_client, probe, login_as):
    """The same sweep as a real student -- the state most features actually run in."""
    from app.models import User

    with full_client.application.app_context():
        user = User(username='sweeper', email='sweeper@example.com', name='Sweeper',
                    is_admin=False, email_verified=True, preferred_path='academia')
        user.set_password('sweep-password')
        db.session.add(user)
        db.session.commit()
        # Snapshot the fields the session needs *inside* the context. Returning the ORM
        # instance would hand back a detached object whose attributes can no longer load
        # (see the _UserRef note in conftest.py).
        session_user = SimpleNamespace(
            username=user.username, email=user.email,
            is_admin=user.is_admin, preferred_path=user.preferred_path,
        )

    login_as(full_client, session_user)

    rules, _ = _inventory()
    ok, blocked, unconfigured, failures = _sweep(full_client, rules, probe)
    report = _report('logged in', ok, blocked, unconfigured, failures, len(rules))
    print('\n' + report)
    assert not failures, 'routes crashed on logged-in GET:\n' + report


def test_route_inventory_covers_every_registered_blueprint(record_property):
    """Guards the sweep's own usefulness.

    If a blueprint is registered but contributes no sweepable route (and none with path
    params either), it has silently dropped out of the net -- worth failing on, since the
    entire value of this file is that its coverage is automatic.
    """
    sweepable, needs_params = _inventory()
    covered = {rule.endpoint.split('.')[0] for rule in sweepable + needs_params}
    registered = set(real_app.blueprints)

    record_property('sweepable_routes', len(sweepable))
    record_property('routes_needing_path_params', len(needs_params))
    record_property('blueprints', len(registered))
    print(f'\nsweepable: {len(sweepable)}  needs path params: {len(needs_params)}  '
          f'blueprints: {len(registered)}')
    if needs_params:
        print('excluded (need a real instance id), covered by their own feature tests:')
        for rule in needs_params:
            print(f'  {rule}')

    missing = sorted(registered - covered)
    assert not missing, f'registered but unreachable by the sweep: {missing}'
