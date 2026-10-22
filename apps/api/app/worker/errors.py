"""Job-handler errors.

The runner retries every exception with backoff. A `PermanentJobError` is the
exception to that: a bad request, a revoked key or a plan limit will not fix
itself, so the job is marked failed immediately and left for an operator.
"""
from __future__ import annotations


class PermanentJobError(Exception):
    """A handler failure that retrying cannot fix (bad config, 4xx)."""
