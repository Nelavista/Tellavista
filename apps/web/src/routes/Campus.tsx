/**
 * Campus (B5): a light utility reachable from both paths (PRD §2).
 *
 * It is scoped to the student's own university and holds no social features.
 * Some points have coordinates and some are just text, so the map list is built
 * from links rather than an embedded map SDK: no extra bundle, works offline.
 */
import type { CampusItemOut, CampusOut } from '@nelavista/api-client';
import * as React from 'react';

import { ApiError, http } from '../lib/http';
import { ErrorNote, Skeleton } from '../ui';

function pointUrl(item: CampusItemOut): string | null {
  if (item.latitude === null || item.longitude === null) return null;
  const { latitude: lat, longitude: lon } = item;
  return `https://www.openstreetmap.org/?mlat=${lat}&mlon=${lon}#map=18/${lat}/${lon}`;
}

function ItemList({ items, empty }: { items: CampusItemOut[]; empty: string }): JSX.Element {
  if (items.length === 0) return <p className="nv-muted">{empty}</p>;
  return (
    <ul className="nv-list">
      {items.map((item) => {
        const href = pointUrl(item);
        return (
          <li key={item.id}>
            <strong>{item.title}</strong>
            <span className="nv-muted"> · {item.kind}</span>
            {item.body ? <div className="nv-muted">{item.body}</div> : null}
            {href ? (
              <a className="nv-muted" href={href} target="_blank" rel="noreferrer noopener">
                Open on the map
              </a>
            ) : null}
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
        <h1 className="nv-h1">Campus</h1>
        <ErrorNote message={error} />
        <button className="nv-button" type="button" onClick={() => setAttempt((n) => n + 1)}>
          Try again
        </button>
      </div>
    );
  }

  return (
    <div className="nv-stack">
      <h1 className="nv-h1">Campus</h1>

      {!data?.university ? (
        <p className="nv-banner">
          We do not know your university yet, so there is nothing to show here. Add it in onboarding and this
          page fills in.
        </p>
      ) : (
        <>
          <p className="nv-muted">{data.university.name}</p>

          <section className="nv-card" aria-labelledby="nv-campus-info">
            <h2 className="nv-h2" id="nv-campus-info">
              Need to know
            </h2>
            <ItemList
              items={data.info}
              empty="Nothing published for your university yet. This is data, so it can be added without an app update."
            />
          </section>

          <section className="nv-card" aria-labelledby="nv-campus-map">
            <h2 className="nv-h2" id="nv-campus-map">
              Find your way
            </h2>
            <ItemList items={data.map} empty="No map points for your university yet." />
          </section>
        </>
      )}
    </div>
  );
}
