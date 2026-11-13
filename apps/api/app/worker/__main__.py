"""Worker process: `python -m app.worker`.

Runs forever, draining due jobs and sleeping when the queue is empty. It is a
separate Render service (same image, different command) so a slow email never
blocks an API request.
"""
from __future__ import annotations

import logging
import time

from app.db.schema_guard import check_schema, upgrade_database
from app.db.session import SessionLocal, engine
from app.worker.runner import drain
from app.worker.scheduler import enqueue_scheduled


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    # Same migration + guard as the API: a worker running ahead of the schema
    # would fail jobs in the background where nobody sees the 500. The advisory
    # lock means it waits instead of racing the web service.
    upgrade_database(engine)
    check_schema(engine)
    logging.getLogger(__name__).info("worker started")
    while True:
        with SessionLocal() as db:
            enqueue_scheduled(db)
            processed = drain(db, limit=20)
        if not processed:
            time.sleep(2)


if __name__ == "__main__":
    main()
