/**
 * Minimum-version and force-update handling (D3, ADR-0010).
 *
 * The API answers 426 with `min_version` and `store_url`; the client also checks
 * the published policy at launch so an outdated build says so before a request
 * fails. Comparison is numeric per segment; a prerelease suffix is ignored on
 * purpose, since a tester build should still be able to run.
 */
export function compareVersions(a: string, b: string): number {
  const left = a.split('.').map((part) => Number.parseInt(part, 10) || 0);
  const right = b.split('.').map((part) => Number.parseInt(part, 10) || 0);
  const length = Math.max(left.length, right.length);
  for (let index = 0; index < length; index += 1) {
    const l = left[index] ?? 0;
    const r = right[index] ?? 0;
    if (l !== r) return l < r ? -1 : 1;
  }
  return 0;
}

export function needsUpdate(current: string, minimum: string | null | undefined): boolean {
  if (!minimum) return false;
  return compareVersions(current, minimum) < 0;
}
