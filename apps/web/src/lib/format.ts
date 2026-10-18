/**
 * Card-safe display of API values.
 *
 * Dates come back as ISO strings (the API is UTC) and answers as arbitrary JSON.
 * Both are rendered as text, never as HTML, and an empty value says so rather
 * than printing `undefined`.
 */

export function formatDateTime(value: string | null | undefined): string {
  if (!value) return '';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '';
  return date.toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' });
}

/** A submitted or expected answer, as one readable line. */
export function formatAnswer(value: unknown): string {
  if (value === null || value === undefined) return 'No answer';
  if (typeof value === 'string') return value.length > 0 ? value : 'No answer';
  if (typeof value === 'number' || typeof value === 'boolean') return String(value);
  if (Array.isArray(value)) {
    const parts = value.map((item) => formatAnswer(item)).filter((item) => item !== 'No answer');
    return parts.length > 0 ? parts.join(', ') : 'No answer';
  }
  const record = value as Record<string, unknown>;
  const keys = Object.keys(record);
  if (keys.length === 1 && keys[0] !== undefined) {
    const only = record[keys[0]];
    if (typeof only === 'string' || typeof only === 'number') return String(only);
  }
  return JSON.stringify(value);
}
