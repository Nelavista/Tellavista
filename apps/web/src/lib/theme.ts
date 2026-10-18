import { colors, radius, spacing, typography } from '@nelavista/design-tokens';

/**
 * Publish the design tokens as CSS variables once. Stylesheets reference
 * `var(--nv-*)`, so changing a colour in packages/design-tokens changes every
 * app without touching CSS.
 */
export function applyTheme(): void {
  const root = document.documentElement;
  const vars: Record<string, string> = {
    '--nv-bg': colors.bg,
    '--nv-surface': colors.surface,
    '--nv-border': colors.border,
    '--nv-text': colors.text,
    '--nv-text-muted': colors.textMuted,
    '--nv-accent': colors.accent,
    '--nv-accent-strong': colors.accentStrong,
    '--nv-success': colors.success,
    '--nv-warning': colors.warning,
    '--nv-danger': colors.danger,
    '--nv-font': typography.fontFamily,
    '--nv-text-sm': `${typography.sizes.sm}px`,
    '--nv-text-md': `${typography.sizes.md}px`,
    '--nv-text-lg': `${typography.sizes.lg}px`,
    '--nv-text-xxl': `${typography.sizes.xxl}px`,
  };
  for (const [key, value] of Object.entries(vars)) root.style.setProperty(key, value);

  const spaceVars: Record<string, number> = {
    '--nv-space-xs': spacing.xs,
    '--nv-space-sm': spacing.sm,
    '--nv-space-md': spacing.md,
    '--nv-space-lg': spacing.lg,
    '--nv-space-xl': spacing.xl,
    '--nv-space-xxl': spacing.xxl,
    '--nv-radius-sm': radius.sm,
    '--nv-radius-md': radius.md,
    '--nv-radius-lg': radius.lg,
    '--nv-radius-pill': radius.pill,
  };
  for (const [key, value] of Object.entries(spaceVars)) root.style.setProperty(key, `${value}px`);
}
