import Constants from 'expo-constants';
import { StatusBar } from 'expo-status-bar';
import * as React from 'react';
import { StyleSheet, Text, View } from 'react-native';

import { colors, spacing } from '@nelavista/design-tokens';

/**
 * Hello-world. Proves: the tokens/config packages resolve, the API base URL comes
 * from the build profile (never hardcoded), and the environment is visible so a
 * tester can tell a DEV build from PROD.
 *
 * The version switcher lives on web/admin (a native app has one version installed);
 * native force-update is handled by the API's 426 contract (ADR-0010).
 */
export default function App(): JSX.Element {
  const extra = (Constants.expoConfig?.extra ?? {}) as Record<string, string>;
  const [health, setHealth] = React.useState('…');

  React.useEffect(() => {
    const url = `${extra.apiBaseUrl}/${extra.apiVersion}/health`;
    fetch(url)
      .then((r) => r.json())
      .then((d) => setHealth(d.status))
      .catch(() => setHealth('unreachable'));
  }, [extra.apiBaseUrl, extra.apiVersion]);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Nelavista</Text>
      <Text style={styles.line}>env: {extra.appVariant}</Text>
      <Text style={styles.line}>api: {extra.apiBaseUrl}</Text>
      <Text style={styles.line}>health: {health}</Text>
      <StatusBar style="light" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.bg,
    alignItems: 'center',
    justifyContent: 'center',
    padding: spacing.xl,
  },
  title: { color: colors.text, fontSize: 28, fontWeight: '700', marginBottom: spacing.md },
  line: { color: colors.textMuted, fontSize: 14 },
});
