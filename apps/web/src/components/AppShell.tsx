import { Avatar, BrandMark, ThemeToggle } from '@nelavista/ui';
import {
  BadgeCheck,
  Bell,
  BookOpen,
  Briefcase,
  ClipboardCheck,
  FileText,
  GraduationCap,
  LayoutDashboard,
  LogOut,
  MapPin,
  Settings,
  Sparkles,
  Wallet,
  type LucideIcon,
} from 'lucide-react';
import { MotionConfig, motion } from 'motion/react';
import * as React from 'react';
import { Link, NavLink, useLocation, useNavigate } from 'react-router-dom';

import { useSession } from '../lib/session';
import { useTheme } from '../lib/theme-context';

interface NavItem {
  to: string;
  label: string;
  icon: LucideIcon;
}

const GROUPS: Array<{ label: string; items: NavItem[] }> = [
  {
    label: 'Overview',
    items: [{ to: '/home', label: 'Home', icon: LayoutDashboard }],
  },
  {
    label: 'Learn',
    items: [
      { to: '/academia', label: 'Academia', icon: GraduationCap },
      { to: '/academia/materials', label: 'Materials', icon: BookOpen },
      { to: '/academia/ask', label: 'Ask Nelavista', icon: Sparkles },
      { to: '/academia/cbt', label: 'CBT practice', icon: ClipboardCheck },
      { to: '/campus', label: 'Campus', icon: MapPin },
    ],
  },
  {
    label: 'Prove',
    items: [
      { to: '/skills', label: 'Skills', icon: Sparkles },
      { to: '/skills/my-learning', label: 'My learning', icon: BookOpen },
      { to: '/verification', label: 'Verification', icon: BadgeCheck },
      { to: '/transcript', label: 'Transcript', icon: FileText },
      { to: '/talent', label: 'Talent profile', icon: FileText },
    ],
  },
  {
    label: 'Work',
    items: [
      { to: '/opportunities', label: 'Opportunities', icon: Briefcase },
      { to: '/work', label: 'My work', icon: ClipboardCheck },
      { to: '/earnings', label: 'Earnings', icon: Wallet },
    ],
  },
  {
    label: 'Account',
    items: [
      { to: '/notifications', label: 'Notifications', icon: Bell },
      { to: '/settings', label: 'Settings', icon: Settings },
    ],
  },
];

const MOBILE: NavItem[] = [
  { to: '/home', label: 'Home', icon: LayoutDashboard },
  { to: '/academia', label: 'Academia', icon: GraduationCap },
  { to: '/skills', label: 'Skills', icon: Sparkles },
  { to: '/opportunities', label: 'Work', icon: Briefcase },
  { to: '/earnings', label: 'Earnings', icon: Wallet },
  { to: '/settings', label: 'Settings', icon: Settings },
];

const TITLES: Array<[string, string]> = [
  ['/home', 'Overview'],
  ['/academia/materials', 'Materials'],
  ['/academia/ask', 'Ask Nelavista'],
  ['/academia/cbt/history', 'CBT history'],
  ['/academia/cbt', 'CBT practice'],
  ['/academia/courses', 'Course'],
  ['/academia', 'Academia'],
  ['/campus', 'Campus'],
  ['/skills/my-learning', 'My learning'],
  ['/skills/paths', 'Skill path'],
  ['/skills/lessons', 'Lesson'],
  ['/skills/practice', 'Practice'],
  ['/skills', 'Skills'],
  ['/verification/assessments', 'Assessment'],
  ['/verification/attempts', 'Attempt review'],
  ['/verification/practical', 'Practical task'],
  ['/verification', 'Verification'],
  ['/transcript', 'Transcript'],
  ['/opportunities/applications', 'My applications'],
  ['/opportunities', 'Opportunities'],
  ['/work', 'My work'],
  ['/earnings', 'Earnings'],
  ['/notifications', 'Notifications'],
  ['/settings/security', 'Security'],
  ['/settings/notifications', 'Notifications'],
  ['/settings/data', 'Your data'],
  ['/settings', 'Settings'],
  ['/talent', 'Talent profile'],
  ['/onboarding', 'Set up your account'],
];

function titleFor(pathname: string): string {
  const match = TITLES.find(([prefix]) => pathname === prefix || pathname.startsWith(`${prefix}/`));
  return match?.[1] ?? 'Nelavista';
}

export function PageTransition({ children }: { children: React.ReactNode }): JSX.Element {
  const location = useLocation();
  return (
    <MotionConfig reducedMotion="user">
      <motion.div
        key={location.pathname}
        initial={{ opacity: 0, y: 5 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.2, ease: [0.22, 1, 0.36, 1] }}
      >
        {children}
      </motion.div>
    </MotionConfig>
  );
}

export function AppShell({ children }: { children: React.ReactNode }): JSX.Element {
  const { me, profile, logout } = useSession();
  const { theme, toggle } = useTheme();
  const location = useLocation();
  const navigate = useNavigate();
  const [busy, setBusy] = React.useState(false);
  const mainRef = React.useRef<HTMLElement | null>(null);
  const firstRoute = React.useRef(true);

  const name = profile?.display_name ?? me?.name ?? me?.username ?? 'Student';
  const role = me?.role === 'super_admin' ? 'Admin' : me?.role === 'employer' ? 'Employer' : 'Student';

  React.useEffect(() => {
    document.title = `${titleFor(location.pathname)} · Nelavista`;
    if (firstRoute.current) {
      firstRoute.current = false;
      return;
    }
    mainRef.current?.focus();
  }, [location.pathname]);

  async function onSignOut(): Promise<void> {
    setBusy(true);
    try {
      await logout();
      navigate('/', { replace: true });
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="nv-shell">
      <a className="nv-skip-link" href="#main">
        Skip to content
      </a>

      <aside className="nv-sidebar" aria-label="Primary">
        <Link className="nv-sidebar__brand" to="/home" aria-label="Nelavista home">
          <BrandMark />
          <span>Nelavista</span>
        </Link>

        <nav className="nv-sidebar__nav">
          {GROUPS.map((group) => (
            <React.Fragment key={group.label}>
              <p className="nv-sidebar__group">{group.label}</p>
              {group.items.map((item) => {
                const Icon = item.icon;
                return (
                  <NavLink className="nv-sidebar__link" key={item.to} to={item.to}>
                    <Icon aria-hidden="true" size={16} strokeWidth={1.7} />
                    <span>{item.label}</span>
                  </NavLink>
                );
              })}
            </React.Fragment>
          ))}
        </nav>

        <div className="nv-sidebar__footer">
          <div className="nv-row" style={{ marginBottom: 'var(--nv-space-md)' }}>
            <Avatar name={name} />
            <div style={{ minWidth: 0 }}>
              <p
                className="nv-h4"
                style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}
              >
                {name}
              </p>
              <p className="nv-meta">{role}</p>
            </div>
          </div>
          <button
            className="nv-button nv-button--ghost nv-button--block nv-button--sm"
            type="button"
            disabled={busy}
            onClick={() => void onSignOut()}
          >
            <LogOut aria-hidden="true" size={15} />
            {busy ? 'Signing out' : 'Sign out'}
          </button>
        </div>
      </aside>

      <div className="nv-shell__main">
        <div className="nv-mobile-bar">
          <Link className="nv-sidebar__brand" to="/home" aria-label="Nelavista home">
            <BrandMark />
            <span>Nelavista</span>
          </Link>
          <div className="nv-row" style={{ gap: 'var(--nv-space-xs)' }}>
            <ThemeToggle theme={theme} onToggle={toggle} />
            <Link className="nv-icon-button" to="/notifications" aria-label="Notifications">
              <Bell aria-hidden="true" size={17} />
            </Link>
            <Link className="nv-avatar" to="/settings" aria-label="Account settings">
              {name.slice(0, 1).toUpperCase()}
            </Link>
          </div>
        </div>

        <header className="nv-topbar">
          <div className="nv-topbar__left">
            <span className="nv-meta">Student workspace</span>
            <span aria-hidden="true" className="nv-subtle">
              /
            </span>
            <span className="nv-topbar__title">{titleFor(location.pathname)}</span>
          </div>
          <div className="nv-topbar__actions">
            <ThemeToggle theme={theme} onToggle={toggle} />
            <Link className="nv-icon-button" to="/notifications" aria-label="Notifications">
              <Bell aria-hidden="true" size={17} />
            </Link>
            <Link className="nv-icon-button" to="/settings" aria-label="Account settings">
              <Avatar name={name} />
            </Link>
          </div>
        </header>

        <nav className="nv-mobile-nav" aria-label="Student mobile">
          {MOBILE.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink key={item.to} to={item.to}>
                <Icon aria-hidden="true" size={14} strokeWidth={1.7} />
                {item.label}
              </NavLink>
            );
          })}
        </nav>

        <main className="nv-content" id="main" ref={mainRef} tabIndex={-1}>
          <div className="nv-content__inner">
            <PageTransition>{children}</PageTransition>
          </div>
        </main>
      </div>
    </div>
  );
}
