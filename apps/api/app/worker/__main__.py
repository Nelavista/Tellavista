"""Worker process: `python -m app.worker`.

Runs forever, draining due jobs and sleeping when the queue is empty. It is a
separate Render service (same image, different command) so a slow email never
blocks an API request.
"""
from __future__ import annotations

import logging
import time

from app.db.session import SessionLocal
from app.worker.runner import drain


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    logging.getLogger(__name__).info("worker started")
    while True:
        with SessionLocal() as db:
            processed = drain(db, limit=20)
        if not processed:
            time.sleep(2)


if __name__ == "__main__":
    main()
