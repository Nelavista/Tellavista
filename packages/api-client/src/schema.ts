/**
 * Types generated from the API's OpenAPI schema (A1).
 *
 * `./generated/schema.d.ts` is produced by `pnpm generate:api-client`; CI re-runs
 * the generator and fails if the committed file differs (ADR-0001). Import from
 * here rather than from the generated path so the generated layout can change
 * without touching app code.
 *
 * Routes that return a bare `dict` (dashboard, campus, most journey reads) have
 * no `response_model` yet, so the generated schema cannot describe them. Those
 * shapes live in `@nelavista/contracts` until the routes gain models.
 */
import type { components, paths } from './generated/schema';

export type ApiPaths = paths;
export type Schemas = components['schemas'];

/** Signed-in user, as returned by `/v1/auth/me`. */
export type MeOut = Schemas['MeOut'];
/** Session token pair; cookie clients only use `access_token`. */
export type TokenOut = Schemas['TokenOut'];
/** The student's own profile (`/v1/me`). */
export type ProfileOut = Schemas['ProfileOut'];
