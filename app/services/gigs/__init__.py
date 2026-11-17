"""Gigs: paid work and projects in the Opportunities space.

    core.py      taxonomy, availability/freshness, pay formatting, skill match, feed,
                 per-student state, analytics events, admin checks and actions
    adapters.py  ProviderAdapter base + one adapter per source (fetch_gigs,
                 normalize_gig, get_status); every adapter yields a NormalizedGig
    sync.py      the background synchronisation: upsert, dedupe, close/expire,
                 failure handling, the scheduler loop and the `flask gigs-sync` CLI

Rules that hold everywhere:
- Only sources whose terms permit redistribution are integrated. A provider can't be
  enabled until an admin records that basis (GigProvider.redistribution_confirmed).
  There is no scraper.
- Students see gigs from Nelavista's database only. No browser ever calls a provider.
- A gig is "open" only while a source or an admin has confirmed it recently. Otherwise
  it shows as "Availability unknown" and is kept out of the Open Gigs feed.
- External gigs are never presented as Nelavista's. "I applied" is self-reported.
"""
