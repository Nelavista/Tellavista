"""The catalog filters and the ALL hub read (I1/I4).

Filters are applied by the API, not the client, so web and mobile cannot disagree
about what a programme or level contains. These tests build the rows they filter
on rather than trusting the seed.
"""

from __future__ import annotations

from factories import make_skill, make_user

from app.core.security import create_access_token
from app.models.skills import (
    STATUS_PUBLISHED,
    CareerTrack,
    CareerTrackStep,
    LearningPath,
    SkillCategory,
)

PREFIX = "/v1"


def _headers(user) -> dict:
    return {
        "Authorization": f"Bearer {create_access_token(user.id, user.role.code if user.role else None)}"
    }


def _path(db, skill, level: str, status: str = STATUS_PUBLISHED) -> LearningPath:
    row = LearningPath(
        skill_id=skill.id,
        slug=f"{skill.slug}-{level}",
        title=f"{skill.name} ({level})",
        level=level,
        status=status,
    )
    db.add(row)
    db.flush()
    return row


def test_catalog_filters_by_programme_language_tag_and_level(api) -> None:
    client, db = api
    student = make_user(db)
    headers = _headers(student)

    all_category = SkillCategory(slug="transcription", name="Transcription", program="all", ordinal=20)
    core_category = SkillCategory(slug="annotation", name="Annotation", program="core", ordinal=1)
    db.add_all([all_category, core_category])
    db.flush()

    yoruba = make_skill(
        db,
        slug="yoruba-transcription",
        name="Yoruba Transcription",
        description="Turn Yoruba speech into text.",
        language="yoruba",
        tags=["speech", "text"],
        category_id=all_category.id,
    )
    tag_only = make_skill(
        db,
        slug="general-annotation",
        name="General Annotation",
        language=None,
        tags=["text"],
        category_id=core_category.id,
    )
    _path(db, yoruba, "beginner")
    _path(db, yoruba, "advanced")
    _path(db, tag_only, "intermediate")

    def rows(**params) -> list[dict]:
        response = client.get(f"{PREFIX}/skills", params=params, headers=headers)
        assert response.status_code == 200, response.text
        return response.json()["skills"]

    assert {row["slug"] for row in rows()} == {"yoruba-transcription", "general-annotation"}

    every = {row["slug"]: row for row in rows()}
    assert every["yoruba-transcription"]["program"] == "all"
    assert every["yoruba-transcription"]["language_label"] == "Yoruba"
    assert every["yoruba-transcription"]["levels"] == ["advanced", "beginner"]
    assert every["general-annotation"]["program"] == "core"

    assert {row["slug"] for row in rows(program="all")} == {"yoruba-transcription"}
    assert {row["slug"] for row in rows(language="yoruba")} == {"yoruba-transcription"}
    assert {row["slug"] for row in rows(tag="text")} == {"yoruba-transcription", "general-annotation"}
    assert {row["slug"] for row in rows(tag="speech")} == {"yoruba-transcription"}
    assert {row["slug"] for row in rows(level="intermediate")} == {"general-annotation"}
    assert {row["slug"] for row in rows(category="annotation")} == {"general-annotation"}
    assert {row["slug"] for row in rows(q="yoruba speech")} == {"yoruba-transcription"}
    assert rows(level="advanced", program="core") == []


def test_a_level_is_only_claimed_when_a_published_path_has_it(api) -> None:
    client, db = api
    student = make_user(db)
    skill = make_skill(db, slug="draft-level", name="Draft Level")
    _path(db, skill, "advanced", status="draft")

    body = client.get(f"{PREFIX}/skills", headers=_headers(student)).json()
    row = next(item for item in body["skills"] if item["slug"] == "draft-level")
    assert row["levels"] == []
    assert client.get(
        f"{PREFIX}/skills", params={"level": "advanced"}, headers=_headers(student)
    ).json()["skills"] == []


def test_career_tracks_return_their_ordered_skills_and_filter(api) -> None:
    client, db = api
    student = make_user(db)
    headers = _headers(student)

    first = make_skill(db, slug="track-first", name="Track First", language="igbo")
    second = make_skill(db, slug="track-second", name="Track Second", language=None)
    other = make_skill(db, slug="other-skill", name="Other Skill", language=None)

    all_track = CareerTrack(
        slug="igbo-specialist",
        title="Igbo Language Data Specialist",
        tagline="Transcribe and translate Igbo data.",
        program="all",
        status=STATUS_PUBLISHED,
    )
    core_track = CareerTrack(
        slug="core-route", title="Core Route", program="core", status=STATUS_PUBLISHED
    )
    db.add_all([all_track, core_track])
    db.flush()
    db.add_all(
        [
            CareerTrackStep(track_id=all_track.id, skill_id=first.id, ordinal=1),
            CareerTrackStep(track_id=all_track.id, skill_id=second.id, ordinal=2),
            CareerTrackStep(track_id=core_track.id, skill_id=other.id, ordinal=1),
        ]
    )
    db.flush()

    body = client.get(f"{PREFIX}/skills/career-tracks", headers=headers).json()
    tracks = {track["slug"]: track for track in body["tracks"]}
    assert set(tracks) == {"igbo-specialist", "core-route"}
    assert [skill["slug"] for skill in tracks["igbo-specialist"]["skills"]] == [
        "track-first",
        "track-second",
    ]
    assert tracks["igbo-specialist"]["skills"][0]["language_label"] == "Igbo"
    assert tracks["igbo-specialist"]["program"] == "all"

    filtered = client.get(
        f"{PREFIX}/skills/career-tracks", params={"program": "all"}, headers=headers
    ).json()["tracks"]
    assert [track["slug"] for track in filtered] == ["igbo-specialist"]

    by_language = client.get(
        f"{PREFIX}/skills/career-tracks", params={"language": "igbo"}, headers=headers
    ).json()["tracks"]
    assert [track["slug"] for track in by_language] == ["igbo-specialist"]

    searched = client.get(
        f"{PREFIX}/skills/career-tracks", params={"q": "core"}, headers=headers
    ).json()["tracks"]
    assert [track["slug"] for track in searched] == ["core-route"]


def test_catalog_and_tracks_require_a_session(api) -> None:
    client, _db = api
    assert client.get(f"{PREFIX}/skills").status_code == 401
    assert client.get(f"{PREFIX}/skills/career-tracks").status_code == 401
