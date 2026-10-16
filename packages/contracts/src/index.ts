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
