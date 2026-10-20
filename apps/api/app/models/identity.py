"""Identity: one student across Academia and Skills (PRD §14).

Phase 0 built this module in two steps. **PR 0.1a** added the account itself:
`users` gains a role and a soft-deletion timestamp, and `UserProfile` holds
profile, preferences and the Choose Path flag. **PR 0.1b (this change)** adds
the credential and reliability tables — single-use refresh-token families, email
tokens, consent records and the idempotency-key store (ADR-0007, ADR-0009).

`Role` and `AuditLog` live in :mod:`app.models.admin` (05-domain-map.md). The
auth service, role enforcement and audit writes land in PR 0.8–0.10; nothing
here is exposed to clients yet. Every table below is a *shape*: the behaviour
(rotation, reuse detection, replay) is PR 0.5 and 0.8.
"""
from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.admin import JSONPayload, Role


class User(Base, TimestampMixin):
    """One identity for Academia, Skills, work and earnings (PRD §14).

    Expand-only from PR 0.1a: the original skeleton columns stay as they are.
    ``university``/``department``/``level`` are still free strings — M1 adds the
    academia foreign keys and backfills them (04-v1-to-v2-migration.md).
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    username: Mapped[str] = mapped_column(String(80), nullable=False, unique=True, index=True)
    password_hash: Mapped[str | None] = mapped_column(String(255))
    google_sub: Mapped[str | None] = mapped_column(String(255), unique=True)
    name: Mapped[str | None] = mapped_column(String(150))
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Academic context (PRD §3) — free strings in the skeleton; FK'd in the real model.
    university: Mapped[str | None] = mapped_column(String(150))
    department: Mapped[str | None] = mapped_column(String(150))
    level: Mapped[str | None] = mapped_column(String(20))

    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # --- Phase 0 PR 0.1a ---
    # One role per account (student, reviewer, ops_admin, super_admin, plus the
    # reserved department_rep/company rows). Roles are data, not code, so a future
    # role is a seed row. Nullable so skeleton/local accounts stay valid.
    role_id: Mapped[int | None] = mapped_column(
        ForeignKey("roles.id", ondelete="SET NULL"), index=True
    )
    # Set when deletion anonymises and deactivates the account (ADR-0009); the row
    # is never hard-deleted because payments and audit rows must stay explainable.
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # --- Two-factor (F1/C8) ---
    # Base32 TOTP secret. It is stored only while 2FA is being enrolled or after
    # it is enabled; a disabled account keeps it so re-enabling does not start
    # from scratch. `totp_enabled_at` is the switch the login flow reads.
    totp_secret: Mapped[str | None] = mapped_column(String(64))
    totp_enabled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    # SHA-256 hashes of the one-time recovery codes. The plaintext codes are
    # returned exactly once, when 2FA is confirmed.
    totp_recovery_hashes: Mapped[list | None] = mapped_column(JSONPayload)

    # Unidirectional: nothing needs `role.users` yet, and leaving it out keeps
    # this module free of a cycle with app.models.admin.
    role: Mapped[Role | None] = relationship()
    profile: Mapped[UserProfile | None] = relationship(
        back_populates="user", cascade="all, delete-orphan", uselist=False
    )

    __table_args__ = (UniqueConstraint("email", name="uq_users_email"),)


class UserProfile(Base, TimestampMixin):
    """Profile, preferences and the Choose Path flag (1:1 with a user).

    ``UserPreferences`` from the domain map is folded in here as typed columns
    rather than a JSON blob, so preferences stay queryable and validated.
    """

    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    display_name: Mapped[str | None] = mapped_column(String(150))
    avatar_url: Mapped[str | None] = mapped_column(String(1024))
    # Used by matching only when an opportunity says location matters.
    location: Mapped[str | None] = mapped_column(String(120))
    bio: Mapped[str | None] = mapped_column(String(500))
    locale: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    timezone: Mapped[str | None] = mapped_column(String(64))

    # Choose Path (PRD §2): 'academia' | 'skills'; null until the student chooses.
    preferred_path: Mapped[str | None] = mapped_column(String(16))
    # Age hook only — 18 is the policy pending legal review, not enforced yet.
    date_of_birth: Mapped[date | None] = mapped_column(Date)
    onboarding_completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    notify_email: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    notify_push: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    # The Talent profile is opt-in: nothing is exposed to companies by default.
    profile_visibility: Mapped[str] = mapped_column(String(16), default="private", nullable=False)

    user: Mapped[User] = relationship(back_populates="profile")


# --- Phase 0 PR 0.1b: credentials, consent and idempotency (ADR-0007, ADR-0009) ---
#
# Two rules hold across all four tables below:
# 1. Only a **hash** of any bearer value is stored. A database dump must not be a
#    set of usable sessions or password-reset links.
# 2. The raw token/key is returned to the client exactly once, when it is minted.

REFRESH_PLATFORMS: tuple[str, ...] = ("web", "ios", "android", "admin")
EMAIL_TOKEN_PURPOSES: tuple[str, ...] = ("verify_email", "reset_password")
CONSENT_KINDS: tuple[str, ...] = (
    "terms_of_service",
    "privacy_policy",
    "contributor_terms",
    "marketing",
)

# Why a refresh token stopped working. Recorded so a support question
# ("why was I logged out?") has an answer without guessing.
REVOKE_LOGOUT = "logout"
REVOKE_REUSE_DETECTED = "reuse_detected"
REVOKE_PASSWORD_RESET = "password_reset"
REVOKE_ACCOUNT_DELETED = "account_deleted"
REVOKE_ROTATED = "rotated"


class RefreshToken(Base, TimestampMixin):
    """One link in a rotating refresh-token family (ADR-0009).

    A login mints a `family_id` and the first token. Every refresh marks the
    presented token `used_at` and inserts its replacement in the same family, so
    a token is **single-use by construction**. Presenting a token that already
    has `used_at` is a replay: the service revokes the whole family
    (`REVOKE_REUSE_DETECTED`), which is what makes a stolen token short-lived.

    `platform` records which client the session belongs to, so "log out all my
    phones" is a query rather than a guess.
    """

    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    # Shared by every token in one login chain; a UUID, not a second table.
    family_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(String(64), nullable=False)  # sha256 hex
    platform: Mapped[str] = mapped_column(
        String(10), default="web", server_default="web", nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    revoked_reason: Mapped[str | None] = mapped_column(String(40))
    # Rotation chain, kept for forensics: the replacement may itself be revoked.
    replaced_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("refresh_tokens.id", ondelete="SET NULL")
    )

    __table_args__ = (UniqueConstraint("token_hash", name="uq_refresh_tokens_token_hash"),)


class EmailToken(Base, TimestampMixin):
    """Verification / password-reset token: hashed, expiring, single use.

    Only one token per `(user, purpose)` is ever active; minting a new one
    replaces the previous, so an old link stops working (the service enforces
    this in PR 0.8 — the model makes the hash unique and keeps the intent clear).
    """

    __tablename__ = "email_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    purpose: Mapped[str] = mapped_column(String(20), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (UniqueConstraint("token_hash", name="uq_email_tokens_token_hash"),)


class Consent(Base):
    """Append-only evidence of what a student agreed to, and when (PRD §13).

    Consent is a record, not a flag: agreeing to new terms adds a row, it never
    edits the old one, so "what did they accept in October?" is answerable.
    There is no `updated_at` for the same reason `AuditLog` has none.

    `user_id` is `SET NULL` on deletion: the evidence is retained after an account
    is anonymised, but stops pointing at a person. Ages and terms are hooks only
    — 18 remains a policy under legal review, not enforced here.
    """

    __tablename__ = "consents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    kind: Mapped[str] = mapped_column(String(30), nullable=False)
    document_version: Mapped[str] = mapped_column(String(20), nullable=False)
    granted: Mapped[bool] = mapped_column(Boolean, nullable=False)
    ip_hash: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )


class UserLanguage(Base, TimestampMixin):
    """A language a student can work in; matching reads these rows."""

    __tablename__ = "user_languages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    language: Mapped[str] = mapped_column(String(60), nullable=False)
    # "basic" | "conversational" | "fluent" | "native"
    level: Mapped[str] = mapped_column(
        String(20), default="fluent", server_default="fluent", nullable=False
    )

    __table_args__ = (
        UniqueConstraint("user_id", "language", name="uq_user_language"),
    )


class UserAvailability(Base, TimestampMixin):
    """How much work a student can take on, and when they can start."""

    __tablename__ = "user_availability"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    hours_per_week: Mapped[int | None] = mapped_column(Integer)
    available_from: Mapped[date | None] = mapped_column(Date)
    note: Mapped[str | None] = mapped_column(String(255))


class IdempotencyKey(Base):
    """Replay guard for every write that must not happen twice (ADR-0007).

    The client sends a UUIDv4 `Idempotency-Key`; the API stores the key with the
    fingerprint of the request and, once it finishes, the response. A replay
    returns the stored response instead of writing again — that is what makes
    "no lost work, no lost payments" true on a dropped connection.

    `completed_at IS NULL` means the first attempt is still in flight, so a
    concurrent replay gets 409 rather than a second write. The same key with a
    *different* body is a client bug and also a 409.

    The payload is JSONB on Postgres. Rows are purged after `expires_at`
    (24h by default, set by the service in PR 0.5).
    """

    __tablename__ = "idempotency_keys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(64), nullable=False)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    method: Mapped[str] = mapped_column(String(8), nullable=False)
    path: Mapped[str] = mapped_column(String(255), nullable=False)
    request_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    response_status: Mapped[int | None] = mapped_column(Integer)
    response_body: Mapped[dict | None] = mapped_column(JSONPayload)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (UniqueConstraint("key", name="uq_idempotency_keys_key"),)
