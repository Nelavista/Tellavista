"""Deterministic scoring for structured language-data tasks (ALL).

The African Languages Lab (ALL) skills contain four task kinds: transcription,
translation, labeling and recording. Their answer keys already live on the
server (`TaskTemplate.config["expected_answer"]` / `AssessmentTask.expected_answer`
and the task spec itself); this module turns a submitted `responses` mapping into
a deterministic 0-100 score.

Everything is plain Python and deterministic: the same answers always receive the
same score. There is no AI call in this path and no randomness, which is what lets
the assessment gate verification.

Submitted shape (the V2 answer envelope)::

    {"responses": {"<item id>": value, ...}}

* transcription: value is the transcript string, or an object with `text`,
  `speaker` and `start` when the spec asks for them.
* translation: value is the translated string.
* labeling: value is an object of `{field name: answer}`; an optional
  `responses["report"]` or `responses["__report__"]` holds the written report.
* recording: value is `{duration_seconds, clip_pct, rms_db, silence_pct}` and an
  optional `responses["metadata"]` holds declared metadata fields.

Scores are never returned with the expected answers unless the caller asks for
them (`reveal=True`), so a student cannot retake an assessment by reading the
result payload.
"""
from __future__ import annotations

import copy
import re
import unicodedata
from dataclasses import dataclass, field
from typing import Any

TASK_KINDS: tuple[str, ...] = ("transcription", "translation", "labeling", "recording")
DEFAULT_PASS_SCORE = 70
MIN_JUDGEMENTS_PER_REPORTED_DIMENSION = 3

_TAG_RE = re.compile(r"\[([^\]]{1,40})\]")


class TaskSpecError(ValueError):
    """A task spec that cannot be scored; content/ops problem, not a student one."""


def _nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text or "")


def strip_diacritics(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text or "")
    return unicodedata.normalize(
        "NFC", "".join(char for char in decomposed if unicodedata.category(char) != "Mn")
    )


def normalize_tokens(text: str, keep_diacritics: bool = True) -> list[str]:
    """Lower-cased word tokens with punctuation removed.

    Bracketed tags such as ``[inaudible]`` stay as single tokens because producing
    them correctly is part of the transcription guidelines.
    """
    text = _nfc(text).lower()
    if not keep_diacritics:
        text = strip_diacritics(text)
    tags: list[str] = []

    def keep_tag(match: re.Match[str]) -> str:
        tags.append("[" + re.sub(r"\s+", "_", match.group(1).strip()) + "]")
        return f" \x00{len(tags) - 1}\x00 "

    text = _TAG_RE.sub(keep_tag, text)
    cleaned: list[str] = []
    for char in text:
        if char == "\x00" or char.isdigit():
            cleaned.append(char)
        elif unicodedata.category(char)[0] in ("P", "S"):
            cleaned.append(" ")
        else:
            cleaned.append(char)
    tokens: list[str] = []
    for token in "".join(cleaned).split():
        match = re.fullmatch(r"\x00(\d+)\x00", token)
        tokens.append(tags[int(match.group(1))] if match else token)
    return tokens


def edit_distance(reference: list[str] | str, hypothesis: list[str] | str) -> int:
    previous = list(range(len(hypothesis) + 1))
    for i, ref_token in enumerate(reference, 1):
        current = [i] + [0] * len(hypothesis)
        for j, hyp_token in enumerate(hypothesis, 1):
            current[j] = min(
                previous[j] + 1,
                current[j - 1] + 1,
                previous[j - 1] + (ref_token != hyp_token),
            )
        previous = current
    return previous[-1]


def word_error_rate(reference: str, hypothesis: str, keep_diacritics: bool = True) -> float:
    ref = normalize_tokens(reference, keep_diacritics)
    hyp = normalize_tokens(hypothesis, keep_diacritics)
    if not ref:
        return 0.0 if not hyp else 1.0
    return edit_distance(ref, hyp) / len(ref)


def chrf(hypothesis: str, reference: str, max_n: int = 6, beta: float = 2.0) -> float:
    """Character n-gram F-score (chrF, Popović 2015), 0-100, diacritic-sensitive."""
    hyp = re.sub(r"\s+", "", _nfc(hypothesis).lower())
    ref = re.sub(r"\s+", "", _nfc(reference).lower())
    if not hyp or not ref:
        return 0.0
    precisions: list[float] = []
    recalls: list[float] = []
    for n in range(1, max_n + 1):
        if len(hyp) < n or len(ref) < n:
            break
        hyp_grams: dict[str, int] = {}
        ref_grams: dict[str, int] = {}
        for i in range(len(hyp) - n + 1):
            gram = hyp[i : i + n]
            hyp_grams[gram] = hyp_grams.get(gram, 0) + 1
        for i in range(len(ref) - n + 1):
            gram = ref[i : i + n]
            ref_grams[gram] = ref_grams.get(gram, 0) + 1
        matches = sum(min(count, ref_grams.get(gram, 0)) for gram, count in hyp_grams.items())
        precisions.append(matches / sum(hyp_grams.values()))
        recalls.append(matches / sum(ref_grams.values()))
    if not precisions:
        return 0.0
    precision = sum(precisions) / len(precisions)
    recall = sum(recalls) / len(recalls)
    if precision == 0 and recall == 0:
        return 0.0
    beta_squared = beta * beta
    return 100 * (1 + beta_squared) * precision * recall / (
        beta_squared * precision + recall
    )


def parse_timestamp(value: Any) -> float | None:
    """Accept 12.5, '0:12.5' or '00:00:12.5' as seconds."""
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value or "").strip()
    if not text:
        return None
    try:
        parts = [float(part) for part in text.split(":")]
    except ValueError:
        return None
    seconds = 0.0
    for part in parts:
        seconds = seconds * 60 + part
    return seconds


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _text_equal(left: Any, right: Any) -> bool:
    return normalize_tokens(str(left)) == normalize_tokens(str(right))


def _tags(tokens: list[str]) -> list[str]:
    return sorted(token for token in tokens if token.startswith("["))


@dataclass
class TaskScore:
    score: int
    is_correct: bool
    feedback: str
    summary: dict[str, Any] = field(default_factory=dict)
    items: list[dict[str, Any]] = field(default_factory=list)
    content: str = ""


def _transcription(spec: dict, responses: dict, reveal: bool) -> TaskScore:
    tolerance = float(spec.get("timestamp_tolerance", 0.5))
    total_ref = total_edits = total_edits_plain = 0
    tag_segments = tag_ok = 0
    speaker_total = speaker_ok = ts_total = ts_ok = 0
    items: list[dict[str, Any]] = []
    lines: list[str] = []

    for segment in spec.get("segments", []):
        segment_id = segment["id"]
        value = responses.get(segment_id)
        if isinstance(value, dict):
            answer = str(value.get("text") or "").strip()
            speaker = value.get("speaker")
            start = parse_timestamp(value.get("start"))
        else:
            answer = str(value or "").strip()
            speaker = None
            start = None

        reference = str(segment.get("reference") or "")
        ref_tokens = normalize_tokens(reference)
        hyp_tokens = normalize_tokens(answer)
        edits = edit_distance(ref_tokens, hyp_tokens)
        edits_plain = edit_distance(
            normalize_tokens(reference, False), normalize_tokens(answer, False)
        )
        total_ref += len(ref_tokens)
        total_edits += edits
        total_edits_plain += edits_plain

        if _tags(ref_tokens) or _tags(hyp_tokens):
            tag_segments += 1
            tag_ok += _tags(ref_tokens) == _tags(hyp_tokens)

        item: dict[str, Any] = {
            "id": segment_id,
            "answer": answer,
            "accuracy": round(max(0.0, 1 - edits / len(ref_tokens)) * 100)
            if ref_tokens
            else 100,
            "accuracy_no_diacritics": round(max(0.0, 1 - edits_plain / len(ref_tokens)) * 100)
            if ref_tokens
            else 100,
        }
        line = answer
        if segment.get("speaker"):
            speaker_total += 1
            item["speaker_correct"] = str(speaker or "").lower() == str(segment["speaker"]).lower()
            speaker_ok += item["speaker_correct"]
            item["speaker"] = speaker
            line = f"{speaker if speaker else '?'}: {line}"
            if reveal:
                item["expected_speaker"] = segment["speaker"]
        if segment.get("start") is not None:
            ts_total += 1
            item["timestamp_correct"] = (
                start is not None and abs(start - float(segment["start"])) <= tolerance
            )
            ts_ok += item["timestamp_correct"]
            item["start"] = start
            line = f"[{start if start is not None else '?'}s] {line}"
            if reveal:
                item["expected_start"] = segment["start"]
        if reveal:
            item["reference"] = reference
        items.append(item)
        lines.append(line)

    text_accuracy = max(0.0, 1 - total_edits / total_ref) if total_ref else 1.0
    components: list[tuple[float, float]] = [
        (text_accuracy, 0.7 if (speaker_total or ts_total) else 1.0)
    ]
    if speaker_total:
        components.append((speaker_ok / speaker_total, 0.15 if ts_total else 0.3))
    if ts_total:
        components.append((ts_ok / ts_total, 0.15 if speaker_total else 0.3))
    weight = sum(component_weight for _, component_weight in components)
    score = round(100 * sum(value * component_weight for value, component_weight in components) / weight)

    summary: dict[str, Any] = {
        "word_accuracy": round(text_accuracy * 100),
        "word_accuracy_no_diacritics": round(
            max(0.0, 1 - total_edits_plain / total_ref) * 100
        )
        if total_ref
        else 100,
        "word_error_rate": round(total_edits / total_ref, 3) if total_ref else 0,
    }
    if speaker_total:
        summary["speaker_accuracy"] = round(100 * speaker_ok / speaker_total)
    if ts_total:
        summary["timestamp_accuracy"] = round(100 * ts_ok / ts_total)
    if tag_segments:
        summary["tag_compliance"] = round(100 * tag_ok / tag_segments)

    if summary["word_error_rate"] == 0:
        feedback = "Every segment matches the reference transcription."
    elif summary["word_accuracy"] >= 90:
        feedback = (
            f"Close. Word accuracy {summary['word_accuracy']}% "
            f"(word error rate {summary['word_error_rate']}). Check the remaining words and tone marks."
        )
    else:
        feedback = (
            f"Word accuracy {summary['word_accuracy']}% "
            f"(word error rate {summary['word_error_rate']}). "
            "Re-read the guidelines and compare each segment."
        )
    return TaskScore(score, False, feedback, summary, items, "\n".join(lines))


def _translation(spec: dict, responses: dict, reveal: bool) -> TaskScore:
    items: list[dict[str, Any]] = []
    lines: list[str] = []
    scores: list[float] = []
    for item_spec in spec.get("items", []):
        item_id = item_spec["id"]
        answer = str(responses.get(item_id) or "").strip()
        references = [str(ref) for ref in _as_list(item_spec.get("references"))]
        similarity = max((chrf(answer, ref) for ref in references), default=0.0) if answer else 0.0
        key_terms = [str(term) for term in _as_list(item_spec.get("key_terms"))]
        answer_normalized = " ".join(normalize_tokens(answer))
        terms_found = [
            term for term in key_terms if " ".join(normalize_tokens(term)) in answer_normalized
        ]
        if key_terms:
            item_score = 0.8 * similarity + 20 * len(terms_found) / len(key_terms)
        else:
            item_score = similarity
        scores.append(item_score)
        item: dict[str, Any] = {
            "id": item_id,
            "answer": answer,
            "similarity": round(similarity),
            "score": round(item_score),
        }
        if key_terms:
            item["key_terms_found"] = len(terms_found)
            item["key_terms_total"] = len(key_terms)
        if reveal:
            item["references"] = references
            item["key_terms"] = key_terms
        items.append(item)
        lines.append(f"{item_spec.get('source', '')}\n=> {answer}")

    score = round(sum(scores) / len(scores)) if scores else 0
    summary: dict[str, Any] = {
        "mean_similarity": round(sum(item["similarity"] for item in items) / len(items))
        if items
        else 0
    }
    term_total = sum(item.get("key_terms_total", 0) for item in items)
    if term_total:
        summary["terminology"] = round(
            100 * sum(item.get("key_terms_found", 0) for item in items) / term_total
        )
    feedback = (
        f"Translation similarity {summary['mean_similarity']}%."
        + (
            f" Key terminology {summary['terminology']}%."
            if "terminology" in summary
            else ""
        )
        + (" Review the reference wording and key terms." if score < 100 else "")
    )
    return TaskScore(score, False, feedback, summary, items, "\n\n".join(lines))


def _field_correct(task_field: dict, raw: Any) -> bool | None:
    expected = _as_list(task_field.get("expected"))
    if not expected:
        return None
    field_type = task_field.get("type", "choice")
    if field_type == "number":
        try:
            given = float(str(raw).strip())
        except (TypeError, ValueError):
            return False
        tolerance = float(task_field.get("tolerance", 0))
        return any(abs(given - float(value)) <= tolerance + 1e-9 for value in expected)
    if field_type == "text":
        return any(_text_equal(raw or "", value) for value in expected)
    return any(
        str(raw or "").strip().lower() == str(value).strip().lower() for value in expected
    )


def _labeling(spec: dict, responses: dict, reveal: bool) -> TaskScore:
    total = correct = 0
    by_field: dict[str, list[int]] = {}
    answers_by_item: dict[str, dict[str, str]] = {}
    items: list[dict[str, Any]] = []
    lines: list[str] = []

    for item_spec in spec.get("items", []):
        item_id = item_spec["id"]
        given = responses.get(item_id)
        given_map = given if isinstance(given, dict) else {}
        fields_out: list[dict[str, Any]] = []
        answers: list[str] = []
        for task_field in item_spec.get("fields", []):
            name = task_field["name"]
            submitted = given_map.get(name)
            # `0` and `0.0` are real answers; only `None`/missing means blank.
            raw = "" if submitted is None else str(submitted).strip()
            answers_by_item.setdefault(item_id, {})[name] = raw
            ok = _field_correct(task_field, raw)
            out: dict[str, Any] = {
                "name": name,
                "label": task_field.get("label", name),
                "answer": raw,
            }
            if ok is not None:
                total += 1
                correct += ok
                tally = by_field.setdefault(out["label"], [0, 0])
                tally[0] += ok
                tally[1] += 1
                out["correct"] = ok
                if reveal:
                    out["expected"] = _as_list(task_field.get("expected"))
            fields_out.append(out)
            answers.append(f"{out['label']}: {raw or '(blank)'}")
        items.append({"id": item_id, "fields": fields_out})
        lines.append(f"[{item_id}] " + "; ".join(answers))

    field_score = correct / total if total else 1.0

    report_config = spec.get("report")
    report_result = None
    if report_config:
        report_text = str(
            responses.get("report") or responses.get("__report__") or ""
        ).strip()
        min_words = int(report_config.get("min_words", 15))
        report_result = {
            "words": len(report_text.split()),
            "min_words": min_words,
            "ok": len(report_text.split()) >= min_words,
        }
        if report_text:
            lines.append(f"\nReport:\n{report_text}")

    if report_result is not None:
        score = round(100 * (0.9 * field_score + 0.1 * report_result["ok"]))
    else:
        score = round(100 * field_score)

    summary: dict[str, Any] = {"correct": correct, "total": total}
    visible_by_field = by_field
    if not reveal:
        # A dimension backed by one or two judgements is just that item's mark.
        visible_by_field = {
            label: tally
            for label, tally in by_field.items()
            if tally[1] >= MIN_JUDGEMENTS_PER_REPORTED_DIMENSION
        }
    if len(visible_by_field) > 1:
        summary["by_field"] = {
            label: round(100 * tally[0] / tally[1]) for label, tally in visible_by_field.items()
        }

    repeats = [item for item in spec.get("items", []) if item.get("repeat_of")]
    if repeats:
        same = pairs = 0
        for item_spec in repeats:
            original = answers_by_item.get(item_spec["repeat_of"], {})
            for name, value in answers_by_item.get(item_spec["id"], {}).items():
                pairs += 1
                same += bool(value) and value.lower() == (original.get(name) or "").lower()
        if pairs:
            summary["consistency"] = round(100 * same / pairs)
    if report_result is not None:
        summary["report"] = report_result

    if total == 0:
        feedback = "This task has no scored fields."
    else:
        feedback = f"{correct} of {total} fields correct."
        if "consistency" in summary:
            feedback += f" Repeat consistency {summary['consistency']}%."
        if report_result is not None:
            feedback += (
                " The written report meets the word minimum."
                if report_result["ok"]
                else f" The written report needs at least {report_result['min_words']} words."
            )
    return TaskScore(score, False, feedback, summary, items, "\n".join(lines))


def _check_recording(metrics: dict, requirements: dict) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": bool(ok), "detail": detail})

    duration = metrics.get("duration_seconds")
    if duration is None:
        add("Recorded", False, "No recording received")
        return checks
    if "min_seconds" in requirements or "max_seconds" in requirements:
        low = float(requirements.get("min_seconds", 0))
        high = float(requirements.get("max_seconds", 10**6))
        add("Length", low <= duration <= high, f"{duration:.1f}s (needs {low}-{high}s)")
    if "max_clip_pct" in requirements and metrics.get("clip_pct") is not None:
        add(
            "No clipping",
            metrics["clip_pct"] <= float(requirements["max_clip_pct"]),
            f"{metrics['clip_pct']:.2f}% clipped samples (max {requirements['max_clip_pct']}%)",
        )
    if "min_rms_db" in requirements and metrics.get("rms_db") is not None:
        add(
            "Loud enough",
            metrics["rms_db"] >= float(requirements["min_rms_db"]),
            f"{metrics['rms_db']:.1f} dBFS average level (min {requirements['min_rms_db']} dBFS)",
        )
    if "max_silence_pct" in requirements and metrics.get("silence_pct") is not None:
        add(
            "Not mostly silence",
            metrics["silence_pct"] <= float(requirements["max_silence_pct"]),
            f"{metrics['silence_pct']:.0f}% silent (max {requirements['max_silence_pct']}%)",
        )
    return checks


def _recording(spec: dict, responses: dict, reveal: bool) -> TaskScore:
    requirements = spec.get("requirements") or {}
    items: list[dict[str, Any]] = []
    lines: list[str] = []
    passed = 0
    prompts = spec.get("prompts", [])

    for prompt in prompts:
        prompt_id = prompt["id"]
        raw = responses.get(prompt_id)
        metrics: dict[str, float] = {}
        if isinstance(raw, dict):
            for key in ("duration_seconds", "clip_pct", "rms_db", "silence_pct"):
                if isinstance(raw.get(key), (int, float)):
                    metrics[key] = float(raw[key])
        checks = _check_recording(metrics, requirements)
        ok = bool(checks) and all(check["ok"] for check in checks)
        passed += ok
        items.append(
            {
                "id": prompt_id,
                "prompt": prompt.get("text"),
                "checks": checks,
                "passed": ok,
                "metrics": metrics,
            }
        )
        lines.append(
            f"{prompt.get('text', '')} -> "
            + ("meets requirements" if ok else "needs re-recording")
        )

    metadata: dict[str, str] = {}
    missing_metadata = 0
    metadata_responses = responses.get("metadata")
    metadata_map = metadata_responses if isinstance(metadata_responses, dict) else {}
    for metadata_field in spec.get("metadata_fields", []):
        name = metadata_field["name"]
        value = str(metadata_map.get(name, "") or "").strip()
        metadata[name] = value
        missing_metadata += not value
        lines.append(f"{metadata_field.get('label', name)}: {value or '(blank)'}")

    score = round(100 * passed / len(prompts)) if prompts else 0
    if missing_metadata:
        score = max(0, score - 10 * missing_metadata)

    summary: dict[str, Any] = {
        "passed": passed,
        "total": len(prompts),
        "metadata": metadata,
        "note": "Audio levels are measured in your browser when you record.",
    }
    if reveal and spec.get("metadata_fields"):
        summary["metadata_complete"] = missing_metadata == 0
    feedback = f"{passed} of {len(prompts)} recordings meet the technical requirements."
    if missing_metadata:
        feedback += f" {missing_metadata} metadata field(s) are still blank."
    return TaskScore(score, False, feedback, summary, items, "\n".join(lines))


def score_task(
    spec: dict,
    responses: dict,
    *,
    pass_score: int = DEFAULT_PASS_SCORE,
    reveal: bool = True,
) -> TaskScore:
    """Score one submission. `responses` is the `responses` mapping, not the envelope."""
    kind = spec.get("kind")
    if kind not in TASK_KINDS:
        raise TaskSpecError(f"unknown task kind: {kind!r}")
    if not isinstance(responses, dict):
        responses = {}

    if kind == "transcription":
        result = _transcription(spec, responses, reveal)
    elif kind == "translation":
        result = _translation(spec, responses, reveal)
    elif kind == "labeling":
        result = _labeling(spec, responses, reveal)
    else:
        result = _recording(spec, responses, reveal)

    result.score = max(0, min(100, result.score))
    result.is_correct = result.score >= pass_score

    if not reveal and kind != "recording":
        # Assessments keep aggregate scores only: per-item marks would let a
        # retake flip one answer at a time until every item reads correct.
        result.items = [{"id": item["id"]} for item in result.items]

    if result.is_correct:
        result.feedback = f"Passed: {result.score}/100. " + result.feedback
    else:
        result.feedback = (
            f"{result.score}/100, and {pass_score} is needed to pass. " + result.feedback
        )
    return result


def has_any_answer(responses: dict) -> bool:
    """An empty submission is rejected instead of being recorded as a 0% attempt."""
    if not isinstance(responses, dict):
        return False
    for key, value in responses.items():
        if key == "metadata":
            if isinstance(value, dict) and any(str(item or "").strip() for item in value.values()):
                return True
            continue
        if isinstance(value, dict):
            if any(str(item or "").strip() for item in value.values()):
                return True
        elif str(value or "").strip():
            return True
    return False


def public_task_spec(spec: dict) -> dict:
    """The student-safe view of a task spec: no references, expected values or
    hidden speaker/timestamp answers.

    The client still needs to know that a speaker or start time is *required*, so
    those keys become booleans instead of expected values.
    """
    if not isinstance(spec, dict):
        return spec
    public = copy.deepcopy(spec)
    kind = public.get("kind")
    if kind == "labeling":
        for item in public.get("items", []):
            for task_field in item.get("fields", []):
                task_field.pop("expected", None)
    elif kind == "transcription":
        for segment in public.get("segments", []):
            segment.pop("reference", None)
            if "speaker" in segment:
                segment["speaker_required"] = True
                segment.pop("speaker", None)
            if "start" in segment:
                segment["start_required"] = True
                segment.pop("start", None)
    elif kind == "translation":
        for item in public.get("items", []):
            item.pop("references", None)
    return public


def validate_task_spec(spec: dict) -> list[str]:
    """Problems with a task spec; an empty list means it is valid."""
    errors: list[str] = []
    if not isinstance(spec, dict) or spec.get("kind") not in TASK_KINDS:
        return [f"kind must be one of {TASK_KINDS}"]
    kind = spec["kind"]
    if kind == "transcription":
        segments = spec.get("segments") or []
        if not segments:
            errors.append("transcription needs at least one segment")
        for segment in segments:
            if not segment.get("id") or not segment.get("reference"):
                errors.append(f"segment missing id/reference: {segment.get('id')}")
    elif kind == "translation":
        items = spec.get("items") or []
        if not items:
            errors.append("translation needs at least one item")
        for item in items:
            if (
                not item.get("id")
                or not item.get("source")
                or not _as_list(item.get("references"))
            ):
                errors.append(
                    f"translation item missing id/source/references: {item.get('id')}"
                )
    elif kind == "labeling":
        items = spec.get("items") or []
        if not items:
            errors.append("labeling needs at least one item")
        for item in items:
            if not item.get("id") or not item.get("fields"):
                errors.append(f"labeling item missing id/fields: {item.get('id')}")
            for task_field in item.get("fields") or []:
                if task_field.get("type", "choice") == "choice" and task_field.get(
                    "expected"
                ) is not None:
                    options = [str(option).lower() for option in task_field.get("options") or []]
                    for expected in _as_list(task_field["expected"]):
                        if str(expected).lower() not in options:
                            errors.append(
                                f"item {item.get('id')} field {task_field.get('name')}: "
                                f"expected {expected!r} not in options"
                            )
    elif kind == "recording":
        if not spec.get("prompts"):
            errors.append("recording needs at least one prompt")
    return errors
