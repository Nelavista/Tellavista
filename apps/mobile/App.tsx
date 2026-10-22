import type { MeOut } from '@nelavista/api-client';
import { StatusBar } from 'expo-status-bar';
import * as React from 'react';
import { AppState, Linking } from 'react-native';

import { UpgradeRequired, api, hydrateSession, refresh, setUpgradeHandler } from './src/lib/api';
import { parseDeepLink, type Route } from './src/lib/deepLink';
import { registerForPush } from './src/lib/notifications';
import { flushQueue } from './src/lib/sync';
import { AcademiaHome, AskScreen, CbtScreen, MaterialsScreen, MaterialScreen } from './src/screens/Academia';
import { Auth } from './src/screens/Auth';
import { Home } from './src/screens/Home';
import { LessonScreen, PathScreen, PracticeScreen, SkillDetail, Skills } from './src/screens/Learning';
import { Earnings } from './src/screens/Money';
import { Opportunities, OpportunityScreen } from './src/screens/Opportunities';
import { AssessmentScreen, Transcript, Verification } from './src/screens/Proof';
import { Notifications, Settings } from './src/screens/Settings';
import { TalentScreen } from './src/screens/Talent';
import { AssignmentScreen, Work } from './src/screens/Work';
import { Button, Card, H2, Loading, Muted, Screen } from './src/ui';

function UpgradeScreen({ error }: { error: UpgradeRequired }): JSX.Element {
  return (
    <Screen title="Update required">
      <Card>
        <H2>This version is no longer supported</H2>
        <Muted>
          Update Nelavista to keep your learning, proof and earnings in sync.
          {error.minVersion ? ` Minimum version: ${error.minVersion}.` : ''}
        </Muted>
        {error.storeUrl ? (
          <Button label="Open the store" onPress={() => void Linking.openURL(error.storeUrl as string)} />
        ) : null}
      </Card>
    </Screen>
  );
}

function SignedIn({
  me,
  onSignedOut,
}: {
  me: MeOut;
  onSignedOut: () => void;
}): JSX.Element {
  const [stack, setStack] = React.useState<Route[]>([{ name: 'home' }]);
  const route = stack[stack.length - 1] ?? { name: 'home' };

  const navigate = React.useCallback((next: Route) => {
    setStack((current) => (next.name === 'home' ? [next] : [...current, next]));
  }, []);
  // Universal links and `nelavista://` both arrive here.
  React.useEffect(() => {
    const handle = (url: string | null): void => {
      const next = url ? parseDeepLink(url) : null;
      if (next) navigate(next);
    };
    void Linking.getInitialURL().then(handle);
    const subscription = Linking.addEventListener('url', (event) => handle(event.url));
    return () => subscription.remove();
  }, [navigate]);

  // Retry queued work when the app comes back to the foreground.
  React.useEffect(() => {
    const subscription = AppState.addEventListener('change', (state) => {
      if (state === 'active') void flushQueue();
    });
    void flushQueue();
    return () => subscription.remove();
  }, []);

  React.useEffect(() => {
    void registerForPush();
  }, []);

  switch (route.name) {
    case 'skills':
      return <Skills navigate={navigate} />;
    case 'skill':
      return <SkillDetail slug={route.slug} navigate={navigate} />;
    case 'path':
      return <PathScreen slug={route.slug} navigate={navigate} />;
    case 'lesson':
      return <LessonScreen slug={route.slug} navigate={navigate} />;
    case 'practice':
      return <PracticeScreen templateId={route.id} navigate={navigate} />;
    case 'verification':
      return <Verification navigate={navigate} />;
    case 'assessment':
      return <AssessmentScreen slug={route.slug} navigate={navigate} />;
    case 'transcript':
      return <Transcript navigate={navigate} />;
    case 'academia':
      return <AcademiaHome navigate={navigate} />;
    case 'materials':
      return <MaterialsScreen navigate={navigate} />;
    case 'material':
      return <MaterialScreen id={route.id} navigate={navigate} />;
    case 'ask':
      return <AskScreen navigate={navigate} />;
    case 'cbt':
      return <CbtScreen navigate={navigate} />;
    case 'talent':
      return <TalentScreen navigate={navigate} />;
    case 'opportunities':
      return <Opportunities navigate={navigate} />;
    case 'opportunity':
      return <OpportunityScreen slug={route.slug} navigate={navigate} />;
    case 'work':
      return <Work navigate={navigate} />;
    case 'assignment':
      return <AssignmentScreen id={route.id} navigate={navigate} />;
    case 'earnings':
      return <Earnings navigate={navigate} />;
    case 'notifications':
      return <Notifications navigate={navigate} />;
    case 'settings':
      return <Settings me={me} navigate={navigate} onSignedOut={onSignedOut} />;
    default:
      return <Home me={me} navigate={navigate} />;
  }
}

export default function App(): JSX.Element {
  const [booting, setBooting] = React.useState(true);
  const [me, setMe] = React.useState<MeOut | null>(null);
  const [upgrade, setUpgrade] = React.useState<UpgradeRequired | null>(null);

  React.useEffect(() => {
    setUpgradeHandler(setUpgrade);
    return () => setUpgradeHandler(null);
  }, []);

  const loadMe = React.useCallback(async (): Promise<void> => {
    try {
      setMe(await api.get<MeOut>('/auth/me'));
    } catch (err) {
      if (err instanceof UpgradeRequired) return;
      setMe(null);
    }
  }, []);

  React.useEffect(() => {
    void (async () => {
      try {
        const hasToken = await hydrateSession();
        if (hasToken && (await refresh())) await loadMe();
      } catch {
        // A stale refresh token is not an error the student needs to see.
      } finally {
        setBooting(false);
      }
    })();
  }, [loadMe]);

  if (upgrade) return <UpgradeScreen error={upgrade} />;
  if (booting) {
    return (
      <Screen title="Nelavista">
        <Loading />
      </Screen>
    );
  }

  if (!me) {
    return (
      <>
        <Auth onSignedIn={() => void loadMe()} />
        <StatusBar style="light" />
      </>
    );
  }

  return (
    <>
      <SignedIn me={me} onSignedOut={() => setMe(null)} />
      <StatusBar style="light" />
    </>
  );
}
