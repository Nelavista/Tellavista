# V2 design direction — Gate 2

| Field | Value |
|---|---|
| Status | **Approved 2026-10-27. Build in progress.** |
| Gate | Gate 2 — design direction |
| Date | 2026-10-27; palette corrected to brand blue/white 2026-10-28 |
| Applies to | `apps/web`, `apps/admin`, `packages/design-tokens`, `packages/ui` |
| Does not apply to | V1 at the repository root, API contracts, deployment |
| Companion documents | `docs/v2-ui/AUDIT.md`, `docs/v2-ui/PARITY.md`, `docs/v2-ui/ROUTE-MAP.md`, `docs/v2-ui/IMAGE-PROMPTS.md`, `docs/design/ui-ux-framework.md` |

> This document records the approved visual and interaction direction for the
> whole V2 surface: public pages, auth, student app and admin. It is not a component
> inventory for its own sake. The question it answers is: **what should Nelavista
> look and feel like so it is unmistakably stronger than V1 without copying it?**

---

## 1. The idea: The Working Record

Nelavista is not a content library with a jobs board attached. It is a record of
what a student can actually do: what they studied, what they proved, what they
delivered, what they were paid. The interface should feel like that record.

**The Working Record** is a design language built from four things:

1. **The prospectus** — public pages read like a university prospectus or a field
   notebook: editorial, confident, specific, with room around the words.
2. **The work order** — briefs, requirements, deadlines and assignments are
   structured like a job ticket, not a marketing card.
3. **The transcript** — proof is presented as a record with evidence, dates,
   status and a clear source. Nothing is self-reported without saying so.
4. **The receipt** — money is a ledger. Rates, deductions, status and payout dates
   are visible, tabular and explainable.

That gives us a visual signature that is specific to Nelavista and cannot be
swapped into any SaaS template: **ruled lines, margin notes, stamped statuses,
tabular numbers, asymmetric editorial layouts, and one brand blue used like a
marker, not a decoration.**

### What this replaces

| V1 pattern | V2 direction |
|---|---|
| Long single landing page with `#section` anchors | Separate routed public pages, each with one job |
| Glassy cards, gradients, floating hero mockups | Flat surfaces, hairline rules, real product artifacts |
| Identical feature-card grids | Rows, ledgers and editorial sections with different shapes |
| Cyan glow and decorative motion | One brand blue used like a marker, motion only to explain change |
| Marketing copy with unverified counts | Claims only where the product or the business can evidence them |
| A desktop nav wrapped onto mobile | A real app shell: rail on desktop, bottom bar on mobile |
| Admin as a second, darker skin | Admin as the same system at a denser rhythm |

### Why it fits the product

- The primary user is a student who needs to know **what to do next**, not to be
  impressed by a dashboard.
- The product's differentiator is **verified proof and paid work**, so evidence
  and money must look first-class, not like secondary cards.
- Ops users work in the same system all day. A ledger/table language scales from a
  student's transcript to a payout batch without changing visual grammar.
- The public promise is serious: *Learn it. Prove it. Get paid for it.* The design
  should feel like a place where that sentence is kept.

---

## 2. Surface and theme model

### Recommendation: one brand, two surfaces — light and dark

| Surface | Used for | Default |
|---|---|---|
| **Light** | Public marketing, legal, long-form reading, printable transcript | Public pages |
| **Dark** | Student app, admin, auth side panels, dense data | Signed-in app and admin |

This is one token system with two surface themes, not two brands. The same type,
spacing, rules, stamps and components are used on both. The user can switch
between light and dark from the header, and the choice is remembered. The brand
palette is fixed: **Nelavista blue `#1535A8`** and **white `#FFFFFF`**. The dark
surface uses a lighter blue for text and focus so contrast holds on navy; the
brand blue remains the primary fill and the logo colour.

**Why keep both surfaces?**

- V1 has a light/dark toggle. Dropping it would make V2 feel like less, not more.
- Long legal and course material is easier to read on white.
- It gives the public site a clean editorial surface without creating a second
  design language.
- It makes the printed transcript and shared proof page feel like a document.

**Theme rules**

- No pure black (`#000`). The dark background is deep navy `#050810`, not black.
- No auto-inversion. Each theme is designed, not generated.
- The accent is re-mixed for each surface so contrast holds; it is not the same hex
  pasted onto both.
- Images are not tinted differently per theme. A photo is a photo.
- Charts and data visualisation use the semantic palette, not the brand accent
  alone.

---

## 3. Colour

### 3.1 Brand and semantic palette

The brand colour is Nelavista blue `#1535A8`; white `#FFFFFF` is the primary
light surface and the logo knockout. The V1 cyan is not carried forward as a brand
colour. It remains only as the `info` semantic, never as the action colour.

**Dark theme**

| Token | Value | Use |
|---|---|---|
| `bg` | `#050810` | Page background |
| `surface` | `#0A0F1A` | Panels, tables, inputs |
| `surfaceRaised` | `#0F1825` | Menus, drawers, hover rows |
| `surfaceSunken` | `#03060D` | Wells, code, table headers |
| `border` | `#1C2A3A` | Hairlines |
| `borderStrong` | `#2B4055` | Selected/active borders |
| `text` | `#EEF2F7` | Primary text |
| `textMuted` | `#8FA8C8` | Secondary text |
| `textSubtle` | `#6B84A3` | Metadata, placeholders |
| `accent` | `#6E8BFF` | Primary action, active nav, focus |
| `accentStrong` | `#8FA8FF` | Pressed/hover |
| `accentContrast` | `#050810` | Text on accent |
| `success` | `#2DD4BF` | Verified, paid, approved |
| `warning` | `#F5B942` | At risk, needs attention |
| `danger` | `#FF6B6B` | Error, destructive, rejected |
| `info` | `#7CC7FF` | Neutral information, links in prose |

**Light theme**

| Token | Value | Use |
|---|---|---|
| `bg` | `#FFFFFF` | Page background |
| `surface` | `#F7F9FC` | Panels, table headers |
| `surfaceRaised` | `#EEF2F7` | Menus, hover rows |
| `surfaceSunken` | `#FBFCFE` | Wells, code, inputs |
| `border` | `#DCE3EC` | Hairlines |
| `borderStrong` | `#B9C6D8` | Selected/active borders |
| `text` | `#0B1A2F` | Primary text |
| `textMuted` | `#3F5470` | Secondary text |
| `textSubtle` | `#6B7F99` | Metadata, placeholders |
| `accent` | `#1535A8` | Primary action, active nav, focus |
| `accentStrong` | `#0F2A86` | Pressed/hover |
| `accentContrast` | `#FFFFFF` | Text on accent |
| `success` | `#13805F` | Verified, paid, approved |
| `warning` | `#9A6400` | At risk, needs attention |
| `danger` | `#B42318` | Error, destructive, rejected |
| `info` | `#1D5F9E` | Neutral information, links in prose |

Contrast checks for the primary pairs (computed, not guessed):

| Pair | Ratio |
|---|---|
| Dark text / Dark bg | 17.81:1 |
| Dark muted / Dark bg | 8.20:1 |
| Dark accent / Dark bg | 6.48:1 |
| Dark accentContrast / Dark accent | 6.48:1 |
| Light text / Light bg | 17.46:1 |
| Light muted / Light bg | 7.74:1 |
| Light accent / Light bg | 9.97:1 |
| Light accentContrast / Light accent | 9.97:1 |

`textSubtle` is metadata only; it is not used for body copy. Warning and danger are
never used as the only signal: every status has a word and, where useful, an icon.

### 3.2 Colour rules

- The accent may cover at most **10%** of a screen. It marks the action, the
  current location and the focus ring; it is not a background wash.
- No gradients for surfaces, buttons, text or borders. No glow. No coloured
  shadows. No gradient blobs. No glassmorphism or backdrop blur.
- No second brand colour. The semantic colours are functional, not decorative.
- Selection and focus use `accent`; do not use a separate blue focus ring.
- Tables use `surface` and hairlines, not zebra stripes. Hover is
  `surfaceRaised`. Selected is a 2px `accent` inline-start border plus a tint of
  `accent` at 8%.
- Charts use `info`, `success`, `warning` and `danger`; the accent is reserved for
  the primary series only if the chart has a single series.

---

## 4. Typography

### 4.1 Families

| Role | Family | Why |
|---|---|---|
| Display / editorial | **Instrument Serif** (400, italic) | Gives public pages a prospectus voice and a human edge without looking like a startup template. |
| UI / body | **Instrument Sans** (400–700, variable) | Compact, legible at 13–16px, good in dense tables; pairs with the serif without matching it. |
| Data / metadata | **IBM Plex Mono** (400–600) | Course codes, dates, rates, status stamps, ledger values, keyboard hints. Tabular numerals. |

All three are open-source and self-hosted. Do not load them from a third-party CDN
at runtime. Subset Latin, use `font-display: swap`, preload only the display
regular and the UI regular, and provide metric-compatible fallbacks:

- Display fallback: `Georgia, 'Times New Roman', serif`
- UI fallback: `system-ui, -apple-system, 'Segoe UI', sans-serif`
- Mono fallback: `ui-monospace, 'Cascadia Mono', Consolas, monospace`

This is deliberately different from V1's Bricolage Grotesque / DM Sans / JetBrains
Mono trio. Do not carry those families into V2.

### 4.2 Scale

A 1.25 ratio, not a collection of arbitrary sizes:

| Token | Size | Line height | Use |
|---|---|---|---|
| `xs` | 12px / 0.75rem | 1.4 | Stamps, table metadata, legal notes |
| `sm` | 14px / 0.875rem | 1.45 | Secondary UI, table body |
| `base` | 16px / 1rem | 1.55 | Body, forms, public copy |
| `lg` | 20px / 1.25rem | 1.35 | Lead paragraphs, card titles |
| `xl` | 25px / 1.5625rem | 1.2 | Section headings |
| `2xl` | 31px / 1.9375rem | 1.15 | Page titles |
| `3xl` | 39px / 2.4375rem | 1.1 | Public section headings |
| `4xl` | 49px / 3.0625rem | 1.05 | Public hero |

- Display headings use Instrument Serif, `font-weight: 400`, tight tracking
  (`-0.02em`). Italic is reserved for one emphasized phrase, not whole headings.
- UI headings use Instrument Sans 600/700.
- Body copy is 16px on public and reading surfaces; app body is 14–16px; admin
  body is 14px.
- Mono labels are 11–12px, uppercase, `letter-spacing: 0.08em`.
- Numerals in money, dates, counts and scores use `font-variant-numeric:
  tabular-nums`.
- Never use more than three weights on one screen.

---

## 5. Space, shape and elevation

### 5.1 Spacing

4px base. Tokens: `4, 8, 12, 16, 24, 32, 40, 48, 64, 80, 96`.

| Surface | Section rhythm | Component gap |
|---|---|---|
| Public | 64–96px desktop, 40–56px mobile | 16–24px |
| Auth | 32–48px | 12–16px |
| Student app | 24–40px | 8–16px |
| Admin | 16–24px | 4–12px |
| Table rows | 40–44px | 0 (hairlines) |

No empty bands of space used to signal “premium”. Space must group or separate
meaning.

### 5.2 Shape

| Token | Value | Use |
|---|---|---|
| `stamp` | 2px | Status stamps, tags |
| `control` | 4px | Buttons, inputs, selects |
| `panel` | 8px | Tables, panels, drawers |
| `dialog` | 12px | Modals, command menu |
| `pill` | 999px | Only for filters/chips that are genuinely toggleable |

The sharper radii are intentional: rounded 20px cards are the default SaaS look.
A 4px control and an 8px panel read as a working tool. Do not round every surface.

### 5.3 Elevation

- No shadows by default.
- Use `border` and `surface` contrast to separate layers.
- Dialogs and drawers may use a single neutral shadow at 10–12% opacity, plus a
  scrim. No coloured shadow, no glow.
- Sticky headers use a 1px bottom rule and a solid surface, not blur.

---

## 6. Layout and density

### 6.1 Public pages

- Max content width **1200px**; text measure **680px**.
- 12-column grid, 24px gutter. Use asymmetric splits: 7/5, 8/4, 5/7.
- The hero is not full-viewport. It is a composition: headline + proof artifact,
  then a horizontal journey strip.
- Sections are separated by hairlines and margin labels, not by cards.
- One dominant anchor per page. On the landing page it is **Create your account**.
- Public header: logo, Platform, How it works, About, Log in, Get started. Sticky,
  solid white, 1px bottom rule. No translucent blur.
- Public footer: sitemap, legal, contact, social. No giant decorative wordmark.

### 6.2 Student app

- Desktop: 240px left rail, 64px top bar, content max 1120px, optional 320px
  inspector on detail screens. Collapse the rail to icons at 1024px; bottom bar
  below 768px.
- Mobile: 56px top bar, 64px bottom bar, safe-area padding, content full width.
- Page header: eyebrow (mono), title, one-line purpose, primary action. No
  dashboard card grid at the top of every page.
- Home is a **next-action** screen, not a welcome screen. It answers: what should I
  do now, what is due, what changed, what did I earn?
- Lists and tables are the default for courses, materials, opportunities, work and
  earnings. Cards are for a single object that needs a boundary (a course summary,
  a proof artifact), not for every item in a collection.
- Detail screens use a two-column layout: main content + a sticky context rail
  (requirements, deadline, rate, status, actions).
- Empty states keep the page structure and explain how data appears. They are not
  a centred illustration with “Nothing here yet”.

### 6.3 Admin

- 220px rail, 56px top bar, content max 1440px, dense tables.
- Every screen follows the same shape: page header with count and primary action,
  filter bar, table, detail drawer, audit footer.
- Table rows 32–36px; touch targets are still 44px where the admin may be used on
  a tablet.
- Keyboard path: `/` focuses search, `j/k` moves rows, `Enter` opens, `Esc` closes.
- Bulk actions appear in a sticky bar only when rows are selected.
- No marketing language. No cards where a table is the right object.

### 6.4 Responsive rules

- 320px minimum; 375px primary design width; 768px tablet; 1024px small desktop;
  1280px and 1440px desktop.
- No horizontal scrolling for page content. Tables may scroll horizontally inside
  a labelled region, with a frozen first column.
- At 200% zoom, content reflows; nothing is clipped.
- Touch targets are at least 44×44px on web; admin may use 32px rows but must keep
  a 44px hit area for interactive cells.
- Use logical properties (`margin-inline`, `padding-block`) from the start.

---

## 7. Components and patterns

### 7.1 Primitives to build once in `packages/ui`

Button, IconButton, Link, Input, Textarea, Select, Checkbox, Radio, Switch, Field,
FormError, Stamp, Tag, Avatar, Tooltip, Popover, Dialog, Drawer, Toast, Banner,
Tabs, Accordion, Breadcrumbs, Pagination, Table, DataTable, EmptyState,
ErrorState, Skeleton, Progress, Meter, Stepper, PageHeader, SectionHeader, Money,
DateTime, CopyButton, Prose, TOC, SearchInput, FilterBar, SegmentedControl,
StatusDot, Timeline.

Every primitive has: default, hover, focus-visible, active, disabled, loading,
invalid, read-only, and dark/light states where relevant. No screen re-implements
a button or a field locally.

### 7.2 Signature patterns

| Pattern | What it is | Where |
|---|---|---|
| **Proof chain** | A vertical or horizontal sequence of evidence: learned → assessed → verified → worked → paid. Each step links to its record. | Landing, Home, Verification, Transcript |
| **Ledger row** | A 40–44px row with a mono reference, a title, a status stamp, a date and a right-aligned value. | Materials, Opportunities, Work, Earnings, Admin |
| **Stamp** | A 2px-radius, uppercase mono status mark with a word, not just a colour. | Everywhere a status appears |
| **Work order** | A brief panel with scope, requirements, rate, deadline and submission. | Assignment detail, opportunity detail |
| **Receipt** | A money panel with line items, deductions, total and payout status. | Earnings, admin money |
| **Transcript** | A document-like record with evidence links, dates and verification status. | `/transcript`, shared profile |
| **Margin note** | A small mono annotation in the left column of a public section. | Public pages |
| **Question palette** | A numbered grid of answered/unanswered questions with a timer. | CBT, assessments |

### 7.3 What we will not build

- No hero that fills the viewport.
- No gradient blobs, mesh gradients, glow, glass, or coloured shadows.
- No identical three-card feature grid.
- No bento grid used as a substitute for information architecture.
- No icon-only primary navigation.
- No decorative charts, fake dashboards, fake testimonials or invented metrics.
- No emoji in UI copy.
- No autoplay carousels, scroll hijacking, parallax, or infinite decorative
  animation.
- No “AI magic” sparkle iconography. AI is a tool with a name and a limit, not a
  personality.

---

## 8. Motion

Use **Motion** (the package formerly called Framer Motion) only where it explains
a change. Use CSS transitions for hover, focus, pressed and simple disclosure.

| Motion | Duration | Easing | Notes |
|---|---|---|---|
| Hover/press | 120ms | `ease-out` | Colour/border only |
| Disclosure | 180ms | `cubic-bezier(0.2, 0, 0, 1)` | Height/opacity |
| Page enter | 180ms | same | 8px translate + opacity, no full-page slide |
| Drawer | 240ms | same | Translate from inline-end |
| Toast | 240ms | same | Enter from bottom, no bounce |
| Layout change | 200ms | same | Shared layout only when it clarifies a move |

Rules:

- Respect `prefers-reduced-motion: reduce`: remove transforms and animation;
  keep instant state changes and opacity only where needed.
- Never animate a number just to show off. Count-up is allowed only for a single
  summary value and must be disabled under reduced motion.
- No animation may delay an action or block input.
- Use `LazyMotion`/`domAnimation` or lazy-load Motion on public pages to protect
  the 150KB JS budget. If Motion would break the budget, use CSS for that screen.

---

## 9. Imagery and product artifacts

### 9.1 Photography

Use real photography where it carries content, not as decoration. The subject is
Nigerian/African university students in real study and work settings: lecture
halls, campus walkways, shared desks, a phone in hand, a laptop with real work on
screen. Documentary, natural light, no stock “happy graduate” clichés, no
poverty framing, no generic “African pattern” overlay.

Needed images (exact filenames will be listed in `IMAGE-PROMPTS.md` before build):

- `public/images/home/hero-student.webp` — 4:5, a student working on a phone/laptop
  in a real campus setting. This is the only hero image.
- `public/images/home/campus-study.webp` — 3:2, students working together.
- `public/images/about/founder.webp` — real founder portrait, not generated.
- `public/images/about/team.webp` — real team photo, only if one exists.
- `public/images/og/default.webp` — 1200×630 social card using the wordmark and one
  real product artifact, not a stock photo.
- `public/images/share/og-proof.webp` — 1200×630 for shared profiles, generic
  enough not to leak a student's data.

If a real image is not available, use a solid `surfaceRaised` block with a short
caption and alt text. Do not fill the gap with a generated person or a fake
testimonial.

### 9.2 Product artifacts

The strongest imagery is the product itself. Public pages should show **real V2
screens and real data shapes**, not a fake “dashboard” illustration. Use live
components where possible; otherwise use static captures that match the current
build and are regenerated when the UI changes.

Artifacts to show on the landing page:

1. A transcript row with a verified skill and a date.
2. A work order with a rate and a deadline.
3. A payout receipt with a line item and a paid stamp.
4. A CBT result with a topic and a next action.

These are the proof chain. They must be real components or real captures, not
invented numbers.

---

## 10. Content voice

- Direct, specific, calm. Write like a good ops lead, not a growth marketer.
- Use “you” and the active voice. Name the action in the button.
- Prefer a number with a unit over an adjective: “12,500 NGN”, “3 days left”,
  “2 of 5 lessons”.
- No hype words: unlock, unleash, revolutionise, seamless, supercharge, elevate,
  game-changing, world-class.
- No fake urgency, no invented social proof, no “trusted by thousands” unless the
  number is verified and current.
- Empty states explain how the data appears and what to do next.
- Error states say what happened, what was preserved, and the next step. A
  feature-flag 404 says “not switched on here”, not “something went wrong”.
- Legal and consent copy must be reviewed by counsel. Do not ship V1 legal text
  unchanged; V2 no longer has community groups or employer self-service.

---

## 11. Accessibility, performance and quality gates

### Accessibility

- WCAG 2.2 AA. Body text targets 7:1 and never falls below 4.5:1.
- Visible focus ring: 2px `accent`, 2px offset, on every interactive element.
- Skip link to main content; route-change focus moves to the page heading.
- `aria-current="page"` on active navigation.
- All status colours have a text label and, where useful, an icon.
- Keyboard path for every task, including tables, drawers, dialogs and the CBT
  question palette.
- Reduced motion, forced-colors mode, 200% zoom and 320px width are tested.
- No `dangerouslySetInnerHTML` without a vetted sanitizer.

### Performance

- First-load budget stays **150KB JS gzip / 20KB CSS gzip**.
- Self-hosted fonts, subset, preload only critical faces; use `font-display: swap`.
- Images: AVIF/WebP, `srcset`, width/height, lazy loading except the hero.
- Public pages are static content; do not block them on API calls.
- Motion and icon packages are tree-shaken; lazy-load non-critical motion.
- No API response caching in the PWA. API data can contain one student's work,
  earnings or identity.

### Definition of done for a screen

- Loading, empty, error, partial/stale, feature-off and success states where they
  can occur.
- 320px, 375px, 768px, 1280px and 1440px reviewed.
- Keyboard-only path and screen-reader labels checked.
- Light and dark surfaces checked.
- No console errors; typecheck, lint, tests and production build pass.
- Screenshots added to the PR for visual review.

---

## 12. How this beats V1, specifically

| V1 | V2 |
|---|---|
| One long landing page with repeated sections | Routed pages: Home, Features, How it works, About, Contact, FAQ, Legal |
| Glassy cards and animated pillar cards | Editorial rows, proof artifacts and a ledger strip |
| A top nav that wraps on mobile | A real responsive shell with a mobile bottom bar |
| Student app is a collection of pages with inconsistent headers | One app shell, one page-header pattern, one table/list language |
| Admin is a separate dark skin | Same tokens, same primitives, denser rhythm |
| Theme toggle with a light/dark inversion | Light and dark are both designed; the choice persists |
| Hard-coded “2,500+ students” and “20 paths” | Only verified, current numbers; otherwise no number |
| Legal text that describes V1 features V2 dropped | Legal and consent copy rewritten for the V2 product |
| No 404, no error boundary, no notification centre | Utility screens and a dedicated notifications route |
| Public pages stop at the landing page | Full public surface: features, how it works, about, contact, FAQ, legal |

---

## 13. Implementation order after approval

1. **Tokens and theme bridge** — light/dark, type, spacing, radius, motion,
   breakpoints, focus ring. Remove admin's duplicate palette.
2. **Primitives in `packages/ui`** — button, field, select, checkbox, stamp,
   banner, table, empty/error/skeleton, dialog, drawer, toast.
3. **App shell and page-header patterns** — web and admin.
4. **Public pages** — home, features, how it works, about, contact, FAQ, legal.
5. **Auth** — login, signup, verify, reset, 2FA where relevant.
6. **Student app** — home, notifications, academia, skills, verification,
   opportunities, work, earnings, transcript, talent, settings, campus.
7. **Admin** — audit, imports, users, opportunities, work, review, money, content,
   platform, security, plus the missing waitlist/campus/application/payout-item
   actions.
8. **Utility** — 404, error boundary, offline, maintenance/announcement if approved.
9. **Verification** — screenshots, keyboard path, budgets, reduced motion, both
   themes.

Do not build a screen before its tokens and primitives exist. Do not build a
primitive twice.

---

## 14. Approval recorded

These decisions were approved on 2026-10-27 and corrected on 2026-10-28 to keep
the platform on the V1 brand palette:

1. **Concept:** The Working Record (prospectus + work order + transcript +
   receipt).
2. **Theme model:** light + dark, using the Nelavista blue and white brand palette.
3. **Accent:** Nelavista blue `#1535A8`; white surfaces; no orange brand accent.
4. **Type:** Instrument Serif + Instrument Sans + IBM Plex Mono.
5. **Density:** public editorial, app compact, admin dense.
6. **Motion:** Motion for route/disclosure/drawer only; CSS for micro-interactions.
7. **Imagery:** editorial blue/white block-print illustrations for mood, real
   photography where the content is documentary, and real product artifacts. Never
   generated evidence, testimonials or metrics.
8. **Scope:** public pages and missing app/admin screens are in scope; newsletter
   and the platform announcement banner are deferred post-launch (see `AUDIT.md`).

The first change was the token and primitive foundation, not a page. The palette
is Nelavista blue `#1535A8` and white `#FFFFFF`; the dark surface uses a readable
blue tint for text and focus, not a second brand colour.
