"""YouTube Data API v3 search, used to auto-surface real tutorial videos for Skills
lessons — the same idea Geeg uses for its lesson videos, adapted to Nelavista's
admin-curated (not per-student AI-generated) Lesson model: results are fetched once per
lesson and cached on it (see Lesson.videos in models.py), not refetched per student.

Reuses the same YOUTUBE_API_KEY config already declared for routes/video_routes.py's
(currently unused) /api/youtube/search endpoint, rather than adding a second config var.
"""
import html
import requests
from config import YOUTUBE_API_KEY

SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'


def build_lesson_video_query(skill_name, lesson_title):
    """One shared query-builder so a lesson's video and its written content are always
    searched for the same specific topic, not a generic skill-wide one. Lesson title leads
    (it's the actual topic), skill name disambiguates it, 'tutorial' steers away from vlogs
    and news clips toward the same kind of educational content Geeg's search targets."""
    return f'{lesson_title} {skill_name} tutorial'


def search_youtube_videos(query, max_results=3):
    """Best-effort search for embeddable, education-category videos. Returns [] — never
    raises — when the API key isn't configured or the request fails, so a missing key
    degrades to 'no videos shown' instead of breaking the lesson page."""
    if not (YOUTUBE_API_KEY and query):
        return []

    params = {
        'key': YOUTUBE_API_KEY,
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

    try:
        resp = requests.get(SEARCH_URL, params=params, timeout=8)
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, ValueError):
        return []

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
