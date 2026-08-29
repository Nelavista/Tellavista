"""YouTube Data API v3 search, used to auto-surface real tutorial videos for Skills
lessons and Academia topics — the same idea Geeg uses for its lesson videos, adapted to
Nelavista's admin-curated (not per-student AI-generated) Lesson/Topic models: results
are fetched once per lesson/topic and cached on it (see Lesson.videos / Topic.videos in
models.py), not refetched per student.

Reuses the same YOUTUBE_API_KEY config already declared for routes/video_routes.py's
(unrelated, Campus-Videos-feature) /api/youtube/search endpoint, rather than adding a
second config var or a second YouTube integration.
"""
import html
import requests
from config import YOUTUBE_API_KEY, YOUTUBE_API_KEY_2

SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'

_API_KEYS = [k for k in (YOUTUBE_API_KEY, YOUTUBE_API_KEY_2) if k]


def build_lesson_video_query(skill_name, lesson_title):
    """One shared query-builder so a lesson's video and its written content are always
    searched for the same specific topic, not a generic skill-wide one. Lesson title leads
    (it's the actual topic), skill name disambiguates it, 'tutorial' steers away from vlogs
    and news clips toward the same kind of educational content Geeg's search targets."""
    return f'{lesson_title} {skill_name} tutorial'


def build_topic_video_query(course_code, course_title, topic_title):
    """Same idea as build_lesson_video_query, for an Academia Topic: topic leads (it's
    the actual thing being taught), course code+title disambiguate which course's
    version of the topic this is (e.g. 'Linked Lists CSC213' rather than a generic CS
    result), 'tutorial' steers toward educational content."""
    return f'{topic_title} {course_code} {course_title} tutorial'


def search_youtube_videos(query, max_results=3):
    """Best-effort search for embeddable, education-category videos.

    Returns a list (possibly []) when we got a real answer from YouTube -- [] means
    "searched, genuinely found nothing", safe to cache as a confirmed result. Returns
    None -- never [] -- when no key is configured, or every configured key failed
    (quota-exceeded, network error, etc.): this is "couldn't determine, try again
    later", and callers MUST NOT cache a None result as if it were a confirmed empty
    search (see models.Topic.videos / models.Lesson.videos' None-vs-[] contract).

    Tries YOUTUBE_API_KEY_2 (a second Google Cloud project, if configured) after
    YOUTUBE_API_KEY hits its daily search.list quota -- YouTube's quota is per-project,
    so a second real project gets its own separate daily allowance. A single key with
    no YOUTUBE_API_KEY_2 configured behaves exactly as before this fallback existed.
    """
    if not (_API_KEYS and query):
        return None

    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': max_results,
        'safeSearch': 'strict',
        'videoEmbeddable': 'true',
        'relevanceLanguage': 'en',
        'order': 'relevance',
        'videoCategoryId': '27',  # Education
    }

    data = None
    for key in _API_KEYS:
        try:
            resp = requests.get(SEARCH_URL, params={**params, 'key': key}, timeout=8)
        except requests.RequestException:
            continue  # network error on this key -- try the next one
        if resp.status_code == 429:
            continue  # this key's daily quota is exhausted -- try the next one
        try:
            resp.raise_for_status()
            data = resp.json()
        except (requests.RequestException, ValueError):
            continue
        break  # got a real response

    if data is None:
        return None  # every configured key failed -- unknown, not "no results"

    videos = []
    for item in data.get('items', []):
        video_id = (item.get('id') or {}).get('videoId')
        snippet = item.get('snippet') or {}
        if not video_id:
            continue
        videos.append({
            'video_id': video_id,
            # YouTube's search endpoint sometimes returns titles with HTML entities
            # already encoded (e.g. "I&#39;d") — unescape so Jinja's own autoescaping
            # doesn't double-encode them into "I&amp;#39;d".
            'title': html.unescape(snippet.get('title', '')),
            'channel': html.unescape(snippet.get('channelTitle', '')),
            'thumbnail': ((snippet.get('thumbnails') or {}).get('medium') or {}).get('url', ''),
        })
    return videos
