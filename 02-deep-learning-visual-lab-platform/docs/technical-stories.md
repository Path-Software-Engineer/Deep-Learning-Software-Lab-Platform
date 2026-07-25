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
