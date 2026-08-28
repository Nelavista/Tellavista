import os
import re
import time
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from extensions import db
from models import User
from config import DATABASE_URL
from logging_config import logger

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

def _create_all_and_stamp_if_alembic_untracked(app):
    """The db.create_all()-vs-Alembic race, fixed: db.create_all() creates any table
    defined in models.py that's missing, with zero awareness of migration history. Once
    a database has ever been touched by Alembic (its `alembic_version` table exists),
    create_all() must never run again on it — if a migration is about to CREATE TABLE
    something new, importing app.py first (which any script using `from app import app`
    has to do, including a migration-running one-liner, and including every normal app
    boot before the migration is run) silently creates that same table via create_all(),
    and the migration then fails on "relation already exists". This bit us for real: a
    routine `flask db current` check against production silently created a bare,
    un-indexed, un-tracked `topics` table ahead of the actual migration, which then had
    to be manually dropped before the real migration could run.

    Fix: check whether `alembic_version` exists first.
      - If it does NOT exist, this is either a genuinely fresh database (no tables at
        all -- first-ever local/CI setup) or a legacy database that predates Alembic
        being wired into this project (already has tables, never stamped) -- the
        existing "legacy bridge" scenario this function's tables-upgrade blocks below
        were written for. Either way, create_all() is safe to run (a no-op for tables
        that already exist), and the database is then stamped at the current Alembic
        head so a subsequent `flask db upgrade` sees "nothing to apply" instead of
        replaying the entire migration history against tables that already exist.
      - If `alembic_version` DOES exist, this database is already Alembic-tracked
        (true of every real deployed environment, production included) -- create_all()
        is skipped entirely. From that point on, `flask db upgrade` is the only path
        that may ever create a new table, exactly as the module docstring below always
        intended.
    """
    from sqlalchemy import inspect
    from flask_migrate import stamp

    alembic_tracked = inspect(db.engine).has_table('alembic_version')
    if alembic_tracked:
        debug_print("Database already tracked by Alembic -- skipping db.create_all(), migrations are the only path.")
        return

    db.create_all()
    stamp()
    print("✅ Fresh/legacy database: tables created and stamped at the current Alembic head.")


def init_database(app):
    """Initialize database with error handling and upgrade video columns.

    NOTE: Flask-Migrate is now wired into app.py (see migrations/). New schema changes
    should go through `flask db migrate` / `flask db upgrade`, not another ad-hoc ALTER
    TABLE block here. The blocks below are a legacy bridge for databases that predate
    Flask-Migrate being wired in — once `flask db upgrade` has been run against every
    live database, these can be retired.
    """
    try:
        create_database_if_not_exists()
        with app.app_context():
            _create_all_and_stamp_if_alembic_untracked(app)
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
        configured_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '') or ''
        is_sqlite_configured = configured_uri.startswith('sqlite')
        # str(e) from psycopg2/SQLAlchemy connection errors does not echo the DSN/password
        # (they report things like "connection failed: timeout expired", "password
        # authentication failed") -- safe to log as-is; never log configured_uri itself,
        # which does contain the password.
        logger.error(f"Database initialization failed: {e}")

        if not is_sqlite_configured:
            # A real (non-SQLite) database was configured -- e.g. Postgres in production
            # -- and connecting to it failed. Previously this silently swapped to a local,
            # empty, non-durable SQLite file and kept serving traffic, which turned a
            # visible outage into a silent one (the app "came up successfully" against an
            # empty database, any writes during that window were lost on next restart).
            # Fail startup loudly instead so the outage is impossible to miss.
            logger.error(
                "Refusing to silently fall back to SQLite -- DATABASE_URL was configured "
                "for a real database. Fix the database connection (check DATABASE_URL, "
                "network access, credentials) and restart. The process will now exit."
            )
            raise RuntimeError(
                'Database initialization failed and a non-SQLite DATABASE_URL was '
                'configured. Refusing to start against a silent empty fallback database. '
                f'Original error: {e}'
            ) from e

        # DATABASE_URL was already sqlite (the local-dev default when DATABASE_URL is
        # unset) -- this is not a production fallback, just a retry of the same local
        # file, which is the intentional, supported local/test path.
        try:
            with app.app_context():
                _create_all_and_stamp_if_alembic_untracked(app)
                logger.info("SQLite (local dev) database created/verified.")
                return True
        except Exception as e2:
            logger.error(f"SQLite initialization also failed: {e2}")
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