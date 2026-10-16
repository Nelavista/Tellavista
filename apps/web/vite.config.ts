import react from '@vitejs/plugin-react';
import { defineConfig, loadEnv } from 'vite';

// Fixed, documented port map (docs/runbooks/local-setup.md):
// V1 5000 · API 8000 · web 5173 · admin 5174 · Mailpit 8025
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const apiTarget = env.VITE_API_BASE_URL || 'http://localhost:8000';
  return {
    plugins: [react()],
    server: {
      port: 5173,
      strictPort: true,
      // Same-origin API in local dev -> no CORS surprises; cookies keep working.
      proxy: { '/api': { target: apiTarget, changeOrigin: true } },
    },
    build: { outDir: 'dist', sourcemap: true },
  };
});
