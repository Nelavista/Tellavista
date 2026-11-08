"""Deterministic scoring for the four African Languages Lab task kinds."""

from __future__ import annotations

from app.services.skills.language_tasks import (
    chrf,
    public_task_spec,
    score_task,
    validate_task_spec,
    word_error_rate,
)
from app.services.skills.tasks import validate

LABELING_SPEC = {
    "kind": "labeling",
    "items": [
        {
            "id": "a1",
            "text": "This phone sweet well well!",
            "fields": [
                {
                    "name": "sentiment",
                    "label": "Sentiment",
                    "type": "choice",
                    "options": ["Positive", "Negative", "Neutral"],
                    "expected": "Positive",
                }
            ],
        },
        {
            "id": "a2",
            "text": "The meeting is at 4pm.",
            "fields": [
                {
                    "name": "sentiment",
                    "label": "Sentiment",
                    "type": "choice",
                    "options": ["Positive", "Negative", "Neutral"],
                    "expected": "Neutral",
                }
            ],
        },
        {
            "id": "r1",
            "text": "Repeat of a1",
            "repeat_of": "a1",
            "fields": [
                {
                    "name": "sentiment",
                    "label": "Sentiment",
                    "type": "choice",
                    "options": ["Positive", "Negative", "Neutral"],
                    "expected": "Positive",
                }
            ],
        },
    ],
}

TRANSCRIPTION_SPEC = {
    "kind": "transcription",
    "mode": "clean",
    "segments": [
        {"id": "s1", "reference": "Mo fe lo si oja"},
        {"id": "s2", "reference": "E kaaro, se daadaa ni?"},
    ],
}

TRANSLATION_SPEC = {
    "kind": "translation",
    "source_lang": "Yoruba",
    "target_lang": "English",
    "items": [
        {
            "id": "t1",
            "source": "E kaaro",
            "references": ["Good morning"],
            "key_terms": ["morning"],
        }
    ],
}

RECORDING_SPEC = {
    "kind": "recording",
    "prompts": [{"id": "p1", "text": "Read this sentence aloud."}],
    "requirements": {
        "min_seconds": 1.5,
        "max_seconds": 10,
        "max_clip_pct": 0.5,
        "min_rms_db": -40,
        "max_silence_pct": 60,
    },
    "metadata_fields": [{"name": "dialect", "label": "Your dialect"}],
}


def test_word_error_rate_and_chrf_are_deterministic() -> None:
    assert word_error_rate("the cat sat", "the cat sat") == 0
    assert round(word_error_rate("the cat sat", "the cat sit"), 3) == 0.333
    assert round(chrf("Good morning", "Good morning")) == 100
    assert chrf("Good morning", "Good night") < 80
    assert chrf("Good morning", "Good morning") == chrf("Good morning", "Good morning")


def test_labeling_scores_every_field_and_repeat_consistency() -> None:
    correct = {
        "a1": {"sentiment": "Positive"},
        "a2": {"sentiment": "Neutral"},
        "r1": {"sentiment": "Positive"},
    }
    result = score_task(LABELING_SPEC, correct)
    assert result.score == 100
    assert result.is_correct is True
    assert result.summary["consistency"] == 100

    mixed = {
        "a1": {"sentiment": "Positive"},
        "a2": {"sentiment": "Negative"},
        # The repeated item disagrees with the first answer.
        "r1": {"sentiment": "Negative"},
    }
    result = score_task(LABELING_SPEC, mixed)
    assert result.score == 33
    assert result.summary["correct"] == 1
    assert result.summary["total"] == 3
    assert result.summary["consistency"] == 0
    assert result.is_correct is False


def test_labeling_report_is_part_of_the_score() -> None:
    spec = {
        **LABELING_SPEC,
        "items": [LABELING_SPEC["items"][0]],
        "report": {"label": "Explain", "min_words": 5},
    }
    short = score_task(spec, {"a1": {"sentiment": "Positive"}, "report": "too short"})
    long = score_task(
        spec,
        {"a1": {"sentiment": "Positive"}, "report": "this report has enough words to count"},
    )
    assert short.score == 90
    assert long.score == 100


def test_transcription_uses_partial_word_accuracy_not_a_binary_mark() -> None:
    exact = score_task(
        TRANSCRIPTION_SPEC,
        {"s1": "Mo fe lo si oja", "s2": "E kaaro, se daadaa ni?"},
    )
    assert exact.score == 100
    assert exact.summary["word_error_rate"] == 0

    partial = score_task(
        TRANSCRIPTION_SPEC,
        {"s1": "Mo fe lo si oja", "s2": "E kaaro, se daada ni"},
    )
    assert 0 < partial.score < 100
    assert partial.summary["word_accuracy"] < 100
    assert partial.summary["word_accuracy"] > 0


def test_transcription_grades_speaker_and_timestamp_when_the_spec_asks() -> None:
    spec = {
        "kind": "transcription",
        "segments": [
            {
                "id": "s1",
                "reference": "Mo fe lo si oja",
                "speaker": "SPEAKER_1",
                "start": 2.0,
            }
        ],
    }
    good = score_task(
        spec, {"s1": {"text": "Mo fe lo si oja", "speaker": "SPEAKER_1", "start": "0:02.0"}}
    )
    bad = score_task(spec, {"s1": {"text": "Mo fe lo si oja", "speaker": "SPEAKER_2", "start": ""}})
    assert good.score == 100
    assert good.summary["speaker_accuracy"] == 100
    assert good.summary["timestamp_accuracy"] == 100
    assert bad.score < good.score
    assert bad.summary["speaker_accuracy"] == 0


def test_translation_uses_chrf_similarity_and_key_terms() -> None:
    exact = score_task(TRANSLATION_SPEC, {"t1": "Good morning"})
    assert exact.score == 100
    assert exact.summary["terminology"] == 100

    missing_term = score_task(TRANSLATION_SPEC, {"t1": "Good day"})
    assert 0 < missing_term.score < 100
    assert missing_term.summary["terminology"] == 0


def test_recording_checks_the_declared_technical_requirements() -> None:
    good = {
        "p1": {
            "duration_seconds": 3.0,
            "clip_pct": 0.0,
            "rms_db": -20,
            "silence_pct": 10,
        },
        "metadata": {"dialect": "Ekiti"},
    }
    result = score_task(RECORDING_SPEC, good)
    assert result.score == 100
    assert result.is_correct is True

    clipped = {
        "p1": {
            "duration_seconds": 3.0,
            "clip_pct": 4.0,
            "rms_db": -20,
            "silence_pct": 10,
        },
        "metadata": {"dialect": "Ekiti"},
    }
    assert score_task(RECORDING_SPEC, clipped).score == 0

    missing_metadata = score_task(RECORDING_SPEC, {"p1": good["p1"], "metadata": {}})
    assert missing_metadata.score == 90


def test_pass_score_decides_the_verdict_but_the_score_is_kept() -> None:
    responses = {
        "a1": {"sentiment": "Positive"},
        "a2": {"sentiment": "Positive"},
        "r1": {"sentiment": "Positive"},
    }
    result = score_task(LABELING_SPEC, responses, pass_score=70)
    assert result.score == 67
    assert result.is_correct is False
    assert "67/100" in result.feedback


def test_assessment_reveal_false_hides_per_item_answers() -> None:
    result = score_task(
        TRANSCRIPTION_SPEC,
        {"s1": "Mo fe lo si oja", "s2": "E kaaro, se daadaa ni?"},
        reveal=False,
    )
    assert all(set(item) == {"id"} for item in result.items)


def test_validation_envelope_reports_a_partial_score() -> None:
    config = {"task_kind": "labeling", "task_spec": LABELING_SPEC, "pass_score": 70}
    expected = {
        "responses": {
            "a1": {"sentiment": "Positive"},
            "a2": {"sentiment": "Neutral"},
            "r1": {"sentiment": "Positive"},
        }
    }
    result = validate(
        "all_language_task",
        {"responses": {"a1": {"sentiment": "Positive"}, "a2": {"sentiment": "Neutral"}}},
        expected,
        config,
    )
    assert result.score < 100
    assert "expected" not in result.details


def test_public_task_spec_strips_every_answer_key() -> None:
    labeling = public_task_spec(LABELING_SPEC)
    assert "expected" not in labeling["items"][0]["fields"][0]
    assert labeling["items"][0]["text"] == LABELING_SPEC["items"][0]["text"]

    transcription = public_task_spec(
        {
            "kind": "transcription",
            "segments": [
                {"id": "s1", "reference": "secret", "speaker": "SPEAKER_1", "start": 2}
            ],
        }
    )
    segment = transcription["segments"][0]
    assert "reference" not in segment
    assert "speaker" not in segment
    assert "start" not in segment
    assert segment["speaker_required"] is True
    assert segment["start_required"] is True

    translation = public_task_spec(TRANSLATION_SPEC)
    assert "references" not in translation["items"][0]
    assert translation["items"][0]["source"] == "E kaaro"


def test_task_spec_validation_catches_broken_content() -> None:
    assert validate_task_spec(LABELING_SPEC) == []
    broken = {
        "kind": "labeling",
        "items": [
            {
                "id": "a1",
                "fields": [
                    {"name": "x", "type": "choice", "options": ["A"], "expected": "B"}
                ],
            }
        ],
    }
    assert validate_task_spec(broken)
    assert validate_task_spec({"kind": "unknown"})
