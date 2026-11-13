# UI audit and redesign plan

Reviewed against [`UI-REFERENCE.md`](./UI-REFERENCE.md). Scope: the public site (`apps/web`), the signed-in student shell and dashboard, and the shared component layer (`packages/ui`, `packages/design-tokens`). Admin and mobile inherit the same token and component decisions; they are called out where their structure differs.

## What is already strong

- A real token system: semantic colour per theme, spacing/radius/type/motion/z-index scales, and a CSS bridge shared by web and admin.
- A distinctive type pairing: Instrument Serif display, Instrument Sans UI, IBM Plex Mono for record data.
- The landing hero has a genuinely product-specific object: the illustrative record card (verified skill → work order → quality check → payout).
- The app shell has grouped sidebar navigation, a persistent top bar, a skip link, focus handling on route change, and a reduced-motion page transition.
- Copy is concrete. There are no fake metrics or testimonials; the impact section explicitly refuses them.

## Findings

### 1. Landing: the composition repeats one skeleton

- Hero → section head + 3 rows → section head + 4 rows → 2-column + card → card → CTA band.
- Five of six chapters open with an uppercase mono eyebrow ("The problem", "One chain", "Two ways in", "What stays with you", "Impact"). That is the reference's most explicit anti-pattern, and it flattens hierarchy: every chapter announces itself the same way.
- The problem list (01/02/03) and proof chain (01/02/03/04) are both full-width numbered ledgers. The numbers are meaningful on the chain, not on the problems. The two sections read as the same component with different copy.
- The two ways in section uses two equal `nv-home-next` cards; the "what stays with you" card is the same quiet surface, so nothing marks it as the thing you keep.
- The impact section is a card with an eyebrow and a badge icon — the most generic region on the page.
- Every chapter is wrapped in `Reveal` (fade + slide on scroll), so motion is ambient rather than meaningful.
- The hero is essentially 50/50 (`.nv-hero` 1.05fr / 0.95fr), so the statement and the record object compete.

### 2. Dashboard: no summary, no primary region

- `Home.tsx` is a vertical stack: page header → "Your space" panel → email banner → "Your next step" panel → "Your courses" panel → footer row.
- The page header says "What to do next" and then the *space switcher* comes first. The actual next action is third.
- There is no at-a-glance summary of the student's real state (courses enrolled, semester, chosen space, setup status), even though `OnboardingState` already carries all of it.
- "Your next step" and "Your courses" have equal visual weight; the working view (courses) is the last panel.
- The space switcher is a 2×2 grid of equal options, so it reads as the main content rather than a context switch.
- Loading and error states replace one panel with a skeleton/error but leave the rest of the page looking complete, which misrepresents the state.

### 3. Mobile shell: two headers and six destinations

- At ≤860px the app shows `.nv-mobile-bar` (brand + theme + notifications + avatar) **and** `.nv-topbar` (breadcrumb + the same actions). That is duplicate chrome and two competing headers.
- `.nv-mobile-nav` is a horizontal, scrollable pill row with six items (Home, Academia, Skills, Work, Earnings, Settings). The reference's mobile pattern is a stable bottom bar with 3–5 destinations and one unambiguous active state.
- Settings has three entry points on mobile (bottom nav, avatar, header). Notifications has two.

### 4. Component layer

- `Panel` and `Card` share one anatomy and one radius. There is no inverted/featured surface, so "this is different" can only be said with a badge.
- `nv-space-option` is a well-built control but only reads correctly in a 2×2 grid; in a rail it needs a vertical variant.
- Table rows are readable, but numbers are not tabular by default.
- No `prefers-contrast` handling.

## Design plan

### Landing

**Concept.** An editorial ledger. The page alternates between *statement* (large serif, lots of air) and *record* (hairline-ruled rows, mono metadata). The hero is the single loud moment; every later chapter lowers its voice.

- **Focal point:** the hero headline, then the record card. Everything else is quiet.
- **Grid:** 12-column container. Hero is asymmetric 7/5 with the record card offset slightly below the headline baseline and allowed to hang past the media column's right edge. Chapters use three different skeletons: split statement + ruled faults, a horizontal four-node chain, and an asymmetric split with one inverted panel.
- **Type roles:** display (clamp 3–5rem serif, italic only on "Get paid for it"), chapter titles (serif, 2–3.4rem), body (15–18px sans, 60–70ch), record data (mono 12–13px). One eyebrow total, in the hero.
- **Spacing:** `--nv-space-7xl` hero top, `--nv-space-6xl` between chapters, `--nv-space-xxl` heading-to-content, `--nv-space-lg` inside rows.
- **Radius and depth:** hairline borders and tonal steps; one inverted panel; no shadows.
- **Signature moment:** the record card overlapping the hero media edge, with the italic payout line in the headline.
- **Motion:** one orchestrated hero reveal (copy, then media 80ms later). No scroll reveals after the hero. Reduced motion removes all of it.

```
┌──────────────────────────────────────────────────────────────┐
│  nav: brand            links            [Sign in] [Create]   │
├──────────────────────────────────────────────────────────────┤
│  THE WORKING RECORD                                          │
│  Learn it.                                                   │
│  Prove it.                          ┌──────────────────────┐ │
│  Get paid for it.                   │ record: verified     │ │
│                                     │ skill / order / QC / │ │
│  lede ............................  │ payout (illustrative)│ │
│  [Create account] [How it works]    └──────────────────────┘ │
│  ── facts ── facts ── facts ──                              │ │
├──────────────────────────────────────────────────────────────┤
│  Your CV says you can.        │ Scattered learning      ─── │
│  Your record should show it.  │ Self-reported proof     ─── │
│  (sticky statement)           │ Untrustworthy work      ─── │
├──────────────────────────────────────────────────────────────┤
│  From a topic to a receipt.                                  │
│  ①────────②────────③────────④   (horizontal chain)          │
├──────────────────────────────────────────────────────────────┤
│  Start with your course       │ ┌─────────────────────────┐ │
│  or your skill.               │ │ INVERTED: what stays    │ │
│  01 Academia  ───────────     │ │ verification, work,     │ │
│  02 Skills    ───────────     │ │ earnings, transcript    │ │
│                               │ └─────────────────────────┘ │
├──────────────────────────────────────────────────────────────┤
│  "A record we can stand behind."   (statement, no card)      │
├──────────────────────────────────────────────────────────────┤
│  Your next step should be obvious.        [Create account]   │
└──────────────────────────────────────────────────────────────┘
```

### Dashboard

**Concept.** A workspace, not a welcome page. The greeting orients; the summary strip reports; the primary column holds the next action and the working view; the rail holds the space switch and account context.

- **Focal point:** the next action. If setup is incomplete, that panel dominates and the courses table moves below it. If ready, the primary CTA sits inside the summary strip's "Next" cell and the courses table becomes the largest region.
- **Summary strip:** four real values from `OnboardingState` — courses enrolled, current semester, chosen space, setup status. No deltas are invented; the context line says what the value means ("0 enrolled · add during onboarding").
- **Primary working view:** courses table, full width of the primary column, with sticky header and tabular numerals.
- **Actionable queue:** the email-verification banner and the next-step panel sit above the table in the primary column, not in a separate stack.
- **Rail:** space switcher as a vertical list with the selected item inverted, then account/refresh meta. On mobile the rail moves below the primary column.
- **Spacing:** `--nv-space-xxl` between the header, summary, and grid; `--nv-space-xl` inside panels.
- **Motion:** the existing page transition is the only entrance. The selected space indicator changes tone instantly; no layout animation.

```
┌──────────────────────────────────────────────────────────────┐
│ Good to see you, Ada.                    [Academia badge]     │
│ 2025/2026 · First semester                                   │
├───────────────┬───────────────┬───────────────┬──────────────┤
│ COURSES       │ SEMESTER      │ SPACE         │ NEXT         │
│ 3 enrolled    │ 2025/2026     │ Academia      │ Ready        │
├───────────────────────────────────────────┬──────────────────┤
│ ┌─ Your next step ──────────────────────┐ │ SPACE            │
│ │ Open your Academia dashboard          │ │ ● Academia       │
│ │ [Open Academia →] [Materials]         │ │ ○ Skills         │
│ └───────────────────────────────────────┘ │ ○ Opportunities  │
│ ┌─ Your courses ────────────────────────┐ │ ○ Campus         │
│ │ Code  Course  Department  Status      │ ├──────────────────┤
│ │ ...   ...     ...         ...         │ │ Signed in as ... │
│ └───────────────────────────────────────┘ │ [Refresh]        │
└───────────────────────────────────────────┴──────────────────┘
```

### Mobile shell

- One header: brand on the left; theme, notifications, avatar on the right. The breadcrumb top bar is hidden below 860px.
- Bottom navigation, five items: Home, Academia, Skills, Work, Earnings. Active item gets a filled pill plus label; inactive items are outline icons. Settings stays in the avatar.
- Content gets bottom padding equal to the bar height plus the safe-area inset.

## Rollout

1. `docs/design/UI-REFERENCE.md` — the shared reference.
2. `docs/design/AUDIT-AND-PLAN.md` — this document.
3. Landing recomposition (`Landing.tsx`, `apps/web/src/styles.css`).
4. Dashboard workspace (`Home.tsx`, `apps/web/src/styles.css`).
5. Mobile shell (`AppShell.tsx`, `packages/ui/src/styles.css`).
6. Shared surfaces: inverted panel, rail variant of the space switcher, tabular numerals, contrast media query.
7. Verify: unit tests, typecheck, build, then a visual pass at 360/390/768/1024/1440.

## Deliberately not changed

- The token values and brand palette. The reference is palette-agnostic; the existing light/dark semantic tokens already meet AA on the checked pairs.
- The landing hero copy and the illustrative record. They are specific and honest, and the record card is the page's signature object.
- The impact section's refusal to publish unverified numbers. The redesign makes it a statement instead of a card; the claim stays.
- Admin layouts. They use the same shell and tokens; the inverted surface and rail variants are opt-in.
