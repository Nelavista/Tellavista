"""Create or repair the local development accounts.

    python -m tools.create_local_user

Local only. It gives the seeded ``student1@example.test`` account a known
password so you can sign in immediately without email or a signup step, and
creates ``admin@example.test`` for the admin app. It is idempotent: if you
change a password later, re-running does not overwrite it. Use ``-ResetDb`` in
``scripts/dev-local.ps1`` (or delete the SQLite file) to start over.

The admin app still requires 2FA enrollment on first login (a product rule, not
something this tool bypasses).

Refuses unless ``APP_ENV=local`` and the database target is local (the shared
prod guard). It never runs against DEV or PROD.
"""
from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

# Repo root and apps/api, so `tools` and `app` resolve when run as a module.
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "apps" / "api"))

from tools.prodguard import guard  # noqa: E402

guard("create_local_user")

from app.core.config import get_settings  # noqa: E402
from app.core.security import hash_password  # noqa: E402
from app.db.base import Base  # noqa: E402,F401  (register models before use)
from app.db.session import SessionLocal, engine  # noqa: E402
from app.models.admin import ROLE_STUDENT, ROLE_SUPER_ADMIN, Role  # noqa: E402
from app.models.identity import User  # noqa: E402
from app.seed.roles import seed_roles  # noqa: E402

PASSWORD = "localdevpass123"

ACCOUNTS = (
    ("student1@example.test", "student1", "Local Dev Student", ROLE_STUDENT),
    ("admin@example.test", "admin", "Local Dev Admin", ROLE_SUPER_ADMIN),
)


def _upsert_user(
    db: Session, *, email: str, username: str, name: str, role_code: str
) -> tuple[str, bool]:
    role = db.scalar(select(Role).where(Role.code == role_code))
    if role is None:
        raise RuntimeError(
            f"role {role_code!r} is missing; run `python -m tools.seed_local` first."
        )

    user = db.scalar(select(User).where(User.email == email))
    if user is None:
        user = User(
            email=email,
            username=username,
            name=name,
            password_hash=hash_password(PASSWORD),
            email_verified=True,
            role_id=role.id,
        )
        db.add(user)
        return "created", True

    changed = False
    password_set = False
    if not user.password_hash:
        # The seed deliberately leaves this empty. Do not overwrite a password
        # you changed in the UI on the next run.
        user.password_hash = hash_password(PASSWORD)
        changed = True
        password_set = True
    if not user.email_verified:
        user.email_verified = True
        changed = True
    if user.role_id != role.id:
        user.role_id = role.id
        changed = True
    if user.is_deleted:
        user.is_deleted = False
        changed = True
    return ("updated" if changed else "unchanged"), password_set


def main() -> int:
    settings = get_settings()
    if settings.APP_ENV != "local":
        print(
            "[create_local_user] refused: this tool only runs with APP_ENV=local.",
            file=sys.stderr,
        )
        return 2

    # Local convenience: make the tool work even if the seed has not run yet.
    Base.metadata.create_all(engine)

    with SessionLocal() as db:
        seed_roles(db)
        for email, username, name, role_code in ACCOUNTS:
            action, password_set = _upsert_user(
                db, email=email, username=username, name=name, role_code=role_code
            )
            note = f"password: {PASSWORD}" if password_set else "password left unchanged"
            print(f"[create_local_user] {action} {email} ({note})")
        db.commit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
