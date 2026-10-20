"""Phase 6 — the 90/8/2 split is exact, and no minor unit is invented or lost.

The PRD gives one worked example ($10,000) and one rule that matters more than the
example: the department's 2% comes out of the fee, never out of the student's 90%.
The property-style loops below assert both for every total they try, which is the
closest thing to a proof this suite can carry without a hypothesis dependency.
"""
from __future__ import annotations

import pytest

from app.services.money.split import allocate, split_project_value


def test_the_prd_example_is_exact() -> None:
    split = split_project_value(1_000_000)  # $10,000.00 in minor units

    assert split.student_pool_minor == 900_000
    assert split.platform_retained_minor == 80_000
    assert split.platform_fee_minor == 100_000
    assert split.department_share_minor == 20_000
    assert (
        split.student_pool_minor + split.platform_retained_minor + split.department_share_minor
        == split.total_minor
    )


def test_the_split_conserves_value_for_every_small_total() -> None:
    for total in range(0, 1_001):
        split = split_project_value(total)
        assert (
            split.student_pool_minor
            + split.platform_retained_minor
            + split.department_share_minor
            == total
        )
        assert split.platform_fee_minor == (
            split.platform_retained_minor + split.department_share_minor
        )


def test_department_share_never_reduces_the_students_share() -> None:
    for total in range(0, 5_001):
        split = split_project_value(total)
        assert split.student_pool_minor >= (total * 90) // 100
        # The fee is always taken from the total first; the department comes after.
        assert split.student_pool_minor == total - split.platform_fee_minor


def test_a_negative_value_is_rejected() -> None:
    with pytest.raises(ValueError):
        split_project_value(-1)


def test_allocation_sums_to_the_pool() -> None:
    weights = {1: 3, 2: 5, 3: 1, 4: 0}
    for pool in range(0, 500):
        amounts = allocate(pool, weights)
        assert sum(amounts.values()) == pool
        assert amounts[4] == 0  # zero weight, zero pay


def test_allocation_is_deterministic_and_largest_remainder_wins() -> None:
    # Three equal students cannot share 100 exactly; the extra unit goes to the
    # lowest user id by the documented tie-break.
    amounts = allocate(100, {7: 1, 3: 1, 5: 1})
    assert amounts == {3: 34, 5: 33, 7: 33}
    assert allocate(100, {7: 1, 3: 1, 5: 1}) == amounts


def test_allocation_with_no_weight_returns_zeroes() -> None:
    assert allocate(500, {1: 0, 2: 0}) == {1: 0, 2: 0}
    assert allocate(500, {}) == {}
