"""Aggregate v1 router. Domain routers attach here as they are built."""
from __future__ import annotations

from fastapi import APIRouter

from app.api.v1 import health

api_v1_router = APIRouter()
api_v1_router.include_router(health.router)

# As V2 features land, add e.g.:
#   from app.api.v1.domains import identity, academia, skills
#   api_v1_router.include_router(identity.router, prefix="/auth", tags=["identity"])
