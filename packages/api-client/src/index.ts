/**
 * @nelavista/api-client
 *
 * The **generated** client lives in ./generated (produced from the API's OpenAPI
 * schema by `pnpm --filter @nelavista/api-client generate`). This file is the small,
 * hand-written wrapper the apps import, so generated churn never touches app code.
 *
 * The schema is generated from the API and committed; CI re-runs the generator
 * and fails when the committed client is stale (ADR-0001). Generated types are
 * re-exported from ./schema so app code never imports the generated path.
 */
export type {
  ApiPaths,
  ApplicationListOut,
  ApplicationOut,
  ApplyOut,
  AssessmentListOut,
  AssessmentOut,
  AttemptOut,
  AttemptReviewOut,
  AttemptResultOut,
  AttemptResultTaskOut,
  AttemptTaskOut,
  AssignOut,
  AssignmentDetailOut,
  AssignmentListOut,
  AssignmentOut,
  AssignmentStateOut,
  AssignmentTaskOut,
  AskAnswerOut,
  AskCitationOut,
  AskCourseRefOut,
  AskMessageOut,
  AskSessionListOut,
  AskSessionOut,
  AskSessionSummaryOut,
  AuditLogListOut,
  AuditLogOut,
  AvailabilityOut,
  BatchStateOut,
  CampusCreatedOut,
  CampusItemOut,
  CampusOut,
  CandidateListOut,
  CandidateOut,
  CbtAnswerOut,
  CbtCourseRefOut,
  CbtPracticeNextOut,
  CbtPracticeQuestionOut,
  CbtQuestionOut,
  CbtQuizOut,
  CbtRecentOut,
  CbtRecommendationOut,
  CbtResultsOut,
  CohortOut,
  CohortWriteOut,
  ConsentListOut,
  ConsentOut,
  ContentLessonListOut,
  ContentLessonOut,
  ContentPathOut,
  ContentStepOut,
  ContentTemplateOut,
  ContentPathListOut,
  ContentTemplateListOut,
  DashboardOut,
  EarningLineOut,
  EarningsOut,
  EligibilityOut,
  EnrolmentOut,
  FinancialsOut,
  FundOut,
  GapListOut,
  ImportListOut,
  ImportReportOut,
  ImportResultOut,
  InviteListOut,
  LanguagesOut,
  LedgerOut,
  LessonCompletedOut,
  LessonOut,
  MatchCheckOut,
  MatchListOut,
  MatchOut,
  MaterialChunkOut,
  MaterialCourseOut,
  MaterialDetailOut,
  MaterialListOut,
  MaterialOut,
  MaterialSearchOut,
  MaterialSearchResultOut,
  MeOut,
  MessageListOut,
  MfaEnableOut,
  MfaSetupOut,
  MfaStatusOut,
  NextStepOut,
  NotificationListOut,
  NotificationOut,
  OnboardingStateOut,
  OpportunityApplicationsOut,
  OpportunityAdminListOut,
  OpportunityAdminRowOut,
  OpportunityListOut,
  OpportunityMatchOut,
  OpportunityOut,
  OverrideOut,
  PayoutBatchDetailOut,
  PayoutBatchListOut,
  PayoutItemStateOut,
  PlatformConfigOut,
  PlatformSettingsIn,
  PlatformSettingsOut,
  PracticalQueueOut,
  PracticalReviewOut,
  PracticalSubmissionOut,
  PracticalTaskListOut,
  PracticalTaskOut,
  ProjectListOut,
  ProjectOut,
  ProjectSummaryOut,
  PushDeviceListOut,
  PushDeviceOut,
  QualityOut,
  ReconcileReportOut,
  ReconcileRunOut,
  ReplacementListOut,
  RequirementOut,
  ReverseOut,
  ReviewQueueOut,
  StandardOut,
  SubmissionListOut,
  SubmissionResultOut,
  TranscriptCountsOut,
  UniversityOut,
  UserDetailOut,
  UserListOut,
  UserSummaryOut,
  ValidatorListOut,
  WaitlistOut,
  MyLearningOut,
  NextActionOut,
  PathOut,
  PathStepOut,
  PracticeBriefOut,
  PracticeItemOut,
  PracticeResultOut,
  ProfileOut,
  RecentItemOut,
  ReviewOut,
  ReviewTaskOut,
  Schemas,
  ShareCreatedOut,
  ShareIn,
  ShareListOut,
  ShareOut,
  ShareRevokedOut,
  SkillDetailOut,
  SkillOut,
  SkillsOut,
  TalentAcademicOut,
  TalentAccountOut,
  TalentAvailabilityOut,
  TalentLanguageOut,
  TalentProfileOut,
  TalentProjectRefOut,
  TalentProjectSummaryOut,
  TalentQualityOut,
  TalentQualityOverallOut,
  TalentQualityProjectOut,
  TalentSkillOut,
  TalentTranscriptOut,
  TalentWorkEvidenceOut,
  TalentWorkHistoryOut,
  TokenOut,
  TopicStatOut,
  TranscriptEntryOut,
  TranscriptOut,
  VerificationOut,
  VerificationSkillOut,
} from './schema';

export interface ApiClientConfig {
  /** API base URL, e.g. http://localhost:8000 or https://api.nelavista.com */
  baseUrl: string;
  /** API path version, e.g. "v1" (distinct from the product version — ADR-0010). */
  apiVersion?: string;
  /** Returns the current access token, or null when signed out. */
  getAccessToken?: () => string | null | Promise<string | null>;
}

export interface ApiError {
  status: number;
  code?: string;
  message: string;
  request_id?: string;
}

/** Minimal fetch wrapper with auth + idempotency support (ADR-0007/0009). */
export function createApiClient(config: ApiClientConfig) {
  const version = config.apiVersion ?? 'v1';
  const root = config.baseUrl.replace(/\/$/, '');

  async function request<T>(
    method: string,
    path: string,
    opts: { body?: unknown; idempotencyKey?: string; headers?: Record<string, string> } = {},
  ): Promise<T> {
    const token = await config.getAccessToken?.();
    const headers: Record<string, string> = {
      Accept: 'application/json',
      'X-API-Version': version,
      ...(opts.headers ?? {}),
    };
    if (opts.body !== undefined) headers['Content-Type'] = 'application/json';
    if (token) headers['Authorization'] = `Bearer ${token}`;
    if (opts.idempotencyKey) headers['Idempotency-Key'] = opts.idempotencyKey;

    const res = await fetch(`${root}/${version}${path}`, {
      method,
      headers,
      body: opts.body === undefined ? undefined : JSON.stringify(opts.body),
    });

    if (res.status === 426) {
      // Force-update required (ADR-0010): surface a typed error for the client to handle.
      const body = await res.json().catch(() => ({}));
      throw {
        status: 426,
        code: 'upgrade_required',
        message: 'Please update the app',
        ...body,
      } as ApiError & {
        min_version?: string;
        store_url?: string;
      };
    }
    if (!res.ok) {
      // Every failure is `{ error: { code, message, request_id } }`;
      // read the envelope, not the top level, or every message is lost.
      const body = (await res.json().catch(() => ({}))) as {
        error?: { code?: string; message?: string; request_id?: string };
      };
      throw {
        status: res.status,
        code: body.error?.code ?? `http_${res.status}`,
        message: body.error?.message ?? res.statusText,
        request_id: body.error?.request_id,
      } as ApiError;
    }
    return (res.status === 204 ? undefined : await res.json()) as T;
  }

  return {
    get: <T>(path: string) => request<T>('GET', path),
    post: <T>(path: string, body?: unknown, idempotencyKey?: string) =>
      request<T>('POST', path, { body, idempotencyKey }),
    put: <T>(path: string, body?: unknown) => request<T>('PUT', path, { body }),
    del: <T>(path: string) => request<T>('DELETE', path),
  };
}

export type ApiClient = ReturnType<typeof createApiClient>;
