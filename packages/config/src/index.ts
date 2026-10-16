import versions from '../versions.json' with { type: 'json' };

export type ProductVersionStatus = 'current' | 'maintenance' | 'deprecated';
export type Platform = 'ios' | 'android';

export interface ProductVersion {
  id: string;
  label: string;
  url: string;
  status: ProductVersionStatus;
}

export interface MobilePolicy {
  min_supported: string;
  latest: string;
  store_url: string;
}

export interface VersionsFile {
  current: string;
  versions: ProductVersion[];
  api: { current_path_version: string; supported_path_versions: string[] };
  mobile: Record<Platform, MobilePolicy>;
}

export const VERSIONS = versions as VersionsFile;

/** All versions, newest (current) first. */
export function allVersions(): ProductVersion[] {
  return [...VERSIONS.versions].sort((a, b) => (a.status === 'current' ? -1 : b.status === 'current' ? 1 : 0));
}

export function currentVersion(): ProductVersion {
  const found = VERSIONS.versions.find((v) => v.id === VERSIONS.current);
  if (!found) throw new Error(`versions.json: current="${VERSIONS.current}" has no matching entry`);
  return found;
}

export function mobilePolicy(platform: Platform): MobilePolicy {
  return VERSIONS.mobile[platform];
}

/** Compare two semver-ish strings ("2.10.1" > "2.9.0"). Returns -1|0|1. */
export function compareVersions(a: string, b: string): number {
  const pa = a.split('.').map((n) => parseInt(n, 10) || 0);
  const pb = b.split('.').map((n) => parseInt(n, 10) || 0);
  for (let i = 0; i < Math.max(pa.length, pb.length); i++) {
    const d = (pa[i] ?? 0) - (pb[i] ?? 0);
    if (d !== 0) return d > 0 ? 1 : -1;
  }
  return 0;
}
