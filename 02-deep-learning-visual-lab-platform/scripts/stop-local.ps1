[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$runtime = Join-Path $projectRoot ".runtime"
$portFiles = @(
    (Join-Path $runtime "web.port"),
    (Join-Path $runtime "api.port")
)
$pidFiles = @(
    (Join-Path $runtime "web.pid"),
    (Join-Path $runtime "api.pid")
)

foreach ($portFile in $portFiles) {
    if (-not (Test-Path -LiteralPath $portFile)) {
        continue
    }

    $port = [int](Get-Content -Raw -LiteralPath $portFile)
    $listeners = Get-NetTCPConnection `
        -LocalPort $port `
        -State Listen `
        -ErrorAction SilentlyContinue
    foreach ($listener in $listeners) {
        Stop-Process -Id $listener.OwningProcess -ErrorAction SilentlyContinue
        Write-Host "Stopped listener on port $port (PID $($listener.OwningProcess))."
    }
    Remove-Item -LiteralPath $portFile -Force
}

foreach ($pidFile in $pidFiles) {
    if (-not (Test-Path -LiteralPath $pidFile)) {
        continue
    }

    $processId = [int](Get-Content -Raw -LiteralPath $pidFile)
    $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
    if ($process) {
        Stop-Process -Id $processId
        Write-Host "Stopped $($process.ProcessName) (PID $processId)."
    }
    Remove-Item -LiteralPath $pidFile -Force
}

Write-Host "Axon local processes are stopped."
