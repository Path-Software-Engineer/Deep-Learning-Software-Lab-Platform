# Sprint 1 Technical Stories

## TS-P2-S1-001 — Deterministic PyTorch MLP

### Need

Provide one reproducible neural implementation for the controlled XOR task.

### Acceptance criteria

- topology is 2–4–1 with 17 parameters;
- seed and training configuration are recorded;
- all four XOR predictions are correct in the registered artifact.

### Status

Completed.

### Evidence

`config.py`, `dataset.py`, `model.py`, `train_neural_network.py`,
`test_dataset.py`, `test_model.py`.

### Related User Stories

US-P2-S1-001, US-P2-S1-003.

## TS-P2-S1-002 — Structured forward snapshot

### Need

Expose internal forward values without coupling PyTorch objects to HTTP or UI.

### Acceptance criteria

- snapshots contain weights, biases, preactivations and activations;
- values are JSON-safe;
- hidden and output layer order is validated.

### Status

Completed.

### Evidence

`snapshot.py`, `service.py`, `LayerResource`, service and API tests.

### Related User Stories

US-P2-S1-001, US-P2-S1-002.

## TS-P2-S1-003 — Integrity-checked artifact pipeline

### Need

Prevent a stale checkpoint, manifest or history from being served.

### Acceptance criteria

- checksum and byte size are verified;
- model and history configuration must match the manifest;
- corruption fails closed with a controlled error.

### Status

Completed.

### Evidence

`artifacts.py`, `manifest.json`, `training-history.json`, `test_artifacts.py`.

### Related User Stories

US-P2-S1-002, US-P2-S1-003, US-P2-S1-004.

## TS-P2-S1-004 — Versioned FastAPI contract

### Need

Expose bounded read and inference operations through typed resources.

### Acceptance criteria

- only summary, forward and history business routes are present;
- invalid input produces a typed 422 response;
- OpenAPI and the frontend client stay aligned.

### Status

Completed.

### Evidence

FastAPI router and resources, `docs/api/openapi.json`,
`check_contract_alignment.py`, backend and contract tests.

### Related User Stories

US-P2-S1-001, US-P2-S1-003, US-P2-S1-004.

## TS-P2-S1-005 — Accessible Next.js experience

### Need

Represent the registered trace and training evidence without neural logic in
React.

### Acceptance criteria

- binary controls identify pressed state;
- computed SVG nodes support pointer, Enter and Space;
- loading, error, empty and connected states exist;
- reduced motion and visible focus are supported;
- component tests validate API-derived values.

### Status

Completed in code; final live-browser evidence remains environment-dependent.

### Evidence

`NeuralNetworkExplainer.tsx`, `NetworkDiagram.tsx`, CSS Module,
frontend tests and production build.

### Related User Stories

US-P2-S1-001, US-P2-S1-002, US-P2-S1-003, US-P2-S1-004.

## TS-P2-S1-006 — Cross-layer quality gate

### Need

Detect regressions across Python, contracts and frontend before release.

### Acceptance criteria

- lint, strict type checking, tests and coverage pass;
- OpenAPI is regenerated and checked;
- frontend lint, types, component tests and build pass;
- Sprint 2 and Sprint 3 contexts remain unopened.

### Status

Completed.

### Evidence

`run-quality-gate.ps1`, `check_sprint_01.py`, contract and integration tests.

### Related User Stories

US-P2-S1-001, US-P2-S1-002, US-P2-S1-003, US-P2-S1-004.

## Traceability

| Technical Story | User Stories | Primary evidence |
|---|---|---|
| TS-P2-S1-001 | US-P2-S1-001, US-P2-S1-003 | model and training script |
| TS-P2-S1-002 | US-P2-S1-001, US-P2-S1-002 | snapshot and service |
| TS-P2-S1-003 | US-P2-S1-002, US-P2-S1-003, US-P2-S1-004 | artifact loader and tests |
| TS-P2-S1-004 | US-P2-S1-001, US-P2-S1-003, US-P2-S1-004 | FastAPI and OpenAPI |
| TS-P2-S1-005 | all Sprint 1 stories | Next.js module and tests |
| TS-P2-S1-006 | all Sprint 1 stories | root quality gate |

## Sprint 2 — CNN Feature Map Viewer

### TS-P2-S2-001 — Reproducible Fashion CNN evidence

### Need

Train and register one bounded convolutional model over a traceable official
source.

### Acceptance criteria

- source checksum and deterministic stratified split are versioned;
- architecture, seed, optimizer and loss are recorded;
- checkpoint, manifest, history, gallery and evaluation agree.

### Status

Completed.

### Evidence

`dataset.py`, `model.py`, `train_cnn.py`, `fashion-cnn-v1.pt`,
`manifest.json`, dataset/model tests.

### Related User Stories

US-P2-S2-001, US-P2-S2-003, US-P2-S2-004.

### TS-P2-S2-002 — Integrity-checked CNN artifact bundle

### Need

Fail closed when the CNN checkpoint, sample gallery or configuration is stale
or corrupted.

### Acceptance criteria

- checksum and byte size are verified;
- model, training and dataset versions must match;
- gallery contains one valid unique sample per class.

### Status

Completed.

### Evidence

`artifacts.py`, `manifest.json`, `sample-gallery.json`,
`test_artifacts.py`.

### Related User Stories

US-P2-S2-001, US-P2-S2-003.

### TS-P2-S2-003 — Controlled activation capture

### Need

Observe intermediate tensors without changing the registered model or exposing
arbitrary modules.

### Acceptance criteria

- only published ReLU layers can be captured;
- hooks are removed after the request;
- logits and activations belong to the same forward pass;
- invalid layers and channels fail safely.

### Status

Completed.

### Evidence

`hooks.py`, `service.py`, `test_model.py`, `test_service.py`.

### Related User Stories

US-P2-S2-002, US-P2-S2-003.

### TS-P2-S2-004 — Auditable display transformation

### Need

Make spatial patterns visible while preserving the distinction between raw
activation values and display colors.

### Acceptance criteria

- each channel is independently normalized to `[0, 1]`;
- constant maps are handled deterministically;
- raw min, max, mean and standard deviation remain available;
- the non-comparability rule is documented.

### Status

Completed.

### Evidence

`service.py`, `feature-map-normalization-lab/README.md`,
`FeatureMapTile.tsx`, service tests.

### Related User Stories

US-P2-S2-002, US-P2-S2-003, US-P2-S2-004.

### TS-P2-S2-005 — Versioned CNN FastAPI contract

### Need

Expose metadata, samples, prediction and feature maps through bounded typed
resources.

### Acceptance criteria

- four Sprint 2 endpoints appear in OpenAPI;
- uploads are validated and never persisted;
- typed 422 errors describe invalid input safely;
- the TypeScript client and OpenAPI paths remain aligned.

### Status

Completed.

### Evidence

CNN router/resources/application service, `openapi.json`,
`check_contract_alignment.py`, backend API tests.

### Related User Stories

US-P2-S2-001, US-P2-S2-002, US-P2-S2-003.

### TS-P2-S2-006 — Responsive Next.js representation viewer

### Need

Present predictions, selectable layers, channels and maps without neural logic
in the browser.

### Acceptance criteria

- registered sample and upload states are keyboard operable;
- loading, connected, error and empty states exist;
- feature maps expose accessible labels and raw statistics;
- responsive and reduced-motion behavior is defined;
- component and live E2E flows use API evidence.

### Status

Completed.

### Evidence

`CnnFeatureMapViewer.tsx`, `FeatureMapTile.tsx`, CSS Module, frontend component
and Playwright tests.

### Related User Stories

US-P2-S2-001, US-P2-S2-002, US-P2-S2-003, US-P2-S2-004.

### TS-P2-S2-007 — Cross-context release gate

### Need

Close Sprint 2 without regressing Sprint 1 or opening Sprint 3.

### Acceptance criteria

- lint, strict types, tests, coverage and builds pass;
- OpenAPI and frontend contracts are aligned;
- Sprint 1 and Sprint 2 checks pass together;
- the autoencoder context remains absent.

### Status

Completed.

### Evidence

`run-quality-gate.ps1`, `check_sprint_01.py`, `check_sprint_02.py`,
contract and integration suites.

### Related User Stories

US-P2-S2-001, US-P2-S2-002, US-P2-S2-003, US-P2-S2-004.

## Sprint 2 Traceability

| Technical Story | User Stories | Primary evidence |
|---|---|---|
| TS-P2-S2-001 | US-P2-S2-001, US-P2-S2-003, US-P2-S2-004 | dataset, model and training pipeline |
| TS-P2-S2-002 | US-P2-S2-001, US-P2-S2-003 | artifact loader and tests |
| TS-P2-S2-003 | US-P2-S2-002, US-P2-S2-003 | controlled hooks and service |
| TS-P2-S2-004 | US-P2-S2-002, US-P2-S2-003, US-P2-S2-004 | normalization contract |
| TS-P2-S2-005 | US-P2-S2-001, US-P2-S2-002, US-P2-S2-003 | FastAPI and OpenAPI |
| TS-P2-S2-006 | all Sprint 2 stories | Next.js viewer and tests |
| TS-P2-S2-007 | all Sprint 2 stories | root quality gate |
