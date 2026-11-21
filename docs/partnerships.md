# Partnerships: TEF and Naijalancers

Two partner pipelines, both live in the **Opportunities** space on V1. Neither needs a
schema change or a new application flow: TEF is a Discover listing, and Naijalancers is
a gig provider.

The V1 community group-chat is retired (`/community` redirects to the dashboard), so the
"TEF pre-application community" stays in the external group. The site's job is to hold
the verified programme listing and the preparation information, not to host a second
group chat.

## TEF (Tony Elumelu Foundation)

Students see TEF under **Discover → Entrepreneurship**
(`/opportunities/discover?category=entrepreneurship`). The detail page already renders
Overview, Eligibility, What you get, What you'll need and How to apply, so the
pre-application education lives in those fields.

### How to publish it

1. Add an entry to `seed_data/opportunities/opportunities.json` (or use the admin form
   at `/admin/student-opportunities`).
2. Fill only facts copied from TEF's own pages. **Never guess a URL, date or
   eligibility rule.** Required inputs from the client/TEF:
   - official programme page and application URL;
   - application window (`opens_at`, `deadline`, or `is_rolling` with a note);
   - who is eligible (level, discipline, country);
   - what applicants must prepare, and the do's / don'ts;
   - whether TEF approves the public wording "Nelavista partner" and use of its name.
3. Set `category` to `entrepreneurship`, `source_url` to the page where the facts were
   checked, and `verified_on` to the date checked. Without `verified_on` the importer
   creates an unverified draft that students never see.
4. Set `is_partner: true` only if TEF has agreed to that public claim. Otherwise leave
   it false; the detail page then shows the "Nelavista isn't affiliated" note.
5. Import on the server and review before publishing:

   ```bash
   python -m scripts.seed.seed_student_opportunities            # dry run
   python -m scripts.seed.seed_student_opportunities --apply    # write drafts
   ```

   Publishing is refused unless the row is verified, has a source URL and an
   application route, and has a deadline or is rolling. An expired programme is never
   published.

Before applications open, set `opens_at` in the future. Discover shows it as
**upcoming**, and students can save it — that is the pre-application phase on the
platform.

The landing page's Entrepreneurship card now links to this filtered Discover view.

## Naijalancers

Naijalancers is a **gig provider**, not a programme listing. Gig providers are created
by `ensure_default_providers()`; the `naijalancers` provider is enabled with the
`manual` adapter, so it never scrapes or syncs.

- Provider name and attribution: **Naijalancers**.
- Admin adds each gig only after checking it with Naijalancers.
- Every gig keeps its official listing URL; students apply there.
- Never bulk-copy Naijalancers pages. If Naijalancers publishes an official API or
  feed, add a proper sync adapter instead of switching on a scraper.

Add gigs at `/admin/gigs`, choosing the Naijalancers provider. Students see them under
**Gigs** (`/opportunities/gigs`) with the provider attribution.

After a deploy, make sure the provider exists:

```bash
flask --app wsgi gigs-seed-providers
```

The command is idempotent; it creates the provider only when it is missing.

## Go-live checklist

- [ ] TEF dates, eligibility and URLs checked on TEF's own pages, with `verified_on`
      recorded.
- [ ] TEF partner badge approved (or left off).
- [ ] Grace has the agreed role/account, and the alumni-community invitation is done.
- [ ] Naijalancers provider exists in the deployed environment.
- [ ] First Naijalancers gigs added, published and linked to their official listing.
- [ ] Landing page checked at desktop and mobile widths (Entrepreneurship card links to
      Discover).
