# ADR-0011 — Money rounding and per-student allocation

**Status:** Accepted · **Date:** 2026-10-17
**Extends:** ADR-0008 (integer minor units, append-only ledger). **Code:** `apps/api/app/services/money/split.py`

## Context

ADR-0008 fixes the split — student 90%, Nelavista fee 10%, department 20% **of the fee** — but not how to round when the percentages do not land on a whole minor unit. Two rules are needed, and both must be deterministic across the API, the ledger job and any client that previews a number:

1. **the three-way split** of a project value, and
2. **the per-student allocation** of the student pool.

Without a written rule, the same project can produce different totals in the API, a reconciliation script and an admin CSV. Money that does not add up destroys trust faster than money that is late.

## Decision

### The split

For a project value `total` in integer minor units:

```
fee        = round_half_up(total × 10%)       → (total × 10 + 50) // 100
department = round_half_up(fee   × 20%)       → (fee   × 20 + 50) // 100
platform   = fee − department
students   = total − fee
```

- Rounding is **half up** on the exact integer arithmetic — no floats at any point.
- The department share is always taken **from the fee**, never from the student pool.
- Any rounding leftover lands with **the platform**. The student pool is therefore never below `floor(total × 90%)`, and never above `total − fee`.
- Invariants, asserted in code and re-checked by reconciliation:
  `students + platform + department == total` and `students >= (total × 90) // 100`.

Example: 1,000,000 minor units → 900,000 students / 80,000 platform / 20,000 department, matching the PRD's ₦10,000 illustration.

### The per-student allocation

The pool is allocated by **largest remainder**:

1. Each student gets `floor(pool × weight / total_weight)`.
2. The leftover minor units go one each, in order of largest remainder.
3. Ties are broken by **ascending user id**, so the result is reproducible for any row order.

A student with zero weight receives zero. The allocation always sums exactly to the pool — no unit is invented or lost.

## Consequences

- Every surface can predict a split without calling the API, and reconciliation can prove it.
- The platform absorbs every rounding unit. This is a deliberate, one-directional rule: it never shortens a student's pay for rounding.
- Changing the rule later is a **ledger migration**, not a code change: existing entries stay as posted. Treat this ADR as binding for new postings.

## Options considered

- **Round the student pool up instead**: rejected — it can make `students + fee > total`, which is not payable from the project value.
- **Give leftovers to the department**: rejected — the department share is derived from the fee, and mixing sources makes the three-way split unprovable.
- **Split per student first, then fee**: rejected — it lets per-student rounding drift the total, and makes the 90% promise depend on cohort size.
