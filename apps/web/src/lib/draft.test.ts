/**
 * Draft storage (B6). The rules worth testing are the ones that protect a
 * student's typed answer: a value round-trips, anything unreadable is ignored
 * rather than rendered into a form, and a retry keeps the same idempotency key.
 */
import { beforeEach, describe, expect, it } from 'vitest';

import { clearDraft, draftKey, readDraft, stableClientKey, writeDraft } from './draft';

describe('draft storage', () => {
  beforeEach(() => localStorage.clear());

  it('round-trips a value and reports when it was saved', () => {
    const key = draftKey('practice', 7, 12);
    const savedAt = writeDraft(key, 'positive');

    const draft = readDraft<string>(key);
    expect(draft?.value).toBe('positive');
    expect(draft?.savedAt).toBe(savedAt);
  });

  it('treats a null answer as "cleared", not as a stored value', () => {
    const key = draftKey('practice', 7, 12);
    writeDraft(key, 'positive');

    expect(writeDraft(key, null)).toBeNull();
    expect(readDraft(key)).toBeNull();
    expect(localStorage.getItem(key)).toBeNull();
  });

  it('ignores a draft written by a different version', () => {
    const key = draftKey('practice', 7, 12);
    localStorage.setItem(key, JSON.stringify({ version: 99, saved_at: 1, value: 'positive' }));

    expect(readDraft(key)).toBeNull();
  });

  it('ignores corrupt JSON instead of throwing', () => {
    const key = draftKey('practice', 7, 12);
    localStorage.setItem(key, '{not json');

    expect(readDraft(key)).toBeNull();
  });

  it('refuses a value the screen cannot render', () => {
    const key = draftKey('practice', 7, 12);
    writeDraft(key, { unexpected: true });

    expect(readDraft(key, (value) => typeof value === 'string')).toBeNull();
  });

  it('builds a key with no separator a caller can inject', () => {
    expect(draftKey('practice', 'a:b', 1)).toBe('nv.draft.v1:practice:a_b:1');
  });

  it('reuses one client key until it is cleared, so a retry is one submission', () => {
    const key = draftKey('work-client-key', 7, 3);
    const first = stableClientKey(key);
    expect(stableClientKey(key)).toBe(first);

    clearDraft(key);
    expect(stableClientKey(key)).not.toBe(first);
  });
});
