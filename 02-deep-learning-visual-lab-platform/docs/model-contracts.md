# Model and Artifact Contracts

## Registered model

- version: `xor-mlp-v1`;
- engine: PyTorch;
- topology: two inputs, four hidden neurons, one output;
- hidden activation: `tanh`;
- output activation: `sigmoid`;
- parameter count: `17`;
- task: binary XOR.

## Training

- seed: `190`;
- epochs: `2000`;
- optimizer: Adam;
- learning rate: `0.05`;
- loss: `BCELoss`;
- execution: offline through `scripts/train_neural_network.py`.

## Artifact set

- `models/neural-network/xor-mlp-v1.pt`;
- `models/neural-network/manifest.json`;
- `models/neural-network/training-history.json`;
- `reports/metrics/neural-network/xor-mlp-v1.json`.

The loader verifies model version, architecture, history configuration,
checkpoint size and SHA-256 before serving inference. A mismatch fails closed.

## Snapshot

Each layer snapshot includes its identifier, label, operation, weights, biases,
preactivations and activations. The snapshot contains only JSON-safe values and
does not expose live tensors or model objects.

## Claims

The artifacts prove a reproducible educational increment for the recorded code
and environment. They do not prove external validity or production readiness.
