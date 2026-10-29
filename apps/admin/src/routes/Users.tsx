/**
 * Support lookup (C3).
 *
 * Search by email, username or name; open one account to see its state. No
 * password hash, token or other secret is ever part of this shape.
 */
import type { UserDetailOut, UserListOut } from '@nelavista/api-client';
import {
  Badge,
  Banner,
  Button,
  EmptyState,
  ErrorState,
  Field,
  PageHeader,
  Panel,
  Skeleton,
} from '@nelavista/ui';
import { Search, UserRound } from 'lucide-react';
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
      <PageHeader
        eyebrow="Trust"
        title="Users"
        description="Look up an account to answer a support question. Changes to roles and money happen in their own screens, with their own audit rows."
      />

      <Panel title="Find an account">
        <form
          className="nv-row"
          style={{ alignItems: 'flex-end' }}
          onSubmit={(event) => {
            event.preventDefault();
            setSubmitted(query);
          }}
        >
          <div style={{ flex: 1, minWidth: 240 }}>
            <Field
              hint="At least 2 characters. Email, username or display name."
              id="user-search"
              label="Search"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
            />
          </div>
          <Button disabled={query.trim().length < 2} type="submit">
            <Search aria-hidden="true" size={15} />
            Search
          </Button>
        </form>
      </Panel>

      {list.resource.status === 'loading' ? <Skeleton lines={4} /> : null}
      {list.resource.status === 'error' ? (
        <ErrorState
          body={list.resource.message}
          action={
            <Button size="sm" type="button" variant="secondary" onClick={list.reload}>
              Try again
            </Button>
          }
        />
      ) : null}
      {list.resource.status === 'ready' ? (
        <Panel title="Matches" actions={<Badge tone="neutral">{list.resource.data.users.length}</Badge>}>
          {list.resource.data.users.length === 0 ? (
            <EmptyState
              body="No account matches that search. Try a shorter fragment of the email or username."
              icon={UserRound}
              title="No match"
            />
          ) : (
            <div className="nv-table-wrap">
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
                        <div className="nv-muted">
                          #{row.id} · {row.username}
                        </div>
                      </td>
                      <td>{row.email}</td>
                      <td>{row.role ?? 'Not set'}</td>
                      <td>{row.email_verified ? 'yes' : 'no'}</td>
                      <td>{when(row.created_at)}</td>
                      <td>
                        <Button size="sm" type="button" variant="ghost" onClick={() => void open(row.id)}>
                          Open
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Panel>
      ) : null}

      {error ? (
        <Banner tone="danger">
          <p>{error}</p>
        </Banner>
      ) : null}

      {detail ? (
        <Panel
          title={detail.name ?? detail.username}
          actions={
            <Badge
              status={detail.is_deleted ? 'deleted' : 'active'}
              tone={detail.is_deleted ? 'danger' : 'success'}
            >
              {detail.is_deleted ? 'Deleted' : 'Active'}
            </Badge>
          }
        >
          <dl className="nv-facts">
            <div>
              <dt>Email</dt>
              <dd>
                {detail.email} · #{detail.id}
              </dd>
            </div>
            <div>
              <dt>Role</dt>
              <dd>{detail.role ?? 'No role'}</dd>
            </div>
            <div>
              <dt>Email</dt>
              <dd>{detail.email_verified ? 'Confirmed' : 'Not confirmed'}</dd>
            </div>
            <div>
              <dt>Google</dt>
              <dd>{detail.google_linked ? 'Linked' : 'Not linked'}</dd>
            </div>
            <div>
              <dt>Display name</dt>
              <dd>{detail.profile.display_name ?? 'Not set'}</dd>
            </div>
            <div>
              <dt>Preferred path</dt>
              <dd>{detail.profile.preferred_path ?? 'Not chosen'}</dd>
            </div>
            <div>
              <dt>Onboarding</dt>
              <dd>
                {detail.profile.onboarding_completed_at
                  ? `Completed ${when(detail.profile.onboarding_completed_at)}`
                  : 'Not complete'}
              </dd>
            </div>
            {detail.deleted_at ? (
              <div>
                <dt>Deleted</dt>
                <dd>{when(detail.deleted_at)}</dd>
              </div>
            ) : null}
          </dl>
        </Panel>
      ) : null}
    </div>
  );
}
