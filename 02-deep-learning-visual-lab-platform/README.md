# Deep Learning Visual Lab Platform

Project 02 of the Software Engineer path. **Axon** is a full-stack educational
platform for inspecting registered PyTorch models through bounded FastAPI
contracts and responsive Next.js experiences.

## Available modules

### Sprint 1 — Neural Network Explainer

Select an XOR observation and inspect weights, biases, preactivations,
activations, prediction and registered loss history for a deterministic 2–4–1
MLP.

### Sprint 2 — CNN Feature Map Viewer

Select an official Fashion-MNIST sample or temporarily upload a PNG/JPEG image,
run the registered CNN, choose an observable convolutional layer and inspect up
to 12 channels with tensor metadata and raw activation statistics.

Feature maps are presented as intermediate activations, never as causal
explanations.

## Architecture

```text
User
→ Next.js 16 + React + TypeScript
→ typed HTTP/JSON client
→ FastAPI + Pydantic
→ bounded application service
→ integrity-checked PyTorch checkpoint
```

PyTorch owns all neural computation. React manages interaction and represents
API resources; it does not implement forward passes, convolution or feature-map
extraction. Training is deterministic and offline.

## Sprint 2 evidence

- official 900-image Fashion-MNIST sprite with verified SHA-256;
- stratified split: 600 training, 150 validation and 150 held-out test images;
- registered `fashion-cnn-v1` checkpoint with 207,018 parameters;
- validation accuracy: 85.33% (128/150);
- held-out accuracy: 81.33% (122/150);
- controlled forward hooks for two allowlisted ReLU layers;
- independent per-channel min–max display normalization with preserved raw
  statistics;
- temporary bounded PNG/JPEG upload that is never persisted.

This is controlled educational evidence, not a complete Fashion-MNIST benchmark
or production-readiness claim.

## API

| Method | Route | Responsibility |
|---|---|---|
| `GET` | `/health` | Process and artifact health |
| `GET` | `/api/v1/platform/modules` | Available platform modules |
| `GET` | `/api/v1/neural-network/summary` | XOR model and checkpoint metadata |
| `POST` | `/api/v1/neural-network/forward` | One XOR forward trace |
| `GET` | `/api/v1/neural-network/training-history` | XOR offline training evidence |
| `GET` | `/api/v1/cnn/summary` | CNN, dataset, layers and evaluation |
| `GET` | `/api/v1/cnn/samples` | One registered sample per class |
| `POST` | `/api/v1/cnn/predict` | Bounded sample or upload prediction |
| `POST` | `/api/v1/cnn/feature-maps` | Prediction plus selected activation maps |

Interactive documentation is available at `http://127.0.0.1:8000/docs`.

## Run locally

Prerequisites: Python 3.12 and Node.js 20.9 or newer.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-dev.txt

Set-Location .\frontend\lab-app
npm ci
Set-Location ..\..

.\scripts\start-local.ps1
```

Open:

- Sprint 1: `http://127.0.0.1:3000`
- Sprint 2: `http://127.0.0.1:3000/cnn`

To reproduce the Sprint 2 artifact:

```powershell
.\.venv\Scripts\python.exe .\scripts\train_cnn.py
```

## Quality gate

```powershell
.\scripts\run-quality-gate.ps1
```

The gate verifies Python dependencies, Ruff, strict mypy, pytest and coverage,
OpenAPI/client alignment, Sprint 1 regression evidence, Sprint 2 acceptance,
frontend lint, TypeScript, component tests, production build and Git
whitespace.

Detailed evidence is in the [Sprint 2 record](docs/sprints/sprint-02-cnn-feature-map-viewer/README.md).
Sprint 3 remains intentionally unopened.
