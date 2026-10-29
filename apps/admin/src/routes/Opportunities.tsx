/**
 * Opportunities (C4).
 *
 * Create and edit a brief, publish it, and see who qualifies  -  with the same
 * explanation the student sees. Requirements are edited as JSON because they are
 * a list of typed rules, not a fixed form; a broken shape is rejected by the API
 * and shown here as an error instead of being half-saved.
 */
import type {
  CandidateListOut,
  OpportunityAdminListOut,
  OpportunityApplicationsOut,
} from '@nelavista/api-client';
import { Badge, Banner, EmptyState, ErrorNote, ErrorState, PageHeader, Panel, Skeleton } from '@nelavista/ui';
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

  async function setApplicationStatus(applicationId: number, status: string): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      await http.post(`/opportunities/applications/${applicationId}/status`, { status });
      setNote(`Application #${applicationId} is now ${status}.`);
      if (selected) await open(selected);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not change the application status.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="nv-stack nv-stack--loose">
      <PageHeader
        eyebrow="Work"
        title="Opportunities"
        description="Managed work is invitation-only; external listings can be applied to. Publishing a managed opportunity requires a currency and a rate."
      />

      <Panel title="New opportunity">
        <div className="nv-stack">
          <div className="nv-grid">
            <div>
              <label className="nv-label" htmlFor="opp-slug">
                Slug
              </label>
              <input
                className="nv-input"
                id="opp-slug"
                value={slug}
                onChange={(e) => setSlug(e.target.value)}
              />
            </div>
            <div>
              <label className="nv-label" htmlFor="opp-title">
                Title
              </label>
              <input
                className="nv-input"
                id="opp-title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />
            </div>
            <div>
              <label className="nv-label" htmlFor="opp-type">
                Type
              </label>
              <select
                className="nv-select"
                id="opp-type"
                value={type}
                onChange={(e) => setType(e.target.value)}
              >
                <option value="managed">Managed</option>
                <option value="external">External</option>
              </select>
            </div>
            <div>
              <label className="nv-label" htmlFor="opp-client">
                Client name
              </label>
              <input
                className="nv-input"
                id="opp-client"
                value={client}
                onChange={(e) => setClient(e.target.value)}
              />
            </div>
            <div>
              <label className="nv-label" htmlFor="opp-headcount">
                Headcount
              </label>
              <input
                className="nv-input"
                id="opp-headcount"
                type="number"
                value={headcount}
                onChange={(e) => setHeadcount(e.target.value)}
              />
            </div>
            <div>
              <label className="nv-label" htmlFor="opp-currency">
                Currency
              </label>
              <input
                className="nv-input"
                id="opp-currency"
                maxLength={3}
                value={currency}
                onChange={(e) => setCurrency(e.target.value)}
              />
            </div>
            <div>
              <label className="nv-label" htmlFor="opp-rate">
                Rate per task (major units)
              </label>
              <input
                className="nv-input"
                id="opp-rate"
                type="number"
                step="0.01"
                value={rate}
                onChange={(e) => setRate(e.target.value)}
              />
            </div>
          </div>
          <div>
            <label className="nv-label" htmlFor="opp-description">
              Description
            </label>
            <textarea
              className="nv-textarea"
              id="opp-description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>
          <div>
            <label className="nv-label" htmlFor="opp-requirements">
              Requirements (JSON array)
            </label>
            <textarea
              className="nv-textarea"
              id="opp-requirements"
              value={requirements}
              onChange={(e) => setRequirements(e.target.value)}
            />
          </div>
          <ErrorNote message={error} />
          {note ? <Banner tone="success">{note}</Banner> : null}
          <button
            className="nv-button"
            disabled={busy || slug.trim().length < 2 || title.trim().length < 2}
            type="button"
            onClick={() => void create()}
          >
            {busy ? 'Saving…' : 'Create draft'}
          </button>
        </div>
      </Panel>

      <Panel title="All opportunities">
        {list.resource.status === 'loading' ? <Skeleton lines={5} /> : null}
        {list.resource.status === 'error' ? (
          <ErrorState title="Opportunities did not load" body={list.resource.message} />
        ) : null}
        {list.resource.status === 'ready' && list.resource.data.opportunities.length === 0 ? (
          <EmptyState
            title="No opportunity yet"
            body="Create a draft above. It stays hidden from students until you publish it."
          />
        ) : null}
        {list.resource.status === 'ready' && list.resource.data.opportunities.length > 0 ? (
          <div className="nv-table-wrap">
            <table className="nv-table">
              <thead>
                <tr>
                  <th scope="col">Opportunity</th>
                  <th scope="col">Type</th>
                  <th scope="col">Status</th>
                  <th scope="col">Rate</th>
                  <th scope="col">Places</th>
                  <th scope="col">Actions</th>
                </tr>
              </thead>
              <tbody>
                {list.resource.data.opportunities.map((row) => (
                  <tr key={row.id}>
                    <td>
                      <strong>{row.title}</strong>
                      <div className="nv-muted">
                        {row.slug}
                        {row.client_name ? ` · ${row.client_name}` : ''}
                      </div>
                    </td>
                    <td>{row.type}</td>
                    <td>
                      <Badge
                        tone={
                          row.status === 'open' ? 'success' : row.status === 'draft' ? 'warning' : 'danger'
                        }
                      >
                        {row.status}
                      </Badge>
                    </td>
                    <td>{money(row.rate_minor, row.currency)}</td>
                    <td>{row.headcount ?? 'Not set'}</td>
                    <td>
                      <div className="nv-row">
                        <button
                          className="nv-button nv-button--ghost"
                          type="button"
                          onClick={() => void open(row.slug)}
                        >
                          Candidates
                        </button>
                        {row.status !== 'open' ? (
                          <button
                            className="nv-button"
                            type="button"
                            onClick={() => void setStatus(row.slug, 'open')}
                          >
                            Publish
                          </button>
                        ) : (
                          <button
                            className="nv-button nv-button--ghost"
                            type="button"
                            onClick={() => void setStatus(row.slug, 'closed')}
                          >
                            Close
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : null}
      </Panel>

      {selected ? (
        <Panel title={`Candidates for ${selected}`}>
          {candidates ? (
            <p className="nv-muted">
              {candidates.eligible_count} of {candidates.candidates.length} qualify. Every row carries the
              reason.
            </p>
          ) : (
            <Skeleton lines={3} />
          )}
          {candidates ? (
            candidates.candidates.length === 0 ? (
              <EmptyState
                title="No matching evidence yet"
                body="No student currently has the evidence this brief asks for."
              />
            ) : (
              <div className="nv-table-wrap">
                <table className="nv-table">
                  <thead>
                    <tr>
                      <th scope="col">Student</th>
                      <th scope="col">Verdict</th>
                      <th scope="col">Score</th>
                      <th scope="col">Why / what is missing</th>
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
                          <Badge tone={row.eligible ? 'success' : row.blocked ? 'danger' : 'warning'}>
                            {row.eligible ? 'eligible' : row.blocked ? 'blocked' : 'not yet'}
                          </Badge>
                        </td>
                        <td>{row.score}</td>
                        <td>
                          {row.qualifies_because.map((reason) => (
                            <div key={reason}>Qualifies: {reason}</div>
                          ))}
                          {row.next_steps.map((step) => (
                            <div key={step.requirement_id} className="nv-muted">
                              Next: {step.detail}
                            </div>
                          ))}
                          {row.blocked_reason ? <div className="nv-error">{row.blocked_reason}</div> : null}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )
          ) : null}

          {applications ? (
            <>
              <h3 className="nv-h2">Applications</h3>
              {applications.applications.length === 0 ? (
                <EmptyState
                  title="No application yet"
                  body="Applications appear here when an external listing is open."
                />
              ) : (
                <div className="nv-table-wrap">
                  <table className="nv-table">
                    <thead>
                      <tr>
                        <th scope="col">User</th>
                        <th scope="col">Status</th>
                        <th scope="col">Note</th>
                      </tr>
                    </thead>
                    <tbody>
                      {applications.applications.map((row) => (
                        <tr key={row.id}>
                          <td>#{row.user_id}</td>
                          <td>
                            <select
                              aria-label={`Status for application #${row.id}`}
                              className="nv-select"
                              defaultValue={row.status}
                              disabled={busy}
                              onChange={(event) => {
                                if (event.target.value !== row.status) {
                                  void setApplicationStatus(row.id, event.target.value);
                                }
                              }}
                            >
                              {['interested', 'applied', 'shortlisted', 'withdrawn', 'rejected'].map(
                                (status) => (
                                  <option key={status} value={status}>
                                    {status}
                                  </option>
                                ),
                              )}
                            </select>
                          </td>
                          <td>{row.note ?? 'Not set'}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </>
          ) : null}
          <p className="nv-muted">
            Created rows carry their date; invitations are sent from Projects &amp; cohorts.
          </p>
        </Panel>
      ) : null}
    </div>
  );
}
