import { Avatar, BrandMark, ConfirmDialog } from '@nelavista/ui';
import {
  Briefcase,
  Building2,
  ClipboardCheck,
  FileText,
  FolderKanban,
  LayoutDashboard,
  ListChecks,
  LogOut,
  ScrollText,
  Settings2,
  ShieldCheck,
  Upload,
  UserPlus,
  Users,
  Wallet,
  type LucideIcon,
} from 'lucide-react';
import * as React from 'react';

import { useSession } from '../lib/session';

interface NavItem {
  path: string;
  label: string;
  icon: LucideIcon;
}

const GROUPS: Array<{ label: string; items: NavItem[] }> = [
  {
    label: 'Overview',
    items: [{ path: '/overview', label: 'Operations', icon: LayoutDashboard }],
  },
  {
    label: 'Trust',
    items: [
      { path: '/audit', label: 'Audit trail', icon: ScrollText },
      { path: '/users', label: 'Users', icon: Users },
      { path: '/waitlist', label: 'Waitlist', icon: UserPlus },
    ],
  },
  {
    label: 'Delivery',
    items: [
      { path: '/opportunities', label: 'Opportunities', icon: Briefcase },
      { path: '/work', label: 'Projects & cohorts', icon: FolderKanban },
      { path: '/review', label: 'Review queue', icon: ClipboardCheck },
      { path: '/money', label: 'Money', icon: Wallet },
    ],
  },
  {
    label: 'Content',
    items: [
      { path: '/content', label: 'Content', icon: FileText },
      { path: '/campus', label: 'Campus', icon: Building2 },
      { path: '/platform', label: 'Platform settings', icon: Settings2 },
      { path: '/security', label: 'Security', icon: ShieldCheck },
    ],
  },
  {
    label: 'Data',
    items: [{ path: '/imports', label: 'Import runs', icon: Upload }],
  },
];

const TITLES: Array<[string, string]> = [
  ['/overview', 'Operations'],
  ['/audit', 'Audit trail'],
  ['/users', 'Users'],
  ['/waitlist', 'Waitlist'],
  ['/opportunities', 'Opportunities'],
  ['/work', 'Projects & cohorts'],
  ['/review', 'Review queue'],
  ['/money', 'Money'],
  ['/content', 'Content'],
  ['/campus', 'Campus'],
  ['/platform', 'Platform settings'],
  ['/security', 'Security'],
  ['/imports', 'Import runs'],
];

function titleFor(route: string): string {
  const match = TITLES.find(([prefix]) => route === prefix || route.startsWith(`${prefix}/`));
  return match?.[1] ?? 'Not found';
}

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
  const [busy, setBusy] = React.useState(false);
  const [confirmSignOut, setConfirmSignOut] = React.useState(false);
  const mainRef = React.useRef<HTMLElement | null>(null);
  const firstRoute = React.useRef(true);

  React.useEffect(() => {
    document.title = `${titleFor(route)} · Nelavista ops`;
    window.scrollTo(0, 0);
    if (firstRoute.current) {
      firstRoute.current = false;
      return;
    }
    mainRef.current?.focus();
  }, [route]);

  async function signOut(): Promise<void> {
    setBusy(true);
    try {
      await logout();
      setConfirmSignOut(false);
      go('/login');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="nv-shell">
      <a className="nv-skip-link" href="#main">
        Skip to content
      </a>
      <aside className="nv-sidebar" aria-label="Admin sections">
        <div className="nv-sidebar__brand">
          <BrandMark />
        </div>

        <nav className="nv-sidebar__nav">
          {GROUPS.map((group) => (
            <React.Fragment key={group.label}>
              <p className="nv-sidebar__group">{group.label}</p>
              {group.items.map((item) => {
                const Icon = item.icon;
                const active = route === item.path || route.startsWith(`${item.path}/`);
                return (
                  <a
                    aria-current={active ? 'page' : undefined}
                    className="nv-sidebar__link"
                    href={`#${item.path}`}
                    key={item.path}
                    onClick={(event) => {
                      event.preventDefault();
                      go(item.path);
                    }}
                  >
                    <Icon aria-hidden="true" size={16} strokeWidth={1.7} />
                    <span>{item.label}</span>
                  </a>
                );
              })}
            </React.Fragment>
          ))}
        </nav>

        <div className="nv-sidebar__footer">
          <div className="nv-row" style={{ marginBottom: 'var(--nv-space-md)' }}>
            <Avatar name={me?.name ?? me?.username ?? 'Ops'} />
            <div style={{ minWidth: 0 }}>
              <p
                className="nv-h4"
                style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}
              >
                {me?.name ?? me?.username}
              </p>
              <p className="nv-meta">{me?.role ?? 'no role'}</p>
            </div>
          </div>
          <button
            className="nv-button nv-button--ghost nv-button--block nv-button--sm"
            disabled={busy}
            type="button"
            onClick={() => setConfirmSignOut(true)}
          >
            <LogOut aria-hidden="true" size={15} />
            Sign out
          </button>
        </div>
      </aside>

      <div className="nv-shell__main">
        <header className="nv-topbar">
          <div className="nv-topbar__left">
            <span className="nv-meta">Operations</span>
            <span aria-hidden="true" className="nv-subtle">
              /
            </span>
            <span className="nv-topbar__title">{titleFor(route)}</span>
          </div>
          <div className="nv-topbar__actions">
            <a
              className="nv-button nv-button--ghost nv-button--sm"
              href="#/audit"
              onClick={(event) => {
                event.preventDefault();
                go('/audit');
              }}
            >
              <ListChecks aria-hidden="true" size={15} />
              Audit
            </a>
          </div>
        </header>
        <main className="nv-main" id="main" ref={mainRef} tabIndex={-1}>
          {children}
        </main>
      </div>

      <ConfirmDialog
        body={
          <p>
            You will need your password and authenticator code to reopen the ops workspace. No audit record is
            changed by signing out.
          </p>
        }
        busy={busy}
        busyLabel="Signing out"
        confirmLabel="Sign out"
        onCancel={() => setConfirmSignOut(false)}
        onConfirm={() => void signOut()}
        open={confirmSignOut}
        title="Are you sure you want to sign out?"
      />
    </div>
  );
}
