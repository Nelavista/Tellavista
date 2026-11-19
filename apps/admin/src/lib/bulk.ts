/**
 * Shared helpers for the bulk action bars (review, money, content).
 *
 * The API returns a per-record report rather than a single success flag, because
 * a bulk action that silently skips a record looks like it worked. These helpers
 * turn that report into the one sentence an operator needs, and never hide a
 * failure: a partial batch always names the ids that did not take.
 */
import type { BulkResultOut } from '@nelavista/api-client';

export function bulkNote(result: BulkResultOut, action: string): string {
  // `failed` is optional in the generated schema (the server defaults it to []),
  // so an undefined list is treated as "nothing failed" rather than crashing.
  const failed = result.failed ?? [];
  const parts = [`${result.applied ?? 0} ${action}`];
  if ((result.unchanged ?? 0) > 0) parts.push(`${result.unchanged} already in that state`);
  if (failed.length > 0) {
    const ids = failed.map((row) => `#${row.id} (${row.code})`).join(', ');
    parts.push(`${failed.length} failed: ${ids}`);
  }
  return `${parts.join(' · ')}.`;
}

export function toggleId(current: number[], id: number): number[] {
  return current.includes(id) ? current.filter((value) => value !== id) : [...current, id];
}
