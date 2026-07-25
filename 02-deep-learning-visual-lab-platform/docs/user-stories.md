# Sprint 1 User Stories

## US-P2-S1-001 — Run an XOR forward pass

**Story:** As a student, I want to select two XOR inputs so that I can observe
the model result.

**Acceptance criteria:**

- only binary pairs are accepted;
- the response includes probability, target, prediction and sample loss;
- invalid or unknown input fields return a typed error.

**Status:** Completed.

**Evidence:** `dataset.py`, `service.py`, `ForwardRequest`,
`test_neural_network_api.py`.

## US-P2-S1-002 — Inspect internal transformations

**Story:** As a student, I want to inspect layers, weights, biases,
preactivations and activations so that I can relate the model to its forward
equations.

**Acceptance criteria:**

- the hidden and output layers correspond to the loaded checkpoint;
- a keyboard user can select every computed node;
- the frontend does not recompute neural values.

**Status:** Completed.

**Evidence:** `snapshot.py`, `NetworkDiagram.tsx`, `TraceInspector.tsx`,
component and integration tests.

## US-P2-S1-003 — Review learning evidence

**Story:** As a student, I want to see the registered loss history so that I can
observe how offline training progressed.

**Acceptance criteria:**

- history identifies seed, configuration and metrics;
- loss points end at the registered training epoch;
- the browser reads history from FastAPI.

**Status:** Completed.

**Evidence:** `train_neural_network.py`, `training-history.json`,
`LossChart.tsx`, contract tests.

## US-P2-S1-004 — Understand failure and claim boundaries

**Story:** As a user, I want clear error and limitation messages so that I do
not confuse a small visualization with production or causal evidence.

**Acceptance criteria:**

- unreachable API and invalid input are distinguishable;
- Retry is available after a failed initial load;
- scientific limitations are visible inside the module.

**Status:** Completed.

**Evidence:** shared API error handlers, `api-client.ts`,
`NeuralNetworkExplainer.tsx`, `docs/limitations.md`.
