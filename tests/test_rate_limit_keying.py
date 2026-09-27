"""PRD §5.4/§7 rate-limit keying: per-user where a user exists, per-IP otherwise.

The old key was get_remote_address only, which both failed the "per-user rate limits"
AC on AI endpoints and throttled every student behind one campus NAT as a single
client. See extensions.rate_limit_key.
"""
from flask import session

from app.extensions import rate_limit_key


def test_logged_in_key_is_the_user_not_the_ip(app):
    with app.test_request_context('/', environ_base={'REMOTE_ADDR': '10.0.0.5'}):
        session['user'] = {'username': 'alice'}
        assert rate_limit_key() == 'user:alice'
        # Changing the perceived IP must not reset a logged-in user's budget.
        assert rate_limit_key() == 'user:alice'


def test_anonymous_key_falls_back_to_remote_address(app):
    with app.test_request_context('/', environ_base={'REMOTE_ADDR': '10.0.0.5'}):
        assert rate_limit_key() == '10.0.0.5'
    with app.test_request_context('/', environ_base={'REMOTE_ADDR': '10.0.0.6'}):
        assert rate_limit_key() == '10.0.0.6'


def test_different_users_get_different_budgets(app):
    with app.test_request_context('/'):
        session['user'] = {'username': 'alice'}
        alice = rate_limit_key()
        session['user'] = {'username': 'bob'}
        bob = rate_limit_key()
    assert alice != bob
    assert alice == 'user:alice' and bob == 'user:bob'
