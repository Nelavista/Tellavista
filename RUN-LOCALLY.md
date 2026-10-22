# Run V2 locally (Windows)

This runs the V2 API, worker, student web app, and admin app against local
Postgres, Redis and Mailpit. It does not touch V1.

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
