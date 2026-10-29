/**
 * Onboarding wizard (Phase 1): profile + path, then university → faculty →
 * department → courses → enrol. Every list comes from the API taxonomy, so a new
 * university is a data change, never a frontend change.
 */
import type {
  Course,
  Enrolment,
  OnboardingState,
  Profile,
  Semester,
  Subdivision,
  University,
} from '@nelavista/contracts';
import { Banner, Button, Checkbox, Field, PageHeader, Panel, Select } from '@nelavista/ui';
import { ArrowLeft, ArrowRight, GraduationCap } from 'lucide-react';
import * as React from 'react';
import { useNavigate } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { useSession } from '../lib/session';

type Step = 'profile' | 'academic';

const PATHS: Array<{ value: string; label: string }> = [
  { value: 'academia', label: 'Academia: my courses and academic work' },
  { value: 'skills', label: 'Skills: short lessons and paid tasks' },
  { value: 'both', label: 'Both: show me everything' },
];

const LEVELS: Array<{ value: string; label: string }> = [
  { value: '', label: 'All levels' },
  { value: '100', label: '100 level' },
  { value: '200', label: '200 level' },
  { value: '300', label: '300 level' },
  { value: '400', label: '400 level' },
  { value: '500', label: '500 level' },
  { value: '600', label: '600 level' },
];

export function Onboarding(): JSX.Element {
  const { me, profile, reload } = useSession();
  const navigate = useNavigate();

  const [step, setStep] = React.useState<Step>('profile');
  const [state, setState] = React.useState<OnboardingState | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [busy, setBusy] = React.useState(false);

  const [displayName, setDisplayName] = React.useState(profile?.display_name ?? '');
  const [path, setPath] = React.useState(profile?.preferred_path ?? 'both');

  const [universities, setUniversities] = React.useState<University[]>([]);
  const [faculties, setFaculties] = React.useState<Subdivision[]>([]);
  const [departments, setDepartments] = React.useState<Subdivision[]>([]);
  const [courses, setCourses] = React.useState<Course[]>([]);
  const [semester, setSemester] = React.useState<Semester | null>(null);

  const [universityId, setUniversityId] = React.useState('');
  const [facultyId, setFacultyId] = React.useState('');
  const [departmentId, setDepartmentId] = React.useState('');
  const [pickedCourses, setPickedCourses] = React.useState<number[]>([]);
  const [level, setLevel] = React.useState('');

  // Waitlist: an uncovered university is a signal for ops, not a dead end.
  const [waitlistName, setWaitlistName] = React.useState('');
  const [waitlistNote, setWaitlistNote] = React.useState('');
  const [waitlistNoteText, setWaitlistNoteText] = React.useState<string | null>(null);

  React.useEffect(() => {
    void (async () => {
      try {
        const [snapshot, unis, current] = await Promise.all([
          http.get<OnboardingState>('/onboarding/state'),
          http.get<University[]>('/onboarding/universities'),
          http.get<Semester | null>('/onboarding/sessions/current'),
        ]);
        setState(snapshot);
        setUniversities(unis);
        setSemester(current);
        if (snapshot.next_step !== 'enrol') setStep('profile');
        else setStep('academic');
      } catch (err) {
        setError(err instanceof ApiError ? err.message : 'Could not load onboarding.');
      }
    })();
  }, []);

  async function saveProfile(): Promise<void> {
    setError(null);
    setBusy(true);
    try {
      await http.patch<Profile>('/me', { display_name: displayName.trim() });
      await http.post<Profile>('/me/path', { path });
      await reload();
      setStep('academic');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not save your profile.');
    } finally {
      setBusy(false);
    }
  }

  async function loadFaculties(id: string): Promise<void> {
    setUniversityId(id);
    setFacultyId('');
    setDepartmentId('');
    setCourses([]);
    setPickedCourses([]);
    setFaculties(id ? await http.get<Subdivision[]>(`/onboarding/universities/${id}/faculties`) : []);
    setDepartments([]);
  }

  async function loadDepartments(id: string): Promise<void> {
    setFacultyId(id);
    setDepartmentId('');
    setCourses([]);
    setPickedCourses([]);
    setDepartments(id ? await http.get<Subdivision[]>(`/onboarding/faculties/${id}/departments`) : []);
  }

  async function loadCourses(id: string, selectedLevel = level): Promise<void> {
    setDepartmentId(id);
    setPickedCourses([]);
    const query = selectedLevel ? `?level=${encodeURIComponent(selectedLevel)}` : '';
    setCourses(id ? await http.get<Course[]>(`/onboarding/departments/${id}/courses${query}`) : []);
  }

  function changeLevel(next: string): void {
    setLevel(next);
    if (departmentId) void loadCourses(departmentId, next);
  }

  async function joinWaitlist(): Promise<void> {
    if (waitlistName.trim().length < 2) {
      setError('Enter your university name.');
      return;
    }
    setBusy(true);
    setError(null);
    setWaitlistNoteText(null);
    try {
      const result = await http.post<{ message: string }>('/onboarding/waitlist', {
        university_name: waitlistName.trim(),
        email: me?.email,
        note: waitlistNote.trim() || null,
      });
      setWaitlistNoteText(result.message);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not add you to the list.');
    } finally {
      setBusy(false);
    }
  }

  function toggleCourse(id: number): void {
    setPickedCourses((current) =>
      current.includes(id) ? current.filter((c) => c !== id) : [...current, id],
    );
  }

  async function enrol(): Promise<void> {
    if (!semester || pickedCourses.length === 0) {
      setError('Pick at least one course to continue.');
      return;
    }
    setError(null);
    setBusy(true);
    try {
      const rows = await http.post<Enrolment[]>('/onboarding/enrol', {
        course_ids: pickedCourses,
        session_id: semester.session_id,
        semester_id: semester.id,
      });
      if (rows.length === 0) throw new Error('empty');
      await http.post('/me/onboarding/complete');
      await reload();
      navigate('/home', { replace: true });
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not save your courses.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Setup"
        title={step === 'profile' ? 'Set up your account' : 'Where do you study?'}
        description={
          step === 'profile'
            ? 'Two steps: who you are and how you want to learn, then your university and courses.'
            : 'Your courses decide which materials, practice and CBT papers are available.'
        }
      />

      <div className="nv-steps" aria-label="Onboarding progress">
        <span className="nv-step" data-active={step === 'profile'} data-done={step === 'academic'}>
          1. You
        </span>
        <span aria-hidden>·</span>
        <span className="nv-step" data-active={step === 'academic'}>
          2. Your studies
        </span>
      </div>

      {error ? (
        <Banner tone="danger">
          <p>{error}</p>
        </Banner>
      ) : null}

      {step === 'profile' ? (
        <Panel title="You">
          <div className="nv-stack">
            <Field
              hint="This appears on a shared profile."
              label="What should we call you?"
              maxLength={150}
              value={displayName}
              onChange={(event) => setDisplayName(event.target.value)}
            />
            <Select
              label="Which path do you want first?"
              options={PATHS}
              value={path}
              onChange={(event) => setPath(event.target.value)}
            />
            <p className="nv-muted">
              You can switch later. {state?.has_enrolment ? 'Your courses are already saved.' : ''}
            </p>
            <div>
              <Button
                disabled={busy || displayName.trim().length === 0}
                type="button"
                onClick={() => void saveProfile()}
              >
                {busy ? 'Saving…' : 'Continue'}
                <ArrowRight aria-hidden="true" size={15} />
              </Button>
            </div>
          </div>
        </Panel>
      ) : (
        <Panel title="Your studies" actions={<GraduationCap aria-hidden="true" size={16} />}>
          <div className="nv-stack">
            {semester ? (
              <p className="nv-muted">
                {semester.name} ({semester.ordinal}) is the current semester.
              </p>
            ) : (
              <Banner tone="warning">
                <p>No semester is open right now, so enrolment is paused. Your account still works.</p>
              </Banner>
            )}

            <Select
              label="University"
              options={[
                { value: '', label: 'Select…' },
                ...universities.map((u) => ({ value: String(u.id), label: u.name })),
              ]}
              value={universityId}
              onChange={(event) => void loadFaculties(event.target.value)}
            />
            <Select
              disabled={!faculties.length}
              label="Faculty"
              options={[
                { value: '', label: faculties.length ? 'Select…' : 'Pick a university first' },
                ...faculties.map((f) => ({ value: String(f.id), label: f.name })),
              ]}
              value={facultyId}
              onChange={(event) => void loadDepartments(event.target.value)}
            />
            <Select
              disabled={!departments.length}
              label="Department"
              options={[
                { value: '', label: departments.length ? 'Select…' : 'Pick a faculty first' },
                ...departments.map((d) => ({ value: String(d.id), label: d.name })),
              ]}
              value={departmentId}
              onChange={(event) => void loadCourses(event.target.value)}
            />
            <Select
              disabled={!departmentId}
              label="Level"
              options={LEVELS}
              value={level}
              onChange={(event) => changeLevel(event.target.value)}
            />

            {courses.length > 0 ? (
              <fieldset className="nv-field">
                <legend className="nv-label">Courses this semester</legend>
                <ul className="nv-list">
                  {courses.map((course) => (
                    <li key={course.id}>
                      <Checkbox
                        checked={pickedCourses.includes(course.id)}
                        label={`${course.code}: ${course.title} (${course.level})`}
                        onChange={() => toggleCourse(course.id)}
                      />
                    </li>
                  ))}
                </ul>
              </fieldset>
            ) : null}

            <details className="nv-card nv-card--flat">
              <summary>My university is not listed</summary>
              <div className="nv-stack" style={{ marginTop: 'var(--nv-space-md)' }}>
                <p className="nv-muted">
                  Tell us where you study. We add universities in batches; your account and any other
                  enrolment are unaffected.
                </p>
                <Field
                  label="University name"
                  maxLength={200}
                  value={waitlistName}
                  onChange={(event) => setWaitlistName(event.target.value)}
                />
                <Field
                  label="Anything we should know? (optional)"
                  maxLength={500}
                  value={waitlistNote}
                  onChange={(event) => setWaitlistNote(event.target.value)}
                />
                <div>
                  <Button disabled={busy} type="button" variant="ghost" onClick={() => void joinWaitlist()}>
                    {busy ? 'Sending…' : 'Join the waitlist'}
                  </Button>
                </div>
                {waitlistNoteText ? (
                  <Banner tone="success">
                    <p>{waitlistNoteText}</p>
                  </Banner>
                ) : null}
              </div>
            </details>

            <div className="nv-row nv-row--between">
              <Button type="button" variant="ghost" onClick={() => setStep('profile')}>
                <ArrowLeft aria-hidden="true" size={15} />
                Back
              </Button>
              <Button
                disabled={busy || !semester || pickedCourses.length === 0}
                type="button"
                onClick={() => void enrol()}
              >
                {busy ? 'Saving…' : 'Finish setup'}
                <ArrowRight aria-hidden="true" size={15} />
              </Button>
            </div>
          </div>
        </Panel>
      )}
    </div>
  );
}
