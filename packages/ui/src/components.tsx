import { CircleAlert, Eye, EyeOff, Inbox, Moon, Sun, TriangleAlert, type LucideIcon } from 'lucide-react';
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

export function ConfirmDialog({
  open,
  title,
  body,
  confirmLabel = 'Confirm',
  cancelLabel = 'Cancel',
  busy = false,
  busyLabel = 'Working',
  tone = 'primary',
  onConfirm,
  onCancel,
}: {
  open: boolean;
  title: string;
  body: React.ReactNode;
  confirmLabel?: string;
  cancelLabel?: string;
  busy?: boolean;
  busyLabel?: string;
  tone?: ButtonVariant;
  onConfirm: () => void;
  onCancel: () => void;
}): JSX.Element {
  const titleId = React.useId();
  const bodyId = React.useId();
  const dialogRef = React.useRef<HTMLDialogElement | null>(null);

  React.useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    if (open && !dialog.open) dialog.showModal();
    if (!open && dialog.open) dialog.close();
  }, [open]);

  React.useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    const handleCancel = (event: Event) => {
      event.preventDefault();
      if (!busy) onCancel();
    };
    dialog.addEventListener('cancel', handleCancel);
    return () => dialog.removeEventListener('cancel', handleCancel);
  }, [busy, onCancel]);

  return (
    <dialog
      aria-describedby={bodyId}
      aria-labelledby={titleId}
      className="nv-dialog"
      onClick={(event) => {
        if (event.target === dialogRef.current && !busy) onCancel();
      }}
      ref={dialogRef}
    >
      <div className="nv-dialog__panel">
        <h2 className="nv-dialog__title" id={titleId}>
          {title}
        </h2>
        <div className="nv-dialog__body" id={bodyId}>
          {body}
        </div>
        <div className="nv-dialog__actions">
          <Button disabled={busy} onClick={onCancel} type="button" variant="secondary">
            {cancelLabel}
          </Button>
          <Button disabled={busy} onClick={onConfirm} type="button" variant={tone}>
            {busy ? busyLabel : confirmLabel}
          </Button>
        </div>
      </div>
    </dialog>
  );
}

export function Field({
  label,
  hint,
  error,
  id,
  endAdornment,
  ...props
}: React.InputHTMLAttributes<HTMLInputElement> & {
  label: string;
  hint?: string;
  error?: string | null;
  endAdornment?: React.ReactNode;
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
      <div className="nv-field__control">
        <input
          id={fieldId}
          className="nv-input"
          aria-describedby={cx(hintId, errorId) || undefined}
          aria-invalid={error ? true : undefined}
          {...props}
        />
        {endAdornment}
      </div>
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

export function PasswordField({
  label,
  hint,
  error,
  ...props
}: Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> & {
  label: string;
  hint?: string;
  error?: string | null;
}): JSX.Element {
  const [visible, setVisible] = React.useState(false);
  return (
    <Field
      {...props}
      endAdornment={
        <button
          aria-label={visible ? 'Hide password' : 'Show password'}
          className="nv-field__reveal"
          onClick={() => setVisible((current) => !current)}
          title={visible ? 'Hide password' : 'Show password'}
          type="button"
        >
          {visible ? <EyeOff aria-hidden="true" size={17} /> : <Eye aria-hidden="true" size={17} />}
        </button>
      }
      error={error}
      hint={hint}
      label={label}
      type={visible ? 'text' : 'password'}
    />
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
  image,
}: {
  title: React.ReactNode;
  body?: React.ReactNode;
  action?: React.ReactNode;
  icon?: LucideIcon;
  image?: { src: string; alt: string; width?: number; height?: number };
}): JSX.Element {
  return (
    <div className={cx('nv-empty', image && 'nv-empty--media')}>
      {image ? (
        <img
          alt={image.alt}
          className="nv-empty__media"
          decoding="async"
          height={image.height ?? 800}
          loading="lazy"
          src={image.src}
          width={image.width ?? 800}
        />
      ) : (
        <Icon aria-hidden="true" size={20} strokeWidth={1.6} />
      )}
      <div className="nv-empty__copy">
        <p className="nv-empty__title">{title}</p>
        {body ? <p className="nv-empty__body">{body}</p> : null}
        {action ? <div className="nv-row">{action}</div> : null}
      </div>
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

export function ErrorNote({ message }: { message: string | null }): JSX.Element | null {
  if (!message) return null;
  return (
    <p className="nv-error" role="alert">
      <CircleAlert aria-hidden="true" size={16} style={{ display: 'inline', marginRight: 6 }} />
      {message}
    </p>
  );
}

export function BrandMark({ size = 28, className }: { size?: number; className?: string }): JSX.Element {
  return (
    <img
      alt=""
      className={cx('nv-brand-mark', className)}
      decoding="async"
      height={size}
      src="/brand/nelavista-mark.png"
      width={size}
    />
  );
}

/**
 * The page-level loading mark. The animated WebP is the primary asset; the
 * still mark replaces it when the visitor asks for reduced motion or the
 * animation cannot be loaded.
 */
export function BrandLoader({
  label = 'Loading',
  full = false,
}: {
  label?: string;
  full?: boolean;
}): JSX.Element {
  const [failed, setFailed] = React.useState(false);
  return (
    <div aria-label={label} className={cx('nv-brand-loader', full && 'nv-brand-loader--full')} role="status">
      {failed ? null : (
        <img
          alt=""
          className="nv-brand-loader__anim"
          decoding="async"
          height={144}
          onError={() => setFailed(true)}
          src="/media/nelavista-loader.webp"
          width={144}
        />
      )}
      <BrandMark
        className={cx('nv-brand-loader__still', failed && 'nv-brand-loader__still--visible')}
        size={84}
      />
    </div>
  );
}

export function ThemeToggle({
  theme,
  onToggle,
}: {
  theme: 'light' | 'dark';
  onToggle: () => void;
}): JSX.Element {
  const next = theme === 'light' ? 'dark' : 'light';
  return (
    <IconButton label={`Switch to ${next} theme`} onClick={onToggle} title={`Switch to ${next} theme`}>
      {theme === 'dark' ? <Sun aria-hidden="true" size={17} /> : <Moon aria-hidden="true" size={17} />}
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
