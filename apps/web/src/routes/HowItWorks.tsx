import * as React from 'react';
import { Link } from 'react-router-dom';

import { EditorialImage } from '../components/EditorialImage';
import { Reveal } from '../components/Reveal';

const STEPS: Array<{
  number: string;
  title: string;
  body: string;
  detail: string;
  image?: { name: string; alt: string };
}> = [
  {
    number: '01',
    title: 'Enrol and choose a path',
    body: 'Add your university, department and courses. Choose Academia, Skills or both. You can switch later without losing anything.',
    detail: 'The account starts with your context, not a blank dashboard.',
    image: {
      name: 'how-learn',
      alt: 'A student drawing a simple path of blank boxes in a notebook.',
    },
  },
  {
    number: '02',
    title: 'Learn with the material you already have',
    body: 'Open your course materials, read them in the app, practise with CBT questions and ask about the part that is not clear.',
    detail: 'Every screen keeps the next action visible: read, practise, ask or verify.',
  },
  {
    number: '03',
    title: 'Prove it with an assessment or a task',
    body: 'A verification is a real assessment or practical task. The result, the evidence and the date stay attached to the skill.',
    detail: 'No click-to-complete. A status is only as good as the work behind it.',
    image: {
      name: 'how-prove',
      alt: 'A hand lowering a rubber stamp onto a ruled page.',
    },
  },
  {
    number: '04',
    title: 'See the work you can actually do',
    body: 'Opportunities show the eligibility reason, rate, deadline and what the work involves. If you are not eligible, the screen says what closes the gap.',
    detail: 'The explanation is part of the product, not a support ticket.',
    image: {
      name: 'how-work',
      alt: 'A student reviewing a printed work ticket with a pencil.',
    },
  },
  {
    number: '05',
    title: 'Do the work and get a quality decision',
    body: 'A work order holds the brief, the deadline and the deliverable. Quality review is explicit, including what happens if the work fails.',
    detail: 'You should never have to guess whether the work was accepted.',
  },
  {
    number: '06',
    title: 'Get paid and keep the receipt',
    body: 'Earnings are line items: what the work paid, what was deducted, whether it is pending or paid. Your transcript keeps the proof.',
    detail: 'The money is part of the record, not a separate screen with a number and no explanation.',
    image: {
      name: 'how-earn',
      alt: 'A student checking a printed receipt against a small cash box.',
    },
  },
];

export function HowItWorks(): JSX.Element {
  return (
    <>
      <section className="nv-container nv-section">
        <div className="nv-how-grid">
          <Reveal className="nv-how-sticky nv-stack">
            <p className="nv-eyebrow">How it works</p>
            <h1 className="nv-display" style={{ fontSize: 'clamp(2.6rem, 5vw, 4.6rem)' }}>
              Six steps. One record.
            </h1>
            <p className="nv-lede">
              The chain is deliberately boring: learn, prove, match, work, check, pay. Each step leaves
              evidence for the next one.
            </p>
            <div className="nv-row">
              <Link className="nv-button" to="/signup">
                Create your account
              </Link>
              <Link className="nv-button nv-button--ghost" to="/features">
                See the features
              </Link>
            </div>
          </Reveal>

          <div className="nv-how-list">
            {STEPS.map((step, index) => (
              <Reveal delay={index * 0.04} key={step.number}>
                <article className={step.image ? 'nv-how-item nv-how-item--media' : 'nv-how-item'}>
                  <div className="nv-how-item__copy">
                    <div className="nv-how-item__meta">
                      <span>{step.number}</span>
                      <span>{step.detail}</span>
                    </div>
                    <h3>{step.title}</h3>
                    <p>{step.body}</p>
                  </div>
                  {step.image ? (
                    <EditorialImage
                      alt={step.image.alt}
                      className="nv-how-item__figure"
                      height={1024}
                      name={step.image.name}
                      width={1024}
                    />
                  ) : null}
                </article>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      <section className="nv-container nv-section nv-section--tight">
        <Reveal>
          <div className="nv-cta-band">
            <h2>You do not need a perfect CV. You need a record.</h2>
            <div className="nv-row">
              <Link className="nv-button" to="/signup">
                Start your record
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
