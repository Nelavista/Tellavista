import react from '@vitejs/plugin-react';
import { defineConfig, loadEnv } from 'vite';
import { VitePWA } from 'vite-plugin-pwa';

// Fixed, documented port map (docs/runbooks/local-setup.md):
// V1 5000 · API 8000 · web 5173 · admin 5174 · Mailpit 8025
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const apiTarget = env.VITE_API_BASE_URL || 'http://localhost:8000';
  return {
    plugins: [
      react(),
      VitePWA({
        registerType: 'autoUpdate',
        includeAssets: ['icons/icon-192.png', 'icons/icon-512.png', 'icons/maskable-512.png'],
        manifest: {
          name: 'Nelavista',
          short_name: 'Nelavista',
          description: 'Learn it, prove it, get paid for it.',
          start_url: '/',
          scope: '/',
          display: 'standalone',
          background_color: '#050810',
          theme_color: '#050810',
          orientation: 'portrait',
          icons: [
            { src: '/icons/icon-192.png', sizes: '192x192', type: 'image/png' },
            { src: '/icons/icon-512.png', sizes: '512x512', type: 'image/png' },
            {
              src: '/icons/maskable-512.png',
              sizes: '512x512',
              type: 'image/png',
              purpose: 'maskable',
            },
          ],
        },
        workbox: {
          // The app shell works offline. API responses are deliberately never
          // cached: they can contain one student's work, earnings or identity,
          // and must not be served to another account after a sign-out.
          navigateFallback: '/index.html',
          navigateFallbackDenylist: [/^\/api\//],
          cleanupOutdatedCaches: true,
        },
      }),
    ],
    server: {
      port: 5173,
      strictPort: true,
      // Same-origin API in local dev -> no CORS surprises; cookies keep working.
      // The API serves /v1/..., the app calls /api/v1/..., so strip the prefix.
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
