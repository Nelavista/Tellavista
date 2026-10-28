# Nelavista image prompts

| Field              | Value                                                                                                                                   |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| Status             | **Art direction approved 2026-10-27; palette corrected to brand blue/white 2026-10-28. Assets are not created yet.**              |
| Date               | 2026-10-28                                                                                                                              |
| Source drops       | `assets/incoming/`                                                                                                                    |
| Public derivatives | `apps/web/public/images/`, `apps/web/public/og/`                                                                                    |
| Rule               | These are editorial illustrations, not evidence. Never use one as a student testimonial, a real campus, a founder portrait or a metric. |

> The illustrations carry mood and context. They do not stand in for a real
> student, a real university, a real founder or a real outcome. Documentary
> sections still need licensed photography with consent, or no photograph at all.

---

## How to use

1. Open one ChatGPT image conversation and keep using it for every image, so the
   style stays consistent.
2. Paste the **style block** first and say "use this style for every image I ask
   for next." Then paste one prompt at a time.
3. Request the right size: **3:2 landscape (1536 by 1024)** for images marked 3:2,
   **1:1 square (1024 by 1024)** for those marked 1:1.
4. If a result is close but wrong, say "same style, change only X" instead of
   rewriting the whole prompt.
5. Save each file as a **PNG named exactly like the filename below** (for example
   `hero-main.png`) and drop it into `assets/incoming/`.
6. Start with the **P1** images. The public pages look finished with those alone.
   P2 can follow.

Check each image before saving: no text, letters, numbers, logos or currency
symbols anywhere; only the navy, blue and white palette; people
shown with dignity; one clear subject; nothing from the avoid list. The subject
must stay inside the centre safe area so a 4:3 or 16:9 crop does not cut it.

The default OG cards and the loading mark are built from code or brand assets.
Do not generate a social card with baked-in text.

---

## Style block (paste first)

```
Editorial block-print illustration, like a limited-colour screenprint or linocut: flat shapes, confident outlines, a slight offset between colour layers, and paper grain visible only inside the artwork. Palette strictly: deep navy (#050810) for linework and dark shapes, brand blue (#1535A8) for one or two key accents, and white (#FFFFFF) as the background. Everyday Nigerian setting shown with dignity and warmth: campuses, shared desks, hostels, buses, markets, small offices, students, traders and families. People have simplified features and natural everyday clothing, with no stereotypes or caricature. Calm, confident mood. One clear focal subject, generous empty space, and the subject kept inside the centre safe area. Solid white background with no border or frame.
Absolutely none of: text, letters, numbers, logos, currency symbols, coins, readable banknotes, rockets, upward arrows, trading charts, glowing phones, robots, brains, circuit patterns, handshakes, lightbulbs, padlock-and-shield icons, graduation caps, trophies, stock-photo smiles at camera, gradients, 3D rendering, isometric style, neon, glass effects, background grids, dot patterns, or decorative patterns.
```

## Image list

| File                  | Ratio | Priority | Used on                                       |
| --------------------- | ----- | -------- | --------------------------------------------- |
| hero-main             | 3:2   | P1       | Landing hero                                  |
| how-learn             | 1:1   | P1       | How it works, step 1                          |
| how-prove             | 1:1   | P1       | How it works, step 2                          |
| how-work              | 1:1   | P1       | How it works, step 3                          |
| how-earn              | 1:1   | P1       | How it works, step 4                          |
| proof-record          | 3:2   | P1       | Features, verification section                |
| auth-record           | 3:2   | P1       | Login and signup side panel                   |
| og-main               | 3:2   | P1       | Link previews (centre-cropped to 1200 by 630) |
| error-404             | 1:1   | P1       | Not found                                     |
| offline               | 1:1   | P1       | Offline                                       |
| empty-notifications   | 1:1   | P1       | Notifications, empty                          |
| empty-applications    | 1:1   | P1       | Applications, empty                           |
| empty-work            | 1:1   | P1       | Work, empty                                   |
| empty-earnings        | 1:1   | P1       | Earnings, empty                               |
| feature-academia      | 1:1   | P2       | Features, academia                            |
| feature-skills        | 1:1   | P2       | Features, skills                              |
| feature-opportunities | 1:1   | P2       | Features, opportunities                       |
| feature-talent        | 1:1   | P2       | Features, talent                              |
| about-record          | 3:2   | P2       | About, the working record                     |
| empty-materials       | 1:1   | P2       | Materials, empty                              |
| empty-cbt             | 1:1   | P2       | CBT history, empty                            |
| empty-transcript      | 1:1   | P2       | Transcript, empty                             |
| empty-skills          | 1:1   | P2       | Skills, empty                                 |
| empty-opportunities   | 1:1   | P2       | Opportunities, empty                          |
| empty-campus          | 1:1   | P2       | Campus, empty                                 |
| empty-learning        | 1:1   | P2       | My learning, empty                            |
| empty-course          | 1:1   | P2       | Course hub, no topics                         |
| error-boundary        | 1:1   | P2       | Error boundary                                |
| maintenance           | 1:1   | P2       | Maintenance state, if enabled                 |
| og-proof              | 3:2   | P2       | Shared-profile preview (centre-cropped)       |

The loading animation, logo, favicon and PWA icons are brand assets, not image
prompts. They live in `apps/*/public/brand/`, `apps/*/public/media/` and
`apps/web/public/icons/`.

---

## P1 prompts

**hero-main** (3:2, alt text: A student at a shared desk reading a long printed record beside a closed notebook.)

```
A calm Nigerian university student sitting at a shared desk in a modest campus study room, reading a long printed paper record. A closed notebook, a pen and a phone face-down rest beside the paper. A window with soft daylight, one empty chair, a small plant. The student is thoughtful and unhurried, not posing for the camera. Brand blue accent on a folder edge only.
```

**how-learn** (1:1, alt text: A student drawing a simple path of blank boxes in a notebook.)

```
A student at a desk drawing a simple path of connected blank boxes in an open notebook, with a stack of books and a cup beside it. The path is a plan, not a chart. Focused, quiet mood. Brand blue accent on the pen.
```

**how-prove** (1:1, alt text: A hand lowering a rubber stamp onto a ruled page.)

```
A close view of a hand lowering a rubber stamp onto a ruled page on a clerk's desk, with a small tray of blank evidence slips beside it. The page has ruled lines but no writing. The stamp is the focal point. Brand blue accent on the stamp handle.
```

**how-work** (1:1, alt text: A student reviewing a printed work ticket with a pencil.)

```
A student at a workbench reviewing a printed work ticket with a pencil, a small box of materials and a pair of headphones beside it. The ticket shows only blank bars where text would be. Practical, focused mood. Brand blue accent on the pencil.
```

**how-earn** (1:1, alt text: A student checking a printed receipt against a small cash box.)

```
A student at a small table checking a long printed receipt against a sturdy cash box, with a ledger open beside it. The receipt has ruled lines but no writing or numbers. Calm, orderly mood. Brand blue accent on the receipt edge.
```

**proof-record** (3:2, alt text: A row of printed records pinned along a string across a window.)

```
A row of long paper records pinned with clothespins along a string across a bright window, each slightly different in length, with simple ruled lines but no writing. A plant on the windowsill. Peaceful, orderly mood. Brand blue accent on a few clothespins.
```

**auth-record** (3:2, alt text: A person arranging printed records into a folder on a desk.)

```
A person at a desk arranging a few printed records into a simple folder, with a lamp, a cup and a small plant nearby. The records show ruled lines but no writing. Calm, welcoming mood. Brand blue accent on the folder tab.
```

**og-main** (3:2, keep the subject centred; the top and bottom will be cropped, alt text: A student reading a printed record at a shared desk.)

```
A simplified, bold version of a student reading a long printed record at a shared desk, centred with wide empty white space above and below. The figure, desk and paper must sit within the middle 60 percent of the height. Brand blue accent on one object.
```

**error-404** (1:1, alt text: A signpost with three blank arrow boards and a person looking up at it.)

```
A wooden signpost at a quiet street corner with three blank arrow boards pointing different ways, and a student with a small bag looking up at it, unsure. Brand blue accent on one board.
```

**offline** (1:1, alt text: A table lamp with its cable lying unplugged on the floor.)

```
A table lamp on a small side table with its power cable trailing down to the floor, unplugged, next to a wall socket. A book and a cup wait on the table. Brand blue accent on the lampshade.
```

**empty-notifications** (1:1, alt text: A neighbourhood mailbox with its flag down.)

```
A small neighbourhood mailbox on a post with its flag down and the door slightly open to show it is empty. A bird sits on top. Brand blue accent on the flag.
```

**empty-applications** (1:1, alt text: A neat stack of blank forms and a pen on a desk.)

```
A neat stack of blank application forms on a plain desk, one form slightly askew, with a pen resting on top. The forms have ruled lines but no writing. Quiet, waiting mood. Brand blue accent on the pen.
```

**empty-work** (1:1, alt text: An empty workbench with a few tools and a blank ticket.)

```
An empty workbench with a few neatly arranged tools, a blank paper ticket pinned above it and a stool tucked underneath. The ticket has ruled lines but no writing. Brand blue accent on the stool.
```

**empty-earnings** (1:1, alt text: An open empty cash box beside a closed ledger.)

```
An open but empty cash box on a table beside a closed ledger, with a receipt spike and a pencil nearby. No coins, notes or numbers. Brand blue accent on the cash-box clasp.
```

---

## P2 prompts

**feature-academia** (1:1, alt text: A student walking across a campus path with books under one arm.)

```
A student walking along a campus path with a few books under one arm, a simple building and a tree behind. Purposeful, everyday mood. Brand blue accent on the book cover.
```

**feature-skills** (1:1, alt text: A person practising with small blank cards arranged in piles.)

```
A person at a desk practising with small blank cards arranged in neat piles, a pencil behind one ear and a simple pegboard on the wall. The cards have no writing. Focused, relaxed mood. Brand blue accent on one pile.
```

**feature-opportunities** (1:1, alt text: A person reading a noticeboard of blank cards.)

```
A person standing at a community noticeboard covered in blank cards, one card in hand, deciding where to place it. No letters or numbers on the cards. Brand blue accent on one card.
```

**feature-talent** (1:1, alt text: A person laying out a folder of blank pages for someone to review.)

```
A person laying out a folder of blank ruled pages on a table for another person to review, both seen from a respectful distance. No handshake, no logos, no readable text. Brand blue accent on the folder.
```

**about-record** (3:2, alt text: A quiet desk with a stack of printed records, a lamp and a plant.)

```
A quiet office desk with a neat stack of printed records, a lamp, a cup and a small plant. The records have ruled lines but no writing. The room feels used and calm. Brand blue accent on the lamp base.
```

**empty-materials** (1:1, alt text: A bookshelf with a few books and an empty reading chair.)

```
A simple bookshelf with a few books and an empty reading chair beside a window, a folded blanket on the chair. Inviting, quiet mood. Brand blue accent on the blanket.
```

**empty-cbt** (1:1, alt text: A desk with a blank answer sheet and a pencil.)

```
A desk with a blank answer sheet, a pencil and a small clock with no numbers, ready for a test. The sheet has ruled lines but no writing. Brand blue accent on the pencil.
```

**empty-transcript** (1:1, alt text: A folder tied with string beside a few blank ruled pages.)

```
A simple folder tied with string on a desk, a few blank ruled pages beside it and a paper clip. No seals, stamps, logos or writing. Brand blue accent on the string.
```

**empty-skills** (1:1, alt text: An empty pegboard with a few hooks.)

```
An empty wooden pegboard on a wall with a few brass hooks, a small shelf below holding one folded cloth. Clean, waiting mood. Brand blue accent on one hook.
```

**empty-opportunities** (1:1, alt text: An empty noticeboard with one blank card.)

```
A community noticeboard with one blank card pinned slightly off-centre and a second pin waiting in the corner. No text. Brand blue accent on the card.
```

**empty-campus** (1:1, alt text: A campus gate with a blank sign and a bench.)

```
A simple campus gate with a blank sign hanging above it, a bench and a tree beside the path. No letters or crests. Quiet afternoon mood. Brand blue accent on the bench.
```

**empty-learning** (1:1, alt text: A path of stepping stones across a garden.)

```
A path of stepping stones across a small garden, leading toward a low wall and a tree, with one stone slightly out of line. No arrows or signs. Brand blue accent on a flower beside the path.
```

**empty-course** (1:1, alt text: A stack of books with a blank bookmark and a reading lamp.)

```
A short stack of books on a desk with a blank bookmark and a reading lamp, one book open to a ruled page with no writing. Brand blue accent on the bookmark.
```

**error-boundary** (1:1, alt text: A toppled stack of blank papers on a desk with a hand reaching to tidy it.)

```
A toppled stack of blank papers on a desk, a mug nearby, and a person's hand reaching in to tidy the pile. The papers have ruled lines but no writing. Calm recovery mood, not disaster. Brand blue accent on the mug.
```

**maintenance** (1:1, alt text: A person on a stepladder repairing a blank shop sign.)

```
A person on a short stepladder repairing a blank shop sign with a screwdriver, a toolbox open on the ground below. No letters on the sign. Brand blue accent on the toolbox.
```

**og-proof** (3:2, keep the subject centred; the top and bottom will be cropped, alt text: A single stamped record on a paper background.)

```
A single long paper record with ruled lines but no writing, centred on a wide white background, with one large stamp mark that contains no letters or numbers. A pencil rests beside it. The record must sit within the middle 60 percent of the height. Brand blue accent on the stamp pad.
```

---

## After generating

1. Put every PNG in `assets/incoming/`, named exactly as in the list.
2. Check the image at 100%: no text, letters, numbers, logos, currency symbols or
   accidental watermark. Reject any image with a sixth finger, a distorted face,
   a fake brand or a stereotype.
3. Export the public derivative to `apps/web/public/images/<name>.webp` at the
   target ratio. Keep the source PNG in `assets/incoming/` (ignored by Git).
4. Use `width` and `height` on every `<img>` so the layout does not shift.
   The hero is `fetchpriority="high"` and not lazy-loaded; everything else is
   `loading="lazy"` and `decoding="async"`.
5. Write alt text for the page, not from the filename. Decorative images use
   `alt=""`.
6. If you change the style later, regenerate all images in the same conversation
   so the set stays matched.

### Placeholder and missing-asset rule

Until a file exists, render the shared empty-state or a solid white/navy panel with
a short caption. Do not ship a stock photo of a different campus, a generated
portrait, or a placeholder URL. A missing illustration is a content gap, not a
reason to fake one.

### Social cards

The default and shared-profile OG cards are composed in code from the brand mark
and live data labels, then exported at 1200 by 630. The generated `og-main` and
`og-proof` art is only the background. Never bake the product name, a student
name, a university, an earnings figure or a testimonial into an image prompt.

---

## Not generated

| Item                 | Why                                                          | What to do instead                                                                                  |
| -------------------- | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| Founder portrait     | A generated face would misrepresent a real person.           | Use a real portrait with written consent, or a text-only founder note.                              |
| Team photo           | Same reason.                                                 | Use a real team photo, or omit the section.                                                         |
| Campus photography   | A generated campus implies a partnership that may not exist. | Use licensed photography of the actual campus, or an illustration that is clearly not documentary.  |
| Student testimonials | A generated quote or face is fabricated evidence.            | Use a real, consented quote with a name and context, or no testimonial.                             |
| Metrics and counts   | Invented numbers are a trust failure.                        | Use a real, dated number from the product, or no number.                                            |
| Social links         | The V1 placeholder links were not real.                      | Add only accounts that exist.                                                                       |
| Logo and favicon     | They are brand assets, not illustrations.                    | Use the V1 assets copied to `apps/*/public/brand/` and `apps/*/public/favicon.ico`.             |
| Loading animation    | It is a brand asset.                                         | Use `apps/web/public/media/nelavista-loader.webp`; the still mark is the reduced-motion fallback. |

## Needs my input

- Real founder and team photography, with consent.
- Licensed campus photography, if the About page should show a real campus.
- The final OG card wording and any real metric that is safe to publish.
- Whether the `maintenance` state will be enabled at launch.
- Whether the `animation3_color_exchange.mp4` brand video should appear anywhere
  beyond the loader. It is a 1920 by 1080, eight-second video with a blue
  background, so it is not a transparent loader. The WebP loader is the loader.
