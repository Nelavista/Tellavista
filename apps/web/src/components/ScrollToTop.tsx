import * as React from 'react';
import { useLocation } from 'react-router-dom';

/** A new route opens at the top, not at the previous page's footer. */
export function ScrollToTop(): null {
  const { pathname } = useLocation();

  React.useLayoutEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return null;
}
