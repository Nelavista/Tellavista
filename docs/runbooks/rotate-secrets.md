# Runbook — Rotate secrets

`docs/SECRETS_ROTATION.md` is the itemised checklist of what was exposed. This is **how** to run it.

## Status (from the audit)
- `.env` is **not tracked** and **not in this repo's current history** (`git log --all -- .env` is empty).
- The commits named in `SECRETS_ROTATION.md` **do not exist in this repo** — either history was already rewritten or they belong to an older lineage. **This does not undo the exposure.** Treat every listed credential as compromised and rotate.

## Procedure (per credential)
1. **Revoke/rotate at the provider** (OpenRouter, Hugging Face, Google Cloud, Cloudinary, Render Postgres passwords, Groq).
2. Put the **new** value in the provider's environment settings (Render → service → Environment; dev and prod **separately**).
3. Update any GitHub Actions secret that needs it.
4. **Redeploy / restart** the service so it picks up the new value.
5. **Delete the old value** at the provider (not just replace it locally).
6. Update `SECRETS_ROTATION.md` (tick the item, note the date).

## `SECRET_KEY`
The audit found V1 never actually set one (it silently used the dev fallback). Generate a real value per environment:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Rules
- **Never print, copy or commit a secret.** Not in a PR, not in a CI log, not in chat.
- **Never commit** a value; `.env.local` is local-only.
- gitleaks (pre-commit + CI) is the backstop — do not bypass it.

## Postgres passwords
Rotate in the Render dashboard; update `DATABASE_URL` in the same service; the app reconnects (`pool_pre_ping`). Do dev first, then prod, in a low-traffic window.
