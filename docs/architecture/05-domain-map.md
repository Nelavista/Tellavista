# 05 — Domain map (PRD entities ↔ V1 tables)

**A map only. No migrations here.** It shows the target entities the PRD implies, how they relate, and which V1 tables (audit §2.3) are their ancestors. "Semantics reused, schema redesigned" is the default — V2 is a new database (ADR-0005).

## Modules ↔ entities

| Module | Entities |
|---|---|
| `identity` | User (one identity), UserProfile, UserPreferences, Session/Token |
| `academia` | University, Faculty, Department, AcademicSession, Semester, Course, Topic, Enrollment, Material, MaterialChunk, Question, Quiz/Exam, Attempt, Answer |
| `skills` | Skill, SkillCategory, LearningPath(+Step), Course/Lesson, Challenge, Project, ProjectTemplate, SkillTranscript, Progress |
| `verification` | VerificationRecord, Assessment, PracticalTask, VerificationEvent |
| `matching` | Opportunity, Requirement, SkillGap, MatchResult |
| `work` | Cohort, CohortMember, Assignment, Submission, WorkStatus |
| `quality` | QualityReview, QualityStandard, QualityRecord |
| `ledger` | LedgerEntry(+Postings), ProjectValue, StudentPayout, PlatformFee, DepartmentShare, Payout, ReconciliationRun |
| `notifications` | Notification, PushToken, MessageThread/Message |
| `admin` | AdminUser/Role, AuditLog, FeatureFlag |

## Entities and their V1 ancestors

| PRD / target entity | Purpose | V1 table(s) today | Verdict |
|---|---|---|---|
| **Identity** | One student across Academia + Skills (PRD §14) | `User`, `UserPreferences`, `StudentPrivacySettings` | Reuse semantics; `User` already has `google_sub`, `preferred_path`, `is_deleted`. |
| **Academic context** | University→Faculty→Dept→Level→Semester→Courses (PRD §3) | `University`, `Faculty`, `Department`, `AcademicSession`, `Semester`, `Course`, `Topic`, `Enrollment` | **Present** (added in migration `b3f7a91c4e28`); carry as-is. |
| **Material + RAG** | Study materials, grounded Q&A (PRD §3) | `Material`, `MaterialView`, `MaterialChunk` (pgvector) | Reuse; `MaterialChunk` is the RAG store. |
| **Learn / Practice** | Skills learning path + lessons + quizzes | `Skill`, `SkillCategory`, `LearningPath`, `LearningPathStep`, `SkillCourse`, `Lesson`, `Quiz`, `StudentQuizAttempt`, `StudentLessonProgress`, `StudentSkill` | Reuse semantics. |
| **Build** | Challenges + projects | `Challenge`, `ChallengeSubmission`, `ProjectTemplate`, `StudentProject`, `ProjectMilestone`, `ProjectFile`, `ProjectMessage` | Reuse semantics (workspace/project model is valuable). |
| **Skill Transcript** | Evidence of what a student can do (PRD §10) | composed of `StudentSkill` + `StudentProject` + verification records | **New entity**; assembled from evidence, not stored as claims. |
| **Verification record** | Earned proof, alive, decays on poor quality (PRD §5) | `StudentSkill` (partial), `GradingEvent`, `ChallengeSubmission` | **Redesign** — needs `VerificationRecord` + `VerificationEvent` history. |
| **Assessment / PracticalTask** | The evidence sources that grant verification (PRD §5) | `Quiz`/`CBTQuestion` (Academia), `Challenge` (Skills) | **Redesign** into first-class verification inputs. |
| **Opportunity** | Managed (fee applies) vs external (no 10%) (PRD §11) | `Opportunity`, `OpportunityApplication`, `OpportunityStatusEvent` | Reuse; **add `type` (managed/external)** — critical for the fee rule. |
| **Requirement → SkillGap → eligibility** | Why you qualify / what you're missing (PRD §6) | `Opportunity` requirements (sketch) | **New**: `Requirement`, `SkillGap`, `MatchResult`. |
| **Cohort** | Group of verified students on a managed project (PRD §8) | `Cohort`, `CohortEnrollment` | Reuse. |
| **Assignment / Submission / WorkStatus** | Distribute + track work (PRD §8) | `Assignment`, `AssignmentSubmission` (partial) | **Redesign** around managed projects. |
| **QualityReview / QualityRecord** | First-class quality stage (PRD §7) | `ChallengeSubmission` feedback, `Rating`, `GradingEvent` | **New**: quality is a workflow, not a flag. |
| **LedgerEntry / Payout / DepartmentShare** | Money, 90/10/2 split (PRD §12, ADR-0008) | `Opportunity` earnings sketch (`OpportunityApplication`) | **New** — the earnings ledger is build-first. |
| **ProjectValue + statuses** | value, student payout, fee, dept share, work/quality/payment status (PRD §12) | none | **New** — must exist on every managed project. |
| **Notification / PushToken** | Async updates | `Notification` | Reuse; add push tokens (ADR-0006). |
| **Messaging** | Work coordination | `MessageThread`, `Message` | Reuse (work-scoped only). |
| **Admin / AuditLog / FeatureFlag** | Internal ops, traceability | `User.is_admin`, `AdminAuditLog` | Reuse; add roles + flags. |
| Community, live classes, reels, employer profiles | **Not in V2** (PRD §2, §14) | `Group*`, `Room`, `Video`, `EmployerProfile` | **Drop from V2**; V1 keeps them until V1 is retired. |

## Key relationships

```
Identity ──1:1── UserProfile
Identity ──*── Enrollment ──*── Course ──*── Topic ──*── Material ──*── MaterialChunk
Identity ──*── SkillProgress ──*── Skill
Identity ──*── VerificationRecord ──*── VerificationEvent        (evidence: Assessment | PracticalTask | QualityRecord)
Opportunity ──(type: managed|external)──*── Requirement ── Skill ──> SkillGap (per identity)
Opportunity ──*── Cohort ──*── CohortMember ──*── Assignment ──*── Submission
Submission ──1:1── QualityReview ──> QualityRecord ──> (feeds VerificationRecord)
ManagedProject ──1:1── ProjectValue {value, student_payout, platform_fee, department_share,
                                     work_status, quality_status, payment_status}
ManagedProject ──*── LedgerEntry (append-only, balanced postings)
DepartmentShare ──*── LedgerEntry      (paid from the FEE, never the student's 90%)
```

## Non-negotiables encoded in this map
- **90 / 10 / 2** split with the department share taken **from the fee**, so `student_payout = 0.90 × value` **exactly**, regardless of the fee.
- **Verification never comes from watching lessons** (PRD §5) — it is granted only by `Assessment` / `PracticalTask` / `QualityRecord` events.
- **External opportunities carry no default fee** (PRD §11) — `Opportunity.type` gates the money flow.
