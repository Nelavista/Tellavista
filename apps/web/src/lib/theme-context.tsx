import * as React from 'react';
import { useLocation } from 'react-router-dom';

import {
  applyInitialTheme,
  applyTheme,
  getStoredTheme,
  isPublicPath,
  resolveTheme,
  setStoredTheme,
  type ThemeName,
} from './theme';

interface ThemeContextValue {
  theme: ThemeName;
  setTheme: (theme: ThemeName) => void;
  toggle: () => void;
}

const ThemeContext = React.createContext<ThemeContextValue | null>(null);

export function ThemeProvider({ children }: { children: React.ReactNode }): JSX.Element {
  const location = useLocation();
  const [theme, setThemeState] = React.useState<ThemeName>(() => applyInitialTheme(window.location.pathname));

  React.useEffect(() => {
    // A saved choice always wins. Without one, public pages read on Paper and the
    // signed-in app stays on Ink, so the surface matches the job.
    if (getStoredTheme()) return;
    const next: ThemeName = isPublicPath(location.pathname) ? 'paper' : 'ink';
    if (next !== theme) {
      applyTheme(next);
      setThemeState(next);
    }
  }, [location.pathname, theme]);

  const setTheme = React.useCallback((next: ThemeName) => {
    setStoredTheme(next);
    applyTheme(next);
    setThemeState(next);
  }, []);

  const toggle = React.useCallback(() => {
    setThemeState((current: ThemeName) => {
      const next: ThemeName = current === 'ink' ? 'paper' : 'ink';
      setStoredTheme(next);
      applyTheme(next);
      return next;
    });
  }, []);

  return <ThemeContext.Provider value={{ theme, setTheme, toggle }}>{children}</ThemeContext.Provider>;
}

const FALLBACK: ThemeContextValue = {
  theme: typeof window === 'undefined' ? 'paper' : resolveTheme(window.location.pathname),
  setTheme: () => undefined,
  toggle: () => undefined,
};

export function useTheme(): ThemeContextValue {
  // Route screens are also rendered in isolation by tests and by the shared
  // profile surface. The fallback keeps those renders honest; the real provider
  // is still the only thing that persists a choice.
  return React.useContext(ThemeContext) ?? FALLBACK;
}
