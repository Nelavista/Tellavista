import type { MeOut, OnboardingStateOut } from '@nelavista/api-client';
import * as React from 'react';
import { Text, View } from 'react-native';

import type { Route } from '../lib/deepLink';
import { useApi } from '../lib/useApi';
import { Body, Button, Card, ErrorText, H2, Loading, Muted, Row, Screen, styles } from '../ui';

export function Home({ me, navigate }: { me: MeOut; navigate: (route: Route) => void }): JSX.Element {
  const state = useApi<OnboardingStateOut>('/onboarding/state');

  return (
    <Screen title={`Hello, ${me.name ?? me.username}`}>
      {me.email_verified ? null : (
        <Card>
          <H2>Confirm your email</H2>
          <Muted>
            Proof and payout notices go to {me.email}. Open the link we sent, or ask for a new one on the
            web home screen.
          </Muted>
        </Card>
      )}

      {state.remote.status === 'loading' ? <Loading /> : null}
      {state.remote.status === 'error' ? <ErrorText message={state.remote.message} /> : null}
      {state.remote.status === 'ready' ? (
        <Card>
          <H2>Where you are</H2>
          {state.remote.data.has_enrolment ? (
            state.remote.data.enrolments.map((row) => (
              <Body key={row.enrolment_id}>
                {row.code} — {row.title}
              </Body>
            ))
          ) : (
            <Muted>No course enrolled yet. Finish setup on the web, then come back here.</Muted>
          )}
          {state.remote.data.current_semester ? (
            <Muted>{state.remote.data.current_semester.name}</Muted>
          ) : null}
          <Muted>
            Next step:{' '}
            {state.remote.data.next_step === 'enrol'
              ? 'choose your courses'
              : state.remote.data.next_step === 'choose_path'
                ? 'choose a path'
                : 'nothing blocking you'}
          </Muted>
        </Card>
      ) : null}

      <Card>
        <H2>Go to</H2>
        <Row>
          <Button label="Skills" onPress={() => navigate({ name: 'skills' })} />
          <Button label="Verification" onPress={() => navigate({ name: 'verification' })} tone="ghost" />
          <Button label="Opportunities" onPress={() => navigate({ name: 'opportunities' })} tone="ghost" />
        </Row>
        <Row>
          <Button label="Work" onPress={() => navigate({ name: 'work' })} tone="ghost" />
          <Button label="Earnings" onPress={() => navigate({ name: 'earnings' })} tone="ghost" />
          <Button label="Transcript" onPress={() => navigate({ name: 'transcript' })} tone="ghost" />
        </Row>
        <Row>
          <Button label="Notifications" onPress={() => navigate({ name: 'notifications' })} tone="ghost" />
          <Button label="Settings" onPress={() => navigate({ name: 'settings' })} tone="ghost" />
        </Row>
      </Card>

      <View>
        <Text style={styles.muted}>
          Lessons and practice are progress. Only a passed assessment or a reviewed practical task is proof.
        </Text>
      </View>
    </Screen>
  );
}
