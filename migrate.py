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