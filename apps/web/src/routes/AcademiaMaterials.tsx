/**
 * Study materials (B14).
 *
 * Search is scoped to the courses the student is enrolled in, and a material
 * outside them is refused rather than shown as empty. The reader renders the
 * chunks the Ask answers cite, so "where did this come from?" has a destination.
 */
import type { MaterialDetailOut, MaterialListOut, MaterialSearchOut } from '@nelavista/api-client';
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
import { ArrowRight, BookOpen, ExternalLink, Search } from 'lucide-react';
import * as React from 'react';
import { Link, useParams } from 'react-router-dom';

import { EMPTY_IMAGES } from '../lib/empty-images';
import { ApiError, http } from '../lib/http';
import { useApiResource } from '../lib/resource';

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
        <PageHeader eyebrow="Academia" title="Study materials" />
        <Banner tone="info">
          <p>Materials are not switched on for this environment yet.</p>
        </Banner>
        <p className="nv-muted">
          <Link to="/home">Back to your home</Link>
        </p>
      </div>
    );
  }

  if (list.resource.status !== 'ready') {
    return (
      <div className="nv-stack">
        <PageHeader eyebrow="Academia" title="Study materials" />
        <ErrorState
          body={list.resource.message}
          action={
            <Button size="sm" type="button" variant="secondary" onClick={list.reload}>
              Try again
            </Button>
          }
        />
      </div>
    );
  }

  const materials = list.resource.data.materials;

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Academia"
        title="Study materials"
        description="Notes, textbooks and past questions for the courses you are enrolled in. Nothing outside them is searchable."
        actions={
          <>
            <Link className="nv-button nv-button--secondary nv-button--sm" to="/academia">
              Dashboard
            </Link>
            <Link className="nv-button nv-button--ghost nv-button--sm" to="/academia/ask">
              Ask about this material
            </Link>
          </>
        }
      />

      <Panel title="Search your courses">
        <form
          className="nv-row"
          onSubmit={(event) => {
            event.preventDefault();
            void runSearch();
          }}
        >
          <div style={{ flex: 1, minWidth: 240 }}>
            <Field
              hint="Searches only the courses you are enrolled in."
              id="material-search"
              label="Topic or phrase"
              maxLength={120}
              placeholder="e.g. recursion, deadlock, cell cycle"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
            />
          </div>
          <Button disabled={searching} type="submit" variant="secondary">
            <Search aria-hidden="true" size={15} />
            {searching ? 'Searching…' : 'Search'}
          </Button>
        </form>

        {error ? (
          <Banner tone="danger">
            <p>{error}</p>
          </Banner>
        ) : null}

        {search ? (
          <div className="nv-stack">
            <div className="nv-row nv-row--between">
              <h2 className="nv-h3">Results for “{search.query}”</h2>
              <Badge tone="neutral">{search.results.length} matches</Badge>
            </div>
            {search.results.length === 0 ? (
              <EmptyState
                body="Try a topic from the course outline. Only material for your enrolled courses is searchable."
                icon={Search}
                title="No match"
              />
            ) : (
              <ul className="nv-list nv-list--ruled">
                {search.results.map((row) => (
                  <li key={row.material_id}>
                    <div className="nv-row nv-row--between">
                      <Link className="nv-h4" to={`/academia/materials/${row.material_id}`}>
                        {row.title}
                      </Link>
                      <span className="nv-meta">
                        {row.course?.code ?? 'Course'} · relevance {row.score}
                      </span>
                    </div>
                    <p className="nv-muted">{row.snippet}</p>
                  </li>
                ))}
              </ul>
            )}
          </div>
        ) : null}
      </Panel>

      <Panel title="Your material" actions={<Badge tone="info">{materials.length}</Badge>}>
        {materials.length === 0 ? (
          <EmptyState
            body="No material yet for your courses. Ask Nelavista can only answer from material that exists."
            icon={BookOpen}
            image={EMPTY_IMAGES.materials}
            title="No material yet"
            action={
              <Link className="nv-button nv-button--secondary nv-button--sm" to="/academia">
                Back to the dashboard
              </Link>
            }
          />
        ) : (
          <div className="nv-table-wrap">
            <table className="nv-table">
              <thead>
                <tr>
                  <th>Material</th>
                  <th>Course</th>
                  <th>Source</th>
                  <th />
                </tr>
              </thead>
              <tbody>
                {materials.map((material) => (
                  <tr key={material.id}>
                    <td>
                      <Link to={`/academia/materials/${material.id}`}>{material.title}</Link>
                    </td>
                    <td>
                      <span className="nv-mono">{material.course?.code ?? 'course'}</span>
                      <div className="nv-muted">{material.course?.title ?? ''}</div>
                    </td>
                    <td>{material.source ?? 'source not stated'}</td>
                    <td>
                      {material.file_url ? (
                        <a
                          className="nv-button nv-button--ghost nv-button--sm"
                          href={material.file_url}
                          rel="noreferrer"
                          target="_blank"
                        >
                          <ExternalLink aria-hidden="true" size={14} />
                          Open file
                        </a>
                      ) : (
                        <Link
                          className="nv-button nv-button--ghost nv-button--sm"
                          to={`/academia/materials/${material.id}`}
                        >
                          Read
                          <ArrowRight aria-hidden="true" size={14} />
                        </Link>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Panel>
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
        <PageHeader eyebrow="Academia" title="Material" />
        <Banner tone="warning">
          <p>This material is not available to you: it may belong to a course you are not enrolled in.</p>
        </Banner>
        {resource.status === 'error' ? <ErrorState body={resource.message} /> : null}
        <div className="nv-row">
          <Button size="sm" type="button" variant="secondary" onClick={reload}>
            Try again
          </Button>
          <Link className="nv-button nv-button--ghost nv-button--sm" to="/academia/materials">
            Back to materials
          </Link>
        </div>
      </div>
    );
  }

  const material = resource.data;

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow={material.course?.code ?? 'Material'}
        title={material.title}
        description={material.course?.title ?? undefined}
        actions={
          <>
            {material.file_url ? (
              <a
                className="nv-button nv-button--secondary nv-button--sm"
                href={material.file_url}
                rel="noreferrer"
                target="_blank"
              >
                <ExternalLink aria-hidden="true" size={15} />
                Open the original file
              </a>
            ) : null}
            <Link className="nv-button nv-button--ghost nv-button--sm" to="/academia/ask">
              Ask about this
            </Link>
          </>
        }
      />

      {material.chunks.length === 0 ? (
        <Banner tone="info">
          <p>This material has no readable text yet.</p>
        </Banner>
      ) : (
        <Panel title="Text">
          <article className="nv-reading">
            {material.chunks.map((chunk) => (
              <p key={chunk.id}>{chunk.content}</p>
            ))}
          </article>
        </Panel>
      )}

      <p className="nv-muted">
        <Link to="/academia/materials">All materials</Link> · <Link to="/academia">Dashboard</Link>
      </p>
    </div>
  );
}
