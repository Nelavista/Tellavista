"""Unit tests for evaluate_project_submission's ground-truth scoring: the AI proposes a
score per PROJECT_REVIEW_DIMENSIONS, but the overall score returned to the caller must
always be Python's own clamped average of those dimensions -- never whatever total (if
any) the AI's raw JSON happened to include. Mirrors the same discipline
evaluate_final_project already applies to rubric criteria, and locks in the 'score' key
staying a top-level 0-100 int, since services/skills_service.py's
_project_counts_as_verified reads exactly that key.

Mocks requests.post directly -- these test pure scoring/parsing logic, not real network
calls or the Flask app (no app/db fixture needed, matching how services/ai_service.py's
functions don't touch the database themselves).
"""
import json
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('SECRET_KEY', 'test-secret-key-for-pytest-only')

from services.ai_service import evaluate_project_submission, PROJECT_REVIEW_DIMENSIONS


def _mock_response(payload_dict):
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = {'choices': [{'message': {'content': json.dumps(payload_dict)}}]}
    return resp


def test_overall_score_is_rounded_mean_of_dimensions_not_ai_total():
    ai_payload = {
        'dimension_scores': {'functionality': 80, 'craft_quality': 60, 'problem_solving': 100,
                              'documentation': 40, 'originality': 70},
        # Deliberately a different number from the true mean, to prove it's ignored.
        'overall_score': 999,
        'strengths': ['Clear structure'], 'improvements': ['Add tests'],
        'explanation': 'Solid work.', 'next_project': {'title': 'Next thing', 'description': 'Build more.'},
    }
    with patch('services.ai_service.requests.post', return_value=_mock_response(ai_payload)):
        result = evaluate_project_submission('Test Project', 'A brief', 'Submission details', ['Python'])

    true_mean = round((80 + 60 + 100 + 40 + 70) / 5)
    assert result['score'] == true_mean
    assert result['score'] != 999
    assert result['dimension_scores'] == {'functionality': 80, 'craft_quality': 60, 'problem_solving': 100,
                                           'documentation': 40, 'originality': 70}
    assert result['next_project'] == {'title': 'Next thing', 'description': 'Build more.'}
    assert result['next_step'] == 'Next thing'  # backward-compat field


def test_out_of_range_dimension_scores_are_clamped_to_0_100():
    ai_payload = {
        'dimension_scores': {'functionality': 150, 'craft_quality': -20, 'problem_solving': 50,
                              'documentation': 50, 'originality': 50},
        'strengths': [], 'improvements': [], 'explanation': '', 'next_project': {},
    }
    with patch('services.ai_service.requests.post', return_value=_mock_response(ai_payload)):
        result = evaluate_project_submission('Test Project', None, 'details', [])

    assert result['dimension_scores']['functionality'] == 100  # clamped down from 150
    assert result['dimension_scores']['craft_quality'] == 0    # clamped up from -20
    assert result['score'] == round((100 + 0 + 50 + 50 + 50) / 5)


def test_missing_or_malformed_dimension_scores_default_to_zero():
    ai_payload = {
        'dimension_scores': {'functionality': 'not-a-number'},  # missing 4 of 5 dimensions entirely
        'strengths': [], 'improvements': [], 'explanation': '',
    }
    with patch('services.ai_service.requests.post', return_value=_mock_response(ai_payload)):
        result = evaluate_project_submission('Test Project', None, 'details', [])

    assert set(result['dimension_scores'].keys()) == set(PROJECT_REVIEW_DIMENSIONS)
    assert result['dimension_scores']['functionality'] == 0  # non-numeric -> defaults to 0
    assert result['dimension_scores']['craft_quality'] == 0  # absent -> defaults to 0
    assert result['score'] == 0
    assert result['next_project'] == {'title': '', 'description': ''}


def test_reflections_are_included_in_the_prompt_when_provided():
    ai_payload = {
        'dimension_scores': {d: 50 for d in PROJECT_REVIEW_DIMENSIONS},
        'strengths': [], 'improvements': [], 'explanation': '', 'next_project': {},
    }
    with patch('services.ai_service.requests.post', return_value=_mock_response(ai_payload)) as mock_post:
        evaluate_project_submission(
            'Test Project', None, 'details', [],
            reflections={'problem_solved': 'Saves time on X', 'challenges': 'Debugging Y', 'improvements': 'Add Z'},
        )

    sent_prompt = mock_post.call_args.kwargs['json']['messages'][1]['content']
    assert 'Saves time on X' in sent_prompt
    assert 'Debugging Y' in sent_prompt
    assert 'Add Z' in sent_prompt


def test_missing_reflections_render_as_not_provided():
    ai_payload = {
        'dimension_scores': {d: 50 for d in PROJECT_REVIEW_DIMENSIONS},
        'strengths': [], 'improvements': [], 'explanation': '', 'next_project': {},
    }
    with patch('services.ai_service.requests.post', return_value=_mock_response(ai_payload)) as mock_post:
        evaluate_project_submission('Test Project', None, 'details', [])  # no reflections kwarg at all

    sent_prompt = mock_post.call_args.kwargs['json']['messages'][1]['content']
    assert sent_prompt.count('(not provided)') == 3
