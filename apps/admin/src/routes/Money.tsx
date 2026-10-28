/**
 * Money (C6).
 *
 * The only way to "fix" a ledger row is a reversal with a reason; there is no
 * edit route. Payouts move create → approve → pay, and the API enforces the
 * second-approver rule for large batches even if this screen did not.
 */
import type {
  BatchStateOut,
  FinancialsOut,
  FundOut,
  LedgerOut,
  PayoutBatchDetailOut,
  PayoutBatchListOut,
  ProjectListOut,
  ReconcileReportOut,
  ReconcileRunOut,
  ReverseOut,
} from '@nelavista/api-client';
import { Badge, Banner, EmptyState, ErrorNote, ErrorState, PageHeader, Panel, Skeleton } from '@nelavista/ui';
import * as React from 'react';

import { ApiError, download, http } from '../lib/http';
import { useResource } from '../lib/resource';
import { money, when } from '../lib/format';

export function Money(): JSX.Element {
  const projects = useResource<ProjectListOut>('/work/projects');
  const [slug, setSlug] = React.useState('');
  const financials = useResource<FinancialsOut>(slug ? `/money/projects/${slug}/financials` : null);
  const ledger = useResource<LedgerOut>(slug ? `/money/projects/${slug}/ledger` : null);
  const batches = useResource<PayoutBatchListOut>(slug ? `/money/projects/${slug}/payout-batches` : null);
  const reconciliation = useResource<ReconcileReportOut>(
    slug ? `/money/projects/${slug}/reconciliation` : null,
  );

  const [fundAmount, setFundAmount] = React.useState('');
  const [reverseId, setReverseId] = React.useState('');
  const [reverseReason, setReverseReason] = React.useState('');
  const [batchIds, setBatchIds] = React.useState('');
  const [batchDetail, setBatchDetail] = React.useState<PayoutBatchDetailOut | null>(null);
  const [cancelReason, setCancelReason] = React.useState('');
  const [failReason, setFailReason] = React.useState('');
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [note, setNote] = React.useState<string | null>(null);

  function refresh(): void {
    financials.reload();
    ledger.reload();
    batches.reload();
    reconciliation.reload();
  }

  async function fund(): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      const result = await http.post<FundOut>(`/money/projects/${slug}/fund`, {
        total_minor: Math.round(Number(fundAmount) * 100),
      });
      setNote(
        `Funded ${money(result.total_minor, result.currency)}: students ${money(result.student_pool_minor, result.currency)}, fee ${money(result.platform_fee_minor, result.currency)}, department ${money(result.department_share_minor, result.currency)}.`,
      );
      setFundAmount('');
      refresh();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not fund that project.');
    } finally {
      setBusy(false);
    }
  }

  async function reverse(): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      const row = await http.post<ReverseOut>(`/money/transactions/${Number(reverseId)}/reverse`, {
        reason: reverseReason.trim(),
      });
      setNote(`Reversal #${row.id} posted; the original row is untouched.`);
      setReverseId('');
      setReverseReason('');
      refresh();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not post that reversal.');
    } finally {
      setBusy(false);
    }
  }

  async function createBatch(): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      const ids = batchIds
        .split(',')
        .map((value) => Number(value.trim()))
        .filter((value) => Number.isInteger(value) && value > 0);
      const batch = await http.post<BatchStateOut>(`/money/projects/${slug}/payout-batches`, {
        earning_line_ids: ids.length > 0 ? ids : null,
        provider: 'manual',
      });
      setNote(`Batch #${batch.id} created (${batch.status}). A second approver is required above the limit.`);
      setBatchIds('');
      refresh();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not create that batch.');
    } finally {
      setBusy(false);
    }
  }

  async function moveBatch(batchId: number, action: 'approve' | 'pay' | 'cancel'): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      const body = action === 'cancel' ? { reason: cancelReason.trim() || 'Cancelled by ops' } : {};
      const row = await http.post<BatchStateOut>(`/money/payout-batches/${batchId}/${action}`, body);
      setNote(`Batch #${row.id} is ${row.status}.`);
      refresh();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : `Could not ${action} that batch.`);
    } finally {
      setBusy(false);
    }
  }

  async function openBatch(batchId: number): Promise<void> {
    setError(null);
    try {
      setBatchDetail(await http.get<PayoutBatchDetailOut>(`/money/payout-batches/${batchId}`));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not load that batch.');
    }
  }

  async function failPayoutItem(itemId: number): Promise<void> {
    if (!batchDetail) return;
    setBusy(true);
    setError(null);
    try {
      await http.post(`/money/payout-items/${itemId}/fail`, { reason: failReason.trim() });
      setNote(`Payout item #${itemId} marked failed; the reason is in the audit trail.`);
      setFailReason('');
      await openBatch(batchDetail.id);
      refresh();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not fail that payout item.');
    } finally {
      setBusy(false);
    }
  }

  async function runReconciliation(): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      const run = await http.post<ReconcileRunOut>('/money/reconciliation/run', {});
      setNote(`Reconciliation #${run.id} finished; balanced: ${run.balanced ? 'yes' : 'no'}.`);
      reconciliation.reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not run reconciliation.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="nv-stack nv-stack--loose">
      <PageHeader
        eyebrow="Money"
        title="Money"
        description="Amounts are integers in minor units. Funding splits once, at funding time; every later movement is a new transaction."
      />

      <ErrorNote message={error} />
      {note ? <Banner tone="success">{note}</Banner> : null}

      <Panel title="Project">
        {projects.resource.status === 'loading' ? <Skeleton lines={2} /> : null}
        {projects.resource.status === 'error' ? (
          <ErrorState title="Projects did not load" body={projects.resource.message} />
        ) : null}
        {projects.resource.status === 'ready' && projects.resource.data.projects.length === 0 ? (
          <EmptyState title="No project yet" body="Create a project before funding work or paying a batch." />
        ) : null}
        {projects.resource.status === 'ready' && projects.resource.data.projects.length > 0 ? (
          <div className="nv-row">
            <select
              className="nv-select"
              value={slug}
              onChange={(event) => setSlug(event.target.value)}
              style={{ maxWidth: 320 }}
            >
              <option value="">Select a project…</option>
              {projects.resource.data.projects.map((row) => (
                <option key={row.id} value={row.slug}>
                  {row.title} ({row.slug})
                </option>
              ))}
            </select>
            {slug ? (
              <button
                className="nv-button nv-button--ghost"
                type="button"
                onClick={() => void download(`/money/projects/${slug}/ledger/export`, `ledger-${slug}.csv`)}
              >
                Export ledger CSV
              </button>
            ) : null}
          </div>
        ) : null}
      </Panel>

      {slug ? (
        <>
          <Panel title="Financials">
            {financials.resource.status === 'ready' ? (
              <Financials data={financials.resource.data} />
            ) : financials.resource.status === 'error' ? (
              <ErrorState title="Financials did not load" body={financials.resource.message} />
            ) : (
              <Skeleton lines={3} />
            )}

            <div className="nv-row">
              <div>
                <label className="nv-label" htmlFor="fund-amount">
                  Fund this project (major units)
                </label>
                <input
                  className="nv-input"
                  id="fund-amount"
                  type="number"
                  value={fundAmount}
                  onChange={(e) => setFundAmount(e.target.value)}
                />
              </div>
              <button
                className="nv-button"
                disabled={busy || !fundAmount}
                type="button"
                onClick={() => void fund()}
              >
                Fund
              </button>
            </div>

            <div className="nv-row">
              <div>
                <label className="nv-label" htmlFor="reverse-id">
                  Reverse transaction id
                </label>
                <input
                  className="nv-input"
                  id="reverse-id"
                  value={reverseId}
                  onChange={(e) => setReverseId(e.target.value)}
                />
              </div>
              <div style={{ minWidth: 260 }}>
                <label className="nv-label" htmlFor="reverse-reason">
                  Reason (required)
                </label>
                <input
                  className="nv-input"
                  id="reverse-reason"
                  value={reverseReason}
                  onChange={(e) => setReverseReason(e.target.value)}
                />
              </div>
              <button
                className="nv-button nv-button--danger"
                disabled={busy || !reverseId || reverseReason.trim().length < 3}
                type="button"
                onClick={() => void reverse()}
              >
                Post reversal
              </button>
            </div>
          </Panel>

          <Panel title="Reconciliation">
            <button
              className="nv-button"
              disabled={busy}
              type="button"
              onClick={() => void runReconciliation()}
            >
              Run now
            </button>
            {reconciliation.resource.status === 'ready' ? (
              <div>
                <Badge tone={reconciliation.resource.data.balanced ? 'success' : 'danger'}>
                  {reconciliation.resource.data.balanced ? 'balanced' : 'does not balance'}
                </Badge>
                <pre className="nv-pre nv-muted">
                  {JSON.stringify(reconciliation.resource.data.details, null, 2)}
                </pre>
              </div>
            ) : reconciliation.resource.status === 'error' ? (
              <ErrorState title="Reconciliation did not load" body={reconciliation.resource.message} />
            ) : (
              <Skeleton lines={3} />
            )}
          </Panel>

          <Panel title="Payout batches">
            <div className="nv-row">
              <div style={{ minWidth: 320 }}>
                <label className="nv-label" htmlFor="batch-lines">
                  Earning line ids (comma separated; empty = all payable)
                </label>
                <input
                  className="nv-input"
                  id="batch-lines"
                  value={batchIds}
                  onChange={(e) => setBatchIds(e.target.value)}
                />
              </div>
              <button className="nv-button" disabled={busy} type="button" onClick={() => void createBatch()}>
                Create batch
              </button>
              <div style={{ minWidth: 220 }}>
                <label className="nv-label" htmlFor="cancel-reason">
                  Cancel reason
                </label>
                <input
                  className="nv-input"
                  id="cancel-reason"
                  value={cancelReason}
                  onChange={(e) => setCancelReason(e.target.value)}
                />
              </div>
            </div>

            {batches.resource.status === 'loading' ? <Skeleton lines={4} /> : null}
            {batches.resource.status === 'error' ? (
              <ErrorState title="Payout batches did not load" body={batches.resource.message} />
            ) : null}
            {batches.resource.status === 'ready' && batches.resource.data.batches.length === 0 ? (
              <EmptyState
                title="No batch yet"
                body="Create a batch from the payable lines above. It starts as a draft."
              />
            ) : null}
            {batches.resource.status === 'ready' && batches.resource.data.batches.length > 0 ? (
              <div className="nv-table-wrap">
                <table className="nv-table">
                  <thead>
                    <tr>
                      <th scope="col">Batch</th>
                      <th scope="col">Total</th>
                      <th scope="col">Status</th>
                      <th scope="col">Paid</th>
                      <th scope="col">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {batches.resource.data.batches.map((row) => (
                      <tr key={row.id}>
                        <td>
                          #{row.id} · {row.provider ?? 'manual'}
                        </td>
                        <td>{money(row.total_minor, row.currency)}</td>
                        <td>
                          <Badge
                            tone={
                              row.status === 'paid'
                                ? 'success'
                                : row.status === 'failed'
                                  ? 'danger'
                                  : 'warning'
                            }
                          >
                            {row.status}
                          </Badge>
                        </td>
                        <td>{when(row.paid_at)}</td>
                        <td>
                          <div className="nv-row">
                            <button
                              className="nv-button nv-button--ghost"
                              type="button"
                              onClick={() => void openBatch(row.id)}
                            >
                              Detail
                            </button>
                            {row.status === 'draft' || row.status === 'created' ? (
                              <button
                                className="nv-button"
                                type="button"
                                disabled={busy}
                                onClick={() => void moveBatch(row.id, 'approve')}
                              >
                                Approve
                              </button>
                            ) : null}
                            {row.status === 'approved' ? (
                              <button
                                className="nv-button"
                                type="button"
                                disabled={busy}
                                onClick={() => void moveBatch(row.id, 'pay')}
                              >
                                Pay
                              </button>
                            ) : null}
                            {row.status !== 'paid' && row.status !== 'cancelled' ? (
                              <button
                                className="nv-button nv-button--danger"
                                type="button"
                                disabled={busy}
                                onClick={() => void moveBatch(row.id, 'cancel')}
                              >
                                Cancel
                              </button>
                            ) : null}
                            <button
                              className="nv-button nv-button--ghost"
                              type="button"
                              onClick={() =>
                                void download(
                                  `/money/payout-batches/${row.id}/export`,
                                  `payout-batch-${row.id}.csv`,
                                )
                              }
                            >
                              CSV
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : null}

            {batchDetail ? (
              <div>
                <h3 className="nv-h2">Batch #{batchDetail.id}</h3>
                <p className="nv-muted">
                  {money(batchDetail.total_minor, batchDetail.currency)} · {batchDetail.status} · created by{' '}
                  {batchDetail.created_by ?? '—'} · approved by {batchDetail.approved_by ?? '—'}
                </p>
                <div>
                  <label className="nv-label" htmlFor="fail-reason">
                    Failure reason (required to mark one item failed)
                  </label>
                  <input
                    className="nv-input"
                    id="fail-reason"
                    value={failReason}
                    onChange={(event) => setFailReason(event.target.value)}
                  />
                </div>
                <div className="nv-table-wrap">
                  <table className="nv-table">
                    <thead>
                      <tr>
                        <th scope="col">Student</th>
                        <th scope="col">Amount</th>
                        <th scope="col">Status</th>
                        <th scope="col">Reference</th>
                        <th scope="col">
                          <span className="nv-sr-only">Actions</span>
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {batchDetail.items.map((item) => (
                        <tr key={item.id}>
                          <td>
                            {item.name ?? `#${item.user_id}`}
                            <div className="nv-muted">{item.email}</div>
                          </td>
                          <td>{money(item.amount_minor, batchDetail.currency)}</td>
                          <td>
                            <Badge
                              tone={
                                item.status === 'paid'
                                  ? 'success'
                                  : item.status === 'failed'
                                    ? 'danger'
                                    : 'warning'
                              }
                            >
                              {item.status}
                            </Badge>
                          </td>
                          <td>{item.provider_reference ?? '—'}</td>
                          <td>
                            {item.status !== 'paid' && item.status !== 'failed' ? (
                              <button
                                className="nv-button nv-button--danger"
                                disabled={busy || failReason.trim().length < 3}
                                type="button"
                                onClick={() => void failPayoutItem(item.id)}
                              >
                                Mark failed
                              </button>
                            ) : null}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ) : null}
          </Panel>

          <Panel title="Ledger">
            {ledger.resource.status === 'loading' ? <Skeleton lines={4} /> : null}
            {ledger.resource.status === 'error' ? (
              <ErrorState title="Ledger did not load" body={ledger.resource.message} />
            ) : null}
            {ledger.resource.status === 'ready' && ledger.resource.data.transactions.length === 0 ? (
              <EmptyState
                title="Nothing has moved yet"
                body="Funding a project posts the first ledger transaction."
              />
            ) : null}
            {ledger.resource.status === 'ready' && ledger.resource.data.transactions.length > 0
              ? ledger.resource.data.transactions.map((transaction) => (
                  <div key={transaction.id}>
                    <p>
                      #{transaction.id} · {transaction.kind} ·{' '}
                      {money(transaction.total_minor, transaction.currency)}{' '}
                      <span className="nv-muted">{when(transaction.created_at)}</span>
                      {transaction.reverses_transaction_id ? (
                        <Badge tone="warning">reversal of #{transaction.reverses_transaction_id}</Badge>
                      ) : null}
                    </p>
                    <div className="nv-table-wrap">
                      <table className="nv-table">
                        <thead>
                          <tr>
                            <th scope="col">Account</th>
                            <th scope="col">Direction</th>
                            <th scope="col">Amount</th>
                            <th scope="col">User</th>
                            <th scope="col">Department</th>
                          </tr>
                        </thead>
                        <tbody>
                          {transaction.entries.map((entry) => (
                            <tr key={entry.id}>
                              <td>{entry.account}</td>
                              <td>{entry.direction}</td>
                              <td>{money(entry.amount_minor, entry.currency)}</td>
                              <td>{entry.user_id ?? '—'}</td>
                              <td>{entry.department_id ?? '—'}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                ))
              : null}
          </Panel>
        </>
      ) : null}
    </div>
  );
}

/**
 * The financials block, given a loaded payload.
 *
 * It takes the data as a prop rather than reading `resource.data` repeatedly: the
 * compiler cannot keep a union narrowed across a `.map` callback, and a screen
 * about money should not be guessing whether its totals exist.
 */
function Financials({ data }: { data: FinancialsOut }): JSX.Element {
  return (
    <>
      <p>
        {money(data.earning_total_minor, data.currency)} earned ·{' '}
        {money(data.student_pool_minor, data.currency)} student pool · {data.payment_status}
      </p>
      <p className="nv-muted">
        {Object.entries(data.earnings_by_status)
          .map(([key, value]) => `${key}: ${money(value, data.currency)}`)
          .join(' · ') || 'No earnings yet.'}
      </p>
      {data.department_share ? (
        <p className="nv-muted">
          Department {data.department_share.department_id ?? '—'} ·{' '}
          {money(data.department_share.amount_minor, data.department_share.currency)} ·{' '}
          {data.department_share.status}
        </p>
      ) : null}
    </>
  );
}
