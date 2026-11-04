import { Check, FileCheck2, GraduationCap, Handshake } from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { Reveal } from '../components/Reveal';

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

export function Impact(): JSX.Element {
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
                This page intentionally publishes no reach figures, testimonials or partner claims. We will
                add numbers only when they are verified against a current source and approved for publication.
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

      <section className="nv-container nv-section nv-section--tight">
        <Reveal>
          <div className="nv-section-head">
            <div>
              <p className="nv-eyebrow">The working record</p>
              <h2>Impact is visible in the product.</h2>
            </div>
            <p>
              We measure outcomes from current records, not from stale marketing copy. Until those measures
              are verified, the honest account is the work the product enables.
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
