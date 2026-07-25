# XOR Data Contract

| `x1` | `x2` | target |
|---:|---:|---:|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

The dataset is generated from constants in
`neural_network_explainer.dataset`; there is no external download, imputation,
split or hidden preprocessing.

## Tensor contract

- features: `float32`, shape `[4, 2]`;
- targets: `float32`, shape `[4, 1]`;
- inference input: `float32`, shape `[1, 2]`;
- allowed values: binary `0` and `1`.

The dataset is intentionally complete and tiny. Its role is to make a nonlinear
forward transformation inspectable, not to provide external evaluation.
