import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    // The fetch layer reads document.cookie and uses browser globals.
    environment: 'jsdom',
    include: ['src/**/*.test.ts', 'src/**/*.test.tsx'],
    restoreMocks: true,
  },
});
