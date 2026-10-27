import type { OnboardingStateOut } from '@nelavista/api-client';
import * as React from 'react';
import { Link, useParams } from 'react-router-dom';

import { useApiResource } from '../lib/resource';
import { Badge, Button, EmptyState, ErrorState, PageHeader, Skeleton } from '../ui';

export function Course(): JSX.Element {
  const { courseCode = '' } = useParams();
  const { resource, reload } = useApiResource<OnboardingStateOut>('/onboarding/state');

  if (resource.status === 'loading') {
    return (
      <div className="nv-card nv-stack" aria-busy="true">
        <Skeleton height="2.5rem" width="40%" />
        <Skeleton lines={3} />
      </div>
    );
  }

  if (resource.status === 'off') {
    return (
      <EmptyState
        title="Academia is not switched on here"
        body="This environment has the feature off. It is not a missing course."
      />
    );
  }

  if (resource.status === 'missing' || resource.status === 'error') {
    return (
      <ErrorState
        title="The course did not load"
        body={resource.message}
        action={
          <Button onClick={reload} type="button" variant="secondary">
            Try again
          </Button>
        }
      />
    );
  }

  const course = resource.data.enrolments.find((row) => row.code.toLowerCase() === courseCode.toLowerCase());

  if (!course) {
    return (
      <EmptyState
        title={`No enrolment for ${courseCode || 'that course'}`}
        body="The course is either not in your current enrolment or the code is wrong. Open Academia to see the courses on your record."
        action={
          <Link className="nv-button" to="/academia">
            Back to Academia
          </Link>
        }
      />
    );
  }

  return <CourseView course={course} />;
}

function CourseView({ course }: { course: OnboardingStateOut['enrolments'][number] }): JSX.Element {
  return (
    <div className="nv-stack nv-stack--loose">
      <PageHeader
        eyebrow={`${course.code} · ${course.level}`}
        title={course.title}
        description={`${course.university} · ${course.faculty} · ${course.department}`}
        actions={
          <div className="nv-row">
            <Link className="nv-button" to="/academia/cbt">
              Practise this course
            </Link>
            <Link className="nv-button nv-button--secondary" to="/academia/ask">
              Ask Nelavista
            </Link>
          </div>
        }
      />

      <div className="nv-grid--2">
        <section className="nv-panel">
          <div className="nv-panel__head">
            <h2 className="nv-h3">Enrolment</h2>
            <Badge tone={course.status === 'active' ? 'success' : 'neutral'}>{course.status}</Badge>
          </div>
          <div className="nv-panel__body">
            <dl className="nv-stack nv-stack--tight">
              <div className="nv-row nv-row--between">
                <dt className="nv-muted">Course code</dt>
                <dd className="nv-mono">{course.code}</dd>
              </div>
              <div className="nv-row nv-row--between">
                <dt className="nv-muted">Level</dt>
                <dd>{course.level}</dd>
              </div>
              <div className="nv-row nv-row--between">
                <dt className="nv-muted">Session</dt>
                <dd className="nv-mono">{course.session_id}</dd>
              </div>
              <div className="nv-row nv-row--between">
                <dt className="nv-muted">Semester</dt>
                <dd className="nv-mono">{course.semester_id ?? 'Not set'}</dd>
              </div>
            </dl>
          </div>
        </section>

        <section className="nv-panel">
          <div className="nv-panel__head">
            <h2 className="nv-h3">What you can do here</h2>
          </div>
          <div className="nv-panel__body nv-stack">
            <p className="nv-muted">
              This course page is the hub for the material, practice and questions attached to the course. It
              does not create a second copy of the record.
            </p>
            <div className="nv-row">
              <Link
                className="nv-button nv-button--secondary nv-button--sm"
                to={`/academia/materials?course=${course.course_id}`}
              >
                Open materials
              </Link>
              <Link className="nv-button nv-button--secondary nv-button--sm" to="/academia/cbt/history">
                CBT history
              </Link>
            </div>
          </div>
        </section>
      </div>

      <CourseMaterials courseId={course.course_id} courseCode={course.code} />
    </div>
  );
}

function CourseMaterials({ courseId, courseCode }: { courseId: number; courseCode: string }): JSX.Element {
  const { resource, reload } = useApiResource<{
    materials: Array<{ id: number; title: string; source?: string | null }>;
  }>(`/academia/materials?course_id=${courseId}`);

  return (
    <section className="nv-panel">
      <div className="nv-panel__head">
        <div>
          <h2 className="nv-h3">Materials</h2>
          <p className="nv-meta">{courseCode}</p>
        </div>
        <Link className="nv-button nv-button--secondary nv-button--sm" to="/academia/materials">
          All materials
        </Link>
      </div>
      {resource.status === 'loading' ? (
        <div className="nv-panel__body" aria-busy="true">
          <Skeleton lines={4} />
        </div>
      ) : resource.status === 'off' ? (
        <div className="nv-panel__body">
          <EmptyState
            title="Materials are not switched on here"
            body="This environment has the feature off."
          />
        </div>
      ) : resource.status === 'missing' || resource.status === 'error' ? (
        <div className="nv-panel__body">
          <ErrorState
            title="Materials did not load"
            body={resource.message}
            action={
              <Button onClick={reload} type="button" variant="secondary">
                Try again
              </Button>
            }
          />
        </div>
      ) : resource.data.materials.length === 0 ? (
        <div className="nv-panel__body">
          <EmptyState
            title="No material for this course yet"
            body="When a note, textbook or past question is attached to the course, it appears here."
          />
        </div>
      ) : (
        <div className="nv-table-wrap" style={{ border: 0, borderRadius: 0 }}>
          <table className="nv-table">
            <caption className="nv-sr-only">Materials for {courseCode}</caption>
            <thead>
              <tr>
                <th scope="col">Title</th>
                <th scope="col">Source</th>
                <th scope="col" />
              </tr>
            </thead>
            <tbody>
              {resource.data.materials.map((material) => (
                <tr key={material.id}>
                  <td>
                    <strong>{material.title}</strong>
                  </td>
                  <td className="nv-muted">{material.source || 'Not recorded'}</td>
                  <td>
                    <Link className="nv-link-arrow" to={`/academia/materials/${material.id}`}>
                      Open
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
