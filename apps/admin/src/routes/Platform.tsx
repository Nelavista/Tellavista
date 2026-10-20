/**
 * Platform settings (G1–G5).
 *
 * Currency, payout approval, age rules, the contributor terms and curriculum
 * ownership are policy, not code. This screen edits them; the API validates them
 * and the services that spend money or start work read the same row, so a change
 * here is live on the next request without a deploy.
 *
 * Only a super admin may save. The form still renders for ops so the rules are
 * visible, but the save button explains why it will be refused.
 */
import type { PlatformSettingsOut } from '@nelavista/api-client';
import * as React from 'react';

import { ApiError, http } from '../lib/http';
import { useResource } from '../lib/resource';
import { useSession } from '../lib/session';
import { when } from '../lib/format';

const AUTHORING_MODELS: Array<{ value: string; label: string }> = [
  { value: 'in_house', label: 'In-house authors' },
  { value: 'community', label: 'Community contributors' },
  { value: 'partner', label: 'University or industry partner' },
];

interface FormState {
  billing_currency: string;
  payout_currency: string;
  allowed_currencies: string;
  payout_second_approver_threshold_major: string;
  payout_second_approver_always: boolean;
  payout_require_verified_email: boolean;
  min_student_age: string;
  guardian_consent_below_age: string;
  terms_version: string;
  contributor_terms_version: string;
  contributor_terms_body: string;
  curriculum_owner: string;
  curriculum_license: string;
  curriculum_authoring_model: string;
  target_launch_date: string;
}

function toForm(data: PlatformSettingsOut): FormState {
  return {
    billing_currency: data.billing_currency,
    payout_currency: data.payout_currency,
    allowed_currencies: data.allowed_currencies.join(', '),
    // The API stores minor units; admins think in the currency's major unit.
    payout_second_approver_threshold_major: (data.payout_second_approver_threshold_minor / 100).toFixed(2),
    payout_second_approver_always: data.payout_second_approver_always,
    payout_require_verified_email: data.payout_require_verified_email,
    min_student_age: String(data.min_student_age),
    guardian_consent_below_age: String(data.guardian_consent_below_age),
    terms_version: data.terms_version,
    contributor_terms_version: data.contributor_terms_version,
    contributor_terms_body: data.contributor_terms_body,
    curriculum_owner: data.curriculum_owner,
    curriculum_license: data.curriculum_license,
    curriculum_authoring_model: data.curriculum_authoring_model,
    target_launch_date: data.target_launch_date ?? '',
  };
}

export function Platform(): JSX.Element {
  const { me } = useSession();
  const resource = useResource<PlatformSettingsOut>('/platform/settings');
  const [form, setForm] = React.useState<FormState | null>(null);
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [note, setNote] = React.useState<string | null>(null);

  React.useEffect(() => {
    if (resource.resource.status === 'ready') setForm(toForm(resource.resource.data));
  }, [resource.resource]);

  const canWrite = me?.role === 'super_admin';

  function update<K extends keyof FormState>(key: K, value: FormState[K]): void {
    setForm((current) => (current ? { ...current, [key]: value } : current));
  }

  async function save(): Promise<void> {
    if (!form) return;
    setBusy(true);
    setError(null);
    setNote(null);
    try {
      await http.patch<PlatformSettingsOut>('/platform/settings', {
        billing_currency: form.billing_currency.trim().toUpperCase(),
        payout_currency: form.payout_currency.trim().toUpperCase(),
        allowed_currencies: form.allowed_currencies
          .split(',')
          .map((code) => code.trim().toUpperCase())
          .filter(Boolean),
        payout_second_approver_threshold_minor: Math.max(
          0,
          Math.round(Number(form.payout_second_approver_threshold_major || '0') * 100),
        ),
        payout_second_approver_always: form.payout_second_approver_always,
        payout_require_verified_email: form.payout_require_verified_email,
        min_student_age: Number(form.min_student_age),
        guardian_consent_below_age: Number(form.guardian_consent_below_age),
        terms_version: form.terms_version.trim(),
        contributor_terms_version: form.contributor_terms_version.trim(),
        contributor_terms_body: form.contributor_terms_body,
        curriculum_owner: form.curriculum_owner.trim(),
        curriculum_license: form.curriculum_license.trim(),
        curriculum_authoring_model: form.curriculum_authoring_model,
        target_launch_date: form.target_launch_date || null,
      });
      setNote('Saved. The next request uses the new policy; the change is in the audit trail.');
      resource.reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not save those settings.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="nv-stack">
      <h1 className="nv-h1">Platform settings</h1>
      <p className="nv-muted">
        Currency, payout approval, age rules, contributor terms and curriculum ownership. Changes apply
        immediately and are audited with their before and after values.
      </p>

      {error ? <p className="nv-error">{error}</p> : null}
      {note ? <p className="nv-muted">{note}</p> : null}

      {resource.resource.status === 'error' ? (
        <p className="nv-error">{resource.resource.message}</p>
      ) : null}

      {form ? (
        <>
          <section className="nv-card">
            <h2 className="nv-h2">Money (G1)</h2>
            <p className="nv-muted">
              The ledger is currency-agnostic and stores integer minor units. The billing currency is
              used when a project does not name one; the payout currency is the default reported to
              students. A currency must be in the allowed list before it can be selected.
            </p>
            <div className="nv-grid">
              <div>
                <label className="nv-label" htmlFor="billing-currency">Billing currency</label>
                <input
                  className="nv-input"
                  id="billing-currency"
                  maxLength={3}
                  value={form.billing_currency}
                  onChange={(e) => update('billing_currency', e.target.value.toUpperCase())}
                />
              </div>
              <div>
                <label className="nv-label" htmlFor="payout-currency">Payout currency</label>
                <input
                  className="nv-input"
                  id="payout-currency"
                  maxLength={3}
                  value={form.payout_currency}
                  onChange={(e) => update('payout_currency', e.target.value.toUpperCase())}
                />
              </div>
              <div style={{ gridColumn: '1 / -1' }}>
                <label className="nv-label" htmlFor="allowed-currencies">
                  Allowed currencies (comma separated ISO codes)
                </label>
                <input
                  className="nv-input"
                  id="allowed-currencies"
                  value={form.allowed_currencies}
                  onChange={(e) => update('allowed_currencies', e.target.value)}
                />
              </div>
            </div>
          </section>

          <section className="nv-card">
            <h2 className="nv-h2">Payout approvals and identity (G2)</h2>
            <div className="nv-grid">
              <div>
                <label className="nv-label" htmlFor="threshold">
                  Second approver above ({form.payout_currency}, major units)
                </label>
                <input
                  className="nv-input"
                  id="threshold"
                  type="number"
                  min={0}
                  step="0.01"
                  value={form.payout_second_approver_threshold_major}
                  onChange={(e) => update('payout_second_approver_threshold_major', e.target.value)}
                />
              </div>
              <label className="nv-check">
                <input
                  type="checkbox"
                  checked={form.payout_second_approver_always}
                  onChange={(e) => update('payout_second_approver_always', e.target.checked)}
                />
                Always require a second approver, even below the threshold
              </label>
              <label className="nv-check">
                <input
                  type="checkbox"
                  checked={form.payout_require_verified_email}
                  onChange={(e) => update('payout_require_verified_email', e.target.checked)}
                />
                Refuse to pay a student whose email is unverified
              </label>
            </div>
            <p className="nv-muted">
              The threshold is stored in minor units. A batch at or above it cannot be approved by the
              person who created it, and payment is blocked before the provider is called.
            </p>
          </section>

          <section className="nv-card">
            <h2 className="nv-h2">Ages and terms (G3)</h2>
            <div className="nv-grid">
              <div>
                <label className="nv-label" htmlFor="min-age">Minimum age for paid work</label>
                <input
                  className="nv-input"
                  id="min-age"
                  type="number"
                  min={13}
                  max={25}
                  value={form.min_student_age}
                  onChange={(e) => update('min_student_age', e.target.value)}
                />
              </div>
              <div>
                <label className="nv-label" htmlFor="guardian-age">Guardian consent below</label>
                <input
                  className="nv-input"
                  id="guardian-age"
                  type="number"
                  min={13}
                  max={25}
                  value={form.guardian_consent_below_age}
                  onChange={(e) => update('guardian_consent_below_age', e.target.value)}
                />
              </div>
              <div>
                <label className="nv-label" htmlFor="contributor-version">Contributor terms version</label>
                <input
                  className="nv-input"
                  id="contributor-version"
                  maxLength={20}
                  value={form.contributor_terms_version}
                  onChange={(e) => update('contributor_terms_version', e.target.value)}
                />
              </div>
              <div>
                <label className="nv-label" htmlFor="terms-version">General terms version</label>
                <input
                  className="nv-input"
                  id="terms-version"
                  maxLength={20}
                  value={form.terms_version}
                  onChange={(e) => update('terms_version', e.target.value)}
                />
              </div>
            </div>
            <label className="nv-label" htmlFor="contributor-body">Contributor terms (shown to students)</label>
            <textarea
              className="nv-input"
              id="contributor-body"
              rows={10}
              value={form.contributor_terms_body}
              onChange={(e) => update('contributor_terms_body', e.target.value)}
            />
            <p className="nv-muted">
              Changing the version asks every student to accept again. Previous agreements stay in the
              consent history; they are never edited or deleted.
            </p>
          </section>

          <section className="nv-card">
            <h2 className="nv-h2">Curriculum ownership (G4) and launch (G5)</h2>
            <div className="nv-grid">
              <div>
                <label className="nv-label" htmlFor="curriculum-owner">Owner</label>
                <input
                  className="nv-input"
                  id="curriculum-owner"
                  value={form.curriculum_owner}
                  onChange={(e) => update('curriculum_owner', e.target.value)}
                />
              </div>
              <div>
                <label className="nv-label" htmlFor="curriculum-license">Licence</label>
                <input
                  className="nv-input"
                  id="curriculum-license"
                  value={form.curriculum_license}
                  onChange={(e) => update('curriculum_license', e.target.value)}
                />
              </div>
              <div>
                <label className="nv-label" htmlFor="curriculum-model">Authoring model</label>
                <select
                  className="nv-select"
                  id="curriculum-model"
                  value={form.curriculum_authoring_model}
                  onChange={(e) => update('curriculum_authoring_model', e.target.value)}
                >
                  {AUTHORING_MODELS.map((option) => (
                    <option key={option.value} value={option.value}>{option.label}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="nv-label" htmlFor="launch-date">Target launch date</label>
                <input
                  className="nv-input"
                  id="launch-date"
                  type="date"
                  value={form.target_launch_date}
                  onChange={(e) => update('target_launch_date', e.target.value)}
                />
              </div>
            </div>
            <p className="nv-muted">
              The owner and licence are shown with published curriculum. The authoring model records how
              content is sourced, so a later audit can tell in-house material from contributed material.
            </p>
          </section>

          <div className="nv-row">
            <button
              className="nv-button"
              disabled={busy || !canWrite}
              type="button"
              onClick={() => void save()}
            >
              Save settings
            </button>
            <span className="nv-muted">
              {canWrite
                ? 'Saving is audited with your account and the changed fields.'
                : 'Only a super admin can change these settings.'}
            </span>
          </div>
          <p className="nv-muted">Last updated {when(resource.resource.status === 'ready' ? resource.resource.data.updated_at : null)}.</p>
        </>
      ) : (
        <p className="nv-muted">Loading settings…</p>
      )}
    </div>
  );
}
