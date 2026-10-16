import { VersionSwitcher } from '@nelavista/ui';
import * as React from 'react';

import { apiUrl } from './lib/api';

/**
 * Hello-world shell. Deliberately featureless — V2 features are built in M1+
 * (docs/architecture/06-roadmap.md). What it proves: the workspace packages
 * resolve, the API base URL comes from config, and the version switcher reads
 * packages/config/versions.json.
 */
export function App(): JSX.Element {
  const [health, setHealth] = React.useState<string>('…');

  React.useEffect(() => {
    fetch(apiUrl('/health'))
      .then((r) => r.json())
      .then((d) => setHealth(`${d.status} (${d.api_version}, ${d.app_env})`))
      .catch(() => setHealth('unreachable'));
  }, []);

  return (
    <main style={{ fontFamily: 'system-ui, sans-serif', padding: 24 }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 style={{ margin: 0 }}>Nelavista</h1>
        <VersionSwitcher />
      </header>
      <p>V2 web — skeleton. API: {health}</p>
    </main>
  );
}
