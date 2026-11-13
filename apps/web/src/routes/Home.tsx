/**
 * Home: the next action, then the working view.
 *
 * The onboarding state decides what the student can do now. The summary strip
 * reports only values the API returned; the primary column puts the next step
 * and the courses table in reading order; the rail is a context switch, not
 * the main content.
 */
import type { OnboardingState, PreferredPath, Profile } from '@nelavista/contracts';
import { Badge, Banner, Button, EmptyState, ErrorState, Panel, Skeleton } from '@nelavista/ui';
import {
  ArrowRight,
  BookOpen,
  Briefcase,
  Check,
  GraduationCap,
  MailCheck,
  MapPin,
  Sparkles,
  type LucideIcon,
} from 'lucide-react';
import * as React from 'react';
import { Link, useNavigate } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { PATH_OPTIONS, isPreferredPath, pathDestination, pathNeedsStudies, pathOption } from '../lib/paths';
import { useSession } from '../lib/session';

const PATH_ICONS: Record<PreferredPath, LucideIcon> = {
  academia: GraduationCap,
  skills: Sparkles,
  opportunities: Briefcase,
  campus: MapPin,
};

function metricValue(label: string, value: string | number, context: string): JSX.Element {
  return (
    <>
      <dt>{label}</dt>
      <dd>
        {value}
        <span className="nv-metric__context">{context}</span>
      </dd>
    </>
  );
}

export function Home(): JSX.Element {
  const { me, profile, reload } = useSession();
  const navigate = useNavigate();
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

  async function switchPath(next: PreferredPath): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      await http.post<Profile>('/me/path', { path: next });
      await reload();
      const academicUniversity =
        typeof state?.academic?.university === 'string' ? state.academic.university : null;
      const needsSetup =
        next === 'campus' ? !academicUniversity : pathNeedsStudies(next) && !(state?.has_enrolment ?? false);
      navigate(needsSetup ? '/onboarding?step=studies' : pathDestination(next));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not switch space.');
    } finally {
      setBusy(false);
    }
  }

  const next = state?.next_step ?? null;
  const currentPath = isPreferredPath(profile?.preferred_path) ? profile.preferred_path : null;
  const currentOption = pathOption(currentPath);
  const CurrentIcon = currentOption ? PATH_ICONS[currentOption.value] : null;
  const currentDestination = pathDestination(currentPath);
  const currentSecondary =
    currentPath === 'academia'
      ? { to: '/academia/materials', label: 'Materials' }
      : currentPath === 'skills'
        ? { to: '/skills/my-learning', label: 'My learning' }
        : currentPath === 'opportunities'
          ? { to: '/opportunities/applications', label: 'My applications' }
          : null;
  const semesterName = state?.current_semester?.name ?? 'Not set';
  const nextLabel =
    next === 'ready'
      ? 'Ready'
      : next === 'enrol'
        ? 'Add courses'
        : next === 'choose_path'
          ? 'Choose a space'
          : '—';
  const nextContext =
    next === 'ready'
      ? 'All setup steps done'
      : next === 'enrol'
        ? 'One step left'
        : next === 'choose_path'
          ? 'Pick a space'
          : 'Not loaded';
  const measured = !loading && !error;

  return (
    <div className="nv-workspace">
      <header className="nv-workspace__header">
        <div>
          <h1 className="nv-h1">Good to see you, {name}.</h1>
          <p className="nv-workspace__context">
            {loading
              ? 'Loading your workspace.'
              : error
                ? 'Your workspace could not load. Retry from the next step panel.'
                : state?.current_semester
                  ? `Current semester: ${state.current_semester.name}.`
                  : 'No semester on record yet.'}
          </p>
        </div>
        {!loading && !error && state ? (
          <Badge tone={next === 'ready' ? 'success' : 'neutral'}>
            {next === 'ready' ? 'Setup complete' : 'Setup in progress'}
          </Badge>
        ) : null}
      </header>

      {loading ? (
        <div className="nv-metrics" aria-hidden="true">
          <div className="nv-metric">
            <Skeleton lines={2} />
          </div>
          <div className="nv-metric">
            <Skeleton lines={2} />
          </div>
          <div className="nv-metric">
            <Skeleton lines={2} />
          </div>
          <div className="nv-metric">
            <Skeleton lines={2} />
          </div>
        </div>
      ) : (
        <dl className="nv-metrics" aria-label="Your workspace at a glance">
          <div className="nv-metric">
            {metricValue('Courses', measured ? (state?.enrolments.length ?? 0) : '—', 'On your record')}
          </div>
          <div className="nv-metric">
            {metricValue('Semester', measured ? semesterName : '—', 'Current semester')}
          </div>
          <div className="nv-metric">
            {metricValue('Space', measured ? (currentOption?.label ?? 'Not chosen') : '—', 'Chosen space')}
          </div>
          <div className="nv-metric">
            <dt>Next</dt>
            <dd>
              {measured ? nextLabel : '—'}
              <span className="nv-metric__context">{measured ? nextContext : 'Unavailable'}</span>
            </dd>
          </div>
        </dl>
      )}

      <div className="nv-workspace__grid">
        <div className="nv-workspace__primary">
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
                  <Button
                    size="sm"
                    type="button"
                    variant="secondary"
                    onClick={() => setAttempt((n) => n + 1)}
                  >
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
                <div className="nv-next">
                  <p className="nv-next__lead">Choose your space.</p>
                  <p className="nv-next__body">
                    Choose one of the four spaces. You can switch later without losing learning, proof or
                    earnings.
                  </p>
                </div>
              ) : null}

              {next === 'enrol' ? (
                <div className="nv-next">
                  <p className="nv-next__lead">Add your courses.</p>
                  <p className="nv-next__body">
                    Your courses decide which materials, practice and CBT papers are available. Nothing
                    outside them is searchable.
                  </p>
                  <div>
                    <Link className="nv-button" to="/onboarding">
                      <BookOpen aria-hidden="true" size={15} />
                      Add your courses
                    </Link>
                  </div>
                </div>
              ) : null}

              {next === 'ready' ? (
                <div className="nv-next">
                  <p className="nv-next__lead">Open your {currentOption?.label ?? 'dashboard'}.</p>
                  <p className="nv-next__body">
                    {currentOption?.detail ??
                      'Your space is ready. Switch space from Your space whenever your semester changes.'}
                  </p>
                  <div className="nv-row">
                    <Link className="nv-button" to={currentDestination}>
                      {CurrentIcon ? <CurrentIcon aria-hidden="true" size={15} /> : null}
                      Open {currentOption?.label ?? 'dashboard'}
                      <ArrowRight aria-hidden="true" size={15} />
                    </Link>
                    {currentSecondary ? (
                      <Link className="nv-button nv-button--ghost" to={currentSecondary.to}>
                        {currentSecondary.label}
                      </Link>
                    ) : null}
                  </div>
                </div>
              ) : null}
            </Panel>
          ) : null}

          {!loading && !error ? (
            <Panel
              title="Your courses"
              actions={
                state?.current_semester ? (
                  <span className="nv-meta">{state.current_semester.name}</span>
                ) : null
              }
            >
              {state && state.enrolments.length === 0 ? (
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
              {state && state.enrolments.length > 0 ? (
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
          ) : null}
        </div>

        <aside className="nv-workspace__rail" aria-label="Workspace settings">
          <Panel
            title="Your space"
            actions={
              currentOption ? <Badge tone="info">{currentOption.label}</Badge> : <Badge>Not chosen</Badge>
            }
          >
            <div className="nv-space-switcher nv-space-switcher--rail">
              {PATH_OPTIONS.map((option) => {
                const Icon = PATH_ICONS[option.value];
                const selected = currentPath === option.value;
                return (
                  <button
                    className="nv-space-option"
                    data-selected={selected}
                    disabled={busy || loading}
                    key={option.value}
                    type="button"
                    onClick={() => void switchPath(option.value)}
                  >
                    <span className="nv-space-option__icon" aria-hidden="true">
                      <Icon size={17} strokeWidth={1.7} />
                    </span>
                    <span className="nv-space-option__copy">
                      <strong>{option.label}</strong>
                      <span>{option.summary}</span>
                    </span>
                    {selected ? (
                      <Check aria-hidden="true" size={15} strokeWidth={2.2} />
                    ) : (
                      <ArrowRight aria-hidden="true" size={15} />
                    )}
                  </button>
                );
              })}
            </div>
            <p className="nv-meta">Switching never deletes courses, proof or earnings.</p>
          </Panel>

          <Panel title="Your account">
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
          </Panel>
        </aside>
      </div>
    </div>
  );
}
