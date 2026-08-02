from app import app, db
from sqlalchemy import text

with app.app_context():
    db.session.execute(text("ALTER TABLE materials ADD COLUMN IF NOT EXISTS course_code VARCHAR(20)"))
    db.session.commit()
    print("✅ Done!")