# Runbook — Read-path load test

The roadmap promises **p95 < 300 ms** on the student journey's read paths. F6
exists because that number is a promise, not a hope: this runbook is how it gets
measured, and `tools/load_read_paths.py` is what measures it.

## What it measures

Eleven GETs, the ones a student's screen actually fires:

| Label | Path |
|---|---|
| me | `/v1/me` |
| academia | `/v1/academia/dashboard` |
| campus | `/v1/me/campus` |
| skills | `/v1/skills` |
| my-learning | `/v1/skills/my-learning` |
| opportunities | `/v1/opportunities` |
| work | `/v1/work/assignments` |
| submissions | `/v1/work/submissions` |
| earnings | `/v1/money/earnings` |
| notifications | `/v1/me/notifications` |
| transcript | `/v1/verification/transcript` |

Nothing is written: the script cannot change the data it is measuring.

## Running it

The account must already exist and, in DEV, must be a **load-test account, never
a real student's**.

```bash
# local (API on :8000, migrations applied, `make seed-local` for a small dataset)
make load-test EMAIL=student1@example.test PASSWORD='…'

# DEV, representative volumes
python tools/load_read_paths.py \
  --base-url https://api-dev.nelavista.com \
  --email loadtest@example.test --password "$LOADTEST_PASSWORD" \
  --requests 100 --concurrency 8
```

Useful flags: `--requests` (per path, minimum 20 — a p95 of five samples is just
the slowest of five), `--concurrency`, `--budget-ms` (default 300), `--only label`
(repeatable), `--min-rows` (override the row floor).

Exit codes: `0` within budget, `1` a path exceeded it or returned non-200, `2`
the API could not be reached or the login failed.

## Reading the output

```
path                n      p50      p95      p99   rows  verdict
skills             60    41ms     78ms    102ms     24  ok
work               60   120ms    290ms    340ms    180  ok
```

- **p95 is the budget.** p50 hides the tail a student on a slow link feels.
- **`rows` is part of the result.** A p95 measured on twelve rows does not
  predict twelve hundred: the script prints a warning when a path is below its
  row floor (`--min-rows 0` silences it, which is only appropriate when you are
  testing the shape of the response, not its budget).
- **Median of per-path p95** is the one-line summary to paste into a PR.

## What to do when a path is over budget

1. Re-run once: a CI runner or a cold laptop is noisy.
2. Check the row counts. If they are below the floor, seed more data first.
3. Explain the query before changing it: `EXPLAIN (ANALYZE, BUFFERS)` on the
   statement the route emits, against DEV, is the only evidence that matters.
4. The usual fixes, in order of preference: an index that matches the WHERE and
   ORDER BY; removing an N+1 in the serializer; pagination that actually limits
   (the cursor envelope already exists); caching only if the data tolerates it.

## Cadence

Run it before any change to a read path that touches more than one table, and
once against DEV before a release. It is deliberately a script and not a CI job:
shared runners make wall-clock budgets flaky, and a flaky budget gets ignored.
