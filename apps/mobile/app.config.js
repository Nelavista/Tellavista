/**
 * Expo app config. Environment comes from build profiles, NOT runtime guessing (ADR-0002/0009).
 *
 * EAS sets APP_VARIANT per profile (see eas.json). DEV builds get a `.dev` suffix on
 * both the iOS bundle identifier and the Android package name so DEV and PROD apps
 * install side by side, with different names and icons.
 */
const VARIANT = process.env.APP_VARIANT || 'development';

const isProd = VARIANT === 'production';
const isDev = VARIANT === 'development';

const suffix = isProd ? '' : isDev ? '.dev' : '.preview';
const name = isProd ? 'Nelavista' : isDev ? 'Nelavista Dev' : 'Nelavista (Preview)';

// Base URLs are per-environment and never hardcoded in app code.
const apiBaseUrl =
  process.env.API_BASE_URL ||
  (isProd ? 'https://api.nelavista.com' : 'https://api-dev.nelavista.com');

module.exports = {
  expo: {
    name,
    slug: 'nelavista',
    scheme: 'nelavista',
    version: '1.0.0',
    orientation: 'portrait',
    userInterfaceStyle: 'automatic',
    runtimeVersion: { policy: 'appVersion' },
    updates: { url: 'https://u.expo.dev/00000000-0000-0000-0000-000000000000' },
    ios: {
      bundleIdentifier: `com.nelavista.app${suffix}`,
      supportsTablet: false,
      // Universal links on nelavista.com (ADR-0001); dev uses a dev host.
      associatedDomains: isProd
        ? ['applinks:nelavista.com']
        : ['applinks:api-dev.nelavista.com'],
    },
    android: {
      package: `com.nelavista.app${suffix}`,
      // Android App Links
      intentFilters: [
        {
          action: 'VIEW',
          autoVerify: true,
          data: [{ scheme: 'https', host: isProd ? 'nelavista.com' : 'api-dev.nelavista.com' }],
          category: ['BROWSABLE', 'DEFAULT'],
        },
      ],
      adaptiveIcon: { backgroundColor: '#050810' },
    },
    plugins: ['expo-secure-store', 'expo-notifications', 'expo-updates'],
    extra: {
      appVariant: VARIANT,
      apiBaseUrl,
      apiVersion: 'v1',
      eas: { projectId: '00000000-0000-0000-0000-000000000000' },
    },
  },
};
