"""DEPRECATED (Level 1 cleanup pass): this was a one-off, hand-run ALTER TABLE script
predating Flask-Migrate being wired into this project (see migrations/, and
database.py's init_database() comment). Both columns it adds already exist in the
current models.py/migrations chain -- running this against an up-to-date database is a
safe no-op (IF NOT EXISTS), but it should not be treated as how schema changes get made
going forward. Any new schema change belongs in a real Alembic migration:
    flask db migrate -m "description"
    flask db upgrade
Running raw ALTER TABLE scripts like this one outside Alembic risks desynchronizing the
alembic_version table from the database's actual schema. Kept only for a database that
somehow still predates both this script's original run AND Flask-Migrate.
"""
import sys
sys.path.insert(0, 'C:\\Users\\PC\\Documents\\Tellavista')

from app import app
from extensions import db
from sqlalchemy import text

with app.app_context():
    with db.engine.connect() as conn:
        conn.execute(text('ALTER TABLE "user" ADD COLUMN IF NOT EXISTS semester VARCHAR(20)'))
        conn.execute(text('ALTER TABLE materials ADD COLUMN IF NOT EXISTS semester VARCHAR(20)'))
        conn.commit()
    print("Done! Columns added successfully.")