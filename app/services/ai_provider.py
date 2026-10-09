"""Provider-agnostic AI layer (PRD §6): one interface, swappable vendors.

Every AI call previously went through ~20 copy-pasted
`requests.post("https://openrouter.ai/api/v1/chat/completions", ...)` blocks, each with
its own headers/payload/error handling. This module replaces that duplication with:

    AIProvider (interface)
    ├── OpenRouterProvider   -- current behaviour, byte-for-byte compatible
    └── (extensible: a GeminiProvider etc. only has to implement chat())

...so a vendor switch is a config change, not a 20-site refactor. Callers keep their
own prompts/models; they just stop owning transport.

Design constraints honoured from the codebase:
- Never raises into a caller that has its own fallback path -- chat() returns the
  parsed `choices[0].message.content` or raises AIProviderError; stream_chat() mirrors
  tutor_service's existing SSE-parsing contract exactly (fallback-string on failure),
  so routes/tutor_routes.py's behaviour is unchanged.
- Existing tests patch `app.services.ai_grading.requests.post` and
  `app.services.tutor_service.*` module attributes -- those modules keep their own
  `requests` imports until migrated, so nothing breaks.
- API keys only ever read server-side from env (PRD §7).
"""
import json
import logging
import time
from abc import ABC, abstractmethod

import requests

from app.config import OPENROUTER_API_KEY

logger = logging.getLogger(__name__)

OPENROUTER_CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_EMBEDDINGS_URL = "https://openrouter.ai/api/v1/embeddings"

DEFAULT_HEADERS = {
    "HTTP-Referer": "https://nelavista.com",
    "X-Title": "Nelavista",
}


class AIProviderError(RuntimeError):
    """Raised when a provider call fails (network, non-200, unparseable). Callers with
    a fallback path catch this; callers without it let it surface like the old
    raise-on-failure behaviour."""


class AIProvider(ABC):
    """The PRD's provider interface: chat completion + streaming + embeddings."""

    name = 'abstract'

    @abstractmethod
    def chat(self, messages, model, *, temperature=0.5, max_tokens=1000, timeout=60,
             response_json=False):
        """One non-streamed chat completion. Returns the assistant message content
        string. Raises AIProviderError on failure."""

    @abstractmethod
    def stream_chat(self, messages, model, *, temperature=0.5, max_tokens=1000, timeout=120):
        """Generator of incremental text deltas. On total failure yields a single
        user-facing fallback string (never raises mid-stream)."""

    @abstractmethod
    def embed(self, texts, model):
        """Embed a list of texts; returns a list of float vectors. Raises
        AIProviderError on failure."""


class OpenRouterProvider(AIProvider):
    """OpenRouter's OpenAI-compatible API -- what every call site uses today."""

    name = 'openrouter'

    def __init__(self, api_key=None):
        # Resolved lazily-ish here so a test can inject a fake key; unset key is not an
        # error until a call actually needs it (same tolerate-unset-config posture as
        # the rest of the app).
        self.api_key = api_key or OPENROUTER_API_KEY

    def _headers(self, title):
        if not self.api_key:
            raise AIProviderError('OPENROUTER_API_KEY is not configured')
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            **DEFAULT_HEADERS,
            "X-Title": title,
        }

    def chat(self, messages, model, *, temperature=0.5, max_tokens=1000, timeout=60,
             response_json=False, feature=None, user_id=None):
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if response_json:
            payload["response_format"] = {"type": "json_object"}
        try:
            response = requests.post(
                OPENROUTER_CHAT_URL, headers=self._headers("Nelavista"),
                json=payload, timeout=timeout,
            )
        except requests.exceptions.RequestException as e:
            self._log_usage(user_id, feature, model, None, None, ok=False)
            raise AIProviderError(f'AI request failed: {e}') from e
        except Exception as e:   # misconfigured envs raise odd things; keep the contract
            self._log_usage(user_id, feature, model, None, None, ok=False)
            raise AIProviderError(f'AI request failed: {e}') from e
        if response.status_code != 200:
            self._log_usage(user_id, feature, model, None, None, ok=False)
            raise AIProviderError(f'AI API error: {response.status_code}')
        try:
            data = response.json()
            self._log_usage_from_payload(user_id, feature, model, data, ok=True)
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, ValueError) as e:
            raise AIProviderError(f'Unexpected AI response shape: {e}') from e

    def stream_chat(self, messages, model, *, temperature=0.5, max_tokens=1000, timeout=120):
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }
        fallback = "I'm having trouble reaching the tutor right now — please try again in a moment."
        retryable_statuses = {408, 425, 429, 500, 502, 503, 504}
        got_any = False
        for attempt in range(3):
            response = None
            try:
                response = requests.post(
                    OPENROUTER_CHAT_URL, headers=self._headers("Nelavista AI Tutor"),
                    json=payload, stream=True, timeout=timeout,
                )
            except AIProviderError as exc:
                logger.error("Tutor provider is not configured: %s", exc)
                yield fallback
                return
            except requests.exceptions.RequestException as exc:
                logger.warning("Tutor provider request failed (attempt %s/3): %s", attempt + 1, exc)
                if attempt < 2:
                    time.sleep(0.5 * (attempt + 1))
                    continue
                yield fallback
                return

            if response.status_code != 200:
                status = response.status_code
                response.close()
                logger.warning("Tutor provider returned HTTP %s", status)
                if status in retryable_statuses and attempt < 2:
                    time.sleep(0.5 * (attempt + 1))
                    continue
                yield fallback
                return

            # Force UTF-8 before decode_unicode -- OpenRouter streams declare no charset.
            response.encoding = 'utf-8'
            try:
                for raw_line in response.iter_lines(decode_unicode=True):
                    if not raw_line or not raw_line.startswith('data: '):
                        continue
                    data = raw_line[len('data: '):].strip()
                    if data == '[DONE]':
                        break
                    try:
                        obj = json.loads(data)
                    except ValueError:
                        continue
                    choices = obj.get('choices') or []
                    if not choices:
                        continue
                    delta = (choices[0].get('delta') or {}).get('content')
                    if delta:
                        got_any = True
                        yield delta
                break
            except requests.exceptions.RequestException as exc:
                logger.warning("Tutor stream interrupted (attempt %s/3): %s", attempt + 1, exc)
                if not got_any and attempt < 2:
                    time.sleep(0.5 * (attempt + 1))
                    continue
                if not got_any:
                    yield fallback
                return
            finally:
                response.close()
        if not got_any:
            logger.warning("Tutor provider stream completed without any response content")
            yield "I'm having trouble responding right now — please try again."

    def embed(self, texts, model, *, timeout=60, feature='embeddings', user_id=None):
        if isinstance(texts, str):
            texts = [texts]
        try:
            response = requests.post(
                OPENROUTER_EMBEDDINGS_URL, headers=self._headers("Nelavista RAG"),
                json={"model": model, "input": texts}, timeout=timeout,
            )
        except requests.exceptions.RequestException as e:
            self._log_usage(user_id, feature, model, None, None, ok=False)
            raise AIProviderError(f'Embedding request failed: {e}') from e
        if response.status_code != 200:
            self._log_usage(user_id, feature, model, None, None, ok=False)
            raise AIProviderError(f'Embedding API error: {response.status_code}')
        try:
            data = response.json()
            self._log_usage_from_payload(user_id, feature, model, data, ok=True)
            # OpenAI-shaped: {"data": [{"embedding": [...], "index": n}, ...]}
            items = sorted(data["data"], key=lambda item: item.get("index", 0))
            return [item["embedding"] for item in items]
        except (KeyError, IndexError, ValueError, TypeError) as e:
            raise AIProviderError(f'Unexpected embedding response shape: {e}') from e

    @staticmethod
    def _log_usage(user_id, feature, model, prompt_tokens, completion_tokens, ok):
        """PRD §21 AI usage monitoring (gap G6). Best-effort by contract -- never
        raises into the AI call it measures. No app context (e.g. a bare test) skips
        logging rather than crashing."""
        try:
            from flask import has_app_context
            if not has_app_context():
                return
            from app.services.ai_monitoring import log_ai_usage
            from app.services import analytics
            log_ai_usage(user_id, feature or 'unattributed', model,
                         prompt_tokens=prompt_tokens,
                         completion_tokens=completion_tokens, ok=ok)
            # Product-analytics mirror of the same call (§21): aggregate counters only
            # -- never prompt/answer content. Keyed by user id here vs username on the
            # route-emitted events (two PostHog distinct_id namespaces; fine for MVP
            # volume/reliability aggregates). No-op without POSTHOG_API_KEY.
            analytics.capture(
                f'user:{user_id}' if user_id else 'anonymous',
                analytics.EVENT_AI_CALL,
                {'feature': feature or 'unattributed', 'model': model, 'ok': ok},
            )
        except Exception:
            pass

    def _log_usage_from_payload(self, user_id, feature, model, data, ok):
        usage = (data or {}).get('usage') or {}
        self._log_usage(user_id, feature, model,
                        prompt_tokens=usage.get('prompt_tokens'),
                        completion_tokens=usage.get('completion_tokens'), ok=ok)


_default_provider = None


def get_ai_provider():
    """Process-wide default provider. OpenRouter today; a vendor switch is:
        get_ai_provider = lambda: GeminiProvider(...)
    or reading AI_PROVIDER from env here, without touching any call site."""
    global _default_provider
    if _default_provider is None:
        _default_provider = OpenRouterProvider()
    return _default_provider


def set_ai_provider(provider):
    """Test/alt-vendor injection point."""
    global _default_provider
    _default_provider = provider
