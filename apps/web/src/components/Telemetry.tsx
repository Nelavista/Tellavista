import * as React from 'react';
import { useLocation } from 'react-router-dom';

import { capturePageview } from '../lib/telemetry';

/** One page view per route change. Rendered inside the router, renders nothing. */
export function Telemetry(): null {
  const { pathname } = useLocation();

  React.useEffect(() => {
    capturePageview(pathname);
  }, [pathname]);

  return null;
}
