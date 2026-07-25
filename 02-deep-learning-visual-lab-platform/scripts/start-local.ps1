$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"
$frontend = Join-Path $projectRoot "frontend\lab-app"

if (-not (Test-Path -LiteralPath $python)) {
    throw "Create the project .venv before starting the platform."
}

$env:PYTHONPATH = @(
    (Join-Path $projectRoot "backend\api"),
    (Join-Path $projectRoot "ai-services\neural-network-explainer\src")
) -join ";"

Start-Process `
    -FilePath $python `
    -ArgumentList "-m", "uvicorn", "app.main:app", "--app-dir", "backend/api", "--host", "127.0.0.1", "--port", "8000" `
    -WorkingDirectory $projectRoot `
    -WindowStyle Hidden

Start-Process `
    -FilePath "npm.cmd" `
    -ArgumentList "run", "dev" `
    -WorkingDirectory $frontend `
    -WindowStyle Hidden

Write-Host "API docs: http://127.0.0.1:8000/docs"
Write-Host "Web: http://127.0.0.1:3000"
