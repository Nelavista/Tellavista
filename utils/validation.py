"""Shared input-validation helpers used across Skills (and anywhere else that stores a
student-supplied URL that later renders as a clickable link).

One function, one place it can be wrong -- see safe_external_url's docstring for why
this was extracted rather than left as four separate inline checks.
"""
from urllib.parse import urlparse


def safe_external_url(url, max_length=500):
    """Returns `url` stripped and truncated if it's a plain http(s) link with a real
    hostname, or None otherwise.

    Before this existed, update_project()'s `external_links` field ran this exact check
    inline, but `repo_url`/`live_url` on the same model -- rendered as raw `<a href>` on
    both the student's own project page and their PUBLIC Talent Profile -- did not. A
    student could set repo_url to a `javascript:`/`data:`/`vbscript:` URI and have it
    execute in any visitor's browser who clicked it. Centralizing the check here means
    every field that can end up as an href (repo_url, live_url, external_links,
    portfolio_url, a competition entry's submission_url, ...) goes through the same one
    function instead of four independent, driftable copies of the same three lines.

    Deliberately permissive about *content* (no domain allowlist, no reachability check --
    a dead or wrong link is the student's own problem) and strict only about *scheme*,
    since scheme is the only part that can turn a link into code execution.
    """
    if not url:
        return None
    url = str(url).strip()[:max_length]
    if not url:
        return None
    parsed = urlparse(url)
    if parsed.scheme not in ('http', 'https') or not parsed.hostname:
        return None
    return url


def password_strength_error(password):
    """Returns a user-facing error string if `password` is too weak to set (whether at
    signup or via password reset), or None if it's acceptable. Kept as one shared check
    -- routes/auth_routes.py's reset-password flow used only a bare length check before
    this existed, letting through things like '11111111' or 'aaaaaaaa'.

    Deliberately modest requirements (length + a letter + a digit, no symbol/uppercase
    mandate) -- strict composition rules push people toward predictable substitutions
    ('Password1!') without meaningfully raising real entropy, and this app has no
    business being the strictest link in a student's password hygiene.
    """
    if not password or len(password) < 8:
        return 'Password must be at least 8 characters long.'
    if len(password) > 128:
        return 'Password is too long.'
    if not any(c.isalpha() for c in password):
        return 'Password must include at least one letter.'
    if not any(c.isdigit() for c in password):
        return 'Password must include at least one number.'
    return None
