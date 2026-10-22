/**
 * Answers that survive a dropped connection (B6).
 *
 * The mobile app writes every submission to a SQLite queue before sending it
 * (ADR-0007). The web has no such queue, so this is the equivalent guarantee at
 * the smallest useful size: the answer is written to `localStorage` as it is
 * typed, and only the server accepting it clears the draft. A reload, a closed
 * tab, a dead network or a failed submit therefore never silently loses work.
 *
 * Drafts are per student and per task (the key carries both), versioned so an
 * older shape is ignored rather than restored as garbage, and every storage call
 * is guarded: private-mode Safari throws on access, and a full quota must not
 * crash a form.
 */
import * as React from 'react';

const VERSION = 1;
const PREFIX = 'nv.draft.v1:';

export type StoredDraft<T> = { value: T; savedAt: number };

function storage(): Storage | null {
  try {
    return globalThis.localStorage ?? null;
  } catch {
    // Access itself throws when storage is disabled, not just the read.
    return null;
  }
}

/** Build a key from parts, so an id can never contain the separator. */
export function draftKey(...parts: Array<string | number>): string {
  return (
    PREFIX +
    parts
      .map((part) => String(part).replace(/[^a-zA-Z0-9._-]/g, '_'))
      .join(':')
  );
}

/**
 * Read a draft. `accept` guards the shape, because a draft from an older build
 * of the same screen is a real possibility. A `null` value counts as absent.
 */
export function readDraft<T>(
  key: string,
  accept?: (value: unknown) => boolean,
): StoredDraft<T> | null {
  const store = storage();
  if (!store) return null;
  let raw: string | null;
  try {
    raw = store.getItem(key);
  } catch {
    return null;
  }
  if (raw === null) return null;
  try {
    const parsed = JSON.parse(raw) as { version?: unknown; saved_at?: unknown; value?: unknown };
    if (parsed.version !== VERSION) return null;
    if (parsed.value === null || parsed.value === undefined) return null;
    if (accept && !accept(parsed.value)) return null;
    return {
      value: parsed.value as T,
      savedAt: typeof parsed.saved_at === 'number' ? parsed.saved_at : 0,
    };
  } catch {
    return null;
  }
}

/**
 * Write a draft and return when it was saved. `null`/`undefined` clears the key
 * instead of storing a tombstone, so a reset form does not restore as filled.
 */
export function writeDraft<T>(key: string, value: T): number | null {
  const store = storage();
  if (!store) return null;
  if (value === null || value === undefined) {
    clearDraft(key);
    return null;
  }
  const savedAt = Date.now();
  try {
    store.setItem(key, JSON.stringify({ version: VERSION, saved_at: savedAt, value }));
    return savedAt;
  } catch {
    // Quota or a locked store: the form keeps working, it just cannot promise
    // the draft. Returning null is what the UI shows as "not saved".
    return null;
  }
}

export function clearDraft(key: string): void {
  const store = storage();
  if (!store) return;
  try {
    store.removeItem(key);
  } catch {
    // Nothing useful to do; the next write will try again.
  }
}

function newId(prefix: string): string {
  const maybeCrypto = globalThis.crypto as { randomUUID?: () => string } | undefined;
  if (maybeCrypto?.randomUUID) return `${prefix}-${maybeCrypto.randomUUID()}`;
  return `${prefix}-${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

/**
 * An idempotency key that survives a reload. The same key on the retry means the
 * API stores one submission, not two: without this, losing the response after a
 * successful send looks like a failed send to the student.
 */
export function stableClientKey(storageKey: string, prefix = 'web'): string {
  const existing = readDraft<string>(storageKey, (value) => typeof value === 'string' && value.length > 0);
  if (existing) return existing.value;
  const key = newId(prefix);
  writeDraft(storageKey, key);
  return key;
}

export interface DraftControl<T> {
  value: T;
  setValue: (next: T | ((current: T) => T)) => void;
  /** When the draft was last written, or null if storage refused it. */
  savedAt: number | null;
  /** Clear the draft and go back to the initial value. */
  clear: () => void;
}

/**
 * React binding for one draft. The key changes when the route parameter does
 * (React Router reuses the element), so state is re-derived on a key change
 * during render rather than in an effect — no flash of the previous task's
 * answer.
 */
export function useDraft<T>(
  key: string,
  initial: T,
  accept?: (value: unknown) => boolean,
): DraftControl<T> {
  const options = React.useRef({ initial, accept });
  options.current = { initial, accept };

  const restore = React.useCallback(
    (nextKey: string): { key: string; value: T; savedAt: number | null } => {
      const draft = readDraft<T>(nextKey, options.current.accept);
      return { key: nextKey, value: draft ? draft.value : options.current.initial, savedAt: draft?.savedAt ?? null };
    },
    [],
  );

  const [state, setState] = React.useState(() => restore(key));
  if (state.key !== key) {
    setState(restore(key));
  }

  const writtenKey = React.useRef<string | null>(null);
  React.useEffect(() => {
    if (writtenKey.current !== key) {
      // Mount, or a key change that restored a draft: writing it straight back
      // would make an old answer look newly saved.
      writtenKey.current = key;
      return;
    }
    setState((current) => ({ ...current, savedAt: writeDraft(key, current.value) }));
  }, [key, state.value]);

  const setValue = React.useCallback((next: T | ((current: T) => T)) => {
    setState((current) => ({
      ...current,
      value:
        typeof next === 'function' ? (next as (value: T) => T)(current.value) : next,
    }));
  }, []);

  const clear = React.useCallback(() => {
    clearDraft(key);
    setState({ key, value: options.current.initial, savedAt: null });
  }, [key]);

  return { value: state.value, setValue, savedAt: state.savedAt, clear };
}
