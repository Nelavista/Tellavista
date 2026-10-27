/**
 * University waitlist.
 *
 * Students join the waitlist when their university is not covered yet. The
 * screen groups demand by university so the next coverage decision is obvious,
 * then lists every request with its note and any linked account.
 */
import type { WaitlistOut } from '@nelavista/api-client';
import { Badge, Button, EmptyState, ErrorState, PageHeader, Panel, Skeleton } from '@nelavista/ui';
import { Building2, Search, UserPlus } from 'lucide-react';
import * as React from 'react';

import { when } from '../lib/format';
import { useResource } from '../lib/resource';

type Entry = WaitlistOut['waitlist'][number];

interface Demand {
  name: string;
  count: number;
  latest: string | null;
  accounts: number;
}

function byUniversity(entries: Entry[]): Demand[] {
  const map = new Map<string, { count: number; latest: string | null; accounts: Set<number> }>();

  for (const entry of entries) {
    const current = map.get(entry.university_name) ?? {
      count: 0,
      latest: null,
      accounts: new Set<number>(),
    };
    current.count += 1;
    if (
      entry.created_at &&
      (current.latest === null || new Date(entry.created_at).getTime() > new Date(current.latest).getTime())
    ) {
      current.latest = entry.created_at;
    }
    if (entry.user_id !== null && entry.user_id !== undefined) current.accounts.add(entry.user_id);
    map.set(entry.university_name, current);
  }

  return [...map.entries()]
    .map(([name, value]) => ({
      name,
      count: value.count,
      latest: value.latest,
      accounts: value.accounts.size,
    }))
    .sort((a, b) => b.count - a.count || a.name.localeCompare(b.name));
}

function matches(entry: Entry, query: string): boolean {
  if (!query) return true;
  const haystack = [entry.university_name, entry.email, entry.note, entry.user_id]
    .map((value) => (value === null || value === undefined ? '' : String(value)))
    .join(' ')
    .toLowerCase();
  return haystack.includes(query);
}

export function Waitlist(): JSX.Element {
  const { resource, reload } = useResource<WaitlistOut>('/ops/waitlist?limit=500');
  const [query, setQuery] = React.useState('');

  const entries = resource.status === 'ready' ? resource.data.waitlist : [];
  const demand = React.useMemo(() => byUniversity(entries), [entries]);
  const needle = query.trim().toLowerCase();
  const filtered = React.useMemo(() => entries.filter((entry) => matches(entry, needle)), [entries, needle]);

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Demand"
        title="Waitlist"
        description="Requests for universities the platform does not cover yet. Grouped demand shows where the next partnership would serve the most students."
        actions={
          resource.status === 'ready' ? (
            <Badge tone="info">
              {entries.length} {entries.length === 1 ? 'request' : 'requests'}
            </Badge>
          ) : null
        }
      />

      <Panel title="Demand by university">
        {resource.status === 'loading' ? <Skeleton lines={4} /> : null}
        {resource.status === 'error' ? (
          <ErrorState
            body={resource.message}
            action={
              <Button size="sm" type="button" variant="secondary" onClick={reload}>
                Try again
              </Button>
            }
          />
        ) : null}
        {resource.status === 'ready' ? (
          demand.length === 0 ? (
            <EmptyState
              body="No one has asked for an uncovered university yet. Entries appear here when a student joins the waitlist during onboarding."
              icon={Building2}
              title="No university demand yet"
            />
          ) : (
            <div className="nv-table-wrap">
              <table className="nv-table">
                <caption>
                  Counted from the latest {entries.length} entries. Select a university to filter the list
                  below.
                </caption>
                <thead>
                  <tr>
                    <th>University</th>
                    <th>Requests</th>
                    <th>Latest request</th>
                    <th>Linked accounts</th>
                    <th />
                  </tr>
                </thead>
                <tbody>
                  {demand.map((row) => (
                    <tr key={row.name}>
                      <td>{row.name}</td>
                      <td className="nv-num">{row.count}</td>
                      <td>{when(row.latest)}</td>
                      <td className="nv-num">{row.accounts}</td>
                      <td>
                        <Button size="sm" type="button" variant="ghost" onClick={() => setQuery(row.name)}>
                          Filter
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )
        ) : null}
      </Panel>

      <Panel
        title="Every request"
        actions={
          query ? (
            <Button size="sm" type="button" variant="ghost" onClick={() => setQuery('')}>
              Clear filter
            </Button>
          ) : null
        }
      >
        <div>
          <label className="nv-label" htmlFor="waitlist-search">
            Search university, email, note or account id
          </label>
          <div className="nv-search">
            <Search aria-hidden="true" size={16} />
            <input
              className="nv-input"
              id="waitlist-search"
              placeholder="University, email or note"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
            />
          </div>
        </div>

        {resource.status === 'loading' ? <Skeleton lines={5} /> : null}
        {resource.status === 'error' ? (
          <ErrorState
            body={resource.message}
            action={
              <Button size="sm" type="button" variant="secondary" onClick={reload}>
                Try again
              </Button>
            }
          />
        ) : null}
        {resource.status === 'ready' ? (
          filtered.length === 0 ? (
            <EmptyState
              body={
                entries.length === 0
                  ? 'The waitlist is empty. New requests will appear here as students join.'
                  : 'No request matches that search.'
              }
              icon={entries.length === 0 ? UserPlus : Search}
              title={entries.length === 0 ? 'No requests yet' : 'No match'}
            />
          ) : (
            <div className="nv-table-wrap">
              <table className="nv-table">
                <thead>
                  <tr>
                    <th>When</th>
                    <th>University</th>
                    <th>Email</th>
                    <th>Account</th>
                    <th>Note</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((row) => (
                    <tr key={row.id}>
                      <td>{when(row.created_at)}</td>
                      <td>{row.university_name}</td>
                      <td>{row.email ?? '—'}</td>
                      <td className="nv-num">{row.user_id ?? '—'}</td>
                      <td>{row.note ?? '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )
        ) : null}
      </Panel>
    </div>
  );
}
