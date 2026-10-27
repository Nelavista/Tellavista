/**
 * Home: the next action, not a welcome page.
 *
 * The onboarding state decides what the student can do now. Everything else on
 * the page supports that one action: confirm the email, finish the path, add
 * courses, or open the dashboard. No invented metrics.
 */
import type { OnboardingState, Profile } from '@nelavista/contracts';
import {
  Badge,
  Banner,
  Button,
  EmptyState,
  ErrorState,
  PageHeader,
  Panel,
  Select,
  Skeleton,
} from '@nelavista/ui';
import { ArrowRight, BookOpen, GraduationCap, MailCheck } from 'lucide-react';
import * as React from 'react';
import { Link } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { useSession } from '../lib/session';

const PATHS: Array<{ value: string; label: string }> = [
  { value: 'academia', label: 'Academia' },
  { value: 'skills', label: 'Skills' },
  { value: 'both', label: 'Both' },
];

export function Home(): JSX.Element {
  const { me, profile, reload } = useSession();
  const [state, setState] = React.useState<OnboardingState | null>(null);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);
  const [attempt, setAttempt] = React.useState(0);
  const [busy, setBusy] = React.useState(false);
  const [verifyNote, setVerifyNote] = React.useState<string | null>(null);
  const [resending, setResending] = React.useState(false);

  const name = profile?.display_name ?? me?.name ?? me?.username ?? 'there';

  React.useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    void (async () => {
      try {
        const next = await http.get<OnboardingState>('/onboarding/state');
        if (!cancelled) setState(next);
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof ApiError ? err.message : 'Could not load your dashboard.');
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [attempt]);

  async function resendVerification(): Promise<void> {
    setResending(true);
    setVerifyNote(null);
    try {
      const result = await http.post<{ message: string }>('/auth/email/verify/resend');
      setVerifyNote(result.message);
    } catch (err) {
      setVerifyNote(err instanceof ApiError ? err.message : 'Could not send the email.');
    } finally {
      setResending(false);
    }
  }

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

  const next = state?.next_step ?? null;

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Home"
        title="What to do next"
        description={`You are signed in as ${name}. The next step is the one thing this page is for; the rest is context.`}
      />

      {me && !me.email_verified ? (
        <Banner
          tone="warning"
          actions={
            <Button
              disabled={resending}
              size="sm"
              type="button"
              variant="secondary"
              onClick={() => void resendVerification()}
            >
              <MailCheck aria-hidden="true" size={15} />
              {resending ? 'Sending…' : 'Send the link again'}
            </Button>
          }
        >
          <p>Confirm your email so proof and payout notices reach you.</p>
          {verifyNote ? <p className="nv-meta">{verifyNote}</p> : null}
        </Banner>
      ) : null}

      {loading ? (
        <Panel title="Your next step">
          <Skeleton lines={3} />
        </Panel>
      ) : null}

      {!loading && error ? (
        <Panel title="Your next step">
          <ErrorState
            body={error}
            action={
              <Button size="sm" type="button" variant="secondary" onClick={() => setAttempt((n) => n + 1)}>
                Try again
              </Button>
            }
          />
        </Panel>
      ) : null}

      {!loading && !error && state ? (
        <Panel
          title="Your next step"
          actions={<Badge tone="info">{next === 'ready' ? 'Ready' : 'Setup'}</Badge>}
        >
          {next === 'choose_path' ? (
            <div className="nv-stack">
              <div>
                <p className="nv-h2">Choose how you want to learn</p>
                <p className="nv-muted">
                  Academia follows your university courses. Skills follows published paths. You can switch
                  later without losing learning, proof or earnings.
                </p>
              </div>
              <Select
                disabled={busy}
                label="Current path"
                options={PATHS}
                value={profile?.preferred_path ?? 'both'}
                onChange={(event) => void switchPath(event.target.value)}
              />
            </div>
          ) : null}

          {next === 'enrol' ? (
            <div className="nv-stack">
              <div>
                <p className="nv-h2">Add your courses</p>
                <p className="nv-muted">
                  Your courses decide which materials, practice and CBT papers are available. Nothing outside
                  them is searchable.
                </p>
              </div>
              <div>
                <Link className="nv-button" to="/onboarding">
                  <BookOpen aria-hidden="true" size={15} />
                  Add your courses
                </Link>
              </div>
            </div>
          ) : null}

          {next === 'ready' ? (
            <div className="nv-stack">
              <div>
                <p className="nv-h2">Open your Academia dashboard</p>
                <p className="nv-muted">
                  See what you are studying, what you studied recently, what to practise, and where you are
                  weak.
                </p>
              </div>
              <div className="nv-row">
                <Link className="nv-button" to="/academia">
                  <GraduationCap aria-hidden="true" size={15} />
                  Open the dashboard
                  <ArrowRight aria-hidden="true" size={15} />
                </Link>
                <Link className="nv-button nv-button--ghost" to="/skills">
                  Browse skills
                </Link>
              </div>
            </div>
          ) : null}
        </Panel>
      ) : null}

      <Panel
        title="Your courses"
        actions={
          state?.current_semester ? <span className="nv-meta">{state.current_semester.name}</span> : null
        }
      >
        {loading ? <Skeleton lines={4} /> : null}
        {!loading && !error && state && state.enrolments.length === 0 ? (
          <EmptyState
            body="Courses decide which materials and practice are available. Add them during onboarding."
            icon={BookOpen}
            title="No courses yet"
            action={
              <Link className="nv-button nv-button--secondary nv-button--sm" to="/onboarding">
                Add your courses
              </Link>
            }
          />
        ) : null}
        {!loading && !error && state && state.enrolments.length > 0 ? (
          <div className="nv-table-wrap">
            <table className="nv-table">
              <thead>
                <tr>
                  <th>Code</th>
                  <th>Course</th>
                  <th>Department</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {state.enrolments.map((row) => (
                  <tr key={row.enrolment_id}>
                    <td className="nv-mono">{row.code}</td>
                    <td>{row.title}</td>
                    <td>
                      {row.department}
                      <div className="nv-muted">{row.faculty}</div>
                    </td>
                    <td>
                      <Badge tone={row.status === 'active' ? 'success' : 'neutral'}>{row.status}</Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : null}
      </Panel>

      <div className="nv-row nv-row--between">
        <p className="nv-meta">Signed in as {me?.username ?? 'student'}</p>
        <Button
          size="sm"
          type="button"
          variant="ghost"
          onClick={() => {
            setAttempt((n) => n + 1);
            void reload();
          }}
        >
          Refresh my data
        </Button>
      </div>
    </div>
  );
}
