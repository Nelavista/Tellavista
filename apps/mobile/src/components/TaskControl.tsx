import * as React from 'react';
import { Pressable, Text, TextInput, View } from 'react-native';

import type { Control } from '../lib/taskForm';
import { Body, Button, Muted, Row, styles } from '../ui';

export type TaskValue = string | string[] | number | null;

export function TaskControl({
  control,
  value,
  onChange,
}: {
  control: Control;
  value: TaskValue;
  onChange: (next: TaskValue) => void;
}): JSX.Element {
  if (control.kind === 'unsupported') {
    return <Muted>{control.reason}</Muted>;
  }

  if (control.kind === 'choice') {
    return (
      <View>
        {control.options.map((option) => (
          <Pressable
            accessibilityRole="radio"
            accessibilityState={{ selected: value === option.value }}
            key={option.value}
            onPress={() => onChange(option.value)}
            style={{ paddingVertical: 8 }}
          >
            <Text style={{ color: value === option.value ? '#00d1ff' : '#f0f3f8' }}>
              {value === option.value ? '●' : '○'} {option.label}
            </Text>
          </Pressable>
        ))}
      </View>
    );
  }

  if (control.kind === 'labels') {
    const selected = Array.isArray(value) ? value : [];
    return (
      <View>
        {control.options.map((option) => {
          const checked = selected.includes(option);
          return (
            <Pressable
              accessibilityRole="checkbox"
              accessibilityState={{ checked }}
              key={option}
              onPress={() =>
                onChange(checked ? selected.filter((item) => item !== option) : [...selected, option])
              }
              style={{ paddingVertical: 8 }}
            >
              <Text style={{ color: checked ? '#00d1ff' : '#f0f3f8' }}>
                {checked ? '☑' : '☐'} {option}
              </Text>
            </Pressable>
          );
        })}
      </View>
    );
  }

  if (control.kind === 'ranking') {
    const order = Array.isArray(value) && value.length > 0 ? value : control.items;
    const move = (index: number, offset: number): void => {
      const next = [...order];
      const [moved] = next.splice(index, 1);
      if (moved === undefined) return;
      next.splice(index + offset, 0, moved);
      onChange(next);
    };
    return (
      <View>
        {order.map((item, index) => (
          <Row key={item}>
            <Body>
              {index + 1}. {item}
            </Body>
            <Button label="↑" onPress={() => move(index, -1)} disabled={index === 0} tone="ghost" />
            <Button
              label="↓"
              onPress={() => move(index, 1)}
              disabled={index === order.length - 1}
              tone="ghost"
            />
          </Row>
        ))}
      </View>
    );
  }

  return (
    <View>
      <Text style={styles.label}>Answer (whole number)</Text>
      <TextInput
        keyboardType="number-pad"
        onChangeText={(text) => onChange(text === '' ? null : Number(text))}
        placeholderTextColor="#9fb0c6"
        style={styles.input}
        value={typeof value === 'number' ? String(value) : ''}
      />
    </View>
  );
}
