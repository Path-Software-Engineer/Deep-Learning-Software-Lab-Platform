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

# Fashion-MNIST Sprint 2 Data Contract

Sprint 2 versions the official 840 × 840 Fashion-MNIST sprite as
`fashion-mnist-official-sprite-900-v1`. Its 30 × 30 grid contains 900
28 × 28 grayscale observations grouped into ten official classes.

- source SHA-256:
  `a7de0a151f8c68e6e96f157a018ac290d1f6b0e7845892c3d7d85cb64961c3cb`;
- training: 600 images, 60 per class;
- validation: 150 images, 15 per class;
- held-out test: 150 images, 15 per class;
- preprocessing: grayscale, bilinear resize to 28 × 28, `[0, 1]`, then
  `(pixel - 0.2860406) / 0.35302424`;
- runtime input tensor: `float32`, shape `[1, 1, 28, 28]`.

The source is a curated official subset, not the complete 70,000-image
benchmark. Provenance is recorded in
`data/raw/fashion-mnist-official/SOURCE.md`.

# Fashion-MNIST Sprint 3 Data Contract

Sprint 3 reuses the same source checksum and deterministic 600/150/150 split.
The autoencoder receives unstandardized grayscale values in `[0, 1]`, because
its sigmoid decoder produces values on that same reconstruction scale.

- model input and output: `float32`, shape `[N, 1, 28, 28]`;
- latent tensor: `float32`, shape `[N, 2]`;
- evaluation: pixel-level MSE and MAE over the 150-image held-out set;
- gallery: 100 held-out reference points, ten per class;
- runtime point identifiers: registered and allowlisted;
- interpolation: 3–12 coordinates on one straight line between two registered
  endpoints.

Reference labels remain source metadata. They do not turn the latent positions
into ground-truth semantic clusters.
