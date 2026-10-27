import * as React from 'react';
import { Link } from 'react-router-dom';

type LegalKind = 'privacy' | 'terms' | 'contributor-terms';

const NAV: Array<{ kind: LegalKind; to: string; label: string }> = [
  { kind: 'privacy', to: '/legal/privacy', label: 'Privacy notice' },
  { kind: 'terms', to: '/legal/terms', label: 'Terms of service' },
  { kind: 'contributor-terms', to: '/legal/contributor-terms', label: 'Contributor terms' },
];

function DraftNotice(): JSX.Element {
  return (
    <div className="nv-legal__note" role="note">
      <strong>Draft for legal review.</strong> This route exists so the consent link in sign-up has a
      destination. It is not the final agreement and it is not legal advice. Replace this page with
      counsel-reviewed copy before public launch.
    </div>
  );
}

function LegalLayout({ kind, children }: { kind: LegalKind; children: React.ReactNode }): JSX.Element {
  return (
    <div className="nv-container nv-legal-layout">
      <nav className="nv-legal-nav" aria-label="Legal documents">
        <p className="nv-meta" style={{ marginBottom: 'var(--nv-space-sm)' }}>
          Legal
        </p>
        {NAV.map((item) => (
          <Link
            key={item.kind}
            to={item.to}
            aria-current={item.kind === kind ? 'page' : undefined}
            style={item.kind === kind ? { color: 'var(--nv-text)' } : undefined}
          >
            {item.label}
          </Link>
        ))}
        <Link to="/contact">Contact</Link>
      </nav>
      <article className="nv-legal">{children}</article>
    </div>
  );
}

export function Privacy(): JSX.Element {
  return (
    <LegalLayout kind="privacy">
      <p className="nv-eyebrow">Privacy notice</p>
      <h1 className="nv-display" style={{ fontSize: 'clamp(2.4rem, 5vw, 4rem)' }}>
        Your data, in plain language.
      </h1>
      <DraftNotice />
      <p>
        The final privacy notice is being prepared with counsel. This page records the data the V2 product
        actually handles so the legal review starts from the code, not a template.
      </p>

      <h2>What the product stores</h2>
      <ul>
        <li>Account details: name, email, username, password hash, roles and session state.</li>
        <li>Profile and preferences: display name, bio, location, time zone, path and visibility.</li>
        <li>Academic context: university, faculty, department, enrolments and semester.</li>
        <li>
          Learning and verification: materials opened, practice attempts, assessment results and evidence.
        </li>
        <li>
          Work and money: applications, work orders, quality decisions, ledger line items and payout status.
        </li>
        <li>Communications: notification records, email delivery events and push-device registrations.</li>
        <li>Consent records: the policy version you accepted and when you accepted it.</li>
      </ul>

      <h2>What is not decided here</h2>
      <p>
        Retention periods, the lawful basis for each processing purpose, international transfer terms, the
        data protection contact and the deletion exceptions need a legal decision. Do not treat this draft as
        a complete notice.
      </p>

      <h2>Your controls</h2>
      <p>
        The signed-in Settings area exposes profile visibility, notification choices, a machine-readable
        export and account deletion. Deletion anonymises the account and revokes sessions; money and audit
        evidence may survive where a payout must remain explainable.
      </p>

      <h2>Contact</h2>
      <p>
        Questions about this draft: <a href="mailto:support@nelavista.com">support@nelavista.com</a>.
      </p>
    </LegalLayout>
  );
}

export function Terms(): JSX.Element {
  return (
    <LegalLayout kind="terms">
      <p className="nv-eyebrow">Terms of service</p>
      <h1 className="nv-display" style={{ fontSize: 'clamp(2.4rem, 5vw, 4rem)' }}>
        The rules of the record.
      </h1>
      <DraftNotice />
      <p>
        The final terms are being prepared with counsel. Until they are published, this page is a product
        outline, not a binding contract. Do not rely on it as the final terms of service.
      </p>

      <h2>What the product does</h2>
      <p>
        Nelavista provides learning materials, practice, verification, opportunities, work orders and an
        earnings ledger. Some opportunities are managed by Nelavista; others may be provided by a partner. The
        screen for each opportunity must say which one it is.
      </p>

      <h2>What the product does not promise</h2>
      <ul>
        <li>It does not guarantee admission, a verification pass, an opportunity, a job or a payout.</li>
        <li>It does not replace your university&apos;s academic rules or your employer&apos;s contract.</li>
        <li>
          It does not make a self-reported claim verified. Only the assessment, task or work in the record
          does that.
        </li>
      </ul>

      <h2>Your responsibilities</h2>
      <ul>
        <li>Use your own account and keep your credentials private.</li>
        <li>Do not submit someone else&apos;s work as your own.</li>
        <li>Do not attempt to game an assessment, a quality review or a payout.</li>
        <li>Tell us promptly if you believe your account or a payout is wrong.</li>
      </ul>

      <h2>Open questions for counsel</h2>
      <p>
        Eligibility, age, dispute resolution, governing law, refunds, suspension, intellectual property in
        submitted work and the liability cap are not decided on this page.
      </p>

      <h2>Contact</h2>
      <p>
        Questions about this draft: <a href="mailto:support@nelavista.com">support@nelavista.com</a>.
      </p>
    </LegalLayout>
  );
}

export function ContributorTerms(): JSX.Element {
  return (
    <LegalLayout kind="contributor-terms">
      <p className="nv-eyebrow">Contributor terms</p>
      <h1 className="nv-display" style={{ fontSize: 'clamp(2.4rem, 5vw, 4rem)' }}>
        If you contribute material.
      </h1>
      <DraftNotice />
      <p>
        This page is for people who contribute course material, questions, examples or other content. The
        final terms are being prepared with counsel. This draft only lists the decisions that must be made
        before contribution is opened.
      </p>

      <h2>Decisions still owed</h2>
      <ul>
        <li>Who owns the contributed material, and what licence Nelavista receives.</li>
        <li>How attribution works and whether a contributor can withdraw a piece of content.</li>
        <li>How copyright complaints are handled and who receives them.</li>
        <li>Whether contributors are paid, and on what basis.</li>
        <li>What happens to contributed material when an account is deleted.</li>
      </ul>

      <h2>Do not contribute yet</h2>
      <p>
        Contribution is not open while these terms are unresolved. Do not upload third-party material you do
        not have the right to share.
      </p>

      <h2>Contact</h2>
      <p>
        Questions about this draft: <a href="mailto:support@nelavista.com">support@nelavista.com</a>.
      </p>
    </LegalLayout>
  );
}
