"""Declarative base and model registry.

Alembic autogenerate imports ``Base`` from here; every model module must be
imported below so its tables are registered on the metadata.
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all V2 models."""


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


# Import model modules for metadata registration (side-effect imports).
from app.models import academia, identity  # noqa: E402,F401  (noqa: isort)
