/**
 * SQLite storage for the offline queue (D1).
 *
 * One row per queued submission. The payload is JSON text; the queue rules live
 * in `offlineQueue.ts`, so this file only reads and writes rows.
 */
import * as SQLite from 'expo-sqlite';

import type { QueueStore, QueuedSubmission } from './offlineQueue';

type Row = {
  client_key: string;
  assignment_id: number;
  payload: string;
  created_at: number;
  attempts: number;
  next_attempt_at: number;
  last_error: string | null;
};

export function createSqliteStore(): QueueStore {
  const db = SQLite.openDatabaseSync('nelavista.db');
  db.execSync(`
    CREATE TABLE IF NOT EXISTS submission_queue (
      client_key TEXT PRIMARY KEY NOT NULL,
      assignment_id INTEGER NOT NULL,
      payload TEXT NOT NULL,
      created_at INTEGER NOT NULL,
      attempts INTEGER NOT NULL DEFAULT 0,
      next_attempt_at INTEGER NOT NULL,
      last_error TEXT
    );
  `);

  return {
    async load() {
      const rows = db.getAllSync<Row>(
        'SELECT client_key, assignment_id, payload, created_at, attempts, next_attempt_at, last_error FROM submission_queue ORDER BY created_at',
      );
      return rows.map((row) => ({
        clientKey: row.client_key,
        assignmentId: row.assignment_id,
        payload: JSON.parse(row.payload) as Record<string, unknown>,
        createdAt: row.created_at,
        attempts: row.attempts,
        nextAttemptAt: row.next_attempt_at,
        lastError: row.last_error ?? undefined,
      }));
    },

    async save(items: QueuedSubmission[]) {
      db.withTransactionSync(() => {
        db.execSync('DELETE FROM submission_queue');
        for (const item of items) {
          db.runSync(
            'INSERT INTO submission_queue (client_key, assignment_id, payload, created_at, attempts, next_attempt_at, last_error) VALUES (?, ?, ?, ?, ?, ?, ?)',
            [
              item.clientKey,
              item.assignmentId,
              JSON.stringify(item.payload),
              item.createdAt,
              item.attempts,
              item.nextAttemptAt,
              item.lastError ?? null,
            ],
          );
        }
      });
    },
  };
}
