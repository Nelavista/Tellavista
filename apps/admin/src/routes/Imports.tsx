/**
 * V1 import runs (C2).
 *
 * The export is pasted or uploaded here and posted as JSON; nothing reads V1's
 * database, so the one-way rule stays structural. Dry-run is the default action
 * and the report is shown before an apply is possible.
 */
import type { ImportListOut, ImportReportOut, ImportResultOut } from '@nelavista/api-client';
import {
  Badge,
  Banner,
  Button,
  EmptyState,
  ErrorState,
  PageHeader,
  Panel,
  Skeleton,
  Textarea,
} from '@nelavista/ui';
import { FileJson, Upload } from 'lucide-react';
import * as React from 'react';

import { ApiError, http } from '../lib/http';
import { useResource } from '../lib/resource';
import { when } from '../lib/format';

type Mode = 'dry_run' | 'apply';

export function Imports(): JSX.Element {
  const runs = useResource<ImportListOut>('/ops/imports');
  const [data, setData] = React.useState('');
  const [mode, setMode] = React.useState<Mode>('dry_run');
  const [result, setResult] = React.useState<ImportResultOut | ImportReportOut | null>(null);
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  async function run(): Promise<void> {
    setBusy(true);
    setError(null);
    setResult(null);
    try {
      const parsed = JSON.parse(data) as Record<string, unknown>;
      const payload = await http.post<ImportResultOut>('/ops/imports', {
        mode,
        source: 'v1_export',
        data: parsed,
      });
      setResult(payload);
      runs.reload();
    } catch (err) {
      if (err instanceof SyntaxError) setError('That is not valid JSON.');
      else setError(err instanceof ApiError ? err.message : 'The import could not run.');
    } finally {
      setBusy(false);
    }
  }

  async function inspect(runId: number): Promise<void> {
    setError(null);
    try {
      setResult(await http.get<ImportReportOut>(`/ops/imports/${runId}`));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not load that run.');
    }
  }

  const report: ImportReportOut | null =
    result && 'reconciliation' in result ? result.reconciliation : result;

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Data"
        title="Import runs"
        description="Dry-run first. An apply writes rows and keeps this report as its receipt; nothing here reads the V1 database."
        actions={
          <Badge tone="info">
            <FileJson aria-hidden="true" size={13} /> JSON export
          </Badge>
        }
      />

      <Panel title="Paste the V1 export" actions={<Upload aria-hidden="true" size={16} />}>
        <div className="nv-stack">
          <div>
            <label className="nv-label" htmlFor="import-file">
              Or choose the JSON file
            </label>
            <input
              accept="application/json,.json"
              id="import-file"
              type="file"
              onChange={(event) => {
                const file = event.target.files?.[0];
                if (!file) return;
                void file.text().then(setData);
              }}
            />
          </div>
          <Textarea
            hint="Paste the whole export. Nothing is sent until you run it."
            id="import-data"
            label="Export JSON"
            placeholder='{"users": [...], "courses": [...]}'
            rows={10}
            value={data}
            onChange={(event) => setData(event.target.value)}
          />
          <div className="nv-row">
            <label className="nv-check">
              <input
                checked={mode === 'dry_run'}
                name="import-mode"
                type="radio"
                onChange={() => setMode('dry_run')}
              />
              Dry run (read-only)
            </label>
            <label className="nv-check">
              <input
                checked={mode === 'apply'}
                name="import-mode"
                type="radio"
                onChange={() => setMode('apply')}
              />
              Apply
            </label>
          </div>
          {mode === 'apply' ? (
            <Banner tone="warning">
              <p>
                Apply writes to the database. Check the dry-run report first; this cannot be undone from here.
              </p>
            </Banner>
          ) : null}
          {error ? (
            <Banner tone="danger">
              <p>{error}</p>
            </Banner>
          ) : null}
          <div>
            <Button disabled={busy || !data.trim()} type="button" onClick={() => void run()}>
              {busy ? 'Running…' : mode === 'apply' ? 'Apply this import' : 'Run the dry run'}
            </Button>
          </div>
        </div>
      </Panel>

      {report ? (
        <Panel
          title={`Run ${report.run_id}`}
          actions={
            <Badge
              status={report.balanced ? 'balanced' : 'mismatch'}
              tone={report.balanced ? 'success' : 'danger'}
            >
              {report.balanced ? 'Balanced' : 'Mismatch'}
            </Badge>
          }
        >
          <div className="nv-table-wrap">
            <table className="nv-table">
              <thead>
                <tr>
                  <th>Section</th>
                  <th>V1 expected</th>
                  <th>V2 actual</th>
                  <th>Skipped</th>
                  <th>Errors</th>
                  <th>Match</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(report.sections).map(([section, row]) => (
                  <tr key={section}>
                    <td>{section}</td>
                    <td>{row.expected ?? 'Not set'}</td>
                    <td>{row.actual}</td>
                    <td>{row.skipped}</td>
                    <td>{row.errors}</td>
                    <td>
                      <Badge
                        status={row.matched ? 'match' : 'differs'}
                        tone={row.matched ? 'success' : 'danger'}
                      >
                        {row.matched ? 'Match' : 'Differs'}
                      </Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Panel>
      ) : null}

      <Panel title="History">
        {runs.resource.status === 'loading' ? <Skeleton lines={4} /> : null}
        {runs.resource.status === 'error' ? (
          <ErrorState
            body={runs.resource.message}
            action={
              <Button size="sm" type="button" variant="secondary" onClick={runs.reload}>
                Try again
              </Button>
            }
          />
        ) : null}
        {runs.resource.status === 'ready' ? (
          runs.resource.data.runs.length === 0 ? (
            <EmptyState
              body="No import has run yet. Paste an export above and start with a dry run."
              icon={FileJson}
              title="No runs"
            />
          ) : (
            <div className="nv-table-wrap">
              <table className="nv-table">
                <thead>
                  <tr>
                    <th>Run</th>
                    <th>Mode</th>
                    <th>Status</th>
                    <th>Started</th>
                    <th>Finished</th>
                    <th />
                  </tr>
                </thead>
                <tbody>
                  {runs.resource.data.runs.map((row) => (
                    <tr key={row.id}>
                      <td>{row.id}</td>
                      <td>{row.mode}</td>
                      <td>{row.status}</td>
                      <td>{when(row.started_at)}</td>
                      <td>{when(row.finished_at)}</td>
                      <td>
                        <Button size="sm" type="button" variant="ghost" onClick={() => void inspect(row.id)}>
                          Report
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
    </div>
  );
}
