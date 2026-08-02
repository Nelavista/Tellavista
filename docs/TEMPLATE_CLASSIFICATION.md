# Template Classification Report

Every template under `templates/` (51 files, plus the orphaned `templates/pages/settings.html`),
classified per the decision in this refactor: **Active** (keep, currently rendered by a live
route), **Legacy** (superseded but kept for reference, archived out of Flask's template path),
or **Dead** (unreferenced anywhere — routes, other templates, or JS — safe to delete after one
more zero-reference check at delete time).

A fourth marker, **Tawfiq**, covers files carrying the separate "Tawfiq AI" brand — these are
handled by the Tawfiq-extraction pass (Stage 13), not by this A/B/C sweep, since they're neither
"keep for Nelavista" nor "worthless" — they belong to a different product entirely.

Evidence basis: a direct `grep` of every `render_template(...)` call across the live, registered
blueprints in `routes/*.py` (the definitive list of what Flask can actually reach), cross-checked
against template-to-template links and JS references for the handful of files route-grep alone
couldn't rule out.

## A — Active (27)

Rendered by a live, registered route today. Kept in place, refactored in this pass where noted.

| Template | Route (endpoint) |
|---|---|
| `about.html` | `pages.about` (`GET /about`) |
| `admin_materials.html` | `admin.admin_materials` (`GET /admin/materials`) |
| `admin_videos.html` | `video.admin_videos` (`GET /admin/videos`) — **created in this refactor**, the route previously 500'd because this file didn't exist |
| `analyze.html` | `ai.analyze_page` (`GET /analyze`) |
| `campus-map.html` | `pages.campus_map` (`GET /campus-map`) — fixed a case-sensitive image-filename bug (`SIWES` → `siwes`) that broke on production Linux |
| `CBT.html` | `cbt.CBT` (`GET /CBT`) |
| `community.html` | `community.community_page` (`GET /community`) |
| `dashboard.html` | `dashboard.dashboard` (`GET /dashboard`) |
| `forgot_password.html` | `auth.forgot_password` |
| `landing.html` | `dashboard.landing` (`GET /`) |
| `live_meeting.html` | `live.live_meeting` |
| `login.html` | `auth.login` |
| `mat101.html` | `pages.math101` (`GET /mat101`) |
| `materials.html` | `materials.materials` (`GET /materials`) |
| `offline.html` | `pwa.offline`, and the 404/500/503 error handlers |
| `privacy-policy.html` | `pages.privacy_policy` |
| `profile.html` | `profile.profile` |
| `profile_completion_modal.html` | `materials.complete_profile`, and included inline by `dashboard.html` |
| `reels.html` | `reels.reels` |
| `reset_password.html` | `auth.reset_password` |
| `settings.html` | `pages.settings` |
| `signup.html` | `auth.signup` |
| `student_live.html` | `live.live_meeting_student_view` |
| `talk-to-nelavista.html` | `ai.talk_to_nelavista` |
| `teach-me-ai.html` | `ai.teach_me_ai` |
| `teacher_live.html` | `live.live_meeting_teacher_view` |
| `upload.html` | `video.upload_video` — fixed a broken `url_for('upload_video')` that would 500 this page's form submit |
| `video.html` | `video.videos_page` |

`templates/images/` is also Active — it's an asset directory (not a template), and it's the one
of three near-identical image folders actually served, via `core.serve_image` (`/images/<file>`).

## B — Legacy (move to `archive/legacy/`)

Superseded by an Active template covering the same feature, but coherent enough to be worth
keeping for reference rather than deleting outright.

| Template | Superseded by | Note |
|---|---|---|
| `index.html` | `dashboard.html` | Earlier iteration — same sidebar/chat/exam code, missing PWA install banner & offline handling |
| `old materials.html` | `materials.html` | Prior generation of the materials browser |
| `old map.html` | `campus-map.html` | 2 generations back |
| `lasumap.html` | `campus-map.html` | 1 generation back |
| `mat_101.html` | `mat101.html` | Smaller, earlier Math101 page (confusingly-similar filename to the active one) |
| `5mb reels.html` | `reels.html` | Earlier reels UI variant |
| `no youtube reel.html` | `reels.html` | Earlier reels UI variant |
| `largelive.html` | `live_meeting.html` / `teacher_live.html` / `student_live.html` | Earlier live-meeting variant |
| `live.html` | `live_meeting.html` | Rendered only by `routes/live.py`, which is dead code (never imported/registered) |
| `create_hybrid_session.html` | — | Unwired hybrid-session feature; notable as 1 of only 2 templates in the whole repo using `{% extends "base.html" %}` — a real inheritance pattern worth keeping as a reference for future base-template work |
| `hybrid_live_session.html` | — | Same feature/pattern as above |
| `learning_profile.html` | — | Unwired profile-insights page, coherent enough to keep |
| `pages/settings.html` | `settings.html` | Same layout/JS as the active settings page, different color scheme — an experiment, not garbage |
| `file_analyzer.html` | `analyze.html` | Earlier "Turbo AI" fork of the analyzer page |

## C — Dead (delete, after a final zero-reference re-check at delete time)

Not rendered by any route, not linked from any Active template, not loaded by any JS — genuinely
unreferenced.

| Template | Evidence |
|---|---|
| `result.html` | Orphaned; references `url_for('next_level')`/`url_for('restart')`, endpoints that don't exist anywhere |
| `questions.html` | Orphaned bare stub |
| `trivia.html` | Orphaned (918KB), not linked from anywhere |
| `quiz.html` | Orphaned |
| `edit_profile.html` | Orphaned, unstyled stub |
| `error.html` | Orphaned — `app.py`'s error handlers use `offline.html`, not this |
| `talk_to_nelavista.html` | 0 bytes, empty file |
| `lasumaptest.html` | 0 bytes, empty file |
| `chat.html` | Only "referenced" by `summary.html`'s client-side link to `/chat.html` as a static path — which wouldn't resolve anyway (this file lives in `templates/`, not `static/`, and no route serves it). Both ends of this link are dead. |
| `summary.html` | Not rendered by any route; its only outbound link is to the equally-dead `chat.html` |
| `join_meeting.html` | Zero references anywhere — confirmed no route renders it, and `routes/live.py`'s `join_meeting()` function (itself dead/unregistered code) is a same-named form handler that doesn't render this file |

## Tawfiq (handled separately — Stage 13, not this pass)

Corrected after reading actual file *content* rather than going by filename alone — two of these
turned out to be misleadingly named:

| Template | Note |
|---|---|
| `talk_to_tawfiq.html` | Content is "Talk to Tawfiq" — pure Tawfiq AI brand surface, extracted out of this repo |
| `talk-to-tellavista.html` | Despite the Tellavista-sounding filename, its actual title/UI text is "Talk to Tawfiq" ("Ask Tawfiq", "Tawfiq is thinking...") — this is Tawfiq content, not a Nelavista/Tellavista rename target. Extracted. |
| `home.html` | "Tawfiq AI - Your Smart Islamic Companion" branded chat homepage — extracted |

Reclassified as **Legacy** instead (moved to `archive/legacy/`, not extracted) once their content was
checked and turned out to already be Nelavista-branded:

| Template | Note |
|---|---|
| `talk_to_tellavista.html` | Despite the filename, its title/content is already "Talk to Nelavista" — a near-duplicate of the live `talk-to-nelavista.html` |
| `home1.html` | Already titled/branded "Nelavista" throughout — an earlier landing-page draft, not Tawfiq |
| `fomal landing.html` | Already titled/branded "Nelavista" throughout — another landing-page draft |

## Non-template files following the same fate as their Dead/Legacy classification

Not templates, but surfaced by the same "what's actually referenced" analysis, and covered by
the Stage 12 archive/delete pass:

- Root `utils.py` and `services.py` — dead, colliding by name with the real `utils/`/`services/`
  packages; nothing in them is imported anywhere.
- Root backup app files (`old app.py`, `formal tellavista app.py`, `tellavista 2 app.py`,
  `real nelavvista app.py`, `video app.py`) — none imported by the live app.
- Root `images/` and `static/images/` — both confirmed byte-for-byte duplicates of a subset of
  the live `templates/images/`.
