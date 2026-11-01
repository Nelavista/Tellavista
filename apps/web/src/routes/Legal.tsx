import * as React from 'react';
import { Link } from 'react-router-dom';

type LegalKind = 'privacy' | 'terms' | 'contributor-terms';

const NAV: Array<{ kind: LegalKind; to: string; label: string }> = [
  { kind: 'privacy', to: '/legal/privacy', label: 'Privacy notice' },
  { kind: 'terms', to: '/legal/terms', label: 'Terms of service' },
  { kind: 'contributor-terms', to: '/legal/contributor-terms', label: 'Contributor terms' },
];

const TERMS_VERSION = '2026-10-01';

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
      <p className="nv-meta">Version {TERMS_VERSION}</p>
      <p>
        This notice explains what Nelavista collects, why we collect it, who can see it and the controls you
        have. It applies to the Nelavista web app, the student account and the operations tools used to run
        the service.
      </p>

      <h2>What we collect</h2>
      <ul>
        <li>Account details: name, email, username, password hash, roles and session state.</li>
        <li>
          Profile and preferences: display name, bio, location, time zone, learning path and visibility.
        </li>
        <li>Academic context: university, faculty, department, enrolments and semester.</li>
        <li>
          Learning and verification: materials opened, practice attempts, assessment results and evidence
          attached to a verified skill.
        </li>
        <li>
          Work and money: applications, invitations, work orders, quality decisions, ledger line items and
          payout status.
        </li>
        <li>Communications: notification records, email delivery events and push-device registrations.</li>
        <li>Consent records: the document version you accepted and when you accepted it.</li>
        <li>
          Security records: sign-in events, refresh-token history and audit entries for sensitive actions.
        </li>
      </ul>

      <h2>Why we use it</h2>
      <ul>
        <li>To create and secure your account, and to keep you signed in on the device you chose.</li>
        <li>To show your courses, materials, practice record and verification history.</li>
        <li>To match you to opportunities, process applications, assign work and review submissions.</li>
        <li>To calculate earnings, record ledger entries, prepare payouts and meet financial obligations.</li>
        <li>To send the notifications you asked for, and service messages about your account or work.</li>
        <li>To prevent abuse, investigate disputes and keep an audit trail of sensitive actions.</li>
      </ul>

      <h2>When we share data</h2>
      <p>
        We share only what the relevant task needs. A university or employer sees the record connected to your
        application or accepted work, not your private messages or unrelated practice attempts. Service
        providers that host the app, deliver email or process payments receive the data needed to perform that
        service. We may disclose data where the law requires it or where it is necessary to protect a person,
        an account or the service.
      </p>

      <h2>How long we keep it</h2>
      <p>
        We keep your account and learning record while your account is open. When you delete your account, we
        anonymise the account, remove your name, email, username, Google link and password hash, and revoke
        every session. Payout, tax, audit, fraud and dispute records may remain where they are needed to
        explain money or comply with an obligation. Those records no longer identify you by name or email.
      </p>

      <h2>Security</h2>
      <p>
        Passwords are stored as hashes, not plain text. Refresh tokens are rotated and can be revoked. Staff
        access to operations tools is role-based and sensitive actions are audited. No system is completely
        risk-free, so tell us immediately if you believe your account has been accessed without permission.
      </p>

      <h2>Your controls</h2>
      <p>
        Signed-in Settings lets you change your profile visibility, notification choices and password, review
        consent history, download a machine-readable export of your data, and delete your account. You can ask
        us to correct data that is wrong or to explain how a decision was made. If you have a concern we
        cannot resolve, you may contact the data protection authority that applies where you live.
      </p>

      <h2>Age</h2>
      <p>
        You must meet the minimum age shown in your account eligibility settings. If you are under 18, a
        parent or guardian must agree to the contributor terms before you accept paid work.
      </p>

      <h2>Contact</h2>
      <p>
        Privacy questions and data requests: <a href="mailto:support@nelavista.com">support@nelavista.com</a>.
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
      <p className="nv-meta">Version {TERMS_VERSION}</p>
      <p>
        These terms are the agreement between you and Nelavista for using the service. By creating an account,
        signing in or using the service, you accept them. If you do not accept them, do not use the service.
      </p>

      <h2>Who can use Nelavista</h2>
      <p>
        You must meet the minimum age shown in your account eligibility settings and provide accurate account
        information. If you are under 18, a parent or guardian must agree to the contributor terms before you
        accept paid work. You are responsible for the activity on your account and for keeping your
        credentials private.
      </p>

      <h2>Learning and academic integrity</h2>
      <p>
        Nelavista provides course materials, CBT practice, learning paths and verification. Your university
        remains responsible for its own academic rules. You must not present another person&apos;s work as
        your own, share assessment answers to help someone cheat, or use the service in a way that breaks your
        institution&apos;s rules.
      </p>

      <h2>Verification</h2>
      <p>
        A self-reported skill is not a verified skill. Verification comes from the assessment, task or work
        recorded by Nelavista. A verification result describes the evidence that was reviewed at that time; it
        is not a guarantee of future performance and it does not guarantee admission, employment or income.
      </p>

      <h2>Opportunities and work</h2>
      <p>
        Some opportunities are managed by Nelavista and others are provided by a partner. The screen for an
        opportunity identifies which one it is. An invitation is not an assignment until you accept it and the
        required eligibility checks pass. Work is subject to the brief, quality standard and payment terms
        shown for that opportunity.
      </p>

      <h2>Payments</h2>
      <p>
        Earnings are recorded in your ledger when work is approved and the applicable checks are complete.
        Payout timing depends on the payment method, verification and the payout schedule. Nelavista may
        withhold or reverse a payment where a review finds fraud, duplicate work, a failed check or a breach
        of these terms.
      </p>

      <h2>Your content</h2>
      <p>
        You keep ownership of the work and material you create. You give Nelavista permission to host, copy,
        review, format and publish that content as needed to operate the service, verify your skills, deliver
        work and show your record to the people you choose. Do not upload material you do not have the right
        to share.
      </p>

      <h2>Acceptable use</h2>
      <ul>
        <li>Do not use another person&apos;s account or share access to your own.</li>
        <li>Do not submit someone else&apos;s work, fabricate evidence or game an assessment or review.</li>
        <li>Do not attempt to access data that does not belong to you.</li>
        <li>Do not use the service to harass, defraud or break the law.</li>
        <li>Tell us promptly if you believe an account, payment or review is wrong.</li>
      </ul>

      <h2>Suspension and ending the agreement</h2>
      <p>
        We may suspend or close an account where these terms are broken, where a payment or identity check
        fails, or where needed to protect another person or the service. You can delete your account in
        Settings. Ending the agreement does not cancel an obligation that already arose, including a payment
        or an audit record that must remain explainable.
      </p>

      <h2>Availability and liability</h2>
      <p>
        We work to keep the service available, but we do not promise uninterrupted access. Features can change
        or be withdrawn. To the extent the law allows, Nelavista is not liable for indirect or consequential
        loss, lost profit or lost opportunity, and our total liability for a claim is limited to the amount
        you paid us in the 12 months before the claim. Nothing in these terms limits a liability that cannot
        lawfully be limited.
      </p>

      <h2>Changes</h2>
      <p>
        We may update these terms when the service or the law changes. A new version is published here and,
        where the change affects your rights, we ask you to accept it before continuing. The version you
        accepted is recorded in your consent history.
      </p>

      <h2>Contact</h2>
      <p>
        Questions about these terms: <a href="mailto:support@nelavista.com">support@nelavista.com</a>.
      </p>
    </LegalLayout>
  );
}

export function ContributorTerms(): JSX.Element {
  return (
    <LegalLayout kind="contributor-terms">
      <p className="nv-eyebrow">Contributor terms</p>
      <h1 className="nv-display" style={{ fontSize: 'clamp(2.4rem, 5vw, 4rem)' }}>
        If you contribute work.
      </h1>
      <p className="nv-meta">Version {TERMS_VERSION}</p>
      <p>
        These terms apply when you accept paid work or contribute course material, questions, examples or
        other content through Nelavista. They sit alongside the terms of service.
      </p>

      <h2>Your work is your work</h2>
      <p>
        You must do the work yourself. Subcontracting, reselling or passing off another person&apos;s output
        is not allowed. You may use the material you are given for the assigned work, but you may not share it
        outside that work or use it to train a competing service without written permission.
      </p>

      <h2>What you give Nelavista</h2>
      <p>
        You keep ownership of your contribution. You give Nelavista a worldwide, non-exclusive, royalty-free
        licence to host, copy, format, review, publish and use the contribution to operate the service,
        deliver the work, verify skills and promote Nelavista. This licence lasts while the contribution is in
        the service and for the reasonable period needed to wind down backups, audits and disputes.
      </p>

      <h2>Attribution</h2>
      <p>
        Where the work allows it, Nelavista credits the contributor by display name. Work submitted under a
        paid brief may be delivered to the client without a public credit unless the brief says otherwise.
      </p>

      <h2>Quality, rework and payment</h2>
      <p>
        Work is reviewed against the quality standard attached to the opportunity. A reviewer may ask for
        rework or reject a submission that does not meet that standard. Payment is recorded in your ledger
        when the work is approved and the applicable checks are complete. The opportunity screen states the
        rate and currency; no other rate is promised.
      </p>

      <h2>Confidentiality and data</h2>
      <p>
        Client material may be confidential. Use it only for the assigned work and do not copy it into a
        public repository, portfolio or model. Do not include another person&apos;s personal data in a
        submission unless the brief requires it and you have the right to use it.
      </p>

      <h2>Withdrawing a contribution</h2>
      <p>
        You can ask us to stop publishing a contribution you own. We will remove it from the public surface
        where we can, but we may keep a copy for backup, audit, dispute or legal reasons, and we may keep work
        that was already delivered to a client under a paid brief.
      </p>

      <h2>Complaints and copyright</h2>
      <p>
        If you believe a contribution infringes your rights, send the details to{' '}
        <a href="mailto:support@nelavista.com">support@nelavista.com</a>. Include the material, where it
        appears and why you believe it should be removed. We will review the claim and remove or restore the
        material as the evidence supports.
      </p>

      <h2>Account deletion</h2>
      <p>
        Deleting your account ends future contributions and anonymises your account. It does not remove a
        ledger entry, audit record or delivered work that must remain explainable, and it does not cancel a
        payment obligation that already arose.
      </p>

      <h2>Contact</h2>
      <p>
        Contributor questions: <a href="mailto:support@nelavista.com">support@nelavista.com</a>.
      </p>
    </LegalLayout>
  );
}
