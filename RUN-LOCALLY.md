# Run V2 locally (Windows)

This runs the V2 API, worker, student web app, and admin app. It does not touch
V1.

## Fastest path: no Docker, no `.env`

```powershell
# one-time, from the repo root
pnpm install
uv sync --all-packages

# every time
powershell -ExecutionPolicy Bypass -File .\scripts\dev-local.ps1
```

That uses **SQLite** at `apps/api/.local/v2-local.db` and prints verification
emails in the worker window. It does not need Docker, Postgres, Redis, Mailpit,
or any environment file.

Use the script rather than starting `uvicorn` by hand: V1 and V2 both use the
Python package name `app`, and the script selects the V2 environment for you.

Sign in with the seeded local accounts:

```text
Web    student1@example.test / localdevpass123
Admin  admin@example.test    / localdevpass123
```

The admin app asks you to enrol an authenticator (2FA) on first login; that is a
product rule, not a local-setup bug. Or sign up with any email for the web app.

The script sets those passwords when it creates the accounts (or when the
seeded student has none). If you change one in the UI, later starts leave it
alone; `-ResetDb` restores the defaults.

Useful switches:

```powershell
.\scripts\dev-local.ps1 -ResetDb     # delete and re-seed the local DB
.\scripts\dev-local.ps1 -NoWorker    # API + web + admin only
.\scripts\dev-local.ps1 -NoAdmin     # skip the admin app
.\scripts\dev-local.ps1 -NoSeed      # use the existing DB exactly as-is
```

Close the API/worker windows before `-ResetDb`; Windows keeps the SQLite file
locked while they are running.

The rest of this page is the Docker/Postgres path, which is closer to production
and is still the right choice when testing migrations or backend behaviour.

## 1. Start the local services

```powershell
docker compose up -d db redis mailpit
```

Postgres is on `5432`, Redis on `6379`; Mailpit's inbox is http://localhost:8025.

## 2. Create the V2 local environment

```powershell
Copy-Item apps\api\.env.example apps\api\.env.local
```

The example already points at the Docker database (`nelavista`) and Mailpit. The
API loads `apps\api\.env.local` last, so it wins over the V1 root `.env`.

## 3. Install and migrate

```powershell
pnpm install
# If apps\api\.venv does not exist yet, install uv (https://docs.astral.sh/uv/)
# and run: uv sync --all-packages
apps\api\.venv\Scripts\python.exe -m alembic -c apps/api/alembic.ini upgrade head
apps\api\.venv\Scripts\python.exe -m tools.seed_local
```

`seed_local` creates the fake university, two sample courses, the curriculum, and
two sample students. It never touches a real database.

## 4. Start everything

```powershell
.\scripts\dev.ps1
```

That opens four windows (API, worker, web, admin):

| Service | URL |
|---|---|
| API docs | http://localhost:8000/docs |
| Student web | http://localhost:5173 |
| Admin | http://localhost:5174 |
| Mailpit inbox | http://localhost:8025 |

The worker has no URL; it sends queued email and runs scheduled jobs. Leave its
window open, or verification and reset emails will sit in the queue.

If Postgres/Redis/Mailpit are already running, use `.\scripts\dev.ps1 -NoInfra`.

## 5. Make yourself an admin (local only)

Sign up at http://localhost:5173/signup (any email; it lands in Mailpit). Then:

```powershell
apps\api\.venv\Scripts\python.exe -m tools.create_staff `
  --email you@example.test --role super_admin
```

Sign out, sign in at http://localhost:5174, and enrol 2FA. Create a second staff
account with `--role ops_admin` if you want to test the two-approver payout rule.

## Common fixes

- **API says `Invalid configuration`** — read the message. Usually
  `apps\api\.env.local` is missing or `DATABASE_URL` is wrong.
- **DB schema out of date** — rerun the `alembic upgrade head` command above.
- **Start over** — `docker compose down -v` then repeat step 3. This destroys the
  local database only.
