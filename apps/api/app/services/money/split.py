"""The money split, in integers, with an explicit rounding rule (PRD §9, ADR-0008).

The PRD's promise: from a project value of $10,000, students receive $9,000, the
participating department $200 and Nelavista $800. The department share is taken
**from the fee**, never from the student pool.

Rounding rule (proposed, needs approval before real money):

1. fee   = round_half_up(total × 10%)   → (total × 10 + 50) // 100
2. dept  = round_half_up(fee × 20%)     → (fee × 20 + 50) // 100
3. platform keeps fee − dept
4. students get total − fee

Rounding therefore always favours the student pool: `student_pool` is never below
`floor(total × 90%)`, and any leftover minor unit lands with the platform, not with
the student or the department. For 1,000,000 minor units this yields exactly
900,000 / 80,000 / 20,000.

Per-student allocation uses **largest remainder**: every student gets the floor of
their proportional share, and the remaining minor units go one each to the largest
remainders (ties broken by ascending user id, which is deterministic). The
allocation sums exactly to the pool — no cent is invented or lost.
"""
from __future__ import annotations

from dataclasses import dataclass

FEE_PERCENT = 10
DEPARTMENT_SHARE_OF_FEE_PERCENT = 20


@dataclass(frozen=True)
class Split:
    total_minor: int
    student_pool_minor: int
    platform_fee_minor: int
    platform_retained_minor: int
    department_share_minor: int

    def as_dict(self) -> dict[str, int]:
        return {
            "total_minor": self.total_minor,
            "student_pool_minor": self.student_pool_minor,
            "platform_fee_minor": self.platform_fee_minor,
            "platform_retained_minor": self.platform_retained_minor,
            "department_share_minor": self.department_share_minor,
        }


def split_project_value(total_minor: int) -> Split:
    if total_minor < 0:
        raise ValueError("project value cannot be negative")
    fee = (total_minor * FEE_PERCENT + 50) // 100
    department = (fee * DEPARTMENT_SHARE_OF_FEE_PERCENT + 50) // 100
    platform = fee - department
    students = total_minor - fee
    split = Split(
        total_minor=total_minor,
        student_pool_minor=students,
        platform_fee_minor=fee,
        platform_retained_minor=platform,
        department_share_minor=department,
    )
    # The invariant the tests (and reconciliation) enforce.
    assert (
        split.student_pool_minor
        + split.platform_retained_minor
        + split.department_share_minor
        == total_minor
    )
    assert split.student_pool_minor >= (total_minor * 90) // 100
    return split


def allocate(student_pool_minor: int, weights: dict[int, int]) -> dict[int, int]:
    """Split a pool across students by approved-work weight, exactly.

    `weights` maps user id to a non-negative integer (for example, approved task
    count). A student with weight zero receives zero. The result always sums to
    `student_pool_minor`.
    """
    if student_pool_minor < 0:
        raise ValueError("student pool cannot be negative")
    clean = {user_id: max(0, int(weight)) for user_id, weight in weights.items()}
    total_weight = sum(clean.values())
    if total_weight <= 0:
        return {user_id: 0 for user_id in clean}

    amounts: dict[int, int] = {}
    remainders: list[tuple[int, int]] = []
    allocated = 0
    for user_id, weight in sorted(clean.items()):
        numerator = student_pool_minor * weight
        base, remainder = divmod(numerator, total_weight)
        amounts[user_id] = base
        allocated += base
        remainders.append((remainder, user_id))

    leftover = student_pool_minor - allocated
    # Largest remainder first; ties by user id ascending for determinism.
    remainders.sort(key=lambda item: (-item[0], item[1]))
    for _remainder, user_id in remainders[:leftover]:
        amounts[user_id] += 1

    assert sum(amounts.values()) == student_pool_minor
    return amounts
