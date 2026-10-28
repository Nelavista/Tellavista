/**
 * Content (C7).
 *
 * Content is configuration: a new lesson or task type is rows, not a deploy.
 * Drafts are invisible to students because every student query filters on
 * `published`; publishing a template increments its version so work already
 * graded keeps pointing at the definition it was graded against.
 */
import type {
  ContentLessonListOut,
  ContentPathListOut,
  ContentTemplateListOut,
  SkillOut,
  SkillsOut,
  ValidatorListOut,
} from '@nelavista/api-client';
import { Badge, Banner, EmptyState, ErrorNote, ErrorState, PageHeader, Panel, Skeleton } from '@nelavista/ui';
import * as React from 'react';

import { ApiError, http } from '../lib/http';
import { useResource } from '../lib/resource';

type Created = { id: number; slug: string; status: string };

const INPUT_EXAMPLE = JSON.stringify({ options: [{ key: 'positive', label: 'Positive' }] }, null, 2);
const ANSWER_EXAMPLE = JSON.stringify({ type: 'object', properties: { key: { type: 'string' } } }, null, 2);

export function Content(): JSX.Element {
  const skills = useResource<SkillsOut>('/skills');
  const [skillId, setSkillId] = React.useState('');
  const lessons = useResource<ContentLessonListOut>(
    skillId ? `/skills/content/lessons?skill_id=${skillId}` : '/skills/content/lessons',
  );
  const paths = useResource<ContentPathListOut>(
    skillId ? `/skills/content/paths?skill_id=${skillId}` : '/skills/content/paths',
  );
  const templates = useResource<ContentTemplateListOut>(
    skillId ? `/skills/content/tasks?skill_id=${skillId}` : '/skills/content/tasks',
  );
  const validators = useResource<ValidatorListOut>('/skills/content/validators');

  const [lessonSlug, setLessonSlug] = React.useState('');
  const [lessonTitle, setLessonTitle] = React.useState('');
  const [lessonBody, setLessonBody] = React.useState('');
  const [pathSlug, setPathSlug] = React.useState('');
  const [pathTitle, setPathTitle] = React.useState('');
  const [pathLevel, setPathLevel] = React.useState('beginner');
  const [stepPath, setStepPath] = React.useState('');
  const [stepOrdinal, setStepOrdinal] = React.useState('1');
  const [stepKind, setStepKind] = React.useState('lesson');
  const [stepLesson, setStepLesson] = React.useState('');
  const [templateSlug, setTemplateSlug] = React.useState('');
  const [templateName, setTemplateName] = React.useState('');
  const [instructions, setInstructions] = React.useState('');
  const [inputSchema, setInputSchema] = React.useState(INPUT_EXAMPLE);
  const [answerSchema, setAnswerSchema] = React.useState(ANSWER_EXAMPLE);
  const [validator, setValidator] = React.useState('exact_key');
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [note, setNote] = React.useState<string | null>(null);

  async function createLesson(): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      await http.post<Created>('/skills/content/lessons', {
        skill_id: Number(skillId),
        slug: lessonSlug.trim(),
        title: lessonTitle.trim(),
        body_md: lessonBody,
        status: 'draft',
      });
      setNote('Lesson created as a draft.');
      setLessonSlug('');
      setLessonTitle('');
      setLessonBody('');
      lessons.reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not create the lesson.');
    } finally {
      setBusy(false);
    }
  }

  async function publishLesson(lessonId: number, status: string): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      await http.patch(`/skills/content/lessons/${lessonId}`, { status });
      setNote(`Lesson ${lessonId} is now ${status}.`);
      lessons.reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not change the lesson status.');
    } finally {
      setBusy(false);
    }
  }

  async function createPath(): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      await http.post('/skills/content/paths', {
        skill_id: Number(skillId),
        slug: pathSlug.trim(),
        title: pathTitle.trim(),
        level: pathLevel,
        status: 'draft',
      });
      setNote('Path created as a draft.');
      setPathSlug('');
      setPathTitle('');
      paths.reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not create the path.');
    } finally {
      setBusy(false);
    }
  }

  async function publishPath(pathId: number, status: string): Promise<void> {
    setBusy(true);
    try {
      await http.patch(`/skills/content/paths/${pathId}`, { status });
      setNote(`Path ${pathId} is now ${status}.`);
      paths.reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not change the path status.');
    } finally {
      setBusy(false);
    }
  }

  async function addStep(): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      await http.post(`/skills/content/paths/${Number(stepPath)}/steps`, {
        path_id: Number(stepPath),
        ordinal: Number(stepOrdinal),
        kind: stepKind,
        lesson_id: stepLesson ? Number(stepLesson) : null,
      });
      setNote('Step added.');
      setStepOrdinal(String(Number(stepOrdinal) + 1));
      paths.reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not add that step.');
    } finally {
      setBusy(false);
    }
  }

  async function createTemplate(): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      await http.post('/skills/content/tasks', {
        skill_id: Number(skillId),
        slug: templateSlug.trim(),
        name: templateName.trim(),
        instructions_md: instructions,
        input_schema: JSON.parse(inputSchema || '{}') as Record<string, unknown>,
        answer_schema: JSON.parse(answerSchema || '{}') as Record<string, unknown>,
        validator,
        status: 'draft',
      });
      setNote('Task template created as a draft.');
      setTemplateSlug('');
      setTemplateName('');
      templates.reload();
    } catch (err) {
      if (err instanceof SyntaxError) setError('Input and answer schemas must be valid JSON.');
      else setError(err instanceof ApiError ? err.message : 'Could not create the template.');
    } finally {
      setBusy(false);
    }
  }

  async function publishTemplate(templateId: number, status: string): Promise<void> {
    setBusy(true);
    try {
      await http.patch(`/skills/content/tasks/${templateId}`, { status });
      setNote(`Template ${templateId} is now ${status}; publishing bumps its version.`);
      templates.reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not publish the template.');
    } finally {
      setBusy(false);
    }
  }

  const skillRows: SkillOut[] = skills.resource.status === 'ready' ? skills.resource.data.skills : [];

  return (
    <div className="nv-stack nv-stack--loose">
      <PageHeader
        eyebrow="Content"
        title="Content"
        description="Drafts are invisible to students. Publish a lesson or path when it is ready; publishing a task template creates a new version."
      />

      <ErrorNote message={error} />
      {note ? <Banner tone="success">{note}</Banner> : null}

      <Panel title="Scope">
        <div className="nv-row">
          <div style={{ minWidth: 260 }}>
            <label className="nv-label" htmlFor="content-skill">
              Skill
            </label>
            <select
              className="nv-select"
              id="content-skill"
              value={skillId}
              onChange={(event) => setSkillId(event.target.value)}
            >
              <option value="">All skills</option>
              {skillRows.map((row) => (
                <option key={row.id} value={row.id}>
                  {row.name} (#{row.id})
                </option>
              ))}
            </select>
          </div>
          {validators.resource.status === 'ready' ? (
            <p className="nv-muted">Validators: {validators.resource.data.validators.join(' · ')}</p>
          ) : null}
        </div>
        {!skillId ? <p className="nv-muted">Choose a skill before creating content.</p> : null}
      </Panel>

      <Panel title="Lessons">
        <div className="nv-grid">
          <div>
            <label className="nv-label" htmlFor="lesson-slug">
              Slug
            </label>
            <input
              className="nv-input"
              id="lesson-slug"
              value={lessonSlug}
              onChange={(e) => setLessonSlug(e.target.value)}
            />
          </div>
          <div>
            <label className="nv-label" htmlFor="lesson-title">
              Title
            </label>
            <input
              className="nv-input"
              id="lesson-title"
              value={lessonTitle}
              onChange={(e) => setLessonTitle(e.target.value)}
            />
          </div>
        </div>
        <div>
          <label className="nv-label" htmlFor="lesson-body">
            Body (markdown)
          </label>
          <textarea
            className="nv-textarea"
            id="lesson-body"
            value={lessonBody}
            onChange={(e) => setLessonBody(e.target.value)}
          />
        </div>
        <button
          className="nv-button"
          disabled={busy || !skillId || lessonSlug.trim().length < 2}
          type="button"
          onClick={() => void createLesson()}
        >
          Create lesson
        </button>

        {lessons.resource.status === 'loading' ? <Skeleton lines={4} /> : null}
        {lessons.resource.status === 'error' ? (
          <ErrorState title="Lessons did not load" body={lessons.resource.message} />
        ) : null}
        {lessons.resource.status === 'ready' && lessons.resource.data.lessons.length === 0 ? (
          <EmptyState
            title="No lesson yet"
            body="Create a draft above. It stays invisible until you publish it."
          />
        ) : null}
        {lessons.resource.status === 'ready' && lessons.resource.data.lessons.length > 0 ? (
          <div className="nv-table-wrap">
            <table className="nv-table">
              <thead>
                <tr>
                  <th scope="col">Lesson</th>
                  <th scope="col">Status</th>
                  <th scope="col">
                    <span className="nv-sr-only">Actions</span>
                  </th>
                </tr>
              </thead>
              <tbody>
                {lessons.resource.data.lessons.map((row) => (
                  <tr key={row.id}>
                    <td>
                      {row.title}
                      <div className="nv-muted">
                        {row.slug} · #{row.id}
                      </div>
                    </td>
                    <td>
                      <Badge tone={row.status === 'published' ? 'success' : 'warning'}>{row.status}</Badge>
                    </td>
                    <td>
                      <div className="nv-row">
                        {row.status !== 'published' ? (
                          <button
                            className="nv-button"
                            type="button"
                            disabled={busy}
                            onClick={() => void publishLesson(row.id, 'published')}
                          >
                            Publish
                          </button>
                        ) : (
                          <button
                            className="nv-button nv-button--ghost"
                            type="button"
                            disabled={busy}
                            onClick={() => void publishLesson(row.id, 'draft')}
                          >
                            Unpublish
                          </button>
                        )}
                        <button
                          className="nv-button nv-button--ghost"
                          type="button"
                          disabled={busy}
                          onClick={() => void publishLesson(row.id, 'archived')}
                        >
                          Archive
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : null}
      </Panel>

      <Panel title="Paths and steps">
        <div className="nv-grid">
          <div>
            <label className="nv-label" htmlFor="path-slug">
              Path slug
            </label>
            <input
              className="nv-input"
              id="path-slug"
              value={pathSlug}
              onChange={(e) => setPathSlug(e.target.value)}
            />
          </div>
          <div>
            <label className="nv-label" htmlFor="path-title">
              Path title
            </label>
            <input
              className="nv-input"
              id="path-title"
              value={pathTitle}
              onChange={(e) => setPathTitle(e.target.value)}
            />
          </div>
          <div>
            <label className="nv-label" htmlFor="path-level">
              Level
            </label>
            <select
              className="nv-select"
              id="path-level"
              value={pathLevel}
              onChange={(e) => setPathLevel(e.target.value)}
            >
              {['beginner', 'intermediate', 'advanced'].map((level) => (
                <option key={level} value={level}>
                  {level}
                </option>
              ))}
            </select>
          </div>
        </div>
        <button
          className="nv-button"
          disabled={busy || !skillId || pathSlug.trim().length < 2}
          type="button"
          onClick={() => void createPath()}
        >
          Create path
        </button>

        {paths.resource.status === 'loading' ? <Skeleton lines={4} /> : null}
        {paths.resource.status === 'error' ? (
          <ErrorState title="Paths did not load" body={paths.resource.message} />
        ) : null}
        {paths.resource.status === 'ready' && paths.resource.data.paths.length === 0 ? (
          <EmptyState title="No path yet" body="Create a draft path above, then add its first step." />
        ) : null}
        {paths.resource.status === 'ready' && paths.resource.data.paths.length > 0 ? (
          <div className="nv-table-wrap">
            <table className="nv-table">
              <thead>
                <tr>
                  <th scope="col">Path</th>
                  <th scope="col">Status</th>
                  <th scope="col">Steps</th>
                  <th scope="col">
                    <span className="nv-sr-only">Actions</span>
                  </th>
                </tr>
              </thead>
              <tbody>
                {paths.resource.data.paths.map((row) => (
                  <tr key={row.id}>
                    <td>
                      {row.title}
                      <div className="nv-muted">
                        {row.slug} · #{row.id}
                      </div>
                    </td>
                    <td>
                      <Badge tone={row.status === 'published' ? 'success' : 'warning'}>{row.status}</Badge>
                    </td>
                    <td>{row.steps.length}</td>
                    <td>
                      <div className="nv-row">
                        {row.status !== 'published' ? (
                          <button
                            className="nv-button"
                            type="button"
                            disabled={busy}
                            onClick={() => void publishPath(row.id, 'published')}
                          >
                            Publish
                          </button>
                        ) : (
                          <button
                            className="nv-button nv-button--ghost"
                            type="button"
                            disabled={busy}
                            onClick={() => void publishPath(row.id, 'draft')}
                          >
                            Unpublish
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : null}

        <h3 className="nv-h2">Add a step</h3>
        <div className="nv-grid">
          <div>
            <label className="nv-label" htmlFor="step-path">
              Path id
            </label>
            <input
              className="nv-input"
              id="step-path"
              value={stepPath}
              onChange={(e) => setStepPath(e.target.value)}
            />
          </div>
          <div>
            <label className="nv-label" htmlFor="step-ordinal">
              Ordinal
            </label>
            <input
              className="nv-input"
              id="step-ordinal"
              type="number"
              value={stepOrdinal}
              onChange={(e) => setStepOrdinal(e.target.value)}
            />
          </div>
          <div>
            <label className="nv-label" htmlFor="step-kind">
              Kind
            </label>
            <select
              className="nv-select"
              id="step-kind"
              value={stepKind}
              onChange={(e) => setStepKind(e.target.value)}
            >
              {['lesson', 'practice', 'project', 'assessment'].map((kind) => (
                <option key={kind} value={kind}>
                  {kind}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="nv-label" htmlFor="step-lesson">
              Lesson id (lesson steps)
            </label>
            <input
              className="nv-input"
              id="step-lesson"
              value={stepLesson}
              onChange={(e) => setStepLesson(e.target.value)}
            />
          </div>
        </div>
        <button
          className="nv-button"
          disabled={busy || !stepPath || !stepOrdinal}
          type="button"
          onClick={() => void addStep()}
        >
          Add step
        </button>
      </Panel>

      <Panel title="Task templates">
        <div className="nv-grid">
          <div>
            <label className="nv-label" htmlFor="template-slug">
              Slug
            </label>
            <input
              className="nv-input"
              id="template-slug"
              value={templateSlug}
              onChange={(e) => setTemplateSlug(e.target.value)}
            />
          </div>
          <div>
            <label className="nv-label" htmlFor="template-name">
              Name
            </label>
            <input
              className="nv-input"
              id="template-name"
              value={templateName}
              onChange={(e) => setTemplateName(e.target.value)}
            />
          </div>
          <div>
            <label className="nv-label" htmlFor="template-validator">
              Validator
            </label>
            <select
              className="nv-select"
              id="template-validator"
              value={validator}
              onChange={(e) => setValidator(e.target.value)}
            >
              {(validators.resource.status === 'ready'
                ? validators.resource.data.validators
                : ['exact_key']
              ).map((name) => (
                <option key={name} value={name}>
                  {name}
                </option>
              ))}
            </select>
          </div>
        </div>
        <div>
          <label className="nv-label" htmlFor="template-instructions">
            Instructions (markdown)
          </label>
          <textarea
            className="nv-textarea"
            id="template-instructions"
            value={instructions}
            onChange={(e) => setInstructions(e.target.value)}
          />
        </div>
        <div className="nv-grid">
          <div>
            <label className="nv-label" htmlFor="template-input">
              Input schema (JSON)
            </label>
            <textarea
              className="nv-textarea"
              id="template-input"
              value={inputSchema}
              onChange={(e) => setInputSchema(e.target.value)}
            />
          </div>
          <div>
            <label className="nv-label" htmlFor="template-answer">
              Answer schema (JSON)
            </label>
            <textarea
              className="nv-textarea"
              id="template-answer"
              value={answerSchema}
              onChange={(e) => setAnswerSchema(e.target.value)}
            />
          </div>
        </div>
        <button
          className="nv-button"
          disabled={busy || !skillId || templateSlug.trim().length < 2}
          type="button"
          onClick={() => void createTemplate()}
        >
          Create template
        </button>

        {templates.resource.status === 'loading' ? <Skeleton lines={4} /> : null}
        {templates.resource.status === 'error' ? (
          <ErrorState title="Templates did not load" body={templates.resource.message} />
        ) : null}
        {templates.resource.status === 'ready' && templates.resource.data.templates.length === 0 ? (
          <EmptyState
            title="No template yet"
            body="Create a draft task type above. Publishing it creates version 1."
          />
        ) : null}
        {templates.resource.status === 'ready' && templates.resource.data.templates.length > 0 ? (
          <div className="nv-table-wrap">
            <table className="nv-table">
              <thead>
                <tr>
                  <th scope="col">Template</th>
                  <th scope="col">Validator</th>
                  <th scope="col">Version</th>
                  <th scope="col">Status</th>
                  <th scope="col">
                    <span className="nv-sr-only">Actions</span>
                  </th>
                </tr>
              </thead>
              <tbody>
                {templates.resource.data.templates.map((row) => (
                  <tr key={row.id}>
                    <td>
                      {row.name}
                      <div className="nv-muted">
                        {row.slug} · #{row.id}
                      </div>
                    </td>
                    <td>{row.validator}</td>
                    <td>v{row.version}</td>
                    <td>
                      <Badge tone={row.status === 'published' ? 'success' : 'warning'}>{row.status}</Badge>
                    </td>
                    <td>
                      <div className="nv-row">
                        {row.status !== 'published' ? (
                          <button
                            className="nv-button"
                            type="button"
                            disabled={busy}
                            onClick={() => void publishTemplate(row.id, 'published')}
                          >
                            Publish
                          </button>
                        ) : (
                          <button
                            className="nv-button nv-button--ghost"
                            type="button"
                            disabled={busy}
                            onClick={() => void publishTemplate(row.id, 'draft')}
                          >
                            Unpublish
                          </button>
                        )}
                        <button
                          className="nv-button nv-button--ghost"
                          type="button"
                          disabled={busy}
                          onClick={() => void publishTemplate(row.id, 'archived')}
                        >
                          Archive
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : null}
      </Panel>
    </div>
  );
}
