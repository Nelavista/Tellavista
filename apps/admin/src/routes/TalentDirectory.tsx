/**
 * Talent directory (I6).
 *
 * The read behind this screen already existed (`GET /talent/directory`, with
 * language/level/status/background filters); this is the staff surface that uses
 * it, so a recruiter question can be answered from evidence rather than from a
 * claim. It is a search, not a marketplace: no employer self-service exists.
 *
 * Practical-work and verified-skill counts are deliberately absent — the
 * directory shape carries the profile, and inventing a "practical" filter here
 * would suggest a verification the API does not filter on.
 */
import type { TalentDirectoryOut } from '@nelavista/api-client';
import {
  Badge,
  Button,
  EmptyState,
  ErrorState,
  Field,
  PageHeader,
  Panel,
  Select,
  Skeleton,
} from '@nelavista/ui';
import { Users } from 'lucide-react';
import * as React from 'react';

import { useResource } from '../lib/resource';

export function TalentDirectory(): JSX.Element {
  const [language, setLanguage] = React.useState('');
  const [languageLevel, setLanguageLevel] = React.useState('');
  const [level, setLevel] = React.useState('');
  const [status, setStatus] = React.useState('');
  const [background, setBackground] = React.useState('');
  const [submitted, setSubmitted] = React.useState({
    language: '',
    language_level: '',
    level: '',
    status: '',
    background: '',
  });

  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(submitted)) {
    if (value) params.set(key, value);
  }
  const query = params.toString();
  const directory = useResource<TalentDirectoryOut>(
    `/talent/directory${query ? `?${query}` : ''}`,
  );

  function apply(): void {
    setSubmitted({
      language: language.trim(),
      language_level: languageLevel,
      level: level.trim(),
      status,
      background: background.trim(),
    });
  }

  const rows = directory.resource.status === 'ready' ? directory.resource.data.students : [];

  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Trust"
        title="Talent directory"
        description="Students who opted into employer or public visibility. Filters run on the API, so the list you see is the list a share link can support."
      />

      <Panel title="Filters">
        <div className="nv-grid--3">
          <Field
            hint="For example Yoruba, Igbo or Hausa."
            label="Language"
            value={language}
            onChange={(event) => setLanguage(event.target.value)}
          />
          <Select
            label="Language level"
            options={[
              { value: '', label: 'Any' },
              { value: 'basic', label: 'Basic' },
              { value: 'conversational', label: 'Conversational' },
              { value: 'fluent', label: 'Fluent' },
              { value: 'native', label: 'Native' },
            ]}
            value={languageLevel}
            onChange={(event) => setLanguageLevel(event.target.value)}
          />
          <Field
            hint="Study level, e.g. 200 or 300."
            label="Academic level"
            value={level}
            onChange={(event) => setLevel(event.target.value)}
          />
          <Select
            label="Visibility"
            options={[
              { value: '', label: 'Employers and public' },
              { value: 'employers', label: 'Employers only' },
              { value: 'public', label: 'Public' },
            ]}
            value={status}
            onChange={(event) => setStatus(event.target.value)}
          />
          <Field
            hint="University, department, bio or location."
            label="Background"
            value={background}
            onChange={(event) => setBackground(event.target.value)}
          />
          <div className="nv-row nv-row--end" style={{ alignItems: 'flex-end' }}>
            <Button type="button" onClick={apply}>
              Apply filters
            </Button>
          </div>
        </div>
      </Panel>

      {directory.resource.status === 'loading' ? <Skeleton lines={5} /> : null}
      {directory.resource.status === 'error' ? (
        <ErrorState
          body={directory.resource.message}
          action={
            <Button size="sm" type="button" variant="secondary" onClick={directory.reload}>
              Try again
            </Button>
          }
        />
      ) : null}

      {directory.resource.status === 'ready' ? (
        <Panel title="Students" actions={<Badge tone="neutral">{rows.length}</Badge>}>
          {rows.length === 0 ? (
            <EmptyState
              icon={Users}
              title="No student matches"
              body="No visible profile matches these filters. Widen the language or clear the background search."
            />
          ) : (
            <div className="nv-table-wrap">
              <table className="nv-table">
                <thead>
                  <tr>
                    <th>Student</th>
                    <th>Academic</th>
                    <th>Languages</th>
                    <th>Visibility</th>
                    <th>Location</th>
                  </tr>
                </thead>
                <tbody>
                  {rows.map((row) => (
                    <tr key={row.id}>
                      <td>
                        {row.display_name ?? `Student #${row.id}`}
                        <div className="nv-muted">#{row.id}</div>
                      </td>
                      <td>
                        {[row.university, row.department, row.level].filter(Boolean).join(' · ') ||
                          'Not set'}
                      </td>
                      <td>
                        {row.languages.length === 0
                          ? 'None listed'
                          : row.languages.map((item) => `${item.language} (${item.level})`).join(', ')}
                      </td>
                      <td>
                        <Badge tone={row.visibility === 'public' ? 'success' : 'info'}>
                          {row.visibility}
                        </Badge>
                      </td>
                      <td>{row.location ?? 'Not set'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Panel>
      ) : null}
    </div>
  );
}
