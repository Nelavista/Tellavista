import { VersionSwitcher } from '@nelavista/ui';
import * as React from 'react';

const API_VERSION = import.meta.env.VITE_API_VERSION ?? 'v1';

/**
 * Internal ops tools (run managed projects, quality review, audit) live here.
 * Separate from apps/web: a different audience and risk profile (ADR-0001).
 * Access is role-gated server-side; this shell is a hello-world.
 */
export function App(): JSX.Element {
  const [health, setHealth] = React.useState<string>('…');

  React.useEffect(() => {
    fetch(`/api/${API_VERSION}/health`)
      .then((r) => r.json())
      .then((d) => setHealth(d.status))
      .catch(() => setHealth('unreachable'));
  }, []);

  return (
    <main style={{ fontFamily: 'system-ui, sans-serif', padding: 24 }}>
      <header style={{ display: 'flex', justifyContent: 'space-between' }}>
        <h1 style={{ margin: 0 }}>Nelavista Admin</h1>
        <VersionSwitcher />
      </header>
      <p>Internal ops — skeleton. API: {health}</p>
    </main>
  );
}
