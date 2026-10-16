"""Guarded entrypoint for LOCAL/DEV sample data.

    python -m tools.seed_local            # local / dev
    # refuses a production target unless --i-know-this-is-production is passed

This is the ONLY way to run the seed. It enforces the prod guard (ADR-0002) and
always prints the masked database target first.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))            # for `tools` import
sys.path.insert(0, str(REPO_ROOT / "apps" / "api"))  # so `app` == apps/api/app

from tools.prodguard import guard  # noqa: E402

guard("seed_local")

try:
    from app.seed.local import run
except ModuleNotFoundError as exc:  # pragma: no cover - env not bootstrapped yet
    sys.stderr.write(
        "Could not import apps/api. Install its dependencies first:\n"
        "    uv sync --all-packages   (or: pip install -r apps/api/pyproject.toml)\n"
        f"Underlying error: {exc}\n"
    )
    raise SystemExit(2) from exc

result = run()
print("seed_local complete:", ", ".join(f"{k}={v}" for k, v in result.items()))
