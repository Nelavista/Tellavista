# Auto-resume for seed_topic_explanations_broad.py after a reboot/logon.
# Registered as a Scheduled Task (see setup instructions) so the multi-day explanation
# backfill survives this machine's frequent reboots without needing manual restarts.
# Idempotent and safe to fire even if a run is already in progress -- it checks first.

$ErrorActionPreference = "Stop"
$projectDir = "C:\Users\PC\Documents\Tellavista"
$logDir = Join-Path $projectDir "backfill_logs"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }

$already = Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" |
    Where-Object { $_.CommandLine -match "seed_topic_explanations_broad\.py" }

if ($already) {
    Write-Output "$(Get-Date -Format o) Already running (PID $($already.ProcessId)), nothing to do."
    exit 0
}

# A logon-time launch can race the network/DNS coming up (seen in practice: the process
# started and immediately crashed on "could not translate host name ... to address").
# Wait up to 2 minutes for the DB host to resolve before handing off to Python.
$dbHost = "dpg-d5j9gmfgi27c73eqct7g-a.oregon-postgres.render.com"
$deadline = (Get-Date).AddMinutes(2)
$resolved = $false
while ((Get-Date) -lt $deadline) {
    try {
        [System.Net.Dns]::GetHostAddresses($dbHost) | Out-Null
        $resolved = $true
        break
    } catch {
        Start-Sleep -Seconds 5
    }
}
if (-not $resolved) {
    Write-Output "$(Get-Date -Format o) DNS for $dbHost never resolved after 2 minutes, giving up this attempt."
    exit 1
}

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logFile = Join-Path $logDir "explanation_backfill_$stamp.log"

Set-Location $projectDir
$proc = Start-Process -FilePath "python" -ArgumentList "seed_topic_explanations_broad.py", "--apply" `
    -WorkingDirectory $projectDir -RedirectStandardOutput $logFile -RedirectStandardError "$logFile.err" `
    -WindowStyle Hidden -PassThru

Write-Output "$(Get-Date -Format o) Started PID $($proc.Id), logging to $logFile"
