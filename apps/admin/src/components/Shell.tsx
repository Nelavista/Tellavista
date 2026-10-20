import * as React from 'react';

import { useSession } from '../lib/session';

const LINKS: Array<{ path: string; label: string }> = [
  { path: '/audit', label: 'Audit trail' },
  { path: '/imports', label: 'Import runs' },
  { path: '/users', label: 'Users' },
  { path: '/opportunities', label: 'Opportunities' },
  { path: '/work', label: 'Projects & cohorts' },
  { path: '/review', label: 'Review queue' },
  { path: '/money', label: 'Money' },
  { path: '/content', label: 'Content' },
  { path: '/security', label: 'Security' },
];

export function Shell({
  route,
  go,
  children,
}: {
  route: string;
  go: (next: string) => void;
  children: React.ReactNode;
}): JSX.Element {
  const { me, logout } = useSession();

  async function signOut(): Promise<void> {
    await logout();
    go('/login');
  }

  return (
    <div className="nv-shell">
      <aside className="nv-side">
        <div>
          <div className="nv-brand">Nelavista ops</div>
          <p className="nv-muted" style={{ margin: '6px 0 0' }}>
            {me?.name ?? me?.username} · {me?.role ?? 'no role'}
          </p>
        </div>
        <nav className="nv-nav" aria-label="Admin sections">
          {LINKS.map((link) => (
            <a
              data-active={route === link.path || route.startsWith(`${link.path}/`)}
              href={`#${link.path}`}
              key={link.path}
              onClick={(event) => {
                event.preventDefault();
                go(link.path);
              }}
            >
              {link.label}
            </a>
          ))}
        </nav>
        <button className="nv-button nv-button--ghost" type="button" onClick={() => void signOut()}>
          Sign out
        </button>
      </aside>
      <main className="nv-main">{children}</main>
    </div>
  );
}
