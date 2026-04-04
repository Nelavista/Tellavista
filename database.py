import os
import re
import time
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from extensions import db
from models import User
from config import DATABASE_URL

def debug_print(*args, **kwargs):
    from config import DEBUG_MODE
    if DEBUG_MODE:
        print(*args, **kwargs)

def create_database_if_not_exists():
    """Create database if it doesn't exist (PostgreSQL only)."""
    try:
        db_url = DATABASE_URL
        if not db_url or 'postgresql://' not in db_url:
            return True

        parts = db_url.split('/')
        base_url = '/'.join(parts[:-1])
        db_name = parts[-1]

        conn = psycopg2.connect(base_url + '/postgres')
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()
        if not exists:
            print(f"🔄 Creating database: {db_name}")
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            print(f"✅ Database {db_name} created")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"⚠️ Could not create database: {e}")
        return False

def init_database(app):
    """Initialize database with error handling and upgrade video columns."""
    try:
        create_database_if_not_exists()
        with app.app_context():
            db.create_all()
            print("✅ Database tables created/verified")

            # Upgrade video table columns (PostgreSQL)
            try:
                from sqlalchemy import text
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE videos ALTER COLUMN semester TYPE VARCHAR(20)"))
                    conn.execute(text("ALTER TABLE videos ALTER COLUMN level TYPE VARCHAR(50)"))
                    conn.commit()
                    print("✅ Video table columns upgraded")
            except Exception as e:
                debug_print(f"Note: video column upgrade skipped: {e}")

            # Nelavista Student Profile Migration
            try:
                from sqlalchemy import text, inspect
                inspector = inspect(db.engine)
                columns = [col['name'] for col in inspector.get_columns('user')]
                if 'level' in columns and 'user_level' not in columns:
                    if 'sqlite' not in str(db.engine.url):
                        with db.engine.connect() as conn:
                            conn.execute(text('ALTER TABLE "user" RENAME COLUMN level TO user_level'))
                            conn.commit()
                            print("✅ Renamed 'level' column to 'user_level'")
                    columns = [col['name'] for col in inspector.get_columns('user')]

                new_columns = ['name', 'university', 'faculty', 'department', 'level']
                for col_name in new_columns:
                    if col_name not in columns:
                        with db.engine.connect() as conn:
                            col_type = "VARCHAR(100)" if col_name == 'name' else "VARCHAR(150)" if col_name in ['university','faculty','department'] else "VARCHAR(50)"
                            conn.execute(text(f'ALTER TABLE "user" ADD COLUMN {col_name} {col_type}'))
                            conn.commit()
                            print(f"✅ Added column {col_name} to user table")
            except Exception as e:
                print(f"⚠️ User table upgrade skipped: {e}")

            db.session.execute(text('SELECT 1'))
            print("✅ Database connection successful")
            masked_uri = re.sub(r':[^@]*@', ':****@', app.config['SQLALCHEMY_DATABASE_URI'])
            print(f"🗄️ Connected to database: {masked_uri}")
            return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print("🚨 Falling back to SQLite database")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tellavista.db'
        try:
            with app.app_context():
                db.create_all()
                print("✅ SQLite database created as fallback")
                return True
        except Exception as e2:
            print(f"❌ SQLite fallback also failed: {e2}")
            return False

def create_default_user(app):
    """Create default user if none exists."""
    with app.app_context():
        try:
            user = User.query.filter_by(username='test').first()
            if not user:
                user = User(username='test', email='test@example.com')
                user.set_password('test123')
                db.session.add(user)
                db.session.commit()
                print("✅ Created default user: test / test123")
            else:
                print("✅ Default user already exists: test / test123")
        except Exception as e:
            print(f"❌ Error creating default user: {e}")

def cleanup_stale_files():
    """Stub: clean up old uploaded files."""
    pass