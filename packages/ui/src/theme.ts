import {
  breakpoints,
  dark,
  fonts,
  layout,
  light,
  motion,
  radius,
  spacing,
  typography,
  zIndex,
  type ThemeName,
} from '@nelavista/design-tokens';

export type { ThemeName } from '@nelavista/design-tokens';

const STORAGE_KEY = 'nv-theme';

const PUBLIC_PREFIXES = [
  '/features',
  '/how-it-works',
  '/about',
  '/contact',
  '/faq',
  '/legal',
  '/login',
  '/signup',
  '/auth',
  '/share',
  '/offline',
];

export function isPublicPath(pathname: string): boolean {
  if (pathname === '/') return true;
  return PUBLIC_PREFIXES.some((prefix) => pathname === prefix || pathname.startsWith(`${prefix}/`));
}

export function isThemeName(value: string | null): value is ThemeName {
  return value === 'light' || value === 'dark';
}

export function getStoredTheme(): ThemeName | null {
  try {
    const value = window.localStorage.getItem(STORAGE_KEY);
    return isThemeName(value) ? value : null;
  } catch {
    return null;
  }
}

export function setStoredTheme(theme: ThemeName): void {
  try {
    window.localStorage.setItem(STORAGE_KEY, theme);
  } catch {
    // Storage can be unavailable in private mode. The active theme still works.
  }
}

export function resolveTheme(pathname: string): ThemeName {
  return getStoredTheme() ?? (isPublicPath(pathname) ? 'light' : 'dark');
}

/**
 * Publish one theme as CSS variables on the document root. The stylesheet reads
 * these names; the token file remains the only place where values live.
 */
export function applyTheme(theme: ThemeName): void {
  const root = document.documentElement;
  const t = theme === 'light' ? light : dark;
  const vars: Record<string, string> = {
    '--nv-bg': t.bg,
    '--nv-surface': t.surface,
    '--nv-surface-raised': t.surfaceRaised,
    '--nv-surface-sunken': t.surfaceSunken,
    '--nv-border': t.border,
    '--nv-border-strong': t.borderStrong,
    '--nv-text': t.text,
    '--nv-text-muted': t.textMuted,
    '--nv-text-subtle': t.textSubtle,
    '--nv-accent': t.accent,
    '--nv-accent-strong': t.accentStrong,
    '--nv-accent-subtle': t.accentSubtle,
    '--nv-accent-contrast': t.accentContrast,
    '--nv-success': t.success,
    '--nv-warning': t.warning,
    '--nv-danger': t.danger,
    '--nv-info': t.info,
    '--nv-focus-ring': t.focusRing,
    '--nv-font': fonts.sans,
    '--nv-font-serif': fonts.serif,
    '--nv-font-mono': fonts.mono,
    '--nv-text-xs': `${typography.sizes.xs}px`,
    '--nv-text-sm': `${typography.sizes.sm}px`,
    '--nv-text-md': `${typography.sizes.md}px`,
    '--nv-text-lg': `${typography.sizes.lg}px`,
    '--nv-text-xl': `${typography.sizes.xl}px`,
    '--nv-text-xxl': `${typography.sizes.xxl}px`,
    '--nv-text-display': `${typography.sizes.display}px`,
    '--nv-text-display-lg': `${typography.sizes.displayLg}px`,
    '--nv-leading-tight': `${typography.lineHeights.tight}`,
    '--nv-leading-heading': `${typography.lineHeights.heading}`,
    '--nv-leading-body': `${typography.lineHeights.body}`,
    '--nv-leading-ui': `${typography.lineHeights.ui}`,
    '--nv-tracking-tight': typography.tracking.tight,
    '--nv-tracking-wide': typography.tracking.wide,
    '--nv-tracking-wider': typography.tracking.wider,
    '--nv-space-none': `${spacing.none}px`,
    '--nv-space-xs': `${spacing.xs}px`,
    '--nv-space-sm': `${spacing.sm}px`,
    '--nv-space-md': `${spacing.md}px`,
    '--nv-space-lg': `${spacing.lg}px`,
    '--nv-space-xl': `${spacing.xl}px`,
    '--nv-space-xxl': `${spacing.xxl}px`,
    '--nv-space-3xl': `${spacing['3xl']}px`,
    '--nv-space-4xl': `${spacing['4xl']}px`,
    '--nv-space-5xl': `${spacing['5xl']}px`,
    '--nv-space-6xl': `${spacing['6xl']}px`,
    '--nv-space-7xl': `${spacing['7xl']}px`,
    '--nv-space-8xl': `${spacing['8xl']}px`,
    '--nv-radius-xs': `${radius.xs}px`,
    '--nv-radius-sm': `${radius.sm}px`,
    '--nv-radius-md': `${radius.md}px`,
    '--nv-radius-lg': `${radius.lg}px`,
    '--nv-radius-xl': `${radius.xl}px`,
    '--nv-radius-pill': `${radius.pill}px`,
    '--nv-duration-instant': `${motion.duration.instant}ms`,
    '--nv-duration-fast': `${motion.duration.fast}ms`,
    '--nv-duration-base': `${motion.duration.base}ms`,
    '--nv-duration-slow': `${motion.duration.slow}ms`,
    '--nv-ease-out': motion.easeOut,
    '--nv-ease-in': motion.easeIn,
    '--nv-ease-standard': motion.standard,
    '--nv-reading': `${layout.reading}px`,
    '--nv-app': `${layout.app}px`,
    '--nv-admin': `${layout.admin}px`,
    '--nv-auth': `${layout.auth}px`,
    '--nv-touch': `${layout.touchMin}px`,
    '--nv-z-nav': `${zIndex.nav}`,
    '--nv-z-dropdown': `${zIndex.dropdown}`,
    '--nv-z-overlay': `${zIndex.overlay}`,
    '--nv-z-dialog': `${zIndex.dialog}`,
    '--nv-z-toast': `${zIndex.toast}`,
    '--nv-bp-sm': `${breakpoints.sm}px`,
    '--nv-bp-md': `${breakpoints.md}px`,
    '--nv-bp-lg': `${breakpoints.lg}px`,
    '--nv-bp-xl': `${breakpoints.xl}px`,
    '--nv-bp-2xl': `${breakpoints['2xl']}px`,
  };
  for (const [key, value] of Object.entries(vars)) root.style.setProperty(key, value);
  root.dataset.theme = theme;
  root.style.colorScheme = t.colorScheme;
}

export function applyInitialTheme(pathname: string): ThemeName {
  const theme = resolveTheme(pathname);
  applyTheme(theme);
  return theme;
}

export function toggleTheme(theme: ThemeName): ThemeName {
  const next: ThemeName = theme === 'light' ? 'dark' : 'light';
  setStoredTheme(next);
  applyTheme(next);
  return next;
}
