# User Stories

## Sprint 1 — Neural Network Explainer

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

## Sprint 2 — CNN Feature Map Viewer

### US-P2-S2-001 — Select a valid fashion image

**Story:** As a student, I want to select a registered Fashion-MNIST sample or
temporarily upload a valid image so that I can inspect a real CNN inference.

**Acceptance criteria:**

- ten registered class samples are available;
- PNG/JPEG uploads are size, dimension and media-type bounded;
- ambiguous, missing and invalid inputs return typed errors;
- uploaded bytes are not persisted.

**Status:** Completed.

**Evidence:** `image_io.py`, `sample-gallery.json`, CNN FastAPI router, API and
component tests.

### US-P2-S2-002 — Inspect selected layers and channels

**Story:** As a student, I want to choose a convolutional layer and channels so
that I can compare their spatial activation patterns.

**Acceptance criteria:**

- only published layer IDs are accepted;
- one to twelve unique in-range channels are accepted;
- maps come from the registered PyTorch forward pass;
- the frontend performs no convolution or activation extraction.

**Status:** Completed.

**Evidence:** `hooks.py`, `service.py`, `/api/v1/cnn/feature-maps`,
`CnnFeatureMapViewer.tsx`, service and frontend tests.

### US-P2-S2-003 — Read prediction and tensor context

**Story:** As a student, I want the predicted class, confidence and tensor
metadata next to the maps so that I understand what was evaluated.

**Acceptance criteria:**

- all ten class probabilities and selected prediction are returned;
- input, activation and map shapes are explicit;
- each map identifies layer, operation, channel and raw statistics.

**Status:** Completed.

**Evidence:** CNN resources, `FeatureMapTile.tsx`, OpenAPI contract and
cross-layer tests.

### US-P2-S2-004 — Understand representation limitations

**Story:** As a user, I want visible evidence boundaries so that I do not
interpret feature maps as causal explanations.

**Acceptance criteria:**

- independent display normalization is disclosed;
- the 900-image source and 150-image holdout are disclosed;
- activation, confidence and production-readiness limitations remain visible.

**Status:** Completed.

**Evidence:** `config.py`, `docs/limitations.md`,
`CnnFeatureMapViewer.tsx`, Sprint 2 repository check.
