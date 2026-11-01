/** One topic inside an enrolled course. */
import type { TopicDetailOut } from '@nelavista/api-client';
import { Badge, Button, EmptyState, ErrorState, PageHeader, Panel, Skeleton } from '@nelavista/ui';
import { Link, useParams } from 'react-router-dom';

import { EMPTY_IMAGES } from '../lib/empty-images';
import { useApiResource } from '../lib/resource';

export function Topic(): JSX.Element {
  const { topicId = '' } = useParams();
  const { resource, reload } = useApiResource<TopicDetailOut>(`/academia/topics/${topicId}`);

  if (resource.status === 'loading') {
    return (
      <div className="nv-stack" aria-busy="true" aria-label="Loading the topic">
        <Skeleton height="2.5rem" width="45%" />
        <Skeleton lines={4} />
        <Skeleton lines={3} />
      </div>
    );
  }

  if (resource.status === 'off') {
    return (
      <EmptyState
        title="Topic detail is not switched on here"
        body="This environment has the feature off. It is not a missing topic."
      />
    );
  }

  if (resource.status === 'missing') {
    return (
      <EmptyState
        title="This topic is not available"
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
        title="The topic did not load"
        body={resource.message}
        action={
          <Button onClick={reload} type="button" variant="secondary">
            Try again
          </Button>
        }
      />
    );
  }

  const topic = resource.data;
  const accuracy = topic.accuracy === null ? 'Not attempted' : `${topic.accuracy}%`;

  return (
    <div className="nv-stack nv-stack--loose">
      <PageHeader
        eyebrow={`${topic.course.code} · Topic ${topic.ordinal}`}
        title={topic.title}
        description={topic.summary ?? `A topic in ${topic.course.title}.`}
        actions={
          <div className="nv-row">
            <Link className="nv-button" to={`/academia/cbt?course=${topic.course.code}`}>
              Practise this course
            </Link>
            <Link className="nv-button nv-button--secondary" to={`/academia/courses/${topic.course.code}`}>
              Open the course
            </Link>
          </div>
        }
      />

      <div className="nv-grid">
        <div className="nv-stat">
          <p className="nv-stat__value">{topic.question_count}</p>
          <p className="nv-stat__label">Questions</p>
        </div>
        <div className="nv-stat">
          <p className="nv-stat__value">{topic.attempts}</p>
          <p className="nv-stat__label">Answers</p>
        </div>
        <div className="nv-stat">
          <p className="nv-stat__value">{topic.correct}</p>
          <p className="nv-stat__label">Correct</p>
        </div>
        <div className="nv-stat">
          <p className="nv-stat__value">{accuracy}</p>
          <p className="nv-stat__label">Accuracy</p>
        </div>
      </div>

      <Panel
        title="Practice state"
        actions={
          topic.attempts === 0 ? (
            <Badge tone="neutral">Not attempted</Badge>
          ) : topic.strength ? (
            <Badge tone="success">Strong</Badge>
          ) : topic.weakness ? (
            <Badge tone="warning">Needs practice</Badge>
          ) : (
            <Badge tone="info">In progress</Badge>
          )
        }
      >
        <p className="nv-muted">
          {topic.attempts === 0
            ? 'No answer has been recorded for this topic yet. Accuracy is filled by practice, not by reading.'
            : `${topic.correct} of ${topic.attempts} answers were correct. Use CBT history to review the questions, your answers and the explanations.`}
        </p>
        <div className="nv-row" style={{ marginTop: 'var(--nv-space-md)' }}>
          <Link className="nv-button nv-button--secondary nv-button--sm" to="/academia/cbt/history">
            Review CBT history
          </Link>
        </div>
      </Panel>

      <Panel
        title="Materials for the course"
        actions={<Badge tone="neutral">{topic.materials.length}</Badge>}
      >
        {topic.materials.length === 0 ? (
          <EmptyState
            title="No material attached yet"
            body="Material is attached at course level, so this list stays empty until the course has a note, textbook or past question."
            image={EMPTY_IMAGES.materials}
          />
        ) : (
          <ul className="nv-list nv-list--ruled">
            {topic.materials.map((material) => (
              <li className="nv-row nv-row--between" key={material.id}>
                <div className="nv-stack nv-stack--tight">
                  <Link to={`/academia/materials/${material.id}`}>{material.title}</Link>
                  <span className="nv-meta">{material.source || 'Source not recorded'}</span>
                </div>
                <Link className="nv-link-arrow" to={`/academia/materials/${material.id}`}>
                  Open
                </Link>
              </li>
            ))}
          </ul>
        )}
      </Panel>
    </div>
  );
}
