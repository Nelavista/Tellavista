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

export {};
