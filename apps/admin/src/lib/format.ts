/** Formatting shared by the ops screens. Amounts are minor units, always. */
export function money(
  amountMinor: number | null | undefined,
  currency: string | null | undefined,
): string {
  if (amountMinor === null || amountMinor === undefined) return '—';
  if (!currency) return String(amountMinor);
  try {
    return new Intl.NumberFormat(undefined, { style: 'currency', currency }).format(amountMinor / 100);
  } catch {
    return `${currency} ${(amountMinor / 100).toFixed(2)}`;
  }
}

export function when(value: string | null | undefined): string {
  if (!value) return '—';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '—';
  return date.toLocaleString();
}

export function shortDate(value: string | null | undefined): string {
  if (!value) return '—';
  return value.slice(0, 10);
}
