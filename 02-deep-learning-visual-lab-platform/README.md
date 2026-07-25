# Deep Learning Visual Lab Platform

Project 02 of the Software Engineer path. Sprint 1 delivers **Axon**, a
full-stack Neural Network Explainer for a controlled XOR model.

The increment lets a user select two binary inputs, request a real forward
pass, inspect weights, biases, preactivations and activations, review the
registered loss history, and read the scientific limitations inside the
interface.

## Architecture

```text
User
→ Next.js 16 + React + TypeScript
→ HTTP/JSON
→ FastAPI + Pydantic
→ application service
→ registered PyTorch checkpoint
```

PyTorch owns all neural computation. The frontend only represents API data.
Training is deterministic and offline; no HTTP request trains the model.
During local development, Next.js proxies same-origin `/api/*` requests to
FastAPI; it does not duplicate the business API.

## Sprint 1 scope

- controlled four-row XOR contract;
- deterministic 2–4–1 PyTorch MLP;
- offline Adam training with seed `190`;
- versioned checkpoint, manifest, checksum, metrics and loss history;
- safe forward snapshots for hidden and output layers;
- typed FastAPI resources and errors;
- responsive Next.js interface with keyboard-operable neural nodes;
- unit, contract, integration and component tests;
- explicit claims boundary.

Sprint 2 and Sprint 3 modules are intentionally not implemented.

## API

| Method | Route | Responsibility |
|---|---|---|
| `GET` | `/health` | Process health |
| `GET` | `/api/v1/platform/modules` | Available platform modules |
| `GET` | `/api/v1/neural-network/summary` | Dataset, architecture and checkpoint metadata |
| `POST` | `/api/v1/neural-network/forward` | Forward trace for one binary XOR input |
| `GET` | `/api/v1/neural-network/training-history` | Registered offline training evidence |

Interactive documentation is available at `http://127.0.0.1:8000/docs`.

## Run locally

Prerequisites: Python 3.12 and Node.js 20.9 or newer.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-dev.txt

Set-Location .\frontend\lab-app
npm install
Set-Location ..\..

.\scripts\start-local.ps1
```

Open `http://127.0.0.1:3000`.

The proxy target defaults to `http://127.0.0.1:8000` and can be changed with
`API_PROXY_TARGET`. Set `NEXT_PUBLIC_API_ROOT` only when the browser must call a
separate deployed API directly.

To regenerate the registered model:

```powershell
.\.venv\Scripts\python.exe .\scripts\train_neural_network.py
```

## Quality gate

```powershell
.\scripts\run-quality-gate.ps1
```

The gate checks Python imports, Ruff, mypy, pytest with coverage, OpenAPI
alignment, Sprint 1 boundaries, frontend lint, TypeScript, component tests,
the Next.js production build and patch whitespace.

## Evidence boundary

XOR has four synthetic observations. Perfect accuracy on this controlled set is
not evidence of generalization. Internal activations are computations, not
causal explanations. The model is educational and not a production candidate.

Detailed decisions and evidence are in [docs](docs/architecture.md) and the
[Sprint 1 record](docs/sprints/sprint-01-neural-network-explainer/README.md).

## Status

Sprint 1 implementation is complete through Day 210. Release integration,
commit, merge, push and tag remain deliberate Gitflow actions and are not
performed by the implementation gate.
