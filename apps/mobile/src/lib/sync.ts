/**
 * Driving the offline queue (D1).
 *
 * The queue is flushed on launch, on returning to the foreground, and when the
 * work screen is opened. Every attempt uses the queued client key, so a retry
 * after a timeout stores one submission, not two.
 */
import { ApiError, api } from './api';
import { flush, type FlushReport, type SubmitOutcome } from './offlineQueue';
import { createSqliteStore } from './sqliteQueue';

export const queueStore = createSqliteStore();

export async function flushQueue(): Promise<FlushReport> {
  return flush(queueStore, async (item): Promise<SubmitOutcome> => {
    try {
      const result = await api.post<{ id: number; created: boolean }>(
        `/work/assignments/${item.assignmentId}/submissions`,
        { payload: item.payload, client_key: item.clientKey },
      );
      return {
        status: result.created ? 'saved' : 'already_saved',
        submissionId: result.id,
      };
    } catch (err) {
      if (err instanceof ApiError && err.status >= 400 && err.status < 500) {
        // A rejected submission is kept and retried with backoff: the API may be
        // rejecting an obsolete template, but the student's text is not ours to
        // delete. The screen shows `lastError`.
        return { status: 'rejected', code: err.code, message: err.message };
      }
      throw err;
    }
  });
}
