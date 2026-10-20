/**
 * V1 import runs (C2).
 *
 * The export is pasted or uploaded here and posted as JSON; nothing reads V1's
 * database, so the one-way rule stays structural. Dry-run is the default action
 * and the report is shown before an apply is possible.
 */
import type {
  ImportListOut,
  ImportReportOut,
  ImportResultOut,
} from '@nelavista/api-client';
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
      <h1 className="nv-h1">Import runs</h1>
      <p className="nv-muted">
        Dry-run first. An apply writes rows and keeps this report as its receipt; nothing here reads the
        V1 database.
      </p>

      <section className="nv-card">
        <h2 className="nv-h2">Paste the V1 export</h2>
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
        <textarea
          className="nv-textarea"
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
          <p className="nv-error">
            Apply writes to the database. Check the dry-run report first; this cannot be undone from here.
          </p>
        ) : null}
        {error ? <p className="nv-error">{error}</p> : null}
        <button className="nv-button" disabled={busy || !data.trim()} type="button" onClick={() => void run()}>
          {busy ? 'Running…' : mode === 'apply' ? 'Apply this import' : 'Run the dry run'}
        </button>
      </section>

      {report ? (
        <section className="nv-card">
          <div className="nv-row nv-row--between">
            <h2 className="nv-h2">Run {report.run_id}</h2>
            <span className="nv-tag" data-tone={report.balanced ? 'ok' : 'bad'}>
              {report.balanced ? 'Balanced' : 'Mismatch'}
            </span>
          </div>
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
                  <td>{row.expected ?? '—'}</td>
                  <td>{row.actual}</td>
                  <td>{row.skipped}</td>
                  <td>{row.errors}</td>
                  <td>
                    <span className="nv-tag" data-tone={row.matched ? 'ok' : 'bad'}>
                      {row.matched ? 'match' : 'differs'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      ) : null}

      <section className="nv-card">
        <h2 className="nv-h2">History</h2>
        {runs.resource.status === 'loading' ? <p className="nv-muted">Loading…</p> : null}
        {runs.resource.status === 'error' ? <p className="nv-error">{runs.resource.message}</p> : null}
        {runs.resource.status === 'ready' ? (
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
                    <button className="nv-button nv-button--ghost" type="button" onClick={() => void inspect(row.id)}>
                      Report
                    </button>
                  </td>
                </tr>
              ))}
              {runs.resource.data.runs.length === 0 ? (
                <tr>
                  <td colSpan={6} className="nv-muted">
                    No import has run yet.
                  </td>
                </tr>
              ) : null}
            </tbody>
          </table>
        ) : null}
      </section>
    </div>
  );
}
