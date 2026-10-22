"""Grant a staff role to an existing account (first admin, ops approver).

    python -m tools.create_staff --email you@example.com --role super_admin
    python -m tools.create_staff --email ops@example.com --role ops_admin

The account must already exist: sign up in the web app first. This tool never
creates a password and never prints one. It:

* runs through the prod guard (prints the masked target, refuses PROD unless
  `--i-know-this-is-production` or `PRODGUARD_ALLOW=1` is set);
* is idempotent — re-running reports "already set" instead of duplicating work;
* marks the email verified (staff need working email for 2FA recovery);
* writes an `audit_logs` row in the same transaction as the role change.

Why two accounts: payouts at or above the configured threshold (NGN 50,000.00)
need a second approver, and the second approver must be a different user.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.orm import Session

# Repo root and apps/api, so `tools` and `app` resolve when run as a module.
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "apps" / "api"))

from app.db.base import Base  # noqa: E402,F401  (import the model registry first)
from app.models.admin import SEED_ROLES, Role  # noqa: E402
from app.models.identity import User  # noqa: E402

from app.services import audit  # noqa: E402
from tools.prodguard import guard  # noqa: E402

STAFF_ROLE_CODES = tuple(sorted(code for code, _name, is_staff in SEED_ROLES if is_staff))


def promote_user(db: Session, *, email: str, role_code: str) -> tuple[User, Role, bool]:
    """Set the role and verify the email. Returns (user, role, changed)."""
    role = db.scalar(select(Role).where(Role.code == role_code))
    if role is None:
        raise LookupError(
            f"role {role_code!r} does not exist; run the roles migration first "
            f"(known staff roles: {', '.join(STAFF_ROLE_CODES)})"
        )
    if not role.is_staff:
        raise ValueError(f"role {role_code!r} is not a staff role")

    user = db.scalar(select(User).where(func.lower(User.email) == email.strip().lower()))
    if user is None:
        raise LookupError(
            f"no account with email {email!r}. Sign up in the web app first; "
            "this tool never creates a password."
        )

    changed = user.role_id != role.id or not user.email_verified
    user.role_id = role.id
    user.email_verified = True

    if changed:
        audit.record(
            db,
            action="staff.role_granted",
            target_type="user",
            target_id=user.id,
            reason="tools.create_staff",
            context={"email": user.email, "role": role.code, "source": "cli"},
        )
    db.commit()
    return user, role, changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Grant a staff role to an existing account (never creates a password)."
    )
    parser.add_argument(
        "--email",
        action="append",
        required=True,
        help="account email; repeat the flag for several accounts with the same role",
    )
    parser.add_argument(
        "--role",
        default="ops_admin",
        choices=STAFF_ROLE_CODES,
        help="staff role to grant (default: ops_admin)",
    )
    # Guard reads this flag; argparse must accept it too.
    parser.add_argument("--i-know-this-is-production", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    guard("create_staff", argv=sys.argv[1:] if argv is None else argv)

    # Imported after the guard so an accidental PROD run prints the target first.
    from app.db.session import SessionLocal

    exit_code = 0
    with SessionLocal() as db:
        for email in args.email:
            try:
                user, role, changed = promote_user(db, email=email, role_code=args.role)
            except (LookupError, ValueError) as exc:
                print(f"[create_staff] {exc}", file=sys.stderr)
                exit_code = 1
                continue
            suffix = "" if changed else " (already set)"
            print(f"[create_staff] {user.email} -> {role.code}{suffix}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
