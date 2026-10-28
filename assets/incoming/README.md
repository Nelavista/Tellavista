# Incoming image drops

Put generated or licensed source images here, using the exact filenames in
[`docs/v2-ui/IMAGE-PROMPTS.md`](../../docs/v2-ui/IMAGE-PROMPTS.md).

- PNG or WebP is fine for the drop.
- Do not rename, crop, add text, or re-encode before dropping the file.
- Keep the original out of `apps/*/public/`. The public copy is the optimised
  derivative.
- This folder is a working area. Final assets belong in
  `apps/web/public/images/` (and, only where the admin app needs one,
  `apps/admin/public/`).

The loading animation and logo are not in this folder. They are brand assets and
live in `apps/web/public/media/`, `apps/admin/public/media/` and
`apps/*/public/brand/`.
