/**
 * Feature flags (build-time, per environment).
 *
 * Anything half-built merges behind a flag so it can reach `develop`/`main`
 * without being visible in prod (brief: "feature flags for anything half-built").
 *
 * A flag is enabled when its env var is set to 1/true/yes/on. Each client reads
 * its own env prefix:
 *   web/admin:  VITE_FLAG_<NAME>
 *   mobile:     EXPO_PUBLIC_FLAG_<NAME>
 *   any:        FLAG_<NAME>
 *
 * Flags are read at BUILD time (per environment), never guessed at runtime.
 */
export interface FlagEnv {
  [key: string]: string | undefined;
}

const TRUTHY = new Set(['1', 'true', 'yes', 'on']);

export function isFlagEnabled(name: string, env: FlagEnv = {}, defaultEnabled = false): boolean {
  const key = name.toUpperCase().replace(/[^A-Z0-9]/g, '_');
  const raw = env[`FLAG_${key}`] ?? env[`VITE_FLAG_${key}`] ?? env[`EXPO_PUBLIC_FLAG_${key}`];
  if (raw === undefined) return defaultEnabled;
  return TRUTHY.has(String(raw).trim().toLowerCase());
}

/** Client-facing flag names. Keep these in sync with the API's flags. */
export const FLAGS = {
  skillsJourney: 'skills_journey',
  managedWorkforce: 'managed_workforce',
  ledger: 'ledger',
} as const;
