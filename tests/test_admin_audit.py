"""Admin privilege changes must always be logged, from both entry points (the in-app
toggle and the make_admin.py CLI script)."""
from extensions import db
from models import User, AdminAuditLog


def test_web_toggle_admin_writes_audit_log(app, client, make_user, login_as):
    admin = make_user('audit_admin', is_admin=True)
    target = make_user('audit_target', is_admin=False)
    login_as(client, admin)

    res = client.post(f'/admin/users/{target.id}/toggle-admin')
    assert res.status_code == 200
    assert res.get_json()['is_admin'] is True

    with app.app_context():
        logs = AdminAuditLog.query.filter_by(target_user_id=target.id).all()
        assert len(logs) == 1
        assert logs[0].action == 'grant_admin'
        assert logs[0].source == 'web'
        assert logs[0].actor_user_id == admin.id


def test_admin_cannot_remove_own_admin_access(app, client, make_user, login_as):
    admin = make_user('self_admin', is_admin=True)
    login_as(client, admin)
    res = client.post(f'/admin/users/{admin.id}/toggle-admin')
    assert res.status_code == 400


def test_non_admin_cannot_toggle_admin(app, client, make_user, login_as):
    regular = make_user('regular_user', is_admin=False)
    target = make_user('some_target', is_admin=False)
    login_as(client, regular)
    res = client.post(f'/admin/users/{target.id}/toggle-admin')
    assert res.status_code == 403
