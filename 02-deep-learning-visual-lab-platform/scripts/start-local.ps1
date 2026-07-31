[CmdletBinding()]
param(
    [int]$ApiPort = 8000,
    [int]$WebPort = 3000,
    [switch]$Production
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"
$frontend = Join-Path $projectRoot "frontend\lab-app"
$runtime = Join-Path $projectRoot ".runtime"

if (-not (Test-Path -LiteralPath $python)) {
    throw "Create the project .venv before starting the platform."
}
if (-not (Test-Path -LiteralPath (Join-Path $frontend "node_modules"))) {
    throw "Install frontend dependencies with npm ci in frontend\lab-app."
}

function Assert-PortAvailable {
    param([int]$Port)

    $listener = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    if ($listener) {
        throw "Port $Port is already in use by PID $($listener[0].OwningProcess)."
    }
}

Assert-PortAvailable -Port $ApiPort
Assert-PortAvailable -Port $WebPort
New-Item -ItemType Directory -Force -Path $runtime | Out-Null

# Some managed Windows terminals expose both `Path` and `PATH`. Start-Process
# treats them as duplicate dictionary keys, so normalize only this launcher
# process before creating its children.
$processPath = @(
    [Environment]::GetEnvironmentVariable("Path", "Machine"),
    [Environment]::GetEnvironmentVariable("Path", "User")
) -join ";"
[Environment]::SetEnvironmentVariable("PATH", $null, "Process")
[Environment]::SetEnvironmentVariable("Path", $processPath, "Process")

$env:PYTHONPATH = @(
    (Join-Path $projectRoot "backend\api"),
    (Join-Path $projectRoot "ai-services\neural-network-explainer\src"),
    (Join-Path $projectRoot "ai-services\cnn-feature-map-viewer\src"),
    (Join-Path $projectRoot "ai-services\autoencoder-latent-space\src")
) -join ";"

$api = Start-Process `
    -FilePath $python `
    -ArgumentList "-m", "uvicorn", "app.main:app", "--app-dir", "backend/api", "--host", "127.0.0.1", "--port", $ApiPort `
    -WorkingDirectory $projectRoot `
    -WindowStyle Hidden `
    -RedirectStandardOutput (Join-Path $runtime "api.out.log") `
    -RedirectStandardError (Join-Path $runtime "api.err.log") `
    -PassThru

$env:API_PROXY_TARGET = "http://127.0.0.1:$ApiPort"
if ($Production) {
    $standalone = Join-Path $frontend ".next\standalone"
    $server = Join-Path $standalone "server.js"
    if (-not (Test-Path -LiteralPath $server)) {
        throw "The production build is missing. Run npm run build in frontend\lab-app."
    }

    $sourceStatic = Join-Path $frontend ".next\static"
    $targetStatic = Join-Path $standalone ".next\static"
    New-Item -ItemType Directory -Force -Path $targetStatic | Out-Null
    Copy-Item -Path (Join-Path $sourceStatic "*") -Destination $targetStatic -Recurse -Force

    $sourcePublic = Join-Path $frontend "public"
    if (Test-Path -LiteralPath $sourcePublic) {
        Copy-Item -Path $sourcePublic -Destination $standalone -Recurse -Force
    }

    $node = (Get-Command "node.exe").Source
    $env:HOSTNAME = "127.0.0.1"
    $env:PORT = $WebPort
    $web = Start-Process `
        -FilePath $node `
        -ArgumentList $server `
        -WorkingDirectory $standalone `
        -WindowStyle Hidden `
        -RedirectStandardOutput (Join-Path $runtime "web.out.log") `
        -RedirectStandardError (Join-Path $runtime "web.err.log") `
        -PassThru
}
else {
    $web = Start-Process `
        -FilePath "npm.cmd" `
        -ArgumentList "run", "dev", "--", "--hostname", "127.0.0.1", "--port", $WebPort `
        -WorkingDirectory $frontend `
        -WindowStyle Hidden `
        -RedirectStandardOutput (Join-Path $runtime "web.out.log") `
        -RedirectStandardError (Join-Path $runtime "web.err.log") `
        -PassThru
}

Set-Content -LiteralPath (Join-Path $runtime "api.pid") -Value $api.Id
Set-Content -LiteralPath (Join-Path $runtime "web.pid") -Value $web.Id
Set-Content -LiteralPath (Join-Path $runtime "api.port") -Value $ApiPort
Set-Content -LiteralPath (Join-Path $runtime "web.port") -Value $WebPort

Write-Host "Axon started."
Write-Host "Mode: $(if ($Production) { 'production build' } else { 'development' })"
Write-Host "API PID: $($api.Id) | http://127.0.0.1:$ApiPort/docs"
Write-Host "Web PID: $($web.Id) | http://127.0.0.1:$WebPort"
Write-Host "Sprint 2: http://127.0.0.1:$WebPort/cnn"
Write-Host "Sprint 3: http://127.0.0.1:$WebPort/autoencoder"
Write-Host "Stop safely with .\scripts\stop-local.ps1"
