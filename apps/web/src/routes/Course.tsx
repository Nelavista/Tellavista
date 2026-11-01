/**
 * One enrolled course, with the record attached to it.
 *
 * The page is deliberately a reading surface, not a dashboard: the course's
 * topics, its materials and the student's own practice accuracy in one place.
 * A topic opens its own detail route so the course page does not become a wall
 * of duplicated material.
 */
import type { CourseDetailOut, CourseTopicOut, OnboardingStateOut } from '@nelavista/api-client';
import * as React from 'react';
import { Link, useParams } from 'react-router-dom';

import { EMPTY_IMAGES } from '../lib/empty-images';
import { useApiResource } from '../lib/resource';
import { Badge, Button, EmptyState, ErrorState, PageHeader, Panel, Skeleton } from '../ui';

export function Course(): JSX.Element {
  const { courseCode = '' } = useParams();
  const { resource, reload } = useApiResource<OnboardingStateOut>('/onboarding/state');

  if (resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading the course">
        <Skeleton height="2.5rem" width="40%" />
        <Skeleton lines={3} />
        <Skeleton lines={5} />
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
        image={EMPTY_IMAGES.course}
        action={
          <Link className="nv-button" to="/academia">
            Back to Academia
          </Link>
        }
      />
    );
  }

  return <CourseDetailView courseId={course.course_id} />;
}

function CourseDetailView({ courseId }: { courseId: number }): JSX.Element {
  const { resource, reload } = useApiResource<CourseDetailOut>(`/academia/courses/${courseId}`);

  if (resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading the course record">
        <Skeleton height="2.5rem" width="45%" />
        <Skeleton lines={3} />
        <Skeleton lines={6} />
      </div>
    );
  }

  if (resource.status === 'off') {
    return (
      <EmptyState
        title="Course detail is not switched on here"
        body="This environment has the feature off. It is not a missing course."
      />
    );
  }

  if (resource.status === 'missing') {
    return (
      <EmptyState
        title="This course is not on your record"
        body={resource.message}
        image={EMPTY_IMAGES.course}
        action={
          <Link className="nv-button" to="/academia">
            Back to Academia
          </Link>
        }
      />
    );
  }

  if (resource.status === 'error') {
    return (
      <ErrorState
        title="The course record did not load"
        body={resource.message}
        action={
          <Button onClick={reload} type="button" variant="secondary">
            Try again
          </Button>
        }
      />
    );
  }

  const course = resource.data;
  const practised = course.practice.attempts > 0;

  return (
    <div className="nv-stack nv-stack--loose">
      <PageHeader
        eyebrow={`${course.code} · ${course.level}`}
        title={course.title}
        description={`${course.university} · ${course.faculty} · ${course.department}`}
        actions={
          <div className="nv-row">
            <Link className="nv-button" to={`/academia/cbt?course=${course.code}`}>
              Practise this course
            </Link>
            <Link className="nv-button nv-button--secondary" to="/academia/ask">
              Ask Nelavista
            </Link>
          </div>
        }
      />

      <div className="nv-grid">
        <div className="nv-stat">
          <p className="nv-stat__value">{course.topics.length}</p>
          <p className="nv-stat__label">Topics</p>
        </div>
        <div className="nv-stat">
          <p className="nv-stat__value">{course.practice.attempts}</p>
          <p className="nv-stat__label">Answers</p>
        </div>
        <div className="nv-stat">
          <p className="nv-stat__value">{course.practice.correct}</p>
          <p className="nv-stat__label">Correct</p>
        </div>
        <div className="nv-stat">
          <p className="nv-stat__value">{practised ? `${course.practice.accuracy}%` : 'Not set'}</p>
          <p className="nv-stat__label">Accuracy</p>
        </div>
      </div>

      <div className="nv-split">
        <Panel title="Enrolment">
          <dl className="nv-stack nv-stack--tight">
            <div className="nv-row nv-row--between">
              <dt className="nv-muted">Status</dt>
              <dd>
                <Badge tone={course.status === 'active' ? 'success' : 'neutral'}>{course.status}</Badge>
              </dd>
            </div>
            <div className="nv-row nv-row--between">
              <dt className="nv-muted">Session</dt>
              <dd>{course.session_name ?? `Session ${course.session_id}`}</dd>
            </div>
            <div className="nv-row nv-row--between">
              <dt className="nv-muted">Semester</dt>
              <dd>{course.semester_name ?? 'Not set'}</dd>
            </div>
            <div className="nv-row nv-row--between">
              <dt className="nv-muted">Level</dt>
              <dd>{course.level}</dd>
            </div>
          </dl>
        </Panel>

        <Panel title="What you can do here">
          <div className="nv-stack">
            <p className="nv-muted">
              Read the topic list, open the material attached to this course, then practise the topic that
              needs the work.
            </p>
            <div className="nv-row">
              <Link
                className="nv-button nv-button--secondary nv-button--sm"
                to={`/academia/materials?course=${course.id}`}
              >
                Open materials
              </Link>
              <Link className="nv-button nv-button--secondary nv-button--sm" to="/academia/cbt/history">
                CBT history
              </Link>
            </div>
          </div>
        </Panel>
      </div>

      <Panel title="Topics" actions={<Badge tone="info">{course.topics.length}</Badge>}>
        {course.topics.length === 0 ? (
          <EmptyState
            title="No topics attached yet"
            body="A topic groups the material and practice questions for this course. When one is added, it appears here."
            image={EMPTY_IMAGES.course}
          />
        ) : (
          <div className="nv-table-wrap">
            <table className="nv-table">
              <caption className="nv-sr-only">Topics in {course.title}</caption>
              <thead>
                <tr>
                  <th scope="col">Topic</th>
                  <th scope="col">Questions</th>
                  <th scope="col">Answers</th>
                  <th scope="col">Accuracy</th>
                  <th scope="col">State</th>
                </tr>
              </thead>
              <tbody>
                {course.topics.map((topic) => (
                  <tr key={topic.id}>
                    <td>
                      <Link to={`/academia/topics/${topic.id}`}>
                        <strong>{topic.title}</strong>
                      </Link>
                      {topic.summary ? <p className="nv-meta">{topic.summary}</p> : null}
                    </td>
                    <td className="nv-num">{topic.question_count}</td>
                    <td className="nv-num">{topic.attempts}</td>
                    <td className="nv-num">
                      {topic.accuracy === null ? 'Not attempted' : `${topic.accuracy}%`}
                    </td>
                    <td>
                      <TopicState topic={topic} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Panel>

      <Panel title="Materials" actions={<Badge tone="neutral">{course.materials.length}</Badge>}>
        {course.materials.length === 0 ? (
          <EmptyState
            title="No material for this course yet"
            body="When a note, textbook or past question is attached to the course, it appears here."
            image={EMPTY_IMAGES.course}
          />
        ) : (
          <div className="nv-table-wrap">
            <table className="nv-table">
              <caption className="nv-sr-only">Materials for {course.title}</caption>
              <thead>
                <tr>
                  <th scope="col">Title</th>
                  <th scope="col">Source</th>
                  <th scope="col" />
                </tr>
              </thead>
              <tbody>
                {course.materials.map((material) => (
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
      </Panel>
    </div>
  );
}

function TopicState({ topic }: { topic: CourseTopicOut }): JSX.Element {
  if (topic.attempts === 0) return <Badge tone="neutral">Not attempted</Badge>;
  if (topic.strength) return <Badge tone="success">Strong</Badge>;
  if (topic.weakness) return <Badge tone="warning">Needs practice</Badge>;
  return <Badge tone="info">In progress</Badge>;
}
