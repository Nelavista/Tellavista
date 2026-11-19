/**
 * Which platform announcements this browser has already dismissed.
 *
 * Dismissal is per announcement id and per browser, because an announcement is
 * a message ("campus closed Friday") and not a preference: once read, it should
 * stop taking space above the work, but a new one must still arrive. Storing the
 * ids - never a single boolean - is what makes the second part true.
 */
const DISMISSED_KEY = 'nv.announcements.dismissed';
/** Enough ids to cover a year of notices without the key growing without bound. */
const KEEP = 50;

export function readDismissedIds(): number[] {
  try {
    const raw = window.localStorage.getItem(DISMISSED_KEY);
    if (!raw) return [];
    const parsed: unknown = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed.filter((value): value is number => typeof value === 'number');
  } catch {
    // Private mode, a full quota or a hand-edited value: showing the notice
    // again is a far smaller problem than failing to render the shell.
    return [];
  }
}

export function dismissAnnouncement(id: number): number[] {
  const next = [id, ...readDismissedIds().filter((value) => value !== id)].slice(0, KEEP);
  try {
    window.localStorage.setItem(DISMISSED_KEY, JSON.stringify(next));
  } catch {
    // Not persisted; it stays dismissed for this page's lifetime.
  }
  return next;
}

export function clearDismissedAnnouncements(): void {
  try {
    window.localStorage.removeItem(DISMISSED_KEY);
  } catch {
    // Nothing to clear.
  }
}
