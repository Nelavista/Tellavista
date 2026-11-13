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

import { EditorialImage } from '../components/EditorialImage';
import { Reveal } from '../components/Reveal';

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

const FAULTS = [
  {
    label: 'Scattered',
    title: 'Learning lives in five places.',
    body: 'Notes in one app, past questions in another, a video link in a group chat. Nothing connects the topic to the proof.',
  },
  {
    label: 'Self-reported',
    title: '“I know Excel” is a sentence.',
    body: 'A task, a score and an evidence link are a record someone can inspect. A claim on a CV is not.',
  },
  {
    label: 'Unclear',
    title: 'Work is hard to trust.',
    body: 'Who is paying, for what, by when, and what happens if the work fails? Those answers should be visible before you start.',
  },
];

const KEEPS = [
  { icon: ShieldCheck, text: 'Verification status and evidence, not a badge you can buy.' },
  { icon: Briefcase, text: 'Applications, work orders and quality decisions.' },
  { icon: Wallet, text: 'Earnings line items and payout receipts.' },
  { icon: FileText, text: 'A transcript you can share with a scoped link.' },
];

export function Landing(): JSX.Element {
  return (
    <>
      <section className="nv-container nv-landing-hero">
        <div className="nv-hero nv-hero--landing">
          <Reveal className="nv-hero__copy">
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
            <dl className="nv-hero-facts">
              <div>
                <dt>Academia + Skills</dt>
                <dd>Two ways in, one record</dd>
              </div>
              <div>
                <dt>Evidence, not a CV</dt>
                <dd>Assessments and practical work</dd>
              </div>
              <div>
                <dt>Readable money</dt>
                <dd>Ledger, not a mystery balance</dd>
              </div>
            </dl>
          </Reveal>

          <Reveal className="nv-hero__media nv-hero__media--landing" delay={0.08}>
            <EditorialImage
              alt="A student at a shared desk reading a long printed record beside a closed notebook."
              className="nv-hero__figure"
              name="hero-main"
              priority
            />
            <div className="nv-card nv-record" style={{ padding: 0 }}>
              <div className="nv-panel__head">
                <span className="nv-meta">Illustrative record</span>
                <span className="nv-badge nv-badge--success">
                  <BadgeCheck aria-hidden="true" size={12} />
                  Verified
                </span>
              </div>
              <div className="nv-record__body">
                {RECORD.map((row) => (
                  <div key={row.label} className="nv-record__row">
                    <div>
                      <p className="nv-meta">{row.label}</p>
                      <p className="nv-h4">{row.value}</p>
                    </div>
                    <p className="nv-meta nv-record__meta">{row.meta}</p>
                  </div>
                ))}
              </div>
              <div className="nv-panel__foot nv-row nv-row--between">
                <span className="nv-meta">The record is the proof</span>
                <FileText aria-hidden="true" size={16} />
              </div>
            </div>
            <div className="nv-hero__caption">
              <span>Editorial illustration, not a real student or campus.</span>
            </div>
          </Reveal>
        </div>
      </section>

      <section className="nv-container nv-chapter">
        <div className="nv-fault-grid">
          <div className="nv-fault-grid__statement">
            <h2 className="nv-h1">Your CV says you can. Your record should show it.</h2>
            <p className="nv-lede">
              A certificate is easy to claim and hard to check. A group chat is not a work history. Nelavista
              keeps the learning, the evidence and the paid work together, so the next person does not have to
              take your word for it.
            </p>
          </div>
          <div className="nv-faults">
            {FAULTS.map((fault) => (
              <article className="nv-fault" key={fault.label}>
                <p className="nv-fault__label">{fault.label}</p>
                <h3>{fault.title}</h3>
                <p>{fault.body}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="nv-container nv-chapter">
        <div className="nv-chapter__head">
          <h2 className="nv-h1">From a topic to a receipt.</h2>
          <p className="nv-lede">
            Each step leaves a mark in the same record. Nothing is a dead end and nothing has to be
            re-entered.
          </p>
        </div>
        <ol className="nv-chain">
          {PROOF.map((step) => (
            <li className="nv-chain__step" key={step.number}>
              <span className="nv-chain__node" aria-hidden="true">
                {step.number}
              </span>
              <h3>{step.title}</h3>
              <p>{step.body}</p>
            </li>
          ))}
        </ol>
      </section>

      <section className="nv-container nv-chapter">
        <div className="nv-split nv-split--landing">
          <div className="nv-stack">
            <h2 className="nv-h1">Start with your course or your skill.</h2>
            <p className="nv-lede">
              You do not have to choose a permanent identity. Switch path when your semester changes. Your
              learning, proof and earnings stay.
            </p>
            <ul className="nv-paths">
              <li>
                <span className="nv-paths__icon" aria-hidden="true">
                  <BookOpen size={18} strokeWidth={1.7} />
                </span>
                <div>
                  <h3>Academia</h3>
                  <p>Courses, materials, CBT practice and academic evidence.</p>
                </div>
                <span className="nv-meta">For a semester</span>
              </li>
              <li>
                <span className="nv-paths__icon" aria-hidden="true">
                  <Sparkles size={18} strokeWidth={1.7} />
                </span>
                <div>
                  <h3>Skills</h3>
                  <p>Short lessons, practice and a verifiable skill record.</p>
                </div>
                <span className="nv-meta">For a role</span>
              </li>
            </ul>
          </div>
          <aside className="nv-panel nv-panel--inverted nv-keeps">
            <h3 className="nv-h3">What stays with you</h3>
            <p className="nv-keeps__lede">Switching space changes the dashboard, never the record.</p>
            <ul className="nv-keeps__list">
              {KEEPS.map((item) => {
                const Icon = item.icon;
                return (
                  <li key={item.text}>
                    <Icon aria-hidden="true" size={17} strokeWidth={1.7} />
                    <span>{item.text}</span>
                  </li>
                );
              })}
            </ul>
          </aside>
        </div>
      </section>

      <section className="nv-container nv-chapter">
        <div className="nv-statement">
          <h2>A record we can stand behind.</h2>
          <div className="nv-statement__body">
            <p className="nv-lede">
              We publish what the product can prove: learning connected to evidence, evidence connected to
              work, and work connected to a readable payout. Reach figures appear only when they are verified
              against a current source.
            </p>
            <p className="nv-muted">
              No invented metrics, no borrowed testimonials. If a number is not defensible today, it is not on
              the page.
            </p>
            <Link className="nv-link-arrow" to="/impact">
              Read the impact page
              <ArrowRight aria-hidden="true" size={15} />
            </Link>
          </div>
        </div>
      </section>

      <section className="nv-container nv-chapter nv-chapter--bare">
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
