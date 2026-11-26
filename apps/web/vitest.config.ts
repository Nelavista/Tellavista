import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    // The fetch layer reads document.cookie and uses browser globals.
    environment: 'jsdom',
    include: ['src/**/*.test.ts', 'src/**/*.test.tsx'],
    setupFiles: ['./src/test-setup.ts'],
    restoreMocks: true,
    // Route tests now run axe on the rendered page, on top of the lazy-route
    // wait. The default 5 s can abort a slow CI run mid-analysis, and a
    // timed-out axe leaves the next test failing with "Axe is already running".
    // The budget is for test overhead, not a slow product path.
    testTimeout: 20_000,
  },
});
