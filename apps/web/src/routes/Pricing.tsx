import { BadgeCheck, Building2, Check, GraduationCap, Handshake, ShieldCheck } from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { Reveal } from '../components/Reveal';

const PLANS = [
  {
    icon: GraduationCap,
    name: 'Students',
    price: 'Free at launch',
    body: 'No card and no paywall between you and the work you need to do.',
    items: [
      'Course materials and CBT practice',
      'Skill lessons and practice tasks',
      'Verified skill and transcript records',
      'Applications to eligible paid work',
    ],
    action: { to: '/signup', label: 'Create account' },
  },
  {
    icon: Building2,
    name: 'Employers',
    price: 'Scoped quote',
    body: 'Priced per brief after we scope the work, the review and the payout handling.',
    items: [
      'Task volume and deadline',
      'Quality review and rework rules',
      'Payout handling and receipts',
      'A named ops contact for the brief',
    ],
    action: { to: '/contact', label: 'Talk to us' },
  },
  {
    icon: Handshake,
    name: 'Universities',
    price: 'Pilot agreement',
    body: 'A time-boxed pilot with cohort onboarding, campus context and reporting.',
    items: [
      'Cohort onboarding',
      'Campus facts and map points',
      'Adoption reporting',
      'A scoping call before any price',
    ],
    action: { to: '/contact', label: 'Discuss a pilot' },
  },
];

const COVERED = [
  ['Task volume', 'How much work is scoped, and by when.'],
  ['Review effort', 'How much human checking the brief needs.'],
  ['Payout handling', 'Who funds the work and how receipts are issued.'],
  ['Support', 'The ops contact and the response window.'],
];

export function Pricing(): JSX.Element {
  return (
    <>
      <section className="nv-container nv-section">
        <Reveal>
          <div className="nv-stack" style={{ maxWidth: '58rem' }}>
            <p className="nv-eyebrow">Pricing</p>
            <h1 className="nv-display" style={{ fontSize: 'clamp(2.6rem, 6vw, 4.8rem)' }}>
              Pricing that follows the work.
            </h1>
            <p className="nv-lede">
              Students do not pay to learn at launch. Employers pay for scoped, managed work. Universities
              start with a pilot agreement. We do not publish a per-seat number before the work is scoped.
            </p>
          </div>
        </Reveal>
      </section>

      <section className="nv-container nv-section--tight" aria-label="Plans">
        <div className="nv-grid--3">
          {PLANS.map((plan, index) => {
            const Icon = plan.icon;
            return (
              <Reveal delay={index * 0.06} key={plan.name}>
                <article className="nv-card nv-price-card">
                  <div className="nv-row nv-row--between">
                    <span className="nv-price-card__icon">
                      <Icon aria-hidden="true" size={20} strokeWidth={1.7} />
                    </span>
                    <span className="nv-badge">{plan.name}</span>
                  </div>
                  <h2 className="nv-price-card__amount">{plan.price}</h2>
                  <p className="nv-muted">{plan.body}</p>
                  <ul className="nv-price-card__list">
                    {plan.items.map((item) => (
                      <li key={item}>
                        <Check aria-hidden="true" size={15} strokeWidth={2} />
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                  <Link className="nv-button nv-button--secondary nv-button--block" to={plan.action.to}>
                    {plan.action.label}
                  </Link>
                </article>
              </Reveal>
            );
          })}
        </div>
      </section>

      <section className="nv-container nv-section--tight">
        <div className="nv-grid--2">
          <Reveal>
            <div className="nv-stack">
              <p className="nv-eyebrow">What a quote covers</p>
              <h2 className="nv-h2">The price is attached to the brief.</h2>
              <p className="nv-lede">
                A managed brief is not a licence fee. The quote reflects the work Nelavista has to scope,
                review, pay and support.
              </p>
              <dl className="nv-facts">
                {COVERED.map(([term, detail]) => (
                  <div key={term}>
                    <dt>{term}</dt>
                    <dd>{detail}</dd>
                  </div>
                ))}
              </dl>
            </div>
          </Reveal>
          <Reveal delay={0.08}>
            <div className="nv-card nv-stack">
              <span className="nv-price-card__icon">
                <ShieldCheck aria-hidden="true" size={20} strokeWidth={1.7} />
              </span>
              <h2 className="nv-h3">What we do not do</h2>
              <ul className="nv-list">
                <li>We do not charge students to create an account, read materials or practise CBT.</li>
                <li>We do not run a self-serve employer checkout at launch.</li>
                <li>We do not publish a university price before a pilot is scoped.</li>
                <li>We do not add a placement fee that is hidden from the work order.</li>
              </ul>
              <p className="nv-meta">
                <BadgeCheck aria-hidden="true" size={14} /> Commercial positions reviewed 29 October 2026.
              </p>
            </div>
          </Reveal>
        </div>
      </section>

      <section className="nv-container nv-section--tight">
        <Reveal>
          <div className="nv-card nv-stack nv-stack--tight">
            <p className="nv-eyebrow">Need a number?</p>
            <h2 className="nv-h2">Tell us the brief, not the headcount.</h2>
            <p className="nv-lede">
              Send the task, the volume, the deadline and the quality bar. We will reply with a scoped quote
              or say the brief is not a fit.
            </p>
            <div className="nv-row">
              <Link className="nv-button" to="/contact">
                Start a scoping conversation
              </Link>
              <Link className="nv-button nv-button--secondary" to="/how-it-works">
                See how the work runs
              </Link>
            </div>
          </div>
        </Reveal>
      </section>
    </>
  );
}
