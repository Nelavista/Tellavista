"""Test environment for apps/api.

Sets safe defaults BEFORE importing the app, and tells settings not to read a
developer's local .env file. CI sets these too; this keeps bare `pytest` working.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# apps/api on the path so `import app` resolves to this package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

os.environ.setdefault("NELAVISTA_SKIP_ENV_FILE", "1")
os.environ.setdefault("APP_ENV", "local")
os.environ.setdefault("DATABASE_URL", "postgresql://nelavista:nelavista@localhost:5432/nelavista_test")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest-only")
os.environ.setdefault("CORS_ORIGINS", "http://localhost:5173")
