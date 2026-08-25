"""Grant (or revoke) admin privileges for a user.

This is intentionally NOT a one-line "type a username, done" script anymore -- granting
admin is a real privilege escalation, and this script is the only place it can happen
outside the in-app admin UI (routes/admin_routes.py, which is itself gated by
@admin_required). Every grant/revoke made here is written to AdminAuditLog (source='cli')
so there is always a record of who has ever been made admin and when, even though a
script run from a shell has no logged-in session to attribute the change to.

Usage:
    python make_admin.py <username> grant   # requires typing a confirmation phrase
    python make_admin.py <username> revoke
"""
import sys
from datetime import datetime
from app import app
from models import User, AdminAuditLog, db


def main():
    if len(sys.argv) != 3 or sys.argv[2] not in ('grant', 'revoke'):
        print("Usage: python make_admin.py <username> grant|revoke")
        sys.exit(1)

    username, action = sys.argv[1], sys.argv[2]

    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"❌ User '{username}' not found")
            sys.exit(1)

        want_admin = action == 'grant'
        if user.is_admin == want_admin:
            print(f"ℹ️  '{username}' already has is_admin={want_admin}. Nothing to do.")
            sys.exit(0)

        print(f"About to set is_admin={want_admin} for user '{username}' (id={user.id}, email={user.email}).")
        print(f"This action is permanently logged to AdminAuditLog.")
        confirm = input(f"Type the username again to confirm ('{username}'): ").strip()
        if confirm != username:
            print("❌ Confirmation did not match. Aborted -- no change made.")
            sys.exit(1)

        user.is_admin = want_admin
        db.session.add(AdminAuditLog(
            target_user_id=user.id, actor_user_id=None,
            action='grant_admin' if want_admin else 'revoke_admin',
            source='cli', created_at=datetime.utcnow(),
        ))
        db.session.commit()
        print(f"✅ '{username}' is_admin is now {want_admin}. Logged to AdminAuditLog.")


if __name__ == '__main__':
    main()
