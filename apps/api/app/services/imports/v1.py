"""V1 bridge: one-way, idempotent import from a V1 export file (PRD, ADR-0005).

V2 never connects to the V1 database. This module reads a JSON **export** (or a
read-only snapshot that has been dumped to the same shape), and:

* runs in `dry_run` mode that performs the work inside a savepoint and rolls it
  back, so a preview cannot half-import;
* is idempotent: a second apply updates/skips rather than duplicating, because
  every lookup is by the same natural key V1 uses (email, taxonomy name, course
  code, skill slug);
* never overwrites a V1 password with anything but V1's own hash, and never needs
  the plaintext;
* returns counts and checksums per section as a reconciliation report.

The import deliberately does **not** create enrolments: V1's course registrations
are not trustworthy enough to become academic records without the student
confirming them in the onboarding wizard. `users` keep their university/department
strings as a hint, which is what "Continue with your V1 account" shows.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.core.time import utcnow
from app.models.academia import Course, Department, Faculty, Material, Question, University
from app.models.admin import ROLE_STUDENT, Role
from app.models.identity import User, UserProfile
from app.models.ops import (
    IMPORT_APPLY,
    IMPORT_DONE,
    IMPORT_DRY_RUN,
    IMPORT_FAILED,
    ImportRun,
)
from app.models.skills import (
    STATUS_PUBLISHED,
    LearningPath,
    LearningPathStep,
    Lesson,
    Skill,
    SkillCategory,
)
from app.models.verification import Assessment, AssessmentTask

SECTIONS: tuple[str, ...] = ("users", "taxonomy", "materials", "questions", "skills")


@dataclass
class SectionCounts:
    read: int = 0
    created: int = 0
    updated: int = 0
    skipped: int = 0
    errors: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "read": self.read,
            "created": self.created,
            "updated": self.updated,
            "skipped": self.skipped,
            "errors": self.errors[:50],
        }


def load_export(path: str | Path) -> dict:
    file = Path(path)
    if not file.exists():
        raise ApiError(404, "export_not_found", "The V1 export file does not exist.")
    try:
        data = json.loads(file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ApiError(400, "export_invalid", "The V1 export is not valid JSON.") from exc
    if not isinstance(data, dict):
        raise ApiError(400, "export_invalid", "The V1 export must be a JSON object.")
    return data


def checksum(value: Any) -> str:
    """Stable checksum of a section, comparable with V1's own export checksum."""
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return "sha256:" + hashlib.sha256(canonical.encode()).hexdigest()


# --- users -------------------------------------------------------------------


def _import_users(db: Session, rows: list[dict], counts: SectionCounts) -> dict[str, int]:
    student_role_id = db.scalar(select(Role.id).where(Role.code == ROLE_STUDENT))
    seen: set[str] = set()
    for row in rows:
        counts.read += 1
        email = (row.get("email") or "").strip().lower()
        if not email or "@" not in email:
            counts.errors.append(f"user {row.get('id')}: missing email")
            continue
        if email in seen:
            counts.skipped += 1
            continue
        seen.add(email)

        user = db.scalar(select(User).where(User.email == email))
        if user is None:
            username = (row.get("username") or email.split("@")[0]).strip()[:60]
            username = _unique_username(db, username)
            user = User(
                email=email,
                username=username,
                name=(row.get("name") or "")[:150] or None,
                email_verified=bool(row.get("email_verified", True)),
                university=row.get("university"),
                department=row.get("department"),
                level=row.get("level"),
                role_id=student_role_id,
            )
            # The V1 hash is copied as-is; the plaintext never leaves V1, and the
            # auth service upgrades PBKDF2 or scrypt on first V2 login (ADR-0005).
            legacy_hash = row.get("password_hash") or ""
            if legacy_hash.startswith(("pbkdf2:", "scrypt:")):
                user.password_hash = legacy_hash
            else:
                user.password_hash = None
            db.add(user)
            db.flush()
            db.add(UserProfile(user_id=user.id, display_name=user.name or username))
            counts.created += 1
        else:
            # V2 is authoritative after creation: an import must not undo a profile
            # edit or reset a password a student changed in V2.
            changed = False
            legacy_hash = row.get("password_hash") or ""
            if not user.password_hash and legacy_hash.startswith(("pbkdf2:", "scrypt:")):
                user.password_hash = legacy_hash
                changed = True
            if user.email_verified is False and row.get("email_verified"):
                user.email_verified = True
                changed = True
            if changed:
                counts.updated += 1
            else:
                counts.skipped += 1
    return {"created": counts.created, "updated": counts.updated, "skipped": counts.skipped}


def _unique_username(db: Session, base: str) -> str:
    candidate = base or "student"
    suffix = 0
    while db.scalar(select(User.id).where(User.username == candidate)) is not None:
        suffix += 1
        candidate = f"{base}{suffix}"[:60]
    return candidate


# --- taxonomy ----------------------------------------------------------------


def _import_taxonomy(db: Session, rows: list[dict], counts: SectionCounts) -> dict[str, int]:
    for uni_row in rows:
        counts.read += 1
        name = (uni_row.get("name") or "").strip()
        if not name:
            counts.errors.append("university without a name")
            continue
        slug = (uni_row.get("slug") or _slug(name))[:200]
        uni = db.scalar(select(University).where(University.slug == slug))
        if uni is None:
            uni = University(name=name[:200], slug=slug)
            db.add(uni)
            db.flush()
            counts.created += 1
        else:
            counts.skipped += 1

        for fac_row in uni_row.get("faculties") or []:
            fac_name = (fac_row.get("name") or "").strip()
            if not fac_name:
                continue
            fac = db.scalar(
                select(Faculty).where(
                    Faculty.university_id == uni.id, Faculty.name == fac_name[:200]
                )
            )
            if fac is None:
                fac = Faculty(university_id=uni.id, name=fac_name[:200])
                db.add(fac)
                db.flush()
                counts.created += 1
            for dept_row in fac_row.get("departments") or []:
                dept_name = (dept_row.get("name") or "").strip()
                if not dept_name:
                    continue
                dept = db.scalar(
                    select(Department).where(
                        Department.faculty_id == fac.id, Department.name == dept_name[:200]
                    )
                )
                if dept is None:
                    dept = Department(faculty_id=fac.id, name=dept_name[:200])
                    db.add(dept)
                    db.flush()
                    counts.created += 1
                for course_row in dept_row.get("courses") or []:
                    created = _upsert_course(db, dept.id, course_row)
                    counts.created += int(created)
                    counts.skipped += int(not created)
    return {"created": counts.created, "skipped": counts.skipped}


def _upsert_course(db: Session, department_id: int, row: dict) -> bool:
    code = (row.get("code") or "").strip()[:20]
    title = (row.get("title") or "").strip()[:255]
    level = str(row.get("level") or "").strip()[:10]
    if not code or not title:
        return False
    exists = db.scalar(
        select(Course).where(
            Course.department_id == department_id, Course.code == code, Course.level == level
        )
    )
    if exists is not None:
        return False
    db.add(Course(department_id=department_id, code=code, title=title, level=level))
    db.flush()
    return True


# --- materials and questions -------------------------------------------------


def _find_course(db: Session, row: dict) -> Course | None:
    """Locate a course from a V1 export row by the names it actually carries."""
    code = (row.get("course_code") or "").strip()
    level = str(row.get("level") or "").strip()
    if not code:
        return None
    stmt = (
        select(Course)
        .join(Department, Department.id == Course.department_id)
        .join(Faculty, Faculty.id == Department.faculty_id)
        .join(University, University.id == Faculty.university_id)
        .where(Course.code == code)
    )
    if level:
        stmt = stmt.where(Course.level == level)
    if row.get("department"):
        stmt = stmt.where(Department.name == row["department"])
    if row.get("university"):
        stmt = stmt.where(University.name == row["university"])
    return db.scalar(stmt.limit(1))


def _import_materials(db: Session, rows: list[dict], counts: SectionCounts) -> dict[str, int]:
    for row in rows:
        counts.read += 1
        course = _find_course(db, row)
        title = (row.get("title") or "").strip()[:255]
        if course is None or not title:
            counts.errors.append(f"material {title!r}: course not found")
            continue
        exists = db.scalar(
            select(Material).where(Material.course_id == course.id, Material.title == title)
        )
        if exists is not None:
            counts.skipped += 1
            continue
        db.add(
            Material(
                course_id=course.id,
                title=title,
                file_url=(row.get("file_url") or None),
                source="v1_import",
            )
        )
        db.flush()
        counts.created += 1
    return {"created": counts.created, "skipped": counts.skipped}


def _import_questions(db: Session, rows: list[dict], counts: SectionCounts) -> dict[str, int]:
    import hashlib as _hashlib

    for row in rows:
        counts.read += 1
        course = _find_course(db, row)
        prompt = (row.get("prompt") or "").strip()
        options = row.get("options")
        correct_key = (row.get("correct_key") or "").strip()
        if course is None or not prompt or not isinstance(options, list) or not correct_key:
            counts.errors.append(f"question {prompt[:40]!r}: incomplete row")
            continue
        if correct_key not in {str(option.get("key")) for option in options if isinstance(option, dict)}:
            counts.errors.append(f"question {prompt[:40]!r}: correct_key not in options")
            continue
        fingerprint = _hashlib.sha256(f"{course.id}:{prompt}".encode()).hexdigest()
        # Cheap duplicate check without a new column: compare the prompt for the course.
        exists = db.scalar(
            select(Question.id).where(Question.course_id == course.id, Question.prompt == prompt)
        )
        if exists is not None:
            counts.skipped += 1
            continue
        db.add(
            Question(
                course_id=course.id,
                prompt=prompt,
                options=options,
                correct_key=correct_key,
                explanation=(row.get("explanation") or None),
                difficulty=(row.get("difficulty") or "medium")[:10],
                source="v1_import",
            )
        )
        db.flush()
        counts.created += 1
        _ = fingerprint  # kept for a future stable external id column
    return {"created": counts.created, "skipped": counts.skipped}


# --- skills ------------------------------------------------------------------


def _import_skills(db: Session, rows: list[dict], counts: SectionCounts) -> dict[str, int]:
    for row in rows:
        counts.read += 1
        slug = (row.get("slug") or _slug(row.get("name") or ""))[:80]
        name = (row.get("name") or "").strip()[:120]
        if not slug or not name:
            counts.errors.append("skill without a name")
            continue

        category_name = (row.get("category") or "General").strip()[:120]
        category_slug = _slug(category_name)[:80]
        category = db.scalar(select(SkillCategory).where(SkillCategory.slug == category_slug))
        if category is None:
            category = SkillCategory(slug=category_slug, name=category_name, description=None)
            db.add(category)
            db.flush()

        skill = db.scalar(select(Skill).where(Skill.slug == slug))
        if skill is None:
            skill = Skill(
                category_id=category.id,
                slug=slug,
                name=name,
                description=(row.get("description") or None),
            )
            db.add(skill)
            db.flush()
            counts.created += 1
        else:
            counts.skipped += 1

        for path_row in row.get("paths") or []:
            _import_path(db, skill, path_row, counts)
    return {"created": counts.created, "skipped": counts.skipped}


def _import_path(db: Session, skill: Skill, row: dict, counts: SectionCounts) -> None:
    path_slug = (row.get("slug") or _slug(row.get("title") or ""))[:80]
    title = (row.get("title") or "").strip()[:200]
    if not path_slug or not title:
        return
    path = db.scalar(select(LearningPath).where(LearningPath.slug == path_slug))
    if path is None:
        path = LearningPath(
            skill_id=skill.id,
            slug=path_slug,
            title=title,
            summary=(row.get("summary") or None),
            level=(row.get("level") or "beginner")[:20],
            status=STATUS_PUBLISHED,
        )
        db.add(path)
        db.flush()
        counts.created += 1
    else:
        counts.skipped += 1

    existing_steps = db.scalar(
        select(LearningPathStep.id).where(LearningPathStep.path_id == path.id).limit(1)
    )
    if existing_steps is not None:
        return

    for ordinal, lesson_row in enumerate(row.get("lessons") or [], start=1):
        lesson_slug = (lesson_row.get("slug") or _slug(lesson_row.get("title") or ""))[:80]
        lesson_title = (lesson_row.get("title") or "").strip()[:200]
        if not lesson_slug or not lesson_title:
            continue
        lesson = db.scalar(select(Lesson).where(Lesson.slug == lesson_slug))
        if lesson is None:
            lesson = Lesson(
                skill_id=skill.id,
                slug=lesson_slug,
                title=lesson_title,
                body_md=lesson_row.get("body_md") or "",
                status=STATUS_PUBLISHED,
            )
            db.add(lesson)
            db.flush()
            counts.created += 1
        db.add(
            LearningPathStep(
                path_id=path.id, ordinal=ordinal, kind="lesson", title=lesson_title,
                lesson_id=lesson.id,
            )
        )
        db.flush()


# --- run ---------------------------------------------------------------------


def run_import(
    db: Session,
    *,
    data: dict,
    mode: str = IMPORT_DRY_RUN,
    source: str = "v1_export",
    created_by: int | None = None,
) -> ImportRun:
    if mode not in {IMPORT_DRY_RUN, IMPORT_APPLY}:
        raise ApiError(400, "invalid_import_mode", "Import mode must be dry_run or apply.")
    if not isinstance(data, dict):
        raise ApiError(400, "export_invalid", "The export must be a JSON object.")

    run = ImportRun(source=source, mode=mode, created_by=created_by, status=IMPORT_DONE)
    db.add(run)
    db.flush()

    counts: dict[str, dict] = {}
    checksums: dict[str, str] = {}
    errors: list[str] = []

    savepoint = db.begin_nested()
    try:
        users = data.get("users") or []
        taxonomy = data.get("taxonomy") or []
        materials = data.get("materials") or []
        questions = data.get("questions") or []
        skills = data.get("skills") or []

        for section, rows in (
            ("users", users),
            ("taxonomy", taxonomy),
            ("materials", materials),
            ("questions", questions),
            ("skills", skills),
        ):
            checksums[section] = checksum(rows)

        user_counts = SectionCounts()
        _import_users(db, users, user_counts)
        counts["users"] = user_counts.as_dict()

        taxonomy_counts = SectionCounts()
        _import_taxonomy(db, taxonomy, taxonomy_counts)
        counts["taxonomy"] = taxonomy_counts.as_dict()

        material_counts = SectionCounts()
        _import_materials(db, materials, material_counts)
        counts["materials"] = material_counts.as_dict()

        question_counts = SectionCounts()
        _import_questions(db, questions, question_counts)
        counts["questions"] = question_counts.as_dict()

        skill_counts = SectionCounts()
        _import_skills(db, skills, skill_counts)
        counts["skills"] = skill_counts.as_dict()

        errors = [
            f"{section}: {message}"
            for section in counts
            for message in counts[section]["errors"]
        ]
        db.flush()

        if mode == IMPORT_DRY_RUN:
            savepoint.rollback()
        else:
            savepoint.commit()
    except Exception as exc:  # noqa: BLE001 - the run must record the failure
        savepoint.rollback()
        run.status = IMPORT_FAILED
        run.finished_at = utcnow()
        run.counts = counts or None
        run.checksums = checksums or None
        run.errors = [f"{type(exc).__name__}: {exc}"]
        db.flush()
        raise

    run.counts = counts
    run.checksums = checksums
    run.errors = errors or None
    run.finished_at = utcnow()
    run.status = IMPORT_DONE
    db.flush()
    return run


def reconciliation(run: ImportRun, v1_counts: dict[str, int] | None = None) -> dict:
    """Compare what V2 imported with what V1 says it exported."""
    imported = run.counts or {}
    report = {
        "run_id": run.id,
        "mode": run.mode,
        "source": run.source,
        "checksums": run.checksums or {},
        "sections": {},
        "balanced": True,
    }
    for section in SECTIONS:
        section_counts = imported.get(section) or {}
        expected = (v1_counts or {}).get(section)
        actual = section_counts.get("created", 0) + section_counts.get("updated", 0)
        matched = expected is None or expected == actual
        if not matched:
            report["balanced"] = False
        report["sections"][section] = {
            "expected": expected,
            "actual": actual,
            "skipped": section_counts.get("skipped", 0),
            "errors": len(section_counts.get("errors") or []),
            "matched": matched,
        }
    return report


def _slug(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "-" for ch in value.strip())
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-") or "item"


# `Assessment` is imported so a future export section can create assessments
# without changing the importer's public surface.
__all__ = [
    "Assessment",
    "AssessmentTask",
    "SECTIONS",
    "checksum",
    "load_export",
    "reconciliation",
    "run_import",
]
