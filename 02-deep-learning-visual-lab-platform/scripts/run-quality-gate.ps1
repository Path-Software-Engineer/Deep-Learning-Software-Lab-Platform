[CmdletBinding()]
param(
    [switch]$SkipFrontend
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"
$frontend = Join-Path $projectRoot "frontend\lab-app"
$env:PYTHONPATH = @(
    (Join-Path $projectRoot "backend\api"),
    (Join-Path $projectRoot "ai-services\neural-network-explainer\src")
) -join ";"
$env:MYPYPATH = $env:PYTHONPATH

if (-not (Test-Path -LiteralPath $python)) {
    throw "Project virtual environment is missing. Create .venv with Python 3.12."
}

Push-Location $projectRoot
try {
    Write-Host "[1/8] Verifying Python imports"
    & $python -c "import fastapi, pydantic, torch; print(f'FastAPI {fastapi.__version__} | Pydantic {pydantic.__version__} | PyTorch {torch.__version__}')"
    if ($LASTEXITCODE -ne 0) { throw "Python dependency verification failed." }

    Write-Host "[2/8] Running Python lint"
    & $python -m ruff check backend\api ai-services\neural-network-explainer scripts checks tests
    if ($LASTEXITCODE -ne 0) { throw "Ruff failed." }

    Write-Host "[3/8] Running Python typecheck"
    & $python -m mypy
    if ($LASTEXITCODE -ne 0) { throw "Mypy failed." }

    Write-Host "[4/8] Running Python tests and coverage"
    & $python -m pytest --cov --cov-report=term-missing
    if ($LASTEXITCODE -ne 0) { throw "Pytest failed." }

    Write-Host "[5/8] Exporting and checking contracts"
    & $python scripts\export_openapi.py
    if ($LASTEXITCODE -ne 0) { throw "OpenAPI export failed." }
    & $python checks\check_contract_alignment.py
    if ($LASTEXITCODE -ne 0) { throw "Contract check failed." }
    & $python checks\check_sprint_01.py
    if ($LASTEXITCODE -ne 0) { throw "Sprint check failed." }

    if (-not $SkipFrontend) {
        Write-Host "[6/8] Running frontend lint, types and component tests"
        Push-Location $frontend
        try {
            if (-not (Test-Path -LiteralPath "node_modules")) {
                throw "Frontend dependencies are missing. Run npm install in frontend\lab-app."
            }
            & npm run lint
            if ($LASTEXITCODE -ne 0) { throw "Frontend lint failed." }
            & npm run typecheck
            if ($LASTEXITCODE -ne 0) { throw "Frontend typecheck failed." }
            & npm run test
            if ($LASTEXITCODE -ne 0) { throw "Frontend tests failed." }

            Write-Host "[7/8] Building Next.js"
            & npm run build
            if ($LASTEXITCODE -ne 0) { throw "Next.js build failed." }
        }
        finally {
            Pop-Location
        }
    }
    else {
        Write-Host "[6/8] Frontend gate explicitly skipped by caller"
        Write-Host "[7/8] Next.js build explicitly skipped by caller"
    }

    Write-Host "[8/8] Checking patch whitespace"
    & git diff --check
    if ($LASTEXITCODE -ne 0) { throw "git diff --check failed." }
    Write-Host "OK - Sprint 1 quality gate passed"
}
finally {
    Pop-Location
}
