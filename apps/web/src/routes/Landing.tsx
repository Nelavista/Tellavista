import {
  ArrowRight,
  BadgeCheck,
  BookOpen,
  Briefcase,
  FileText,
  ShieldCheck,
  Sparkles,
  Wallet,
} from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

const PROOF = [
  {
    number: '01',
    title: 'Learn',
    body: 'Course materials, CBT practice and short skill lessons in one place. Ask Nelavista when a topic will not sit still.',
  },
  {
    number: '02',
    title: 'Prove',
    body: 'Assessments, practical tasks and evidence. Your transcript records what you did, when, and what it was checked against.',
  },
  {
    number: '03',
    title: 'Work',
    body: 'Eligible opportunities with the reason you qualify, the rate, the deadline and the work order in the same record.',
  },
  {
    number: '04',
    title: 'Get paid',
    body: 'A ledger you can read: line items, quality decisions, payout status and the receipt. No mystery balance.',
  },
];

const RECORD = [
  { label: 'Verified skill', value: 'Data annotation', meta: 'Evidence attached · 12 Oct' },
  { label: 'Work order', value: 'Annotation pilot', meta: '5 hours · USD 15.00' },
  { label: 'Quality check', value: 'Passed', meta: 'Reviewed by ops · 14 Oct' },
  { label: 'Payout', value: 'Paid', meta: 'Line item · USD 15.00' },
];

export function Landing(): JSX.Element {
  return (
    <>
      <section className="nv-container nv-home-hero">
        <div className="nv-hero" style={{ padding: 0 }}>
          <div className="nv-hero__copy">
            <p className="nv-eyebrow">The working record</p>
            <h1 className="nv-display">
              Learn it.
              <br />
              Prove it.
              <br />
              <em>Get paid for it.</em>
            </h1>
            <p className="nv-lede">
              Nelavista verifies what you actually know, then matches you to paid work you can do from your
              phone. One account for your courses, skills, evidence, work and earnings.
            </p>
            <div className="nv-row">
              <Link className="nv-button" to="/signup">
                Create your account
                <ArrowRight aria-hidden="true" size={16} />
              </Link>
              <Link className="nv-button nv-button--secondary" to="/how-it-works">
                See how it works
              </Link>
            </div>
            <div className="nv-hero-proof">
              <div className="nv-hero-proof__item">
                <strong>Academia + Skills</strong>
                <span>Two ways in, one record</span>
              </div>
              <div className="nv-hero-proof__item">
                <strong>Evidence, not a CV</strong>
                <span>Assessments and practical work</span>
              </div>
              <div className="nv-hero-proof__item">
                <strong>Readable money</strong>
                <span>Ledger, not a mystery balance</span>
              </div>
            </div>
          </div>

          <div className="nv-hero__media">
            <div className="nv-card nv-card--flat" style={{ padding: 0 }}>
              <div className="nv-panel__head">
                <span className="nv-meta">Illustrative record</span>
                <span className="nv-badge nv-badge--success">
                  <BadgeCheck aria-hidden="true" size={12} />
                  Verified
                </span>
              </div>
              <div style={{ padding: 'var(--nv-space-lg)' }}>
                {RECORD.map((row) => (
                  <div
                    key={row.label}
                    className="nv-row nv-row--between"
                    style={{
                      alignItems: 'flex-start',
                      borderBottom: '1px solid var(--nv-border)',
                      padding: 'var(--nv-space-md) 0',
                    }}
                  >
                    <div>
                      <p className="nv-meta">{row.label}</p>
                      <p className="nv-h4">{row.value}</p>
                    </div>
                    <p className="nv-meta" style={{ textAlign: 'right' }}>
                      {row.meta}
                    </p>
                  </div>
                ))}
              </div>
              <div className="nv-panel__foot nv-row nv-row--between">
                <span className="nv-meta">The record is the proof</span>
                <FileText aria-hidden="true" size={16} />
              </div>
            </div>
            <div className="nv-hero__caption">
              <span>Not a stock photo. The product is the artifact.</span>
              <span>V2</span>
            </div>
          </div>
        </div>
      </section>

      <section className="nv-container nv-section nv-section--tight">
        <div className="nv-section-head">
          <div>
            <p className="nv-eyebrow">The problem</p>
            <h2>Your CV says you can. Your record should show it.</h2>
          </div>
          <p>
            A certificate is easy to claim and hard to check. A group chat is not a work history. Nelavista
            keeps the learning, the evidence and the paid work together, so the next person does not have to
            take your word for it.
          </p>
        </div>
        <div className="nv-problem-list">
          <div className="nv-problem">
            <span className="nv-problem__number">01</span>
            <h3>Learning is scattered</h3>
            <p>
              Notes in one app, past questions in another, a video link in a group chat. Nothing connects the
              topic to the proof.
            </p>
          </div>
          <div className="nv-problem">
            <span className="nv-problem__number">02</span>
            <h3>Proof is self-reported</h3>
            <p>
              “I know Excel” is a sentence. A task, a score and an evidence link are a record someone can
              inspect.
            </p>
          </div>
          <div className="nv-problem">
            <span className="nv-problem__number">03</span>
            <h3>Work is hard to trust</h3>
            <p>
              Who is paying, for what, by when, and what happens if the work fails? Those answers should be
              visible before you start.
            </p>
          </div>
        </div>
      </section>

      <section className="nv-container nv-section">
        <div className="nv-section-head">
          <div>
            <p className="nv-eyebrow">One chain</p>
            <h2>From a topic to a receipt.</h2>
          </div>
          <p>
            Each step leaves a mark in the same record. Nothing is a dead end and nothing has to be
            re-entered.
          </p>
        </div>
        <div className="nv-proof-chain">
          {PROOF.map((step) => (
            <div className="nv-proof-step" key={step.number}>
              <span className="nv-proof-step__number">{step.number}</span>
              <h3>{step.title}</h3>
              <p>{step.body}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="nv-container nv-section nv-section--tight">
        <div className="nv-grid--2">
          <div className="nv-stack">
            <p className="nv-eyebrow">Two ways in</p>
            <h2 className="nv-h1">Start with your course or your skill.</h2>
            <p className="nv-lede">
              You do not have to choose a permanent identity. Switch path when your semester changes. Your
              learning, proof and earnings stay.
            </p>
            <div className="nv-home-next">
              <div className="nv-home-next__item">
                <BookOpen aria-hidden="true" size={18} />
                <h2>Academia</h2>
                <p>Courses, materials, CBT practice and academic evidence.</p>
              </div>
              <div className="nv-home-next__item">
                <Sparkles aria-hidden="true" size={18} />
                <h2>Skills</h2>
                <p>Short lessons, practice and a verifiable skill record.</p>
              </div>
            </div>
          </div>
          <div className="nv-card">
            <p className="nv-eyebrow">What stays with you</p>
            <ul className="nv-list" style={{ marginTop: 'var(--nv-space-lg)' }}>
              <li className="nv-row">
                <ShieldCheck aria-hidden="true" size={18} />
                <span>Verification status and evidence, not a badge you can buy.</span>
              </li>
              <li className="nv-row">
                <Briefcase aria-hidden="true" size={18} />
                <span>Applications, work orders and quality decisions.</span>
              </li>
              <li className="nv-row">
                <Wallet aria-hidden="true" size={18} />
                <span>Earnings line items and payout receipts.</span>
              </li>
              <li className="nv-row">
                <FileText aria-hidden="true" size={18} />
                <span>A transcript you can share with a scoped link.</span>
              </li>
            </ul>
          </div>
        </div>
      </section>

      <section className="nv-container nv-section">
        <div className="nv-cta-band">
          <h2>Your next step should be obvious.</h2>
          <div className="nv-stack nv-stack--tight">
            <p className="nv-muted" style={{ maxWidth: '40ch' }}>
              Create an account, choose your path, and start with the work in front of you.
            </p>
            <div className="nv-row">
              <Link className="nv-button" to="/signup">
                Create your account
                <ArrowRight aria-hidden="true" size={16} />
              </Link>
              <Link className="nv-button nv-button--ghost" to="/login">
                I already have one
              </Link>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
