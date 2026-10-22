/**
 * Opportunities (C4).
 *
 * Create and edit a brief, publish it, and see who qualifies — with the same
 * explanation the student sees. Requirements are edited as JSON because they are
 * a list of typed rules, not a fixed form; a broken shape is rejected by the API
 * and shown here as an error instead of being half-saved.
 */
import type {
  CandidateListOut,
  OpportunityAdminListOut,
  OpportunityApplicationsOut,
} from '@nelavista/api-client';
import * as React from 'react';

import { ApiError, http } from '../lib/http';
import { useResource } from '../lib/resource';
import { money } from '../lib/format';

type Created = { id: number; slug: string; status: string };

const REQUIREMENT_EXAMPLE = JSON.stringify(
  [{ kind: 'skill', skill_id: 1, is_mandatory: true, description: 'Annotation skill' }],
  null,
  2,
);

export function Opportunities(): JSX.Element {
  const list = useResource<OpportunityAdminListOut>('/opportunities/admin/all');
  const [slug, setSlug] = React.useState('');
  const [title, setTitle] = React.useState('');
  const [type, setType] = React.useState('managed');
  const [description, setDescription] = React.useState('');
  const [client, setClient] = React.useState('');
  const [headcount, setHeadcount] = React.useState('5');
  const [currency, setCurrency] = React.useState('USD');
  const [rate, setRate] = React.useState('1.50');
  const [requirements, setRequirements] = React.useState(REQUIREMENT_EXAMPLE);
  const [selected, setSelected] = React.useState<string | null>(null);
  const [candidates, setCandidates] = React.useState<CandidateListOut | null>(null);
  const [applications, setApplications] = React.useState<OpportunityApplicationsOut | null>(null);
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [note, setNote] = React.useState<string | null>(null);

  async function create(): Promise<void> {
    setBusy(true);
    setError(null);
    setNote(null);
    try {
      const parsed = requirements.trim() ? (JSON.parse(requirements) as unknown[]) : [];
      const created = await http.post<Created>('/opportunities', {
        type,
        slug: slug.trim(),
        title: title.trim(),
        description,
        client_name: client.trim() || null,
        headcount: Number(headcount) || null,
        currency: currency.trim().toUpperCase() || null,
        rate_minor: rate.trim() ? Math.round(Number(rate) * 100) : null,
        requirements: parsed,
      });
      setNote(`Created ${created.slug} as ${created.status}. Publish it when the brief is ready.`);
      setSlug('');
      setTitle('');
      list.reload();
    } catch (err) {
      if (err instanceof SyntaxError) setError('Requirements must be valid JSON.');
      else setError(err instanceof ApiError ? err.message : 'Could not create the opportunity.');
    } finally {
      setBusy(false);
    }
  }

  async function open(next: string): Promise<void> {
    setSelected(next);
    setCandidates(null);
    setApplications(null);
    setError(null);
    try {
      const [candidateRows, applicationRows] = await Promise.all([
        http.get<CandidateListOut>(`/opportunities/${next}/candidates`),
        http.get<OpportunityApplicationsOut>(`/opportunities/${next}/applications`),
      ]);
      setCandidates(candidateRows);
      setApplications(applicationRows);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not load that opportunity.');
    }
  }

  async function setStatus(nextSlug: string, status: string): Promise<void> {
    setError(null);
    try {
      await http.patch(`/opportunities/${nextSlug}`, { status });
      list.reload();
      setNote(`${nextSlug} is now ${status}.`);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not change the status.');
    }
  }

  return (
    <div className="nv-stack">
      <h1 className="nv-h1">Opportunities</h1>
      <p className="nv-muted">
        Managed work is invitation-only; external listings can be applied to. Publishing a managed
        opportunity requires a currency and a rate.
      </p>

      <section className="nv-card">
        <h2 className="nv-h2">New opportunity</h2>
        <div className="nv-grid">
          <div>
            <label className="nv-label" htmlFor="opp-slug">Slug</label>
            <input className="nv-input" id="opp-slug" value={slug} onChange={(e) => setSlug(e.target.value)} />
          </div>
          <div>
            <label className="nv-label" htmlFor="opp-title">Title</label>
            <input className="nv-input" id="opp-title" value={title} onChange={(e) => setTitle(e.target.value)} />
          </div>
          <div>
            <label className="nv-label" htmlFor="opp-type">Type</label>
            <select className="nv-select" id="opp-type" value={type} onChange={(e) => setType(e.target.value)}>
              <option value="managed">Managed</option>
              <option value="external">External</option>
            </select>
          </div>
          <div>
            <label className="nv-label" htmlFor="opp-client">Client name</label>
            <input className="nv-input" id="opp-client" value={client} onChange={(e) => setClient(e.target.value)} />
          </div>
          <div>
            <label className="nv-label" htmlFor="opp-headcount">Headcount</label>
            <input className="nv-input" id="opp-headcount" type="number" value={headcount} onChange={(e) => setHeadcount(e.target.value)} />
          </div>
          <div>
            <label className="nv-label" htmlFor="opp-currency">Currency</label>
            <input className="nv-input" id="opp-currency" maxLength={3} value={currency} onChange={(e) => setCurrency(e.target.value)} />
          </div>
          <div>
            <label className="nv-label" htmlFor="opp-rate">Rate per task (major units)</label>
            <input className="nv-input" id="opp-rate" type="number" step="0.01" value={rate} onChange={(e) => setRate(e.target.value)} />
          </div>
        </div>
        <div>
          <label className="nv-label" htmlFor="opp-description">Description</label>
          <textarea className="nv-textarea" id="opp-description" value={description} onChange={(e) => setDescription(e.target.value)} />
        </div>
        <div>
          <label className="nv-label" htmlFor="opp-requirements">Requirements (JSON array)</label>
          <textarea className="nv-textarea" id="opp-requirements" value={requirements} onChange={(e) => setRequirements(e.target.value)} />
        </div>
        {error ? <p className="nv-error">{error}</p> : null}
        {note ? <p className="nv-muted">{note}</p> : null}
        <button className="nv-button" disabled={busy || slug.trim().length < 2 || title.trim().length < 2} type="button" onClick={() => void create()}>
          {busy ? 'Saving…' : 'Create draft'}
        </button>
      </section>

      <section className="nv-card">
        <h2 className="nv-h2">All opportunities</h2>
        {list.resource.status === 'loading' ? <p className="nv-muted">Loading…</p> : null}
        {list.resource.status === 'error' ? <p className="nv-error">{list.resource.message}</p> : null}
        {list.resource.status === 'ready' ? (
          <table className="nv-table">
            <thead>
              <tr>
                <th>Opportunity</th>
                <th>Type</th>
                <th>Status</th>
                <th>Rate</th>
                <th>Places</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {list.resource.data.opportunities.map((row) => (
                <tr key={row.id}>
                  <td>
                    <strong>{row.title}</strong>
                    <div className="nv-muted">{row.slug}{row.client_name ? ` · ${row.client_name}` : ''}</div>
                  </td>
                  <td>{row.type}</td>
                  <td>
                    <span className="nv-tag" data-tone={row.status === 'open' ? 'ok' : row.status === 'draft' ? 'warn' : 'bad'}>
                      {row.status}
                    </span>
                  </td>
                  <td>{money(row.rate_minor, row.currency)}</td>
                  <td>{row.headcount ?? '—'}</td>
                  <td>
                    <div className="nv-row">
                      <button className="nv-button nv-button--ghost" type="button" onClick={() => void open(row.slug)}>
                        Candidates
                      </button>
                      {row.status !== 'open' ? (
                        <button className="nv-button" type="button" onClick={() => void setStatus(row.slug, 'open')}>
                          Publish
                        </button>
                      ) : (
                        <button className="nv-button nv-button--ghost" type="button" onClick={() => void setStatus(row.slug, 'closed')}>
                          Close
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
              {list.resource.data.opportunities.length === 0 ? (
                <tr>
                  <td colSpan={6} className="nv-muted">No opportunity yet.</td>
                </tr>
              ) : null}
            </tbody>
          </table>
        ) : null}
      </section>

      {selected ? (
        <section className="nv-card">
          <h2 className="nv-h2">Candidates for {selected}</h2>
          {candidates ? (
            <p className="nv-muted">
              {candidates.eligible_count} of {candidates.candidates.length} qualify. Every row carries the
              reason.
            </p>
          ) : (
            <p className="nv-muted">Loading…</p>
          )}
          {candidates ? (
            <table className="nv-table">
              <thead>
                <tr>
                  <th>Student</th>
                  <th>Verdict</th>
                  <th>Score</th>
                  <th>Why / what is missing</th>
                </tr>
              </thead>
              <tbody>
                {candidates.candidates.map((row) => (
                  <tr key={row.user_id}>
                    <td>
                      {row.student?.name ?? `#${row.user_id}`}
                      <div className="nv-muted">{row.student?.email ?? ''}</div>
                    </td>
                    <td>
                      <span className="nv-tag" data-tone={row.eligible ? 'ok' : row.blocked ? 'bad' : 'warn'}>
                        {row.eligible ? 'eligible' : row.blocked ? 'blocked' : 'not yet'}
                      </span>
                    </td>
                    <td>{row.score}</td>
                    <td>
                      {row.qualifies_because.map((reason) => (
                        <div key={reason}>✓ {reason}</div>
                      ))}
                      {row.next_steps.map((step) => (
                        <div key={step.requirement_id} className="nv-muted">→ {step.detail}</div>
                      ))}
                      {row.blocked_reason ? <div className="nv-error">{row.blocked_reason}</div> : null}
                    </td>
                  </tr>
                ))}
                {candidates.candidates.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="nv-muted">No student has matching evidence yet.</td>
                  </tr>
                ) : null}
              </tbody>
            </table>
          ) : null}

          {applications ? (
            <>
              <h3 className="nv-h2">Applications</h3>
              <table className="nv-table">
                <thead>
                  <tr>
                    <th>User</th>
                    <th>Status</th>
                    <th>Note</th>
                  </tr>
                </thead>
                <tbody>
                  {applications.applications.map((row) => (
                    <tr key={row.id}>
                      <td>#{row.user_id}</td>
                      <td>{row.status}</td>
                      <td>{row.note ?? '—'}</td>
                    </tr>
                  ))}
                  {applications.applications.length === 0 ? (
                    <tr>
                      <td colSpan={3} className="nv-muted">No application yet.</td>
                    </tr>
                  ) : null}
                </tbody>
              </table>
            </>
          ) : null}
          <p className="nv-muted">Created rows carry their date; invitations are sent from Projects &amp; cohorts.</p>
        </section>
      ) : null}
    </div>
  );
}
