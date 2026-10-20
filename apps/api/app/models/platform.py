"""Platform settings: the switches ops can change without a deploy (G1–G5).

One row, id = 1. It holds the decisions that are policy rather than code:

* **G1** the billing and payout currencies, and which currencies are allowed,
* **G2** the payout second-approver threshold and the payout identity checks,
* **G3** the minimum working age and the age that needs guardian consent,
* **G4** who owns the curriculum and under which licence,
* **G5** the target launch date and the contributor terms in force.

`allowed_currencies` is a list so a new currency is a settings change, not a
migration. The `contributor_terms_body` is stored here (not in code) because it is
shown to students and must match the version they accepted.

Money stays integer minor units everywhere; this table never stores an amount in
major units and never stores a float.
"""
from __future__ import annotations

from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin
from app.models.admin import JSONPayload

SETTINGS_ID = 1

# A settings row is created with these values the first time it is read. They are
# also the migration's server defaults, so an existing database upgrades to the
# same state as a fresh one.
DEFAULT_BILLING_CURRENCY = "NGN"
DEFAULT_PAYOUT_CURRENCY = "NGN"
DEFAULT_ALLOWED_CURRENCIES: tuple[str, ...] = ("NGN", "USD", "GBP", "EUR", "GHS", "KES", "ZAR")
# NGN 50,000.00 in kobo: below this one approver is enough, above it a second
# person must approve, because a mistake at that size is expensive to reverse.
DEFAULT_SECOND_APPROVER_THRESHOLD_MINOR = 5_000_000
DEFAULT_MIN_STUDENT_AGE = 16
DEFAULT_GUARDIAN_CONSENT_BELOW_AGE = 18
DEFAULT_TERMS_VERSION = "2026-10-01"
DEFAULT_CONTRIBUTOR_TERMS_VERSION = "2026-10-01"
DEFAULT_CURRICULUM_OWNER = "Nelavista"
DEFAULT_CURRICULUM_LICENSE = "Nelavista Contributor Licence 1.0"

DEFAULT_CONTRIBUTOR_TERMS = (
    "Contributing work to Nelavista means the following.\n\n"
    "1. You do the work yourself. Subcontracting or reselling an assignment is not "
    "allowed, and a submission must be your own output.\n"
    "2. You may use the material you are given only for the assigned work. Do not "
    "share client data, task instructions or gold answers with anyone else.\n"
    "3. You keep ownership of the underlying skills you bring; you grant Nelavista "
    "a licence to deliver, review and improve the work you submit.\n"
    "4. Payment is per approved task at the rate shown on the assignment. A rejected "
    "or reworked task is reviewed again under the published quality standard.\n"
    "5. You can stop at any time. Work already approved is still paid.\n"
    "6. If you are under the guardian-consent age, a parent or guardian must agree "
    "before you accept paid work.\n"
)


class PlatformSettings(Base, TimestampMixin):
    """The single row of platform policy (see module docstring)."""

    __tablename__ = "platform_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=SETTINGS_ID)

    billing_currency: Mapped[str] = mapped_column(
        String(3), default=DEFAULT_BILLING_CURRENCY, nullable=False
    )
    payout_currency: Mapped[str] = mapped_column(
        String(3), default=DEFAULT_PAYOUT_CURRENCY, nullable=False
    )
    allowed_currencies: Mapped[list] = mapped_column(
        JSONPayload, default=lambda: list(DEFAULT_ALLOWED_CURRENCIES), nullable=False
    )

    payout_second_approver_threshold_minor: Mapped[int] = mapped_column(
        Integer, default=DEFAULT_SECOND_APPROVER_THRESHOLD_MINOR, nullable=False
    )
    # When true, even a small batch needs someone other than its creator.
    payout_second_approver_always: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    payout_require_verified_email: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )

    min_student_age: Mapped[int] = mapped_column(
        Integer, default=DEFAULT_MIN_STUDENT_AGE, nullable=False
    )
    guardian_consent_below_age: Mapped[int] = mapped_column(
        Integer, default=DEFAULT_GUARDIAN_CONSENT_BELOW_AGE, nullable=False
    )

    terms_version: Mapped[str] = mapped_column(
        String(20), default=DEFAULT_TERMS_VERSION, nullable=False
    )
    contributor_terms_version: Mapped[str] = mapped_column(
        String(20), default=DEFAULT_CONTRIBUTOR_TERMS_VERSION, nullable=False
    )
    contributor_terms_body: Mapped[str] = mapped_column(
        Text, default=DEFAULT_CONTRIBUTOR_TERMS, nullable=False
    )

    curriculum_owner: Mapped[str] = mapped_column(
        String(160), default=DEFAULT_CURRICULUM_OWNER, nullable=False
    )
    curriculum_license: Mapped[str] = mapped_column(
        String(80), default=DEFAULT_CURRICULUM_LICENSE, nullable=False
    )
    # "in_house" | "community" | "partner"
    curriculum_authoring_model: Mapped[str] = mapped_column(
        String(40), default="in_house", nullable=False
    )

    target_launch_date: Mapped[date | None] = mapped_column(Date)

    updated_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )


__all__ = [
    "DEFAULT_ALLOWED_CURRENCIES",
    "DEFAULT_BILLING_CURRENCY",
    "DEFAULT_CONTRIBUTOR_TERMS",
    "DEFAULT_CONTRIBUTOR_TERMS_VERSION",
    "DEFAULT_CURRICULUM_LICENSE",
    "DEFAULT_CURRICULUM_OWNER",
    "DEFAULT_GUARDIAN_CONSENT_BELOW_AGE",
    "DEFAULT_MIN_STUDENT_AGE",
    "DEFAULT_PAYOUT_CURRENCY",
    "DEFAULT_SECOND_APPROVER_THRESHOLD_MINOR",
    "DEFAULT_TERMS_VERSION",
    "PlatformSettings",
    "SETTINGS_ID",
]
