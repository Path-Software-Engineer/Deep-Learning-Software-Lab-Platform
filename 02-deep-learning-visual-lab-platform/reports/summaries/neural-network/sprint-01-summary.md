# Sprint 1 Technical Summary

The Neural Network Explainer uses a self-contained PyTorch 2–4–1 MLP trained
offline on the controlled XOR truth table. The registered artifact uses seed
`190`, Adam, `BCELoss`, learning rate `0.05` and `2000` epochs.

## Registered evidence

| Signal | Value |
|---|---:|
| Model version | `xor-mlp-v1` |
| Parameters | 17 |
| Controlled observations | 4 |
| Registered accuracy | 1.00 |
| Checkpoint integrity | SHA-256 verified |
| HTTP training endpoints | 0 |

The API exposes model metadata, one bounded forward trace and recorded training
history. The Next.js interface visualizes those values without recomputing
neural behavior.

## Boundary

This evidence demonstrates an inspectable educational model under a controlled
contract. It does not demonstrate generalization, production readiness or a
causal explanation of neural behavior.
