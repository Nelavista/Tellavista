/**
 * Study materials (B14).
 *
 * Search is scoped to the courses the student is enrolled in, and a material
 * outside them is refused rather than shown as empty. The reader renders the
 * chunks the Ask answers cite, so "where did this come from?" has a destination.
 */
import type { MaterialDetailOut, MaterialListOut, MaterialSearchOut } from '@nelavista/api-client';
import * as React from 'react';
import { Link, useParams } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { useApiResource } from '../lib/resource';
import { ErrorNote, Skeleton } from '../ui';

export function Materials(): JSX.Element {
  const list = useApiResource<MaterialListOut>('/academia/materials');
  const [query, setQuery] = React.useState('');
  const [search, setSearch] = React.useState<MaterialSearchOut | null>(null);
  const [searching, setSearching] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  async function runSearch(): Promise<void> {
    const cleaned = query.trim();
    if (cleaned.length < 2) {
      setError('Type at least two characters.');
      return;
    }
    setSearching(true);
    setError(null);
    try {
      setSearch(
        await http.get<MaterialSearchOut>(`/academia/materials/search?q=${encodeURIComponent(cleaned)}`),
      );
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not search your materials.');
    } finally {
      setSearching(false);
    }
  }

  if (list.resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading your materials">
        <Skeleton height="2rem" width="35%" />
        <Skeleton lines={4} />
      </div>
    );
  }

  if (list.resource.status === 'off') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Study materials</h1>
        <p className="nv-banner">Materials are not switched on for this environment yet.</p>
      </div>
    );
  }

  if (list.resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Study materials</h1>
        <ErrorNote message={list.resource.message} />
        <button className="nv-button" type="button" onClick={list.reload}>
          Try again
        </button>
      </div>
    );
  }

  return (
    <div className="nv-stack">
      <h1 className="nv-h1">Study materials</h1>
      <p className="nv-muted">
        Notes, textbooks and past questions for the courses you are enrolled in. Nothing outside them is
        searchable.
      </p>

      <section className="nv-card">
        <form
          className="nv-row"
          onSubmit={(event) => {
            event.preventDefault();
            void runSearch();
          }}
        >
          <div style={{ flex: 1, minWidth: 240 }}>
            <label className="nv-label" htmlFor="material-search">Search your courses</label>
            <input
              className="nv-input"
              id="material-search"
              maxLength={120}
              placeholder="e.g. recursion, deadlock, cell cycle"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
            />
          </div>
          <button className="nv-button" disabled={searching} type="submit">
            {searching ? 'Searching…' : 'Search'}
          </button>
        </form>
        <ErrorNote message={error} />
        {search ? (
          <div>
            <h2 className="nv-h2">Results for “{search.query}”</h2>
            {search.results.length === 0 ? (
              <p className="nv-muted">
                Nothing in your enrolled courses matches that. Try a topic from the course outline.
              </p>
            ) : (
              <ul className="nv-list">
                {search.results.map((row) => (
                  <li key={row.material_id} className="nv-card">
                    <Link to={`/academia/materials/${row.material_id}`}>
                      <strong>{row.title}</strong>
                    </Link>
                    <p className="nv-muted">
                      {row.course?.code ?? 'Course'} · relevance {row.score}
                    </p>
                    <p>{row.snippet}</p>
                  </li>
                ))}
              </ul>
            )}
          </div>
        ) : null}
      </section>

      {list.resource.data.materials.length === 0 ? (
        <p className="nv-banner">
          No material yet for your courses. Ask Nelavista can only answer from material that exists.
        </p>
      ) : (
        <ul className="nv-list">
          {list.resource.data.materials.map((material) => (
            <li key={material.id} className="nv-card">
              <div className="nv-row nv-row--between">
                <Link to={`/academia/materials/${material.id}`}>
                  <strong>{material.title}</strong>
                </Link>
                <span className="nv-tag">{material.course?.code ?? 'course'}</span>
              </div>
              <p className="nv-muted">
                {material.course?.title ?? 'Course'} · {material.source ?? 'source not stated'}
              </p>
              {material.file_url ? (
                <a href={material.file_url} rel="noreferrer" target="_blank">
                  Open the original file
                </a>
              ) : null}
            </li>
          ))}
        </ul>
      )}

      <p className="nv-muted">
        <Link to="/academia">Back to the dashboard</Link> · <Link to="/academia/ask">Ask about this material</Link>
      </p>
    </div>
  );
}

export function MaterialReader(): JSX.Element {
  const { materialId = '' } = useParams();
  const { resource, reload } = useApiResource<MaterialDetailOut>(`/academia/materials/${materialId}`);

  if (resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading the material">
        <Skeleton height="2rem" width="50%" />
        <Skeleton lines={6} />
      </div>
    );
  }

  if (resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <h1 className="nv-h1">Material</h1>
        <p className="nv-banner">
          This material is not available to you: it may belong to a course you are not enrolled in.
        </p>
        {resource.status === 'error' ? <ErrorNote message={resource.message} /> : null}
        <button className="nv-button" type="button" onClick={reload}>
          Try again
        </button>
        <p className="nv-muted">
          <Link to="/academia/materials">Back to materials</Link>
        </p>
      </div>
    );
  }

  const material = resource.data;

  return (
    <div className="nv-stack">
      <h1 className="nv-h1">{material.title}</h1>
      <p className="nv-muted">{material.course?.code ?? 'Course'} · {material.course?.title ?? ''}</p>
      {material.file_url ? (
        <p>
          <a href={material.file_url} rel="noreferrer" target="_blank">
            Open the original file
          </a>
        </p>
      ) : null}

      {material.chunks.length === 0 ? (
        <p className="nv-banner">This material has no readable text yet.</p>
      ) : (
        <article className="nv-card">
          {material.chunks.map((chunk) => (
            <p key={chunk.id}>{chunk.content}</p>
          ))}
        </article>
      )}

      <p className="nv-muted">
        <Link to="/academia/materials">All materials</Link> · <Link to="/academia/ask">Ask about this</Link>
      </p>
    </div>
  );
}
