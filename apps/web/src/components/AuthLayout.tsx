import { BrandMark, ThemeToggle } from '@nelavista/ui';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { usePageMeta } from '../lib/page-meta';
import { useTheme } from '../lib/theme-context';
import { EditorialImage } from './EditorialImage';

export function AuthLayout({
  title,
  description,
  children,
  footer,
}: {
  title: string;
  description?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}): JSX.Element {
  usePageMeta();
  const { theme, toggle } = useTheme();

  return (
    <div className="nv-auth">
      <a className="nv-skip-link" href="#main">
        Skip to content
      </a>
      <section className="nv-auth__panel">
        <div className="nv-auth__form">
          <div className="nv-row nv-row--between">
            <Link className="nv-auth__brand" to="/" aria-label="Nelavista home">
              <BrandMark />
              <span>Nelavista</span>
            </Link>
            <ThemeToggle theme={theme} onToggle={toggle} />
          </div>
          <div className="nv-stack nv-stack--tight">
            <h1 className="nv-h1">{title}</h1>
            {description ? <p className="nv-muted">{description}</p> : null}
          </div>
          <main id="main" tabIndex={-1} className="nv-stack">
            {children}
          </main>
          {footer ? <div className="nv-auth__footer">{footer}</div> : null}
        </div>
      </section>

      <aside className="nv-auth__aside" aria-label="Why Nelavista">
        <div className="nv-stack nv-stack--loose">
          <p className="nv-eyebrow">The working record</p>
          <p className="nv-auth__quote">Learn it. Prove it. Get paid for it.</p>
          <p className="nv-muted" style={{ maxWidth: '34ch' }}>
            One account for your courses, verified skills, paid work and the evidence an employer can actually
            check.
          </p>
          <EditorialImage
            alt="A person arranging printed records into a folder on a desk."
            className="nv-auth__figure"
            name="auth-record"
          />
        </div>
        <div className="nv-auth__meta">
          <span>Academia + Skills</span>
          <span>Verified evidence, not a self-reported CV</span>
          <span>Built for a phone, a slow connection and a real deadline</span>
        </div>
      </aside>
    </div>
  );
}
