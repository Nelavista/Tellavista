/**
 * One accessibility assertion for route tests.
 *
 * axe runs on the rendered route container, so a screen that loses a label,
 * heading or landmark fails its own route test rather than only in a manual
 * audit. Colour contrast is not evaluated by axe in jsdom; the CSS media
 * queries cover that, and the manual high-contrast pass in the launch checklist
 * remains the check for real pixels.
 */
import { axe } from 'vitest-axe';
import { expect } from 'vitest';

export async function expectNoA11yViolations(container: HTMLElement): Promise<void> {
  // jsdom has no layout engine or canvas, so colour contrast can never be
  // computed and icon-ligature measurement throws. Leaving those rules on adds
  // seconds of doomed analysis and noise; the high-contrast media queries plus
  // the manual pass cover pixels.
  const results = await axe(container, {
    preload: false,
    rules: {
      'color-contrast': { enabled: false },
      'label-content-name-mismatch': { enabled: false },
    },
  });
  expect(results).toHaveNoViolations();
}
