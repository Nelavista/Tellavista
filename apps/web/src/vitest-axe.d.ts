/**
 * vitest-axe 0.1.0 declares its matcher on the Jest-era global `Vi` namespace,
 * which Vitest 2 no longer uses. Augment the interface Vitest 2 actually
 * exposes so `expect(await axe(...)).toHaveNoViolations()` type-checks. The
 * matcher itself is registered in test-setup.ts.
 */
declare module '@vitest/expect' {
  // Vitest declares the same default; an augmentation must match it exactly.
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  interface Assertion<T = any> {
    toHaveNoViolations(): {
      pass: boolean;
      message(): string;
      actual: T;
    };
  }
}

export {};
