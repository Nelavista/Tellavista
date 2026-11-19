/**
 * Announcements and the newsletter list.
 *
 * Two things ops asks for in the first week of launch: a way to put a message
 * inside the product, and a way to email the people who asked to hear from us.
 * They are one screen because they are one message -- the channel decides where
 * it goes.
 *
 * The screen deliberately does not offer editing after publishing: the API
 * refuses it, and showing a form that cannot save is worse than showing none.
 */
import type {
  AnnouncementListOut,
  AnnouncementOut,
  NewsletterSubscriberListOut,
  NewsletterSubscriberOut,
} from '@nelavista/api-client';
import {
  Badge,
  Banner,
  ConfirmDialog,
  EmptyState,
  ErrorNote,
  ErrorState,
  PageHeader,
  Panel,
  Skeleton,
} from '@nelavista/ui';
import * as React from 'react';

import { when } from '../lib/format';
import { ApiError, http } from '../lib/http';
import { useResource } from '../lib/resource';

const AUDIENCES = ['all', 'students', 'staff'];
const CHANNELS = ['platform', 'email', 'both'];

export function Announcements(): JSX.Element {
  const list = useResource<AnnouncementListOut>('/ops/announcements');
  const subscribers = useResource<NewsletterSubscriberListOut>('/ops/newsletter/subscribers');

  const [title, setTitle] = React.useState('');
  const [body, setBody] = React.useState('');
  const [audience, setAudience] = React.useState('all');
  const [channel, setChannel] = React.useState('platform');
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [note, setNote] = React.useState<string | null>(null);
  const [pendingPublish, setPendingPublish] = React.useState<AnnouncementOut | null>(null);
  const [pendingArchive, setPendingArchive] = React.useState<AnnouncementOut | null>(null);

  const [email, setEmail] = React.useState('');

  async function compose(): Promise<void> {
    setBusy(true);
    setError(null);
    setNote(null);
    try {
      const row = await http.post<AnnouncementOut>('/ops/announcements', {
        title: title.trim(),
        body,
        audience,
        channel,
      });
      setTitle('');
      setBody('');
      list.reload();
      setNote(`Draft #${row.id} saved. Publishing is the step that sends it.`);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not save that announcement.');
    } finally {
      setBusy(false);
    }
  }

  async function publish(row: AnnouncementOut): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      const saved = await http.post<AnnouncementOut>(`/ops/announcements/${row.id}/publish`);
      list.reload();
      subscribers.reload();
      setNote(
        saved.email_recipient_count > 0
          ? `Published. ${saved.email_recipient_count} newsletter email(s) queued.`
          : 'Published in the product.',
      );
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not publish that announcement.');
    } finally {
      setBusy(false);
      setPendingPublish(null);
    }
  }

  async function archive(row: AnnouncementOut): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      await http.post<AnnouncementOut>(`/ops/announcements/${row.id}/archive`);
      list.reload();
      setNote(`Announcement #${row.id} archived. It is no longer shown in the product.`);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not archive that announcement.');
    } finally {
      setBusy(false);
      setPendingArchive(null);
    }
  }

  async function addSubscriber(): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      await http.post<NewsletterSubscriberOut>('/ops/newsletter/subscribers', {
        email: email.trim(),
        source: 'manual',
      });
      setEmail('');
      subscribers.reload();
      setNote('Address added to the newsletter list.');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not add that address.');
    } finally {
      setBusy(false);
    }
  }

  async function unsubscribe(row: NewsletterSubscriberOut): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      await http.del<NewsletterSubscriberOut>(`/ops/newsletter/subscribers/${row.id}`);
      subscribers.reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not unsubscribe that address.');
    } finally {
      setBusy(false);
    }
  }

  const statusTone = { draft: 'neutral', published: 'success', archived: 'neutral' } as const;

  return (
    <div className="nv-stack nv-stack--loose">
      <PageHeader
        eyebrow="Communications"
        title="Announcements"
        description="A message is a draft until you publish it. Publishing is the only step that shows it in the product or emails the list, and it happens once."
      />

      <ErrorNote message={error} />
      {note ? <Banner tone="success">{note}</Banner> : null}

      <Panel title="Compose">
        <div>
          <label className="nv-label" htmlFor="announcement-title">
            Title
          </label>
          <input
            className="nv-input"
            id="announcement-title"
            maxLength={200}
            value={title}
            onChange={(event) => setTitle(event.target.value)}
          />
        </div>
        <div>
          <label className="nv-label" htmlFor="announcement-body">
            Message
          </label>
          <textarea
            className="nv-textarea"
            id="announcement-body"
            rows={6}
            value={body}
            onChange={(event) => setBody(event.target.value)}
          />
        </div>
        <div className="nv-grid">
          <div>
            <label className="nv-label" htmlFor="announcement-audience">
              Audience
            </label>
            <select
              className="nv-select"
              id="announcement-audience"
              value={audience}
              onChange={(event) => setAudience(event.target.value)}
            >
              {AUDIENCES.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="nv-label" htmlFor="announcement-channel">
              Channel
            </label>
            <select
              className="nv-select"
              id="announcement-channel"
              value={channel}
              onChange={(event) => setChannel(event.target.value)}
            >
              {CHANNELS.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </div>
        </div>
        <p className="nv-muted">
          {channel === 'email'
            ? 'Email-only: nothing appears in the product.'
            : channel === 'both'
              ? 'Shown in the product and emailed to every active subscriber.'
              : 'In-product only: no email is sent.'}
        </p>
        <button
          className="nv-button"
          disabled={busy || title.trim().length < 2}
          type="button"
          onClick={() => void compose()}
        >
          Save draft
        </button>
      </Panel>

      <Panel
        title="All announcements"
        actions={
          list.resource.status === 'ready' ? (
            <span className="nv-meta">{list.resource.data.announcements.length} saved</span>
          ) : null
        }
      >
        {list.resource.status === 'loading' ? <Skeleton lines={4} /> : null}
        {list.resource.status === 'error' ? (
          <ErrorState title="Announcements did not load" body={list.resource.message} />
        ) : null}
        {list.resource.status === 'ready' && list.resource.data.announcements.length === 0 ? (
          <EmptyState
            title="Nothing composed yet"
            body="A draft is invisible until you publish it. Use Compose above."
          />
        ) : null}
        {list.resource.status === 'ready' && list.resource.data.announcements.length > 0 ? (
          <ul className="nv-list nv-list--ruled">
            {list.resource.data.announcements.map((row) => (
              <li key={row.id}>
                <div className="nv-row nv-row--between" style={{ alignItems: 'flex-start' }}>
                  <div style={{ minWidth: 0 }}>
                    <p className="nv-h4">
                      #{row.id} · {row.title}
                    </p>
                    <p className="nv-muted">{row.body.slice(0, 160) || 'No message body yet.'}</p>
                    <p className="nv-meta">
                      {row.audience} · {row.channel}
                      {row.published_at ? ` · published ${when(row.published_at)}` : ' · draft'}
                      {row.email_sent_at
                        ? ` · ${row.email_recipient_count} email(s) queued`
                        : ''}
                    </p>
                  </div>
                  <Badge tone={statusTone[row.status as keyof typeof statusTone] ?? 'neutral'}>
                    {row.status}
                  </Badge>
                </div>
                <div className="nv-row" style={{ marginTop: 'var(--nv-space-sm)' }}>
                  {row.status === 'draft' ? (
                    <button
                      className="nv-button nv-button--sm"
                      disabled={busy}
                      type="button"
                      onClick={() => setPendingPublish(row)}
                    >
                      Publish
                    </button>
                  ) : null}
                  {row.status === 'published' ? (
                    <button
                      className="nv-button nv-button--ghost nv-button--sm"
                      disabled={busy}
                      type="button"
                      onClick={() => setPendingArchive(row)}
                    >
                      Archive
                    </button>
                  ) : null}
                </div>
              </li>
            ))}
          </ul>
        ) : null}
      </Panel>

      <Panel
        title="Newsletter"
        actions={
          subscribers.resource.status === 'ready' ? (
            <span className="nv-meta">
              {subscribers.resource.data.active_count} active of{' '}
              {subscribers.resource.data.total_count}
            </span>
          ) : null
        }
      >
        <div className="nv-row" style={{ alignItems: 'flex-end' }}>
          <div style={{ flex: 1 }}>
            <label className="nv-label" htmlFor="newsletter-email">
              Add an address (with their consent)
            </label>
            <input
              className="nv-input"
              id="newsletter-email"
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
            />
          </div>
          <button
            className="nv-button nv-button--secondary"
            disabled={busy || email.trim().length < 3}
            type="button"
            onClick={() => void addSubscriber()}
          >
            Add
          </button>
        </div>

        {subscribers.resource.status === 'loading' ? <Skeleton lines={4} /> : null}
        {subscribers.resource.status === 'error' ? (
          <ErrorState title="Subscribers did not load" body={subscribers.resource.message} />
        ) : null}
        {subscribers.resource.status === 'ready' &&
        subscribers.resource.data.subscribers.length === 0 ? (
          <EmptyState
            title="Nobody has subscribed yet"
            body="The public form records an address once, and an opt-out is kept so an import cannot re-add it."
          />
        ) : null}
        {subscribers.resource.status === 'ready' &&
        subscribers.resource.data.subscribers.length > 0 ? (
          <div className="nv-table-wrap">
            <table className="nv-table">
              <thead>
                <tr>
                  <th scope="col">Address</th>
                  <th scope="col">Source</th>
                  <th scope="col">State</th>
                  <th scope="col">
                    <span className="nv-sr-only">Actions</span>
                  </th>
                </tr>
              </thead>
              <tbody>
                {subscribers.resource.data.subscribers.map((row) => (
                  <tr key={row.id}>
                    <td className="nv-mono">{row.email}</td>
                    <td>{row.source}</td>
                    <td>
                      {row.is_active ? (
                        <Badge tone="success">active</Badge>
                      ) : (
                        <Badge tone="neutral">unsubscribed</Badge>
                      )}
                    </td>
                    <td>
                      {row.is_active ? (
                        <button
                          className="nv-button nv-button--ghost nv-button--sm"
                          disabled={busy}
                          type="button"
                          onClick={() => void unsubscribe(row)}
                        >
                          Unsubscribe
                        </button>
                      ) : null}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : null}
      </Panel>

      <ConfirmDialog
        body={
          <p>
            Publishing sends this message once and cannot be undone. Email addresses that unsubscribed are
            skipped; the number sent is recorded on the announcement.
          </p>
        }
        busy={busy}
        confirmLabel="Publish"
        onCancel={() => setPendingPublish(null)}
        onConfirm={() => {
          if (pendingPublish) void publish(pendingPublish);
        }}
        open={pendingPublish !== null}
        title={`Publish "${pendingPublish?.title ?? ''}"?`}
      />

      <ConfirmDialog
        body={<p>It disappears from the product for everyone. The row and its audit trail remain.</p>}
        busy={busy}
        confirmLabel="Archive"
        onCancel={() => setPendingArchive(null)}
        onConfirm={() => {
          if (pendingArchive) void archive(pendingArchive);
        }}
        open={pendingArchive !== null}
        title={`Archive "${pendingArchive?.title ?? ''}"?`}
      />
    </div>
  );
}
