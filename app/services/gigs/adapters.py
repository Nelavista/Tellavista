"""Provider adapters. Each one turns a provider's API/feed into NormalizedGig objects:

    fetch_gigs()        -> list of raw items (one HTTP call or a few pages, server-side)
    normalize_gig(raw)  -> NormalizedGig, or None to skip it (not a gig, not open to
                           Nigerian students, missing an application link...)
    get_status(ids)     -> {source_gig_id: 'OPEN'|'CLOSED'|'UNKNOWN'} for gigs that were
                           missing from this fetch. Only adapters whose provider has a
                           status endpoint answer anything but UNKNOWN.

Adding a source = subclass ProviderAdapter, set `key`, register it in ADAPTERS, then
create a GigProvider row in the admin with that adapter. A provider whose terms don't
permit redistribution is never added: there is deliberately no HTML scraper adapter.

Credentials: GigProvider.credentials_env names an environment variable. The key is
read from the environment at sync time and is never stored in the database or sent
to a browser.
"""
import json
import logging
import os
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime, date, timezone

import requests

from app.services.gigs import core
from app.utils.validation import safe_external_url

logger = logging.getLogger('nelavista.gigs.sync')

USER_AGENT = 'NelavistaGigSync/1.0 (+https://nelavista.com)'
MAX_RESPONSE_BYTES = 8 * 1024 * 1024
HTTP_TIMEOUT = 20


class ProviderError(Exception):
    """A fetch failed (network, HTTP status, bad payload). The sync records it and keeps
    every existing gig as it was."""


@dataclass
class NormalizedGig:
    source_gig_id: str
    title: str
    organization: str
    application_url: str
    source_url: str = None
    description: str = None
    summary: str = None
    requirements: str = None
    eligibility: str = None
    category: str = 'other'
    skills: list = field(default_factory=list)
    pay_min: int = None
    pay_max: int = None
    currency: str = None
    pay_type: str = 'not_stated'
    pay_text: str = None
    work_type: str = None
    location_type: str = 'remote'
    location: str = None
    posted_at: datetime = None
    deadline: date = None
    status: str = 'OPEN'          # what the source says right now: OPEN | CLOSED | UNKNOWN
    organization_logo_url: str = None
    external_reference: str = None
    raw: dict = None

    def as_fields(self):
        d = asdict(self)
        d.pop('raw', None)
        d.pop('status', None)
        d.pop('source_gig_id', None)
        d['skills_json'] = json.dumps(d.pop('skills') or [])
        return d


# ---------------------------------------------------------------- parsing helpers

def parse_datetime(value):
    if not value:
        return None
    if isinstance(value, (int, float)):
        try:
            return datetime.utcfromtimestamp(value / 1000 if value > 10**11 else value)
        except (OverflowError, OSError, ValueError):
            return None
    text = str(value).strip()
    try:
        dt = datetime.fromisoformat(text.replace('Z', '+00:00'))
    except ValueError:
        dt = None
        try:
            from email.utils import parsedate_to_datetime
            dt = parsedate_to_datetime(text)
        except (TypeError, ValueError, IndexError):
            pass
        if dt is None:
            for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
                try:
                    dt = datetime.strptime(text[:19], fmt)
                    break
                except ValueError:
                    continue
    if dt is None:
        return None
    if dt.tzinfo:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


def parse_date(value):
    dt = parse_datetime(value)
    return dt.date() if dt else None


def parse_amount(value):
    if value in (None, ''):
        return None
    if isinstance(value, (int, float)):
        return int(value) if value > 0 else None
    text = str(value).lower().replace(',', '').strip()
    m = re.search(r'(\d+(?:\.\d+)?)\s*([km])?', text)
    if not m:
        return None
    n = float(m.group(1)) * {'k': 1000, 'm': 1_000_000}.get(m.group(2), 1)
    return int(n) if n > 0 else None


PERIOD_MAP = {
    'hour': 'hourly', 'hourly': 'hourly', 'hr': 'hourly', 'day': 'daily', 'daily': 'daily', 'week': 'weekly',
    'weekly': 'weekly', 'month': 'monthly', 'monthly': 'monthly', 'year': 'yearly', 'yearly': 'yearly',
    'annual': 'yearly', 'annually': 'yearly', 'project': 'fixed', 'fixed': 'fixed', 'task': 'per_task',
}

WORK_TYPE_MAP = {
    'contract': 'contract', 'contractor': 'contract', 'freelance': 'freelance', 'freelancer': 'freelance',
    'part-time': 'part_time', 'part_time': 'part_time', 'part time': 'part_time', 'full-time': 'full_time',
    'full_time': 'full_time', 'full time': 'full_time', 'internship': 'internship', 'intern': 'internship',
    'temporary': 'project', 'temp': 'project', 'project': 'project', 'gig': 'project', 'one-off': 'project',
}


def as_list(value):
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [str(v) for v in value if v not in (None, '')]
    return [s.strip() for s in str(value).split(',') if s.strip()]


def dig(obj, path):
    """dig({'a': {'b': [1]}}, 'a.b') -> [1]. Missing keys -> None."""
    if not path:
        return obj
    for part in str(path).split('.'):
        if isinstance(obj, dict):
            obj = obj.get(part)
        elif isinstance(obj, list) and part.isdigit() and int(part) < len(obj):
            obj = obj[int(part)]
        else:
            return None
    return obj


def trim_raw(raw, max_len=4000):
    try:
        text = json.dumps(raw, default=str)
    except (TypeError, ValueError):
        return None
    return text[:max_len]


# ---------------------------------------------------------------- base adapter

class ProviderAdapter:
    key = ''
    label = ''
    description = ''
    # The provider's feed lists every gig it currently has open, so a gig missing from a
    # complete, non-empty fetch has closed. False for feeds that only show recent items.
    absence_means_closed = False
    # Terms-driven floor on how often Nelavista may poll this provider.
    min_interval_minutes = 60
    syncable = True

    def __init__(self, provider, http=None):
        self.provider = provider
        self.config = provider.config if provider else {}
        self.http = http or requests.Session()

    # -- the three adapter operations
    def fetch_gigs(self):
        raise NotImplementedError

    def normalize_gig(self, raw):
        raise NotImplementedError

    def get_status(self, source_gig_ids):
        return {sid: 'UNKNOWN' for sid in source_gig_ids}

    # -- shared helpers
    def credential(self):
        env = (self.provider.credentials_env or '').strip() if self.provider else ''
        return os.environ.get(env) if env else None

    def request_json(self, url, params=None):
        from app.services.link_fetch_service import _is_safe_url
        if not url or not _is_safe_url(url):
            raise ProviderError(f"Couldn't resolve the host, or it points at a private address (not called): {url!r}")
        headers = {'User-Agent': USER_AGENT, 'Accept': 'application/json'}
        params = dict(params or {})
        key = self.credential()
        method = self.provider.auth_method if self.provider else 'none'
        if method != 'none' and not key:
            raise ProviderError(f'Missing credential: set the {self.provider.credentials_env or "?"} environment variable.')
        if method == 'bearer':
            headers['Authorization'] = f'Bearer {key}'
        elif method == 'api_key_header':
            headers[self.provider.auth_param or 'X-API-Key'] = key
        elif method == 'query_param':
            params[self.provider.auth_param or 'api_key'] = key
        try:
            resp = self.http.get(url, params=params, headers=headers, timeout=HTTP_TIMEOUT, stream=True)
        except requests.RequestException as e:
            raise ProviderError(f'Network error: {e.__class__.__name__}') from e
        try:
            if resp.status_code == 429:
                raise ProviderError(f'Rate limited by the provider (429). Retry-After: {resp.headers.get("Retry-After", "?")}')
            if resp.status_code >= 400:
                raise ProviderError(f'Provider returned HTTP {resp.status_code}')
            body = resp.raw.read(MAX_RESPONSE_BYTES + 1, decode_content=True) if hasattr(resp, 'raw') and resp.raw else resp.content
            if len(body) > MAX_RESPONSE_BYTES:
                raise ProviderError('Provider response is too large.')
            try:
                return json.loads(body)
            except ValueError as e:
                raise ProviderError('Provider response is not valid JSON.') from e
        finally:
            try:
                resp.close()
            except Exception:
                pass

    def nigeria_filter_skips(self, location, location_type):
        """Skip gigs a Nigerian student plainly can't take (e.g. 'USA only') unless the
        provider's config turns this off. Unknown eligibility is kept."""
        if self.config.get('nigeria_eligible_only', True) is False:
            return False
        return core.open_to_nigeria(location, location_type) is False


# ---------------------------------------------------------------- Jobicy

class JobicyAdapter(ProviderAdapter):
    """Jobicy's public remote-jobs API (jobicy.com/api/jobs). Its fair-use terms allow
    showing listings in other products if Jobicy is credited and the canonical Jobicy
    job URL is kept. Polling no more than hourly. The feed covers recent jobs only, so a
    job missing from it isn't necessarily closed; the /status endpoint answers that
    (closed only on an explicit 'closed')."""
    key = 'jobicy'
    label = 'Jobicy remote jobs API'
    description = 'Public JSON API. Credit Jobicy, keep the Jobicy job URL, poll at most hourly.'
    absence_means_closed = False
    min_interval_minutes = 60
    DEFAULT_URL = 'https://jobicy.com/api/jobs'
    # Gigs, not salaried jobs: by default only contract/freelance/part-time/temporary/
    # internship listings come in. Add "full-time" in the provider config to widen it.
    DEFAULT_JOB_TYPES = ['contract', 'freelance', 'part-time', 'part_time', 'temporary', 'internship']

    def _base(self):
        return (self.provider.api_base_url or self.DEFAULT_URL).rstrip('/')

    def fetch_gigs(self):
        params = {'count': int(self.config.get('count', 100))}
        for k in ('industry', 'geo', 'tag'):
            if self.config.get(k):
                params[k] = self.config[k]
        items = []
        pages = max(1, min(int(self.config.get('max_pages', 1)), 5))
        cursor_param = self.config.get('cursor_param', 'cursor')
        for _ in range(pages):
            data = self.request_json(self._base(), params)
            jobs = data.get('jobs') if isinstance(data, dict) else None
            if not isinstance(jobs, list):
                raise ProviderError('Unexpected Jobicy response: no "jobs" list.')
            items.extend(jobs)
            nxt = data.get('nextCursor')
            if not (data.get('hasMore') and nxt):
                break
            params[cursor_param] = nxt
        return items

    def normalize_gig(self, raw):
        if not isinstance(raw, dict):
            return None
        sid = raw.get('id')
        url = safe_external_url(raw.get('url'))
        title = (raw.get('jobTitle') or raw.get('title') or '').strip()
        org = (raw.get('companyName') or raw.get('company') or '').strip()
        if not sid or not url or not title or not org:
            return None
        job_types = [t.lower().strip() for t in as_list(raw.get('jobType'))]
        allowed = [t.lower() for t in self.config.get('job_types', self.DEFAULT_JOB_TYPES)]
        if allowed and job_types and not any(t in allowed for t in job_types):
            return None
        work_type = next((WORK_TYPE_MAP[t] for t in job_types if t in WORK_TYPE_MAP), None)
        location = (', '.join(as_list(raw.get('jobGeo'))) or None)
        if self.nigeria_filter_skips(location, 'remote'):
            return None
        industries = as_list(raw.get('jobIndustry'))
        excerpt = core.html_to_text(raw.get('jobExcerpt'), 600)
        description = core.html_to_text(raw.get('jobDescription'))
        period = PERIOD_MAP.get(str(raw.get('salaryPeriod') or '').lower().strip(), None)
        pay_min, pay_max = parse_amount(raw.get('salaryMin')), parse_amount(raw.get('salaryMax'))
        return NormalizedGig(
            source_gig_id=str(sid), title=title[:200], organization=org[:150],
            application_url=url, source_url=url,
            description=description, summary=core.summarize(excerpt or description),
            category=core.infer_category(' '.join(industries), title),
            skills=core.extract_skills(title, ' '.join(industries), excerpt or ''),
            pay_min=pay_min, pay_max=pay_max,
            currency=(str(raw.get('salaryCurrency') or '').upper()[:10] or None) if (pay_min or pay_max) else None,
            pay_type=(period or 'yearly') if (pay_min or pay_max) else 'not_stated',
            work_type=work_type, location_type='remote', location=location,
            eligibility=(f'Open to candidates in: {location}' if location else None),
            posted_at=parse_datetime(raw.get('pubDate')),
            status='OPEN',  # it is in Jobicy's active feed right now
            organization_logo_url=safe_external_url(raw.get('companyLogo')),
            raw=raw,
        )

    def get_status(self, source_gig_ids):
        out = {sid: 'UNKNOWN' for sid in source_gig_ids}
        ids = list(source_gig_ids)
        url = self.config.get('status_url') or (self._base() + '/status')
        for i in range(0, len(ids), 100):
            batch = ids[i:i + 100]
            try:
                data = self.request_json(url, {'ids': ','.join(batch)})
            except ProviderError as e:
                logger.warning('Jobicy status check failed: %s', e)
                continue
            for sid, st in _iter_status_pairs(data):
                if sid in out:
                    out[sid] = {'active': 'OPEN', 'open': 'OPEN', 'closed': 'CLOSED', 'expired': 'CLOSED'}.get(st, 'UNKNOWN')
        return out


def _iter_status_pairs(data):
    """Tolerant reader for a status response: {"jobs": [{"id":1,"status":"closed"}]},
    {"results": {...}}, {"statuses": {"1": "active"}} or a bare mapping."""
    container = data
    if isinstance(data, dict):
        for key in ('jobs', 'results', 'statuses', 'data'):
            if key in data:
                container = data[key]
                break
    if isinstance(container, list):
        for row in container:
            if isinstance(row, dict) and row.get('id') is not None:
                yield str(row['id']), str(row.get('status') or '').lower()
    elif isinstance(container, dict):
        for k, v in container.items():
            if isinstance(v, dict):
                v = v.get('status')
            if isinstance(v, str):
                yield str(k), v.lower()


# ---------------------------------------------------------------- generic JSON feed

class JsonFeedAdapter(ProviderAdapter):
    """Any provider or partner that offers a JSON API/feed, configured without code.

    config_json example:
      {"items_path": "data.gigs", "absence_means_closed": true,
       "fields": {"source_gig_id": "id", "title": "title", "organization": "company.name",
                  "description": "description", "category": "category", "skills": "skills",
                  "pay_min": "budget.min", "pay_max": "budget.max", "currency": "budget.currency",
                  "pay_type": "budget.type", "pay_text": "budget.text", "work_type": "type",
                  "location": "location", "remote": "is_remote", "application_url": "apply_url",
                  "source_url": "url", "posted_at": "created_at", "deadline": "deadline",
                  "status": "status"},
       "status_map": {"open": "OPEN", "active": "OPEN", "closed": "CLOSED", "filled": "CLOSED"},
       "defaults": {"organization": "Acme", "category": "design", "currency": "NGN"}}
    """
    key = 'json_feed'
    label = 'Generic JSON API / feed'
    description = 'Field-mapped JSON. For official provider APIs and direct partner feeds.'
    min_interval_minutes = 30

    @property
    def absence_means_closed(self):
        return bool(self.config.get('absence_means_closed', False))

    def fetch_gigs(self):
        data = self.request_json(self.provider.api_base_url, self.config.get('params') or {})
        items = dig(data, self.config.get('items_path')) if self.config.get('items_path') else data
        if not isinstance(items, list):
            raise ProviderError('items_path does not point at a list in the response.')
        return items

    def _get(self, raw, name):
        path = (self.config.get('fields') or {}).get(name)
        value = dig(raw, path) if path else None
        if value in (None, ''):
            value = (self.config.get('defaults') or {}).get(name)
        return value

    def normalize_gig(self, raw):
        if not isinstance(raw, dict):
            return None
        sid = self._get(raw, 'source_gig_id')
        title = str(self._get(raw, 'title') or '').strip()
        org = str(self._get(raw, 'organization') or '').strip()
        app_url = safe_external_url(self._get(raw, 'application_url'))
        src_url = safe_external_url(self._get(raw, 'source_url')) or app_url
        if not sid or not title or not org or not app_url:
            return None
        raw_status = str(self._get(raw, 'status') or '').lower().strip()
        status_map = {k.lower(): v for k, v in (self.config.get('status_map') or {}).items()}
        status = status_map.get(raw_status, 'OPEN' if not raw_status else 'UNKNOWN')
        remote_flag = self._get(raw, 'remote')
        location = str(self._get(raw, 'location') or '').strip() or None
        if isinstance(remote_flag, bool):
            location_type = 'remote' if remote_flag else 'onsite'
        else:
            lt = str(self._get(raw, 'location_type') or '').lower()
            location_type = lt if lt in core.LOCATION_TYPE_KEYS else ('remote' if not location or 'remote' in location.lower() else 'onsite')
        if self.nigeria_filter_skips(location, location_type):
            return None
        description = core.html_to_text(self._get(raw, 'description'))
        category = str(self._get(raw, 'category') or '').strip().lower().replace(' ', '_')
        if category not in core.CATEGORY_KEYS:
            category = core.infer_category(category, title)
        skills = [s[:40] for s in as_list(self._get(raw, 'skills'))][:15] or core.extract_skills(title, description or '')
        pay_min, pay_max = parse_amount(self._get(raw, 'pay_min')), parse_amount(self._get(raw, 'pay_max'))
        pay_type = PERIOD_MAP.get(str(self._get(raw, 'pay_type') or '').lower(), None)
        work_raw = str(self._get(raw, 'work_type') or '').lower().strip()
        return NormalizedGig(
            source_gig_id=str(sid)[:120], title=title[:200], organization=org[:150],
            application_url=app_url, source_url=src_url, description=description,
            summary=core.summarize(self._get(raw, 'summary') or description),
            requirements=core.html_to_text(self._get(raw, 'requirements')),
            eligibility=core.html_to_text(self._get(raw, 'eligibility'), 2000),
            category=category, skills=skills, pay_min=pay_min, pay_max=pay_max,
            currency=(str(self._get(raw, 'currency') or '').upper()[:10] or None),
            pay_type=pay_type or ('fixed' if (pay_min or pay_max) else 'not_stated'),
            pay_text=(str(self._get(raw, 'pay_text'))[:120] if self._get(raw, 'pay_text') else None),
            work_type=WORK_TYPE_MAP.get(work_raw), location_type=location_type, location=location,
            posted_at=parse_datetime(self._get(raw, 'posted_at')), deadline=parse_date(self._get(raw, 'deadline')),
            status=status, organization_logo_url=safe_external_url(self._get(raw, 'logo_url')),
            external_reference=(str(self._get(raw, 'external_reference'))[:200] if self._get(raw, 'external_reference') else None),
            raw=raw,
        )


# ---------------------------------------------------------------- RSS / Atom

class RssFeedAdapter(ProviderAdapter):
    """An official RSS/Atom feed that a provider publishes for redistribution. Feeds
    usually carry only recent items, so absence never closes a gig by default."""
    key = 'rss_feed'
    label = 'Official RSS / Atom feed'
    description = 'For providers that publish an official feed and permit its reuse.'
    min_interval_minutes = 60

    @property
    def absence_means_closed(self):
        return bool(self.config.get('absence_means_closed', False))

    def fetch_gigs(self):
        from app.services.link_fetch_service import _is_safe_url
        url = self.provider.api_base_url
        if not url or not _is_safe_url(url):
            raise ProviderError('Feed URL is missing or unsafe.')
        try:
            resp = self.http.get(url, headers={'User-Agent': USER_AGENT}, timeout=HTTP_TIMEOUT)
        except requests.RequestException as e:
            raise ProviderError(f'Network error: {e.__class__.__name__}') from e
        if resp.status_code >= 400:
            raise ProviderError(f'Feed returned HTTP {resp.status_code}')
        if len(resp.content) > MAX_RESPONSE_BYTES:
            raise ProviderError('Feed is too large.')
        return parse_feed(resp.content)

    def normalize_gig(self, raw):
        link = safe_external_url(raw.get('link'))
        title = (raw.get('title') or '').strip()
        org = (raw.get('author') or self.config.get('organization') or self.provider.name or '').strip()
        if not link or not title:
            return None
        description = core.html_to_text(raw.get('description'))
        return NormalizedGig(
            source_gig_id=(raw.get('guid') or link)[:120], title=title[:200], organization=org[:150],
            application_url=link, source_url=link, description=description, summary=core.summarize(description),
            category=self.config.get('category') if self.config.get('category') in core.CATEGORY_KEYS
            else core.infer_category(' '.join(raw.get('categories') or []), title),
            skills=core.extract_skills(title, ' '.join(raw.get('categories') or [])),
            location_type=self.config.get('location_type', 'remote'), location=self.config.get('location'),
            posted_at=parse_datetime(raw.get('published')), status='OPEN', raw=raw,
        )


def parse_feed(content):
    """RSS 2.0 or Atom -> [{'title','link','guid','description','published','categories','author'}].
    Uses defusedxml when installed. Python's expat already refuses entity-expansion
    bombs, and DTDs/external entities aren't resolved by ElementTree."""
    try:
        from defusedxml import ElementTree as ET  # type: ignore
    except ImportError:
        import xml.etree.ElementTree as ET
    try:
        root = ET.fromstring(content)
    except Exception as e:
        raise ProviderError('Feed is not valid XML.') from e

    def local(tag):
        return tag.rsplit('}', 1)[-1] if isinstance(tag, str) else ''

    def text_of(el, name):
        for child in el:
            if local(child.tag) == name:
                return (child.text or '').strip()
        return None

    items = []
    for el in root.iter():
        kind = local(el.tag)
        if kind not in ('item', 'entry'):
            continue
        link = text_of(el, 'link')
        if kind == 'entry' or not link:
            for child in el:
                if local(child.tag) == 'link' and child.get('href'):
                    link = child.get('href')
                    break
        items.append({
            'title': text_of(el, 'title'), 'link': link,
            'guid': text_of(el, 'guid') or text_of(el, 'id'),
            'description': text_of(el, 'description') or text_of(el, 'summary') or text_of(el, 'content'),
            'published': text_of(el, 'pubDate') or text_of(el, 'published') or text_of(el, 'updated'),
            'categories': [(c.text or c.get('term') or '').strip() for c in el if local(c.tag) == 'category'],
            'author': text_of(el, 'creator') or text_of(el, 'author'),
        })
    return items


class ManualAdapter(ProviderAdapter):
    """Gigs an admin adds by hand (and, later, direct partner gigs). Nothing to fetch."""
    key = 'manual'
    label = 'Manual (added by Nelavista admins)'
    description = 'No sync. Admins add and re-verify these gigs.'
    syncable = False

    def fetch_gigs(self):
        return []

    def normalize_gig(self, raw):
        return None


ADAPTERS = {cls.key: cls for cls in (JobicyAdapter, JsonFeedAdapter, RssFeedAdapter, ManualAdapter)}


def get_adapter(provider, http=None):
    cls = ADAPTERS.get(provider.adapter)
    if not cls:
        raise ProviderError(f'No adapter named {provider.adapter!r}.')
    return cls(provider, http=http)
