import * as React from 'react';
import { Navigate, Route, Routes, useLocation } from 'react-router-dom';

import { AppShell } from './components/AppShell';
import { ErrorBoundary } from './components/ErrorBoundary';
import { PublicLayout } from './components/PublicLayout';
import { SessionProvider, useSession } from './lib/session';
import { ThemeProvider } from './lib/theme-context';
import { Landing } from './routes/Landing';
import { Login } from './routes/Login';
import { Signup } from './routes/Signup';
import { NotFound } from './routes/NotFound';
import { Offline } from './routes/Offline';

const Home = React.lazy(() => import('./routes/Home').then((m) => ({ default: m.Home })));
const Onboarding = React.lazy(() => import('./routes/Onboarding').then((m) => ({ default: m.Onboarding })));
const AcademiaDashboard = React.lazy(() =>
  import('./routes/AcademiaDashboard').then((m) => ({ default: m.AcademiaDashboard })),
);
const Campus = React.lazy(() => import('./routes/Campus').then((m) => ({ default: m.Campus })));
const Materials = React.lazy(() =>
  import('./routes/AcademiaMaterials').then((m) => ({ default: m.Materials })),
);
const MaterialReader = React.lazy(() =>
  import('./routes/AcademiaMaterials').then((m) => ({ default: m.MaterialReader })),
);
const AskNelavista = React.lazy(() =>
  import('./routes/AskNelavista').then((m) => ({ default: m.AskNelavista })),
);
const Cbt = React.lazy(() => import('./routes/Cbt').then((m) => ({ default: m.Cbt })));
const Skills = React.lazy(() => import('./routes/Skills').then((m) => ({ default: m.Skills })));
const SkillDetail = React.lazy(() =>
  import('./routes/SkillDetail').then((m) => ({ default: m.SkillDetail })),
);
const PathDetail = React.lazy(() => import('./routes/PathDetail').then((m) => ({ default: m.PathDetail })));
const LessonReader = React.lazy(() =>
  import('./routes/LessonReader').then((m) => ({ default: m.LessonReader })),
);
const Practice = React.lazy(() => import('./routes/Practice').then((m) => ({ default: m.Practice })));
const MyLearning = React.lazy(() => import('./routes/MyLearning').then((m) => ({ default: m.MyLearning })));
const Verification = React.lazy(() =>
  import('./routes/Verification').then((m) => ({ default: m.Verification })),
);
const AssessmentSitting = React.lazy(() =>
  import('./routes/AssessmentSitting').then((m) => ({ default: m.AssessmentSitting })),
);
const AttemptReview = React.lazy(() =>
  import('./routes/AttemptReview').then((m) => ({ default: m.AttemptReview })),
);
const Transcript = React.lazy(() => import('./routes/Transcript').then((m) => ({ default: m.Transcript })));
const PracticalTask = React.lazy(() =>
  import('./routes/PracticalTask').then((m) => ({ default: m.PracticalTask })),
);
const Opportunities = React.lazy(() =>
  import('./routes/Opportunities').then((m) => ({ default: m.Opportunities })),
);
const OpportunityDetail = React.lazy(() =>
  import('./routes/OpportunityDetail').then((m) => ({ default: m.OpportunityDetail })),
);
const Work = React.lazy(() => import('./routes/Work').then((m) => ({ default: m.Work })));
const AssignmentDetail = React.lazy(() =>
  import('./routes/AssignmentDetail').then((m) => ({ default: m.AssignmentDetail })),
);
const Earnings = React.lazy(() => import('./routes/Earnings').then((m) => ({ default: m.Earnings })));
const Settings = React.lazy(() => import('./routes/Settings').then((m) => ({ default: m.Settings })));
const Talent = React.lazy(() => import('./routes/Talent').then((m) => ({ default: m.Talent })));
const SharedProfile = React.lazy(() =>
  import('./routes/SharedProfile').then((m) => ({ default: m.SharedProfile })),
);
const VerifyEmail = React.lazy(() =>
  import('./routes/VerifyEmail').then((m) => ({ default: m.VerifyEmail })),
);
const ResetPassword = React.lazy(() =>
  import('./routes/ResetPassword').then((m) => ({ default: m.ResetPassword })),
);

const Features = React.lazy(() => import('./routes/Features').then((m) => ({ default: m.Features })));
const HowItWorks = React.lazy(() => import('./routes/HowItWorks').then((m) => ({ default: m.HowItWorks })));
const About = React.lazy(() => import('./routes/About').then((m) => ({ default: m.About })));
const Contact = React.lazy(() => import('./routes/Contact').then((m) => ({ default: m.Contact })));
const Faq = React.lazy(() => import('./routes/Faq').then((m) => ({ default: m.Faq })));
const Privacy = React.lazy(() => import('./routes/Legal').then((m) => ({ default: m.Privacy })));
const Terms = React.lazy(() => import('./routes/Legal').then((m) => ({ default: m.Terms })));
const ContributorTerms = React.lazy(() =>
  import('./routes/Legal').then((m) => ({ default: m.ContributorTerms })),
);
const Notifications = React.lazy(() =>
  import('./routes/Notifications').then((m) => ({ default: m.Notifications })),
);
const Applications = React.lazy(() =>
  import('./routes/Applications').then((m) => ({ default: m.Applications })),
);
const CbtHistory = React.lazy(() => import('./routes/CbtHistory').then((m) => ({ default: m.CbtHistory })));
const Course = React.lazy(() => import('./routes/Course').then((m) => ({ default: m.Course })));

function Loading(): JSX.Element {
  return (
    <div className="nv-container nv-section" aria-busy="true">
      <div className="nv-skeleton-group">
        <span className="nv-skeleton" style={{ width: '38%', height: '2.5rem' }} />
        <span className="nv-skeleton" style={{ width: '70%' }} />
        <span className="nv-skeleton" style={{ width: '55%' }} />
      </div>
    </div>
  );
}

/** Guards the signed-in area; keeps the attempted URL so login can return to it. */
function RequireAuth({ children }: { children: React.ReactNode }): JSX.Element {
  const { status } = useSession();
  const location = useLocation();
  if (status === 'loading') return <Loading />;
  if (status === 'anonymous') {
    return <Navigate to="/login" replace state={{ from: `${location.pathname}${location.search}` }} />;
  }
  return <>{children}</>;
}

/** Signed-in users never need the auth screens. */
function PublicOnly({ children }: { children: React.ReactNode }): JSX.Element {
  const { status } = useSession();
  if (status === 'loading') return <Loading />;
  if (status === 'authenticated') return <Navigate to="/home" replace />;
  return <>{children}</>;
}

function Protected({ children }: { children: React.ReactNode }): JSX.Element {
  return (
    <RequireAuth>
      <AppShell>{children}</AppShell>
    </RequireAuth>
  );
}

function Public({ children }: { children: React.ReactNode }): JSX.Element {
  return <PublicLayout>{children}</PublicLayout>;
}

function NotFoundRoute(): JSX.Element {
  const { status } = useSession();
  return status === 'authenticated' ? (
    <AppShell>
      <NotFound />
    </AppShell>
  ) : (
    <PublicLayout>
      <NotFound />
    </PublicLayout>
  );
}

function RouteTable(): JSX.Element {
  return (
    <React.Suspense fallback={<Loading />}>
      <Routes>
        <Route
          path="/"
          element={
            <PublicOnly>
              <PublicLayout>
                <Landing />
              </PublicLayout>
            </PublicOnly>
          }
        />
        <Route
          path="/features"
          element={
            <Public>
              <Features />
            </Public>
          }
        />
        <Route
          path="/how-it-works"
          element={
            <Public>
              <HowItWorks />
            </Public>
          }
        />
        <Route
          path="/about"
          element={
            <Public>
              <About />
            </Public>
          }
        />
        <Route
          path="/contact"
          element={
            <Public>
              <Contact />
            </Public>
          }
        />
        <Route
          path="/faq"
          element={
            <Public>
              <Faq />
            </Public>
          }
        />
        <Route
          path="/legal/privacy"
          element={
            <Public>
              <Privacy />
            </Public>
          }
        />
        <Route
          path="/legal/terms"
          element={
            <Public>
              <Terms />
            </Public>
          }
        />
        <Route
          path="/legal/contributor-terms"
          element={
            <Public>
              <ContributorTerms />
            </Public>
          }
        />
        <Route
          path="/offline"
          element={
            <Public>
              <Offline />
            </Public>
          }
        />

        <Route
          path="/signup"
          element={
            <PublicOnly>
              <Signup />
            </PublicOnly>
          }
        />
        <Route
          path="/login"
          element={
            <PublicOnly>
              <Login />
            </PublicOnly>
          }
        />
        <Route path="/auth/verify" element={<VerifyEmail />} />
        <Route path="/auth/reset" element={<ResetPassword />} />

        <Route
          path="/onboarding"
          element={
            <RequireAuth>
              <Onboarding />
            </RequireAuth>
          }
        />
        <Route
          path="/home"
          element={
            <Protected>
              <Home />
            </Protected>
          }
        />
        <Route
          path="/academia"
          element={
            <Protected>
              <AcademiaDashboard />
            </Protected>
          }
        />
        <Route
          path="/academia/materials"
          element={
            <Protected>
              <Materials />
            </Protected>
          }
        />
        <Route
          path="/academia/materials/:materialId"
          element={
            <Protected>
              <MaterialReader />
            </Protected>
          }
        />
        <Route
          path="/academia/ask"
          element={
            <Protected>
              <AskNelavista />
            </Protected>
          }
        />
        <Route
          path="/academia/cbt"
          element={
            <Protected>
              <Cbt />
            </Protected>
          }
        />
        <Route
          path="/academia/cbt/history"
          element={
            <Protected>
              <CbtHistory />
            </Protected>
          }
        />
        <Route
          path="/academia/courses/:courseCode"
          element={
            <Protected>
              <Course />
            </Protected>
          }
        />
        <Route
          path="/campus"
          element={
            <Protected>
              <Campus />
            </Protected>
          }
        />
        <Route
          path="/verification"
          element={
            <Protected>
              <Verification />
            </Protected>
          }
        />
        <Route
          path="/verification/assessments/:assessmentSlug"
          element={
            <Protected>
              <AssessmentSitting />
            </Protected>
          }
        />
        <Route
          path="/verification/attempts/:attemptId"
          element={
            <Protected>
              <AttemptReview />
            </Protected>
          }
        />
        <Route
          path="/verification/practical/:taskSlug"
          element={
            <Protected>
              <PracticalTask />
            </Protected>
          }
        />
        <Route
          path="/transcript"
          element={
            <Protected>
              <Transcript />
            </Protected>
          }
        />
        <Route
          path="/opportunities"
          element={
            <Protected>
              <Opportunities />
            </Protected>
          }
        />
        <Route
          path="/opportunities/applications"
          element={
            <Protected>
              <Applications />
            </Protected>
          }
        />
        <Route
          path="/opportunities/:slug"
          element={
            <Protected>
              <OpportunityDetail />
            </Protected>
          }
        />
        <Route
          path="/work"
          element={
            <Protected>
              <Work />
            </Protected>
          }
        />
        <Route
          path="/work/assignments/:assignmentId"
          element={
            <Protected>
              <AssignmentDetail />
            </Protected>
          }
        />
        <Route
          path="/earnings"
          element={
            <Protected>
              <Earnings />
            </Protected>
          }
        />
        <Route
          path="/notifications"
          element={
            <Protected>
              <Notifications />
            </Protected>
          }
        />
        <Route
          path="/settings"
          element={
            <Protected>
              <Settings />
            </Protected>
          }
        />
        <Route
          path="/settings/security"
          element={
            <Protected>
              <Settings />
            </Protected>
          }
        />
        <Route
          path="/settings/notifications"
          element={
            <Protected>
              <Settings />
            </Protected>
          }
        />
        <Route
          path="/settings/data"
          element={
            <Protected>
              <Settings />
            </Protected>
          }
        />
        <Route
          path="/talent"
          element={
            <Protected>
              <Talent />
            </Protected>
          }
        />
        <Route
          path="/skills"
          element={
            <Protected>
              <Skills />
            </Protected>
          }
        />
        <Route
          path="/skills/my-learning"
          element={
            <Protected>
              <MyLearning />
            </Protected>
          }
        />
        <Route
          path="/skills/paths/:pathSlug"
          element={
            <Protected>
              <PathDetail />
            </Protected>
          }
        />
        <Route
          path="/skills/lessons/:lessonSlug"
          element={
            <Protected>
              <LessonReader />
            </Protected>
          }
        />
        <Route
          path="/skills/practice/:templateId"
          element={
            <Protected>
              <Practice />
            </Protected>
          }
        />
        <Route
          path="/skills/:skillSlug"
          element={
            <Protected>
              <SkillDetail />
            </Protected>
          }
        />

        {/* Public by design: the token in the URL is the grant (B13). */}
        <Route path="/share/:token" element={<SharedProfile />} />

        <Route path="*" element={<NotFoundRoute />} />
      </Routes>
    </React.Suspense>
  );
}

export function App(): JSX.Element {
  return (
    <ErrorBoundary>
      <ThemeProvider>
        <SessionProvider>
          <RouteTable />
        </SessionProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}
