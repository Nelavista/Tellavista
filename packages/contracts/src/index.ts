/**
 * Shared contracts. Types that must be identical across API, web, admin and mobile.
 * Money and status types live here so they can never drift between clients.
 */

/** Money is ALWAYS integer minor units + an explicit currency (ADR-0008). */
export interface Money {
  amount_minor: number;
  currency: string; // ISO 4217, e.g. "NGN"
}

export function formatMoney(m: Money, locale = 'en-NG'): string {
  const major = m.amount_minor / 100;
  return new Intl.NumberFormat(locale, { style: 'currency', currency: m.currency }).format(major);
}

/** Cursor pagination (ADR-0007) — no offset paging on large sets. */
export interface Page<T> {
  items: T[];
  next_cursor: string | null;
}

export interface PaginationQuery {
  cursor?: string;
  limit?: number;
}

/** The three independent statuses a managed project tracks (PRD §12). */
export type WorkStatus = 'unassigned' | 'assigned' | 'in_progress' | 'submitted' | 'completed';
export type QualityStatus = 'not_reviewed' | 'in_review' | 'approved' | 'needs_revision' | 'rejected';
export type PaymentStatus = 'unpaid' | 'pending' | 'paid' | 'reversed';

/** Opportunity type gates the fee rule (PRD §11): fee applies to `managed` only. */
export type OpportunityType = 'managed' | 'external';

/** API version pinned separately from the product version (ADR-0010). */
export const API_PATH_VERSION = 'v1' as const;

/**
 * Every API failure is the same envelope (app/core/errors.py). `code` is the
 * machine-readable contract; `message` is safe to show a student.
 */
export interface ApiErrorEnvelope {
  error: {
    code: string;
    message: string;
    details?: unknown;
    request_id?: string;
  };
}

/** The three student paths (PRD §6). Switching never deletes prior work. */
export type PreferredPath = 'academia' | 'skills' | 'both';

// `Me` and `AuthToken` deliberately do not live here any more: both come from
// the API's own schema. Import `MeOut` and `TokenOut` from `@nelavista/api-client`
// so those two can never drift from the server (A1).

export interface Profile {
  display_name: string | null;
  bio: string | null;
  location: string | null;
  avatar_url: string | null;
  locale: string;
  timezone: string | null;
  preferred_path: PreferredPath | string | null;
  notify_email: boolean;
  notify_push: boolean;
  profile_visibility: string;
  date_of_birth: string | null;
  onboarding_completed_at: string | null;
}

export interface University {
  id: number;
  name: string;
  slug: string;
}

export interface Subdivision {
  id: number;
  name: string;
}

export interface Course {
  id: number;
  code: string;
  title: string;
  level: string;
}

export interface Semester {
  id: number;
  name: string;
  ordinal: number;
  session_id: number;
}

export interface Enrolment {
  enrolment_id: number;
  course_id: number;
  code: string;
  title: string;
  level: string;
  session_id: number;
  semester_id: number | null;
  status: string;
  department: string;
  faculty: string;
  university: string;
}

export interface OnboardingState {
  profile_completed: boolean;
  has_enrolment: boolean;
  current_semester: Semester | null;
  academic: Record<string, unknown>;
  enrolments: Enrolment[];
  next_step: 'choose_path' | 'enrol' | 'ready';
}

/*
 * The journey responses the web app reads — the Academia dashboard, campus and
 * the whole skills path — are **not** declared here. Those routes have
 * `response_model`s, so their shapes are generated from the API and exported by
 * `@nelavista/api-client` (`DashboardOut`, `CampusOut`, `PathOut`, …). Keeping a
 * second copy here is how the two drift apart, so there isn't one (A3).
 */
