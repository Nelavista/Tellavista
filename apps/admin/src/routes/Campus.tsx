/**
 * Campus publisher.
 *
 * The API can publish a campus fact or map point but has no ops read for the
 * published set yet. This screen is honest about that: it publishes, shows the
 * write receipt, and keeps a session list of what this browser just created.
 * It never presents that list as the live campus.
 */
import type { CampusCreatedOut, UniversityOut } from '@nelavista/api-client';
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

interface Receipt {
  id: number;
  kind: string;
  title: string;
  university: string;
  at: string;
}

function coordinate(raw: string, limit: number): number | null | 'invalid' {
  const trimmed = raw.trim();
  if (!trimmed) return null;
  const value = Number(trimmed);
  if (!Number.isFinite(value) || Math.abs(value) > limit) return 'invalid';
  return value;
}

export function Campus(): JSX.Element {
  const universities = useResource<UniversityOut[]>('/onboarding/universities');

  const [universityId, setUniversityId] = React.useState('');
  const [kind, setKind] = React.useState('info');
  const [title, setTitle] = React.useState('');
  const [body, setBody] = React.useState('');
  const [latitude, setLatitude] = React.useState('');
  const [longitude, setLongitude] = React.useState('');
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [note, setNote] = React.useState<string | null>(null);
  const [receipts, setReceipts] = React.useState<Receipt[]>([]);

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

  const selected =
    universities.resource.status === 'ready'
      ? (universities.resource.data.find((row) => String(row.id) === universityId) ?? null)
      : null;

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
      setReceipts((current) => [
        {
          id: created.id,
          kind: created.kind,
          title: created.title,
          university: universityName,
          at: new Date().toISOString(),
        },
        ...current,
      ]);
      setNote(`Published “${created.title}” for ${universityName}. Campus item #${created.id}.`);
      setTitle('');
      setBody('');
      setLatitude('');
      setLongitude('');
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
        description="Publish university information and map points. Students see published items on their campus screen."
        actions={<Badge tone="neutral">Write only</Badge>}
      />

      <Banner tone="warning" actions={null}>
        <p>
          Ops can publish campus items but cannot read the published set yet. The list below is this browser
          session&rsquo;s receipts, not the live campus. A read endpoint is a launch dependency.
        </p>
      </Banner>

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
              placeholder="Opening hours, entrance, who to ask…"
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
                {busy ? 'Publishing…' : 'Publish item'}
              </Button>
            </div>
          </form>
        ) : null}
      </Panel>

      <Panel title="Published in this session">
        {receipts.length === 0 ? (
          <EmptyState
            body="Nothing has been published from this browser since the page loaded. Successful writes will appear here with their receipt."
            icon={MapPin}
            title="No receipts yet"
          />
        ) : (
          <div className="nv-table-wrap">
            <table className="nv-table">
              <caption>
                Session receipts only. Reloading the page clears this list; the published items remain in the
                database.
              </caption>
              <thead>
                <tr>
                  <th>Published</th>
                  <th>University</th>
                  <th>Kind</th>
                  <th>Title</th>
                  <th>Id</th>
                </tr>
              </thead>
              <tbody>
                {receipts.map((row) => (
                  <tr key={`${row.id}-${row.at}`}>
                    <td>{when(row.at)}</td>
                    <td>{row.university}</td>
                    <td>{row.kind}</td>
                    <td>{row.title}</td>
                    <td className="nv-num">#{row.id}</td>
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
