"""Deterministic scoring for structured practical tasks (services/language_task_service.py).
These scores gate ALL skill assessments and verification, so they must be stable,
diacritic-aware, and never reveal assessment answers."""
import io

from werkzeug.datastructures import FileStorage

from app.services.language_task_service import (
    normalize_tokens, word_error_rate, chrf, parse_timestamp, score_submission, validate_task_spec, has_any_answer,
)


def _audio(seconds=3, mimetype='audio/webm'):
    return FileStorage(io.BytesIO(b'' * int(4000 * seconds)), filename='p1.webm', content_type=mimetype)


def test_tone_marks_count_as_errors_but_are_reported_separately():
    spec = {'kind': 'transcription', 'segments': [{'id': 's1', 'reference': 'Ẹ káàárọ̀, ṣé dáadáa ni?'}]}
    result = score_submission(spec, {'seg-s1-text': 'E kaaaro, se daadaa ni?'})
    assert result['summary']['word_accuracy'] < 50
    assert result['summary']['word_accuracy_no_diacritics'] == 100
    perfect = score_submission(spec, {'seg-s1-text': 'Ẹ káàárọ̀ ṣé dáadáa ni'})
    assert perfect['score'] == 100  # punctuation and case are not scored


def test_nfd_and_nfc_input_score_identically():
    import unicodedata
    ref = 'Ọkọ̀ náà ti dé.'
    nfd = unicodedata.normalize('NFD', ref)
    assert word_error_rate(ref, nfd) == 0.0


def test_tags_are_tokens():
    assert '[inaudible]' in normalize_tokens('we agreed [inaudible] yesterday')
    assert word_error_rate('So we agreed [inaudible] yesterday', 'So we agreed yesterday') == 0.2


def test_speaker_and_timestamp_components():
    spec = {'kind': 'transcription', 'speakers': ['A', 'B'], 'segments': [
        {'id': 's1', 'reference': 'hello', 'speaker': 'A', 'start': 1.0}]}
    good = score_submission(spec, {'seg-s1-text': 'hello', 'seg-s1-speaker': 'A', 'seg-s1-start': '0:01.2'})
    assert good['score'] == 100
    bad = score_submission(spec, {'seg-s1-text': 'hello', 'seg-s1-speaker': 'B', 'seg-s1-start': '5'})
    assert bad['score'] == 70


def test_chrf_bounds():
    assert chrf('Good morning', 'Good morning') == 100.0
    assert chrf('', 'Good morning') == 0.0
    assert 0 < chrf('Good morning, my brother', 'Good morning, my sister') < 100


def test_translation_uses_best_reference_and_key_terms():
    spec = {'kind': 'translation', 'items': [{'id': 't1', 'source': 'x', 'references': ['I am going to the market.', "I'm going to the market."],
                                              'key_terms': ['market']}]}
    assert score_submission(spec, {'item-t1-translation': "I'm going to the market."})['score'] == 100
    assert score_submission(spec, {'item-t1-translation': 'Something else entirely'})['score'] < 40


def test_labeling_choice_number_text_and_report():
    spec = {'kind': 'labeling', 'report': {'min_words': 3}, 'items': [{'id': '1', 'text': 't', 'fields': [
        {'name': 'c', 'type': 'choice', 'options': ['Yes', 'No'], 'expected': 'Yes'},
        {'name': 'n', 'type': 'number', 'expected': 0.4, 'tolerance': 0.005},
        {'name': 'x', 'type': 'text', 'expected': ['five kilometres', 'five kilometers']}]}]}
    full = score_submission(spec, {'item-1-c': 'yes', 'item-1-n': '0.40', 'item-1-x': 'Five kilometers', 'report': 'one two three'})
    assert full['score'] == 100
    no_report = score_submission(spec, {'item-1-c': 'yes', 'item-1-n': '0.40', 'item-1-x': 'five kilometres'})
    assert no_report['score'] == 90
    wrong = score_submission(spec, {'item-1-c': 'No', 'item-1-n': 'abc', 'item-1-x': 'six'})
    assert wrong['score'] == 0


def test_assessment_results_never_contain_expected_answers():
    spec = {'kind': 'labeling', 'items': [{'id': '1', 'text': 't', 'fields': [
        {'name': 'c', 'type': 'choice', 'options': ['Yes', 'No'], 'expected': 'Yes'}]}]}
    hidden = score_submission(spec, {'item-1-c': 'No'}, reveal=False)
    # Assessments keep only aggregates: no expected answers AND no per-item right/wrong
    # marks, which would let a retake flip answers one at a time.
    assert hidden['items'] == [{'id': '1'}]
    assert hidden['score'] == 0 and hidden['summary']['correct'] == 0
    shown = score_submission(spec, {'item-1-c': 'No'}, reveal=True)
    assert shown['items'][0]['fields'][0]['correct'] is False
    assert shown['items'][0]['fields'][0]['expected'] == ['Yes']


def test_recording_checks_and_metadata():
    spec = {'kind': 'recording', 'prompts': [{'id': 'p1', 'text': 'hi'}],
            'requirements': {'min_seconds': 1, 'max_seconds': 10, 'max_clip_pct': 0.5, 'min_rms_db': -40, 'max_silence_pct': 70},
            'metadata_fields': [{'name': 'dialect'}]}
    good = '{"duration": 3, "clip_pct": 0, "rms_db": -25, "silence_pct": 30}'
    assert score_submission(spec, {'rec-p1-metrics': good, 'meta-dialect': 'Ijebu'}, files={'rec-p1-audio': _audio()})['score'] == 100
    assert score_submission(spec, {'rec-p1-metrics': good}, files={'rec-p1-audio': _audio()})['score'] == 90  # missing metadata
    clipped = '{"duration": 3, "clip_pct": 4, "rms_db": -10, "silence_pct": 30}'
    assert score_submission(spec, {'rec-p1-metrics': clipped, 'meta-dialect': 'x'}, files={'rec-p1-audio': _audio()})['score'] == 0
    assert score_submission(spec, {'meta-dialect': 'x'})['score'] == 0  # nothing recorded


def test_uploader_is_called_for_recordings():
    spec = {'kind': 'recording', 'prompts': [{'id': 'p1', 'text': 'hi'}], 'requirements': {}}
    result = score_submission(spec, {'rec-p1-metrics': '{"duration": 2}'}, files={'rec-p1-audio': _audio(2)},
                              uploader=lambda f: 'https://example.com/a.webm')
    assert result['items'][0]['audio_url'] == 'https://example.com/a.webm'


def test_validate_task_spec_catches_bad_specs():
    assert validate_task_spec({'kind': 'nope'})
    assert validate_task_spec({'kind': 'transcription', 'segments': []})
    bad_choice = {'kind': 'labeling', 'items': [{'id': '1', 'fields': [{'name': 'c', 'options': ['A'], 'expected': 'B'}]}]}
    assert validate_task_spec(bad_choice)


def test_has_any_answer_and_timestamps():
    assert not has_any_answer({}, {'csrf_token': 'x', 'rec-p1-metrics': '{}'})
    assert has_any_answer({}, {'item-1-c': 'Yes'})
    assert parse_timestamp('1:05.5') == 65.5
    assert parse_timestamp('bad') is None


def test_curriculum_is_valid():
    import seed_data.all_skills as curriculum
    assert curriculum.validate(validate_task_spec) == []
    assert len(curriculum.CATEGORIES) == 9
    assert len(curriculum.SKILLS) >= 90


def test_labeling_reports_per_dimension_accuracy_and_repeat_consistency():
    spec = {'kind': 'labeling', 'items': [
        {'id': 'a', 'text': 't', 'fields': [{'name': 'cat', 'label': 'Category', 'options': ['X', 'Y'], 'expected': 'X'},
                                            {'name': 'sev', 'label': 'Severity', 'options': ['Minor', 'Major'], 'expected': 'Major'}]},
        {'id': 'ar', 'repeat_of': 'a', 'text': 't', 'fields': [{'name': 'cat', 'label': 'Category', 'options': ['X', 'Y'], 'expected': 'X'},
                                                               {'name': 'sev', 'label': 'Severity', 'options': ['Minor', 'Major'], 'expected': 'Major'}]}]}
    r = score_submission(spec, {'item-a-cat': 'X', 'item-a-sev': 'Minor', 'item-ar-cat': 'Y', 'item-ar-sev': 'Minor'})
    assert r['summary']['by_field'] == {'Category': 50, 'Severity': 0}
    assert r['summary']['consistency'] == 50  # severity answered the same both times, category not


def test_single_dimension_tasks_report_no_breakdown_and_no_consistency():
    spec = {'kind': 'labeling', 'items': [{'id': 'a', 'text': 't', 'fields': [{'name': 'c', 'options': ['X'], 'expected': 'X'}]}]}
    summary = score_submission(spec, {'item-a-c': 'X'})['summary']
    assert 'by_field' not in summary and 'consistency' not in summary


def test_tag_compliance_only_when_tags_are_involved():
    spec = {'kind': 'transcription', 'segments': [{'id': 's1', 'reference': 'we agreed [inaudible] yesterday'},
                                                  {'id': 's2', 'reference': 'hello there'}]}
    r = score_submission(spec, {'seg-s1-text': 'we agreed [noise] yesterday', 'seg-s2-text': 'hello there'})
    assert r['summary']['tag_compliance'] == 0
    plain = score_submission({'kind': 'transcription', 'segments': [{'id': 's1', 'reference': 'hello'}]}, {'seg-s1-text': 'hello'})
    assert 'tag_compliance' not in plain['summary']


def test_translation_reports_terminology_only_when_terms_exist():
    spec = {'kind': 'translation', 'items': [{'id': 't1', 'source': 'x', 'references': ['Please give me water.'], 'key_terms': ['water']}]}
    assert score_submission(spec, {'item-t1-translation': 'Please give me water.'})['summary']['terminology'] == 100
    spec['items'][0]['key_terms'] = []
    assert 'terminology' not in score_submission(spec, {'item-t1-translation': 'Please give me water.'})['summary']


def test_every_all_project_is_labelled_practice_simulation():
    import seed_data.all_skills as curriculum
    for s in curriculum.SKILLS:
        assert s['project']['title'].startswith('Practice Project'), s['slug']
        assert s['project']['description'].startswith('Simulation'), s['slug']


def test_assessment_breakdown_never_exposes_single_item_dimensions():
    """A one- or two-item 'dimension' in an assessment is just that item's right/wrong mark."""
    many = [{'id': f'm{i}', 'text': 't', 'fields': [{'name': 'c', 'label': 'Category', 'options': ['X', 'Y'], 'expected': 'X'},
                                                    {'name': 's', 'label': 'Severity', 'options': ['A', 'B'], 'expected': 'A'}]}
            for i in range(3)]
    single = [{'id': 'one', 'text': 't', 'fields': [{'name': 'i', 'label': 'Intent', 'options': ['P', 'Q'], 'expected': 'P'}]}]
    spec = {'kind': 'labeling', 'items': many + single}
    form = {'item-m0-c': 'X', 'item-m1-c': 'Y', 'item-m2-c': 'X', 'item-m0-s': 'A', 'item-m1-s': 'A', 'item-m2-s': 'A', 'item-one-i': 'Q'}
    hidden = score_submission(spec, form, reveal=False)['summary']['by_field']
    assert hidden == {'Category': 67, 'Severity': 100}           # 'Intent' (1 judgement) withheld
    shown = score_submission(spec, form, reveal=True)['summary']['by_field']
    assert shown['Intent'] == 0                                   # practice may show it


def test_recording_metrics_alone_never_pass():
    """Regression: the levels are browser-reported, so typed-in metrics with no recording
    (or a file too small to hold the claimed length) must not score."""
    spec = {'kind': 'recording', 'prompts': [{'id': 'p1', 'text': 'hi'}], 'requirements': {'min_seconds': 1, 'max_seconds': 10}}
    forged = '{"duration": 5, "clip_pct": 0, "rms_db": -20, "silence_pct": 0}'
    assert score_submission(spec, {'rec-p1-metrics': forged})['score'] == 0
    tiny = FileStorage(io.BytesIO(b'x' * 200), filename='p1.webm', content_type='audio/webm')
    assert score_submission(spec, {'rec-p1-metrics': forged}, files={'rec-p1-audio': tiny})['score'] == 0
    assert score_submission(spec, {'rec-p1-metrics': forged}, files={'rec-p1-audio': _audio(5, 'text/plain')})['score'] == 0
    result = score_submission(spec, {'rec-p1-metrics': forged}, files={'rec-p1-audio': _audio(5)})
    assert result['score'] == 100 and result['items'][0]['checks'][0]['name'] == 'Audio received'


def test_recording_metrics_of_the_wrong_shape_do_not_crash():
    spec = {'kind': 'recording', 'prompts': [{'id': 'p1', 'text': 'hi'}], 'requirements': {}}
    for raw in ('[1, 2]', '5', '"x"', 'null', '{"duration": true}', '{"duration": NaN}'):
        assert score_submission(spec, {'rec-p1-metrics': raw})['score'] == 0, raw


def test_key_terms_match_whole_words_only():
    spec = {'kind': 'translation', 'items': [{'id': 't1', 'source': 'x', 'references': ['ọmọ náà'], 'key_terms': ['ọmọ']}]}
    assert score_submission(spec, {'item-t1-translation': 'ọmọde'})['items'][0]['key_terms_found'] == 0
    assert score_submission(spec, {'item-t1-translation': 'Ọmọ náà'})['items'][0]['key_terms_found'] == 1
