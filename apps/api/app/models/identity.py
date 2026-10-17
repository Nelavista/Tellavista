"""Identity: one student across Academia and Skills (PRD §14).

Phase 0 builds this module in two steps. **PR 0.1a (this change)** adds the
account itself: `users` gains a role and a soft-deletion timestamp, and
`UserProfile` holds profile, preferences and the Choose Path flag. **PR 0.1b**
adds the credential tables — single-use refresh-token families, email tokens,
consent records and the idempotency-key store (ADR-0007, ADR-0009).

`Role` and `AuditLog` live in :mod:`app.models.admin` (05-domain-map.md). The
auth service, role enforcement and audit writes land in PR 0.8–0.10; nothing
here is exposed to clients yet.
"""
from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.admin import Role


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
