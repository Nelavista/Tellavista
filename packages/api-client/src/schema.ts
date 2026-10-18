/**
 * Types generated from the API's OpenAPI schema (A1).
 *
 * `./generated/schema.d.ts` is produced by `pnpm generate:api-client`; CI re-runs
 * the generator and fails if the committed file differs (ADR-0001). Import from
 * here rather than from the generated path so the generated layout can change
 * without touching app code.
 *
 * Routes that still return a bare `dict` (materials, CBT, Ask) have no
 * `response_model` yet, so the generated schema cannot describe them. The routes
 * the student journey reads — auth, profile, onboarding, campus, the Academia
 * dashboard, all of `/v1/skills` and the verification journey — are modelled, and
 * their shapes come from here (A3, B7).
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
/** One enrolment, as the onboarding and dashboard routes return it. */
export type EnrolmentOut = Schemas['EnrolmentOut'];

// --- Academia dashboard (`/v1/academia/dashboard`) --------------------------
export type DashboardOut = Schemas['DashboardOut'];
export type NextActionOut = Schemas['NextActionOut'];
export type TopicStatOut = Schemas['TopicStatOut'];
export type PracticeItemOut = Schemas['PracticeItemOut'];
export type RecentItemOut = Schemas['RecentItemOut'];

// --- Campus (`/v1/me/campus`) ----------------------------------------------
export type CampusOut = Schemas['CampusOut'];
export type CampusItemOut = Schemas['CampusItemOut'];

// --- Skills journey (`/v1/skills/*`) ---------------------------------------
export type SkillOut = Schemas['SkillOut'];
export type SkillsOut = Schemas['SkillsOut'];
export type SkillDetailOut = Schemas['SkillDetailOut'];
export type PathOut = Schemas['PathOut'];
export type PathStepOut = Schemas['PathStepOut'];
export type MyLearningOut = Schemas['MyLearningOut'];
export type LessonOut = Schemas['LessonOut'];
export type LessonCompletedOut = Schemas['LessonCompletedOut'];
export type PracticeBriefOut = Schemas['PracticeBriefOut'];
export type PracticeResultOut = Schemas['PracticeResultOut'];

// --- Verification journey (`/v1/verification/*`) ----------------------------
export type VerificationOut = Schemas['VerificationOut'];
export type VerificationSkillOut = Schemas['VerificationSkillOut'];
export type TranscriptOut = Schemas['TranscriptOut'];
export type TranscriptEntryOut = Schemas['TranscriptEntryOut'];
export type AssessmentOut = Schemas['AssessmentOut'];
export type AssessmentListOut = Schemas['AssessmentListOut'];
export type AttemptOut = Schemas['AttemptOut'];
export type AttemptTaskOut = Schemas['AttemptTaskOut'];
export type AttemptResultOut = Schemas['AttemptResultOut'];
export type AttemptResultTaskOut = Schemas['AttemptResultTaskOut'];
export type ReviewOut = Schemas['ReviewOut'];
export type ReviewTaskOut = Schemas['ReviewTaskOut'];
