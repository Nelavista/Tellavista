/**
 * Campus publisher and read surface.
 *
 * Ops publish a university fact or map point and then read the live campus set,
 * including unpublished rows. The list is the API's record, not a browser
 * session receipt, so a reload never hides what was published.
 */
import type { CampusAdminListOut, CampusCreatedOut, UniversityOut } from '@nelavista/api-client';
import {
  Badge,
  Banner,
  Button,
  EmptyState,
  ErrorState,
  Field,
  PageHeader,
  Panel,
  Select,
  Skeleton,
  Textarea,
} from '@nelavista/ui';
import { Building2, MapPin, Plus } from 'lucide-react';
import * as React from 'react';

import { ApiError, http } from '../lib/http';
import { when } from '../lib/format';
import { useResource } from '../lib/resource';

const KINDS = [
  { value: 'info', label: 'Information' },
  { value: 'building', label: 'Building' },
  { value: 'library', label: 'Library' },
  { value: 'hall', label: 'Hall' },
  { value: 'department', label: 'Department' },
  { value: 'hostel', label: 'Hostel' },
  { value: 'food', label: 'Food' },
  { value: 'map', label: 'Map point' },
];

const MAP_KINDS = new Set(['building', 'library', 'hall', 'department', 'hostel', 'food', 'map']);

function coordinate(raw: string, limit: number): number | null | 'invalid' {
  const trimmed = raw.trim();
  if (!trimmed) return null;
  const value = Number(trimmed);
  if (!Number.isFinite(value) || Math.abs(value) > limit) return 'invalid';
  return value;
}

function coordinateLabel(latitude: number | null | undefined, longitude: number | null | undefined): string {
  if (latitude === null || latitude === undefined || longitude === null || longitude === undefined) {
    return 'No map point';
  }
  return `${latitude.toFixed(5)}, ${longitude.toFixed(5)}`;
}

export function Campus(): JSX.Element {
  const universities = useResource<UniversityOut[]>('/onboarding/universities');
  const campus = useResource<CampusAdminListOut>('/ops/campus');

  const [universityId, setUniversityId] = React.useState('');
  const [kind, setKind] = React.useState('info');
  const [title, setTitle] = React.useState('');
  const [body, setBody] = React.useState('');
  const [latitude, setLatitude] = React.useState('');
  const [longitude, setLongitude] = React.useState('');
  const [filterUniversity, setFilterUniversity] = React.useState('all');
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [note, setNote] = React.useState<string | null>(null);

  const options = React.useMemo(() => {
    const rows =
      universities.resource.status === 'ready'
        ? [...universities.resource.data].sort((a, b) => a.name.localeCompare(b.name))
        : [];
    return [
      { value: '', label: 'Choose a university' },
      ...rows.map((row) => ({ value: String(row.id), label: row.name })),
    ];
  }, [universities.resource]);

  const filterOptions = React.useMemo(() => {
    const rows = universities.resource.status === 'ready' ? universities.resource.data : [];
    const campusRows = campus.resource.status === 'ready' ? campus.resource.data.items : [];
    const names = new Map<number, string>();
    for (const row of rows) names.set(row.id, row.name);
    for (const row of campusRows) names.set(row.university_id, row.university_name);
    return [
      { value: 'all', label: 'All universities' },
      ...[...names.entries()]
        .sort((a, b) => a[1].localeCompare(b[1]))
        .map(([id, name]) => ({ value: String(id), label: name })),
    ];
  }, [universities.resource, campus.resource]);

  const selected =
    universities.resource.status === 'ready'
      ? (universities.resource.data.find((row) => String(row.id) === universityId) ?? null)
      : null;

  const items =
    campus.resource.status === 'ready'
      ? campus.resource.data.items.filter(
          (row) => filterUniversity === 'all' || String(row.university_id) === filterUniversity,
        )
      : [];

  async function publish(event: React.FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();
    setError(null);
    setNote(null);

    if (!universityId) {
      setError('Choose the university this item belongs to.');
      return;
    }
    if (!title.trim()) {
      setError('Give the item a title.');
      return;
    }

    const lat = coordinate(latitude, 90);
    const lng = coordinate(longitude, 180);
    if (lat === 'invalid') {
      setError('Latitude must be a number between -90 and 90.');
      return;
    }
    if (lng === 'invalid') {
      setError('Longitude must be a number between -180 and 180.');
      return;
    }
    if ((lat === null) !== (lng === null)) {
      setError('Give both coordinates, or neither.');
      return;
    }

    setBusy(true);
    try {
      const created = await http.post<CampusCreatedOut>('/ops/campus', {
        university_id: Number(universityId),
        kind,
        title: title.trim(),
        body: body.trim(),
        latitude_micro: lat === null ? null : Math.round(lat * 1_000_000),
        longitude_micro: lng === null ? null : Math.round(lng * 1_000_000),
      });
      const universityName = selected?.name ?? `University #${universityId}`;
      setNote(`Published ${created.title} for ${universityName}. Campus item #${created.id}.`);
      setTitle('');
      setBody('');
      setLatitude('');
      setLongitude('');
      campus.reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'That item could not be published.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Configure"
        title="Campus"
        description="Publish university information and map points, then read the live set students can see."
        actions={
          <Badge tone={campus.resource.status === 'ready' ? 'success' : 'neutral'}>
            {campus.resource.status === 'ready' ? 'Live read' : 'Reading'}
          </Badge>
        }
      />

      <Panel title="Publish an item" actions={<Plus aria-hidden="true" size={16} />}>
        {universities.resource.status === 'loading' ? <Skeleton lines={4} /> : null}
        {universities.resource.status === 'error' ? (
          <ErrorState
            body={universities.resource.message}
            action={
              <Button size="sm" type="button" variant="secondary" onClick={universities.reload}>
                Try again
              </Button>
            }
          />
        ) : null}
        {universities.resource.status === 'ready' && universities.resource.data.length === 0 ? (
          <EmptyState
            body="No university is loaded, so there is nothing to attach a campus item to. Import or seed the university directory first."
            icon={Building2}
            title="No universities available"
          />
        ) : null}

        {universities.resource.status === 'ready' && universities.resource.data.length > 0 ? (
          <form className="nv-stack" onSubmit={(event) => void publish(event)}>
            <div className="nv-grid--2">
              <Select
                label="University"
                options={options}
                value={universityId}
                onChange={(event) => setUniversityId(event.target.value)}
              />
              <Select
                hint={
                  MAP_KINDS.has(kind) ? 'Plotted as a map point.' : 'Shown in the campus information list.'
                }
                label="Kind"
                options={KINDS}
                value={kind}
                onChange={(event) => setKind(event.target.value)}
              />
            </div>

            <Field
              label="Title"
              placeholder="Main library"
              required
              value={title}
              onChange={(event) => setTitle(event.target.value)}
            />
            <Textarea
              hint="What a student needs to know. Plain text; no markup is rendered."
              label="Body"
              placeholder="Opening hours, entrance, who to ask..."
              rows={4}
              value={body}
              onChange={(event) => setBody(event.target.value)}
            />

            <div className="nv-grid--2">
              <Field
                hint="Decimal degrees, optional."
                inputMode="decimal"
                label="Latitude"
                placeholder="6.5244"
                value={latitude}
                onChange={(event) => setLatitude(event.target.value)}
              />
              <Field
                hint="Decimal degrees, optional. Give both coordinates or neither."
                inputMode="decimal"
                label="Longitude"
                placeholder="3.3792"
                value={longitude}
                onChange={(event) => setLongitude(event.target.value)}
              />
            </div>

            {error ? (
              <Banner tone="danger">
                <p>{error}</p>
              </Banner>
            ) : null}
            {note ? (
              <Banner tone="success">
                <p>{note}</p>
              </Banner>
            ) : null}

            <div className="nv-row nv-row--between">
              <p className="nv-meta">
                {selected ? `Publishing to ${selected.name}` : 'Choose a university to continue'}
              </p>
              <Button disabled={busy || !universityId} type="submit">
                <MapPin aria-hidden="true" size={15} />
                {busy ? 'Publishing...' : 'Publish item'}
              </Button>
            </div>
          </form>
        ) : null}
      </Panel>

      <Panel title="Campus record" actions={<Badge tone="neutral">{items.length}</Badge>}>
        {filterOptions.length > 2 ? (
          <div className="nv-row" style={{ marginBottom: 'var(--nv-space-md)', maxWidth: '20rem' }}>
            <Select
              label="Filter by university"
              options={filterOptions}
              value={filterUniversity}
              onChange={(event) => setFilterUniversity(event.target.value)}
            />
          </div>
        ) : null}
        {campus.resource.status === 'loading' ? <Skeleton lines={5} /> : null}
        {campus.resource.status === 'error' ? (
          <ErrorState
            body={campus.resource.message}
            action={
              <Button size="sm" type="button" variant="secondary" onClick={campus.reload}>
                Try again
              </Button>
            }
          />
        ) : null}
        {campus.resource.status === 'ready' && campus.resource.data.items.length === 0 ? (
          <EmptyState
            body="Publish the first item above. It will appear here with its publication state."
            icon={MapPin}
            title="No campus items yet"
          />
        ) : null}
        {campus.resource.status === 'ready' && campus.resource.data.items.length > 0 && items.length === 0 ? (
          <EmptyState
            body="No item belongs to that university. Choose another filter to see the rest of the set."
            title="Nothing in this filter"
            action={
              <Button onClick={() => setFilterUniversity('all')} size="sm" type="button" variant="secondary">
                Show all universities
              </Button>
            }
          />
        ) : null}
        {campus.resource.status === 'ready' && items.length > 0 ? (
          <div className="nv-table-wrap">
            <table className="nv-table">
              <caption>The live campus set. Unpublished rows are visible to ops only.</caption>
              <thead>
                <tr>
                  <th>Created</th>
                  <th>University</th>
                  <th>Kind</th>
                  <th>Title</th>
                  <th>Map point</th>
                  <th>State</th>
                </tr>
              </thead>
              <tbody>
                {items.map((row) => (
                  <tr key={row.id}>
                    <td>
                      <span>{when(row.created_at)}</span>
                      <p className="nv-meta nv-mono">#{row.id}</p>
                    </td>
                    <td>{row.university_name}</td>
                    <td className="nv-mono">{row.kind}</td>
                    <td>
                      <strong>{row.title}</strong>
                      {row.body ? <p className="nv-meta">{row.body}</p> : null}
                    </td>
                    <td className="nv-mono">{coordinateLabel(row.latitude, row.longitude)}</td>
                    <td>
                      <Badge tone={row.is_published ? 'success' : 'warning'}>
                        {row.is_published ? 'Published' : 'Hidden'}
                      </Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : null}
      </Panel>
    </div>
  );
}
