/** Small, dependency-free primitives. Tailwind is deliberately not added yet. */
import * as React from 'react';

export function Button({
  variant = 'primary',
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'ghost';
}): JSX.Element {
  const cls = variant === 'ghost' ? 'nv-button nv-button--ghost' : 'nv-button';
  return <button {...props} className={cls} />;
}

export function Field({
  label,
  hint,
  ...props
}: React.InputHTMLAttributes<HTMLInputElement> & { label: string; hint?: string }): JSX.Element {
  const id = React.useId();
  return (
    <div className="nv-field">
      <label className="nv-label" htmlFor={id}>
        {label}
      </label>
      <input id={id} className="nv-input" {...props} />
      {hint ? <span className="nv-muted">{hint}</span> : null}
    </div>
  );
}

export function Select({
  label,
  options,
  ...props
}: React.SelectHTMLAttributes<HTMLSelectElement> & {
  label: string;
  options: Array<{ value: string; label: string }>;
}): JSX.Element {
  const id = React.useId();
  return (
    <div className="nv-field">
      <label className="nv-label" htmlFor={id}>
        {label}
      </label>
      <select id={id} className="nv-select" {...props}>
        {options.map((o) => (
          <option key={o.value} value={o.value}>
            {o.label}
          </option>
        ))}
      </select>
    </div>
  );
}

/**
 * A skeleton block, never a spinner (B12): the page keeps its shape while data
 * arrives, so nothing jumps and the screen reads as "loading", not "stuck".
 */
export function Skeleton({
  lines = 1,
  width = '100%',
  height,
}: {
  lines?: number;
  width?: string;
  height?: string;
}): JSX.Element {
  return (
    <div className="nv-skeleton-group" aria-hidden="true">
      {Array.from({ length: lines }, (_, index) => (
        <span
          className="nv-skeleton"
          key={index}
          style={{ width: index === lines - 1 && lines > 1 ? '60%' : width, height }}
        />
      ))}
    </div>
  );
}

export function ErrorNote({ message }: { message: string | null }): JSX.Element | null {
  if (!message) return null;
  return (
    <p className="nv-error" role="alert">
      {message}
    </p>
  );
}
