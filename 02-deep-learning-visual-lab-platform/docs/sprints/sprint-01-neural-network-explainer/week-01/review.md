# Week 1 Review — Days 190–196

| Day | Completed evidence |
|---:|---|
| 190 | Goal, scope, user/technical stories, risks and architecture decision |
| 191 | Minimal dependency/configuration base and ADRs |
| 192 | Fixed XOR tensor contract and tests |
| 193 | PyTorch MLP, shape and parameter tests |
| 194 | Structured snapshot serialization and reproducibility tests |
| 195 | Isolated activation behavior lab with claims boundary |
| 196 | Consolidated service unit tests and Week 1 documentation |

## Validation evidence

- XOR tensors: `[4, 2]` features and `[4, 1]` targets;
- architecture: 2 inputs, 4 hidden nodes, 1 output;
- parameter count: 17;
- snapshot order: hidden then output;
- production imports no code from `labs/`.

## Weekly closure

The model contract and representation boundary are stable enough to train and
register the official artifact in Week 2.
