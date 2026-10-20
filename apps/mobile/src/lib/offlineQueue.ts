/**
 * The offline submission queue (D1, ADR-0007).
 *
 * A student may lose signal mid-task. Every submission is written to the queue
 * first, with a client key generated once; the same key is what the API uses to
 * make the retry idempotent. Nothing is deleted until the API has stored it
 * (`saved` or `already_saved`). A rejection is kept with its reason and retried
 * with backoff, because deleting a student's work to make the queue look clean is
 * the one unacceptable outcome.
 *
 * The store is an interface so the SQLite implementation can be swapped for an
 * in-memory one in tests, and so the rules above are testable without a device.
 */

export type QueuedSubmission = {
  clientKey: string;
  assignmentId: number;
  payload: Record<string, unknown>;
  createdAt: number;
  attempts: number;
  nextAttemptAt: number;
  lastError?: string;
};

export interface QueueStore {
  load(): Promise<QueuedSubmission[]>;
  save(items: QueuedSubmission[]): Promise<void>;
}

const BACKOFF_MS = [5_000, 15_000, 60_000, 300_000, 900_000];

export function backoffFor(attempts: number): number {
  const index = Math.min(Math.max(attempts - 1, 0), BACKOFF_MS.length - 1);
  return BACKOFF_MS[index] ?? BACKOFF_MS[BACKOFF_MS.length - 1] ?? 60_000;
}

export function newClientKey(prefix = 'mobile'): string {
  // `crypto.randomUUID` is available in Hermes; the fallback keeps old devices
  // working without weakening the idempotency guarantee (the key is still unique
  // enough for one device's queue).
  const maybeCrypto = globalThis.crypto as { randomUUID?: () => string } | undefined;
  if (maybeCrypto?.randomUUID) return `${prefix}-${maybeCrypto.randomUUID()}`;
  return `${prefix}-${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

export async function enqueue(
  store: QueueStore,
  assignmentId: number,
  payload: Record<string, unknown>,
  now = Date.now(),
): Promise<QueuedSubmission> {
  const items = await store.load();
  const existing = items.find(
    (item) => item.assignmentId === assignmentId && JSON.stringify(item.payload) === JSON.stringify(payload),
  );
  if (existing) return existing;
  const item: QueuedSubmission = {
    clientKey: newClientKey(),
    assignmentId,
    payload,
    createdAt: now,
    attempts: 0,
    nextAttemptAt: now,
  };
  await store.save([...items, item]);
  return item;
}

export function due(items: QueuedSubmission[], now = Date.now()): QueuedSubmission[] {
  return items.filter((item) => item.nextAttemptAt <= now).sort((a, b) => a.createdAt - b.createdAt);
}

export type SubmitOutcome =
  | { status: 'saved' | 'already_saved'; submissionId?: number }
  | { status: 'rejected'; code?: string; message?: string };

export type FlushReport = {
  attempted: number;
  saved: number;
  rejected: number;
  remaining: number;
};

/**
 * Send every due item once. The API's answer decides the queue's next state:
 * a rejection keeps the item with a backoff, never drops it.
 */
export async function flush(
  store: QueueStore,
  submit: (item: QueuedSubmission) => Promise<SubmitOutcome>,
  now = Date.now(),
): Promise<FlushReport> {
  const items = await store.load();
  let saved = 0;
  let rejected = 0;
  let attempted = 0;

  for (const item of due(items, now)) {
    attempted += 1;
    try {
      const outcome = await submit(item);
      // Test the narrow member first: `status` on the success member is itself a
      // union, so an `!== 'saved'` check cannot eliminate it in the else branch.
      if (outcome.status === 'rejected') {
        rejected += 1;
        item.attempts += 1;
        item.lastError = outcome.message ?? outcome.code ?? 'Rejected';
        item.nextAttemptAt = now + backoffFor(item.attempts);
      } else {
        saved += 1;
        const index = items.findIndex((row) => row.clientKey === item.clientKey);
        if (index >= 0) items.splice(index, 1);
      }
    } catch (err) {
      rejected += 1;
      item.attempts += 1;
      item.lastError = err instanceof Error ? err.message : 'Network error';
      item.nextAttemptAt = now + backoffFor(item.attempts);
    }
  }

  await store.save(items);
  return { attempted, saved, rejected, remaining: items.length };
}

/** In-memory store: tests, and a device whose SQLite file cannot be opened. */
export function createMemoryStore(initial: QueuedSubmission[] = []): QueueStore {
  let items = [...initial];
  return {
    load: async () => [...items],
    save: async (next) => {
      items = [...next];
    },
  };
}
