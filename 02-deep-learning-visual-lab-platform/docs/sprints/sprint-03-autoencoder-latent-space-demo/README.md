# Sprint 3 — Autoencoder Latent Space Demo

## Goal

Complete Axon with a third bounded context that makes a registered
Fashion-MNIST autoencoder inspectable without moving neural computation into
the browser.

## Scope

- deterministic convolutional autoencoder with a two-dimensional bottleneck;
- integrity-checked checkpoint, history, metrics and 100-point gallery;
- original/reconstruction comparison with server-calculated error;
- selectable latent points and nearest registered neighbors;
- decoder-backed interpolation between two registered points;
- five versioned FastAPI operations;
- responsive Next.js module integrated with the two prior sprints;
- Docker Compose for the complete local platform.

## Completed user outcomes

| Story | Outcome | Status |
|---|---|---|
| US-P2-S3-001 | Compare an original Fashion-MNIST image with its reconstruction and error | Completed |
| US-P2-S3-002 | Select a registered 2D point and inspect its sample and neighbors | Completed |
| US-P2-S3-003 | Decode a configurable interpolation between two reference points | Completed |
| US-P2-S3-004 | Read the scientific and product limitations beside the evidence | Completed |

## Registered evidence

- dataset: official 900-image Fashion-MNIST sprite;
- split: 600 training, 150 validation and 150 held-out images;
- model: `fashion-autoencoder-2d-v1`, 215,923 parameters;
- training: seed `20260729`, Adam, MSE, 90 epochs;
- validation MSE / MAE: `0.033606` / `0.108231`;
- held-out MSE / MAE: `0.033027` / `0.106527`;
- gallery: 100 registered points, ten per reference class;
- CPU training duration recorded by the pipeline: 39.90 seconds.

## Official outputs

- `models/autoencoder/fashion-autoencoder-2d-v1.pt`;
- `models/autoencoder/manifest.json`;
- `models/autoencoder/training-history.json`;
- `models/autoencoder/latent-gallery.json`;
- `reports/metrics/autoencoder/fashion-autoencoder-2d-v1.json`;
- `reports/summaries/autoencoder/fashion-autoencoder-2d-v1.md`;
- `/api/v1/autoencoder/*`;
- `/autoencoder`.

## Validation model

The final gate runs Ruff, strict mypy, pytest with coverage, OpenAPI alignment,
three sprint checks, frontend lint/types/components/build, Docker Compose
validation and Git whitespace checks. Live Docker and browser evidence is
recorded separately and only after it is actually executed.

## Evidence boundary

The 2D bottleneck is intentionally restrictive. Euclidean proximity describes
this registered representation only. Smooth decoder interpolation demonstrates
continuity along one segment; it does not demonstrate understanding, causality
or universal semantic structure. The 900-image educational subset and this
checkpoint are not production-readiness evidence.

## Closure criteria

- all four Sprint 3 user stories are traceable;
- all five API routes are present in the versioned OpenAPI document;
- the frontend performs no encoding, decoding, neighbor or interpolation math;
- all three modules remain navigable;
- Docker describes the complete two-process platform;
- the full quality gate and local smoke flow pass;
- Git integration and the `v1.0.0` tag occur only after explicit authorization.
