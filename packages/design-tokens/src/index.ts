/**
 * Nelavista design tokens.
 *
 * One system, two surfaces:
 * - Dark: the signed-in app, admin and dense operational screens.
 * - Light: public, legal, reading and the shared proof page.
 *
 * The tokens are deliberately plain values, not a component library. CSS reads
 * them through the web/admin bridge; React Native reads the same source.
 */

export const fonts = {
  serif: "'Instrument Serif', 'Iowan Old Style', 'Palatino Linotype', Georgia, serif",
  sans: "'Instrument Sans', 'Segoe UI', system-ui, -apple-system, sans-serif",
  mono: "'IBM Plex Mono', 'SFMono-Regular', Consolas, 'Liberation Mono', monospace",
} as const;

export const typography = {
  fontFamily: fonts.sans,
  displayFamily: fonts.serif,
  monoFamily: fonts.mono,
  sizes: {
    xs: 12,
    sm: 13,
    md: 15,
    lg: 18,
    xl: 22,
    xxl: 28,
    display: 48,
    displayLg: 64,
  },
  lineHeights: {
    tight: 1.05,
    heading: 1.15,
    body: 1.55,
    ui: 1.35,
  },
  weights: {
    regular: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
  tracking: {
    tight: '-0.02em',
    normal: '0',
    wide: '0.08em',
    wider: '0.14em',
  },
} as const;

export const spacing = {
  none: 0,
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  xxl: 32,
  '3xl': 40,
  '4xl': 48,
  '5xl': 64,
  '6xl': 80,
  '7xl': 96,
  '8xl': 128,
} as const;

export const radius = {
  xs: 2,
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  pill: 999,
} as const;

export const dark = {
  name: 'dark',
  colorScheme: 'dark',
  bg: '#050810',
  surface: '#0A0F1A',
  surfaceRaised: '#0F1825',
  surfaceSunken: '#03060D',
  border: '#1C2A3A',
  borderStrong: '#2B4055',
  text: '#EEF2F7',
  textMuted: '#8FA8C8',
  textSubtle: '#6B84A3',
  accent: '#6E8BFF',
  accentStrong: '#8FA8FF',
  accentSubtle: '#101D3D',
  accentContrast: '#050810',
  success: '#2DD4BF',
  warning: '#F5B942',
  danger: '#FF6B6B',
  info: '#7CC7FF',
  focusRing: '#8FA8FF',
} as const;

export const light = {
  name: 'light',
  colorScheme: 'light',
  bg: '#FFFFFF',
  surface: '#F7F9FC',
  surfaceRaised: '#EEF2F7',
  surfaceSunken: '#FBFCFE',
  border: '#DCE3EC',
  borderStrong: '#B9C6D8',
  text: '#0B1A2F',
  textMuted: '#3F5470',
  textSubtle: '#6B7F99',
  accent: '#1535A8',
  accentStrong: '#0F2A86',
  accentSubtle: '#E8EDFF',
  accentContrast: '#FFFFFF',
  success: '#13805F',
  warning: '#9A6400',
  danger: '#B42318',
  info: '#1D5F9E',
  focusRing: '#1535A8',
} as const;

export const themes = { light, dark } as const;
export type ThemeName = keyof typeof themes;

/** Backwards-compatible default. The web bridge publishes the active theme. */
export const colors = dark;

export const elevation = {
  none: 'none',
  raised: '0 1px 0 rgba(0, 0, 0, 0.04)',
} as const;

export const motion = {
  duration: { instant: 90, fast: 140, base: 200, slow: 280 },
  easeOut: 'cubic-bezier(0.22, 1, 0.36, 1)',
  easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
  standard: 'cubic-bezier(0.2, 0, 0, 1)',
} as const;

export const layout = {
  reading: 680,
  app: 1180,
  admin: 1360,
  auth: 420,
  touchMin: 44,
} as const;

export const breakpoints = {
  sm: 375,
  md: 768,
  lg: 1024,
  xl: 1280,
  '2xl': 1440,
} as const;

export const zIndex = {
  base: 0,
  nav: 20,
  dropdown: 30,
  overlay: 40,
  dialog: 50,
  toast: 60,
} as const;
