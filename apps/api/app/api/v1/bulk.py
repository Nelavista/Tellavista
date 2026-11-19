"""Bulk actions: one request, many records, an honest per-record report.

Every ops surface that edits a record grew the same need once real queues existed
-- a reviewer clearing twenty submissions one POST at a time, an editor publishing
a whole lesson set, money approving a batch run. The pattern here is deliberately
boring, because the failures are what matter:

* A bulk call never hides a refusal. The answer carries `applied`, `unchanged`
  and a row per failure with the same `code`/`message` the single-record endpoint
  would have returned, so the admin UI can show exactly which ids did not take.
* One bad id does not abort the rest. A batch of twenty where one was already
  reviewed applies nineteen and reports the twentieth -- retrying the whole batch
  would otherwise re-audit nineteen records.
* Duplicate ids are collapsed. A UI that sends an id twice must not perform the
  action twice, which for a money or quality decision means a second audit row.
* Nothing here commits: the caller owns the transaction, so a bulk action is one
  unit of work exactly like the single-record version.
"""
from __future__ import annotations

from collections.abc import Callable
from typing import Literal

from pydantic import BaseModel, Field

from app.core.errors import ApiError

Outcome = Literal["applied", "unchanged"]

# An action returns "unchanged" when the record was already in the requested
# state; anything else (including None) counts as a change.
BulkAction = Callable[[int], Outcome | None]


class BulkFailureOut(BaseModel):
    id: int
    code: str
    message: str


class BulkResultOut(BaseModel):
    requested: int
    applied: int
    unchanged: int
    failed: list[BulkFailureOut] = Field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failed


class BulkIdsIn(BaseModel):
    """The shared shape for "do this to these ids".

    `max_length` is the anti-accident guard: a caller that sends a whole table by
    mistake is refused rather than issuing ten thousand audits in one request.
    """

    ids: list[int] = Field(min_length=1, max_length=200)


def apply_bulk(ids: list[int], action: BulkAction) -> BulkResultOut:
    seen: list[int] = []
    for value in ids:
        if value not in seen:
            seen.append(value)

    applied = 0
    unchanged = 0
    failed: list[BulkFailureOut] = []

    for value in seen:
        try:
            outcome = action(value)
        except ApiError as exc:
            # The record's own refusal, reported against its id. Anything else is
            # a bug and must surface as a 500 rather than be swallowed per-row.
            failed.append(BulkFailureOut(id=value, code=exc.code, message=exc.message))
            continue
        if outcome == "unchanged":
            unchanged += 1
        else:
            applied += 1

    return BulkResultOut(
        requested=len(seen),
        applied=applied,
        unchanged=unchanged,
        failed=failed,
    )


__all__ = ["BulkAction", "BulkFailureOut", "BulkIdsIn", "BulkResultOut", "Outcome", "apply_bulk"]
