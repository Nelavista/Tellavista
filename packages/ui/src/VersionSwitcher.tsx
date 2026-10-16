import { allVersions, currentVersion } from '@nelavista/config';
import * as React from 'react';

/**
 * Nav dropdown listing product versions, driven entirely by
 * packages/config/versions.json. Adding a future version is a single edit there.
 */
export function VersionSwitcher({ label = 'Version' }: { label?: string }): JSX.Element {
  const current = currentVersion();
  const versions = allVersions();

  function onChange(e: React.ChangeEvent<HTMLSelectElement>) {
    const target = versions.find((v) => v.id === e.target.value);
    if (target && target.id !== current.id) {
      // Full navigation: each version is its own app on its own subdomain.
      window.location.href = target.url;
    }
  }

  return (
    <label style={{ display: 'inline-flex', gap: 6, alignItems: 'center', fontSize: 13 }}>
      <span style={{ opacity: 0.7 }}>{label}</span>
      <select value={current.id} onChange={onChange} aria-label="Select product version">
        {versions.map((v) => (
          <option key={v.id} value={v.id}>
            {v.label}
            {v.status !== 'current' ? ` (${v.status})` : ''}
          </option>
        ))}
      </select>
    </label>
  );
}
