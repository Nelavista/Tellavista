/**
 * Design tokens. Seeded from V1's palette (audit §2.5) so V2 does not start from
 * a blank canvas. Mobile-first: these are the single source; Tailwind config and
 * React Native styles both read from here.
 */
export const colors = {
  bg: '#050810',
  surface: '#0e1420',
  border: '#1f2a3a',
  text: '#f0f3f8',
  textMuted: '#9fb0c6',
  accent: '#00d1ff',
  accentStrong: '#007bff',
  success: '#22c55e',
  warning: '#f59e0b',
  danger: '#ef4444',
} as const;

export const spacing = { xs: 4, sm: 8, md: 12, lg: 16, xl: 24, xxl: 32 } as const;

export const radius = { sm: 8, md: 12, lg: 20, pill: 999 } as const;

export const typography = {
  fontFamily: 'system-ui, -apple-system, Segoe UI, Roboto, sans-serif',
  sizes: { sm: 13, md: 15, lg: 18, xl: 24, xxl: 32 },
} as const;
