"""Read a V1 Postgres database and write the JSON shape the V2 importer expects.

    $env:V1_DATABASE_URL = "<V1 external Postgres URL>"
    $env:PRODGUARD_ALLOW = "1"   # a remote database is treated as production
    apps/api/.venv/Scripts/python.exe -m tools.export_v1 --out v1-export.json

This tool is **read-only**: it sets the transaction read-only before it queries
anything. It never imports V1's Flask app and never writes to V1.

The output is consumed by Admin -> Imports (dry run first) or by
``app.services.imports.v1.run_import``.

If a table is missing, that section is exported empty and the reason is listed in
``meta.warnings`` so the operator can see it before applying.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sqlalchemy import MetaData, Table, create_engine, select, text
from sqlalchemy.exc import NoSuchTableError, SQLAlchemyError

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tools.prodguard import guard  # noqa: E402

TABLES = (
    "user",
    "universities",
    "faculties",
    "departments",
    "courses",
    "materials",
    "cbt_questions",
    "skill_categories",
    "skills",
    "learning_paths",
    "learning_path_steps",
    "skill_courses",
    "course_modules",
    "lessons",
)

_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# V1's seeded material PDFs live under app/static/materials and are not part of
# V2's web build. Keep those links working by pointing them at the V1 host that
# stays up after cutover, until the files are migrated (post-launch).
V1_PUBLIC_BASE = "https://v1.nelavista.com"


def _slug(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "-" for ch in (value or "").strip())
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-") or "item"


def _get(row: dict, key: str, default: Any = None) -> Any:
    value = row.get(key, default)
    return default if value is None else value


def _absolute_v1_url(value: Any) -> str:
    """Turn a relative V1 /static path into a link that still works after cutover."""
    url = str(value or "").strip()
    if url.startswith("/static/"):
        return f"{V1_PUBLIC_BASE}{url}"
    if url.startswith("static/"):
        return f"{V1_PUBLIC_BASE}/{url}"
    return url


def _html_to_markdown(value: Any) -> str:
    """Convert the HTML V1 lessons store into the Markdown subset V2 renders.

    V2 deliberately parses a small Markdown subset rather than rendering HTML
    (no sanitiser in the bundle), so importing V1 HTML as-is would show raw tags.
    This handles the tags V1's lesson editor actually writes; unknown tags are
    stripped, never passed through.
    """
    text = str(value or "")
    if "<" not in text:
        return text.strip()

    text = re.sub(r"<\s*pre[^>]*>\s*<\s*code[^>]*>", "\n```\n", text, flags=re.I)
    text = re.sub(r"<\s*/\s*code\s*>\s*<\s*/\s*pre\s*>", "\n```\n", text, flags=re.I)
    text = re.sub(r"<\s*br\s*/?>", "\n", text, flags=re.I)
    for level in (1, 2, 3):
        text = re.sub(
            rf"<\s*h{level}[^>]*>", "\n" + "#" * level + " ", text, flags=re.I
        )
    text = re.sub(r"<\s*h[4-6][^>]*>", "\n### ", text, flags=re.I)
    text = re.sub(r"<\s*/\s*h[1-6]\s*>", "\n", text, flags=re.I)
    text = re.sub(r"<\s*li[^>]*>", "\n- ", text, flags=re.I)
    text = re.sub(
        r"<\s*/\s*(p|div|section|article|ul|ol|blockquote)\s*>", "\n", text, flags=re.I
    )
    text = re.sub(r"<\s*(strong|b)[^>]*>", "**", text, flags=re.I)
    text = re.sub(r"<\s*/\s*(strong|b)\s*>", "**", text, flags=re.I)
    text = re.sub(
        r'<\s*a[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a\s*>',
        r"[\2](\1)",
        text,
        flags=re.I | re.S,
    )
    text = re.sub(r"<\s*code[^>]*>", "`", text, flags=re.I)
    text = re.sub(r"<\s*/\s*code\s*>", "`", text, flags=re.I)
    text = re.sub(r"<\s*pre[^>]*>", "\n```\n", text, flags=re.I)
    text = re.sub(r"<\s*/\s*pre\s*>", "\n```\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text).replace("\xa0", " ")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _on(value: Any) -> bool:
    """True for a reflected boolean that is True/1; None and missing are off."""
    return value is True or value == 1


def _off(value: Any) -> bool:
    """True for a reflected boolean that is False/0; None is not off."""
    return value is False or value == 0


def _rows(conn, table: Table | None) -> list[dict]:
    if table is None:
        return []
    stmt = select(table)
    if "id" in table.c:
        stmt = stmt.order_by(table.c.id)
    return [dict(row) for row in conn.execute(stmt).mappings()]


def _tables(conn, warnings: list[str]) -> dict[str, Table | None]:
    found: dict[str, Table | None] = {}
    metadata = MetaData()
    for name in TABLES:
        try:
            found[name] = Table(name, metadata, autoload_with=conn)
        except NoSuchTableError:
            found[name] = None
            warnings.append(f"table {name!r} does not exist; its section is empty")
    return found


def _export_users(users: list[dict], warnings: list[str]) -> list[dict]:
    rows: list[dict] = []
    for row in users:
        if _on(row.get("is_deleted")):
            continue
        email = str(_get(row, "email", "")).strip().lower()
        if not email or "@" not in email:
            warnings.append(f"user {row.get('id')} has no usable email; skipped")
            continue
        rows.append(
            {
                "id": row.get("id"),
                "email": email,
                "username": _get(row, "username", email.split("@")[0]),
                "name": _get(row, "name", ""),
                "email_verified": bool(_get(row, "email_verified", True)),
                "university": _get(row, "university", ""),
                "department": _get(row, "department", ""),
                "level": _get(row, "level", ""),
                "password_hash": _get(row, "password_hash", ""),
            }
        )
    return rows


def _export_taxonomy(
    universities: list[dict],
    faculties: list[dict],
    departments: list[dict],
    courses: list[dict],
    warnings: list[str],
) -> list[dict]:
    fac_by_uni: dict[Any, list[dict]] = {}
    for row in faculties:
        fac_by_uni.setdefault(row.get("university_id"), []).append(row)
    dept_by_fac: dict[Any, list[dict]] = {}
    for row in departments:
        dept_by_fac.setdefault(row.get("faculty_id"), []).append(row)
    course_by_dept: dict[Any, list[dict]] = {}
    for row in courses:
        course_by_dept.setdefault(row.get("department_id"), []).append(row)

    export: list[dict] = []
    for uni in universities:
        name = str(_get(uni, "name", "")).strip()
        if not name:
            warnings.append(f"university {uni.get('id')} has no name; skipped")
            continue
        fac_rows = []
        for fac in sorted(fac_by_uni.get(uni.get("id"), []), key=lambda r: r.get("id") or 0):
            fac_name = str(_get(fac, "name", "")).strip()
            if not fac_name:
                continue
            dept_rows = []
            for dept in sorted(dept_by_fac.get(fac.get("id"), []), key=lambda r: r.get("id") or 0):
                dept_name = str(_get(dept, "name", "")).strip()
                if not dept_name:
                    continue
                course_rows = []
                for course in sorted(course_by_dept.get(dept.get("id"), []), key=lambda r: r.get("id") or 0):
                    code = str(_get(course, "code", "")).strip()
                    title = str(_get(course, "title", "")).strip()
                    if not code or not title:
                        continue
                    course_rows.append(
                        {
                            "code": code,
                            "title": title,
                            "level": str(_get(course, "level", "")).strip(),
                        }
                    )
                dept_rows.append({"name": dept_name, "courses": course_rows})
            fac_rows.append({"name": fac_name, "departments": dept_rows})
        export.append(
            {
                "name": name,
                "slug": str(_get(uni, "slug", "")) or _slug(name),
                "faculties": fac_rows,
            }
        )
    return export


def _context(
    row: dict,
    courses: dict[Any, dict],
    courses_by_code: dict[str, list[dict]],
    departments: dict[Any, dict],
    faculties: dict[Any, dict],
    universities: dict[Any, dict],
) -> dict[str, str]:
    course = courses.get(row.get("course_id"))
    if course is None:
        code = str(_get(row, "course_code", "")).strip().lower()
        candidates = courses_by_code.get(code, [])
        for candidate in candidates:
            dept = departments.get(candidate.get("department_id"))
            fac = faculties.get(dept.get("faculty_id")) if dept else None
            uni = universities.get(fac.get("university_id")) if fac else None
            if row.get("department") and dept and dept.get("name") != row.get("department"):
                continue
            if row.get("university") and uni and uni.get("name") != row.get("university"):
                continue
            course = candidate
            break
        if course is None and candidates:
            course = candidates[0]
    if course:
        dept = departments.get(course.get("department_id"))
        fac = faculties.get(dept.get("faculty_id")) if dept else None
        uni = universities.get(fac.get("university_id")) if fac else None
        return {
            "course_code": str(_get(course, "code", "")).strip(),
            "level": str(_get(course, "level", "")).strip(),
            "department": str(_get(dept or {}, "name", "")).strip(),
            "university": str(_get(uni or {}, "name", "")).strip(),
        }
    return {
        "course_code": str(_get(row, "course_code", "")).strip(),
        "level": str(_get(row, "level", "")).strip(),
        "department": str(_get(row, "department", "")).strip(),
        "university": str(_get(row, "university", "")).strip(),
    }


def _export_materials(
    materials: list[dict],
    courses: dict[Any, dict],
    courses_by_code: dict[str, list[dict]],
    departments: dict[Any, dict],
    faculties: dict[Any, dict],
    universities: dict[Any, dict],
    warnings: list[str],
) -> list[dict]:
    rows: list[dict] = []
    static_count = 0
    for row in materials:
        if _off(row.get("is_approved")):
            continue
        title = str(_get(row, "title", "")).strip()
        context = _context(
            row, courses, courses_by_code, departments, faculties, universities
        )
        url = _absolute_v1_url(
            _get(row, "file_url", "") or _get(row, "external_url", "")
        )
        if url.startswith(V1_PUBLIC_BASE):
            static_count += 1
        if not title:
            warnings.append(f"material {row.get('id')} has no title; skipped")
            continue
        if not context["course_code"]:
            warnings.append(f"material {row.get('id')} has no course code; skipped")
            continue
        if not url:
            warnings.append(f"material {row.get('id')} has no file URL; skipped")
            continue
        rows.append(
            {
                "title": title,
                "file_url": url,
                **context,
            }
        )
    if static_count:
        warnings.append(
            f"{static_count} materials point at V1's /static files and were rewritten "
            f"to {V1_PUBLIC_BASE}/static/...; keep V1 running until those files are migrated"
        )
    return rows


def _option_rows(raw: Any) -> list[dict]:
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except ValueError:
            return []
    if not isinstance(raw, list):
        return []
    rows: list[dict] = []
    for index, option in enumerate(raw):
        key = _LETTERS[index] if index < len(_LETTERS) else str(index + 1)
        if isinstance(option, dict):
            text = option.get("text") or option.get("label") or option.get("value") or ""
            key = str(option.get("key") or key)
        else:
            text = str(option)
        rows.append({"key": key, "text": str(text)})
    return rows


def _export_questions(
    questions: list[dict],
    courses: dict[Any, dict],
    courses_by_code: dict[str, list[dict]],
    departments: dict[Any, dict],
    faculties: dict[Any, dict],
    universities: dict[Any, dict],
    warnings: list[str],
) -> list[dict]:
    rows: list[dict] = []
    for row in questions:
        if _off(row.get("is_active")):
            continue
        if str(_get(row, "question_type", "cbt")).lower() != "cbt":
            continue
        prompt = str(_get(row, "question_text", "")).strip()
        options = _option_rows(row.get("options_json"))
        index = row.get("correct_index")
        context = _context(
            row, courses, courses_by_code, departments, faculties, universities
        )
        if not prompt or not options or not context["course_code"]:
            warnings.append(f"question {row.get('id')} is incomplete; skipped")
            continue
        if not isinstance(index, int) or not (0 <= index < len(options)):
            warnings.append(f"question {row.get('id')} has no valid correct_index; skipped")
            continue
        rows.append(
            {
                "prompt": prompt,
                "options": options,
                "correct_key": options[index]["key"],
                "explanation": _get(row, "explanation", ""),
                "difficulty": str(_get(row, "difficulty", "medium") or "medium"),
                **context,
            }
        )
    return rows


def _export_skills(
    categories: list[dict],
    skills: list[dict],
    paths: list[dict],
    steps: list[dict],
    skill_courses: list[dict],
    modules: list[dict],
    lessons: list[dict],
    warnings: list[str],
) -> list[dict]:
    category_name = {row.get("id"): _get(row, "name", "General") for row in categories}
    path_by_skill = {row.get("skill_id"): row for row in paths}
    steps_by_path: dict[Any, list[dict]] = {}
    for row in steps:
        steps_by_path.setdefault(row.get("path_id"), []).append(row)
    modules_by_course: dict[Any, list[dict]] = {}
    for row in modules:
        modules_by_course.setdefault(row.get("course_id"), []).append(row)
    lessons_by_module: dict[Any, list[dict]] = {}
    for row in lessons:
        lessons_by_module.setdefault(row.get("module_id"), []).append(row)
    courses_by_skill: dict[Any, list[dict]] = {}
    for row in skill_courses:
        courses_by_skill.setdefault(row.get("skill_id"), []).append(row)

    used_lesson_slugs: set[str] = set()
    converted_html = 0

    def add_lessons(target: list[dict], course_ids: list[Any]) -> None:
        nonlocal converted_html
        for course_id in course_ids:
            mods = sorted(modules_by_course.get(course_id, []), key=lambda r: r.get("order") or 0)
            for module in mods:
                for lesson in sorted(
                    lessons_by_module.get(module.get("id"), []), key=lambda r: r.get("order") or 0
                ):
                    if _off(lesson.get("is_published")):
                        continue
                    title = str(_get(lesson, "title", "")).strip()
                    if not title:
                        continue
                    slug = _slug(str(_get(lesson, "slug", "")) or title)
                    candidate = slug
                    suffix = 1
                    while candidate in used_lesson_slugs:
                        suffix += 1
                        candidate = f"{slug}-{suffix}"
                    used_lesson_slugs.add(candidate)
                    raw_body = str(_get(lesson, "content", ""))
                    if "<" in raw_body:
                        converted_html += 1
                    target.append(
                        {
                            "slug": candidate,
                            "title": title,
                            "body_md": _html_to_markdown(raw_body),
                        }
                    )

    export: list[dict] = []
    for skill in skills:
        if _off(skill.get("is_published")):
            continue
        name = str(_get(skill, "name", "")).strip()
        slug = _slug(str(_get(skill, "slug", "")) or name)
        if not name or not slug:
            warnings.append(f"skill {skill.get('id')} has no name; skipped")
            continue
        path = path_by_skill.get(skill.get("id")) or {}
        path_steps = sorted(steps_by_path.get(path.get("id"), []), key=lambda r: r.get("order") or 0)
        course_ids = [
            step.get("course_id")
            for step in path_steps
            if step.get("step_type") == "course" and step.get("course_id")
        ]
        if not course_ids:
            courses = sorted(
                courses_by_skill.get(skill.get("id"), []),
                key=lambda r: r.get("order") or 0,
            )
            course_ids = [
                row.get("id") for row in courses if not _off(row.get("is_published"))
            ]
        lesson_rows: list[dict] = []
        add_lessons(lesson_rows, course_ids)
        export.append(
            {
                "slug": slug,
                "name": name,
                "category": category_name.get(skill.get("category_id"), "General"),
                "description": _get(skill, "description", "") or _get(skill, "tagline", ""),
                "paths": [
                    {
                        "slug": f"{slug}-path",
                        "title": _get(path, "title", f"{name}: learning path"),
                        "summary": _get(path, "description", "") or _get(skill, "description", ""),
                        "level": str(_get(skill, "level", "beginner") or "beginner"),
                        "lessons": lesson_rows,
                    }
                ],
            }
        )
    if converted_html:
        warnings.append(
            f"{converted_html} V1 lessons were HTML; converted to the Markdown subset V2 renders"
        )
    return export


def build_export(conn, warnings: list[str]) -> dict:
    tables = _tables(conn, warnings)
    users = _rows(conn, tables["user"])
    universities = _rows(conn, tables["universities"])
    faculties = _rows(conn, tables["faculties"])
    departments = _rows(conn, tables["departments"])
    courses = _rows(conn, tables["courses"])
    materials = _rows(conn, tables["materials"])
    questions = _rows(conn, tables["cbt_questions"])
    categories = _rows(conn, tables["skill_categories"])
    skills = _rows(conn, tables["skills"])
    paths = _rows(conn, tables["learning_paths"])
    steps = _rows(conn, tables["learning_path_steps"])
    skill_courses = _rows(conn, tables["skill_courses"])
    modules = _rows(conn, tables["course_modules"])
    lessons = _rows(conn, tables["lessons"])

    course_by_id = {row.get("id"): row for row in courses}
    courses_by_code: dict[str, list[dict]] = {}
    for row in courses:
        code = str(row.get("code") or "").strip().lower()
        if code:
            courses_by_code.setdefault(code, []).append(row)
    dept_by_id = {row.get("id"): row for row in departments}
    fac_by_id = {row.get("id"): row for row in faculties}
    uni_by_id = {row.get("id"): row for row in universities}

    data = {
        "users": _export_users(users, warnings),
        "taxonomy": _export_taxonomy(universities, faculties, departments, courses, warnings),
        "materials": _export_materials(
            materials,
            course_by_id,
            courses_by_code,
            dept_by_id,
            fac_by_id,
            uni_by_id,
            warnings,
        ),
        "questions": _export_questions(
            questions,
            course_by_id,
            courses_by_code,
            dept_by_id,
            fac_by_id,
            uni_by_id,
            warnings,
        ),
        "skills": _export_skills(
            categories, skills, paths, steps, skill_courses, modules, lessons, warnings
        ),
    }
    data["meta"] = {
        "source": "v1",
        "exported_at": datetime.now(UTC).isoformat(),
        "counts": {
            "users": len(data["users"]),
            "taxonomy": len(data["taxonomy"]),
            "materials": len(data["materials"]),
            "questions": len(data["questions"]),
            "skills": len(data["skills"]),
        },
        "warnings": warnings,
    }
    return data


def export_database(database_url: str) -> dict:
    engine = create_engine(database_url, future=True)
    warnings: list[str] = []
    try:
        with engine.connect() as conn:
            # Read-only at the database level, not just by convention.
            if engine.dialect.name == "postgresql":
                conn.execute(text("SET TRANSACTION READ ONLY"))
            elif engine.dialect.name == "sqlite":
                conn.execute(text("PRAGMA query_only = ON"))
            return build_export(conn, warnings)
    finally:
        engine.dispose()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export V1 data for the V2 importer.")
    parser.add_argument(
        "--database-url",
        default=os.environ.get("V1_DATABASE_URL", ""),
        help="V1 Postgres URL (default: V1_DATABASE_URL).",
    )
    parser.add_argument("--out", default="v1-export.json", help="Output JSON path.")
    parser.add_argument(
        "--i-know-this-is-production",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args(argv)

    if not args.database_url:
        parser.error("set V1_DATABASE_URL or pass --database-url")

    guard("export_v1", database_url=args.database_url)
    try:
        data = export_database(args.database_url)
    except SQLAlchemyError as exc:
        sys.stderr.write(f"Could not read V1: {type(exc).__name__}: {exc}\n")
        return 2

    out = Path(args.out)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    counts = data["meta"]["counts"]
    print(f"Wrote {out} ({', '.join(f'{k}={v}' for k, v in counts.items())})")
    for warning in data["meta"]["warnings"][:20]:
        print(f"warning: {warning}")
    if len(data["meta"]["warnings"]) > 20:
        print(f"... and {len(data['meta']['warnings']) - 20} more warnings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
