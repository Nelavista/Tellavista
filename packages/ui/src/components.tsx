import {
  ArrowRight,
  CircleAlert,
  Inbox,
  LoaderCircle,
  Moon,
  Sun,
  TriangleAlert,
  type LucideIcon,
} from 'lucide-react';
import * as React from 'react';

type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'danger';
type ButtonSize = 'md' | 'sm';

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(' ');
}

export function Button({
  variant = 'primary',
  size = 'md',
  block = false,
  className,
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: ButtonVariant;
  size?: ButtonSize;
  block?: boolean;
}): JSX.Element {
  return (
    <button
      {...props}
      className={cx(
        'nv-button',
        variant !== 'primary' && `nv-button--${variant}`,
        size === 'sm' && 'nv-button--sm',
        block && 'nv-button--block',
        className,
      )}
    />
  );
}

export function IconButton({
  label,
  className,
  children,
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement> & { label: string }): JSX.Element {
  return (
    <button {...props} aria-label={label} className={cx('nv-icon-button', className)}>
      {children}
    </button>
  );
}

export function Field({
  label,
  hint,
  error,
  id,
  ...props
}: React.InputHTMLAttributes<HTMLInputElement> & {
  label: string;
  hint?: string;
  error?: string | null;
}): JSX.Element {
  const generated = React.useId();
  const fieldId = id ?? generated;
  const hintId = hint ? `${fieldId}-hint` : undefined;
  const errorId = error ? `${fieldId}-error` : undefined;
  return (
    <div className="nv-field">
      <label className="nv-label" htmlFor={fieldId}>
        {label}
      </label>
      <input
        id={fieldId}
        className="nv-input"
        aria-describedby={cx(hintId, errorId) || undefined}
        aria-invalid={error ? true : undefined}
        {...props}
      />
      {hint ? (
        <span className="nv-field__hint" id={hintId}>
          {hint}
        </span>
      ) : null}
      {error ? (
        <span className="nv-field__error" id={errorId}>
          {error}
        </span>
      ) : null}
    </div>
  );
}

export function Textarea({
  label,
  hint,
  error,
  id,
  ...props
}: React.TextareaHTMLAttributes<HTMLTextAreaElement> & {
  label: string;
  hint?: string;
  error?: string | null;
}): JSX.Element {
  const generated = React.useId();
  const fieldId = id ?? generated;
  const hintId = hint ? `${fieldId}-hint` : undefined;
  const errorId = error ? `${fieldId}-error` : undefined;
  return (
    <div className="nv-field">
      <label className="nv-label" htmlFor={fieldId}>
        {label}
      </label>
      <textarea
        id={fieldId}
        className="nv-textarea"
        aria-describedby={cx(hintId, errorId) || undefined}
        aria-invalid={error ? true : undefined}
        {...props}
      />
      {hint ? (
        <span className="nv-field__hint" id={hintId}>
          {hint}
        </span>
      ) : null}
      {error ? (
        <span className="nv-field__error" id={errorId}>
          {error}
        </span>
      ) : null}
    </div>
  );
}

export function Select({
  label,
  hint,
  error,
  options,
  id,
  ...props
}: React.SelectHTMLAttributes<HTMLSelectElement> & {
  label: string;
  hint?: string;
  error?: string | null;
  options: Array<{ value: string; label: string }>;
}): JSX.Element {
  const generated = React.useId();
  const fieldId = id ?? generated;
  const hintId = hint ? `${fieldId}-hint` : undefined;
  const errorId = error ? `${fieldId}-error` : undefined;
  return (
    <div className="nv-field">
      <label className="nv-label" htmlFor={fieldId}>
        {label}
      </label>
      <select
        id={fieldId}
        className="nv-select"
        aria-describedby={cx(hintId, errorId) || undefined}
        aria-invalid={error ? true : undefined}
        {...props}
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {hint ? (
        <span className="nv-field__hint" id={hintId}>
          {hint}
        </span>
      ) : null}
      {error ? (
        <span className="nv-field__error" id={errorId}>
          {error}
        </span>
      ) : null}
    </div>
  );
}

export function Checkbox({
  label,
  className,
  ...props
}: React.InputHTMLAttributes<HTMLInputElement> & { label: React.ReactNode }): JSX.Element {
  return (
    <label className={cx('nv-check', className)}>
      <input type="checkbox" {...props} />
      <span>{label}</span>
    </label>
  );
}

export function Card({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>): JSX.Element {
  return (
    <div {...props} className={cx('nv-card', className)}>
      {children}
    </div>
  );
}

export function Panel({
  title,
  actions,
  children,
  footer,
  className,
}: {
  title?: React.ReactNode;
  actions?: React.ReactNode;
  children: React.ReactNode;
  footer?: React.ReactNode;
  className?: string;
}): JSX.Element {
  return (
    <section className={cx('nv-panel', className)}>
      {title || actions ? (
        <header className="nv-panel__head">
          {title ? <h2 className="nv-h3">{title}</h2> : <span />}
          {actions ? <div className="nv-row">{actions}</div> : null}
        </header>
      ) : null}
      <div className="nv-panel__body">{children}</div>
      {footer ? <footer className="nv-panel__foot">{footer}</footer> : null}
    </section>
  );
}

export function PageHeader({
  eyebrow,
  title,
  description,
  actions,
}: {
  eyebrow?: React.ReactNode;
  title: React.ReactNode;
  description?: React.ReactNode;
  actions?: React.ReactNode;
}): JSX.Element {
  return (
    <header className="nv-stack nv-stack--tight">
      {eyebrow ? <span className="nv-eyebrow">{eyebrow}</span> : null}
      <div className="nv-row nv-row--between">
        <h1 className="nv-h1">{title}</h1>
        {actions ? <div className="nv-row">{actions}</div> : null}
      </div>
      {description ? <p className="nv-lede">{description}</p> : null}
    </header>
  );
}

export function Stamp({
  tone = 'accent',
  children,
}: {
  tone?: 'accent' | 'success' | 'danger';
  children: React.ReactNode;
}): JSX.Element {
  return (
    <span
      className={cx(
        'nv-stamp',
        tone === 'success' && 'nv-stamp--verified',
        tone === 'accent' && 'nv-stamp--paid',
      )}
    >
      {children}
    </span>
  );
}

export function Badge({
  tone = 'neutral',
  status,
  children,
}: {
  tone?: 'neutral' | 'success' | 'info' | 'warning' | 'danger';
  /** Machine-readable state for tests and automation; never the only signal. */
  status?: string;
  children: React.ReactNode;
}): JSX.Element {
  return (
    <span className={cx('nv-badge', tone !== 'neutral' && `nv-badge--${tone}`)} data-status={status}>
      {children}
    </span>
  );
}

export function Banner({
  tone = 'info',
  children,
  actions,
}: {
  tone?: 'info' | 'success' | 'warning' | 'danger';
  children: React.ReactNode;
  actions?: React.ReactNode;
}): JSX.Element {
  return (
    <div className={cx('nv-banner', `nv-banner--${tone}`)} role={tone === 'danger' ? 'alert' : 'status'}>
      <div>{children}</div>
      {actions ? <div className="nv-row">{actions}</div> : null}
    </div>
  );
}

export function EmptyState({
  title,
  body,
  action,
  icon: Icon = Inbox,
}: {
  title: React.ReactNode;
  body?: React.ReactNode;
  action?: React.ReactNode;
  icon?: LucideIcon;
}): JSX.Element {
  return (
    <div className="nv-empty">
      <Icon aria-hidden="true" size={20} strokeWidth={1.6} />
      <p className="nv-empty__title">{title}</p>
      {body ? <p className="nv-empty__body">{body}</p> : null}
      {action ? <div className="nv-row">{action}</div> : null}
    </div>
  );
}

export function ErrorState({
  title = 'That did not load',
  body,
  action,
}: {
  title?: React.ReactNode;
  body?: React.ReactNode;
  action?: React.ReactNode;
}): JSX.Element {
  return (
    <div className="nv-error-state" role="alert">
      <TriangleAlert aria-hidden="true" size={20} strokeWidth={1.6} />
      <p className="nv-error-state__title">{title}</p>
      {body ? <p className="nv-error-state__body">{body}</p> : null}
      {action ? <div className="nv-row">{action}</div> : null}
    </div>
  );
}

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

export function Spinner({ label = 'Loading' }: { label?: string }): JSX.Element {
  return (
    <span className="nv-row" role="status" aria-label={label}>
      <LoaderCircle className="nv-spin" aria-hidden="true" size={18} />
    </span>
  );
}

export function ErrorNote({ message }: { message: string | null }): JSX.Element | null {
  if (!message) return null;
  return (
    <p className="nv-error" role="alert">
      <CircleAlert aria-hidden="true" size={16} style={{ display: 'inline', marginRight: 6 }} />
      {message}
    </p>
  );
}

export function Logo({ to = '/', compact = false }: { to?: string; compact?: boolean }): JSX.Element {
  return (
    <a className="nv-public__brand" href={to} aria-label="Nelavista home">
      <span className="nv-public__brand-mark" aria-hidden="true">
        NV
      </span>
      {compact ? null : <span>Nelavista</span>}
    </a>
  );
}

export function ThemeToggle({
  theme,
  onToggle,
}: {
  theme: 'ink' | 'paper';
  onToggle: () => void;
}): JSX.Element {
  const next = theme === 'ink' ? 'paper' : 'ink';
  return (
    <IconButton label={`Switch to ${next} theme`} onClick={onToggle} title={`Switch to ${next} theme`}>
      {theme === 'ink' ? <Sun aria-hidden="true" size={17} /> : <Moon aria-hidden="true" size={17} />}
    </IconButton>
  );
}

export function Avatar({ name }: { name: string }): JSX.Element {
  const initials = name
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join('');
  return (
    <span className="nv-avatar" aria-hidden="true">
      {initials || 'N'}
    </span>
  );
}

export function ArrowLink({
  to,
  children,
  className,
}: {
  to: string;
  children: React.ReactNode;
  className?: string;
}): JSX.Element {
  return (
    <a className={cx('nv-link-arrow', className)} href={to}>
      {children}
      <ArrowRight aria-hidden="true" size={16} />
    </a>
  );
}
