"""The language profile: self-reported claims vs verified capabilities."""

from __future__ import annotations

from factories import make_skill, make_user, verify

from app.core.security import create_access_token
from app.models.skills import SkillCategory

PREFIX = "/v1"


def _headers(user) -> dict:
    return {"Authorization": f"Bearer {create_access_token(user.id, user.role.code if user.role else None)}"}


def test_language_profile_keeps_self_reported_capabilities_editable(api) -> None:
    client, db = api
    student = make_user(db)

    response = client.put(
        f"{PREFIX}/skills/languages",
        json={
            "languages": [
                {
                    "language": "Yoruba",
                    "level": "native",
                    "dialect": "Ekiti",
                    "can_speak": True,
                    "can_read": True,
                    "can_write": False,
                    "can_transcribe": True,
                    "can_translate": False,
                }
            ]
        },
        headers=_headers(student),
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert len(body["languages"]) == 1
    row = body["languages"][0]
    assert row["language"] == "yoruba"
    assert row["dialect"] == "Ekiti"
    assert row["proficiency"] == "native"
    assert set(row["self_reported"]) == {"can_speak", "can_read", "can_transcribe"}
    assert row["verified"] == []
    assert {item["key"] for item in body["capabilities"]} == {
        "can_speak",
        "can_read",
        "can_write",
        "can_transcribe",
        "can_translate",
    }


def test_verified_capabilities_are_derived_from_verified_skills(api) -> None:
    client, db = api
    student = make_user(db)

    client.put(
        f"{PREFIX}/skills/languages",
        json={"languages": [{"language": "Yoruba", "level": "fluent", "can_speak": True}]},
        headers=_headers(student),
    )

    category = SkillCategory(
        slug="transcription", name="Transcription", program="all", ordinal=20
    )
    db.add(category)
    db.flush()
    skill = make_skill(
        db,
        slug="yoruba-transcription",
        name="Yoruba Transcription",
        language="yoruba",
        category_id=category.id,
    )
    verify(db, student, skill)
    db.flush()

    body = client.get(f"{PREFIX}/skills/languages", headers=_headers(student)).json()
    row = body["languages"][0]
    assert "can_transcribe" in row["verified"]
    assert "can_transcribe" not in row["self_reported"]
    assert [item["slug"] for item in row["verified_skills"]] == ["yoruba-transcription"]

    # A profile edit cannot write the verified side.
    client.put(
        f"{PREFIX}/skills/languages",
        json={
            "languages": [
                {"language": "Yoruba", "level": "fluent", "can_translate": True}
            ]
        },
        headers=_headers(student),
    )
    row = client.get(f"{PREFIX}/skills/languages", headers=_headers(student)).json()["languages"][0]
    assert "can_transcribe" in row["verified"]
    assert set(row["self_reported"]) == {"can_translate"}


def test_the_simple_settings_editor_does_not_erase_the_richer_profile(api) -> None:
    client, db = api
    student = make_user(db)
    headers = _headers(student)

    client.put(
        f"{PREFIX}/skills/languages",
        json={
            "languages": [
                {
                    "language": "Igbo",
                    "level": "fluent",
                    "dialect": "Nsukka",
                    "can_speak": True,
                    "can_translate": True,
                }
            ]
        },
        headers=headers,
    )
    # Settings sends only name + level; the capability claims and dialect stay.
    response = client.put(
        f"{PREFIX}/me/languages",
        json={"languages": [{"language": "igbo", "level": "native"}]},
        headers=headers,
    )
    assert response.status_code == 200, response.text

    row = client.get(f"{PREFIX}/skills/languages", headers=headers).json()["languages"][0]
    assert row["proficiency"] == "native"
    assert row["dialect"] == "Nsukka"
    assert set(row["self_reported"]) == {"can_speak", "can_translate"}


def test_duplicate_and_unknown_values_are_rejected(api) -> None:
    client, db = api
    student = make_user(db)
    headers = _headers(student)

    duplicate = client.put(
        f"{PREFIX}/skills/languages",
        json={
            "languages": [
                {"language": "Hausa", "level": "fluent"},
                {"language": "hausa", "level": "basic"},
            ]
        },
        headers=headers,
    )
    assert duplicate.status_code == 400

    unknown_level = client.put(
        f"{PREFIX}/skills/languages",
        json={"languages": [{"language": "Hausa", "level": "expert"}]},
        headers=headers,
    )
    assert unknown_level.status_code == 400
