"""Identity: one student across Academia and Skills (PRD §14).

Minimal skeleton so the seed and health checks have something real to write to.
The full identity service (tokens, Argon2, rotation, MFA) is V2 feature work (ADR-0009).
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class User(Base, TimestampMixin):
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

    __table_args__ = (UniqueConstraint("email", name="uq_users_email"),)
