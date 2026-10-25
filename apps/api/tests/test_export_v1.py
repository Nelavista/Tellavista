"""The V1 exporter must produce the importer's shape from a real database.

SQLite stands in for V1 Postgres here: the exporter reflects columns and reads
rows, so the test proves the mapping (course context, option keys, lesson order,
unique slugs) without a V1 server.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from tools.export_v1 import export_database  # noqa: E402


def _schema() -> MetaData:
    metadata = MetaData()
    Table(
        "user",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("username", String(150)),
        Column("email", String(150)),
        Column("password_hash", String(200)),
        Column("name", String(100)),
        Column("university", String(150)),
        Column("department", String(150)),
        Column("level", String(50)),
        Column("email_verified", Boolean),
        Column("is_deleted", Boolean, default=False),
    )
    Table(
        "universities",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(150)),
        Column("slug", String(160)),
    )
    Table(
        "faculties",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("university_id", Integer),
        Column("name", String(150)),
    )
    Table(
        "departments",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("faculty_id", Integer),
        Column("name", String(150)),
    )
    Table(
        "courses",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("department_id", Integer),
        Column("code", String(20)),
        Column("title", String(200)),
        Column("level", String(10)),
    )
    Table(
        "materials",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("title", String(200)),
        Column("course_id", Integer),
        Column("course_code", String(20)),
        Column("course_type", String(20)),
        Column("level", String(50)),
        Column("department", String(150)),
        Column("university", String(150)),
        Column("file_url", String(500)),
        Column("external_url", String(500)),
        Column("is_approved", Boolean, default=True),
    )
    Table(
        "cbt_questions",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("question_text", Text),
        Column("options_json", Text),
        Column("correct_index", Integer),
        Column("explanation", Text),
        Column("difficulty", String(10)),
        Column("course_id", Integer),
        Column("course_code", String(20)),
        Column("question_type", String(10), default="cbt"),
        Column("is_active", Boolean, default=True),
    )
    Table(
        "skill_categories",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(100)),
        Column("slug", String(100)),
    )
    Table(
        "skills",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("category_id", Integer),
        Column("name", String(120)),
        Column("slug", String(120)),
        Column("description", Text),
        Column("tagline", String(200)),
        Column("level", String(20)),
        Column("is_published", Boolean, default=True),
    )
    Table(
        "learning_paths",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("skill_id", Integer),
        Column("title", String(150)),
        Column("description", Text),
    )
    Table(
        "learning_path_steps",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("path_id", Integer),
        Column("order", Integer),
        Column("step_type", String(20)),
        Column("course_id", Integer),
    )
    Table(
        "skill_courses",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("skill_id", Integer),
        Column("title", String(150)),
        Column("slug", String(150)),
        Column("order", Integer),
        Column("is_published", Boolean, default=True),
    )
    Table(
        "course_modules",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("course_id", Integer),
        Column("title", String(150)),
        Column("order", Integer),
    )
    Table(
        "lessons",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("module_id", Integer),
        Column("title", String(150)),
        Column("slug", String(150)),
        Column("order", Integer),
        Column("content", Text),
        Column("is_published", Boolean, default=True),
    )
    return metadata


def _seed(engine) -> None:
    metadata = _schema()
    metadata.create_all(engine)
    with engine.begin() as conn:
        conn.execute(
            metadata.tables["user"].insert(),
            [
                {
                    "id": 1,
                    "username": "ada",
                    "email": "Ada@Example.test",
                    "password_hash": "pbkdf2:sha256:600000$salt$hash",
                    "name": "Ada",
                    "university": "Test University",
                    "department": "Computer Science",
                    "level": "200",
                    "email_verified": True,
                    "is_deleted": False,
                },
                {
                    "id": 2,
                    "username": "deleted",
                    "email": "deleted@example.test",
                    "password_hash": None,
                    "name": "Deleted",
                    "university": None,
                    "department": None,
                    "level": None,
                    "email_verified": False,
                    "is_deleted": True,
                },
            ],
        )
        conn.execute(
            metadata.tables["universities"].insert(),
            [{"id": 1, "name": "Test University", "slug": "test-university"}],
        )
        conn.execute(
            metadata.tables["faculties"].insert(),
            [{"id": 1, "university_id": 1, "name": "Science"}],
        )
        conn.execute(
            metadata.tables["departments"].insert(),
            [{"id": 1, "faculty_id": 1, "name": "Computer Science"}],
        )
        conn.execute(
            metadata.tables["courses"].insert(),
            [{"id": 1, "department_id": 1, "code": "CSC101", "title": "Intro", "level": "100"}],
        )
        conn.execute(
            metadata.tables["materials"].insert(),
            [
                {
                    "id": 1,
                    "title": "Stored file",
                    "course_id": 1,
                    "course_code": None,
                    "course_type": None,
                    "level": None,
                    "department": None,
                    "university": None,
                    "file_url": "https://res.cloudinary.com/x/file.pdf",
                    "external_url": None,
                    "is_approved": True,
                },
                {
                    "id": 2,
                    "title": "External file",
                    "course_id": 1,
                    "course_code": None,
                    "course_type": None,
                    "level": None,
                    "department": None,
                    "university": None,
                    "file_url": None,
                    "external_url": "https://example.test/file.pdf",
                    "is_approved": True,
                },
                {
                    "id": 3,
                    "title": "No link",
                    "course_id": 1,
                    "course_code": None,
                    "course_type": None,
                    "level": None,
                    "department": None,
                    "university": None,
                    "file_url": None,
                    "external_url": None,
                    "is_approved": True,
                },
                {
                    "id": 4,
                    "title": "Code only",
                    "course_id": None,
                    "course_code": "CSC101",
                    "course_type": None,
                    "level": None,
                    "department": None,
                    "university": None,
                    "file_url": None,
                    "external_url": "https://example.test/code-only.pdf",
                    "is_approved": True,
                },
                {
                    "id": 5,
                    "title": "Static file",
                    "course_id": 1,
                    "course_code": None,
                    "course_type": None,
                    "level": None,
                    "department": None,
                    "university": None,
                    "file_url": "static/materials/legacy.pdf",
                    "external_url": None,
                    "is_approved": True,
                },
                {
                    # V1's OpenStax seed parked the code in course_type only.
                    "id": 6,
                    "title": "OER chapter",
                    "course_id": None,
                    "course_code": None,
                    "course_type": "csc 101",
                    "level": None,
                    "department": "General",
                    "university": None,
                    "file_url": None,
                    "external_url": "https://openstax.test/chapter",
                    "is_approved": True,
                },
                {
                    # course_type is NOT a code here, so this one must still be skipped.
                    "id": 7,
                    "title": "Nothing to attach",
                    "course_id": None,
                    "course_code": None,
                    "course_type": "CORE",
                    "level": None,
                    "department": "General",
                    "university": None,
                    "file_url": None,
                    "external_url": "https://example.test/orphan.pdf",
                    "is_approved": True,
                },
            ],
        )
        conn.execute(
            metadata.tables["cbt_questions"].insert(),
            [
                {
                    "id": 1,
                    "question_text": "Pick B",
                    "options_json": json.dumps(["A", "B", "C"]),
                    "correct_index": 1,
                    "explanation": "Because B.",
                    "difficulty": "easy",
                    "course_id": 1,
                    "course_code": None,
                    "question_type": "cbt",
                    "is_active": True,
                }
            ],
        )
        conn.execute(
            metadata.tables["skill_categories"].insert(),
            [{"id": 1, "name": "AI & Data", "slug": "ai-and-data"}],
        )
        conn.execute(
            metadata.tables["skills"].insert(),
            [
                {
                    "id": 1,
                    "category_id": 1,
                    "name": "Annotation",
                    "slug": "annotation",
                    "description": "Label things.",
                    "tagline": None,
                    "level": "beginner",
                    "is_published": True,
                }
            ],
        )
        conn.execute(
            metadata.tables["learning_paths"].insert(),
            [{"id": 1, "skill_id": 1, "title": "Annotation path", "description": "Start here."}],
        )
        conn.execute(
            metadata.tables["learning_path_steps"].insert(),
            [{"id": 1, "path_id": 1, "order": 1, "step_type": "course", "course_id": 10}],
        )
        conn.execute(
            metadata.tables["skill_courses"].insert(),
            [{"id": 10, "skill_id": 1, "title": "Intro", "slug": "intro", "order": 1, "is_published": True}],
        )
        conn.execute(
            metadata.tables["course_modules"].insert(),
            [
                {"id": 20, "course_id": 10, "title": "One", "order": 1},
                {"id": 21, "course_id": 10, "title": "Two", "order": 2},
            ],
        )
        conn.execute(
            metadata.tables["lessons"].insert(),
            [
                {"id": 30, "module_id": 20, "title": "First", "slug": "intro", "order": 1,
                 "content": "<h2>First</h2><p>Hello <strong>world</strong></p>", "is_published": True},
                {"id": 31, "module_id": 21, "title": "Second", "slug": "intro", "order": 1,
                 "content": "Second body", "is_published": True},
                {"id": 32, "module_id": 21, "title": "Draft", "slug": "draft", "order": 2,
                 "content": "Draft body", "is_published": False},
            ],
        )


def test_export_matches_the_importer_shape(tmp_path) -> None:
    path = tmp_path / "v1.db"
    engine = create_engine(f"sqlite:///{path}")
    _seed(engine)
    engine.dispose()

    data = export_database(f"sqlite:///{path}")

    assert data["meta"]["counts"] == {
        "users": 1,
        "taxonomy": 1,
        "materials": 5,
        "questions": 1,
        "skills": 1,
    }
    assert data["users"][0]["email"] == "ada@example.test"
    assert data["users"][0]["password_hash"].startswith("pbkdf2:")

    course = data["taxonomy"][0]["faculties"][0]["departments"][0]["courses"][0]
    assert course == {"code": "CSC101", "title": "Intro", "level": "100"}

    assert {row["title"] for row in data["materials"]} == {
        "Stored file",
        "External file",
        "Code only",
        "Static file",
        "OER chapter",
    }
    assert data["materials"][1]["file_url"] == "https://example.test/file.pdf"
    assert data["materials"][3]["file_url"] == (
        "https://v1.nelavista.com/static/materials/legacy.pdf"
    )
    assert any("V1's /static files" in warning for warning in data["meta"]["warnings"])
    assert all(row["course_code"] == "CSC101" for row in data["materials"])

    # A code parked in course_type is recovered (canonical casing from the course);
    # a non-code course_type still leaves the material unplaceable.
    oer = next(row for row in data["materials"] if row["title"] == "OER chapter")
    assert oer["file_url"] == "https://openstax.test/chapter"
    assert oer["department"] == "Computer Science"
    assert any("material 7 has no course code" in w for w in data["meta"]["warnings"])

    question = data["questions"][0]
    assert question["correct_key"] == "B"
    assert [option["key"] for option in question["options"]] == ["A", "B", "C"]
    assert question["course_code"] == "CSC101"

    path_row = data["skills"][0]["paths"][0]
    assert path_row["title"] == "Annotation path"
    assert [lesson["slug"] for lesson in path_row["lessons"]] == ["intro", "intro-2"]
    assert path_row["lessons"][0]["body_md"].startswith("## First")
    assert "Hello **world**" in path_row["lessons"][0]["body_md"]
    assert "<p>" not in path_row["lessons"][0]["body_md"]
    assert path_row["lessons"][1]["body_md"] == "Second body"
    assert any("converted to the Markdown" in warning for warning in data["meta"]["warnings"])
