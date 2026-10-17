"""The configurable task engine (PRD §4).

A task type is rows: `input_schema` says what the student sees, `answer_schema`
what they submit, and `validator` names one of the small registered functions
below. Adding a new *label set* or a new instruction is content; adding a new
validator is code, and it is one tested function.

Practice is a sandbox. Its verdict is feedback, never verification: `is_correct`
lives on `PracticeAttempt` and no verification service reads it.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.identity import User
from app.models.skills import (
    STATUS_PUBLISHED,
    PracticeAttempt,
    TaskTemplate,
)


@dataclass(frozen=True)
class ValidationResult:
    is_correct: bool
    score: int  # 0-100
    feedback: str
    details: dict[str, Any] = field(default_factory=dict)


def _labels(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip().lower() for item in value if str(item).strip()]


def validate_exact_key(answer: dict, expected: dict, config: dict) -> ValidationResult:
    given = str(answer.get("key", "")).strip()
    wanted = str(expected.get("key", "")).strip()
    correct = bool(given) and given == wanted
    return ValidationResult(
        is_correct=correct,
        score=100 if correct else 0,
        feedback="Correct." if correct else "That is not the right key. Compare the options again.",
        details={"expected_key": wanted} if not correct else {},
    )


def validate_label_set(answer: dict, expected: dict, config: dict) -> ValidationResult:
    given = _labels(answer.get("labels"))
    wanted = _labels(expected.get("labels"))
    correct = sorted(given) == sorted(wanted)
    missing = sorted(set(wanted) - set(given))
    extra = sorted(set(given) - set(wanted))
    if correct:
        feedback = "Correct: every label matches."
    elif missing and not extra:
        feedback = f"Close. Missing: {', '.join(missing)}."
    elif extra and not missing:
        feedback = f"Too many labels. Remove: {', '.join(extra)}."
    else:
        feedback = (
            f"Missing: {', '.join(missing) or 'none'}. "
            f"Not needed: {', '.join(extra) or 'none'}."
        )
    return ValidationResult(
        is_correct=correct,
        score=100 if correct else 0,
        feedback=feedback,
        details={"missing": missing, "extra": extra},
    )


def validate_ranking(answer: dict, expected: dict, config: dict) -> ValidationResult:
    given = [str(item) for item in (answer.get("order") or [])]
    wanted = [str(item) for item in (expected.get("order") or [])]
    if sorted(given) != sorted(wanted):
        return ValidationResult(
            is_correct=False,
            score=0,
            feedback="Rank every item exactly once.",
            details={"expected_count": len(wanted), "given_count": len(given)},
        )
    if given == wanted:
        return ValidationResult(is_correct=True, score=100, feedback="Correct order.")
    # Partial credit by pairwise agreement, so feedback is useful on a wrong order.
    pairs = [(a, b) for i, a in enumerate(wanted) for b in wanted[i + 1 :]]
    agree = sum(1 for a, b in pairs if given.index(a) < given.index(b))
    score = round(100 * agree / len(pairs)) if pairs else 0
    return ValidationResult(
        is_correct=False,
        score=score,
        feedback="Some pairs are in the right order. Check the first two items again.",
        details={"pairwise_agreement_percent": score},
    )


def validate_numeric_tolerance(answer: dict, expected: dict, config: dict) -> ValidationResult:
    tolerance = int(config.get("tolerance", 0))
    try:
        given = int(answer.get("value"))
        wanted = int(expected.get("value"))
    except (TypeError, ValueError):
        return ValidationResult(
            is_correct=False, score=0, feedback="Enter a whole number."
        )
    difference = abs(given - wanted)
    correct = difference <= tolerance
    return ValidationResult(
        is_correct=correct,
        score=100 if correct else 0,
        feedback=(
            "Correct."
            if correct
            else f"Not quite. The answer is within {tolerance} of the correct value."
        ),
        details={"difference": difference, "tolerance": tolerance},
    )


def _span_key(span: dict) -> tuple[int, int, str]:
    return (int(span.get("start", 0)), int(span.get("end", 0)), str(span.get("label", "")).lower())


def validate_span_overlap(answer: dict, expected: dict, config: dict) -> ValidationResult:
    """Entity tagging with an IoU threshold; whole-set correctness is required.

    A span is `{start, end, label}` over the input text, in characters. Partial
    credit is reported so feedback can point at what is missing, but `is_correct`
    only when every expected span is matched and no extra span is submitted.
    """
    threshold = float(config.get("min_overlap", 0.5))
    given = [_span for _span in (answer.get("spans") or []) if isinstance(_span, dict)]
    wanted = [_span for _span in (expected.get("spans") or []) if isinstance(_span, dict)]

    matched: list[tuple[int, int]] = []
    used: set[int] = set()
    for index, gold in enumerate(wanted):
        gold_start, gold_end, gold_label = _span_key(gold)
        best: tuple[float, int] | None = None
        for pos, span in enumerate(given):
            if pos in used:
                continue
            start, end, label = _span_key(span)
            if label != gold_label:
                continue
            overlap = max(0, min(end, gold_end) - max(start, gold_start))
            union = max(end, gold_end) - min(start, gold_start)
            if union <= 0:
                continue
            iou = overlap / union
            if iou >= threshold and (best is None or iou > best[0]):
                best = (iou, pos)
        if best is not None:
            matched.append((index, best[1]))
            used.add(best[1])

    correct = len(matched) == len(wanted) and len(used) == len(given)
    missing = len(wanted) - len(matched)
    extra = len(given) - len(used)
    score = 0 if not wanted else round(100 * len(matched) / len(wanted))
    if correct:
        feedback = "Correct: every span and label matches."
    else:
        feedback = (
            f"{len(matched)} of {len(wanted)} spans match. "
            f"{missing} missing, {extra} extra."
        )
    return ValidationResult(
        is_correct=correct,
        score=score,
        feedback=feedback,
        details={"missing": missing, "extra": extra, "min_overlap": threshold},
    )


Validator = Callable[[dict, dict, dict], ValidationResult]

VALIDATORS: dict[str, Validator] = {
    "exact_key": validate_exact_key,
    "label_set": validate_label_set,
    "ranking": validate_ranking,
    "numeric_tolerance": validate_numeric_tolerance,
    "span_overlap": validate_span_overlap,
}


def validate(
    validator_name: str,
    answer: dict,
    expected: dict,
    config: dict | None = None,
) -> ValidationResult:
    validator = VALIDATORS.get(validator_name)
    if validator is None:
        # A template naming an unknown validator is an ops error, not a student
        # error; fail loudly rather than silently marking work correct.
        raise ApiError(
            500,
            "validator_missing",
            "This task type is not available right now.",
            {"validator": validator_name},
        )
    if not isinstance(answer, dict):
        raise ApiError(400, "invalid_answer", "Submit an answer object.")
    return validator(answer, expected, config or {})


# --- practice ----------------------------------------------------------------


def _published_template(db: Session, template_id: int) -> TaskTemplate:
    template = db.get(TaskTemplate, template_id)
    if template is None or template.status != STATUS_PUBLISHED:
        raise ApiError(404, "task_not_found", "This practice task is not available.")
    return template


def practice_brief(db: Session, template_id: int) -> dict:
    """What the student sees: input and instructions, never the expected answer."""
    template = _published_template(db, template_id)
    config = template.config or {}
    return {
        "template_id": template.id,
        "slug": template.slug,
        "name": template.name,
        "instructions_md": template.instructions_md,
        "input_schema": template.input_schema,
        "answer_schema": template.answer_schema,
        "sample": config.get("sample"),
        "version": template.version,
    }


def submit_practice(
    db: Session,
    user: User,
    *,
    template_id: int,
    answer: dict,
    duration_ms: int | None = None,
) -> tuple[PracticeAttempt, ValidationResult]:
    template = _published_template(db, template_id)
    config = template.config or {}
    expected = config.get("expected_answer")
    if not isinstance(expected, dict):
        raise ApiError(
            503,
            "practice_unavailable",
            "This practice task has no sample answer yet. Try another one.",
        )

    result = validate(template.validator, answer, expected, config)
    attempt = PracticeAttempt(
        user_id=user.id,
        template_id=template.id,
        answer=answer,
        is_correct=result.is_correct,
        feedback=result.feedback,
        duration_ms=duration_ms,
    )
    db.add(attempt)
    db.flush()
    return attempt, result
