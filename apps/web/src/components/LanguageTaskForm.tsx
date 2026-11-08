/**
 * Structured language-data task form.
 *
 * Renders the four African Languages Lab task kinds from the task spec the API
 * already sends on the practice brief: transcription, translation, labeling and
 * recording. Listening and labelling quality is scored server-side; this form
 * only collects the response envelope.
 */
import { Badge, Banner, Button, Field, Select, Textarea } from '@nelavista/ui';
import { CheckCircle2, Circle, Mic, Square } from 'lucide-react';
import * as React from 'react';

import {
  type LanguageResponses,
  type LanguageTaskSpec,
  type RecordingMetrics,
} from '../lib/language-task';

type Value = string | number | boolean;

function recordOf(value: unknown): Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : {};
}

function textOf(value: unknown): string {
  return typeof value === 'string' ? value : '';
}

function RecordingPrompt({
  prompt,
  metrics,
  onChange,
}: {
  prompt: { id: string; text: string };
  metrics: RecordingMetrics | null;
  onChange: (metrics: RecordingMetrics | null) => void;
}): JSX.Element {
  const [recording, setRecording] = React.useState(false);
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const recorder = React.useRef<MediaRecorder | null>(null);
  const chunks = React.useRef<Blob[]>([]);

  async function analyse(blob: Blob): Promise<RecordingMetrics> {
    const AudioContextClass =
      window.AudioContext ??
      (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
    if (!AudioContextClass) throw new Error('Audio analysis is not available in this browser.');
    const context = new AudioContextClass();
    try {
      const buffer = await context.decodeAudioData(await blob.arrayBuffer());
      const samples = buffer.getChannelData(0);
      let clipped = 0;
      let squared = 0;
      for (const sample of samples) {
        if (Math.abs(sample) >= 0.99) clipped += 1;
        squared += sample * sample;
      }
      const frameSize = 1024;
      let silentFrames = 0;
      let frames = 0;
      for (let start = 0; start < samples.length; start += frameSize) {
        const end = Math.min(start + frameSize, samples.length);
        let frameSquared = 0;
        for (let index = start; index < end; index += 1) {
          frameSquared += samples[index] ?? 0;
        }
        if (Math.sqrt(frameSquared / (end - start)) < 0.01) silentFrames += 1;
        frames += 1;
      }
      const rms = samples.length > 0 ? Math.sqrt(squared / samples.length) : 0;
      return {
        duration_seconds: buffer.duration,
        clip_pct: samples.length > 0 ? (100 * clipped) / samples.length : 100,
        rms_db: rms > 0 ? 20 * Math.log10(rms) : -100,
        silence_pct: frames > 0 ? (100 * silentFrames) / frames : 100,
      };
    } finally {
      void context.close();
    }
  }

  async function start(): Promise<void> {
    setError(null);
    if (!navigator.mediaDevices?.getUserMedia || typeof MediaRecorder === 'undefined') {
      setError('This browser cannot record audio. Try a recent Chrome, Edge or Safari.');
      return;
    }
    setBusy(true);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      chunks.current = [];
      const next = new MediaRecorder(stream);
      recorder.current = next;
      next.ondataavailable = (event) => {
        if (event.data.size > 0) chunks.current.push(event.data);
      };
      next.onstop = () => {
        stream.getTracks().forEach((track) => track.stop());
        const blob = new Blob(chunks.current, { type: next.mimeType || 'audio/webm' });
        void analyse(blob)
          .then((result) => onChange(result))
          .catch((err: unknown) =>
            setError(err instanceof Error ? err.message : 'Could not read that recording.'),
          )
          .finally(() => setBusy(false));
      };
      next.start();
      setRecording(true);
    } catch {
      setError('Microphone access was not granted.');
      setBusy(false);
    }
  }

  function stop(): void {
    recorder.current?.stop();
    setRecording(false);
  }

  return (
    <div className="nv-card nv-stack nv-stack--tight">
      <p>{prompt.text}</p>
      <div className="nv-row">
        {recording ? (
          <Button size="sm" type="button" variant="danger" onClick={stop}>
            <Square aria-hidden="true" size={14} />
            Stop recording
          </Button>
        ) : (
          <Button disabled={busy} size="sm" type="button" variant="secondary" onClick={() => void start()}>
            <Mic aria-hidden="true" size={14} />
            {metrics ? 'Record again' : 'Record'}
          </Button>
        )}
        {metrics ? (
          <Badge tone="success">
            <CheckCircle2 aria-hidden="true" size={12} />
            {metrics.duration_seconds.toFixed(1)}s captured
          </Badge>
        ) : null}
      </div>
      {metrics ? (
        <p className="nv-meta">
          Level {metrics.rms_db.toFixed(1)} dBFS · {metrics.clip_pct.toFixed(1)}% clipped ·{' '}
          {metrics.silence_pct.toFixed(0)}% silence. Your browser measured this; the API scores it.
        </p>
      ) : null}
      {error ? <Banner tone="danger">{error}</Banner> : null}
    </div>
  );
}

export function LanguageTaskForm({
  spec,
  responses,
  onChange,
}: {
  spec: LanguageTaskSpec;
  responses: LanguageResponses;
  onChange: (next: LanguageResponses) => void;
}): JSX.Element {
  function set(key: string, value: unknown): void {
    onChange({ ...responses, [key]: value });
  }

  function setField(itemId: string, field: string, value: Value): void {
    const item = recordOf(responses[itemId]);
    set(itemId, { ...item, [field]: value });
  }

  return (
    <div className="nv-stack">
      {spec.brief ? <p>{spec.brief}</p> : null}
      {spec.guidelines?.length ? (
        <div className="nv-card nv-stack nv-stack--tight">
          <p className="nv-eyebrow">Guidelines</p>
          <ul className="nv-list">
            {spec.guidelines.map((line) => (
              <li key={line} className="nv-row">
                <Circle aria-hidden="true" size={10} />
                <span>{line}</span>
              </li>
            ))}
          </ul>
        </div>
      ) : null}

      {spec.kind === 'transcription' ? (
        <div className="nv-stack">
          <p className="nv-muted">
            {spec.mode === 'clean'
              ? 'Write the clean transcript: no filler words, keep the meaning.'
              : 'Write the verbatim transcript, including tags such as [inaudible].'}
          </p>
          {(spec.segments ?? []).map((segment) => {
            const value = responses[segment.id];
            const rich =
              typeof value === 'object' && value !== null
                ? recordOf(value)
                : { text: textOf(value) };
            const usesSpeaker = Boolean(segment.speaker_required);
            const usesStart = Boolean(segment.start_required);
            return (
              <div className="nv-card nv-stack nv-stack--tight" key={segment.id}>
                {segment.context ? <p className="nv-meta">{segment.context}</p> : null}
                <Textarea
                  label={`Segment ${segment.id}`}
                  rows={3}
                  value={textOf(rich.text)}
                  onChange={(event) => {
                    if (!usesSpeaker && !usesStart) {
                      set(segment.id, event.target.value);
                    } else {
                      setField(segment.id, 'text', event.target.value);
                    }
                  }}
                />
                {usesSpeaker || usesStart ? (
                  <div className="nv-grid--2">
                    {usesSpeaker ? (
                      <Select
                        label="Speaker"
                        options={[
                          { value: '', label: 'Choose a speaker' },
                          ...(spec.speakers ?? []).map((speaker) => ({
                            value: speaker,
                            label: speaker,
                          })),
                        ]}
                        value={textOf(rich.speaker)}
                        onChange={(event) => setField(segment.id, 'speaker', event.target.value)}
                      />
                    ) : null}
                    {usesStart ? (
                      <Field
                        hint="Seconds or mm:ss.s"
                        label="Start time"
                        value={textOf(rich.start)}
                        onChange={(event) => setField(segment.id, 'start', event.target.value)}
                      />
                    ) : null}
                  </div>
                ) : null}
              </div>
            );
          })}
        </div>
      ) : null}

      {spec.kind === 'translation' ? (
        <div className="nv-stack">
          <p className="nv-muted">
            Translate {spec.source_lang ?? 'the source'} into {spec.target_lang ?? 'the target'}. Keep
            the key terms natural, not word-for-word.
          </p>
          {(spec.items ?? []).map((item) => (
            <div className="nv-card nv-stack nv-stack--tight" key={item.id}>
              <p className="nv-eyebrow">
                {item.id}
                {item.context ? <span className="nv-muted"> · {item.context}</span> : null}
              </p>
              <p>{item.source}</p>
              <Textarea
                label="Your translation"
                rows={3}
                value={textOf(responses[item.id])}
                onChange={(event) => set(item.id, event.target.value)}
              />
            </div>
          ))}
        </div>
      ) : null}

      {spec.kind === 'labeling' ? (
        <div className="nv-stack">
          {(spec.items ?? []).map((item) => {
            const values = recordOf(responses[item.id]);
            return (
              <div className="nv-card nv-stack nv-stack--tight" key={item.id}>
                <p className="nv-eyebrow">
                  {item.id}
                  {item.repeat_of ? <span className="nv-muted"> · repeat check</span> : null}
                </p>
                {item.context ? <p className="nv-meta">{item.context}</p> : null}
                <p>{item.text}</p>
                {(item.fields ?? []).map((field) => {
                  const value = textOf(values[field.name]);
                  if (field.type === 'text') {
                    return (
                      <Textarea
                        key={field.name}
                        label={field.label ?? field.name}
                        rows={2}
                        value={value}
                        onChange={(event) => setField(item.id, field.name, event.target.value)}
                      />
                    );
                  }
                  if (field.type === 'number') {
                    return (
                      <Field
                        key={field.name}
                        label={field.label ?? field.name}
                        type="number"
                        value={value}
                        onChange={(event) => setField(item.id, field.name, event.target.value)}
                      />
                    );
                  }
                  return (
                    <fieldset className="nv-field" key={field.name}>
                      <legend className="nv-label">{field.label ?? field.name}</legend>
                      {(field.options ?? []).map((option) => (
                        <label className="nv-check" key={option}>
                          <input
                            checked={value === option}
                            name={`${item.id}-${field.name}`}
                            type="radio"
                            value={option}
                            onChange={() => setField(item.id, field.name, option)}
                          />
                          {option}
                        </label>
                      ))}
                    </fieldset>
                  );
                })}
              </div>
            );
          })}
          {spec.report ? (
            <div className="nv-card nv-stack nv-stack--tight">
              <Textarea
                label={spec.report.label ?? 'Written report'}
                rows={5}
                value={textOf(responses.report)}
                onChange={(event) => set('report', event.target.value)}
              />
              <p className="nv-meta">
                At least {spec.report.min_words ?? 15} words. It is scored separately from the labels.
              </p>
            </div>
          ) : null}
        </div>
      ) : null}

      {spec.kind === 'recording' ? (
        <div className="nv-stack">
          <p className="nv-muted">
            Record each prompt in one clean take. The browser measures length, level, clipping and
            silence; the API checks them against the task requirements.
          </p>
          {(spec.prompts ?? []).map((prompt) => (
            <RecordingPrompt
              key={prompt.id}
              prompt={prompt}
              metrics={(responses[prompt.id] as RecordingMetrics | null) ?? null}
              onChange={(metrics) => set(prompt.id, metrics)}
            />
          ))}
          {(spec.metadata_fields ?? []).length > 0 ? (
            <div className="nv-card nv-stack nv-stack--tight">
              <p className="nv-eyebrow">Recording details</p>
              {(spec.metadata_fields ?? []).map((field) => {
                const metadata = recordOf(responses.metadata);
                const value = textOf(metadata[field.name]);
                const update = (next: string): void =>
                  set('metadata', { ...metadata, [field.name]: next });
                return field.options?.length ? (
                  <Select
                    key={field.name}
                    label={field.label ?? field.name}
                    options={[
                      { value: '', label: 'Choose one' },
                      ...field.options.map((option) => ({ value: option, label: option })),
                    ]}
                    value={value}
                    onChange={(event) => update(event.target.value)}
                  />
                ) : (
                  <Field
                    key={field.name}
                    label={field.label ?? field.name}
                    value={value}
                    onChange={(event) => update(event.target.value)}
                  />
                );
              })}
            </div>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}
