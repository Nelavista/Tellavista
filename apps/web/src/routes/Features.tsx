import {
  BadgeCheck,
  BookOpen,
  Briefcase,
  ClipboardCheck,
  FileText,
  MapPin,
  Sparkles,
  Wallet,
} from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

const FEATURES = [
  {
    icon: BookOpen,
    title: 'Academia',
    body: 'Your enrolled courses, the materials attached to them, and a place to ask when a topic is not clear.',
  },
  {
    icon: ClipboardCheck,
    title: 'CBT practice',
    body: 'Timed practice that shows the result, the topic and the next thing to revise. Not a score with no explanation.',
  },
  {
    icon: Sparkles,
    title: 'Skills',
    body: 'Short lessons, practice and a skill record that says what you can do and what evidence supports it.',
  },
  {
    icon: BadgeCheck,
    title: 'Verification',
    body: 'Assessments and practical tasks produce a status you can share. The evidence stays attached.',
  },
  {
    icon: Briefcase,
    title: 'Opportunities',
    body: 'Paid work with the eligibility reason, rate, deadline and work order visible before you apply.',
  },
  {
    icon: Wallet,
    title: 'Earnings',
    body: 'A ledger with line items, quality decisions and payout status. The receipt is part of the record.',
  },
  {
    icon: FileText,
    title: 'Transcript + Talent',
    body: 'A proof page you control. Share a scoped link instead of sending a CV and hoping.',
  },
  {
    icon: MapPin,
    title: 'Campus',
    body: 'Your campus context, kept with your account so the right courses and opportunities can find you.',
  },
];

export function Features(): JSX.Element {
  return (
    <>
      <section className="nv-container nv-section">
        <div className="nv-stack" style={{ maxWidth: '54rem' }}>
          <p className="nv-eyebrow">Features</p>
          <h1 className="nv-display" style={{ fontSize: 'clamp(2.6rem, 6vw, 4.8rem)' }}>
            One record for the whole journey.
          </h1>
          <p className="nv-lede">
            Nelavista is not a course catalogue with a job board bolted on. It is the record that connects
            what you learn, what you can prove, the work you do and the money you earn.
          </p>
        </div>
      </section>

      <section className="nv-container nv-section nv-section--tight">
        <div className="nv-feature-grid">
          {FEATURES.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <article className="nv-feature" key={feature.title}>
                <span className="nv-feature__number">{String(index + 1).padStart(2, '0')}</span>
                <Icon aria-hidden="true" size={20} strokeWidth={1.6} />
                <h3>{feature.title}</h3>
                <p>{feature.body}</p>
              </article>
            );
          })}
        </div>
      </section>

      <section className="nv-container nv-section">
        <div className="nv-grid--2">
          <div className="nv-stack">
            <p className="nv-eyebrow">What makes it different</p>
            <h2 className="nv-h1">The evidence is the product.</h2>
            <p className="nv-lede">
              A status with no evidence is a sticker. Every verified item in Nelavista keeps the assessment,
              task or work that produced it, so a person reviewing your record can see the basis, not just the
              badge.
            </p>
          </div>
          <div className="nv-card nv-stack">
            <div className="nv-row nv-row--between">
              <span className="nv-meta">Example transcript row</span>
              <span className="nv-badge nv-badge--success">Verified</span>
            </div>
            <div>
              <p className="nv-h3">Data annotation</p>
              <p className="nv-muted">Practical task · 5 hours · reviewed</p>
            </div>
            <div className="nv-divider" />
            <div className="nv-row nv-row--between">
              <span className="nv-muted">Evidence</span>
              <span className="nv-mono">task-1042</span>
            </div>
            <div className="nv-row nv-row--between">
              <span className="nv-muted">Status</span>
              <span className="nv-mono">verified</span>
            </div>
            <Link className="nv-link-arrow" to="/how-it-works">
              See the proof chain
            </Link>
          </div>
        </div>
      </section>

      <section className="nv-container nv-section">
        <div className="nv-cta-band">
          <h2>Start with what is in front of you.</h2>
          <div className="nv-row">
            <Link className="nv-button" to="/signup">
              Create your account
            </Link>
            <Link className="nv-button nv-button--secondary" to="/faq">
              Read the FAQ
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
