import { BrandMark, ThemeToggle } from '@nelavista/ui';
import { MotionConfig } from 'motion/react';
import * as React from 'react';
import { Link, NavLink, useLocation } from 'react-router-dom';

import { usePageMeta } from '../lib/page-meta';
import { useSession } from '../lib/session';
import { useTheme } from '../lib/theme-context';
import { BrandFilm } from './BrandFilm';
import { PageTransition } from './Reveal';
import { SocialLinks } from './SocialLinks';

const NAV = [
  { to: '/features', label: 'Features' },
  { to: '/how-it-works', label: 'How it works' },
  { to: '/pricing', label: 'Pricing' },
  { to: '/about', label: 'About' },
  { to: '/faq', label: 'FAQ' },
];

export function PublicLayout({ children }: { children: React.ReactNode }): JSX.Element {
  usePageMeta();
  const location = useLocation();
  const { status } = useSession();
  const { theme, toggle } = useTheme();
  const signedIn = status === 'authenticated';
  const mainRef = React.useRef<HTMLElement | null>(null);
  const firstRoute = React.useRef(true);

  React.useEffect(() => {
    if (firstRoute.current) {
      firstRoute.current = false;
      return;
    }
    mainRef.current?.focus();
  }, [location.pathname]);

  return (
    <div className="nv-public">
      <a className="nv-skip-link" href="#main">
        Skip to content
      </a>
      <header className="nv-public__header">
        <div className="nv-public__header-inner">
          <Link className="nv-public__brand" to="/" aria-label="Nelavista home">
            <BrandMark />
            <span>Nelavista</span>
          </Link>

          <nav className="nv-public__nav" aria-label="Public">
            {NAV.map((item) => (
              <NavLink key={item.to} to={item.to}>
                {item.label}
              </NavLink>
            ))}
          </nav>

          <div className="nv-public__actions">
            <ThemeToggle theme={theme} onToggle={toggle} />
            {signedIn ? (
              <Link className="nv-button nv-button--sm" to="/home">
                Open app
              </Link>
            ) : (
              <>
                <Link className="nv-button nv-button--ghost nv-button--sm" to="/login">
                  Sign in
                </Link>
                <Link className="nv-button nv-button--sm" to="/signup">
                  Create account
                </Link>
              </>
            )}
          </div>
        </div>

        <nav className="nv-public__mobile-nav" aria-label="Public mobile">
          {NAV.map((item) => (
            <NavLink key={item.to} to={item.to}>
              {item.label}
            </NavLink>
          ))}
        </nav>
      </header>

      <main id="main" ref={mainRef} tabIndex={-1}>
        <MotionConfig reducedMotion="user">
          <PageTransition key={location.pathname}>{children}</PageTransition>
        </MotionConfig>
      </main>

      <BrandFilm />

      <footer className="nv-public__footer">
        <div className="nv-public__footer-inner">
          <div className="nv-footer-grid">
            <div className="nv-footer-col">
              <Link className="nv-public__brand" to="/" aria-label="Nelavista home">
                <BrandMark />
                <span>Nelavista</span>
              </Link>
              <p style={{ maxWidth: '34ch', marginTop: 'var(--nv-space-sm)' }}>
                A working record for Nigerian university students: learn it, prove it, get paid for it.
              </p>
              <SocialLinks />
            </div>
            <div className="nv-footer-col">
              <h2>Product</h2>
              <Link to="/features">Features</Link>
              <Link to="/how-it-works">How it works</Link>
              <Link to="/pricing">Pricing</Link>
              <Link to="/about">About</Link>
            </div>
            <div className="nv-footer-col">
              <h2>Students</h2>
              <Link to="/signup">Create account</Link>
              <Link to="/login">Sign in</Link>
              <Link to="/faq">FAQ</Link>
            </div>
            <div className="nv-footer-col">
              <h2>Legal</h2>
              <Link to="/legal/privacy">Privacy</Link>
              <Link to="/legal/terms">Terms</Link>
              <Link to="/legal/contributor-terms">Contributor terms</Link>
              <Link to="/contact">Contact</Link>
            </div>
          </div>
          <div className="nv-footer-base">
            <span>Nelavista &copy; 2025 - {new Date().getFullYear()} All rights reserved.</span>
            <span>Built for African university students. Nigeria first.</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
