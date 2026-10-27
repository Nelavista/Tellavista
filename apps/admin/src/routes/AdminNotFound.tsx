/**
 * Unknown admin hash.
 *
 * The ops app keeps the address the operator typed, says the screen does not
 * exist, and offers the two places worth trying instead of silently falling
 * back to Audit.
 */
import { EmptyState, PageHeader } from '@nelavista/ui';
import { Compass } from 'lucide-react';

export function AdminNotFound({ route }: { route: string }): JSX.Element {
  return (
    <div className="nv-stack">
      <PageHeader
        eyebrow="Not found"
        title="That screen does not exist"
        description={`No ops screen is mapped to ${route}. The address is unchanged so you can correct it.`}
      />
      <EmptyState
        action={
          <>
            <a className="nv-button nv-button--secondary nv-button--sm" href="#/overview">
              Operations overview
            </a>
            <a className="nv-button nv-button--ghost nv-button--sm" href="#/audit">
              Audit trail
            </a>
          </>
        }
        body="Check the hash after #. The sidebar lists every screen this account can open."
        icon={Compass}
        title="Check the address"
      />
    </div>
  );
}
