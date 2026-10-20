import * as React from 'react';
import { Navigate, Route, Routes, useLocation } from 'react-router-dom';

import { Layout } from './components/Layout';
import { SessionProvider, useSession } from './lib/session';
import { Landing } from './routes/Landing';
import { Login } from './routes/Login';
import { Signup } from './routes/Signup';

// Signed-in screens are split out of the first load (B12). Landing, sign-in and
// sign-up stay eager: they are the entry point and must paint without a second
// round trip.
const Home = React.lazy(() => import('./routes/Home').then((m) => ({ default: m.Home })));
const Onboarding = React.lazy(() => import('./routes/Onboarding').then((m) => ({ default: m.Onboarding })));
const AcademiaDashboard = React.lazy(() =>
  import('./routes/AcademiaDashboard').then((m) => ({ default: m.AcademiaDashboard })),
);
const Campus = React.lazy(() => import('./routes/Campus').then((m) => ({ default: m.Campus })));
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
const VerifyEmail = React.lazy(() =>
  import('./routes/VerifyEmail').then((m) => ({ default: m.VerifyEmail })),
);
const ResetPassword = React.lazy(() =>
  import('./routes/ResetPassword').then((m) => ({ default: m.ResetPassword })),
);

function Loading(): JSX.Element {
  return (
    <div className="nv-card nv-card--narrow">
      <p className="nv-muted" role="status">
        Loading…
      </p>
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

function RouteTable(): JSX.Element {
  return (
    <Layout>
      <React.Suspense fallback={<Loading />}>
        <Routes>
          <Route path="/" element={<Landing />} />
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
              <RequireAuth>
                <Home />
              </RequireAuth>
            }
          />
          <Route
            path="/academia"
            element={
              <RequireAuth>
                <AcademiaDashboard />
              </RequireAuth>
            }
          />
          <Route
            path="/campus"
            element={
              <RequireAuth>
                <Campus />
              </RequireAuth>
            }
          />
          <Route
            path="/verification"
            element={
              <RequireAuth>
                <Verification />
              </RequireAuth>
            }
          />
          <Route
            path="/verification/assessments/:assessmentSlug"
            element={
              <RequireAuth>
                <AssessmentSitting />
              </RequireAuth>
            }
          />
          <Route
            path="/verification/attempts/:attemptId"
            element={
              <RequireAuth>
                <AttemptReview />
              </RequireAuth>
            }
          />
          <Route
            path="/verification/practical/:taskSlug"
            element={
              <RequireAuth>
                <PracticalTask />
              </RequireAuth>
            }
          />
          <Route
            path="/transcript"
            element={
              <RequireAuth>
                <Transcript />
              </RequireAuth>
            }
          />
          <Route
            path="/opportunities"
            element={
              <RequireAuth>
                <Opportunities />
              </RequireAuth>
            }
          />
          <Route
            path="/opportunities/:slug"
            element={
              <RequireAuth>
                <OpportunityDetail />
              </RequireAuth>
            }
          />
          <Route
            path="/work"
            element={
              <RequireAuth>
                <Work />
              </RequireAuth>
            }
          />
          <Route
            path="/work/assignments/:assignmentId"
            element={
              <RequireAuth>
                <AssignmentDetail />
              </RequireAuth>
            }
          />
          <Route
            path="/earnings"
            element={
              <RequireAuth>
                <Earnings />
              </RequireAuth>
            }
          />
          <Route
            path="/settings"
            element={
              <RequireAuth>
                <Settings />
              </RequireAuth>
            }
          />
          <Route
            path="/skills"
            element={
              <RequireAuth>
                <Skills />
              </RequireAuth>
            }
          />
          {/* Static segments rank above the parameter, so this route wins. */}
          <Route
            path="/skills/my-learning"
            element={
              <RequireAuth>
                <MyLearning />
              </RequireAuth>
            }
          />
          <Route
            path="/skills/paths/:pathSlug"
            element={
              <RequireAuth>
                <PathDetail />
              </RequireAuth>
            }
          />
          <Route
            path="/skills/lessons/:lessonSlug"
            element={
              <RequireAuth>
                <LessonReader />
              </RequireAuth>
            }
          />
          <Route
            path="/skills/practice/:templateId"
            element={
              <RequireAuth>
                <Practice />
              </RequireAuth>
            }
          />
          <Route
            path="/skills/:skillSlug"
            element={
              <RequireAuth>
                <SkillDetail />
              </RequireAuth>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </React.Suspense>
    </Layout>
  );
}

export function App(): JSX.Element {
  return (
    <SessionProvider>
      <RouteTable />
    </SessionProvider>
  );
}
