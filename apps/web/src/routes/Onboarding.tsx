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
import * as React from 'react';
import { useNavigate } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { useSession } from '../lib/session';
import { Button, ErrorNote, Field, Select } from '../ui';

type Step = 'profile' | 'academic';

const PATHS: Array<{ value: string; label: string }> = [
  { value: 'academia', label: 'Academia — my courses and academic work' },
  { value: 'skills', label: 'Skills — short lessons and paid tasks' },
  { value: 'both', label: 'Both — show me everything' },
];

export function Onboarding(): JSX.Element {
  const { profile, reload } = useSession();
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

  async function loadCourses(id: string): Promise<void> {
    setDepartmentId(id);
    setPickedCourses([]);
    setCourses(id ? await http.get<Course[]>(`/onboarding/departments/${id}/courses`) : []);
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
      <div className="nv-steps" aria-label="Onboarding progress">
        <span className="nv-step" data-active={step === 'profile'}>
          1. You
        </span>
        <span aria-hidden>·</span>
        <span className="nv-step" data-active={step === 'academic'}>
          2. Your studies
        </span>
      </div>

      <ErrorNote message={error} />

      {step === 'profile' ? (
        <section className="nv-card">
          <h1 className="nv-h2">Let&apos;s set up your account</h1>
          <Field
            label="What should we call you?"
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            maxLength={150}
          />
          <Select
            label="Which path do you want first?"
            value={path}
            onChange={(e) => setPath(e.target.value)}
            options={PATHS}
          />
          <p className="nv-muted">
            You can switch later. {state?.has_enrolment ? 'Your courses are already saved.' : ''}
          </p>
          <Button
            type="button"
            disabled={busy || displayName.trim().length === 0}
            onClick={() => void saveProfile()}
          >
            {busy ? 'Saving…' : 'Continue'}
          </Button>
        </section>
      ) : (
        <section className="nv-card">
          <h1 className="nv-h2">Where do you study?</h1>
          {semester ? (
            <p className="nv-muted">
              {semester.name} ({semester.ordinal}) is the current semester.
            </p>
          ) : (
            <p className="nv-banner">
              No semester is open right now, so enrolment is paused. Your account still works.
            </p>
          )}

          <Select
            label="University"
            value={universityId}
            onChange={(e) => void loadFaculties(e.target.value)}
            options={[
              { value: '', label: 'Select…' },
              ...universities.map((u) => ({ value: String(u.id), label: u.name })),
            ]}
          />
          <Select
            label="Faculty"
            value={facultyId}
            disabled={!faculties.length}
            onChange={(e) => void loadDepartments(e.target.value)}
            options={[
              { value: '', label: faculties.length ? 'Select…' : 'Pick a university first' },
              ...faculties.map((f) => ({ value: String(f.id), label: f.name })),
            ]}
          />
          <Select
            label="Department"
            value={departmentId}
            disabled={!departments.length}
            onChange={(e) => void loadCourses(e.target.value)}
            options={[
              { value: '', label: departments.length ? 'Select…' : 'Pick a faculty first' },
              ...departments.map((d) => ({ value: String(d.id), label: d.name })),
            ]}
          />

          {courses.length > 0 ? (
            <fieldset className="nv-field">
              <legend className="nv-label">Courses this semester</legend>
              <ul className="nv-list">
                {courses.map((course) => (
                  <li key={course.id}>
                    <label className="nv-check">
                      <input
                        type="checkbox"
                        checked={pickedCourses.includes(course.id)}
                        onChange={() => toggleCourse(course.id)}
                      />
                      <span>
                        {course.code} — {course.title} ({course.level})
                      </span>
                    </label>
                  </li>
                ))}
              </ul>
            </fieldset>
          ) : null}

          <div className="nv-row">
            <Button type="button" variant="ghost" onClick={() => setStep('profile')}>
              Back
            </Button>
            <Button
              type="button"
              disabled={busy || !semester || pickedCourses.length === 0}
              onClick={() => void enrol()}
            >
              {busy ? 'Saving…' : 'Finish setup'}
            </Button>
          </div>
        </section>
      )}
    </div>
  );
}
