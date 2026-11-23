import type { ImpactOut } from '@nelavista/api-client';
import { Check, FileCheck2, GraduationCap, Handshake } from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { Reveal } from '../components/Reveal';
import { useApiResource } from '../lib/resource';

const OUTCOMES = [
  {
    icon: GraduationCap,
    title: 'Learning stays connected',
    body: 'Students can move from university context and practice into a record of what they learned.',
  },
  {
    icon: FileCheck2,
    title: 'Evidence replaces assertion',
    body: 'Assessments, practical tasks and quality decisions stay attached to the skills they support.',
  },
  {
    icon: Handshake,
    title: 'Work starts with clarity',
    body: 'Eligible opportunities explain the brief, deadline, rate and quality expectations before work begins.',
  },
];

function formatMoney(amountMinor: number, currency: string): string {
  const amount = amountMinor / 100;
  try {
    return new Intl.NumberFormat(undefined, {
      style: 'currency',
      currency,
      maximumFractionDigits: 2,
    }).format(amount);
  } catch {
    return `${currency} ${amount.toFixed(2)}`;
  }
}

export function Impact(): JSX.Element {
  const { resource } = useApiResource<ImpactOut>('/platform/impact');
  const data = resource.status === 'ready' ? resource.data : null;

  return (
    <>
      <section className="nv-container nv-section">
        <Reveal>
          <div className="nv-grid--2">
            <div className="nv-stack">
              <p className="nv-eyebrow">Impact</p>
              <h1 className="nv-display" style={{ fontSize: 'clamp(2.6rem, 6vw, 4.8rem)' }}>
                Make the work easier to trust.
              </h1>
              <p className="nv-lede">
                Nelavista connects learning, evidence and paid work so students can show what they can do
                without relying on a claim alone.
              </p>
              <p className="nv-muted" style={{ maxWidth: '58ch' }}>
                The figures below are read from the product database. They count what the platform has
                recorded — verified skills, passed assessments, reviewed practical work and approved paid work
                — not a projection or a survey.
              </p>
              <div className="nv-row">
                <Link className="nv-button" to="/how-it-works">
                  See how it works
                </Link>
                <Link className="nv-button nv-button--secondary" to="/contact">
                  Contact us
                </Link>
              </div>
            </div>
            <div className="nv-card nv-stack">
              <p className="nv-eyebrow">What we can stand behind</p>
              <ul className="nv-list">
                <li className="nv-row">
                  <Check aria-hidden="true" size={16} />
                  <span>Current product capabilities are described, not inflated.</span>
                </li>
                <li className="nv-row">
                  <Check aria-hidden="true" size={16} />
                  <span>Verification is tied to assessments, practical work or review.</span>
                </li>
                <li className="nv-row">
                  <Check aria-hidden="true" size={16} />
                  <span>Financial records show what changed and why.</span>
                </li>
              </ul>
            </div>
          </div>
        </Reveal>
      </section>

      <section className="nv-container nv-section nv-section--tight" aria-labelledby="impact-figures">
        <Reveal>
          <div className="nv-section-head">
            <div>
              <p className="nv-eyebrow">The working record</p>
              <h2 id="impact-figures">What the platform has recorded.</h2>
            </div>
            <p>
              Each number is a count of current rows. Nothing is estimated, and a figure of zero stays visible
              because zero is the honest answer until the work happens.
            </p>
          </div>
        </Reveal>

        {resource.status === 'loading' ? (
          <p className="nv-meta" role="status">
            Reading the record…
          </p>
        ) : null}

        {resource.status !== 'ready' && resource.status !== 'loading' ? (
          <div className="nv-card nv-stack">
            <p className="nv-h3">Live figures are unavailable right now.</p>
            <p className="nv-muted">
              We will not replace them with an estimate. The qualitative account below still describes what
              the product does.
            </p>
          </div>
        ) : null}

        {data ? (
          <>
            {data.metrics.length === 0 ? (
              <div className="nv-card nv-stack">
                <p className="nv-h3">Figures are being checked before publication.</p>
                <p className="nv-muted">
                  The product is running; the reach numbers are temporarily held back while ops verifies them.
                  Nothing here is a placeholder.
                </p>
              </div>
            ) : (
              <Reveal delay={0.06}>
                <div className="nv-feature-grid" style={{ gridTemplateColumns: 'repeat(3, minmax(0, 1fr))' }}>
                  {data.metrics.map((metric) => (
                    <article className="nv-feature" key={metric.key}>
                      <p className="nv-meta">{metric.label}</p>
                      <p className="nv-stat__value">{metric.value.toLocaleString()}</p>
                      <p>{metric.detail}</p>
                    </article>
                  ))}
                </div>
              </Reveal>
            )}

            {data.paid_by_currency.length > 0 ? (
              <Reveal delay={0.08}>
                <div className="nv-card nv-stack" style={{ marginTop: 'var(--nv-space-lg)' }}>
                  <p className="nv-eyebrow">Paid to students</p>
                  <ul className="nv-list">
                    {data.paid_by_currency.map((row) => (
                      <li key={row.currency}>
                        <span className="nv-h3">{formatMoney(row.amount_minor, row.currency)}</span>
                        <span className="nv-meta"> · {row.currency}</span>
                      </li>
                    ))}
                  </ul>
                  <p className="nv-muted">
                    Only earnings the ledger marks as paid are included. Amounts are never added across
                    currencies.
                  </p>
                </div>
              </Reveal>
            ) : null}

            <p className="nv-meta" style={{ marginTop: 'var(--nv-space-md)' }}>
              Read from the platform database on{' '}
              {new Date(data.generated_at).toLocaleDateString(undefined, {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
              })}
              .
            </p>
          </>
        ) : null}
      </section>

      <section className="nv-container nv-section nv-section--tight">
        <Reveal>
          <div className="nv-section-head">
            <div>
              <p className="nv-eyebrow">How impact shows up</p>
              <h2>The record is the outcome.</h2>
            </div>
            <p>
              These are the product behaviours behind the figures: learning that connects to proof, proof that
              connects to work, and work that connects to a readable payout.
            </p>
          </div>
        </Reveal>
        <Reveal delay={0.06}>
          <div className="nv-feature-grid" style={{ gridTemplateColumns: 'repeat(3, minmax(0, 1fr))' }}>
            {OUTCOMES.map((outcome) => {
              const Icon = outcome.icon;
              return (
                <article className="nv-feature" key={outcome.title}>
                  <Icon aria-hidden="true" size={20} strokeWidth={1.6} />
                  <h3>{outcome.title}</h3>
                  <p>{outcome.body}</p>
                </article>
              );
            })}
          </div>
        </Reveal>
      </section>

      <section className="nv-container nv-section">
        <Reveal>
          <div className="nv-cta-band">
            <h2>Build a record that can travel with you.</h2>
            <div className="nv-row">
              <Link className="nv-button" to="/signup">
                Create your account
              </Link>
              <Link className="nv-button nv-button--secondary" to="/about">
                Why Nelavista
              </Link>
            </div>
          </div>
        </Reveal>
      </section>
    </>
  );
}
