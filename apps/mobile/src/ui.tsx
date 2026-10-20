/** Small native primitives, using the shared design tokens. */
import { colors, spacing } from '@nelavista/design-tokens';
import * as React from 'react';
import {
  ActivityIndicator,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';

export function Screen({
  title,
  children,
  onBack,
  right,
}: {
  title: string;
  children: React.ReactNode;
  onBack?: () => void;
  right?: React.ReactNode;
}): JSX.Element {
  return (
    <View style={styles.screen}>
      <View style={styles.header}>
        <View style={styles.headerLeft}>
          {onBack ? (
            <Pressable accessibilityLabel="Go back" onPress={onBack} style={styles.back}>
              <Text style={styles.backText}>‹</Text>
            </Pressable>
          ) : null}
          <Text style={styles.title}>{title}</Text>
        </View>
        {right}
      </View>
      <ScrollView contentContainerStyle={styles.content}>{children}</ScrollView>
    </View>
  );
}

export function Card({ children }: { children: React.ReactNode }): JSX.Element {
  return <View style={styles.card}>{children}</View>;
}

export function H2({ children }: { children: React.ReactNode }): JSX.Element {
  return <Text style={styles.h2}>{children}</Text>;
}

export function Body({ children }: { children: React.ReactNode }): JSX.Element {
  return <Text style={styles.body}>{children}</Text>;
}

export function Muted({ children }: { children: React.ReactNode }): JSX.Element {
  return <Text style={styles.muted}>{children}</Text>;
}

export function Button({
  label,
  onPress,
  disabled,
  tone = 'primary',
}: {
  label: string;
  onPress: () => void;
  disabled?: boolean;
  tone?: 'primary' | 'ghost' | 'danger';
}): JSX.Element {
  return (
    <Pressable
      accessibilityRole="button"
      disabled={disabled}
      onPress={onPress}
      style={[
        styles.button,
        tone === 'ghost' ? styles.buttonGhost : null,
        tone === 'danger' ? styles.buttonDanger : null,
        disabled ? styles.buttonDisabled : null,
      ]}
    >
      <Text style={[styles.buttonText, tone === 'ghost' ? styles.buttonTextGhost : null]}>{label}</Text>
    </Pressable>
  );
}

export function Field({
  label,
  ...props
}: React.ComponentProps<typeof TextInput> & { label: string }): JSX.Element {
  return (
    <View style={styles.field}>
      <Text style={styles.label}>{label}</Text>
      <TextInput
        placeholderTextColor={colors.textMuted}
        style={styles.input}
        {...props}
      />
    </View>
  );
}

export function Row({ children }: { children: React.ReactNode }): JSX.Element {
  return <View style={styles.row}>{children}</View>;
}

export function Badge({ label, tone = 'muted' }: { label: string; tone?: 'ok' | 'warn' | 'bad' | 'muted' }): JSX.Element {
  return (
    <Text
      style={[
        styles.badge,
        tone === 'ok' ? styles.badgeOk : tone === 'warn' ? styles.badgeWarn : tone === 'bad' ? styles.badgeBad : null,
      ]}
    >
      {label}
    </Text>
  );
}

export function Loading(): JSX.Element {
  return (
    <View style={styles.loading}>
      <ActivityIndicator color={colors.accent} />
      <Text style={styles.muted}>Loading…</Text>
    </View>
  );
}

export function ErrorText({ message }: { message: string | null }): JSX.Element | null {
  if (!message) return null;
  return <Text style={styles.error}>{message}</Text>;
}

export function Note({ message }: { message: string | null }): JSX.Element | null {
  if (!message) return null;
  return <Text style={styles.note}>{message}</Text>;
}

export const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg },
  header: {
    paddingTop: spacing.xl,
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing.md,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: colors.border,
  },
  headerLeft: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  back: { paddingRight: spacing.sm },
  backText: { color: colors.text, fontSize: 28, lineHeight: 30 },
  title: { color: colors.text, fontSize: 20, fontWeight: '700' },
  content: { padding: spacing.lg, gap: spacing.md, paddingBottom: spacing.xl * 2 },
  card: {
    backgroundColor: colors.surface,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: 14,
    padding: spacing.lg,
    gap: spacing.sm,
  },
  h2: { color: colors.text, fontSize: 16, fontWeight: '600' },
  body: { color: colors.text, fontSize: 14, lineHeight: 20 },
  muted: { color: colors.textMuted, fontSize: 13, lineHeight: 18 },
  label: { color: colors.textMuted, fontSize: 12, marginBottom: 4 },
  field: { gap: 2 },
  input: {
    backgroundColor: colors.bg,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: 10,
    color: colors.text,
    paddingHorizontal: 12,
    paddingVertical: 10,
  },
  button: {
    backgroundColor: colors.accent,
    borderRadius: 10,
    paddingVertical: 12,
    paddingHorizontal: 16,
    alignItems: 'center',
  },
  buttonGhost: { backgroundColor: 'transparent', borderColor: colors.border, borderWidth: 1 },
  buttonDanger: { backgroundColor: '#b91c1c' },
  buttonDisabled: { opacity: 0.5 },
  buttonText: { color: '#04121c', fontWeight: '700' },
  buttonTextGhost: { color: colors.text },
  row: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, alignItems: 'center' },
  badge: {
    color: colors.textMuted,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: 999,
    paddingHorizontal: 8,
    paddingVertical: 1,
    fontSize: 12,
    overflow: 'hidden',
  },
  badgeOk: { color: '#4ade80', borderColor: '#4ade80' },
  badgeWarn: { color: '#fbbf24', borderColor: '#fbbf24' },
  badgeBad: { color: '#f87171', borderColor: '#f87171' },
  loading: { alignItems: 'center', gap: spacing.sm, padding: spacing.xl },
  error: { color: '#f87171', fontSize: 13 },
  note: { color: '#7dd3fc', fontSize: 13 },
});
