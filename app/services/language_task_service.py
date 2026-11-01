"""Deterministic scoring for structured practical tasks (Challenge.task_spec).

Built for the African Languages Lab (ALL) skills — transcription, translation,
annotation, AI-evaluation, QA and speech-recording work — where a student has to show
they can actually do the task, not just describe it. Everything here is plain Python
(no new dependencies) and fully deterministic: the same answers always get the same
score, which is what lets an assessment gate skill verification. AI feedback, where a
task asks for it, is layered on top by the route and never changes this score.

task_spec schema (JSON on Challenge.task_spec_json). Common keys:
    kind:        'transcription' | 'translation' | 'labeling' | 'recording'
    brief:       short context shown above the task
    guidelines:  list of guideline strings the student must follow
    ai_feedback: optional bool — also ask the AI coach for written feedback

kind == 'transcription':
    mode: 'verbatim' | 'clean'; audio_url: optional; speakers: optional label list
    segments: [{id, reference, draft?, context?, speaker?, start?}]
      draft    pre-fills the box (e.g. machine output with tone marks stripped)
      speaker  expected speaker label  -> a speaker dropdown is shown and scored
      start    expected start time (s) -> a timestamp box is shown and scored
    timestamp_tolerance: seconds (default 0.5)
kind == 'translation':
    source_lang, target_lang
    items: [{id, source, references: [...], key_terms?: [...]}]
kind == 'labeling':
    items: [{id, text, context?, repeat_of?, fields: [{name, label, type, options?, expected, tolerance?}]}]
      type: 'choice' | 'number' | 'text'; expected may be a list of accepted answers
      repeat_of: id of an earlier item with the same content -- an unannounced repeat used
      to measure the annotator's consistency (as gold-repeat checks do on real projects)
    report: optional {label, min_words} — a written explanation / QA report
kind == 'recording':
    prompts: [{id, text}]
    requirements: {min_seconds, max_seconds, max_clip_pct, min_rms_db, max_silence_pct}
    metadata_fields: optional [{name, label, type, options?}] (e.g. dialect, environment)
"""
import json
import re
import unicodedata

TASK_KINDS = ('transcription', 'translation', 'labeling', 'recording')
DEFAULT_PASS_SCORE = 70
MIN_JUDGEMENTS_PER_REPORTED_DIMENSION = 3

_TAG_RE = re.compile(r'\[([^\]]{1,40})\]')


# ---------------------------------------------------------------- text normalisation

def _nfc(text):
    return unicodedata.normalize('NFC', text or '')


def strip_diacritics(text):
    """Removes combining marks (Yoruba/Igbo tone marks and under-dots) — used only to
    report 'accuracy ignoring diacritics' next to the real, diacritic-sensitive score,
    so a student can see whether their errors are words or tone marks."""
    decomposed = unicodedata.normalize('NFD', text or '')
    return unicodedata.normalize('NFC', ''.join(c for c in decomposed if unicodedata.category(c) != 'Mn'))


def normalize_tokens(text, keep_diacritics=True):
    """Lower-cased word tokens with punctuation removed. Bracketed tags such as
    [inaudible] or [laughter] are kept as single tokens, since producing them correctly
    is part of transcription guidelines."""
    text = _nfc(text).lower()
    if not keep_diacritics:
        text = strip_diacritics(text)
    tags = []

    def _keep_tag(match):
        tags.append('[' + re.sub(r'\s+', '_', match.group(1).strip()) + ']')
        return f' \x00{len(tags) - 1}\x00 '

    text = _TAG_RE.sub(_keep_tag, text)
    cleaned = []
    for ch in text:
        cat = unicodedata.category(ch)
        if ch == '\x00' or ch.isdigit():
            cleaned.append(ch)
        elif cat[0] in ('P', 'S'):
            cleaned.append(' ')
        else:
            cleaned.append(ch)
    tokens = []
    for tok in ''.join(cleaned).split():
        m = re.fullmatch(r'\x00(\d+)\x00', tok)
        tokens.append(tags[int(m.group(1))] if m else tok)
    return tokens


def edit_distance(ref, hyp):
    """Levenshtein distance between two token (or character) sequences."""
    prev = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        cur = [i] + [0] * len(hyp)
        for j, h in enumerate(hyp, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (r != h))
        prev = cur
    return prev[-1]


def word_error_rate(reference, hypothesis, keep_diacritics=True):
    ref = normalize_tokens(reference, keep_diacritics)
    hyp = normalize_tokens(hypothesis, keep_diacritics)
    if not ref:
        return 0.0 if not hyp else 1.0
    return edit_distance(ref, hyp) / len(ref)


def chrf(hypothesis, reference, max_n=6, beta=2.0):
    """Character n-gram F-score (chrF, Popović 2015), 0-100. Whitespace is ignored, as in
    the standard definition, and comparison is diacritic-sensitive."""
    hyp = re.sub(r'\s+', '', _nfc(hypothesis).lower())
    ref = re.sub(r'\s+', '', _nfc(reference).lower())
    if not hyp or not ref:
        return 0.0
    precisions, recalls = [], []
    for n in range(1, max_n + 1):
        if len(hyp) < n or len(ref) < n:
            break
        hyp_grams, ref_grams = {}, {}
        for i in range(len(hyp) - n + 1):
            g = hyp[i:i + n]
            hyp_grams[g] = hyp_grams.get(g, 0) + 1
        for i in range(len(ref) - n + 1):
            g = ref[i:i + n]
            ref_grams[g] = ref_grams.get(g, 0) + 1
        matches = sum(min(c, ref_grams.get(g, 0)) for g, c in hyp_grams.items())
        precisions.append(matches / sum(hyp_grams.values()))
        recalls.append(matches / sum(ref_grams.values()))
    if not precisions:
        return 0.0
    p = sum(precisions) / len(precisions)
    r = sum(recalls) / len(recalls)
    if p == 0 and r == 0:
        return 0.0
    b2 = beta * beta
    return 100 * (1 + b2) * p * r / (b2 * p + r)


def parse_timestamp(value):
    """Accepts '12.5', '0:12.5', '00:00:12.5' -> seconds (float), or None."""
    value = (value or '').strip()
    if not value:
        return None
    try:
        parts = [float(p) for p in value.split(':')]
    except ValueError:
        return None
    seconds = 0.0
    for p in parts:
        seconds = seconds * 60 + p
    return seconds


def _as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _text_equal(a, b):
    return normalize_tokens(str(a)) == normalize_tokens(str(b))


# ---------------------------------------------------------------- per-kind scorers

def _tags(tokens):
    return sorted(t for t in tokens if t.startswith('['))


def _score_transcription(spec, form, reveal):
    tolerance = float(spec.get('timestamp_tolerance', 0.5))
    total_ref = total_edits = total_edits_plain = 0
    tag_segments = tag_ok = 0
    speaker_total = speaker_ok = ts_total = ts_ok = 0
    items, lines = [], []
    for seg in spec.get('segments', []):
        sid = seg['id']
        answer = (form.get(f'seg-{sid}-text') or '').strip()
        ref_tokens = normalize_tokens(seg['reference'])
        hyp_tokens = normalize_tokens(answer)
        edits = edit_distance(ref_tokens, hyp_tokens)
        edits_plain = edit_distance(normalize_tokens(seg['reference'], False), normalize_tokens(answer, False))
        total_ref += len(ref_tokens)
        total_edits += edits
        total_edits_plain += edits_plain
        if _tags(ref_tokens) or _tags(hyp_tokens):
            # Formatting compliance: exactly the tags the guideline calls for, no invented
            # or missing ones. Only segments where tags are involved are counted.
            tag_segments += 1
            tag_ok += _tags(ref_tokens) == _tags(hyp_tokens)
        item = {
            'id': sid, 'answer': answer,
            'accuracy': round(max(0.0, 1 - edits / len(ref_tokens)) * 100) if ref_tokens else 100,
            'accuracy_no_diacritics': round(max(0.0, 1 - edits_plain / len(ref_tokens)) * 100) if ref_tokens else 100,
        }
        line = answer
        if seg.get('speaker'):
            got = (form.get(f'seg-{sid}-speaker') or '').strip()
            speaker_total += 1
            item['speaker_correct'] = got.lower() == str(seg['speaker']).lower()
            speaker_ok += item['speaker_correct']
            item['speaker'] = got
            line = f'{got}: {line}'
            if reveal:
                item['expected_speaker'] = seg['speaker']
        if seg.get('start') is not None:
            got_ts = parse_timestamp(form.get(f'seg-{sid}-start'))
            ts_total += 1
            item['timestamp_correct'] = got_ts is not None and abs(got_ts - float(seg['start'])) <= tolerance
            ts_ok += item['timestamp_correct']
            item['start'] = got_ts
            line = f'[{got_ts if got_ts is not None else "?"}s] {line}'
            if reveal:
                item['expected_start'] = seg['start']
        if reveal:
            item['reference'] = seg['reference']
        items.append(item)
        lines.append(line)

    text_acc = max(0.0, 1 - total_edits / total_ref) if total_ref else 1.0
    components = [(text_acc, 0.7 if (speaker_total or ts_total) else 1.0)]
    if speaker_total:
        components.append((speaker_ok / speaker_total, 0.15 if ts_total else 0.3))
    if ts_total:
        components.append((ts_ok / ts_total, 0.15 if speaker_total else 0.3))
    weight = sum(w for _, w in components)
    score = round(100 * sum(v * w for v, w in components) / weight)
    summary = {
        'word_accuracy': round(text_acc * 100),
        'word_accuracy_no_diacritics': round(max(0.0, 1 - total_edits_plain / total_ref) * 100) if total_ref else 100,
        'word_error_rate': round(total_edits / total_ref, 3) if total_ref else 0,
    }
    if speaker_total:
        summary['speaker_accuracy'] = round(100 * speaker_ok / speaker_total)
    if ts_total:
        summary['timestamp_accuracy'] = round(100 * ts_ok / ts_total)
    if tag_segments:
        summary['tag_compliance'] = round(100 * tag_ok / tag_segments)
    return score, items, summary, '\n'.join(lines)


def _score_translation(spec, form, reveal):
    items, lines, scores = [], [], []
    for it in spec.get('items', []):
        iid = it['id']
        answer = (form.get(f'item-{iid}-translation') or '').strip()
        refs = _as_list(it.get('references'))
        similarity = max((chrf(answer, r) for r in refs), default=0.0) if answer else 0.0
        terms = _as_list(it.get('key_terms'))
        answer_norm = ' '.join(normalize_tokens(answer))
        terms_found = [t for t in terms if ' '.join(normalize_tokens(t)) in answer_norm]
        if terms:
            item_score = 0.8 * similarity + 20 * len(terms_found) / len(terms)
        else:
            item_score = similarity
        scores.append(item_score)
        item = {'id': iid, 'answer': answer, 'similarity': round(similarity), 'score': round(item_score)}
        if terms:
            item['key_terms_found'] = len(terms_found)
            item['key_terms_total'] = len(terms)
        if reveal:
            item['references'] = refs
            item['key_terms'] = terms
        items.append(item)
        lines.append(f"{it['source']}\n=> {answer}")
    score = round(sum(scores) / len(scores)) if scores else 0
    summary = {'mean_similarity': round(sum(i['similarity'] for i in items) / len(items)) if items else 0}
    term_total = sum(i.get('key_terms_total', 0) for i in items)
    if term_total:
        summary['terminology'] = round(100 * sum(i.get('key_terms_found', 0) for i in items) / term_total)
    return score, items, summary, '\n\n'.join(lines)


def _field_correct(field, raw):
    expected = _as_list(field.get('expected'))
    if not expected:
        return None  # an unscored field (free metadata)
    ftype = field.get('type', 'choice')
    if ftype == 'number':
        try:
            got = float(str(raw).strip())
        except (TypeError, ValueError):
            return False
        tolerance = float(field.get('tolerance', 0))
        return any(abs(got - float(e)) <= tolerance + 1e-9 for e in expected)
    if ftype == 'text':
        return any(_text_equal(raw or '', e) for e in expected)
    return any(str(raw or '').strip().lower() == str(e).strip().lower() for e in expected)


def _report_result(spec, form):
    report_cfg = spec.get('report')
    if not report_cfg:
        return None, ''
    text = (form.get('report') or '').strip()
    min_words = int(report_cfg.get('min_words', 15))
    return {'words': len(text.split()), 'min_words': min_words, 'ok': len(text.split()) >= min_words}, text


def _score_labeling(spec, form, reveal):
    total = correct = 0
    by_field = {}   # label -> [correct, total]: e.g. error category vs severity, issue vs score
    answers_by_item = {}
    items, lines = [], []
    for it in spec.get('items', []):
        iid = it['id']
        fields_out, answers = [], []
        for field in it.get('fields', []):
            raw = (form.get(f"item-{iid}-{field['name']}") or '').strip()
            answers_by_item.setdefault(iid, {})[field['name']] = raw
            ok = _field_correct(field, raw)
            out = {'name': field['name'], 'label': field.get('label', field['name']), 'answer': raw}
            if ok is not None:
                total += 1
                correct += ok
                tally = by_field.setdefault(out['label'], [0, 0])
                tally[0] += ok
                tally[1] += 1
                out['correct'] = ok
                if reveal:
                    out['expected'] = _as_list(field.get('expected'))
            fields_out.append(out)
            answers.append(f"{out['label']}: {raw or '(blank)'}")
        items.append({'id': iid, 'fields': fields_out})
        lines.append(f"[{iid}] " + '; '.join(answers))

    field_score = correct / total if total else 1.0
    report, report_text = _report_result(spec, form)
    if report is not None:
        score = round(100 * (0.9 * field_score + 0.1 * report['ok']))
        if report_text:
            lines.append(f"\nReport:\n{report_text}")
    else:
        score = round(100 * field_score)
    summary = {'correct': correct, 'total': total}
    if not reveal:
        # In an assessment a dimension with only one or two judgements is effectively that
        # item's right/wrong mark -- report only dimensions backed by at least 3.
        by_field = {label: ct for label, ct in by_field.items() if ct[1] >= MIN_JUDGEMENTS_PER_REPORTED_DIMENSION}
    if len(by_field) > 1:
        summary['by_field'] = {label: round(100 * c / t) for label, (c, t) in by_field.items()}
    repeats = [it for it in spec.get('items', []) if it.get('repeat_of')]
    if repeats:
        same = pairs = 0
        for it in repeats:
            original = answers_by_item.get(it['repeat_of'], {})
            for name, value in answers_by_item.get(it['id'], {}).items():
                pairs += 1
                same += bool(value) and value.lower() == (original.get(name) or '').lower()
        if pairs:
            summary['consistency'] = round(100 * same / pairs)
    if report is not None:
        summary['report'] = report
    return score, items, summary, '\n'.join(lines)


def _check_recording(metrics, req):
    checks = []

    def add(name, ok, detail):
        checks.append({'name': name, 'ok': bool(ok), 'detail': detail})

    duration = metrics.get('duration')
    if duration is None:
        add('Recorded', False, 'No recording received')
        return checks
    if 'min_seconds' in req or 'max_seconds' in req:
        lo, hi = req.get('min_seconds', 0), req.get('max_seconds', 10 ** 6)
        add('Length', lo <= duration <= hi, f'{duration:.1f}s (needs {lo}-{hi}s)')
    if 'max_clip_pct' in req and metrics.get('clip_pct') is not None:
        add('No clipping', metrics['clip_pct'] <= req['max_clip_pct'],
            f"{metrics['clip_pct']:.2f}% clipped samples (max {req['max_clip_pct']}%)")
    if 'min_rms_db' in req and metrics.get('rms_db') is not None:
        add('Loud enough', metrics['rms_db'] >= req['min_rms_db'],
            f"{metrics['rms_db']:.1f} dBFS average level (min {req['min_rms_db']} dBFS)")
    if 'max_silence_pct' in req and metrics.get('silence_pct') is not None:
        add('Not mostly silence', metrics['silence_pct'] <= req['max_silence_pct'],
            f"{metrics['silence_pct']:.0f}% silent (max {req['max_silence_pct']}%)")
    return checks


def _score_recording(spec, form, files, uploader):
    req = spec.get('requirements') or {}
    items, lines, passed = [], [], 0
    prompts = spec.get('prompts', [])
    for p in prompts:
        pid = p['id']
        try:
            metrics = json.loads(form.get(f'rec-{pid}-metrics') or '{}')
            metrics = {k: float(v) for k, v in metrics.items() if isinstance(v, (int, float))}
        except (ValueError, TypeError):
            metrics = {}
        checks = _check_recording(metrics, req)
        ok = bool(checks) and all(c['ok'] for c in checks)
        passed += ok
        audio_url = None
        audio = files.get(f'rec-{pid}-audio') if files else None
        if audio and uploader:
            audio_url = uploader(audio)
        items.append({'id': pid, 'prompt': p['text'], 'checks': checks, 'passed': ok, 'audio_url': audio_url,
                      'metrics': metrics})
        lines.append(f"{p['text']} -> {'meets requirements' if ok else 'needs re-recording'}"
                     + (f' ({audio_url})' if audio_url else ''))
    metadata = {}
    meta_missing = 0
    for field in spec.get('metadata_fields', []):
        val = (form.get(f"meta-{field['name']}") or '').strip()
        metadata[field['name']] = val
        meta_missing += not val
        lines.append(f"{field.get('label', field['name'])}: {val or '(blank)'}")
    score = round(100 * passed / len(prompts)) if prompts else 0
    if meta_missing:
        score = max(0, score - 10 * meta_missing)
    summary = {'passed': passed, 'total': len(prompts), 'metadata': metadata,
               'note': 'Audio levels are measured in your browser when you record.'}
    return score, items, summary, '\n'.join(lines)


# ---------------------------------------------------------------- public API

def validate_task_spec(spec):
    """Returns a list of problems with a task_spec (empty list = valid). Used by the seed
    script and the admin API so a malformed spec never reaches a student."""
    errors = []
    if not isinstance(spec, dict) or spec.get('kind') not in TASK_KINDS:
        return [f"kind must be one of {TASK_KINDS}"]
    kind = spec['kind']
    if kind == 'transcription':
        segs = spec.get('segments') or []
        if not segs:
            errors.append('transcription needs at least one segment')
        for s in segs:
            if not s.get('id') or not s.get('reference'):
                errors.append(f'segment missing id/reference: {s}')
    elif kind == 'translation':
        items = spec.get('items') or []
        if not items:
            errors.append('translation needs at least one item')
        for it in items:
            if not it.get('id') or not it.get('source') or not _as_list(it.get('references')):
                errors.append(f"translation item missing id/source/references: {it.get('id')}")
    elif kind == 'labeling':
        items = spec.get('items') or []
        if not items:
            errors.append('labeling needs at least one item')
        for it in items:
            if not it.get('id') or not it.get('fields'):
                errors.append(f"labeling item missing id/fields: {it.get('id')}")
            for f in it.get('fields') or []:
                if f.get('type', 'choice') == 'choice' and f.get('expected') is not None:
                    opts = [str(o).lower() for o in f.get('options') or []]
                    for e in _as_list(f['expected']):
                        if str(e).lower() not in opts:
                            errors.append(f"item {it.get('id')} field {f.get('name')}: expected {e!r} not in options")
    elif kind == 'recording':
        if not spec.get('prompts'):
            errors.append('recording needs at least one prompt')
    return errors


def score_submission(spec, form, files=None, uploader=None, reveal=True):
    """Scores one attempt. `form` is a mapping of submitted field values (request.form),
    `files` the uploaded files (request.files, recording tasks only), `uploader` a
    callable(file) -> url or None. With reveal=False (assessments) expected answers are
    left out of the stored result so a retake can't be answered from the last result.

    Returns {'score': 0-100, 'items': [...], 'summary': {...}, 'content': str} where
    content is a readable record of what the student submitted."""
    kind = spec.get('kind')
    if kind == 'transcription':
        score, items, summary, content = _score_transcription(spec, form, reveal)
    elif kind == 'translation':
        score, items, summary, content = _score_translation(spec, form, reveal)
    elif kind == 'labeling':
        score, items, summary, content = _score_labeling(spec, form, reveal)
    elif kind == 'recording':
        score, items, summary, content = _score_recording(spec, form, files, uploader)
    else:
        raise ValueError(f'unknown task kind: {kind!r}')
    if not reveal and kind != 'recording':
        # Assessments keep only aggregate scores. Per-item right/wrong marks (or per-item
        # accuracy) would let a student retake and flip one answer at a time until every
        # item reads correct, without knowing the material. Recording checks are technical
        # feedback about the student's own audio, not answers, so they stay.
        items = [{'id': it['id']} for it in items]
    return {'kind': kind, 'score': max(0, min(100, score)), 'items': items, 'summary': summary,
            'content': content or '(empty submission)'}


def has_any_answer(spec, form):
    """Whether the student filled in anything at all — an empty form is rejected rather
    than recorded as a 0% attempt."""
    for key, value in form.items():
        if key.startswith(('seg-', 'item-', 'rec-', 'meta-')) or key == 'report':
            if (value or '').strip() and value.strip() != '{}':
                return True
    return False
