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

### Sprint 3 — Autoencoder Latent Space Demo

Compare a Fashion-MNIST image with its reconstruction, select one of 100
registered two-dimensional points, inspect nearest references and decode a
controlled interpolation between two points.

Latent distance and smooth interpolation describe this checkpoint only; they
are not universal semantic or causal explanations.

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

## Sprint 3 evidence

- registered `fashion-autoencoder-2d-v1` checkpoint with 215,923 parameters;
- deterministic 600/150/150 split over the verified official sprite;
- held-out MSE `0.033027` and MAE `0.106527` over 150 images;
- 100 registered 2D reference points, ten per class;
- reconstruction error, neighbors and interpolation calculated by PyTorch;
- checksum-verified checkpoint and gallery loaded once by FastAPI.

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
| `GET` | `/api/v1/autoencoder/summary` | Autoencoder, dataset and evaluation evidence |
| `GET` | `/api/v1/autoencoder/samples` | One reconstruction reference per class |
| `GET` | `/api/v1/autoencoder/latent-points` | Registered 2D gallery and bounds |
| `POST` | `/api/v1/autoencoder/reconstruct` | Source, reconstruction, error and neighbors |
| `POST` | `/api/v1/autoencoder/interpolate` | Decoder-backed interpolation sequence |

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

For the already-built production frontend:

```powershell
.\scripts\start-local.ps1 -Production
```

Open:

- Sprint 1: `http://127.0.0.1:3000`
- Sprint 2: `http://127.0.0.1:3000/cnn`
- Sprint 3: `http://127.0.0.1:3000/autoencoder`

Stop only the processes recorded by the launcher:

```powershell
.\scripts\stop-local.ps1
```

To reproduce the Sprint 2 artifact:

```powershell
.\.venv\Scripts\python.exe .\scripts\train_cnn.py
```

To reproduce the Sprint 3 artifact:

```powershell
.\.venv\Scripts\python.exe .\scripts\train_autoencoder.py
```

To run the production-shaped local topology:

```powershell
docker compose up --build
```

## Quality gate

```powershell
.\scripts\run-quality-gate.ps1
```

The gate verifies Python dependencies, Ruff, strict mypy, pytest and coverage,
OpenAPI/client alignment, all three sprint checks, frontend lint, TypeScript,
component tests, production build, Docker Compose and Git whitespace.

Detailed final evidence is in the
[Sprint 3 record](docs/sprints/sprint-03-autoencoder-latent-space-demo/README.md).
