/**
 * Mobile shell rules that must hold without a device: nothing is lost offline,
 * a retry is idempotent, links resolve to the right screen, and an old build is
 * told to update.
 */
import { describe, expect, it } from 'vitest';

import { parseDeepLink } from './deepLink';
import { backoffFor, createMemoryStore, enqueue, flush } from './offlineQueue';
import { answerFor, controlFor } from './taskForm';
import { compareVersions, needsUpdate } from './version';

describe('offline queue', () => {
  it('keeps a queued item until the API has stored it', async () => {
    const store = createMemoryStore();
    const item = await enqueue(store, 12, { key: 'positive' }, 1_000);

    const pending = await flush(store, async () => ({ status: 'rejected', message: 'offline' }), 1_000);
    expect(pending.remaining).toBe(1);
    const rows = await store.load();
    expect(rows[0]?.clientKey).toBe(item.clientKey);
    expect(rows[0]?.lastError).toBe('offline');
    expect(rows[0]?.nextAttemptAt).toBeGreaterThan(1_000);
  });

  it('removes an item after saved or already_saved and never duplicates a payload', async () => {
    const store = createMemoryStore();
    const first = await enqueue(store, 7, { key: 'negative' }, 1_000);
    const second = await enqueue(store, 7, { key: 'negative' }, 1_100);
    expect(second.clientKey).toBe(first.clientKey);

    const report = await flush(store, async () => ({ status: 'already_saved' }), 2_000);
    expect(report).toEqual({ attempted: 1, saved: 1, rejected: 0, remaining: 0 });
    expect(await store.load()).toHaveLength(0);
  });

  it('backs off further after each attempt, with a ceiling', () => {
    expect(backoffFor(1)).toBeLessThan(backoffFor(2));
    expect(backoffFor(50)).toBe(backoffFor(5));
  });

  it('does not attempt an item before its retry time', async () => {
    const store = createMemoryStore([
      {
        clientKey: 'mobile-a',
        assignmentId: 1,
        payload: { value: 3 },
        createdAt: 0,
        attempts: 1,
        nextAttemptAt: 10_000,
      },
    ]);
    let called = 0;
    const report = await flush(
      store,
      async () => {
        called += 1;
        return { status: 'saved' };
      },
      5_000,
    );
    expect(called).toBe(0);
    expect(report.remaining).toBe(1);
  });
});

describe('deep links', () => {
  it('resolves custom-scheme and universal links to the same route', () => {
    expect(parseDeepLink('nelavista://skills/lessons/intro')).toEqual({ name: 'lesson', slug: 'intro' });
    expect(parseDeepLink('https://nelavista.com/skills/lessons/intro')).toEqual({
      name: 'lesson',
      slug: 'intro',
    });
    expect(parseDeepLink('https://nelavista.com/work/assignments/9')).toEqual({
      name: 'assignment',
      id: 9,
    });
    expect(parseDeepLink('https://nelavista.com/verification/assessments/annotation')).toEqual({
      name: 'assessment',
      slug: 'annotation',
    });
  });

  it('refuses a foreign host or unknown path', () => {
    expect(parseDeepLink('https://evil.example/skills')).toBeNull();
    expect(parseDeepLink('https://nelavista.com/nope')).toBeNull();
  });
});

describe('task controls', () => {
  it('builds the answer object the validator expects', () => {
    const control = controlFor(
      { options: [{ key: 'positive', label: 'Positive' }] },
      { type: 'object', properties: { key: { type: 'string' } } },
    );
    expect(answerFor(control, 'positive')).toEqual({ key: 'positive' });
    expect(answerFor(control, null)).toBeNull();
  });

  it('refuses a task it cannot render instead of sending noise', () => {
    const control = controlFor({ text: 'hello' }, { spans: [] });
    expect(control.kind).toBe('unsupported');
    expect(answerFor(control, 'anything')).toBeNull();
  });
});

describe('version policy', () => {
  it('compares dotted versions numerically', () => {
    expect(compareVersions('1.0.0', '1.0.1')).toBe(-1);
    expect(compareVersions('1.10.0', '1.9.9')).toBe(1);
    expect(compareVersions('2.0', '2.0.0')).toBe(0);
  });

  it('blocks only a build below the minimum', () => {
    expect(needsUpdate('1.0.0', '1.1.0')).toBe(true);
    expect(needsUpdate('1.1.0', '1.1.0')).toBe(false);
    expect(needsUpdate('1.2.0', '1.1.0')).toBe(false);
    expect(needsUpdate('1.0.0', null)).toBe(false);
  });
});
