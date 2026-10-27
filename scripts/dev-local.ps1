# Run the V2 stack locally with SQLite: no Docker, no Postgres, no Redis,
# no Mailpit and no .env file to fill in.
#
#   powershell -ExecutionPolicy Bypass -File .\scripts\dev-local.ps1
#   powershell -ExecutionPolicy Bypass -File .\scripts\dev-local.ps1 -ResetDb
#   powershell -ExecutionPolicy Bypass -File .\scripts\dev-local.ps1 -NoWorker
#   powershell -ExecutionPolicy Bypass -File .\scripts\dev-local.ps1 -NoSeed
#
# This only starts V2. It never starts or touches V1.

param(
    [switch]$ResetDb,
    [switch]$NoWorker,
    [switch]$NoSeed,
    [switch]$NoAdmin
)

$ErrorActionPreference = "Stop"

if ($ResetDb -and $NoSeed) {
    throw "-ResetDb cannot be combined with -NoSeed: a fresh database needs the seed."
}

if (-not (Get-Command pnpm -ErrorAction SilentlyContinue)) {
    throw "pnpm not found. Run: corepack enable (or install pnpm 9+), then pnpm install."
}
if (-not (Test-Path (Join-Path (Split-Path -Parent $PSScriptRoot) "node_modules"))) {
    throw "Dependencies are not installed. Run: pnpm install && uv sync --all-packages"
}

$root = Split-Path -Parent $PSScriptRoot
$apiDir = Join-Path $root "apps\api"
$localDir = Join-Path $apiDir ".local"
$dbPath = Join-Path $localDir "v2-local.db"
$dbUrl = "sqlite:///" + ($dbPath -replace '\\', '/')

if ($NoSeed -and -not (Test-Path $dbPath)) {
    throw "-NoSeed needs an existing database at $dbPath."
}

$python = Join-Path $apiDir ".venv\Scripts\python.exe"
$useUv = $false
if (-not (Test-Path $python)) {
    if (Get-Command uv -ErrorAction SilentlyContinue) {
        $useUv = $true
    } else {
        throw "No Python environment found. Run: uv sync --all-packages (install uv first: https://docs.astral.sh/uv/)"
    }
}

New-Item -ItemType Directory -Force $localDir | Out-Null

if ($ResetDb) {
    foreach ($suffix in @("", "-wal", "-shm", "-journal")) {
        $path = "$dbPath$suffix"
        if (Test-Path $path) { Remove-Item $path -Force }
    }
}

# Everything is set here, so apps/api/.env.local is optional. Skipping the env
# files also guarantees V2 never reads the V1 root .env.
$env:APP_ENV = "local"
$env:NELAVISTA_SKIP_ENV_FILE = "1"
$env:DATABASE_URL = $dbUrl
$env:SECRET_KEY = "local-dev-only-secret-key-at-least-32-bytes-long"
$env:REDIS_URL = ""
$env:CORS_ORIGINS = "http://localhost:5173,http://localhost:5174"
$env:WEB_BASE_URL = "http://localhost:5173"
$env:EMAIL_PROVIDER = "console"

function Invoke-V2Python {
    param([string[]]$Arguments)
    if ($useUv) {
        & uv run --package nelavista-api python @Arguments
    } else {
        & $python @Arguments
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Python command failed with exit code $LASTEXITCODE"
    }
}

if (-not $NoSeed) {
    Write-Host "Seeding the local SQLite database..." -ForegroundColor Cyan
    Invoke-V2Python @("-m", "tools.seed_local")
    Write-Host "Preparing the local login accounts..." -ForegroundColor Cyan
    Invoke-V2Python @("-m", "tools.create_local_user")
}

if ($useUv) {
    $apiCommand = "uv run --package nelavista-api uvicorn app.main:app --reload --port 8000 --app-dir apps/api"
    $workerCommand = "uv run --package nelavista-api python -m app.worker"
} else {
    $apiCommand = "& '$python' -m uvicorn app.main:app --reload --port 8000 --app-dir apps/api"
    $workerCommand = "& '$python' -m app.worker"
}

Start-Process powershell -WorkingDirectory $root -ArgumentList @(
    "-NoExit", "-Command", $apiCommand
)
if (-not $NoWorker) {
    Start-Process powershell -WorkingDirectory $apiDir -ArgumentList @(
        "-NoExit", "-Command", $workerCommand
    )
}
Start-Process powershell -WorkingDirectory $root -ArgumentList @(
    "-NoExit", "-Command", "pnpm --filter @nelavista/web dev"
)
if (-not $NoAdmin) {
    Start-Process powershell -WorkingDirectory $root -ArgumentList @(
        "-NoExit", "-Command", "pnpm --filter @nelavista/admin dev"
    )
}

Write-Host ""
Write-Host "V2 is starting (SQLite, no Docker):" -ForegroundColor Green
Write-Host "  Web    http://localhost:5173"
if (-not $NoAdmin) { Write-Host "  Admin  http://localhost:5174" }
Write-Host "  API    http://localhost:8000/docs"
if (-not $NoWorker) {
    Write-Host "  Email  printed in the worker window (EMAIL_PROVIDER=console)"
}
Write-Host ""
Write-Host "  Web login    student1@example.test / localdevpass123"
if (-not $NoAdmin) {
    Write-Host "  Admin login  admin@example.test / localdevpass123"
    Write-Host "               (the admin app asks you to enrol 2FA on first login)"
}
Write-Host "  DB           $dbPath"
Write-Host ""
Write-Host "Reset everything with: .\scripts\dev-local.ps1 -ResetDb" -ForegroundColor DarkGray
