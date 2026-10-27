import { Mail, ShieldCheck } from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

const SUPPORT_EMAIL = 'support@nelavista.com';

export function Contact(): JSX.Element {
  return (
    <section className="nv-container nv-section">
      <div className="nv-contact-grid">
        <div className="nv-stack">
          <p className="nv-eyebrow">Contact</p>
          <h1 className="nv-display" style={{ fontSize: 'clamp(2.6rem, 6vw, 4.8rem)' }}>
            Tell us what is not working.
          </h1>
          <p className="nv-lede">
            For account, verification, work or payout questions, email the support inbox. Include the email on
            your account and the reference from the screen you were on.
          </p>
          <a className="nv-button" href={`mailto:${SUPPORT_EMAIL}`} style={{ alignSelf: 'flex-start' }}>
            <Mail aria-hidden="true" size={16} />
            {SUPPORT_EMAIL}
          </a>
          <p className="nv-muted" style={{ maxWidth: '52ch' }}>
            Do not send your password, a one-time code or full bank details. We will never ask for them by
            email.
          </p>
        </div>

        <div className="nv-contact-card nv-stack">
          <ShieldCheck aria-hidden="true" size={22} strokeWidth={1.6} />
          <h2>Before you write</h2>
          <ul className="nv-list">
            <li>
              <strong>Account:</strong> the email you signed up with.
            </li>
            <li>
              <strong>Verification:</strong> the skill or assessment name and the date.
            </li>
            <li>
              <strong>Work:</strong> the opportunity or assignment reference.
            </li>
            <li>
              <strong>Money:</strong> the payout or line-item reference, never a full card number.
            </li>
          </ul>
          <div className="nv-divider" />
          <p className="nv-muted" style={{ fontSize: 'var(--nv-text-sm)' }}>
            If you are a student with an account, the fastest route is the support link in the app footer.
          </p>
          <Link className="nv-link-arrow" to="/faq">
            Read the FAQ first
          </Link>
        </div>
      </div>
    </section>
  );
}
