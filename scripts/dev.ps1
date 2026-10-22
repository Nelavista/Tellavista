# Start the V2 stack locally on Windows (three windows: API, web, admin).
# Usage, from the repo root:
#   .\scripts\dev.ps1
#   .\scripts\dev.ps1 -NoInfra   # if Postgres/Redis/Mailpit are already running

param([switch]$NoInfra)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$apiDir = Join-Path $root "apps\api"
$python = Join-Path $apiDir ".venv\Scripts\python.exe"

if (-not $NoInfra) {
    Push-Location $root
    try {
        docker compose up -d db redis mailpit
    } finally {
        Pop-Location
    }
}

if (Test-Path $python) {
    $apiCommand = "& '$python' -m uvicorn app.main:app --reload --port 8000 --app-dir apps/api"
    $workerCommand = "& '$python' -m app.worker"
} elseif (Get-Command uv -ErrorAction SilentlyContinue) {
    $apiCommand = "uv run --package nelavista-api uvicorn app.main:app --reload --port 8000 --app-dir apps/api"
    $workerCommand = "uv run --package nelavista-api python -m app.worker"
} else {
    throw "No Python environment. Run: uv sync --all-packages (install uv first: https://docs.astral.sh/uv/)"
}

Start-Process powershell -WorkingDirectory $root -ArgumentList @(
    "-NoExit", "-Command", $apiCommand
)
Start-Process powershell -WorkingDirectory $apiDir -ArgumentList @(
    "-NoExit", "-Command", $workerCommand
)
Start-Process powershell -WorkingDirectory $root -ArgumentList @(
    "-NoExit", "-Command", "pnpm --filter @nelavista/web dev"
)
Start-Process powershell -WorkingDirectory $root -ArgumentList @(
    "-NoExit", "-Command", "pnpm --filter @nelavista/admin dev"
)

Write-Host ""
Write-Host "API   http://localhost:8000/docs"
Write-Host "Web   http://localhost:5173"
Write-Host "Admin http://localhost:5174"
Write-Host "Mail  http://localhost:8025"
