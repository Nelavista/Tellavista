# Secrets Rotation Checklist

Every credential below has been present in this repo's git history (tracked `.env`, committed across
commits `866dea3`, `5c78a68`, `070ec51`, `d27dc45`) and pushed to the public remote
`github.com/ABDULAFEEZ12/Tellavista.git`. Purging history (Stage 2) removes them from *this* repo going
forward, but does **not** undo the exposure -- cached views, forks, and clones may already have copies.

**Treat every value below as compromised. Rotate all of them, regardless of whether history purge succeeds.**

- [ ] **Postgres (Render, `nelavistauser`)** -- reset the database password in the Render dashboard, update
      `DATABASE_URL` everywhere it's deployed.
- [ ] **Postgres (Render, `tawfiqdb_user`)** -- same, if that database is still in use.
- [ ] **Postgres (Render, `tellavista_user`)** -- same, if that database is still in use.
- [ ] **OpenRouter API key** (`sk-or-v1-d74a6222...`) -- this exact key has been publicly exposed since the
      very first commit to the repo. Revoke and issue a new one at openrouter.ai.
- [ ] **OpenRouter API key (older rotation)** (`sk-or-v1-bc7d14c2...`) -- also found in history; revoke if
      still active.
- [ ] **Hugging Face token** (`hf_yZaF...`) -- revoke at huggingface.co/settings/tokens.
- [ ] **Google API key (general)** (`AIzaSyCfJI...`) -- rotate in Google Cloud Console. Note: this specific
      key (`GOOGLE_API` env var) is not read anywhere in the live app -- confirm it's not used elsewhere
      before deciding whether to keep it at all.
- [ ] **Google Custom Search API key** (`AIzaSyAun...`) -- rotate in Google Cloud Console; this one IS used
      live (`routes/materials_routes.py`).
- [ ] **Google Search Engine ID** -- lower sensitivity, but pairs with the key above; consider rotating the
      Custom Search Engine too.
- [ ] **Cloudinary** (cloud name `dvqrbydge`, API key `997128687793466`, API secret) -- rotate the API
      secret in the Cloudinary console (cloud name/key alone aren't secret, but the secret is).
- [ ] **Groq key** (`gsk_CMBt...`) -- found as a bare, unlabeled line in `.env` (not even a valid
      `VAR=value` pair, so it was never actually loaded by the app). Revoke it anyway since it was
      sitting in a file that has been committed to git before.
- [ ] **SECRET_KEY** -- was never actually set (app silently used the hardcoded dev fallback). Generate and
      set a real random value now; not a rotation, but equally required.

After rotating, update the live values in your deployment platform's environment variable settings (Render,
etc.) and in your local `.env` (copied from `.env.example`, never committed).
