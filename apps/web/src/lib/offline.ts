/**
 * Offline cache helpers.
 *
 * The service worker only precaches the app shell. API responses are never
 * stored, because an authenticated response belongs to one student and must
 * not survive a sign-out. Older builds did cache API GETs under `nv-api`, so
 * we delete that cache whenever the app starts or the session changes.
 */
const LEGACY_API_CACHE = 'nv-api';

export async function clearApiCache(): Promise<void> {
  if (typeof caches === 'undefined') return;
  try {
    const names = await caches.keys();
    await Promise.all(
      names
        .filter((name) => name === LEGACY_API_CACHE || name.startsWith(`${LEGACY_API_CACHE}-`))
        .map((name) => caches.delete(name)),
    );
  } catch {
    // Cache storage can be unavailable (private mode, storage pressure). A
    // failed cleanup must never block sign-in or sign-out.
  }
}
