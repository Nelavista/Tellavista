"""The student language profile for language-data work (African Languages Lab).

What a student *says* they can do lives on `UserLanguage` rows and is always
shown as self-reported. What they have *proven* is derived here at read time from
verified language-specific skills, so selecting a language never verifies it and
there is no stored "verified" flag that could drift.

Capability labels are fixed: speak, read, write, transcribe, translate. A verified
skill backs one capability based on its ALL category; the mapping is intentionally
narrow, matching the V1 behaviour.
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.identity import User, UserLanguage
from app.models.skills import Skill, SkillCategory
from app.models.verification import VERIFIED, VerificationRecord
from app.services.identity.profile import LANGUAGE_LEVELS

# key -> display name. Keys are what Skill.language and UserLanguage.language store.
LANGUAGES: dict[str, str] = {
    "yoruba": "Yoruba",
    "igbo": "Igbo",
    "hausa": "Hausa",
    "pidgin": "Nigerian Pidgin",
    "nigerian-english": "Nigerian English",
    "english": "English",
    "edo": "Edo (Bini)",
    "efik": "Efik",
    "ibibio": "Ibibio",
    "tiv": "Tiv",
    "nupe": "Nupe",
    "fulfulde": "Fulfulde",
    "kanuri": "Kanuri",
    "ijaw": "Ijaw",
    "urhobo": "Urhobo",
    "igala": "Igala",
    "idoma": "Idoma",
    "ebira": "Ebira",
    "swahili": "Swahili",
    "amharic": "Amharic",
    "akan": "Akan (Twi)",
    "ewe": "Ewe",
    "wolof": "Wolof",
    "zulu": "isiZulu",
    "xhosa": "isiXhosa",
    "somali": "Somali",
    "french": "French",
    "arabic": "Arabic",
    "portuguese": "Portuguese",
}

PROFICIENCY_LABELS: dict[str, str] = {
    "basic": "Basic",
    "conversational": "Conversational",
    "fluent": "Fluent",
    "native": "Native / first language",
}

CAPABILITIES: tuple[tuple[str, str], ...] = (
    ("can_speak", "Speak"),
    ("can_read", "Read"),
    ("can_write", "Write"),
    ("can_transcribe", "Transcribe"),
    ("can_translate", "Translate"),
)

# Which self-reported capability a verified skill in each ALL category backs up.
_CATEGORY_CAPABILITY: dict[str, str] = {
    "transcription": "can_transcribe",
    "translation": "can_translate",
    "speech-voice-data": "can_speak",
}


def language_label(key: str | None) -> str | None:
    if not key:
        return None
    return LANGUAGES.get(key, key.replace("-", " ").title())


def normalize_language_key(raw: str | None) -> str | None:
    text = (raw or "").strip().lower()
    if not text:
        return None
    for key, label in LANGUAGES.items():
        if text in (key, label.lower()):
            return key
    return "-".join(text.split())[:60]


def _verified_skills_by_language(
    db: Session, user: User
) -> dict[str, list[tuple[Skill, str | None]]]:
    rows = db.execute(
        select(Skill, SkillCategory.slug)
        .join(VerificationRecord, VerificationRecord.skill_id == Skill.id)
        .outerjoin(SkillCategory, SkillCategory.id == Skill.category_id)
        .where(
            VerificationRecord.user_id == user.id,
            VerificationRecord.status == VERIFIED,
            Skill.language.isnot(None),
        )
    ).all()
    grouped: dict[str, list[tuple[Skill, str | None]]] = {}
    for skill, category_slug in rows:
        if skill.language:
            grouped.setdefault(skill.language, []).append((skill, category_slug))
    return grouped


def get_language_profile(db: Session, user: User) -> list[dict]:
    """One entry per language row: the self-reported claims plus what is proven."""
    rows = list(
        db.scalars(
            select(UserLanguage)
            .where(UserLanguage.user_id == user.id)
            .order_by(UserLanguage.language)
        )
    )
    if not rows:
        return []

    verified_by_language = _verified_skills_by_language(db, user)
    profile: list[dict] = []
    for row in rows:
        verified_skills = verified_by_language.get(row.language, [])
        verified_keys = {
            _CATEGORY_CAPABILITY[category_slug]
            for _skill, category_slug in verified_skills
            if category_slug in _CATEGORY_CAPABILITY
        }
        profile.append(
            {
                "language": row.language,
                "label": language_label(row.language),
                "dialect": row.dialect,
                "proficiency": row.level,
                "proficiency_label": PROFICIENCY_LABELS.get(row.level, row.level),
                "self_reported": [key for key, _ in CAPABILITIES if getattr(row, key)],
                "verified": [key for key, _ in CAPABILITIES if key in verified_keys],
                "verified_skills": [
                    {"id": skill.id, "slug": skill.slug, "name": skill.name}
                    for skill, _category_slug in verified_skills
                ],
            }
        )
    return profile


def set_language_profile(db: Session, user: User, entries: list[dict]) -> list[dict]:
    """Replace the self-reported language profile.

    Capabilities are self-reported claims only. No amount of checking a box can
    make a capability verified; that comes from `VerificationRecord`.
    """
    seen: set[str] = set()
    cleaned: list[dict] = []
    for entry in entries:
        name = str(entry.get("language") or "").strip()
        key = normalize_language_key(name)
        if not key:
            raise ApiError(400, "invalid_language", "Language cannot be empty.")
        if key in seen:
            raise ApiError(400, "duplicate_language", f"{name} is listed twice.")
        level = str(entry.get("level") or "fluent").strip()
        if level not in LANGUAGE_LEVELS:
            raise ApiError(400, "invalid_language_level", "Unknown language level.")
        dialect = str(entry.get("dialect") or "").strip()[:60] or None
        seen.add(key)
        cleaned.append(
            {
                "language": key[:60],
                "level": level,
                "dialect": dialect,
                **{capability: bool(entry.get(capability)) for capability, _ in CAPABILITIES},
            }
        )

    for row in db.scalars(select(UserLanguage).where(UserLanguage.user_id == user.id)):
        db.delete(row)
    db.flush()

    db.add_all([UserLanguage(user_id=user.id, **values) for values in cleaned])
    db.flush()
    return get_language_profile(db, user)


def catalog() -> list[dict]:
    return [{"key": key, "label": label} for key, label in LANGUAGES.items()]
