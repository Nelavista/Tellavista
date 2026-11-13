# UI Design Reference for AI Coding Agents

A reusable reference for making interface decisions. It is not a spec for one product. Read it before designing or restyling any UI, then apply it to the project at hand.

The reference screens behind this file (marketing pages, dashboards, mobile apps, before/after redesigns, mobile header patterns) are evidence of *qualities*, not templates. Extract the principles. Never reproduce a layout, copy, or a distinctive component one-for-one.

This file deliberately says nothing about specific colours, palettes, brands, or design systems. Choose those per project, from the project's subject and audience. Everything here is about structure, rhythm, proportion, type, components, depth, and motion, so it holds under any palette.

---

## 0. How to use this file

1. **Understand the subject first.** Who uses this, what is the one job of this screen, what does the domain look and feel like (its objects, vocabulary, materials)? Distinctive decisions come from the subject, not from a house style you carry everywhere.
2. **Write a short design plan before code.** One paragraph each: layout concept, type roles, spacing scale, radius/border/depth logic, one signature moment, motion plan. Add an ASCII wireframe of each key screen.
3. **Review the plan against the defaults in section 13.** If any part is what you'd produce for any similar brief, change it and say what you changed.
4. **Build with tokens** (section 11), not ad-hoc values.
5. **Critique at the end.** Squint test, keyboard test, mobile test, then remove one decorative element.

---

## 1. What the reference screens have in common

Studying the set, the strongest work shares these traits. Treat them as the quality bar.

- **A clear first read.** In every screen you know in under a second where to look: one dominant element (a headline, a hero panel, a primary KPI, a featured card), then a clear second tier, then quiet support content.
- **Composition built from unequal parts.** Panels differ in size, weight, and density. Large next to small, dense next to airy, filled next to outlined. Nothing is a row of identical siblings.
- **Containers are used as information.** A tinted surface, a heavy outline, a stacked-card edge, or an inverted (high-contrast) panel marks *why* something is different (featured, in-progress, urgent, personal), not just decoration.
- **Disciplined component families.** Chips, pills, avatars, progress bars, and buttons repeat across the screen with the same anatomy, so the interface feels authored rather than assembled.
- **Generous, rhythmic spacing.** Tight inside components, loose between groups. Whitespace is used to separate ideas, not to fill a template.
- **Typography does real work.** Large light-to-regular display type, small quiet metadata, tabular numerals for data, and occasionally one deliberate contrast of styles (e.g. a roman/italic or sans/serif pairing) used as a signature rather than a habit.
- **Shape language with a point of view.** Pills, notched or "merged" shapes, cutout corners, overlapping elements, and mixed radii by hierarchy. The shape vocabulary is chosen, consistent, and recognisable.
- **Depth is restrained.** Layering comes from overlap, stacked edges, tonal steps, and borders more often than from heavy shadows.
- **Real, specific content.** Concrete labels, plausible names, real units, real states. The designs feel like products because the content is specific.
- **Before/after lessons.** The redesigns improve by *removing* chrome, consolidating controls, enlarging touch targets, clarifying the active state, simplifying the header, and giving the key action one obvious home.

---

## 2. Visual hierarchy

Hierarchy is the first design decision on every screen. Establish it deliberately.

**Rules**
- Each view has **one primary focal point**, **a few secondary elements**, and the rest recede. If you can't name the focal point, the design isn't done.
- Create hierarchy with several levers together: size, weight, tone/contrast, position, whitespace, and container treatment. Size alone is a blunt tool.
- Use **at most three emphasis levels** in any region (primary, secondary, tertiary). More than that reads as noise.
- **Contrast of scale** is the cheapest way to look intentional: a large display number or headline against small, quiet supporting text. Avoid mid-size everything.
- **One loud thing per viewport.** If a hero, a stat strip, a promo banner, and a CTA all shout, none of them are heard.
- De-emphasise through tone and weight before you delete. Metadata, timestamps, and helper text should be visibly quieter than the data they describe.
- Group by proximity first. Use dividers, borders, or containers only when proximity alone isn't enough.
- The primary action is unmistakable. Secondary actions are visibly lower in emphasis (outlined, ghost, or text). Never give three actions equal weight.

**Test:** blur or squint at a screenshot. You should still see a clear order of importance, a clear grouping, and an obvious primary action.

---

## 3. Layout and composition

### Build compositions, not stacks of sections

Avoid the default of "full-width section, centred heading, three equal cards, repeat." Instead, choose a layout concept for the page and let regions vary.

**Layout moves worth using (pick what fits the content):**
- **Asymmetric split:** a dominant region (about 60 to 70%) beside a supporting region, rather than 50/50.
- **Modular/bento composition:** a grid with deliberately mixed spans (1x1, 2x1, 1x2, 2x2) where the *content importance* decides the size. Keep the gutter constant and let sizes carry the variety. Don't mix more than a few distinct tile sizes.
- **Shell + content:** persistent navigation (sidebar, rail, or top bar) framing a content area, with the content area itself containing a strong top-level summary, then primary working area, then secondary panels.
- **Overlap and bleed:** let one element break its container, overlap a neighbour, or bleed to an edge (a floating card over a hero panel, an image running off the frame, a stacked card peeking out behind another). Use once or twice per screen, with intent.
- **Contained "stage":** an inset framed canvas inside the page background, so the product reads as an object with its own edges.
- **Dense/airy contrast:** place a dense data region next to an open, sparsely populated one so each makes the other legible.
- **Left-aligned reading axis:** most text and controls share a strong left edge. Centre only short, ceremonial content (a hero line, an empty state), not whole pages.

### Rules of composition
- Establish a **grid** (12 columns on wide screens is a common default) and a **baseline rhythm**. Align edges. Elements that are not aligned should be *obviously* different, not accidentally off by a few pixels.
- Use **optical alignment** where geometry misleads: icons inside circles, text next to icons, large type's side bearings.
- Keep **consistent outer margins** and **consistent gutters** across a page. Change density through content, not through random spacing.
- Prefer **fewer, larger, more meaningful regions** over many small boxes. A screen with 4 to 6 clear regions beats one with 14 tiles.
- Don't give every region a container. Content can sit directly on the page surface; reserve containers for things that need to be grouped, elevated, or marked as different.
- Avoid symmetrical decoration for its own sake. Balance can be asymmetric (a heavy left, a light right) and still feel stable.

### Marketing / landing pages
- Open with the **most characteristic thing in the subject's world**: a strong statement, a product view, a live or interactive moment, a distinctive image. Choose the form deliberately; a big number with a small label and an accent glow is the default, not the best.
- Vary section *structure*, not just content: a statement band, a split with a product view, a modular proof area, a dense comparison table, a quiet FAQ. No two consecutive sections should share the same skeleton.
- Make section transitions meaningful: a change in surface, scale, or density, not just more padding.
- Social proof, pricing, and comparison content should each be formatted for what they are (a logo row, a quote with a face, a real table), not forced into the same card.
- Keep navigation simple and the primary call to action visible at all times.

### Dashboards / product UI
- Lead with a **summary strip** of key figures, but make it earn its place: 3 to 6 indicators, one of which may be emphasised as the headline metric. Include the *delta or context* (change, period), not just the value.
- Follow with the **primary working view** (pipeline, board, schedule, activity, table), giving it the largest area.
- Place **actionable queues** ("needs review", "due today", "waiting") beside or below, since they answer "what do I do next?"
- Use a persistent **navigation rail or sidebar** with grouped sections, counts for items that have them, and one clearly active item. Put the account/profile switch at the bottom, workspace switch at the top.
- Greet or orient the user (a short, human line with their name and context) when it helps, then get out of the way.
- Show real density where users need it. Don't spread six numbers across a screen just to fill space, and don't cram a screen where scanning is the job.
- A different visualisation for different data. A heatmap, a pipeline funnel, a timeline, a stacked bar, a progress track, and a board each answer different questions. Don't reach for a generic line chart by default.

### Mobile
- **One primary column.** Use a clear top region (location/greeting, profile, notifications), a prominent search or primary action, then content modules in a consistent rhythm.
- **Consolidate controls.** Several rows of filters/tabs/sort buttons become one search field with a single filter entry point and a compact segmented control.
- **Bottom navigation** with 3 to 5 destinations, a clearly emphasised active state (a filled pill or filled icon plus label), and comfortable touch targets. A floating, pill-shaped bar with a prominent central action is a valid pattern when there is a real primary "create" action.
- **Horizontal carousels** for browsing homogeneous items, with the next card peeking in to signal scroll.
- Respect safe areas (status bar, home indicator). Content should never sit under system UI.
- Use **sticky, minimal headers**. Simplify to a leading control, a central identity/title, and at most two trailing actions (see the header notes in section 7).

---

## 4. Spacing, alignment, and proportion

**Scale.** Use one spacing scale based on a small base unit (4px or 8px steps: 4, 8, 12, 16, 24, 32, 48, 64, 96). Never invent one-off values like 13px or 37px. Spacing is a vocabulary; keep it small.

**Principles**
- **Inside < between < around.** Padding inside a component is smaller than the gap between sibling components, which is smaller than the gap between groups or sections. This single rule creates most of the perceived order in a screen.
- **Padding scales with container size.** A small chip: 4 to 8px vertical. A card: 16 to 24px. A hero panel: 32 to 64px. Large containers with tiny padding look cramped; small ones with huge padding look empty.
- **Consistent gutters** inside a grid. Don't vary gap between cards in the same grid.
- **Whitespace is a tool for emphasis.** Isolating an element gives it importance. Use it for the focal point, tighten it for related details.
- **Vertical rhythm.** Keep section spacing on the scale and repeat it. A recognisable rhythm (e.g. generous gap above a section heading, small gap below it) makes content scannable.
- **Proportion.** Prefer a few intentional ratios (e.g. 2:1, 3:2, 1:1, 16:9, 4:5) for media and tiles and reuse them. Avoid arbitrary aspect ratios per card.
- **Touch targets** are at least about 44px square on touch devices, with adequate space between them.
- **Line length.** Body copy at 45 to 75 characters per line (use `ch` units for max-width). Serif body benefits from slightly more line-height than sans.
- **Align to shared edges.** Labels, values, and actions in sibling cards should line up across cards (consistent internal layout), so the eye can scan horizontally and vertically.

---

## 5. Typography

Typography carries personality and structure. Make it a deliberate choice.

**Typeface selection**
- Choose typefaces for the project's subject and tone. Don't default to whichever family you'd reach for on any project.
- **One family or two.** If two, make the contrast obvious (e.g. a geometric/grotesque sans with a high-contrast serif or a distinctive italic). Avoid pairing two similar sans-serifs.
- A *single family with a range of weights and widths* is often more cohesive than two families.
- Prefer variable fonts where available for finer control of weight and width. Always provide a robust fallback stack and `font-display: swap`.

**Scale and rhythm**
- Define a **type scale** (e.g. a modular ratio between 1.2 and 1.333) and use it from tokens. A typical set: caption, small, body, lead, h4, h3, h2, h1, display. Use fluid sizing (`clamp()`) for display and large headings so they scale with the viewport.
- **Display type is large and confident.** Contrast between display and body should be strong. Large headlines usually want *tighter* line-height (about 1.0 to 1.15) and slightly *negative* letter-spacing; small text wants looser spacing and a larger relative size than you think.
- Body text: 15 to 18px on screen, line-height about 1.5 to 1.7. Data-dense UI can drop to 13 to 14px but never below ~12px for anything meant to be read.
- Use **weight and tone, not just size,** to separate levels. A regular-weight large headline against small medium-weight labels often looks more refined than bold everywhere.
- **Tabular numerals** (`font-variant-numeric: tabular-nums`) for any aligned numbers: tables, prices, KPIs, timers, counts. Use proportional numerals for running text.
- **Numerals as display elements:** a large figure with a small caption, a delta, and a timeframe is an effective pattern, but only for numbers that truly matter. Don't make every stat a hero.
- Keep line length and alignment consistent. Left-align by default. Centre-align only short, ceremonial text.

**Typographic expression**
- Treat headline type as part of the composition: scale, weight, line breaks, and mixed styles can create a distinct voice. Set line breaks deliberately (`text-wrap: balance` for headings, `pretty` for paragraphs).
- A **style contrast inside a headline** (e.g. one phrase in an italic or alternate-style face) can be a strong signature, as the references show. Use it as *one considered move for the whole project*, applied with a reason (the emphasised phrase is the meaning of the sentence), not as a reflex added to every heading.
- Avoid by default: uppercase tracked-out labels above every heading, middle-dot-joined meta strings, monospace for every small label, and "01 / 02 / 03" numbering on content that isn't a sequence. Structure (numbers, eyebrows, dividers) must encode real information.
- Sentence case for UI text. Plain verbs. Buttons name the action ("Save changes", "Request a tour"), not "Submit".
- Truncate gracefully (single-line ellipsis for names, `line-clamp` for descriptions) and make sure truncation never hides critical information.

---

## 6. Surfaces, shape, borders, and depth

### Shape language
- Pick **a shape vocabulary** and keep it consistent. Examples: fully rounded pills for controls and chips; moderately rounded rectangles for panels; sharp or minimally rounded for data tables. Define 2 to 4 radius tokens and assign each to a *role* (control, container, media, overlay).
- **Radius follows hierarchy and nesting.** A container's radius = inner element's radius + the padding between them. This keeps nested corners looking concentric. Don't give every element the same large radius.
- **Distinctive shape moves** seen in the references, to use sparingly and consistently:
  - Pill buttons that "merge" into an adjacent circular icon button (a joined or waisted shape).
  - Cards with a notched or cut corner holding an action (an arrow, a bookmark).
  - A leading circle or avatar cluster overlapping a pill.
  - Stacked edges: the card behind another peeking out as a thin layer to imply depth or "more".
  - Framed canvas: product shown inside an inset rounded frame.
  - Implement these with CSS masks, `clip-path`, pseudo-elements, or inline SVG, not with images, and make sure they hold up at all sizes.
- If you use pills everywhere, nothing is special. Limit the signature shape to the elements that carry meaning (the primary CTA, active state, selected filter).

### Borders and outlines
- Borders are a **structural tool.** A strong outline can make a card feel graphic and tactile, while a hairline can separate rows quietly. Choose which role each plays and stay consistent: one border weight for containers, one for dividers.
- A heavy outline combined with a filled surface gives a confident, illustrated feel; a borderless tonal surface gives a soft, calm one. Mixing both in one screen is fine only when the difference *means* something (e.g. selected vs. unselected, featured vs. standard).
- Prefer a tonal step between surfaces (page, container, raised container, inverted container) over relying on borders everywhere.

### Depth and layering
- Establish **a few elevation levels** (flat, raised, floating/overlay) and map each to a role. Not every card needs a shadow.
- **Shadows:** soft, low-opacity, and with larger blur plus a small y-offset. Layer two shadows (a tight contact shadow and a larger ambient one) for convincing depth. Don't reuse one identical shadow on everything.
- Use **overlap** as depth: a card straddling two regions, an element hanging off a container's edge, a sheet partially covering content.
- **Inverted panels** (a surface with the opposite tonal weight from its neighbours) as an intentional counterweight for featured, detail, or "focus" content. One or two per screen.
- **Texture and pattern** (hatching, fine grain, subtle stripes) can communicate state (empty, projected, placeholder, "in progress") or add tactility. Use it where it carries information; don't sprinkle it as decoration.
- **Gradients:** treat as an exception. Valid uses: indicating a real continuous quantity, a rich hero surface where it's the single memorable element, or a scrim for legibility over imagery. Avoid soft gradient washes behind sections or as default card fills.
- Avoid glassmorphism/blur by default. Use `backdrop-filter` only where overlapping content genuinely needs separation (sticky bars, floating navs), and always keep text contrast safe.

### Imagery and illustration
- Use imagery that is specific to the subject: product views, real objects, people, 3D or illustrated assets with a consistent style. Consistency of treatment (crop, framing, level of detail) matters more than the style itself.
- Crop deliberately: tight crops, off-centre subjects, and objects that bleed off the container edge feel designed. Keep corner radii on media consistent with the container logic.
- Avatars: use stacked/overlapping clusters with a "+N" overflow to show community or participation. Keep size, ring, and overlap amount consistent.
- Icons: one family, one stroke weight, one corner style, and one optical size per context. Pair icons with labels unless the meaning is universal.
- Placeholder content must look real: plausible names, dates, units, and states, not "Lorem ipsum" or "Item 1".

---

## 7. Component guidance

### Cards
- A card is a **grouping device**, not a default wrapper. Before adding one, ask: does this content need to be grouped, elevated, selected, or compared?
- **Vary card types by purpose:** a *featured* card (large, rich media), a *metric* card (value, delta, context), a *status* card (progress or state), an *action* card (single clear CTA), a *list* card (rows with dividers), an *inverted/detail* card. Don't repeat one card anatomy for everything.
- **Internal anatomy is consistent:** the same placement of tag/category, title, metadata, and action in a given card type, so users learn to scan.
- Title first, then the 1 or 2 pieces of metadata that help a decision, then the action. Hide the rest behind a detail view.
- Give interactive cards a clear affordance (a corner arrow, a visible action, or a cursor/hover change), and make the whole card a single large hit target when it has one destination.
- **Don't nest card in card in card.** At most two levels of containment.
- Equal-height cards in a row should align internal sections (title, meta, footer) to shared baselines.

### Navigation
- **Top bar (marketing):** logo, 4 to 6 links, one primary and one secondary action. A floating pill-shaped bar, or a bar that visually joins to its action buttons, can feel distinctive; keep it simple and legible.
- **Sidebar (product):** grouped sections with small group labels, icon + label items, counts where meaningful, a clearly marked active item (a filled or inverted treatment), workspace switcher on top, profile at the bottom. Provide a collapsed (icon-only) state for narrow widths.
- **Tabs / segmented controls:** one control for switching *views of the same content*; the selected state is unambiguous (filled, inverted, or underlined). Don't also use a dropdown for the same job.
- **Filter chips:** horizontally scrollable on small screens, with a clearly "on" state and a count if useful. Include an "All" option.
- **Mobile bottom bar:** 3 to 5 items, filled/pill active state plus label, icon outlines for inactive, a stable position (no layout shift on selection). If a central action exists, it should look different from the destinations.
- **Mobile header patterns** (from the header reference set) work because they follow a simple grammar: a leading control (menu or back), a central identity or title, and trailing actions (search, account, cart). Pick one arrangement and keep it consistent across screens. Surface the *most-used* action (search, cart) directly; hide the rest.
- Breadcrumbs or back controls should always make the user's location and exit obvious.

### Buttons
- **Hierarchy:** primary (one per region), secondary (outlined or tonal), tertiary (text/ghost). Never more than one primary in view unless they are truly parallel.
- **Anatomy:** generous horizontal padding (about 1.5 to 2x the vertical), comfortable height (40 to 48px), clear label, optional leading/trailing icon. A trailing icon is for direction or meaning (an arrow, a play glyph, an external link), not to pad the label.
- **Icon buttons:** circular or squared with a consistent size scale; provide `aria-label`; give them the same hover/focus language as other buttons.
- **States:** default, hover, focus-visible, active/pressed, disabled, loading. Pressed states should feel physical (a slight scale-down or inset), and loading should preserve the button width.
- Distinctive button shapes (merged pill + circle, waisted pills) are strongest on *the* main CTA of a page. Everywhere else, keep buttons plain and consistent.

### Forms and inputs
- Labels above fields (not placeholder-only), with helper text beneath and errors that say **what happened and how to fix it**, positioned beside the field they concern.
- Field height 40 to 48px; consistent radius with buttons; clear focus ring using an offset outline; filled vs. outlined style chosen once for the whole product.
- **Search:** treat as a first-class control. Large, with a clear icon, an optional trailing action (filter, scan, voice), and visible focus. A single search + one filter entry point beats a row of five filters.
- Group related fields; use progressive disclosure for advanced options; use smart defaults; and use inline validation on blur, not on every keystroke.
- Toggles, checkboxes, and radios are visually distinct from each other and have large hit areas.
- Provide a clear primary submit action whose label states the result.

### Data display
- **KPI tiles:** value, label, delta, timeframe. Keep the label quiet and the value strong. Show direction with an icon/arrow *and* a sign, never relying on tone alone.
- **Tables:** left-align text, right-align numbers, tabular numerals, sticky header for long tables, row hover and selected states, comfortable row height, and a quiet divider style. Provide an overflow strategy for narrow screens (horizontal scroll with a pinned first column, or a card-per-row transformation).
- **Lists with status:** a status indicator (pill/dot + text), a primary line, a secondary line, and a right-aligned action or value. Status is never conveyed by colour alone.
- **Progress:** bars, tracks, and steppers should show *how much, of what, and what's next* ("5/20 lessons"). A shipment-style stepper (completed nodes, current node, remaining dotted track, estimated time) is a good model for any multi-stage status.
- **Charts:** choose by question. Funnels/pipelines for stage conversion; heatmaps for density over time; stacked bars for composition; timelines for scheduling; sparklines for trend in a small space. Label directly, minimise gridlines and legends, annotate the interesting point, and make the chart a first-class citizen of the layout rather than a box in a grid.
- **Empty and zero states:** explain what belongs here and offer the one action to fill it. Use hatching/placeholder treatments that look intentional.
- **Tags and chips:** a small, consistent set (category, status, filter, count). Each type has its own treatment; don't use the same pill for four different meanings.

### Overlays and feedback
- Dialogs, sheets, popovers, and toasts have a clear elevation, a scrim where needed, a visible close, trapped focus, and `Esc` support.
- On mobile, prefer bottom sheets over centred modals for secondary tasks.
- Toasts confirm actions using the same verb the user triggered ("Published", "Saved"), include an undo when destructive, and don't block interaction.

---

## 8. Interaction and motion

Motion should explain change or confirm action. It is not wallpaper.

**Principles**
- **Respond to the user.** Hover, focus, press, open, close, drag, and reorder all deserve feedback. This is where motion earns its keep.
- **Be sparing with unprompted motion.** Choose *one* orchestrated entrance or one signature moment per page. Do not fade-and-slide every section on scroll, and don't add a hover lift to every card.
- **Durations:** 100 to 150ms for micro-feedback (hover, press, toggles), 200 to 300ms for state changes (menus, tabs, expanding panels), 300 to 500ms for larger transitions (sheets, page transitions, orchestrated reveals). Faster on exit than enter.
- **Easing:** use ease-out (decelerating) for things entering, ease-in for things leaving, and gentle springs for direct manipulation. Avoid linear except for continuous progress and looping indicators.
- **Animate cheap properties only:** `transform` and `opacity`. Avoid animating layout properties (width, height, top, left) where possible; for expand/collapse use `grid-template-rows` transitions or measured heights.
- **Preserve spatial continuity.** Elements that change state should visibly come from somewhere and go somewhere (a card expanding into a detail view, a tab indicator sliding between tabs, a list item moving when reordered). Consider the View Transitions API for page and element transitions where supported.
- **Useful micro-interactions:**
  - Selected-state indicator that glides between tabs/segments.
  - Button press (scale about 0.97) with quick release.
  - Number counters that tick to new values (respect reduced motion).
  - Checkbox/task completion with a small, satisfying check draw and a strike or fade of the item.
  - Expanding rows and accordions with smooth height and a rotating chevron.
  - Skeleton loaders that match the final layout, not generic spinners.
  - Progress/stepper nodes that fill in sequence on first view.
  - Carousel with scroll-snap, edge fade, and a peeking next item.
  - Hover reveal of secondary actions on dense rows (always available via focus and touch too).
- **Loading and optimistic UI:** show structure immediately, then fill content. Prefer optimistic updates for low-risk actions.
- **Respect `prefers-reduced-motion`.** Provide non-motion alternatives (instant state change or a simple fade). Never rely on motion alone to convey information.

---

## 9. Responsive design

Responsive means the design *stays good*, not merely that it fits.

- **Design mobile-first** with the content that matters most, then add structure for larger screens. Choose breakpoints where the *content* breaks, not at device names (roughly: ~480, ~768, ~1024, ~1280+ are good starting guesses).
- **Recompose, don't just stack.** A multi-region desktop composition should reorganise on small screens: promote the focal region to the top, collapse secondary panels into tabs, accordions, or horizontal scrollers, and convert sidebars to bottom bars or drawers. Don't let a bento become a long column of identical boxes without prioritising.
- **Fluid type and spacing** with `clamp()`; keep minimum sizes legible. Display type scales down more aggressively than body text.
- **Container queries** (`@container`) let components adapt to their own width, making cards and widgets reusable across layouts. Prefer them for component-level responsiveness.
- **Tables and data views** need a mobile strategy from the start (see section 7).
- **Images and media:** responsive `srcset`/`sizes`, `aspect-ratio` set to prevent layout shift, and consistent object-fit crops.
- **Touch vs pointer:** hover-only affordances need a touch equivalent. Use `@media (hover: hover)` to scope hover effects.
- **Safe areas and viewport units:** use `dvh`/`svh` rather than `vh` for full-height mobile layouts. Respect `env(safe-area-inset-*)`.
- **Test** at ~360, ~390, ~768, ~1024, ~1440, and a very wide size. Check long names, large numbers, empty content, and zoom at 200%.
- Keep the **shape language, spacing scale, and hierarchy** the same at every size. Only density and arrangement change.

---

## 10. Consistency without sameness

Components share a family resemblance but never become a uniform wall.

- **Define the family once:** radius roles, border weights, spacing scale, type roles, elevation levels, icon style, motion timing. Every component draws from these.
- **Vary by role, not at random.** Differences must mean something: featured vs. standard, active vs. inactive, urgent vs. routine, primary vs. supporting.
- **Vary section skeletons.** Within a page, adjacent regions should differ in structure, density, and scale. If you can copy-paste one section's layout onto another by swapping the text, they're too similar.
- **Hold constants steady** (grid, gutters, type scale, interaction language) so variety in composition feels designed.
- **Limit your distinct treatments.** For instance: two surface treatments, three radii, three card anatomies, one signature shape move. Variety within a small vocabulary reads as sophistication; endless variety reads as chaos.
- **Spend boldness in one place.** Let a single element be the memorable thing (a headline treatment, a hero object, a signature shape, an unusual layout), and keep everything else disciplined and quiet.

---

## 11. Frontend implementation guidelines

### Structure and tokens
- Use **design tokens as CSS custom properties** for spacing, type scale, radii, border widths, elevations, durations, and easings. Colour tokens should be **semantic** (surface, surface-raised, surface-inverted, text-primary, text-muted, border, accent, positive, caution, negative, focus) so any palette can be swapped in without touching components. Support theming (including light and dark) by redefining tokens, not by duplicating components.
- Build with **semantic HTML** (`header`, `nav`, `main`, `section`, `article`, `aside`, `footer`, `button`, `a`, `ul`, `table`, `form`). Visual design does not excuse div soup.
- Use **small, composable components** with a clear API (variants via props, content via slots/children). Avoid components with a dozen boolean props; prefer explicit variants.
- Keep **CSS manageable:** one methodology per project (utility-first with a token-aware config, CSS modules, or well-scoped component CSS). Avoid competing selectors (e.g. `.section` padding vs. a child's margin); manage specificity deliberately and prefer low, flat specificity. Use `@layer` to order resets, tokens, components, and utilities.
- Use **CSS Grid** for two-dimensional layout (bento, shells, dashboards), **Flexbox** for one-dimensional alignment, `gap` for spacing (not margins on siblings), `aspect-ratio` for media, `min()/max()/clamp()` for fluid sizing, and `subgrid` where aligned internals matter.
- Avoid magic numbers. If a value matters, give it a token or a named variable with a comment.
- Prefer **`rem`** for type and spacing (so user font-size settings work), **`ch`** for measure, and `px` only for borders, hairlines, and fine details.

### Shapes, depth, and effects in code
- Implement notches, joins, and cutouts with `mask`, `clip-path`, or SVG, parameterised by CSS variables so radius and size follow tokens. Test them at all sizes and inside overflow containers.
- Compose shadows from tokens (`--shadow-raised`, `--shadow-floating`) with layered values. Never hard-code a shadow on a component.
- Use `isolation: isolate` and deliberate `z-index` tokens (a short ordered scale) to avoid stacking-context bugs.
- Keep effects performant: avoid large blurred elements, animate only `transform`/`opacity`, use `will-change` sparingly, and lazy-load heavy media.

### Accessibility floor (non-negotiable, built-in, not bolted on)
- Text contrast meets WCAG AA at minimum (4.5:1 for body, 3:1 for large text and UI components) in every theme.
- Visible **`:focus-visible`** styles on all interactive elements, with enough offset and contrast to see on every surface.
- Everything works with keyboard only; logical tab order; skip link; trapped focus in dialogs; `Esc` closes overlays.
- Never rely on colour alone to convey state; pair with icon, text, or pattern.
- Proper labels, `aria-*` where semantics are not native, `alt` text that describes purpose, live regions for async feedback.
- Respect `prefers-reduced-motion`, `prefers-color-scheme`, and `prefers-contrast` where relevant.
- Touch targets of at least ~44px.

### Performance and quality
- Ship real, optimised assets: responsive images, modern formats, explicit dimensions, lazy loading below the fold, font subsetting, and minimal layout shift.
- Prefer CSS over JS for visual effects; use JS for behaviour. Keep animation libraries to when CSS can't do the job.
- Keep the DOM lean. Avoid decorative wrappers that exist only for styling when a pseudo-element or grid would do.
- Handle all states for every data component: loading, empty, error, partial, overflowing, and extremely long or short content.
- Write readable code: consistent naming, no dead styles, no duplicated component variants, comments only where intent isn't obvious.

---

## 12. Copy and content as design

- Words are design material. Every label, heading, and message should help the user understand or act. Cut anything that doesn't.
- Write from the user's perspective, in plain language. Name things by what users do ("Manage notifications"), not how the system works.
- Use active voice and sentence case. Buttons state the outcome. The same action keeps the same name throughout a flow.
- Errors explain what happened and how to fix it. Empty states invite a next step. Neither apologises nor jokes at the user's expense.
- Use realistic placeholder content in the project's domain, with believable lengths. Include long names, big numbers, and missing data in your test content.
- Don't invent fake statistics, testimonials, or logos in anything that might ship. Mark placeholders clearly.
- Avoid filler marketing phrases and generic section headings ("Our Features", "Why Choose Us"). Say the specific thing.

---

## 13. Anti-patterns: what makes UI look generically AI-generated

Treat these as defaults to **consciously avoid or justify**, not as laws.

**Layout**
- Stacked full-width sections with a centred heading, a one-line subtitle, and a row of three identical cards.
- Every region wrapped in a card; cards inside cards; one radius on everything.
- A hero with a centred headline, two buttons, and a glowing blob or gradient behind it.
- A symmetric 3 or 4-column feature grid repeated down the page.
- Dashboards that are a wall of equal-sized tiles with a line chart in each.
- Equal visual weight everywhere, so there is no focal point.

**Decoration**
- Gradient washes as backgrounds for sections and cards; gradient text; glow effects.
- The same soft drop shadow on every card.
- Excess glassmorphism and blur.
- Decorative icons in coloured circles above every heading.
- Random floating shapes, blobs, noise overlays, sparkle icons, or emoji used as visual filler.
- Confetti-level decoration: borders, shadows, gradients, and textures all at once.

**Typography**
- Uppercase, widely tracked eyebrow labels above every heading.
- One word in a headline recoloured or italicised by reflex.
- Numbered markers (01, 02, 03) on content that isn't a sequence.
- Meta lines joined with middle dots; "Label: value" strings that add no information.
- A monospace face used for every small label to look technical.
- Arrows appended to every link and button.
- Mid-sized, mid-weight type at every level, so nothing stands out.

**Interaction**
- Fade-and-slide-up on every section as it scrolls into view.
- Hover lift/scale on every card, regardless of whether it's clickable.
- Parallax or scroll-jacking with no purpose.
- Spinners where skeletons would do; abrupt state changes where a short transition would explain.

**Content**
- "Lorem ipsum", "Item 1", "John Doe", and round-number statistics.
- Vague headings and buttons ("Learn more", "Get started", "Submit") with no specific outcome.
- Fake logos or testimonials presented as real.

---

## 14. Pre-delivery checklist

**Hierarchy and composition**
- [ ] I can name the focal point of each screen, and it's obvious at a glance (squint test).
- [ ] Adjacent sections differ in structure, density, or scale.
- [ ] Layout is built on a grid with deliberate alignment; asymmetry is intentional.
- [ ] Not every region is a card; containers mark real differences.

**Spacing and type**
- [ ] All spacing comes from the scale; inside < between < around holds everywhere.
- [ ] Type scale is defined, display/body contrast is strong, line lengths are controlled.
- [ ] Numbers that align use tabular numerals.
- [ ] Typographic flourishes are limited to one deliberate signature.

**Components**
- [ ] Buttons have a clear hierarchy and all interactive states.
- [ ] Cards share an anatomy by type; there are at most 3 to 4 card types.
- [ ] Navigation shows location and active state clearly; mobile navigation has comfortable targets.
- [ ] Forms have labels, helpful errors, and clear focus.
- [ ] Data components handle loading, empty, error, and overflow states.

**Depth and detail**
- [ ] Radii, borders, and shadows follow tokenised roles; nested radii are concentric.
- [ ] Depth comes from layering and tone more than shadow; gradients and effects are justified.
- [ ] Signature shape moves are used sparingly and are consistent.

**Motion**
- [ ] Motion explains change or confirms action; there's at most one orchestrated moment.
- [ ] Durations and easings come from tokens; only cheap properties are animated.
- [ ] `prefers-reduced-motion` is respected.

**Responsive and quality**
- [ ] Layout recomposes (not just stacks) at small sizes; verified at multiple widths and at 200% zoom.
- [ ] Contrast, keyboard use, focus, and semantics are verified.
- [ ] Code uses tokens, semantic HTML, low specificity, and no magic numbers.
- [ ] I removed at least one decorative element that wasn't earning its place.

---

## 15. Closing principle

Good interfaces are the result of many small, deliberate decisions that point in the same direction: a clear first read, a composition with a point of view, a restrained set of recurring components, type that carries voice, depth that explains structure, and motion that answers the user. When in doubt, simplify, make one thing memorable, and make every other thing quiet and correct.

---

## Applying this to Nelavista

Nelavista's subject is the *working record*: a student's learning, evidence, paid work and payout kept in one inspectable chain. The interface should feel like a well-kept ledger — precise, quiet, and trustworthy — not like a generic SaaS dashboard.

Project-specific rules that follow from the reference:

- **Voice and type.** Instrument Serif for display and editorial statements; Instrument Sans for UI; IBM Plex Mono only where the content is genuinely record-like (codes, amounts, timestamps, step markers). Do not use mono for every small label.
- **Signature move.** One italic phrase inside the primary display headline (`Learn it. Prove it. *Get paid for it.*`). Do not repeat the italic treatment on every heading.
- **One inverted panel per screen.** The dark (light theme) or light (dark theme) panel marks "what stays with you" on marketing and the primary next action on the dashboard.
- **Numbers must be real.** KPI values and counts come from the API (`enrolments`, `current_semester`, `next_step`). Never invent figures, testimonials, or logos.
- **Radius roles.** `--nv-radius-xs` for inputs and rows, `--nv-radius-md` for panels, `--nv-radius-pill` for badges and the mobile active state. Media keeps `--nv-radius-sm`.
- **Spacing.** Use the `--nv-space-*` scale only. Inside < between < around. Section rhythm: `--nv-space-6xl`/`--nv-space-7xl` between marketing chapters, `--nv-space-xxl` between dashboard regions.
- **Motion.** One orchestrated hero reveal on the landing page; page transitions already exist in the app shell. Everything else is micro-feedback at `--nv-duration-fast`.
- **Mobile shell.** One header, not two. A bottom navigation with five destinations (Home, Academia, Skills, Work, Earnings); Settings and Notifications live in the header.
