/**
 * Onboarding: the student picks one of four spaces, then supplies only the
 * context that space actually reads.
 *
 * Academia needs a university and courses. Campus needs the university only.
 * Skills and Opportunities need neither, so their onboarding ends at step one
 * instead of forcing an academic form they will never use.
 */
import type {
  Course,
  Enrolment,
  OnboardingState,
  PreferredPath,
  Profile,
  Semester,
  Subdivision,
  University,
} from '@nelavista/contracts';
import {
  Banner,
  Button,
  Checkbox,
  ErrorState,
  Field,
  PageHeader,
  Panel,
  Select,
  Skeleton,
} from '@nelavista/ui';
import {
  ArrowLeft,
  ArrowRight,
  Briefcase,
  Check,
  GraduationCap,
  MapPin,
  Sparkles,
  type LucideIcon,
} from 'lucide-react';
import * as React from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';

import { ApiError, http } from '../lib/http';
import { PATH_OPTIONS, isPreferredPath, pathDestination, pathNeedsStudies, pathOption } from '../lib/paths';
import { useSession } from '../lib/session';

type Step = 'profile' | 'studies';

const LEVELS: Array<{ value: string; label: string }> = [
  { value: '', label: 'All levels' },
  { value: '100', label: '100 level' },
  { value: '200', label: '200 level' },
  { value: '300', label: '300 level' },
  { value: '400', label: '400 level' },
  { value: '500', label: '500 level' },
  { value: '600', label: '600 level' },
];

const PATH_ICONS: Record<PreferredPath, LucideIcon> = {
  academia: GraduationCap,
  skills: Sparkles,
  opportunities: Briefcase,
  campus: MapPin,
};

const NEXT_STEPS: Record<PreferredPath, string[]> = {
  academia: [
    'Choose your university, department and courses.',
    'Read materials and practise CBT for those courses.',
    'Verification stays separate from coursework.',
  ],
  skills: [
    'Open the published skills catalogue.',
    'Follow a path one lesson at a time.',
    'Verification comes from an assessment, not a finished lesson.',
  ],
  opportunities: [
    'Matching uses the skills you have already proved.',
    'Open a role to see why you fit and what is missing.',
    'Applications and their notes stay in your record.',
  ],
  campus: [
    'Choose the university whose campus you want to read.',
    'Campus shows live information and map points for it.',
    'You can add courses later without losing this choice.',
  ],
};

function progressState(current: Step, target: Step, path: PreferredPath | null): string {
  if (current === target) return 'current';
  if (target === 'profile') return 'complete';
  return pathNeedsStudies(path) ? 'upcoming' : 'next';
}

export function Onboarding(): JSX.Element {
  const { me, profile, reload } = useSession();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const [step, setStep] = React.useState<Step>('profile');
  const [state, setState] = React.useState<OnboardingState | null>(null);
  const [initialLoading, setInitialLoading] = React.useState(true);
  const [loadError, setLoadError] = React.useState<string | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [busy, setBusy] = React.useState(false);

  const initialPath: PreferredPath | null = isPreferredPath(profile?.preferred_path)
    ? profile.preferred_path
    : null;
  const [displayName, setDisplayName] = React.useState(profile?.display_name ?? '');
  const [path, setPath] = React.useState<PreferredPath | null>(initialPath);

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

  const [facultiesLoading, setFacultiesLoading] = React.useState(false);
  const [departmentsLoading, setDepartmentsLoading] = React.useState(false);
  const [coursesLoading, setCoursesLoading] = React.useState(false);

  // Waitlist: an uncovered university is a signal for ops, not a dead end.
  const [waitlistName, setWaitlistName] = React.useState('');
  const [waitlistNote, setWaitlistNote] = React.useState('');
  const [waitlistNoteText, setWaitlistNoteText] = React.useState<string | null>(null);

  const loadInitial = React.useCallback(async (): Promise<void> => {
    setInitialLoading(true);
    setLoadError(null);
    try {
      const [snapshot, unis, current] = await Promise.all([
        http.get<OnboardingState>('/onboarding/state'),
        http.get<University[]>('/onboarding/universities'),
        http.get<Semester | null>('/onboarding/sessions/current'),
      ]);
      setState(snapshot);
      setUniversities(unis);
      setSemester(current);

      const storedPath = isPreferredPath(profile?.preferred_path) ? profile.preferred_path : null;
      const wantsStudies =
        storedPath !== null &&
        pathNeedsStudies(storedPath) &&
        (searchParams.get('step') === 'studies' || snapshot.next_step === 'enrol' || !snapshot.has_enrolment);
      setStep(wantsStudies ? 'studies' : 'profile');
    } catch (err) {
      setLoadError(err instanceof ApiError ? err.message : 'Could not load your setup. Try again.');
    } finally {
      setInitialLoading(false);
    }
    // The session is already loaded when this route renders, so the first
    // profile and search string are the ones that decide the starting step.
  }, []);

  React.useEffect(() => {
    void loadInitial();
  }, [loadInitial]);

  async function saveProfile(): Promise<void> {
    if (displayName.trim().length === 0) {
      setError('Enter the name you want us to use.');
      return;
    }
    if (!path) {
      setError('Choose one of the four spaces to continue.');
      return;
    }
    setError(null);
    setBusy(true);
    try {
      await http.patch<Profile>('/me', { display_name: displayName.trim() });
      await http.post<Profile>('/me/path', { path });
      await reload();

      if (!pathNeedsStudies(path)) {
        await completeAndOpen(pathDestination(path));
        return;
      }
      setStep('studies');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not save your profile.');
    } finally {
      setBusy(false);
    }
  }

  async function completeAndOpen(destination: string): Promise<void> {
    await http.post('/me/onboarding/complete');
    await reload();
    navigate(destination, { replace: true });
  }

  async function loadFaculties(id: string): Promise<void> {
    setUniversityId(id);
    setFacultyId('');
    setDepartmentId('');
    setFaculties([]);
    setDepartments([]);
    setCourses([]);
    setPickedCourses([]);
    if (!id) return;
    setFacultiesLoading(true);
    setError(null);
    try {
      setFaculties(await http.get<Subdivision[]>(`/onboarding/universities/${id}/faculties`));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not load faculties.');
    } finally {
      setFacultiesLoading(false);
    }
  }

  async function loadDepartments(id: string): Promise<void> {
    setFacultyId(id);
    setDepartmentId('');
    setDepartments([]);
    setCourses([]);
    setPickedCourses([]);
    if (!id) return;
    setDepartmentsLoading(true);
    setError(null);
    try {
      setDepartments(await http.get<Subdivision[]>(`/onboarding/faculties/${id}/departments`));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not load departments.');
    } finally {
      setDepartmentsLoading(false);
    }
  }

  async function loadCourses(id: string, selectedLevel = level): Promise<void> {
    setDepartmentId(id);
    setPickedCourses([]);
    setCourses([]);
    if (!id) return;
    setCoursesLoading(true);
    setError(null);
    const query = selectedLevel ? `?level=${encodeURIComponent(selectedLevel)}` : '';
    try {
      setCourses(await http.get<Course[]>(`/onboarding/departments/${id}/courses${query}`));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not load courses.');
    } finally {
      setCoursesLoading(false);
    }
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

  async function finishCampus(): Promise<void> {
    if (!universityId) {
      setError('Choose your university to continue.');
      return;
    }
    setError(null);
    setBusy(true);
    try {
      await http.put<{ message: string }>('/onboarding/university', {
        university_id: Number(universityId),
      });
      await completeAndOpen('/campus');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not save your campus.');
    } finally {
      setBusy(false);
    }
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
      await completeAndOpen(pathDestination(path));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not save your courses.');
    } finally {
      setBusy(false);
    }
  }

  const selectedOption = pathOption(path);
  const SelectedIcon = selectedOption ? PATH_ICONS[selectedOption.value] : null;
  const studiesTitle =
    path === 'campus' ? 'Your campus' : path === 'academia' ? 'Your studies' : 'Your dashboard';

  if (initialLoading) {
    return (
      <div className="nv-onboarding-page nv-stack" aria-busy="true" aria-label="Loading setup">
        <PageHeader eyebrow="Setup" title="Set up your workspace" />
        <div className="nv-onboarding">
          <div className="nv-onboarding-page nv-stack">
            <Panel title="You and your path">
              <Skeleton lines={3} height="2.5rem" />
              <Skeleton lines={4} />
            </Panel>
            <Panel title="Loading your choices">
              <Skeleton lines={4} />
            </Panel>
          </div>
          <aside className="nv-onboarding__rail">
            <Panel title="Your choice">
              <Skeleton lines={3} />
            </Panel>
          </aside>
        </div>
      </div>
    );
  }

  if (loadError && !state) {
    return (
      <div className="nv-onboarding-page nv-stack">
        <PageHeader eyebrow="Setup" title="Set up your workspace" />
        <ErrorState
          body={loadError}
          action={
            <Button size="sm" type="button" variant="secondary" onClick={() => void loadInitial()}>
              Try again
            </Button>
          }
        />
      </div>
    );
  }

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Setup"
        title="Set up your workspace"
        description="Pick the space you want first. You can switch from Home at any time without losing work."
      />

      <ol className="nv-onboarding-progress" aria-label="Onboarding progress">
        <li data-state={progressState(step, 'profile', path)}>
          <span className="nv-onboarding-progress__index">01</span>
          <span>
            <strong>You and your path</strong>
            <span>Your name and the space you want first.</span>
          </span>
        </li>
        <li data-state={progressState(step, 'studies', path)}>
          <span className="nv-onboarding-progress__index">02</span>
          <span>
            <strong>{studiesTitle}</strong>
            <span>
              {pathNeedsStudies(path)
                ? 'Only the context this space reads.'
                : 'Opens after your choice is saved.'}
            </span>
          </span>
        </li>
      </ol>

      {error ? (
        <Banner tone="danger">
          <p>{error}</p>
        </Banner>
      ) : null}

      <div className="nv-onboarding">
        <div className="nv-stack">
          {step === 'profile' ? (
            <Panel title="You and your path" actions={<span className="nv-meta">Step 1 of 2</span>}>
              <form
                className="nv-stack"
                onSubmit={(event) => {
                  event.preventDefault();
                  void saveProfile();
                }}
              >
                <Field
                  hint="This appears on a shared profile."
                  label="What should we call you?"
                  maxLength={150}
                  required
                  value={displayName}
                  onChange={(event) => setDisplayName(event.target.value)}
                />

                <fieldset className="nv-path-picker">
                  <legend className="nv-label">Which space do you want first?</legend>
                  <p className="nv-field__hint">
                    Each space has its own dashboard. Switching later keeps courses, proof and earnings.
                  </p>
                  <div className="nv-path-picker__grid">
                    {PATH_OPTIONS.map((option) => {
                      const Icon = PATH_ICONS[option.value];
                      const selected = path === option.value;
                      return (
                        <label className="nv-path-choice" data-selected={selected} key={option.value}>
                          <input
                            checked={selected}
                            className="nv-sr-only"
                            name="path"
                            type="radio"
                            value={option.value}
                            onChange={() => setPath(option.value)}
                          />
                          <span className="nv-path-choice__icon" aria-hidden="true">
                            <Icon size={18} strokeWidth={1.7} />
                          </span>
                          <span className="nv-path-choice__copy">
                            <strong>{option.label}</strong>
                            <span>{option.summary}</span>
                            <span className="nv-path-choice__detail">{option.detail}</span>
                          </span>
                          <span className="nv-path-choice__mark" aria-hidden="true">
                            {selected ? <Check size={14} strokeWidth={2.2} /> : null}
                          </span>
                        </label>
                      );
                    })}
                  </div>
                </fieldset>

                <div className="nv-onboarding__actions">
                  <span className="nv-meta">
                    {!path
                      ? 'Choose a space to see what it needs.'
                      : pathNeedsStudies(path)
                        ? 'Next: the details this space reads.'
                        : 'No university form needed for this space.'}
                  </span>
                  <Button disabled={busy || !path || displayName.trim().length === 0} type="submit">
                    {busy ? 'Saving' : 'Continue'}
                    <ArrowRight aria-hidden="true" size={15} />
                  </Button>
                </div>
              </form>
            </Panel>
          ) : (
            <Panel title={studiesTitle} actions={<span className="nv-meta">Step 2 of 2</span>}>
              <form
                className="nv-stack"
                onSubmit={(event) => {
                  event.preventDefault();
                  if (path === 'campus') void finishCampus();
                  else void enrol();
                }}
              >
                {path === 'campus' ? (
                  <>
                    <p className="nv-muted">
                      Campus reads the live information and map points for one university. Courses are not
                      required for this space.
                    </p>
                    <Select
                      hint="This decides what the Campus dashboard shows."
                      label="University"
                      options={[
                        { value: '', label: 'Select your university' },
                        ...universities.map((u) => ({ value: String(u.id), label: u.name })),
                      ]}
                      value={universityId}
                      onChange={(event) => void loadFaculties(event.target.value)}
                    />
                    {universities.length === 0 ? (
                      <Banner tone="warning">
                        <p>
                          No university is listed yet. Use the waitlist below and your account will still
                          work.
                        </p>
                      </Banner>
                    ) : null}
                  </>
                ) : (
                  <>
                    {semester ? (
                      <p className="nv-muted">
                        {semester.name} ({semester.ordinal}) is the current semester.
                      </p>
                    ) : (
                      <Banner tone="warning">
                        <p>
                          No semester is open right now, so enrolment is paused. Your account still works.
                        </p>
                      </Banner>
                    )}

                    <div className="nv-onboarding__selects">
                      <Select
                        label="University"
                        options={[
                          { value: '', label: 'Select your university' },
                          ...universities.map((u) => ({ value: String(u.id), label: u.name })),
                        ]}
                        value={universityId}
                        onChange={(event) => void loadFaculties(event.target.value)}
                      />
                      <Select
                        disabled={!universityId || facultiesLoading}
                        hint={facultiesLoading ? 'Loading faculties.' : undefined}
                        label="Faculty"
                        options={[
                          {
                            value: '',
                            label: facultiesLoading
                              ? 'Loading faculties'
                              : faculties.length
                                ? 'Select your faculty'
                                : 'Pick a university first',
                          },
                          ...faculties.map((f) => ({ value: String(f.id), label: f.name })),
                        ]}
                        value={facultyId}
                        onChange={(event) => void loadDepartments(event.target.value)}
                      />
                      <Select
                        disabled={!facultyId || departmentsLoading}
                        hint={departmentsLoading ? 'Loading departments.' : undefined}
                        label="Department"
                        options={[
                          {
                            value: '',
                            label: departmentsLoading
                              ? 'Loading departments'
                              : departments.length
                                ? 'Select your department'
                                : 'Pick a faculty first',
                          },
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
                    </div>

                    <fieldset className="nv-field">
                      <legend className="nv-label">
                        Courses this semester
                        <span className="nv-muted"> ({pickedCourses.length} selected)</span>
                      </legend>

                      {!departmentId ? (
                        <p className="nv-muted">
                          Choose a university, faculty and department to see the courses for that department.
                        </p>
                      ) : coursesLoading ? (
                        <div aria-busy="true" aria-label="Loading courses">
                          <Skeleton lines={4} />
                        </div>
                      ) : courses.length === 0 ? (
                        <p className="nv-muted">
                          No courses are listed for this department and level. Try another level, or use the
                          waitlist below if the catalogue is incomplete.
                        </p>
                      ) : (
                        <div className="nv-table-wrap">
                          <table className="nv-table nv-table--compact nv-onboarding__courses">
                            <caption className="nv-sr-only">
                              Courses for the selected department and level
                            </caption>
                            <thead>
                              <tr>
                                <th scope="col">Pick</th>
                                <th scope="col">Code</th>
                                <th scope="col">Course</th>
                                <th scope="col">Level</th>
                              </tr>
                            </thead>
                            <tbody>
                              {courses.map((course) => {
                                const selected = pickedCourses.includes(course.id);
                                return (
                                  <tr data-selected={selected} key={course.id}>
                                    <td>
                                      <Checkbox
                                        checked={selected}
                                        id={`course-${course.id}`}
                                        label={
                                          <span className="nv-sr-only">
                                            Select {course.code}: {course.title}
                                          </span>
                                        }
                                        onChange={() => toggleCourse(course.id)}
                                      />
                                    </td>
                                    <td className="nv-mono">
                                      <label htmlFor={`course-${course.id}`}>{course.code}</label>
                                    </td>
                                    <td>
                                      <label htmlFor={`course-${course.id}`}>{course.title}</label>
                                    </td>
                                    <td>{course.level}</td>
                                  </tr>
                                );
                              })}
                            </tbody>
                          </table>
                        </div>
                      )}
                    </fieldset>
                  </>
                )}

                <details className="nv-card nv-card--flat">
                  <summary>My university is not listed</summary>
                  <div className="nv-stack nv-onboarding__waitlist">
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
                      <Button
                        disabled={busy}
                        type="button"
                        variant="ghost"
                        onClick={() => void joinWaitlist()}
                      >
                        {busy ? 'Sending' : 'Join the waitlist'}
                      </Button>
                    </div>
                    {waitlistNoteText ? (
                      <Banner tone="success">
                        <p>{waitlistNoteText}</p>
                      </Banner>
                    ) : null}
                  </div>
                </details>

                <div className="nv-onboarding__actions">
                  <Button
                    disabled={busy}
                    type="button"
                    variant="ghost"
                    onClick={() => {
                      setError(null);
                      setStep('profile');
                    }}
                  >
                    <ArrowLeft aria-hidden="true" size={15} />
                    Back
                  </Button>
                  <Button
                    disabled={
                      busy || (path === 'campus' ? !universityId : !semester || pickedCourses.length === 0)
                    }
                    type="submit"
                  >
                    {busy ? 'Saving' : path === 'campus' ? 'Finish setup' : 'Save courses'}
                    <ArrowRight aria-hidden="true" size={15} />
                  </Button>
                </div>
              </form>
            </Panel>
          )}
        </div>

        <aside className="nv-onboarding__rail" aria-label="Setup summary">
          <Panel title="Your choice">
            {selectedOption && SelectedIcon ? (
              <div className="nv-onboarding__choice">
                <span className="nv-path-choice__icon" aria-hidden="true">
                  <SelectedIcon size={18} strokeWidth={1.7} />
                </span>
                <div>
                  <p className="nv-h4">{selectedOption.label}</p>
                  <p className="nv-muted">{selectedOption.summary}</p>
                </div>
              </div>
            ) : (
              <p className="nv-muted">Pick one of the four spaces to see what it opens.</p>
            )}
            <p className="nv-meta">Switch from Home whenever you want.</p>
          </Panel>

          <Panel title="What happens next">
            {selectedOption ? (
              <ul className="nv-list">
                {NEXT_STEPS[selectedOption.value].map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            ) : (
              <p className="nv-muted">
                Academia adds courses. Skills and Opportunities open directly. Campus asks for your university
                only.
              </p>
            )}
          </Panel>

          <Panel title="Your account">
            <p className="nv-meta">{me?.email ?? 'Signed in'}</p>
            <p className="nv-muted">
              {me?.email_verified
                ? 'Email confirmed.'
                : 'Confirm your email from Home when you can. It does not block setup.'}
            </p>
          </Panel>
        </aside>
      </div>
    </div>
  );
}
