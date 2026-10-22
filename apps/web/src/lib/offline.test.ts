import { afterEach, describe, expect, it, vi } from 'vitest';

import { clearApiCache } from './offline';

describe('clearApiCache', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('deletes only API caches', async () => {
    const deleted: string[] = [];
    vi.stubGlobal('caches', {
      keys: async () => ['nv-api', 'nv-api-v2', 'workbox-precache', 'images'],
      delete: async (name: string) => {
        deleted.push(name);
        return true;
      },
    });

    await clearApiCache();

    expect(deleted.sort()).toEqual(['nv-api', 'nv-api-v2']);
  });

  it('does nothing when CacheStorage is unavailable', async () => {
    vi.stubGlobal('caches', undefined);
    await expect(clearApiCache()).resolves.toBeUndefined();
  });

  it('swallows cache errors', async () => {
    vi.stubGlobal('caches', {
      keys: async () => {
        throw new Error('denied');
      },
      delete: async () => true,
    });

    await expect(clearApiCache()).resolves.toBeUndefined();
  });
});
