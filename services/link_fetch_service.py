"""Fetches real content from a URL a student submitted with their project (repo_url,
live_url, or an external link) so the AI review can reason about what was actually
built, not just the student's written account of it — see
services/ai_service.py's evaluate_project_submission/evaluate_final_project, which
this feeds via the `submission_details` string built in routes/skills_routes.py.

This is the ONLY place in the codebase that makes an outbound HTTP request to a
URL a student controls, rather than a fixed, trusted API endpoint. That makes it a
textbook SSRF surface (a student could submit `http://169.254.169.254/...` or
`http://localhost:6379/...` to probe internal services) if not handled carefully,
so every request here goes through _is_safe_url first — see its own docstring for
exactly what that checks and its one documented residual limitation.

Every function here is best-effort: network errors, timeouts, and unexpected
response shapes all resolve to None rather than raising, so a fetch failure never
blocks or crashes a review — the caller falls back to the student's own written
description, same as before this module existed.
"""
import re
import socket
import ipaddress
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup

from config import GITHUB_TOKEN

_MAX_REDIRECTS = 3
_DEFAULT_TIMEOUT = 6
_DEFAULT_MAX_BYTES = 250_000
_USER_AGENT = 'NelavistaProjectReview/1.0 (+https://nelavista.com)'


def _is_safe_url(url):
    """True only for an http(s) URL whose hostname resolves exclusively to public,
    routable IP addresses — rejects loopback, private (RFC1918), link-local (which
    covers the 169.254.169.254 cloud-metadata address), reserved, multicast, and
    unspecified ranges, IPv4 and IPv6 alike.

    Limitation, stated plainly: this resolves DNS here and checks the result, but the
    actual HTTP request (made by `requests` moments later) re-resolves the same
    hostname itself. A sub-second DNS-rebinding race between these two lookups is a
    theoretical residual risk. Closing that fully requires pinning the exact IP we
    validated into the connection (a custom transport adapter) — not done here because
    the added complexity isn't proportionate to this being a portfolio/education
    platform's project-review feature, not a payments or infra-control surface. This
    check still blocks the overwhelming majority of real SSRF attempts (anything aimed
    at localhost, private ranges, or cloud metadata) with a straightforward, auditable
    implementation.
    """
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    if parsed.scheme not in ('http', 'https') or not parsed.hostname:
        return False

    try:
        infos = socket.getaddrinfo(parsed.hostname, None)
    except socket.gaierror:
        return False
    if not infos:
        return False

    for info in infos:
        raw_ip = info[4][0]
        try:
            ip = ipaddress.ip_address(raw_ip)
        except ValueError:
            return False
        if (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
                or ip.is_multicast or ip.is_unspecified):
            return False
    return True


def _get_with_safe_redirects(url, timeout, stream):
    """requests.get, but manually following redirects (capped) and re-validating each
    hop with _is_safe_url before following it — a URL that's safe today could otherwise
    redirect straight to an internal address."""
    current = url
    for _ in range(_MAX_REDIRECTS + 1):
        if not _is_safe_url(current):
            return None
        response = requests.get(
            current, timeout=timeout, stream=stream, allow_redirects=False,
            headers={'User-Agent': _USER_AGENT},
        )
        if response.status_code in (301, 302, 303, 307, 308) and response.headers.get('Location'):
            current = urljoin(current, response.headers['Location'])
            response.close()
            continue
        return response
    return None


def fetch_page_text(url, max_bytes=_DEFAULT_MAX_BYTES, timeout=_DEFAULT_TIMEOUT):
    """Best-effort: fetch a page and return its visible text, truncated. None on any
    failure (unsafe URL, unreachable, timeout, not HTML, etc.) — never raises."""
    if not url:
        return None
    try:
        response = _get_with_safe_redirects(url, timeout=timeout, stream=True)
        if response is None or response.status_code != 200:
            return None

        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type and 'application/xhtml' not in content_type:
            response.close()
            return None

        chunks = []
        total = 0
        for chunk in response.iter_content(chunk_size=8192):
            chunks.append(chunk)
            total += len(chunk)
            if total >= max_bytes:
                break
        response.close()

        html = b''.join(chunks).decode('utf-8', errors='replace')
        soup = BeautifulSoup(html, 'html.parser')
        for tag in soup(['script', 'style']):
            tag.decompose()
        text = ' '.join(soup.get_text(separator=' ').split())
        return text[:4000] if text else None
    except Exception:
        return None


_GITHUB_HOSTS = {'github.com', 'www.github.com'}
_SAFE_PATH_SEGMENT = re.compile(r'^[\w.-]+$')


def fetch_github_summary(repo_url):
    """Best-effort: for a github.com repo URL, return a short text summary built from
    GitHub's public REST API (description, language, topics, README excerpt) — no auth
    required for public repos, though an optional GITHUB_TOKEN (config.py) raises the
    rate limit from 60/hr to 5000/hr per the same 'unset = graceful no-op' pattern
    YOUTUBE_API_KEY_2 already uses. Returns None for a non-GitHub URL, a private/
    nonexistent repo, or any error."""
    if not repo_url:
        return None
    try:
        parsed = urlparse(repo_url)
        if parsed.hostname not in _GITHUB_HOSTS:
            return None
        parts = [p for p in parsed.path.split('/') if p]
        if len(parts) < 2:
            return None
        owner, repo = parts[0], parts[1]
        if repo.endswith('.git'):
            repo = repo[:-4]
        if not (_SAFE_PATH_SEGMENT.match(owner) and _SAFE_PATH_SEGMENT.match(repo)):
            return None

        headers = {'User-Agent': _USER_AGENT, 'Accept': 'application/vnd.github+json'}
        if GITHUB_TOKEN:
            headers['Authorization'] = f'Bearer {GITHUB_TOKEN}'

        repo_resp = requests.get(f'https://api.github.com/repos/{owner}/{repo}',
                                  headers=headers, timeout=_DEFAULT_TIMEOUT)
        if repo_resp.status_code != 200:
            return None
        info = repo_resp.json()

        readme_text = ''
        readme_resp = requests.get(
            f'https://api.github.com/repos/{owner}/{repo}/readme',
            headers={**headers, 'Accept': 'application/vnd.github.raw+json'},
            timeout=_DEFAULT_TIMEOUT,
        )
        if readme_resp.status_code == 200:
            readme_text = readme_resp.text[:3000]

        summary_lines = [
            f"Repository: {owner}/{repo}",
            f"Description: {info.get('description') or '(none)'}",
            f"Primary language: {info.get('language') or 'unknown'}",
        ]
        if info.get('topics'):
            summary_lines.append(f"Topics: {', '.join(info['topics'])}")
        if readme_text:
            summary_lines.append(f"README (excerpt):\n{readme_text}")
        return '\n'.join(summary_lines)
    except Exception:
        return None


def is_figma_url(url):
    if not url:
        return False
    try:
        host = urlparse(url).hostname or ''
    except ValueError:
        return False
    return host in ('figma.com', 'www.figma.com')
