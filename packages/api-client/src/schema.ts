/**
 * Types generated from the API's OpenAPI schema (A1).
 *
 * `./generated/schema.d.ts` is produced by `pnpm generate:api-client`; CI re-runs
 * the generator and fails if the committed file differs (ADR-0001). Import from
 * here rather than from the generated path so the generated layout can change
 * without touching app code.
 *
 * The routes the student journey reads — auth, profile, onboarding, campus, the
 * Academia dashboard and its connected screens (B14), the skills journey, the
 * verification journey and the talent profile (B13) — are modelled, and their
 * shapes come from here (A3, B7, B13, B14).
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
// `ReviewOut` exists in both the verification and work schemas. FastAPI's OpenAPI
// disambiguates duplicate class names by prefixing the module path, so both
// aliases here point at the long names: a student reviewing an attempt and an
// ops reviewer grading a submission are different shapes.
export type AttemptReviewOut = Schemas['app__api__v1__domains__verification__schemas__ReviewOut'];
export type ReviewOut = Schemas['app__api__v1__domains__work__schemas__ReviewOut'];
export type ReviewTaskOut = Schemas['ReviewTaskOut'];

// --- Practical tasks (B7) ---------------------------------------------------
export type PracticalTaskOut = Schemas['PracticalTaskOut'];
export type PracticalTaskListOut = Schemas['PracticalTaskListOut'];
export type PracticalSubmissionOut = Schemas['PracticalSubmissionOut'];
export type PracticalQueueOut = Schemas['PracticalQueueOut'];
export type PracticalReviewOut = Schemas['PracticalReviewOut'];

// --- Opportunities and matching (B8) ---------------------------------------
export type OpportunityOut = Schemas['OpportunityOut'];
export type OpportunityListOut = Schemas['OpportunityListOut'];
export type OpportunityMatchOut = Schemas['OpportunityMatchOut'];
export type MatchOut = Schemas['MatchOut'];
export type MatchListOut = Schemas['MatchListOut'];
export type MatchCheckOut = Schemas['MatchCheckOut'];
export type NextStepOut = Schemas['NextStepOut'];
export type RequirementOut = Schemas['RequirementOut'];
export type ApplicationOut = Schemas['ApplicationOut'];
export type ApplicationListOut = Schemas['ApplicationListOut'];
export type ApplyOut = Schemas['ApplyOut'];
export type GapListOut = Schemas['GapListOut'];

// --- Work (B9) --------------------------------------------------------------
export type AssignmentOut = Schemas['AssignmentOut'];
export type AssignmentListOut = Schemas['AssignmentListOut'];
export type AssignmentDetailOut = Schemas['AssignmentDetailOut'];
export type AssignmentTaskOut = Schemas['AssignmentTaskOut'];
export type AssignmentStateOut = Schemas['AssignmentStateOut'];
export type SubmissionResultOut = Schemas['SubmissionResultOut'];
export type SubmissionListOut = Schemas['SubmissionListOut'];
export type QualityOut = Schemas['QualityOut'];
export type MessageListOut = Schemas['MessageListOut'];

// --- Money (B10) ------------------------------------------------------------
export type EarningsOut = Schemas['EarningsOut'];
export type EarningLineOut = Schemas['EarningLineOut'];

// --- Materials, Ask and CBT (B14) -------------------------------------------
export type MaterialCourseOut = Schemas['MaterialCourseOut'];
export type MaterialOut = Schemas['MaterialOut'];
export type MaterialListOut = Schemas['MaterialListOut'];
export type MaterialSearchResultOut = Schemas['MaterialSearchResultOut'];
export type MaterialSearchOut = Schemas['MaterialSearchOut'];
export type MaterialChunkOut = Schemas['MaterialChunkOut'];
export type MaterialDetailOut = Schemas['MaterialDetailOut'];
export type AskCitationOut = Schemas['AskCitationOut'];
export type AskAnswerOut = Schemas['AskAnswerOut'];
export type AskCourseRefOut = Schemas['AskCourseRefOut'];
export type AskSessionSummaryOut = Schemas['AskSessionSummaryOut'];
export type AskSessionListOut = Schemas['AskSessionListOut'];
export type AskMessageOut = Schemas['AskMessageOut'];
export type AskSessionOut = Schemas['AskSessionOut'];
export type CbtCourseRefOut = Schemas['CbtCourseRefOut'];
export type CbtQuestionOut = Schemas['CbtQuestionOut'];
export type CbtQuizOut = Schemas['CbtQuizOut'];
export type CbtAnswerOut = Schemas['CbtAnswerOut'];
export type CbtRecentOut = Schemas['CbtRecentOut'];
export type CbtRecommendationOut = Schemas['CbtRecommendationOut'];
export type CbtResultsOut = Schemas['CbtResultsOut'];
export type CbtPracticeQuestionOut = Schemas['CbtPracticeQuestionOut'];
export type CbtPracticeNextOut = Schemas['CbtPracticeNextOut'];

// --- Talent profile and shares (B13) ----------------------------------------
export type TalentSkillOut = Schemas['TalentSkillOut'];
export type TalentAccountOut = Schemas['TalentAccountOut'];
export type TalentAcademicOut = Schemas['TalentAcademicOut'];
export type TalentQualityOverallOut = Schemas['TalentQualityOverallOut'];
export type TalentQualityProjectOut = Schemas['TalentQualityProjectOut'];
export type TalentQualityOut = Schemas['TalentQualityOut'];
export type TalentProjectRefOut = Schemas['TalentProjectRefOut'];
export type TalentWorkEvidenceOut = Schemas['TalentWorkEvidenceOut'];
export type TalentWorkHistoryOut = Schemas['TalentWorkHistoryOut'];
export type TalentProjectSummaryOut = Schemas['TalentProjectSummaryOut'];
export type TalentLanguageOut = Schemas['TalentLanguageOut'];
export type TalentAvailabilityOut = Schemas['TalentAvailabilityOut'];
export type TalentProfileOut = Schemas['TalentProfileOut'];
export type TalentTranscriptOut = Schemas['TalentTranscriptOut'];
export type ShareIn = Schemas['ShareIn'];
export type ShareOut = Schemas['ShareOut'];
export type ShareListOut = Schemas['ShareListOut'];
export type ShareCreatedOut = Schemas['ShareCreatedOut'];
export type ShareRevokedOut = Schemas['ShareRevokedOut'];

// --- Platform policy (G1–G5) ------------------------------------------------
export type PlatformConfigOut = Schemas['PlatformConfigOut'];
export type PlatformSettingsOut = Schemas['PlatformSettingsOut'];
export type PlatformSettingsIn = Schemas['PlatformSettingsIn'];
export type EligibilityOut = Schemas['EligibilityOut'];
export type ConsentOut = Schemas['ConsentOut'];
export type ConsentListOut = Schemas['ConsentListOut'];

// --- Settings (B11) ---------------------------------------------------------
export type LanguagesOut = Schemas['LanguagesOut'];
export type AvailabilityOut = Schemas['AvailabilityOut'];
export type NotificationListOut = Schemas['NotificationListOut'];
export type NotificationOut = Schemas['NotificationOut'];
export type PushDeviceListOut = Schemas['PushDeviceListOut'];
export type PushDeviceOut = Schemas['PushDeviceOut'];

// --- Admin ops (C1–C7) ------------------------------------------------------
export type MfaSetupOut = Schemas['MfaSetupOut'];
export type MfaEnableOut = Schemas['MfaEnableOut'];
export type MfaStatusOut = Schemas['MfaStatusOut'];
export type AuditLogListOut = Schemas['AuditLogListOut'];
export type AuditLogOut = Schemas['AuditLogOut'];
export type ImportListOut = Schemas['ImportListOut'];
export type ImportReportOut = Schemas['ImportReportOut'];
export type ImportResultOut = Schemas['ImportResultOut'];
export type UserListOut = Schemas['UserListOut'];
export type UserSummaryOut = Schemas['UserSummaryOut'];
export type UserDetailOut = Schemas['UserDetailOut'];
export type WaitlistOut = Schemas['WaitlistOut'];
export type CandidateListOut = Schemas['CandidateListOut'];
export type CandidateOut = Schemas['CandidateOut'];
export type OpportunityAdminListOut = Schemas['OpportunityAdminListOut'];
export type OpportunityAdminRowOut = Schemas['OpportunityAdminRowOut'];
export type OpportunityApplicationsOut = Schemas['OpportunityApplicationsOut'];
export type ProjectOut = Schemas['ProjectOut'];
export type ProjectListOut = Schemas['ProjectListOut'];
export type ProjectSummaryOut = Schemas['ProjectSummaryOut'];
export type CohortOut = Schemas['CohortOut'];
export type CohortWriteOut = Schemas['CohortWriteOut'];
export type InviteListOut = Schemas['InviteListOut'];
export type ReplacementListOut = Schemas['ReplacementListOut'];
export type AssignOut = Schemas['AssignOut'];
export type ReviewQueueOut = Schemas['ReviewQueueOut'];
export type FinancialsOut = Schemas['FinancialsOut'];
export type FundOut = Schemas['FundOut'];
export type ReverseOut = Schemas['ReverseOut'];
export type LedgerOut = Schemas['LedgerOut'];
export type PayoutBatchListOut = Schemas['PayoutBatchListOut'];
export type PayoutBatchDetailOut = Schemas['PayoutBatchDetailOut'];
export type BatchStateOut = Schemas['BatchStateOut'];
export type PayoutItemStateOut = Schemas['PayoutItemStateOut'];
export type ReconcileRunOut = Schemas['ReconcileRunOut'];
export type ReconcileReportOut = Schemas['ReconcileReportOut'];
export type ContentLessonListOut = Schemas['ContentLessonListOut'];
export type ContentLessonOut = Schemas['ContentLessonOut'];
export type ContentPathOut = Schemas['ContentPathOut'];
export type ContentTemplateOut = Schemas['ContentTemplateOut'];
export type ContentStepOut = Schemas['ContentStepOut'];
export type ContentPathListOut = Schemas['ContentPathListOut'];
export type ContentTemplateListOut = Schemas['ContentTemplateListOut'];
export type ValidatorListOut = Schemas['ValidatorListOut'];
export type OnboardingStateOut = Schemas['OnboardingStateOut'];
export type TranscriptCountsOut = Schemas['TranscriptCountsOut'];
export type OverrideOut = Schemas['OverrideOut'];
export type StandardOut = Schemas['StandardOut'];
