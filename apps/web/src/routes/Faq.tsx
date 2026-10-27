import * as React from 'react';
import { Link } from 'react-router-dom';

const QUESTIONS = [
  {
    q: 'Who is Nelavista for?',
    a: 'African university students, Nigeria first, who want their course work and skills to lead to paid work. The product is built around a phone and an intermittent connection.',
  },
  {
    q: 'Do I have to choose between Academia and Skills?',
    a: 'No. You can choose Academia, Skills or both. Switching path does not delete your learning, proof or earnings.',
  },
  {
    q: 'What does “verified” mean?',
    a: 'A verified item has an assessment, practical task or piece of work behind it. The result and evidence stay attached, so the status is inspectable rather than self-reported.',
  },
  {
    q: 'Can I get work without a perfect CV?',
    a: 'The point of the record is to replace the perfect CV. Opportunities show the eligibility reason and what closes the gap. You still have to meet the requirement; Nelavista does not promise employment.',
  },
  {
    q: 'How does pay work?',
    a: 'Work has a rate and a work order. Earnings show line items, quality decisions and payout status. The ledger explains a balance instead of showing a number with no history.',
  },
  {
    q: 'What happens if I fail a verification?',
    a: 'The attempt and its result stay in your record. You can review the attempt and, where the product allows it, try again. A failed attempt is not hidden.',
  },
  {
    q: 'Is there a mobile app?',
    a: 'The web app is installable and is the launch surface. A native mobile app is a later release, not part of this launch.',
  },
  {
    q: 'How do I get help?',
    a: 'Use the contact page or email the support inbox. Include your account email and the reference from the screen you were on.',
  },
];

export function Faq(): JSX.Element {
  return (
    <section className="nv-container nv-section">
      <div className="nv-grid--2">
        <div className="nv-stack">
          <p className="nv-eyebrow">FAQ</p>
          <h1 className="nv-display" style={{ fontSize: 'clamp(2.6rem, 6vw, 4.8rem)' }}>
            The short answers.
          </h1>
          <p className="nv-lede">
            If a question is not here, the contact page is the next step. We will not invent an answer to a
            product question that is still being decided.
          </p>
          <Link className="nv-link-arrow" to="/contact">
            Contact support
          </Link>
        </div>
        <div className="nv-faq">
          {QUESTIONS.map((item) => (
            <details key={item.q}>
              <summary>{item.q}</summary>
              <p>{item.a}</p>
            </details>
          ))}
        </div>
      </div>
    </section>
  );
}
