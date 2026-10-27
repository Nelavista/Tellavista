import { Check, ShieldCheck, Smartphone, Wallet } from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

const PRINCIPLES = [
  {
    icon: ShieldCheck,
    title: 'Evidence over assertion',
    body: 'A claim is a start. A verified item keeps the assessment, task or work that supports it.',
  },
  {
    icon: Smartphone,
    title: 'Built for the phone in your hand',
    body: 'A mid-range Android, a slow connection and a real deadline are the design constraints, not an afterthought.',
  },
  {
    icon: Wallet,
    title: 'Money should be readable',
    body: 'Line items, quality decisions and payout status. If a balance changes, the record says why.',
  },
];

export function About(): JSX.Element {
  return (
    <>
      <section className="nv-container nv-section">
        <div className="nv-grid--2">
          <div className="nv-stack">
            <p className="nv-eyebrow">About</p>
            <h1 className="nv-display" style={{ fontSize: 'clamp(2.6rem, 6vw, 4.8rem)' }}>
              A record that travels with you.
            </h1>
            <p className="nv-lede">
              Nelavista is a platform for African university students, Nigeria first. It takes the work you
              already do in a course or a skill and turns it into evidence you can use to get paid work.
            </p>
            <p className="nv-muted" style={{ maxWidth: '58ch' }}>
              The product is deliberately one journey: Enrol, Learn, Build, Verify, Match, Work, Quality
              check, Earn. The screen should always make the next step obvious, and the record should always
              say what happened.
            </p>
          </div>
          <div className="nv-card nv-stack">
            <p className="nv-eyebrow">What we are not</p>
            <ul className="nv-list">
              <li className="nv-row">
                <Check aria-hidden="true" size={16} />
                <span>Not a certificate mill. Verification is work, not a checkout.</span>
              </li>
              <li className="nv-row">
                <Check aria-hidden="true" size={16} />
                <span>Not a job board with no quality gate.</span>
              </li>
              <li className="nv-row">
                <Check aria-hidden="true" size={16} />
                <span>Not a social feed. The record is the point.</span>
              </li>
              <li className="nv-row">
                <Check aria-hidden="true" size={16} />
                <span>Not a promise of employment. A clearer path to the work you can do.</span>
              </li>
            </ul>
          </div>
        </div>
      </section>

      <section className="nv-container nv-section nv-section--tight">
        <div className="nv-section-head">
          <div>
            <p className="nv-eyebrow">Principles</p>
            <h2>What the product refuses to fake.</h2>
          </div>
          <p>
            These are product rules, not marketing lines. If a screen cannot show the evidence, it should not
            show the badge.
          </p>
        </div>
        <div className="nv-feature-grid" style={{ gridTemplateColumns: 'repeat(3, minmax(0, 1fr))' }}>
          {PRINCIPLES.map((principle) => {
            const Icon = principle.icon;
            return (
              <article className="nv-feature" key={principle.title}>
                <Icon aria-hidden="true" size={20} strokeWidth={1.6} />
                <h3>{principle.title}</h3>
                <p>{principle.body}</p>
              </article>
            );
          })}
        </div>
      </section>

      <section className="nv-container nv-section">
        <div className="nv-cta-band">
          <h2>Bring the work. Leave with a record.</h2>
          <div className="nv-row">
            <Link className="nv-button" to="/signup">
              Create your account
            </Link>
            <Link className="nv-button nv-button--secondary" to="/contact">
              Contact us
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
