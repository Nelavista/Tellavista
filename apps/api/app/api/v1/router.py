"""Aggregate v1 router. Domain routers attach here as they are built.

Each domain owns its own prefix and feature-flag dependency, so this file stays a
list of mounts: the API version path is the only prefix added here.
"""
from __future__ import annotations

from fastapi import APIRouter

from app.api.v1 import health
from app.api.v1.domains.academia import routes as academia_routes
from app.api.v1.domains.identity import onboarding_routes, profile_routes
from app.api.v1.domains.identity import routes as identity_routes
from app.api.v1.domains.money import routes as money_routes
from app.api.v1.domains.opportunities import routes as opportunity_routes
from app.api.v1.domains.ops import routes as ops_routes
from app.api.v1.domains.platform import routes as platform_routes
from app.api.v1.domains.skills import content_routes as skills_content_routes
from app.api.v1.domains.skills import routes as skills_routes
from app.api.v1.domains.talent import routes as talent_routes
from app.api.v1.domains.verification import routes as verification_routes
from app.api.v1.domains.work import routes as work_routes

api_v1_router = APIRouter()
api_v1_router.include_router(health.router)

# Identity: /auth (sessions), /me (profile, path, campus, notifications) and
# /onboarding (wizard). All three are Phase 0/1 and always available.
api_v1_router.include_router(identity_routes.router)
api_v1_router.include_router(profile_routes.router)
api_v1_router.include_router(onboarding_routes.router)

# Phase 2/3 — learning, practice and proof.
api_v1_router.include_router(skills_routes.router)
api_v1_router.include_router(skills_content_routes.router)
api_v1_router.include_router(verification_routes.router)

# Phase 4/7 — opportunities, matching and the Talent profile.
api_v1_router.include_router(opportunity_routes.router)
api_v1_router.include_router(talent_routes.router)

# Phase 5 — delivery and quality control.
api_v1_router.include_router(work_routes.router)

# Phase 6 — money.
api_v1_router.include_router(money_routes.router)

# Phase 8 — Academia connected.
api_v1_router.include_router(academia_routes.router)

# Platform policy (G1–G5): currency, payout thresholds, age rules, terms and
# curriculum ownership. The public config endpoint is read by every client.
api_v1_router.include_router(platform_routes.router)

# Internal tools: imports, support lookup, audit trail.
api_v1_router.include_router(ops_routes.router)
