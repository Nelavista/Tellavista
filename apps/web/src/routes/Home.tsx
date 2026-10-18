import type { OnboardingState, Profile } from '@nelavista/contracts';
import * as React from 'react';

import { ApiError, http } from '../lib/http';
import { useSession } from '../lib/session';
import { Button, ErrorNote, Select } from '../ui';

const PATHS: Array<{ value: string; label: string }> = [
  { value: 'academia', label: 'Academia' },
  { value: 'skills', label: 'Skills' },
  { value: 'both', label: 'Both' },
];

export function Home(): JSX.Element {
  const { me, profile, reload } = useSession();
  const [state, setState] = React.useState<OnboardingState | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [busy, setBusy] = React.useState(false);

  React.useEffect(() => {
    void (async () => {
      try {
        setState(await http.get<OnboardingState>('/onboarding/state'));
      } catch (err) {
        setError(err instanceof ApiError ? err.message : 'Could not load your dashboard.');
      }
    })();
  }, []);

  async function switchPath(next: string): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      await http.post<Profile>('/me/path', { path: next });
      await reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not switch path.');
    } finally {
      setBusy(false);
    }
  }

  const name = profile?.display_name ?? me?.name ?? me?.username ?? 'there';

  return (
    <div className="nv-stack">
      <h1 className="nv-h1">Welcome, {name}</h1>

      {me && !me.email_verified ? (
        <p className="nv-banner">
          Confirm your email so we can send you proof and payout notices.
        </p>
      ) : null}

      <ErrorNote message={error} />

      <section className="nv-card">
        <h2 className="nv-h2">Your path</h2>
        <p className="nv-muted">
          Switching never deletes your learning, proof or earnings.
        </p>
        <Select
          label="Current path"
          value={profile?.preferred_path ?? 'both'}
          disabled={busy}
          onChange={(e) => void switchPath(e.target.value)}
          options={PATHS}
        />
      </section>

      <section className="nv-card">
        <h2 className="nv-h2">Your courses</h2>
        {state === null ? (
          <p className="nv-muted">Loading…</p>
        ) : state.enrolments.length === 0 ? (
          <p className="nv-muted">No courses yet.</p>
        ) : (
          <ul className="nv-list">
            {state.enrolments.map((row) => (
              <li key={row.enrolment_id}>
                <strong>{row.code}</strong> — {row.title}
                <div className="nv-muted">
                  {row.department} · {row.faculty} · {row.university} · {row.status}
                </div>
              </li>
            ))}
          </ul>
        )}
        {state?.current_semester ? (
          <p className="nv-muted">Current semester: {state.current_semester.name}</p>
        ) : null}
      </section>

      <Button variant="ghost" type="button" onClick={() => void reload()}>
        Refresh my data
      </Button>
    </div>
  );
}
