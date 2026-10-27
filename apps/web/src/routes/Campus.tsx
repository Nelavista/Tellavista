/**
 * Campus (B5): a light utility reachable from both paths (PRD §2).
 *
 * It is scoped to the student's own university and holds no social features.
 * Some points have coordinates and some are just text, so the map list is built
 * from links rather than an embedded map SDK: no extra bundle, works offline.
 */
import type { CampusItemOut, CampusOut } from '@nelavista/api-client';
import { Badge, Banner, Button, EmptyState, ErrorState, PageHeader, Panel, Skeleton } from '@nelavista/ui';
import { MapPin, Navigation } from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { ApiError, http } from '../lib/http';

function pointUrl(item: CampusItemOut): string | null {
  if (item.latitude === null || item.longitude === null) return null;
  const { latitude: lat, longitude: lon } = item;
  return `https://www.openstreetmap.org/?mlat=${lat}&mlon=${lon}#map=18/${lat}/${lon}`;
}

function ItemList({ items, empty }: { items: CampusItemOut[]; empty: string }): JSX.Element {
  if (items.length === 0) {
    return <EmptyState body={empty} icon={MapPin} title="Nothing published yet" />;
  }
  return (
    <ul className="nv-list nv-list--ruled">
      {items.map((item) => {
        const href = pointUrl(item);
        return (
          <li key={item.id}>
            <div className="nv-row nv-row--between" style={{ alignItems: 'flex-start' }}>
              <div style={{ minWidth: 0 }}>
                <p className="nv-h4">{item.title}</p>
                <Badge tone="neutral">{item.kind}</Badge>
                {item.body ? <p className="nv-muted">{item.body}</p> : null}
              </div>
              {href ? (
                <a
                  className="nv-button nv-button--ghost nv-button--sm"
                  href={href}
                  rel="noreferrer noopener"
                  target="_blank"
                >
                  <Navigation aria-hidden="true" size={14} />
                  Open on the map
                </a>
              ) : null}
            </div>
          </li>
        );
      })}
    </ul>
  );
}

export function Campus(): JSX.Element {
  const [state, setState] = React.useState<'loading' | 'ready' | 'error'>('loading');
  const [data, setData] = React.useState<CampusOut | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [attempt, setAttempt] = React.useState(0);

  React.useEffect(() => {
    let cancelled = false;
    setState('loading');
    setError(null);
    void (async () => {
      try {
        const campus = await http.get<CampusOut>('/me/campus');
        if (cancelled) return;
        setData(campus);
        setState('ready');
      } catch (err) {
        if (cancelled) return;
        setError(err instanceof ApiError ? err.message : 'Could not load your campus info.');
        setState('error');
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [attempt]);

  if (state === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading campus information">
        <Skeleton height="2rem" width="50%" />
        <Skeleton lines={3} />
        <Skeleton lines={3} />
      </div>
    );
  }

  if (state === 'error') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Campus" title="Campus" />
        <ErrorState
          body={error ?? undefined}
          action={
            <Button size="sm" type="button" variant="secondary" onClick={() => setAttempt((n) => n + 1)}>
              Try again
            </Button>
          }
        />
      </div>
    );
  }

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Campus"
        title="Campus"
        description={
          data?.university
            ? `Information and map points for ${data.university.name}.`
            : 'Information and map points for your university.'
        }
        actions={data?.university ? <Badge tone="info">{data.university.name}</Badge> : null}
      />

      {!data?.university ? (
        <Banner
          tone="warning"
          actions={
            <Link className="nv-button nv-button--secondary nv-button--sm" to="/onboarding">
              Add your university
            </Link>
          }
        >
          <p>
            We do not know your university yet, so there is nothing to show here. Add it in onboarding and
            this page fills in.
          </p>
        </Banner>
      ) : (
        <>
          <Panel title="Need to know">
            <ItemList
              items={data.info}
              empty="Nothing published for your university yet. This is data, so it can be added without an app update."
            />
          </Panel>

          <Panel title="Find your way">
            <ItemList items={data.map} empty="No map points for your university yet." />
          </Panel>
        </>
      )}
    </div>
  );
}
