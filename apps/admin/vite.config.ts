import react from '@vitejs/plugin-react';
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const apiTarget = env.VITE_API_BASE_URL || 'http://localhost:8000';
  return {
    plugins: [react()],
    server: {
      port: 5174,
      strictPort: true,
      // The API serves /v1/..., the app calls /api/v1/...; strip the prefix so
      // the proxy target matches the real route.
      proxy: {
        '/api': {
          target: apiTarget,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
        },
      },
    },
    build: { outDir: 'dist', sourcemap: true },
  };
});
