"""Phase 1 — the V1 bridge is one-way, repeatable and reconcilable.

A dry run must write nothing but its own receipt; an apply must create the account
without ever holding a plaintext password; running the same export twice must not
duplicate rows; and the reconciliation report must compare V2's counts with V1's.
"""
from __future__ import annotations

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.identity import User, UserProfile
from app.models.ops import ImportRun
from app.services.imports import v1 as importer

EXPORT = {
    "users": [
        {
            "id": 1,
            "email": "Amina@example.test",
            "username": "amina",
            "name": "Amina Bello",
            "email_verified": True,
            "university": "University of Lagos",
            "department": "Computer Science",
            "level": "300",
            "password_hash": "pbkdf2:sha256:260000$abc$deadbeef",
        },
        {
            "id": 2,
            "email": "broken-row",
            "name": "No Email",
        },
    ],
    "taxonomy": [
        {
            "name": "University of Lagos",
            "slug": "university-of-lagos",
            "faculties": [
                {
                    "name": "Science",
                    "departments": [
                        {
                            "name": "Computer Science",
                            "courses": [
                                {"code": "CSC213", "title": "Data Structures", "level": "200"}
                            ],
                        }
                    ],
                }
            ],
        }
    ],
    "materials": [],
    "questions": [],
    "skills": [
        {
            "name": "AI Data Annotation",
            "slug": "ai-data-annotation",
            "category": "AI & Data",
            "paths": [{"slug": "annotation-starter", "title": "Annotation starter"}],
        }
    ],
}


def test_a_dry_run_writes_nothing_but_the_receipt(db: Session) -> None:
    run = importer.run_import(db, data=EXPORT, mode="dry_run")

    assert run.status == "done"
    assert run.counts["users"]["created"] == 1
    assert db.scalars(select(User)).all() == []
    assert db.scalars(select(ImportRun)).all() == [run]


def test_an_apply_creates_the_account_without_a_plaintext_password(db: Session) -> None:
    run = importer.run_import(db, data=EXPORT, mode="apply")

    user = db.scalars(select(User).where(User.email == "amina@example.test")).one()
    assert user.email == "amina@example.test"  # normalised, not rejected
    assert user.password_hash.startswith("pbkdf2:")
    assert user.email_verified is True
    assert user.profile.display_name == "Amina Bello"
    assert run.counts["users"]["created"] == 1
    assert run.counts["users"]["errors"]


def test_the_same_export_applied_twice_does_not_duplicate(db: Session) -> None:
    importer.run_import(db, data=EXPORT, mode="apply")
    second = importer.run_import(db, data=EXPORT, mode="apply")

    assert len(db.scalars(select(User)).all()) == 1
    assert len(db.scalars(select(UserProfile)).all()) == 1
    assert second.counts["users"]["created"] == 0
    assert second.counts["users"]["skipped"] >= 1


def test_an_import_never_resets_a_password_changed_in_v2(db: Session) -> None:
    importer.run_import(db, data=EXPORT, mode="apply")
    user = db.scalars(select(User).where(User.email == "amina@example.test")).one()
    user.password_hash = "$argon2id$v=19$m=65536,t=3,p=4$hash"
    db.flush()

    importer.run_import(db, data=EXPORT, mode="apply")

    assert db.get(User, user.id).password_hash.startswith("$argon2id$")


def test_reconciliation_compares_counts_with_v1(db: Session) -> None:
    run = importer.run_import(db, data=EXPORT, mode="apply")

    balanced = importer.reconciliation(run, {"users": 1})
    assert balanced["balanced"] is True
    assert balanced["sections"]["users"] == {
        "expected": 1,
        "actual": 1,
        "skipped": 0,
        "errors": 1,
        "matched": True,
    }

    unbalanced = importer.reconciliation(run, {"users": 5})
    assert unbalanced["balanced"] is False
    assert unbalanced["sections"]["users"]["matched"] is False


def test_checksums_are_stable_and_section_scoped(db: Session) -> None:
    first = importer.run_import(db, data=EXPORT, mode="dry_run")
    second = importer.run_import(db, data=EXPORT, mode="dry_run")

    assert first.checksums == second.checksums
    assert first.checksums["users"].startswith("sha256:")
    assert first.checksums["users"] != first.checksums["skills"]


def test_an_unknown_mode_is_refused(db: Session) -> None:
    with pytest.raises(ApiError) as excinfo:
        importer.run_import(db, data=EXPORT, mode="overwrite")
    assert excinfo.value.code == "invalid_import_mode"


def test_a_malformed_export_is_refused(db: Session) -> None:
    with pytest.raises(ApiError) as excinfo:
        importer.run_import(db, data=["not", "an", "object"], mode="apply")
    assert excinfo.value.code == "export_invalid"


def test_imported_material_reuses_the_course_taxonomy(db: Session) -> None:
    export = {
        **EXPORT,
        "materials": [
            {
                "course_code": "CSC213",
                "level": "200",
                "title": "CSC213 lecture notes",
                "file_url": "https://res.cloudinary.com/nelavista/notes.pdf",
            }
        ],
    }
    importer.run_import(db, data=export, mode="apply")

    from app.models.academia import Material

    material = db.scalars(select(Material)).one()
    assert material.file_url.endswith("notes.pdf")
    assert material.title == "CSC213 lecture notes"
