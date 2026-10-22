import Constants from 'expo-constants';
import * as React from 'react';
import { Linking, Text } from 'react-native';

import { ApiError, login, verifyMfa } from '../lib/api';
import { Body, Button, Card, ErrorText, Field, Muted, Screen, styles } from '../ui';

const webBase = ((Constants.expoConfig?.extra ?? {}) as Record<string, string>).webBaseUrl ?? 'https://nelavista.com';

export function Auth({ onSignedIn }: { onSignedIn: () => void }): JSX.Element {
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [challenge, setChallenge] = React.useState<string | null>(null);
  const [code, setCode] = React.useState('');
  const [error, setError] = React.useState<string | null>(null);
  const [busy, setBusy] = React.useState(false);

  async function submit(): Promise<void> {
    setBusy(true);
    setError(null);
    try {
      if (challenge) {
        await verifyMfa(challenge, code.trim());
      } else {
        await login(email.trim().toLowerCase(), password);
      }
      onSignedIn();
    } catch (err) {
      if (err instanceof ApiError && err.code === 'mfa_required') {
        const details = err.details as { mfa_token?: string } | undefined;
        if (details?.mfa_token) {
          setChallenge(details.mfa_token);
          setError(null);
          return;
        }
      }
      setError(err instanceof ApiError ? err.message : 'Could not sign you in.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <Screen title="Nelavista">
      <Card>
        <Text style={styles.h2}>{challenge ? 'Enter your code' : 'Sign in'}</Text>
        <Muted>
          {challenge
            ? 'Your account has two-factor authentication. Enter the code from your authenticator app.'
            : 'Your learning, proof and earnings, on this device.'}
        </Muted>
        {challenge ? (
          <Field
            autoComplete="one-time-code"
            keyboardType="number-pad"
            label="Code"
            maxLength={20}
            onChangeText={setCode}
            value={code}
          />
        ) : (
          <>
            <Field
              autoCapitalize="none"
              autoComplete="email"
              keyboardType="email-address"
              label="Email"
              onChangeText={setEmail}
              value={email}
            />
            <Field
              autoComplete="current-password"
              label="Password"
              onChangeText={setPassword}
              secureTextEntry
              value={password}
            />
          </>
        )}
        <ErrorText message={error} />
        <Button
          disabled={busy || (challenge ? code.trim().length < 6 : !email.includes('@') || password.length === 0)}
          label={busy ? 'Signing in…' : challenge ? 'Verify and sign in' : 'Sign in'}
          onPress={() => void submit()}
        />
      </Card>

      <Card>
        <Body>Need an account or a password reset?</Body>
        <Muted>
          Account creation and recovery finish on the web, then this app signs in with the same account.
        </Muted>
        <Button label="Open nelavista.com" onPress={() => void Linking.openURL(`${webBase}/login`)} tone="ghost" />
        <Button label="Reset my password" onPress={() => void Linking.openURL(`${webBase}/auth/reset`)} tone="ghost" />
      </Card>
    </Screen>
  );
}
