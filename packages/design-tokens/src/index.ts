/**
 * Nelavista design tokens.
 *
 * One system, two surfaces:
 * - Ink: the signed-in app, admin and dense operational screens.
 * - Paper: public, legal, reading and the shared proof page.
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

export const ink = {
  name: 'ink',
  colorScheme: 'dark',
  bg: '#101114',
  surface: '#17191D',
  surfaceRaised: '#1E2126',
  surfaceSunken: '#0B0C0E',
  border: '#2A2E35',
  borderStrong: '#41464F',
  text: '#E8E6E0',
  textMuted: '#A8A49A',
  textSubtle: '#76736B',
  accent: '#FF5A1F',
  accentStrong: '#FF7A45',
  accentSubtle: '#3A1C11',
  accentContrast: '#101114',
  success: '#3DD68C',
  warning: '#FFC24B',
  danger: '#FF6B5E',
  info: '#7CC7FF',
  focusRing: '#FF8A5C',
} as const;

export const paper = {
  name: 'paper',
  colorScheme: 'light',
  bg: '#FBF8F0',
  surface: '#FFFDF8',
  surfaceRaised: '#F2EDE2',
  surfaceSunken: '#F4EFE4',
  border: '#D8D0C2',
  borderStrong: '#B9AF9E',
  text: '#191A1D',
  textMuted: '#5F5B53',
  textSubtle: '#8A8478',
  accent: '#D9480F',
  accentStrong: '#B93A08',
  accentSubtle: '#FBE3D6',
  accentContrast: '#FFFDF8',
  success: '#1F7A4D',
  warning: '#9A6400',
  danger: '#B42318',
  info: '#1D5F8A',
  focusRing: '#D9480F',
} as const;

export const themes = { ink, paper } as const;
export type ThemeName = keyof typeof themes;

/** Backwards-compatible default. The web bridge publishes the active theme. */
export const colors = ink;

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
