/**
 * React 18 only flushes updates inside `act()` when the environment says it is a
 * test run. Without this, component updates are scheduled asynchronously and the
 * DOM tests can pass for the wrong reason.
 */
declare global {
  var IS_REACT_ACT_ENVIRONMENT: boolean | undefined;
}

globalThis.IS_REACT_ACT_ENVIRONMENT = true;

/**
 * jsdom does not implement scrolling or IntersectionObserver. The admin shell
 * resets scroll on navigation, and Motion may ask for the observer. Both are
 * browser APIs, not product logic, so the tests get inert stand-ins.
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
