# Nelavista V2 UI/UX Engineering and Design Framework

| Field | Value |
|---|---|
| Status | Active for V2 UI/UX work |
| Applies to | `apps/web`, `apps/admin`, `apps/mobile` (post-launch), `packages/ui`, `packages/design-tokens` |
| Does not apply to | V1 at the repository root, API contracts, infrastructure, or deployment |
| Last updated | 2026-10-27 |
| Companion documents | `docs/adr/0001-v2-stack.md`, `docs/architecture/01-target-structure.md`, `CONTRIBUTING.md`, `RUN-LOCALLY.md` |

> **Gate 2 approved 2026-10-27.** The Ink + Paper model in
> `docs/v2-ui/DESIGN-DIRECTION.md` is the current visual direction. This guide is
> the engineering guard for that direction; the route contract lives in
> `docs/v2-ui/ROUTE-MAP.md`. Where this file and those two disagree, the approved
> direction and route map win, and this file is corrected in the same change.
>
> This is the working guide for anyone changing a V2 screen. It is the project-specific version of the master UI/UX framework. The order of authority is:
>
> 1. The live brand tokens in `packages/design-tokens/src/index.ts`.
> 2. `docs/v2-ui/DESIGN-DIRECTION.md` and `docs/v2-ui/ROUTE-MAP.md`.
> 3. This document.
> 4. The generic framework, where this document is silent.
>
> If a rule here is wrong for the product, change this file in the same pull request that changes the UI. Do not leave the guide and the code disagreeing.

---

## 0. Operating summary

- **Primary user:** a Nigerian university student, usually 18-25, on a mid-range Android phone, on a slow or intermittent connection, often holding the phone in one hand.
- **Primary promise:** *Learn it. Prove it. Get paid for it.* Every screen should make the next step in that journey obvious.
- **One screen, one job, one dominant anchor.** If everything is emphasized, nothing is.
- **Data first.** Start with the real API shape, the worst-case value, and every state. Do not start with a card component.
- **Build for the worst case:** long names, empty values, failed requests, partial data, offline, zero earnings, seven-figure earnings, a 320px screen, and 200% zoom.
- **No V1 changes.** V1 is live at `nelavista.com` and is frozen for features. This guide covers V2 only.
- **No new dependency without a reason.** State the bundle cost, the accessibility record, and the category it replaces. One library per category.
- **Done means verified:** lint, typecheck, tests, production build, first-load budget, keyboard path, and screenshots at 375, 768, and 1280 pixels.

---

## 1. V2 project brief

This section fills the project brief that the generic framework leaves blank. Treat it as the default answer for every V2 screen.

### 1.1 Project

| Field | Value |
|---|---|
| Name | Nelavista V2 |
| One-sentence purpose | A platform for African (Nigerian first) university students that takes a student from the lecture hall to paid work. |
| Product journey | Enrol -> Learn -> Build -> Verify -> Match -> Work -> Quality check -> Earn |
| Launch surfaces | Student web PWA at `apps/web` (port 5173); internal admin at `apps/admin` (port 5174). |
| Post-launch surface | Expo / React Native app at `apps/mobile`. The mobile app is not part of the web launch. |
| Public promise | Learn it. Prove it. Get paid for it. |

### 1.2 Stack

| Area | Current choice | Notes |
|---|---|---|
| Framework | React 18.3.1 + Vite 5.4.11 | Web and admin. No Next.js, no SSR. |
| Language | TypeScript 5.6, `strict` and `noUncheckedIndexedAccess` | Mobile uses TypeScript 5.3 with Expo's base config. |
| Routing | React Router 6.28 in web; a small in-repo hash router in admin | Do not add React Router to admin without a concrete need. |
| Styling | Plain CSS plus CSS custom properties from `@nelavista/design-tokens` | Tailwind and CSS-in-JS are deliberately not in use yet. |
| Tokens | `packages/design-tokens/src/index.ts`; shared bridge in `packages/ui/src/theme.ts` | Both apps apply the same Ink/Paper tokens and import the shared CSS. |
| Shared React primitives | `packages/ui` exports the shared primitives, theme bridge, shared CSS and fonts; `apps/web/src/ui.tsx` is a re-export alias | Add a primitive to `packages/ui`; do not copy it between apps. |
| Tests | Vitest 2.1 + jsdom + React DOM | No Testing Library, axe, or Playwright yet. Add them when a component test needs them. |
| Mobile | Expo 52, React Native 0.76.5, Expo SQLite, secure store, notifications | Shares tokens, not web components. |

### 1.3 Brand and tokens

The approved palette is **Ink + Paper**: one token system with two designed
surfaces, not two brands. `docs/v2-ui/DESIGN-DIRECTION.md` holds the full values
and contrast checks; `packages/design-tokens/src/index.ts` is the only source the
code reads.

| Surface | Used for | Default |
|---|---|---|
| **Paper** | Public marketing, legal, long-form reading, printable transcript | Public pages |
| **Ink** | Student app, admin, auth side panels, dense data | Signed-in app and admin |

| Role group | Ink example | Paper example | Use |
|---|---|---|---|
| `bg` | `#0B0D0C` | `#F7F3E8` | Page background |
| `surface` / `surfaceRaised` / `surfaceSunken` | `#111411` / `#171B17` / `#080A09` | `#EFE9DB` / `#E4DCCB` / `#FBF8F0` | Panels, menus, wells |
| `border` / `borderStrong` | `#2E362E` / `#465246` | `#CFC5B2` / `#9D927E` | Hairlines and control boundaries |
| `text` / `textMuted` / `textSubtle` | `#F1EEE4` / `#A9B0A4` / `#737D72` | `#171712` / `#5E6258` / `#7E8277` | Body, secondary, metadata |
| `accent` / `accentStrong` / `accentContrast` | `#F06A3A` / `#D94E1F` / `#160B06` | `#B33A12` / `#8F2D0D` / `#FFF8F0` | Action, active nav, focus |
| `success` / `warning` / `danger` / `info` | `#3DD68C` / `#F5B942` / `#FF5D5D` / `#6FB7FF` | `#1F7A4D` / `#8A5A00` / `#B42318` / `#1D5F9E` | Status only |

**Rules for extending tokens:**

1. Add the token in `packages/design-tokens`, not in a component.
2. Publish it through the shared bridge (`packages/ui/src/theme.ts` and the CSS
   variable layer) so every app receives it.
3. Verify contrast against the surfaces it will be used on in **both** themes.
4. Remove the hard-coded value it replaces in the same pull request.
5. Do not add a third palette. If a dense admin table needs a quieter accent, add
   a named role; do not fork the palette.

**Theme rules:** no pure black or pure white; no auto-inversion; the accent is
re-mixed per surface so contrast holds; images are not tinted per theme. Public
pages respect `prefers-color-scheme` on a first visit; the signed-in app defaults
to Ink; the toggle persists.

### 1.4 Typography

Three self-hosted, subset families ship with the shared UI package:

| Role | Family | Use |
|---|---|---|
| Display / editorial | **Instrument Serif** (400, italic) | Public headings and one emphasized phrase; never whole paragraphs |
| UI / body | **Instrument Sans** (400-700) | App UI, forms, public body, dense tables |
| Data / metadata | **IBM Plex Mono** (400-600) | Course codes, dates, rates, stamps, ledger values, keyboard hints |

All three are open-source and self-hosted under
`packages/ui/src/fonts`; do not load them from a third-party CDN. Subset Latin,
use `font-display: swap`, preload only the display regular and the UI regular,
and keep the metric-compatible fallbacks declared in the token layer.

This is deliberately different from V1's Bricolage Grotesque / DM Sans /
JetBrains Mono trio. Do not carry those families into V2, and do not replace the
approved faces with Inter, Roboto, or Arial as an unexamined default.

The type scale is a 1.25 ratio published as tokens. Do not add arbitrary sizes
inside a feature; revise the scale as one token change with a visual review.

### 1.5 Shape and elevation

- Radius: `stamp` 2, `control` 4, `panel` 8, `dialog` 12, `pill` 999.
- Use 4 for buttons and inputs, 8 for panels, tables and drawers, 12 for dialogs.
  Pill is only for a filter or chip that is genuinely toggleable.
- The sharper radii are intentional: a 4px control and an 8px panel read as a
  working tool. Do not round every surface.
- No shadows by default. Dialogs and drawers may use one neutral shadow at
  10-12% opacity plus a scrim. Prefer borders and surface contrast.
- No glassmorphism, backdrop blur, glow, or colored shadow.

### 1.6 Users and context

| User | Context | Design consequence |
|---|---|---|
| Student | 18-25, Nigerian university, Android mid-range, 3G/4G, data-sensitive, shared device, one hand | Mobile-first, small payloads, large targets, resumable flows, clear offline and partial states, no API caching in the PWA. |
| Internal ops | Desktop, 1280px or wider, repeated all-day use, keyboard, audit-sensitive | Dense tables, sticky headers, filters in the URL/hash, bulk actions, inline editing, clear audit consequences. |
| Employer or talent viewer | Opens a shared profile, may be on mobile, may not have an account | Public proof must be readable without app chrome, with a clear "what this proves" explanation. |

- **Language:** English, Nigerian English. Use "enrol", "organisation", "programme" where the product already does. No RTL at launch, but use logical CSS properties (`inline-start`, `block-end`) so it is not a rewrite later.
- **Currency:** the API supplies an ISO currency and integer minor units. Default display locale is `en-NG` for NGN; otherwise use the user's locale. Never hard-code `₦` or divide money in the API.
- **Time:** default timezone is `Africa/Lagos`; display in the user's saved timezone when available. Store and transport ISO 8601 UTC. Use `Intl.DateTimeFormat`.
- **Devices:** 320px is the minimum supported width; 375px is the primary design width; 768px tablet; 1280px and 1440px desktop.
- **Connectivity:** assume the connection can disappear mid-action. The app shell works offline; API data is never cached because it can contain one student's work, earnings, or identity.

### 1.7 Screen inventory and anchors

The route contract is `docs/v2-ui/ROUTE-MAP.md`. Do not add a screen outside it
without updating that file first. The families are:

| Surface | Routes | Job |
|---|---|---|
| Public | `/`, `/features`, `/how-it-works`, `/about`, `/contact`, `/faq`, `/legal/privacy`, `/legal/terms`, `/legal/contributor-terms`, `/offline`, `*` | Explain the promise, answer objections, give a real 404 and offline state |
| Auth | `/signup`, `/login`, `/auth/verify`, `/auth/reset` | Complete authentication with a visible next step |
| Student app | `/home`, `/onboarding`, `/academia`, `/academia/materials`, `/academia/materials/:materialId`, `/academia/ask`, `/academia/cbt`, `/academia/cbt/history`, `/academia/courses/:courseCode`, `/campus` | Learn and practise |
| Student app | `/skills`, `/skills/:skillSlug`, `/skills/paths/:pathSlug`, `/skills/lessons/:lessonSlug`, `/skills/practice/:templateId`, `/skills/my-learning`, `/verification`, `/verification/assessments/:assessmentSlug`, `/verification/attempts/:attemptId`, `/verification/practical/:taskSlug`, `/transcript` | Build and prove |
| Student app | `/opportunities`, `/opportunities/:slug`, `/opportunities/applications`, `/work`, `/work/assignments/:assignmentId`, `/earnings`, `/talent` | Find, deliver and earn |
| Utility | `/notifications`, `/settings`, `/settings/security`, `/settings/notifications`, `/settings/data`, `/share/:token` | Keep the account safe and share proof |
| Admin | `#/overview`, `#/audit`, `#/imports`, `#/users`, `#/waitlist`, `#/opportunities`, `#/work`, `#/review`, `#/money`, `#/content`, `#/campus`, `#/platform`, `#/security` | Operate and configure |

Every screen gets one anchor. If a screen needs a different anchor, write the
reason in the pull request. Marketing pages are separate routes, never one long
page of `#section` anchors.

### 1.8 Real data shapes

Design with these shapes, not with "John Doe" and "Lorem ipsum".

- **Names:** `Chiamaka Okonkwo`, `Aisha Bello`, `Ifeanyi Nwosu`, `Oluwaseun Adeyemi-Balogun`. Test a 40-character name and a missing display name.
- **Institutions:** `University of Lagos`, `Ahmadu Bello University`, `Michael Okpara University of Agriculture, Umudike`. Test a 70-character institution.
- **Courses:** `CSC 301`, `GST 201`, `MTH 101`; titles up to 120 characters.
- **Money:** integer `amount_minor`, ISO `currency`. Examples: `0 NGN`, `₦12,500.00`, `₦1,250,000.00`. Test missing currency and a reversed line.
- **Dates:** ISO UTC from the API. Display `Due Fri 14 Nov, 23:59` in the user's timezone; show `No deadline` when null.
- **Statuses:** work `assigned`, `in_progress`, `submitted`, `approved`, `rework`, `rejected`; money `pending`, `payable`, `paid`, `reversed`, `on_hold`; verification `unverified`, `in_progress`, `verified`, `expired`.
- **Empty values:** `No courses yet.` plus one action; `No earnings yet. An approved task creates a line here with the rate and reason it was paid at.`; `Rate shared on the brief.`
- **Failure values:** a 404 from a feature flag is "not switched on for this environment", not "something went wrong"; a 401 is a session problem; a 500 is "try again" plus a support path.

### 1.9 Constraints

- **Accessibility:** WCAG 2.2 AA. Body text targets 7:1 contrast and never falls below 4.5:1. Focus indicators are at least 2px and 3:1 against their background. Touch targets are at least 44 by 44px, never below 24 by 24px. Full keyboard path for every task. Reduced motion, forced colors, and 200% zoom must work.
- **Performance:** web first-load budget is 150KB JavaScript gzip and 20KB CSS gzip, enforced by `pnpm check:web-budget`. Target LCP <= 2.5s, INP <= 200ms, CLS <= 0.1 on a mid-range mobile device over a slow connection.
- **Browser support:** last two versions of Chrome, Edge, Firefox, and Safari; Android Chrome is the primary mobile browser; iOS Safari is secondary.
- **Security:** no personal data or tokens in URLs; no secrets in logs; no `dangerouslySetInnerHTML` without a vetted sanitizer; keep the app compatible with a strict content security policy.
- **Offline:** the PWA shell is available offline. API responses are deliberately not cached. Queue a mutation offline only when the API supports an idempotency key and the UI can show pending, failed, and retry states.

### 1.10 Success criteria

Done means:

- A new student can sign up, finish onboarding, see the next action, open a lesson, and start practice on a 375px screen without horizontal scrolling.
- A keyboard-only admin can find the oldest pending review, open it, record a verdict, and see a confirmation without a mouse.
- Every data-driven screen has loading, empty, error, partial, stale, offline, and success states where those states can occur.
- The screen still works at 320px, at 200% text zoom, with reduced motion, and in forced-colors mode.
- The web first-load budget passes, the production build passes, and no new console errors appear.
- No copy contains a banned word and every button names its action.

### 1.11 Out of scope

- V1 UI changes, V1 templates, or V1 CSS.
- Mobile launch work; the mobile app is post-launch.
- A second design language for admin or a third surface theme. Ink and Paper are
  the only themes; do not auto-invert or invent a third palette.
- A Tailwind, CSS-in-JS, or component-kit migration as part of a feature.
- New backend endpoints, auth flows, or payment behavior invented by the UI.
- The newsletter and the platform announcement banner until they are approved
  with a backend and owner.
- Student material upload and PDF analysis. The replacement is curated materials,
  Ask, CBT and the transcript evidence trail; do not ship an upload affordance
  that cannot complete.

---

## 2. Non-negotiable rules for V2

This section is the generic framework's Section 1, tightened for Nelavista. Treat every "banned" item as a failure condition, not a preference.

### 2.1 Layout and spacing

**Banned**

- Section padding above 96px on desktop or 56px on mobile.
- Gaps above 24px between related elements.
- A hero that fills the whole viewport by default.
- Empty bands of space used to signal "premium".
- Content floating in the middle of a huge canvas.
- Uniform padding on everything, regardless of hierarchy.
- Centered body text, centered long forms, and centered everything. Center only short, single-purpose moments such as a final call to action, an auth form, or an empty state.
- Arbitrary pixel values that are not on the 4px scale.

**Required**

- One spacing scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96. Add the missing upper stops to tokens before using them.
- Proximity encodes meaning: label to field 6-8px, field to field 12-16px, group to group 24-32px, section to section 48-96px.
- The first screen shows real primary content and a usable action without scrolling.
- Align every edge to a consistent grid. If two elements are close but not aligned, fix the alignment rather than adding a border.
- Content widths:
  - Reading content: maximum 65 characters per line, roughly 680px.
  - Student application dashboards: 960-1200px.
  - Admin data surfaces: 1280-1440px.
  - Auth forms: 400-440px.
  - Mobile: full width with 16px gutters.
- Content widths are tokens: reading 680px, student app 1120px, admin 1360px, auth 420px. Do not use the reading width for every dashboard.
- Admin uses a 248px grouped sidebar; keep the content area fluid and let tables use the available width.

### 2.2 Cards, metrics, and dashboards

**Banned**

- A row of three or four identical rounded cards, each with an icon, a big number, and a label.
- Cards used only to group content that could sit under a heading and a hairline.
- Card inside card inside card. Maximum one level of surface nesting.
- Identical visual weight on every element, so nothing leads the eye.
- Placeholder metrics: numbers with no unit, period, comparison, or source.

**Required**

- A card is allowed only when it is a single object a person acts on or reads as a document: a plan, a receipt, a record, an assignment, a submission, a payout line.
- Everything else is a list, a table, a ruled row, a key-value row, a timeline, or plain content under a heading.
- Every metric shows its value, unit, period, and a comparison (change, benchmark, or trend). One primary metric per view is larger than the rest.
- Prefer dense, scannable structures: tables with sticky headers, ranked lists, inline sparklines, key-value rows, and timelines.
- Information hierarchy has at least three clearly different levels of emphasis on every screen, built from size, weight, color, and position together.
- Audit every `nv-card`: keep it for a record or an action panel; replace it with a heading, a ruled list, or a table for a group of content.

### 2.3 Color, gradients, and effects

**Banned**

- Neon glows, colored shadows, and glowing borders.
- Decorative gradients: hero washes, mesh gradients, aurora blobs, gradient text, gradient buttons, gradient borders.
- Glassmorphism and backdrop blur used as decoration.
- A second accent hue. Semantic status colors are the only exception.
- Multi-layer soft shadows stacked on every surface.
- Color as the only carrier of meaning.

**Permitted exceptions**

- A gradient is allowed only when it encodes data (a sequential scale in a chart or heatmap) or protects legibility (a scrim over a photograph).
- The skeleton shimmer is a functional loading indicator, not decoration. Keep it, but respect `prefers-reduced-motion`.
- The signal orange is a brand value. Keep it under about 10% of the visible surface and use it for interaction or importance only. It is re-mixed per theme so contrast holds; it is never a background wash.

**Required**

- One neutral ramp, one accent, and four semantic colors: success, warning, danger, info.
- Add the missing semantic and neutral roles as tokens before using them. Do not write raw hex in a component.
- Borders used as the only indicator of a control boundary must meet 3:1 against the adjacent surface. `--nv-border` is a hairline, not a control border; add `--nv-border-strong` for inputs and buttons.
- Focus is always visible: at least 2px, 3:1 against its background, with a 2px offset.
- Disabled states remain readable and explain why the action is blocked when the block is not obvious.
- Do not use `opacity` alone to create a disabled or muted state on text that must remain readable.

### 2.4 Typography

**Banned**

- Gray text on gray surfaces, light-weight text below 18px, thin fonts for body text, or any text under 4.5:1 contrast.
- More than two typefaces plus one monospace.
- Inter, Roboto, or Arial as an unexamined default.
- Headings and body that differ only slightly. Adjacent type levels must differ by at least 1.2 times in size or at least 200 in weight.
- ALL CAPS letter-spaced eyebrow labels above every heading.
- Proportional figures inside tables, prices, or counters.

**Required**

- A type scale with a ratio of 1.25, defined as tokens. Do not add a size inside a feature; revise the scale as one token change with a visual review.
- Base size 15px for applications, 16px for reading content, 14px for dense admin tables.
- Line height 1.1-1.2 for headings, 1.5-1.6 for body.
- Body text targets 7:1 contrast. Secondary text, placeholders, and disabled-but-readable text meet 4.5:1.
- Tabular numerals (`font-variant-numeric: tabular-nums`) for every aligned figure, price, count, and table column.
- A distinct, legible monospace for code, identifiers, and ledger-like values.
- Sentence case. Specific, plain copy. Mono metadata labels may be uppercase at 11-12px with 0.08em tracking; they are a data label, not a decorative eyebrow above every heading.

### 2.5 Decoration

**Banned**

- Meaningless decorative shapes: blobs, orbs, floating circles, abstract squiggles, background grids, dot matrices, noise textures, topography, hexagons, particles, and stars.
- Icons inside colored circles above headings.
- Stock photography and generic 3D illustrations.
- Emoji used as interface elements or bullet points.
- Fake social proof: invented logos, reviews, user counts, or statistics.
- Placeholder text of any kind: lorem ipsum, "Feature one", "Your text here".

**The decoration test:** every non-text visual element must do at least one of these jobs: encode data, aid navigation or orientation, signal state, or carry real content. If it does none of them, delete it.

Icons are allowed where they speed up scanning, but use one set, one stroke weight (1.5px typical), and always pair an icon-only control with an accessible name.

### 2.6 Functional visual anchors

- Every screen and component has exactly one dominant anchor: the primary metric, the primary action, or the primary piece of content.
- The anchor is established through size, weight, contrast, and position together, never by decoration.
- **Squint test:** when the screen is blurred, the anchor is still the first thing seen.
- One primary action per view. Secondary actions are quieter; tertiary actions are plain text.
- Anchors sit where the eye already goes: top left of the content area for reading; near the thumb zone for mobile primary actions.
- Navigation always shows where the person is. Use an active shape or weight change, not color alone.

### 2.7 Motion and micro-interactions

Every motion must answer a question: what changed, where did it come from, or what can I do next. Motion with no answer is removed.

**Rules**

- Animate only `transform` and `opacity` (and `filter` sparingly). Never animate `width`, `height`, `top`, `left`, `margin`, or `box-shadow` for movement.
- Durations: instant 90ms (press, toggle), fast 140ms (hover, focus, small reveal), base 200ms (menus, popovers), slow 280ms (dialogs, sheets, page-level). Nothing above 320ms unless it is a deliberate celebration moment.
- Easing: `cubic-bezier(0.22, 1, 0.36, 1)` for entrances; `cubic-bezier(0.4, 0, 1, 1)` for exits at 60-70% of the entrance duration. For physics-based motion use springs with stiffness 400-500, damping 30-40, mass 1. No bounce except in an intentional celebration.
- Origin: overlays scale and fade from the element that triggered them. Lists reorder with layout animation rather than jumping.
- Every animation is interruptible. A second click mid-animation redirects instead of queueing.
- Respect `prefers-reduced-motion` everywhere: replace movement with an instant or opacity-only change. No motion triggered by keyboard navigation.
- Stagger at most 6 items with at most 40ms between them. No looping idle animation, no scroll-triggered entrance fade on every section, no parallax, no hover lift on every card.
- Hover effects exist only where hover is meaningful and never carry required information. Touch devices have no hover.

**Required micro-interactions**

- **Buttons:** visible pressed state within 90ms; a loading state that keeps the button width; disabled state with a reason when it blocks the main path.
- **Inputs:** focus ring at least 2px and 3:1 contrast; validation on blur and on submit, never while the person is still typing the first time; inline error text tied to the field; success feedback only when useful.
- **Toggles, checkboxes, tabs:** the state change animates and is announced to assistive technology.
- **Async actions:** optimistic update with rollback and a clear message on failure; skeletons shaped like the real content; progress indication for anything over one second; a confirmation of completion.
- **Destructive actions:** confirmation that states the consequence in plain words, or an undo window when the action is reversible.
- **Copy, save, and submit:** confirm in place with a changed label for about 1.5 seconds before using a toast.
- **Counters and balances:** count to the new value rather than jumping, unless the value is a precise financial figure where animation would obscure the number.

### 2.8 Content density and states

**Required**

- Show real data shapes, realistic values, and realistic lengths: long names, large numbers, empty values, failure values. Design for the worst case, not the demo case.
- Offer density modes for data-heavy interfaces: compact (32px row), default (40px), comfortable (48px). Default to default, not comfortable.
- Prefer progressive disclosure: summary first, detail one interaction away.
- Provide keyboard shortcuts and a command palette for power-user applications, bulk actions on lists, inline editing where editing is frequent, and sticky headers on any table taller than the viewport.
- Every data-driven component implements all applicable states: loading, empty, error, partial, stale, offline, and success. An empty state has one sentence of explanation and one primary action.
- Microcopy is specific. Buttons name the action ("Save changes", not "Submit"). Errors say what happened and what to do.
- The feature-off state is first class. A 404 from a flag is "not switched on for this environment yet", not a scary error.

**Banned copy:** "Unlock", "Seamless", "Elevate", "Supercharge", "Revolutionize", "Empower", "Effortless", "Next-generation", and any sentence that would fit on any product.

**V2-specific copy rules**

- Use "student", "course", "material", "skill", "path", "proof", "opportunity", "assignment", "review", "earning", "payout".
- Say what the money means: "Waiting for review", "Ready to be paid", "Paid", "Reversed", "On hold".
- Say what the proof means: "Verified", "In progress", "Not started", "Expired".
- Do not imply a payment is guaranteed before review. Do not call a pending line "earned" if the API distinguishes it.

### 2.9 Data visualisation

- Chart only what a table cannot say faster.
- Label axes with units. Start bars at zero. Never use 3D, pie charts with more than four slices, dual y-axes without clear labeling, or truncated axes that exaggerate change.
- Use one primary data color, one comparison color (muted), and semantic color only for meaning.
- Direct-label lines and bars instead of using a legend when possible.
- Provide a table or text alternative for every chart, keyboard-reachable data points, and a tooltip that does not hide the data.
- Inline sparklines and small multiples are preferred over large single charts for dense dashboards.
- Money charts must show currency and period. Do not smooth a financial series in a way that hides a reversal or a gap.

---

## 3. Stack and library policy

### 3.1 Selection rules

1. Choose one library per category. Never combine two primitive libraries, two motion engines, or two chart libraries in one project unless the second covers a need the first cannot.
2. Prefer headless primitives plus local tokens over heavily styled kits, so the interface does not look like the kit's demo.
3. Check each candidate for accessibility record (WAI-ARIA Authoring Practices coverage), maintenance activity, license, bundle cost, TypeScript support, and SSR compatibility.
4. Tree-shake and lazy-load heavy packages (charts, editors, maps).
5. State the chosen stack and the reason for each choice in one line before writing code.
6. Confirm current versions and APIs from official documentation before using any package.

### 3.2 V2 choices

| Category | V2 choice | Reason | Status |
|---|---|---|---|
| Accessible primitives | Native HTML first; local primitives in `packages/ui`; Radix UI only when a widget needs full APG behavior | Native elements are the most reliable and cheapest; Radix is unstyled and well-tested when a dialog, menu, or combobox needs it | Native/local now; Radix not installed |
| Styling | CSS custom properties plus plain CSS | One token bridge already exists; no second styling system while the UI is being stabilised | In use |
| Styled kits | None | A kit's default theme would fight the brand and add bundle weight | Do not add without an ADR |
| Motion | CSS transitions; Motion for route-level and orchestration that CSS cannot express | CSS is sufficient for press, hover, reveal and reduced motion; Motion is used behind `prefers-reduced-motion` | CSS + Motion installed |
| Forms | Controlled React inputs; React Hook Form + Zod only when a form outgrows the current pattern | The existing forms are small; add a form library when validation and field arrays justify it | Controlled now |
| Tables | Semantic `<table>`; TanStack Table + Virtual only for large admin grids (roughly >100 rows) | Most tables are small; a table library is not worth the first-load cost until it is | Semantic now |
| Charts | Hand-built SVG + D3 scales for sparklines and small marks; Recharts lazy-loaded for standard dashboards | Keeps the first load small and the marks controllable | SVG now |
| Icons | Lucide | One consistent set, tree-shakeable, good accessibility defaults, no emoji | Installed |
| Dates | Native `Intl`; `date-fns` only if date arithmetic becomes complex | `Intl` covers formatting and relative time | `Intl` now |
| Server state | Existing `useApiResource` / `http`; TanStack Query only if caching and invalidation become the bottleneck | Avoid a second data layer before it is needed | Existing hooks |
| Client state | Local state and context; no Redux | The app is route-oriented and small | Existing context |
| Testing | Vitest + jsdom + React DOM; add Testing Library and axe when component tests need them | The current suite is route-level; component-level a11y tests are the next gap | Vitest now |

### 3.3 Do not add without a concrete need

- Next.js, Remix, or another framework.
- Tailwind, CSS-in-JS, styled-components, or a second CSS system.
- A styled component kit (MUI, Chakra, Mantine, HeroUI, shadcn as a default theme).
- A second motion engine (GSAP plus Motion, or Motion plus React Spring).
- A second chart library.
- An icon font, or two icon sets in one screen.
- Moment.js, axios, lodash as a default utility, or a state library for server data.
- A toast library before the native in-place confirmation pattern is exhausted.
- A command palette before there are enough commands to justify it.

### 3.4 Dependency review

Before adding a package, write one line in the pull request:

- What category it fills and what it replaces.
- Its gzip cost on the first load or the lazy chunk.
- Its accessibility record for the widget it provides.
- Its license and maintenance status.
- Why a native platform feature or the existing stack is not enough.

Then run `pnpm install`, commit the lockfile, and run the web budget. If the package is heavy, lazy-load it and prove the first-load budget still passes.

---

## 4. Architecture rules

### 4.1 Layers

Dependencies point downward only:

1. **Tokens:** colour, type, spacing, radius, elevation, motion, z-index, breakpoints, content widths. Three tiers: primitive values, semantic roles (`surface`, `text`, `border`, `accent`, `danger`), and component tokens.
2. **Primitives:** unstyled or lightly styled accessible building blocks. Native elements and local wrappers live here.
3. **Components:** styled, reusable pieces with variants (`Button`, `Field`, `Dialog`, `Tabs`, `Table`).
4. **Patterns:** composed pieces that solve one interaction problem (`DataTable` with filters, `ConfirmDialog`, `EmptyState`, `CommandPalette`, `Money`, `StatusBadge`).
5. **Features:** domain modules that combine patterns with data and logic.
6. **Pages:** thin composition of features only.

### 4.2 Component rules

- Composition over configuration: compound components and slots instead of a prop for every variation. Support an `asChild` or polymorphic pattern where an element must change.
- Separate behaviour from presentation: logic in hooks, rendering in components. No data fetching inside presentational components.
- Variants through a variants helper (class-variance-authority or equivalent) and data attributes, never through string concatenation scattered in markup.
- Support controlled and uncontrolled use for any stateful component.
- Forward refs, or accept the ref as a prop in current React, and spread remaining props onto the root element.
- Files stay under 300 lines and components under 150 lines. One responsibility per file. Co-locate styles, tests, and stories with the component when those exist.
- Strict TypeScript. No `any`, no unchecked casts. Model states as discriminated unions. Use exhaustive checks on switches. Validate all external data with a schema at the boundary.
- Avoid prop drilling past two levels. Use context or composition.
- Avoid barrel files that defeat tree shaking. Named exports only, except where a framework requires default exports.
- Use logical CSS properties (`inline-start`, `block-end`) so right-to-left layouts work later.
- Put every user-facing string behind an internationalization function when the app has one. Until then, keep copy in one place per screen so it can be extracted.

### 4.3 Current package map

| Path | What belongs there | What does not |
|---|---|---|
| `packages/design-tokens` | Primitive and semantic tokens; a CSS-variable bridge; no React | Components, app-specific colours |
| `packages/ui` | Cross-app React primitives, theme bridge, shared CSS and self-hosted fonts | Data fetching, route logic, mobile-only components |
| `apps/web/src/ui.tsx` | Re-export aliases so screens keep importing `../ui` | A second implementation or new local primitives |
| `apps/web/src/routes` | Page composition, feature hooks, route-level states | Reusable design-system primitives |
| `apps/admin/src/components` | Admin shell and admin-only patterns | A second palette or a second button system |
| `apps/mobile/src` | React Native screens, native patterns, offline queue | Web DOM components |

`packages/ui` is the shared design system for web and admin: tokens are consumed
through the theme bridge, primitives live in `components.tsx`, and shared CSS is
imported from `styles.css`. Add a component there when both apps need it; keep
admin-only composition in `apps/admin`. Do not fork a primitive into an app.

### 4.4 Data and state

- Server state belongs in the existing resource hooks (`useApiResource`, `useResource`) or the route's own effect. Do not add a cache library until duplicate requests, invalidation, and optimistic updates are a measured problem.
- Keep client state small and local. URL or hash state is preferred for filters, sort, search, and selected tabs so a link can reproduce the view.
- Model async state as a discriminated union (`loading`, `ready`, `empty`, `error`, `offline`, `unavailable`) rather than a set of booleans.
- Mutations are idempotent where the API supports it. On failure, keep the user's input, show what happened, and provide a retry path.
- Never hide a partial result behind a full-page spinner. Show the sections that loaded and mark the ones that did not.
- Do not cache authenticated API responses in the service worker. The app shell may be cached; the student's data may not.

### 4.5 Error handling

- Errors are specific, recoverable, and never expose internals. Say what happened and what to do.
- A feature-flag 404 is an "unavailable in this environment" state, not an error.
- A 401 sends the person to sign in and returns them to the attempted route.
- A 403 says the account does not have access and names the next step (use the student app, ask an admin, sign in with another account).
- A 500 says "We could not load this. Try again." and offers a retry; do not show a stack trace.
- A failed mutation keeps the form values and focuses the first error.
- Never use `dangerouslySetInnerHTML` without a vetted sanitizer.

---

## 5. Accessibility

V2 targets WCAG 2.2 AA.

### 5.1 Foundations

- Use native elements first: `button`, `a`, `input`, `select`, `textarea`, `dialog`, `details`.
- Add ARIA only where native semantics fall short, and follow the WAI-ARIA Authoring Practices pattern for the widget exactly.
- Every interactive element has an accessible name, a visible focus indicator, a keyboard path, and a target of at least 44 by 44px on touch (never below 24 by 24px).
- Dialogs trap focus, close on Escape, label themselves with `aria-labelledby`, and return focus to the trigger.
- Menus, listboxes, tabs, and comboboxes implement arrow-key navigation, Home and End, and typeahead where the pattern specifies it.
- Forms: visible labels, never placeholder-only; errors associated through `aria-describedby` with `aria-invalid`; required fields marked in text and programmatically; focus moves to the first error on failed submit; autocomplete attributes are present.
- Dynamic updates use polite live regions. Assertive is only for urgent errors.
- Loading states set `aria-busy`. Route changes move focus to the main heading and update the document title.
- Never convey meaning with color alone. Pair it with text, shape, or an icon with an accessible name.
- Landmarks (`header`, `nav`, `main`, `footer`), a skip link, a logical heading order, and one `h1` per page.
- Support `prefers-reduced-motion`, `prefers-color-scheme`, `prefers-contrast`, forced-colors mode, and 200% text zoom without loss of content or function.
- Provide text alternatives for every image, chart, and icon button. Mark decorative images as decorative.

### 5.2 Current accessibility gaps to fix

- Admin and student shells now set `document.title` and move focus to `main` on
  route change. Verify the focus move does not fight a form-level error focus.
- There is no automated axe check in CI. Add it when component-level tests land.
- Verify focus on every new link and shell nav item at 200% zoom and in
  forced-colors mode; the shared `:focus-visible` rule exists but each screen must
  be checked.
- `VersionSwitcher` still uses inline styles; replace them with tokens when it is
  touched.
- The new public pages and the admin overview need a keyboard and reduced-motion
  pass before launch.

### 5.3 Keyboard map

| Widget | Keys | Behaviour |
|---|---|---|
| Button | Enter, Space | Activates; pressed state within 90ms |
| Link | Enter | Follows; must look different from a button |
| Dialog | Escape, Tab, Shift+Tab | Escape closes; focus stays inside; returns to trigger |
| Menu | Arrow keys, Home, End, Enter, Escape, typeahead | Moves through items; Escape closes and returns focus |
| Tabs | Arrow keys, Home, End | Moves selection; focus follows the selected tab |
| Combobox | Arrow keys, Enter, Escape, typeahead | Opens, filters, selects, closes |
| Table | Tab, Arrow keys where interactive | Sticky header; sortable headers are buttons with `aria-sort` |
| Form | Tab, Shift+Tab, Enter | Submit from a text field; focus moves to first error |

---

## 6. Performance

- **Budgets:** web first load is 150KB JavaScript gzip and 20KB CSS gzip, enforced by `pnpm check:web-budget`. Admin is internal but still follows the same discipline; do not ship a chart library on its first load.
- **Core Web Vitals:** LCP <= 2.5s, INP <= 200ms, CLS <= 0.1 on a mid-range mobile device over a slow connection.
- Set width and height (or aspect ratio) on every image and media element. Lazy-load everything below the fold. Prioritize exactly one above-the-fold image.
- Split code by route. Lazy-load heavy components. Virtualize lists and tables beyond about 100 rows.
- Avoid layout thrashing. Memoize only after measuring.
- Self-host and subset fonts, with `font-display: swap` and metric-matched
  fallbacks. The three approved families are subset and shipped from
  `packages/ui/src/fonts`; do not add a fourth or load them from a CDN.
- State the bundle impact of every dependency you add.
- Keep the PWA shell offline-capable. Do not cache API responses; they can contain one student's work, earnings, or identity.
- Test on a throttled connection, not only on localhost.

---

## 7. Testing and verification

### 7.1 Commands

Run these before declaring a UI change finished:

```bash
pnpm --filter @nelavista/web --filter @nelavista/admin lint
pnpm --filter @nelavista/web --filter @nelavista/admin typecheck
pnpm --filter @nelavista/web test
pnpm --filter @nelavista/web --filter @nelavista/admin build
pnpm check:web-budget
pnpm format:check
```

For a mobile change:

```bash
pnpm --filter @nelavista/mobile typecheck
pnpm --filter @nelavista/mobile test
```

If a change touches the API contract, run the API tests as well. If a change touches V1, stop: this guide does not authorize V1 work, and V1 has its own test and template-link checks.

### 7.2 Test coverage

- Unit and interaction tests for every new component, covering keyboard behaviour and every state.
- Add Testing Library and `user-event` when the first component test needs them. Add `jest-axe` or `axe-core` at the same time and run it in CI.
- Test the worst-case data: long names, zero and seven-figure amounts, missing currency, missing deadline, partial response, offline, 401, 403, 404 feature-off, 500.
- Test the route-level states that already exist (`loading`, `offline`, `error`, `unavailable`) so a redesign does not remove them.
- Do not rely on snapshot-only tests for visual quality. Use them for stable markup, not for judgment.

### 7.3 Visual checks

Capture screenshots at:

- 375px wide (primary mobile)
- 768px wide (tablet)
- 1280px wide (desktop)
- 320px wide for the worst-case mobile check
- 200% text zoom for the overflow check

Check both themes where the surface supports them: Ink for the app and admin,
Paper for public, legal and reading. The toggle must persist, and the public
first visit respects `prefers-color-scheme`. Check forced-colors mode separately.

### 7.4 Definition of done

- The screen has one anchor and passes the squint test.
- Every data state is implemented and tested.
- Keyboard-only use completes the task.
- No horizontal scroll at 320px or 200% zoom.
- Focus is visible on every interactive element.
- Contrast passes on the actual tokens.
- Reduced motion is respected.
- The copy has no banned words and every button names its action.
- The production build and first-load budget pass.
- The guide and the code do not disagree.

---

## 8. Surface playbooks

### 8.1 Student web

- Design at 375px first, then widen. The primary action sits in the thumb zone.
- The signed-in app uses a grouped left rail on desktop and a compact top bar
  with a mobile sheet below 768px. The groups follow the journey, not a flat list
  of twelve links: Home, Learn, Prove, Work, Account. Keep the version switcher
  out of the primary task path.
- Use a persistent bottom bar on mobile only if it does not cover content;
  otherwise use the compact top bar and the sheet.
- Reading screens: 65-character measure, 18px body, 1.6 line height, progress, previous/next, and a clear completion action.
- Practice and assessment screens: one question at a time, timer visible but not alarming, save on every answer, resume after a drop, confirm before submitting.
- Work screens: deadline, brief, rubric, submit, and review status in that order. Do not bury the deadline.
- Earnings: one primary balance, then the lines that explain it. Each line shows project, task count, rate, status, and reason. Never show a total that the lines cannot reproduce.
- Opportunities: rate, currency, effort, deadline, and fit come before the description. "Rate shared on the brief" is a valid state; do not invent a number.
- Empty states name the next action. "No courses yet" is not enough; add "Add your courses" or "Browse materials".

### 8.2 Admin

- Desktop-first, 1280px and wider. The 248px grouped sidebar is the navigation;
  the content area uses the remaining width and tops out at 1360px.
- Use tables, not card grids, for queues and records. Sticky headers on any table taller than the viewport.
- Filters, sort, search, and selected tab live in the hash route so a link reproduces the view.
- Provide density modes: compact 32px, default 40px, comfortable 48px. Default to 40px.
- Bulk actions are explicit and reversible where possible. A destructive action states the consequence and requires confirmation.
- Inline editing only where the field is frequently changed and the audit trail is clear.
- Money screens show the ledger reason, not just the amount. A payout exception must show what is wrong and what the reviewer can do.
- Review screens show the submission exactly as the student sent it, the rubric, the automatic result, and the override reason field. An override requires a reason.
- Status tags pair color with text. Do not rely on a colored dot alone.
- The overview is a live read of existing queues, not invented metrics. If one
  read fails, the rest of the screen still renders and the failed row says so.
- Campus can publish but cannot list yet. Say that plainly and show the write
  receipt; do not fake a published list.
- Admin route changes move focus to the new `h1` and update the title.

### 8.3 Mobile (post-launch)

- Use native patterns: stack navigation, safe areas, 44pt targets, native alerts for destructive confirmation, and platform-appropriate date pickers.
- Reuse tokens, not web components. The mobile UI is not a responsive copy of the web DOM.
- Offline is a first-class state: queue mutations with idempotency keys, show pending/failed/retry, and never show a stale balance as current.
- Push notifications must be useful and specific: "Your submission was approved" is useful; "You have a notification" is not.
- Test on a small Android device and a large iPhone, not only in the simulator.

### 8.4 Authentication

- Auth forms are 400-440px wide, single column, and centered because they are a single-purpose moment.
- Visible labels, autocomplete attributes, show/hide password, inline errors, and a loading state that keeps the button width.
- Explain the next step after signup: verify email, complete onboarding, or sign in.
- Admin 2FA is enforced. The enrollment screen explains why it exists and what happens next.
- No fake social proof, no stock photo, no giant hero. The form is the anchor.

---

## 9. Current state and gaps

The design system, public pages, auth, app shell, student utility screens and
admin shell are built. This is the remaining work, in the order that unblocks the
most.

| Area | Current state | Remaining |
|---|---|---|
| Tokens | Ink + Paper palettes, type, spacing, radius, motion, z-index, breakpoints and layout widths live in `packages/design-tokens` and are published through the shared bridge | Keep the values and the guide in sync; verify contrast in both themes |
| Primitives | Buttons, fields, textarea, select, checkbox, cards, panels, page headers, badges, stamps, banners, empty/error states, skeletons, spinner, avatar, theme toggle in `packages/ui` | Add a dialog/menu only when a real screen needs one |
| Public pages | Landing, Features, How it works, About, Contact, FAQ, Privacy, Terms, Contributor terms, NotFound, Offline | Replace draft legal copy after counsel review; add the image assets named in `docs/v2-ui/IMAGE-PROMPTS.md` |
| Auth | Login, Signup, Verify email, Reset password use the shared auth layout | Confirm the signed-in change-password endpoint before wiring it |
| Student app | App shell, Home, Academia, Materials, Ask, CBT, CBT history, Course, Skills, My learning, Verification, Transcript, Opportunities, Applications, Work, Earnings, Talent, Campus, Notifications, Settings subroutes | Add the missing course/topic detail and CBT review endpoints; wire change-password when it exists |
| Admin | Grouped shell, Overview, Audit, Waitlist, Campus, Imports, Users, Opportunities, Projects, Review, Money, Content, Platform, Security, 404 | Move the remaining admin screens (Opportunities, Projects, Review, Money, Content, Platform) to the shared primitives; add campus read and the missing admin actions |
| States | New screens implement loading, empty, error and success; feature-off is a distinct state | Audit the older admin screens against the state checklist; add partial/stale/offline where they can occur |
| Themes | Ink and Paper are both designed; the toggle persists; public first visit respects `prefers-color-scheme` | Verify every screen in both themes, forced colors and 200% zoom |
| Typography | Instrument Sans, Instrument Serif and IBM Plex Mono are self-hosted and subset | Keep the fallback metrics and preloads correct |
| Motion | Shared durations/easing and Motion route transitions; reduced-motion rules exist | Test every animation with `prefers-reduced-motion` |
| Tests | Web route tests, the public-route suite and the admin sign-in test pass | Add theme persistence and admin unknown-hash tests; add Testing Library and axe with the first component test |
| Accessibility | Skip links, landmarks, shared focus styles, labelled forms, route-change focus and document titles in both shells | Sentence-case table headers and a full keyboard/zoom pass |

### 9.1 Next UI tasks

1. **Finish admin.** Move the remaining admin screens (Opportunities, Projects,
   Review, Money, Content, Platform) to the shared primitives and keep
   Overview/Waitlist/Campus honest about missing reads.
2. **Responsive and accessibility QA.** 320px, 375px, 768px, 1280px, 200% zoom,
   keyboard-only, forced colors and reduced motion across both themes.
3. **Tests.** Theme persistence, the admin unknown-hash 404 and the remaining
   state transitions.
4. **Assets and content.** Create the images named in `docs/v2-ui/IMAGE-PROMPTS.md`
   and collect the missing business copy under “Needs my input”; do not invent it.

---

## 10. Screen brief template

Copy this into the pull request or the design note before building a screen.

```text
PROJECT
Name: Nelavista V2
Surface: web / admin / mobile
Route or component:
Job it must do (one sentence):
Primary anchor (metric, action, or content):

DATA
Fields and types:
Realistic values (including worst-case lengths):
Empty value:
Failure values:
Currency and timezone:
Permission or feature-flag states:

STATES
Loading:
Empty:
Error:
Partial:
Stale:
Offline:
Success:
Feature unavailable:

INTERACTIONS
Primary action:
Secondary actions:
Keyboard path:
Bulk actions:
Inline editing:
Destructive actions and confirmation:
Optimistic updates and rollback:

LAYOUT AND DENSITY
Width target:
Density (compact / default / comfortable):
Mobile behaviour:
Reading measure (if prose):

MOTION
Allowed (none / minimal / specific moments):
Reduced-motion alternative:

CONSTRAINTS
Accessibility level: WCAG 2.2 AA
Performance budget:
Browser support:
Security or privacy notes:

SUCCESS CRITERIA
Done means:
Out of scope:
```

Before coding, answer these five questions:

1. What is the one thing the person must be able to do on this screen?
2. What is the worst realistic data that will break the layout?
3. What does the screen show while loading, with no data, after a failure, and offline?
4. What is the keyboard path through the primary task?
5. What will be removed from the screen to make the anchor obvious?

---

## 11. Self-audit

Run this before delivery. A single fail blocks the change.

| # | Check | Evidence |
|---|---|---|
| 1 | No section or group gap exceeds the spacing limits in 2.1 | List the largest gaps and their tokens |
| 2 | Every edge aligns to the grid | Screenshot at 375, 768, 1280; note the grid |
| 3 | No identical-card grid, no card inside a card, and every card meets the card definition | Name each card and its object/action |
| 4 | Every metric shows value, unit, period, and comparison | List each metric and its four parts |
| 5 | No decorative gradient, glow, blur, background pattern, or meaningless shape | Screenshot and element inventory |
| 6 | Every non-text visual passes the decoration test | State the job of each icon, chart, and image |
| 7 | Text contrast meets 4.5:1 everywhere, and body text targets 7:1 | Contrast results for the actual tokens |
| 8 | Type scale, weights, and tabular numerals follow 2.4 | List the sizes and weights used |
| 9 | The screen has exactly one dominant anchor and passes the squint test | Blurred screenshot and the anchor named |
| 10 | Every motion answers a question, uses only transform/opacity, stays within duration limits, and respects reduced motion | List each animation and its duration/easing |
| 11 | Every async and data-driven element has all applicable states | State matrix from the brief |
| 12 | Every interactive element has an accessible name, focus indicator, keyboard path, and adequate target | Keyboard walkthrough and target sizes |
| 13 | No placeholder, ellipsis, TODO, abbreviation, or unexplained shorthand remains | Search the diff |
| 14 | Every library API used was verified, and every dependency is justified with its bundle cost | Dependency review line |
| 15 | Tests, lint, type checks, and the production build pass | Command output |
| 16 | Copy contains none of the banned words and every button names its action | Copy inventory |

---

## 12. Change log

- **2026-10-27:** Created from the master UI/UX framework and filled with the V2 project brief, current tokens, stack reality, screen anchors, gaps, and verification commands.
