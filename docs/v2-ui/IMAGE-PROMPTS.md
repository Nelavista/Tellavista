# Image prompts and asset manifest

| Field | Value |
|---|---|
| Status | **Approved with the design direction. Assets are not created yet.** |
| Date | 2026-10-27 |
| Applies to | `apps/web/public/images/`, `apps/web/public/og/` |
| Rule | Use real photography where it carries content. Do not generate people, testimonials or fake product data. |

> These are art-direction briefs for a real photographer or for selecting real
> licensed images. They are not prompts for generating synthetic people. If a real
> image is not available, ship the product artifact or a solid surface with a
> caption instead. Never fill the gap with a fake student, a fake campus or a fake
> metric.

---

## 1. Required assets

### 1.1 Landing hero

| Field | Value |
|---|---|
| Path | `apps/web/public/images/home/hero-student.webp` (fallback) and `hero-student.avif` |
| Sizes | 1600×2000 (4:5), 800×1000, 400×500 |
| Loading | `fetchpriority="high"`, `decoding="async"`, no lazy loading |
| Alt | “A university student working on a laptop at a campus desk.” |
| Subject | One Nigerian university student, 18–24, working on a laptop or phone at a real campus desk or study space. Hands and screen visible; face optional. Natural light. |
| Art direction | Documentary, not stock. No posed smiling at camera. No graduation cap. No “African pattern” overlay. The screen should show a real note or document, not a fake dashboard. |
| Crop | 4:5 portrait. Leave quiet space at the top for the headline on desktop; keep the subject on the right third. |
| Colour | Warm natural light, neutral greens/browns. Do not tint to match the UI accent. |
| Release | Written consent from the student and the campus, if identifiable. |

### 1.2 Campus study

| Field | Value |
|---|---|
| Path | `apps/web/public/images/home/campus-study.webp` (fallback) and `campus-study.avif` |
| Sizes | 1600×1067 (3:2), 800×533, 400×267 |
| Loading | Lazy, `decoding="async"` |
| Alt | “Two students working together at a table on campus.” |
| Subject | Two or three students collaborating at a table, books or laptops open. A real campus building or walkway in the background, not a generic office. |
| Art direction | Candid, mid-action. No eye contact with the camera. No perfect symmetry. |
| Use | How it works or About, not the hero. |

### 1.3 Founder portrait

| Field | Value |
|---|---|
| Path | `apps/web/public/images/about/founder.webp` (fallback) and `founder.avif` |
| Sizes | 1200×1500 (4:5), 600×750 |
| Loading | Lazy |
| Alt | “Abdul Afeez Tella, founder of Nelavista.” |
| Subject | Real founder portrait, natural light, neutral background. |
| Art direction | Direct, calm, not a corporate headshot on a seamless backdrop. A desk or campus setting is fine. |
| Rule | Do not use a generated portrait. If there is no real portrait, use a text-only founder note. |

### 1.4 Team photo

| Field | Value |
|---|---|
| Path | `apps/web/public/images/about/team.webp` (fallback) and `team.avif` |
| Sizes | 1600×1067 (3:2), 800×533 |
| Loading | Lazy |
| Alt | “The Nelavista team.” |
| Subject | Real team, if one exists. |
| Rule | If there is no real team photo, omit the section. Do not use a stock “team” image. |

### 1.5 Default social card

| Field | Value |
|---|---|
| Path | `apps/web/public/og/default.webp` |
| Size | 1200×630 |
| Alt | Not applicable; OG image |
| Content | The Nelavista wordmark, the line “Learn it. Prove it. Get paid for it.” and one real product artifact (a transcript row or a payout receipt). Paper background. |
| Rule | No stock photo, no fake student count, no gradient blob. |

### 1.6 Shared-profile social card

| Field | Value |
|---|---|
| Path | `apps/web/public/og/share.webp` |
| Size | 1200×630 |
| Alt | Not applicable; OG image |
| Content | Generic proof card: “Verified proof, shared by a Nelavista student.” No name, photo, university or earnings. |
| Rule | The share card must not leak student data. The page itself is scoped by token. |

### 1.7 Optional page social cards

Only if the page needs a distinct preview:

| Path | Size | Content |
|---|---|---|
| `apps/web/public/og/features.webp` | 1200×630 | “Learn it. Prove it. Get paid for it.” plus the four-step chain |
| `apps/web/public/og/how-it-works.webp` | 1200×630 | The proof chain, no people |
| `apps/web/public/og/about.webp` | 1200×630 | Wordmark and mission line |
| `apps/web/public/og/legal.webp` | 1200×630 | Wordmark and document label |

Do not create a separate OG image for every legal page. One legal card is enough.

---

## 2. Product artifacts instead of stock photos

Use real V2 components or real captures for:

- A transcript row with a verified skill, evidence link and date.
- A work order with a brief, rate and deadline.
- A payout receipt with a line item and a paid stamp.
- A CBT result with a topic and a next action.

These are stronger than photography because they show the actual product. If a
static capture is used, regenerate it when the UI changes; do not let a stale
screenshot ship.

---

## 3. Image rules

- Format: AVIF first, WebP fallback. Keep the original out of `public/`.
- Responsive: `srcset` with 1x/2x or width descriptors; always set `width` and
  `height` to prevent layout shift.
- Hero: preload the AVIF/WebP; do not lazy-load the hero.
- Everything else: `loading="lazy"` and `decoding="async"`.
- Max weight: hero 200 KB, other photos 120 KB, OG 150 KB.
- Alt text is written for the page, not copied from the filename. Decorative
  images use `alt=""`.
- No text baked into photos except the OG cards.
- No AI-generated people, campuses, logos, testimonials or product data.
- No image may imply a university partnership or a student outcome that is not
  real.

---

## 4. If an asset is missing

Use this order:

1. A real product artifact (preferred).
2. A solid `surfaceRaised` block with a short caption and correct alt text.
3. No image and more typography.

Do not use a placeholder URL, a stock photo of a different campus, or a generated
person. A missing photo is a content gap, not a design failure.
