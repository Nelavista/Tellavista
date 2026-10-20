"""Read-path load test against the p95 < 300 ms budget (F6).

Runs a fixed set of the student journey's read endpoints against a running API,
records wall-clock latency per request, and prints p50/p95/p99 per path. The p95
is the number the roadmap promises, so a breach fails the run.

Latency on an empty database proves nothing. The script also reports how many
rows each response carried and warns when the dataset is too small to trust;
`--min-rows` raises that floor.

Usage (local, after `make up`, migrations and `make seed-local`):

    python tools/load_read_paths.py --email student1@example.test --password ...

    # DEV with representative data:
    python tools/load_read_paths.py --base-url https://api-dev.nelavista.com \\
        --email loadtest@example.test --password "$LOADTEST_PASSWORD"

The account must already exist: this script only reads, it never writes data.
Exit codes: 0 within budget, 1 a path exceeded it, 2 the run could not start.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any

import httpx

# (label, path). Only GETs: a load test that writes is a load test that changes
# the database it is measuring.
READ_PATHS: list[tuple[str, str]] = [
    ("me", "/v1/me"),
    ("academia", "/v1/academia/dashboard"),
    ("campus", "/v1/me/campus"),
    ("skills", "/v1/skills"),
    ("my-learning", "/v1/skills/my-learning"),
    ("opportunities", "/v1/opportunities"),
    ("work", "/v1/work/assignments"),
    ("submissions", "/v1/work/submissions"),
    ("earnings", "/v1/money/earnings"),
    ("notifications", "/v1/me/notifications"),
    ("transcript", "/v1/verification/transcript"),
]

# What "representative" means per path. A response with fewer rows than this is
# measured, but flagged, because the query plan that matters at scale is not
# necessarily the one a dozen rows exercise.
MIN_ROWS: dict[str, int] = {
    "skills": 20,
    "opportunities": 25,
    "work": 50,
    "submissions": 100,
    "notifications": 100,
    "transcript": 20,
}

# Nested keys differ per endpoint; the first list found is the row count.
LIST_KEYS = (
    "skills",
    "opportunities",
    "assignments",
    "submissions",
    "notifications",
    "entries",
    "items",
    "lessons",
    "paths",
)


@dataclass
class Sample:
    label: str
    path: str
    latencies: list[float] = field(default_factory=list)
    status: int = 0
    rows: int | None = None
    error: str | None = None

    def percentile(self, p: float) -> float:
        if not self.latencies:
            return float("nan")
        ordered = sorted(self.latencies)
        index = min(len(ordered) - 1, max(0, round((p / 100) * (len(ordered) - 1))))
        return ordered[index]


def count_rows(payload: Any) -> int | None:
    if isinstance(payload, list):
        return len(payload)
    if not isinstance(payload, dict):
        return None
    for key in LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return len(value)
    # Fall back to the largest list anywhere one level down (e.g. {"data": {...}}).
    nested = [len(v) for v in payload.values() if isinstance(v, list)]
    return max(nested) if nested else None


def login(client: httpx.Client, email: str, password: str) -> str:
    res = client.post(
        "/v1/auth/login",
        json={"email": email, "password": password, "platform": "web"},
        headers={"X-API-Version": "v1"},
    )
    if res.status_code != 200:
        raise SystemExit(
            f"login failed ({res.status_code}): {res.text[:300]}\n"
            "Create the account first; this script never registers or writes."
        )
    body = res.json()
    token = body.get("access_token")
    if not token:
        details = body.get("error", {}).get("details", {})
        raise SystemExit(
            "login did not return an access token"
            + (f" (mfa_required: {details.get('mfa_token')})" if details.get("mfa_token") else "")
        )
    return str(token)


def measure(
    base_url: str,
    token: str,
    samples: list[Sample],
    *,
    requests_per_path: int,
    concurrency: int,
) -> None:
    headers = {"Authorization": f"Bearer {token}", "X-API-Version": "v1"}

    def hit(sample: Sample) -> None:
        started = time.perf_counter()
        try:
            with httpx.Client(base_url=base_url, headers=headers, timeout=15.0) as client:
                res = client.get(sample.path)
            elapsed = (time.perf_counter() - started) * 1000
            sample.latencies.append(elapsed)
            sample.status = res.status_code
            if res.status_code == 200:
                try:
                    sample.rows = count_rows(res.json())
                except json.JSONDecodeError:
                    sample.rows = None
            elif sample.error is None:
                sample.error = f"HTTP {res.status_code}: {res.text[:160]}"
        except httpx.HTTPError as exc:
            sample.error = f"{type(exc).__name__}: {exc}"

    jobs = [sample for sample in samples for _ in range(requests_per_path)]
    with ThreadPoolExecutor(max_workers=max(1, concurrency)) as pool:
        list(pool.map(hit, jobs))


def report(samples: list[Sample], *, budget_ms: float, min_rows_floor: int | None) -> int:
    print(f"\n{'path':<16} {'n':>4} {'p50':>8} {'p95':>8} {'p99':>8} {'rows':>6}  verdict")
    print("-" * 72)
    breaches = 0
    warnings: list[str] = []

    for sample in samples:
        p50, p95, p99 = (sample.percentile(p) for p in (50, 95, 99))
        if sample.error and not sample.latencies:
            verdict = f"FAIL - {sample.error}"
            breaches += 1
        elif sample.status != 200:
            verdict = f"FAIL - {sample.error or sample.status}"
            breaches += 1
        elif p95 > budget_ms:
            verdict = f"OVER - p95 {p95:.0f} ms > {budget_ms:.0f} ms"
            breaches += 1
        else:
            verdict = "ok"
        rows = "-" if sample.rows is None else str(sample.rows)
        print(
            f"{sample.label:<16} {len(sample.latencies):>4} {p50:>7.0f}ms "
            f"{p95:>7.0f}ms {p99:>7.0f}ms {rows:>6}  {verdict}"
        )

        floor = min_rows_floor if min_rows_floor is not None else MIN_ROWS.get(sample.label)
        if floor and (sample.rows or 0) < floor:
            warnings.append(
                f"{sample.label}: {sample.rows or 0} rows < {floor}; the p95 above is not yet "
                "representative (seed more data in DEV before quoting it)"
            )

    if warnings:
        print("\nData volume warnings:")
        for warning in warnings:
            print(f"  - {warning}")

    overall = statistics.median(
        [sample.percentile(95) for sample in samples if sample.latencies] or [float("nan")]
    )
    # Plain ASCII in the summary: this prints on Windows terminals whose codepage
    # mangles middle dots, and a garbled budget line is a support ticket.
    print(f"\nMedian of per-path p95: {overall:.0f} ms (budget {budget_ms:.0f} ms)")
    if breaches:
        print(f"FAIL: {breaches} path(s) over budget or broken.")
        return 1
    print("PASS: every read path is within budget.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://localhost:8000")
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--requests", type=int, default=60, help="requests per path (default 60)")
    parser.add_argument("--concurrency", type=int, default=8)
    parser.add_argument("--budget-ms", type=float, default=300.0, help="p95 budget (default 300)")
    parser.add_argument(
        "--min-rows",
        type=int,
        default=None,
        help="override the per-path row floor; 0 disables the warnings",
    )
    parser.add_argument("--only", action="append", help="limit to these labels (repeatable)")
    args = parser.parse_args(argv)

    if args.requests < 20:
        # p95 of 5 samples is just "the slowest of five".
        parser.error("--requests must be at least 20 for a p95 to mean anything")

    selected = [
        (label, path) for label, path in READ_PATHS if not args.only or label in args.only
    ]
    if not selected:
        parser.error(
            f"no matching paths; known labels: {', '.join(label for label, _ in READ_PATHS)}"
        )

    base_url = args.base_url.rstrip("/")
    try:
        with httpx.Client(base_url=base_url, timeout=15.0) as client:
            token = login(client, args.email, args.password)
    except httpx.HTTPError as exc:
        print(f"could not reach {base_url}: {exc}", file=sys.stderr)
        return 2

    print(
        f"Load test against {base_url}: {args.requests} requests/path, "
        f"concurrency {args.concurrency}"
    )
    samples = [Sample(label=label, path=path) for label, path in selected]
    measure(
        base_url,
        token,
        samples,
        requests_per_path=args.requests,
        concurrency=args.concurrency,
    )
    return report(samples, budget_ms=args.budget_ms, min_rows_floor=args.min_rows)


if __name__ == "__main__":
    raise SystemExit(main())
