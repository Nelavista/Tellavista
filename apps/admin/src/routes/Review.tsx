/**
 * Quality review (C5).
 *
 * A reviewer sees the submission exactly as the student sent it, records a
 * verdict, and — when overriding the automatic result — must give a reason. The
 * same page holds the verification override, which is always logged.
 */
import type {
  OverrideOut,
  PracticalQueueOut,
  PracticalReviewOut,
  ReviewOut,
  ReviewQueueOut,
  StandardOut,
} from '@nelavista/api-client';
import * as React from 'react';

import { ApiError, http } from '../lib/http';
import { useResource } from '../lib/resource';
import { when } from '../lib/format';

const VERDICTS = ['approved', 'rework', 'rejected'];

export function Review(): JSX.Element {
  const queue = useResource<ReviewQueueOut>('/work/review-queue');
  const [selected, setSelected] = React.useState<number | null>(null);
  const [verdict, setVerdict] = React.useState('approved');
  const [score, setScore] = React.useState('90');
  const [notes, setNotes] = React.useState('');
  const [isOverride, setIsOverride] = React.useState(false);
  const [reason, setReason] = React.useState('');
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [note, setNote] = React.useState<string | null>(null);
  const [reviewed, setReviewed] = React.useState<ReviewOut | null>(null);

  const practical = useResource<PracticalQueueOut>('/verification/practical/submissions');

  const [projectSlug, setProjectSlug] = React.useState('');
  const [standardName, setStandardName] = React.useState('Annotation standard');
  const [threshold, setThreshold] = React.useState('80');
  const [instructions, setInstructions] = React.useState('');
  const [rules, setRules] = React.useState('{}');
  const [standard, setStandard] = React.useState<StandardOut | null>(null);

  const [overrideUser, setOverrideUser] = React.useState('');
  const [overrideSkill, setOverrideSkill] = React.useState('');
  const [overrideStatus, setOverrideStatus] = React.useState('verified');
  const [overrideReason, setOverrideReason] = React.useState('');
  const [overrideResult, setOverrideResult] = React.useState<OverrideOut | null>(null);

  const current = queue.resource.status === 'ready'
    ? queue.resource.data.queue.find((row) => row.submission_id === selected) ?? null
    : null;

  async function submitReview(): Promise<void> {
    if (selected === null) return;
    setBusy(true);
    setError(null);
    setNote(null);
    try {
      const row = await http.post<ReviewOut>(`/work/submissions/${selected}/review`, {
        verdict,
        score: score === '' ? null : Number(score),
        notes: notes.trim() || null,
        is_override: isOverride,
        reason: isOverride ? reason.trim() : null,
      });
      setReviewed(row);
      setSelected(null);
      setNotes('');
      setReason('');
      setIsOverride(false);
      queue.reload();
      setNote(`Submission ${row.submission_id} reviewed: ${row.verdict}.`);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not record that review.');
    } finally {
      setBusy(false);
    }
  }

  async function reviewPractical(id: number, passed: boolean): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      await http.post<PracticalReviewOut>(`/verification/practical/submissions/${id}/review`, {
        score: passed ? Number(score) || 90 : 0,
        passed,
        notes: notes.trim() || null,
      });
      setNote(`Practical submission ${id} ${passed ? 'passed' : 'failed'}.`);
      practical.reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not record that review.');
    } finally {
      setBusy(false);
    }
  }

  async function saveStandard(): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      const row = await http.put<StandardOut>(`/work/projects/${projectSlug.trim()}/quality-standard`, {
        name: standardName.trim(),
        instructions_md: instructions,
        pass_threshold: Number(threshold),
        rules: JSON.parse(rules || '{}') as Record<string, unknown>,
      });
      setStandard(row);
      setNote('Quality standard saved. It applies to reviews from now on.');
    } catch (err) {
      if (err instanceof SyntaxError) setError('Rules must be valid JSON.');
      else setError(err instanceof ApiError ? err.message : 'Could not save the standard.');
    } finally {
      setBusy(false);
    }
  }

  async function override(): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      const row = await http.post<OverrideOut>(
        `/verification/records/${Number(overrideUser)}/${Number(overrideSkill)}/override`,
        { to_status: overrideStatus, reason: overrideReason.trim() },
      );
      setOverrideResult(row);
      setNote('Verification overridden; the reason is in the audit trail.');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not override that record.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="nv-stack">
      <h1 className="nv-h1">Review</h1>
      <p className="nv-muted">
        Gold tasks are mixed into live work to check the reviewer, not the student. An override needs a
        reason; it is stored with your account.
      </p>

      {error ? <p className="nv-error">{error}</p> : null}
      {note ? <p className="nv-muted">{note}</p> : null}

      <section className="nv-card">
        <h2 className="nv-h2">Work queue</h2>
        {queue.resource.status === 'loading' ? <p className="nv-muted">Loading…</p> : null}
        {queue.resource.status === 'error' ? <p className="nv-error">{queue.resource.message}</p> : null}
        {queue.resource.status === 'ready' ? (
          <table className="nv-table">
            <thead>
              <tr>
                <th>Submission</th>
                <th>Student</th>
                <th>Project</th>
                <th>Submitted</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {queue.resource.data.queue.map((row) => (
                <tr key={row.submission_id}>
                  <td>
                    #{row.submission_id} · {row.assignment_title}
                    {row.is_gold ? <span className="nv-tag" data-tone="warn">gold</span> : null}
                  </td>
                  <td>
                    {row.student.name ?? `#${row.student.id}`}
                    <div className="nv-muted">{row.student.email}</div>
                  </td>
                  <td>{row.project.title}</td>
                  <td>{when(row.submitted_at)}</td>
                  <td>
                    <button className="nv-button nv-button--ghost" type="button" onClick={() => setSelected(row.submission_id)}>
                      Review
                    </button>
                  </td>
                </tr>
              ))}
              {queue.resource.data.queue.length === 0 ? (
                <tr>
                  <td colSpan={5} className="nv-muted">The queue is empty.</td>
                </tr>
              ) : null}
            </tbody>
          </table>
        ) : null}
      </section>

      {current ? (
        <section className="nv-card">
          <h2 className="nv-h2">Submission #{current.submission_id}</h2>
          <p className="nv-muted">
            {current.assignment_title} · {current.student.name ?? current.student.email}
          </p>
          <pre className="nv-code nv-pre">{JSON.stringify(current.payload, null, 2)}</pre>

          <div className="nv-grid">
            <div>
              <label className="nv-label" htmlFor="review-verdict">Verdict</label>
              <select className="nv-select" id="review-verdict" value={verdict} onChange={(e) => setVerdict(e.target.value)}>
                {VERDICTS.map((option) => (
                  <option key={option} value={option}>{option}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="nv-label" htmlFor="review-score">Score (0–100)</label>
              <input className="nv-input" id="review-score" type="number" value={score} onChange={(e) => setScore(e.target.value)} />
            </div>
          </div>
          <div>
            <label className="nv-label" htmlFor="review-notes">Notes to the student</label>
            <textarea className="nv-textarea" id="review-notes" value={notes} onChange={(e) => setNotes(e.target.value)} />
          </div>
          <label className="nv-check">
            <input type="checkbox" checked={isOverride} onChange={(e) => setIsOverride(e.target.checked)} />
            This is an override of the automatic result
          </label>
          {isOverride ? (
            <div>
              <label className="nv-label" htmlFor="review-reason">Override reason (required)</label>
              <input className="nv-input" id="review-reason" value={reason} onChange={(e) => setReason(e.target.value)} />
            </div>
          ) : null}
          <div className="nv-row">
            <button className="nv-button" disabled={busy || (isOverride && reason.trim().length < 3)} type="button" onClick={() => void submitReview()}>
              {busy ? 'Saving…' : 'Record review'}
            </button>
            <button className="nv-button nv-button--ghost" type="button" onClick={() => setSelected(null)}>
              Cancel
            </button>
          </div>
        </section>
      ) : null}

      {reviewed ? (
        <p className="nv-muted">
          Last review: submission {reviewed.submission_id} · {reviewed.verdict} · score{' '}
          {reviewed.score ?? '—'}
          {reviewed.gold_correct === null ? '' : ` · gold ${reviewed.gold_correct ? 'correct' : 'incorrect'}`}
        </p>
      ) : null}

      <section className="nv-card">
        <h2 className="nv-h2">Practical submissions</h2>
        {practical.resource.status === 'loading' ? <p className="nv-muted">Loading…</p> : null}
        {practical.resource.status === 'error' ? <p className="nv-muted">{practical.resource.message}</p> : null}
        {practical.resource.status === 'ready' ? (
          <table className="nv-table">
            <thead>
              <tr>
                <th>Submission</th>
                <th>Task</th>
                <th>Student</th>
                <th>Submitted</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {practical.resource.data.submissions.map((row) => (
                <tr key={row.id}>
                  <td>#{row.id}</td>
                  <td>#{row.practical_task_id}</td>
                  <td>#{row.user_id}</td>
                  <td>{when(row.submitted_at)}</td>
                  <td>
                    <div className="nv-row">
                      <button className="nv-button" type="button" disabled={busy} onClick={() => void reviewPractical(row.id, true)}>
                        Pass
                      </button>
                      <button className="nv-button nv-button--danger" type="button" disabled={busy} onClick={() => void reviewPractical(row.id, false)}>
                        Fail
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
              {practical.resource.data.submissions.length === 0 ? (
                <tr>
                  <td colSpan={5} className="nv-muted">No practical submission waiting.</td>
                </tr>
              ) : null}
            </tbody>
          </table>
        ) : null}
      </section>

      <section className="nv-card">
        <h2 className="nv-h2">Quality standard</h2>
        <div className="nv-grid">
          <div>
            <label className="nv-label" htmlFor="standard-project">Project slug</label>
            <input className="nv-input" id="standard-project" value={projectSlug} onChange={(e) => setProjectSlug(e.target.value)} />
          </div>
          <div>
            <label className="nv-label" htmlFor="standard-name">Name</label>
            <input className="nv-input" id="standard-name" value={standardName} onChange={(e) => setStandardName(e.target.value)} />
          </div>
          <div>
            <label className="nv-label" htmlFor="standard-threshold">Pass threshold</label>
            <input className="nv-input" id="standard-threshold" type="number" value={threshold} onChange={(e) => setThreshold(e.target.value)} />
          </div>
        </div>
        <div>
          <label className="nv-label" htmlFor="standard-instructions">Instructions (markdown)</label>
          <textarea className="nv-textarea" id="standard-instructions" value={instructions} onChange={(e) => setInstructions(e.target.value)} />
        </div>
        <div>
          <label className="nv-label" htmlFor="standard-rules">Rules (JSON)</label>
          <textarea className="nv-textarea" id="standard-rules" value={rules} onChange={(e) => setRules(e.target.value)} />
        </div>
        {standard ? (
          <p className="nv-muted">
            Saved: {standard.name} · pass at {standard.pass_threshold}%
          </p>
        ) : null}
        <button className="nv-button" disabled={busy || !projectSlug.trim()} type="button" onClick={() => void saveStandard()}>
          Save standard
        </button>
      </section>

      <section className="nv-card">
        <h2 className="nv-h2">Verification override</h2>
        <p className="nv-muted">
          Use only with evidence in hand. The student sees the new status; the transcript keeps the
          history.
        </p>
        <div className="nv-grid">
          <div>
            <label className="nv-label" htmlFor="override-user">Student user id</label>
            <input className="nv-input" id="override-user" value={overrideUser} onChange={(e) => setOverrideUser(e.target.value)} />
          </div>
          <div>
            <label className="nv-label" htmlFor="override-skill">Skill id</label>
            <input className="nv-input" id="override-skill" value={overrideSkill} onChange={(e) => setOverrideSkill(e.target.value)} />
          </div>
          <div>
            <label className="nv-label" htmlFor="override-status">New status</label>
            <select className="nv-select" id="override-status" value={overrideStatus} onChange={(e) => setOverrideStatus(e.target.value)}>
              {['verified', 'at_risk', 'suspended', 'unverified'].map((option) => (
                <option key={option} value={option}>{option}</option>
              ))}
            </select>
          </div>
        </div>
        <div>
          <label className="nv-label" htmlFor="override-reason">Reason (required)</label>
          <input className="nv-input" id="override-reason" value={overrideReason} onChange={(e) => setOverrideReason(e.target.value)} />
        </div>
        {overrideResult ? (
          <p className="nv-muted">
            User {overrideResult.user_id} · skill {overrideResult.skill_id} is now {overrideResult.status} (event #{overrideResult.event_id}).
          </p>
        ) : null}
        <button
          className="nv-button nv-button--danger"
          disabled={busy || !overrideUser || !overrideSkill || overrideReason.trim().length < 3}
          type="button"
          onClick={() => void override()}
        >
          Override verification
        </button>
      </section>
    </div>
  );
}
