/**
 * Support lookup (C3).
 *
 * Search by email, username or name; open one account to see its state. No
 * password hash, token or other secret is ever part of this shape.
 */
import type { UserDetailOut, UserListOut } from '@nelavista/api-client';
import * as React from 'react';

import { ApiError, http } from '../lib/http';
import { useResource } from '../lib/resource';
import { when } from '../lib/format';

export function Users(): JSX.Element {
  const [query, setQuery] = React.useState('');
  const [submitted, setSubmitted] = React.useState('');
  const [detail, setDetail] = React.useState<UserDetailOut | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const list = useResource<UserListOut>(
    submitted.trim().length >= 2 ? `/ops/users?q=${encodeURIComponent(submitted.trim())}` : null,
  );

  async function open(userId: number): Promise<void> {
    setError(null);
    try {
      setDetail(await http.get<UserDetailOut>(`/ops/users/${userId}`));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not load that account.');
    }
  }

  return (
    <div className="nv-stack">
      <h1 className="nv-h1">Users</h1>
      <p className="nv-muted">
        Look up an account to answer a support question. Changes to roles and money happen in their own
        screens, with their own audit rows.
      </p>

      <form
        className="nv-row"
        onSubmit={(event) => {
          event.preventDefault();
          setSubmitted(query);
        }}
      >
        <div style={{ flex: 1, minWidth: 240 }}>
          <label className="nv-label" htmlFor="user-search">
            Email, username or name (at least 2 characters)
          </label>
          <input
            className="nv-input"
            id="user-search"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
        </div>
        <button className="nv-button" type="submit">
          Search
        </button>
      </form>

      {list.resource.status === 'loading' ? <p className="nv-muted">Searching…</p> : null}
      {list.resource.status === 'error' ? <p className="nv-error">{list.resource.message}</p> : null}
      {list.resource.status === 'ready' ? (
        <div className="nv-card">
          <table className="nv-table">
            <thead>
              <tr>
                <th>User</th>
                <th>Email</th>
                <th>Role</th>
                <th>Verified</th>
                <th>Created</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {list.resource.data.users.map((row) => (
                <tr key={row.id}>
                  <td>
                    {row.name ?? row.username}
                    <div className="nv-muted">#{row.id} · {row.username}</div>
                  </td>
                  <td>{row.email}</td>
                  <td>{row.role ?? '—'}</td>
                  <td>{row.email_verified ? 'yes' : 'no'}</td>
                  <td>{when(row.created_at)}</td>
                  <td>
                    <button className="nv-button nv-button--ghost" type="button" onClick={() => void open(row.id)}>
                      Open
                    </button>
                  </td>
                </tr>
              ))}
              {list.resource.data.users.length === 0 ? (
                <tr>
                  <td colSpan={6} className="nv-muted">
                    No account matches that search.
                  </td>
                </tr>
              ) : null}
            </tbody>
          </table>
        </div>
      ) : null}

      {error ? <p className="nv-error">{error}</p> : null}
      {detail ? (
        <section className="nv-card">
          <div className="nv-row nv-row--between">
            <h2 className="nv-h2">{detail.name ?? detail.username}</h2>
            {detail.is_deleted ? (
              <span className="nv-tag" data-tone="bad">
                deleted
              </span>
            ) : (
              <span className="nv-tag" data-tone="ok">
                active
              </span>
            )}
          </div>
          <p>
            {detail.email} · #{detail.id} · {detail.role ?? 'no role'}
          </p>
          <p className="nv-muted">
            Email {detail.email_verified ? 'confirmed' : 'not confirmed'} · Google{' '}
            {detail.google_linked ? 'linked' : 'not linked'}
            {detail.deleted_at ? ` · deleted ${when(detail.deleted_at)}` : ''}
          </p>
          <p className="nv-muted">
            Display name: {detail.profile.display_name ?? '—'} · path:{' '}
            {detail.profile.preferred_path ?? 'not chosen'} · onboarding{' '}
            {detail.profile.onboarding_completed_at
              ? `completed ${when(detail.profile.onboarding_completed_at)}`
              : 'not complete'}
          </p>
        </section>
      ) : null}
    </div>
  );
}
