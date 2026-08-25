"""DEPRECATED (Level 1 cleanup pass): same status as migrate.py -- a one-off ALTER TABLE
script predating Flask-Migrate. The column it adds already exists in the current schema;
running this is a safe no-op against an up-to-date database. New schema changes belong in
a real Alembic migration (`flask db migrate` / `flask db upgrade`), not another script
like this one -- see migrate.py's docstring for why.
"""
from app import app, db
from sqlalchemy import text

with app.app_context():
    db.session.execute(text("ALTER TABLE materials ADD COLUMN IF NOT EXISTS course_code VARCHAR(20)"))
    db.session.commit()
    print("✅ Done!")