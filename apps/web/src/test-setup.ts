/**
 * React 18 only flushes updates inside `act()` when the environment says it is a
 * test run. Without this, component updates are scheduled asynchronously and the
 * DOM tests pass for the wrong reason (or flake), printing an `act(...)` warning
 * instead of failing honestly.
 */
declare global {
  var IS_REACT_ACT_ENVIRONMENT: boolean | undefined;
}

globalThis.IS_REACT_ACT_ENVIRONMENT = true;

/**
 * jsdom does not implement IntersectionObserver or scrolling. Motion's
 * `whileInView` needs the observer constructor to exist, and the route reset
 * calls `window.scrollTo`. Both are browser APIs, not product logic, so the
 * test environment gets inert stand-ins. Content still renders in the DOM.
 */
if (!('IntersectionObserver' in globalThis)) {
  class InertIntersectionObserver implements IntersectionObserver {
    readonly root = null;
    readonly rootMargin = '';
    readonly thresholds: ReadonlyArray<number> = [];
    disconnect(): void {}
    observe(): void {}
    takeRecords(): IntersectionObserverEntry[] {
      return [];
    }
    unobserve(): void {}
  }

  globalThis.IntersectionObserver = InertIntersectionObserver as unknown as typeof IntersectionObserver;
}

window.scrollTo = (() => undefined) as typeof window.scrollTo;

export {};
