/**
 * Projects and cohorts (C4).
 *
 * Managed work is delivered in cohorts: invite students, remove one with a
 * reason, see replacement candidates who already qualify. Removing a student
 * never deletes their completed work or its earnings; the reason is recorded.
 */
import type {
  AssignOut,
  CohortOut,
  CohortWriteOut,
  ProjectListOut,
  ProjectOut,
  ReplacementListOut,
} from '@nelavista/api-client';
import * as React from 'react';

import { ApiError, http } from '../lib/http';
import { useResource } from '../lib/resource';
import { when } from '../lib/format';

export function Projects(): JSX.Element {
  const list = useResource<ProjectListOut>('/work/projects');
  const [projectSlug, setProjectSlug] = React.useState<string | null>(null);
  const [cohortId, setCohortId] = React.useState<number | null>(null);
  const [project, setProject] = React.useState<ProjectOut | null>(null);
  const [cohort, setCohort] = React.useState<CohortOut | null>(null);
  const [replacements, setReplacements] = React.useState<ReplacementListOut | null>(null);

  const [opportunitySlug, setOpportunitySlug] = React.useState('');
  const [newProjectSlug, setNewProjectSlug] = React.useState('');
  const [newProjectTitle, setNewProjectTitle] = React.useState('');
  const [cohortName, setCohortName] = React.useState('');
  const [cohortCapacity, setCohortCapacity] = React.useState('10');
  const [inviteIds, setInviteIds] = React.useState('');
  const [removeId, setRemoveId] = React.useState('');
  const [removeReason, setRemoveReason] = React.useState('');
  const [assignUser, setAssignUser] = React.useState('');
  const [assignTitle, setAssignTitle] = React.useState('');
  const [assignTemplate, setAssignTemplate] = React.useState('');
  const [assignDue, setAssignDue] = React.useState('');
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [note, setNote] = React.useState<string | null>(null);

  async function openProject(slug: string): Promise<void> {
    setProjectSlug(slug);
    setCohortId(null);
    setCohort(null);
    setReplacements(null);
    setError(null);
    try {
      setProject(await http.get<ProjectOut>(`/work/projects/${slug}`));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not load that project.');
    }
  }

  async function openCohort(id: number): Promise<void> {
    setCohortId(id);
    setReplacements(null);
    setError(null);
    try {
      const [detail, replacementRows] = await Promise.all([
        http.get<CohortOut>(`/work/cohorts/${id}`),
        http.get<ReplacementListOut>(`/work/cohorts/${id}/replacements`),
      ]);
      setCohort(detail);
      setReplacements(replacementRows);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not load that cohort.');
    }
  }

  async function createProject(): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      await http.post('/work/projects', {
        opportunity_slug: opportunitySlug.trim(),
        slug: newProjectSlug.trim(),
        title: newProjectTitle.trim(),
      });
      setNote('Project created.');
      list.reload();
      await openProject(newProjectSlug.trim());
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not create the project.');
    } finally {
      setBusy(false);
    }
  }

  async function createCohort(): Promise<void> {
    if (!projectSlug) return;
    setBusy(true);
    setError(null);
    try {
      const created = await http.post<CohortWriteOut>(`/work/projects/${projectSlug}/cohorts`, {
        name: cohortName.trim(),
        capacity: Number(cohortCapacity) || null,
      });
      setNote(`Cohort ${created.name} created.`);
      await openProject(projectSlug);
      await openCohort(created.id);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not create the cohort.');
    } finally {
      setBusy(false);
    }
  }

  async function invite(): Promise<void> {
    if (!cohortId) return;
    const ids = inviteIds
      .split(',')
      .map((value) => Number(value.trim()))
      .filter((value) => Number.isInteger(value) && value > 0);
    if (ids.length === 0) {
      setError('Enter at least one user id.');
      return;
    }
    setBusy(true);
    setError(null);
    try {
      await http.post(`/work/cohorts/${cohortId}/invites`, { user_ids: ids });
      setNote(`Invited ${ids.length} student(s).`);
      setInviteIds('');
      await openCohort(cohortId);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not send the invitations.');
    } finally {
      setBusy(false);
    }
  }

  async function remove(): Promise<void> {
    if (!cohortId) return;
    setBusy(true);
    setError(null);
    try {
      await http.post(`/work/cohorts/${cohortId}/remove`, {
        member_id: Number(removeId),
        reason: removeReason.trim(),
      });
      setNote('Member removed; the reason is in the audit trail.');
      setRemoveId('');
      setRemoveReason('');
      await openCohort(cohortId);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not remove that member.');
    } finally {
      setBusy(false);
    }
  }

  async function assign(): Promise<void> {
    if (!projectSlug) return;
    setBusy(true);
    setError(null);
    try {
      await http.post<AssignOut>(`/work/projects/${projectSlug}/assignments`, {
        user_id: Number(assignUser),
        title: assignTitle.trim(),
        template_id: assignTemplate.trim() ? Number(assignTemplate) : null,
        due_at: assignDue ? new Date(assignDue).toISOString() : null,
      });
      setNote('Assignment created.');
      setAssignUser('');
      setAssignTitle('');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not assign that task.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="nv-stack">
      <h1 className="nv-h1">Projects &amp; cohorts</h1>
      <p className="nv-muted">
        Invitations are how managed work starts. A replacement must already qualify; the list shows only
        students the engine considers eligible.
      </p>

      <section className="nv-card">
        <h2 className="nv-h2">New project</h2>
        <div className="nv-grid">
          <div>
            <label className="nv-label" htmlFor="proj-opportunity">Opportunity slug</label>
            <input className="nv-input" id="proj-opportunity" value={opportunitySlug} onChange={(e) => setOpportunitySlug(e.target.value)} />
          </div>
          <div>
            <label className="nv-label" htmlFor="proj-slug">Project slug</label>
            <input className="nv-input" id="proj-slug" value={newProjectSlug} onChange={(e) => setNewProjectSlug(e.target.value)} />
          </div>
          <div>
            <label className="nv-label" htmlFor="proj-title">Title</label>
            <input className="nv-input" id="proj-title" value={newProjectTitle} onChange={(e) => setNewProjectTitle(e.target.value)} />
          </div>
        </div>
        <button className="nv-button" disabled={busy || !opportunitySlug.trim()} type="button" onClick={() => void createProject()}>
          Create project
        </button>
      </section>

      {error ? <p className="nv-error">{error}</p> : null}
      {note ? <p className="nv-muted">{note}</p> : null}

      <section className="nv-card">
        <h2 className="nv-h2">Projects</h2>
        {list.resource.status === 'loading' ? <p className="nv-muted">Loading…</p> : null}
        {list.resource.status === 'error' ? <p className="nv-error">{list.resource.message}</p> : null}
        {list.resource.status === 'ready' ? (
          <table className="nv-table">
            <thead>
              <tr>
                <th>Project</th>
                <th>Status</th>
                <th>Starts</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {list.resource.data.projects.map((row) => (
                <tr key={row.id}>
                  <td>
                    <strong>{row.title}</strong>
                    <div className="nv-muted">{row.slug}</div>
                  </td>
                  <td>{row.status}</td>
                  <td>{row.starts_on ?? '—'}</td>
                  <td>
                    <button className="nv-button nv-button--ghost" type="button" onClick={() => void openProject(row.slug)}>
                      Open
                    </button>
                  </td>
                </tr>
              ))}
              {list.resource.data.projects.length === 0 ? (
                <tr>
                  <td colSpan={4} className="nv-muted">No project yet.</td>
                </tr>
              ) : null}
            </tbody>
          </table>
        ) : null}
      </section>

      {project ? (
        <section className="nv-card">
          <h2 className="nv-h2">{project.title}</h2>
          <p className="nv-muted">
            {project.slug} · {project.status} · {Object.entries(project.assignment_counts).map(([key, value]) => `${key}: ${value}`).join(' · ') || 'no assignments'}
          </p>

          <div className="nv-row">
            <div>
              <label className="nv-label" htmlFor="cohort-name">Cohort name</label>
              <input className="nv-input" id="cohort-name" value={cohortName} onChange={(e) => setCohortName(e.target.value)} />
            </div>
            <div>
              <label className="nv-label" htmlFor="cohort-capacity">Capacity</label>
              <input className="nv-input" id="cohort-capacity" type="number" value={cohortCapacity} onChange={(e) => setCohortCapacity(e.target.value)} />
            </div>
            <button className="nv-button" disabled={busy || cohortName.trim().length < 2} type="button" onClick={() => void createCohort()}>
              Create cohort
            </button>
          </div>

          <table className="nv-table">
            <thead>
              <tr>
                <th>Cohort</th>
                <th>Seats</th>
                <th>Status</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {project.cohorts.map((row) => (
                <tr key={row.id}>
                  <td>{row.name}</td>
                  <td>{row.seats_used}{row.capacity ? ` / ${row.capacity}` : ''}</td>
                  <td>{row.status}</td>
                  <td>
                    <button className="nv-button nv-button--ghost" type="button" onClick={() => void openCohort(row.id)}>
                      Members
                    </button>
                  </td>
                </tr>
              ))}
              {project.cohorts.length === 0 ? (
                <tr>
                  <td colSpan={4} className="nv-muted">No cohort yet.</td>
                </tr>
              ) : null}
            </tbody>
          </table>

          <h3 className="nv-h2">Assign a task</h3>
          <div className="nv-grid">
            <div>
              <label className="nv-label" htmlFor="assign-user">Student user id</label>
              <input className="nv-input" id="assign-user" value={assignUser} onChange={(e) => setAssignUser(e.target.value)} />
            </div>
            <div>
              <label className="nv-label" htmlFor="assign-title">Title</label>
              <input className="nv-input" id="assign-title" value={assignTitle} onChange={(e) => setAssignTitle(e.target.value)} />
            </div>
            <div>
              <label className="nv-label" htmlFor="assign-template">Template id (optional)</label>
              <input className="nv-input" id="assign-template" value={assignTemplate} onChange={(e) => setAssignTemplate(e.target.value)} />
            </div>
            <div>
              <label className="nv-label" htmlFor="assign-due">Due at (optional)</label>
              <input className="nv-input" id="assign-due" type="datetime-local" value={assignDue} onChange={(e) => setAssignDue(e.target.value)} />
            </div>
          </div>
          <button className="nv-button" disabled={busy || !assignUser || assignTitle.trim().length < 2} type="button" onClick={() => void assign()}>
            Assign
          </button>
        </section>
      ) : null}

      {cohort ? (
        <section className="nv-card">
          <h2 className="nv-h2">{cohort.name} members</h2>
          <table className="nv-table">
            <thead>
              <tr>
                <th>Member</th>
                <th>Student</th>
                <th>Status</th>
                <th>Joined</th>
              </tr>
            </thead>
            <tbody>
              {cohort.members.map((row) => (
                <tr key={row.member_id}>
                  <td>#{row.member_id}</td>
                  <td>
                    {row.name ?? `#${row.user_id}`}
                    <div className="nv-muted">{row.email}</div>
                  </td>
                  <td>{row.status}</td>
                  <td>{when(row.joined_at)}</td>
                </tr>
              ))}
              {cohort.members.length === 0 ? (
                <tr>
                  <td colSpan={4} className="nv-muted">Nobody invited yet.</td>
                </tr>
              ) : null}
            </tbody>
          </table>

          <div className="nv-row">
            <div style={{ minWidth: 240 }}>
              <label className="nv-label" htmlFor="invite-ids">Invite user ids (comma separated)</label>
              <input className="nv-input" id="invite-ids" value={inviteIds} onChange={(e) => setInviteIds(e.target.value)} />
            </div>
            <button className="nv-button" disabled={busy || !inviteIds.trim()} type="button" onClick={() => void invite()}>
              Send invitations
            </button>
          </div>

          <div className="nv-row">
            <div>
              <label className="nv-label" htmlFor="remove-id">Remove member id</label>
              <input className="nv-input" id="remove-id" value={removeId} onChange={(e) => setRemoveId(e.target.value)} />
            </div>
            <div style={{ minWidth: 260 }}>
              <label className="nv-label" htmlFor="remove-reason">Reason (required, audited)</label>
              <input className="nv-input" id="remove-reason" value={removeReason} onChange={(e) => setRemoveReason(e.target.value)} />
            </div>
            <button className="nv-button nv-button--danger" disabled={busy || !removeId || removeReason.trim().length < 3} type="button" onClick={() => void remove()}>
              Remove
            </button>
          </div>

          <h3 className="nv-h2">Replacement candidates</h3>
          {replacements ? (
            <table className="nv-table">
              <thead>
                <tr>
                  <th>Student</th>
                  <th>Score</th>
                  <th>Because</th>
                </tr>
              </thead>
              <tbody>
                {replacements.candidates.map((row) => (
                  <tr key={row.user_id}>
                    <td>
                      {row.name ?? `#${row.user_id}`}
                      <div className="nv-muted">{row.email ?? ''}</div>
                    </td>
                    <td>{row.score}</td>
                    <td>{row.qualifies_because.join(' · ') || '—'}</td>
                  </tr>
                ))}
                {replacements.candidates.length === 0 ? (
                  <tr>
                    <td colSpan={3} className="nv-muted">No eligible replacement right now.</td>
                  </tr>
                ) : null}
              </tbody>
            </table>
          ) : (
            <p className="nv-muted">Loading…</p>
          )}
        </section>
      ) : null}
    </div>
  );
}
