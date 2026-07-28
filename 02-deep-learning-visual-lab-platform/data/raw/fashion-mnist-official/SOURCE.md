# Fashion-MNIST source

Sprint 2 uses the official Fashion-MNIST sprite published by Zalando Research:

- Source repository: `zalandoresearch/fashion-mnist`
- Source asset: `doc/img/fashion-mnist-sprite.png`
- Local asset: `fashion-mnist-sprite.png`
- SHA-256: `a7de0a151f8c68e6e96f157a018ac290d1f6b0e7845892c3d7d85cb64961c3cb`
- Dimensions: 840 × 840 pixels
- Layout: 30 × 30 tiles of 28 × 28 pixels
- Class grouping: 90 consecutive images for each of the 10 official classes

The registered Sprint 2 experiment uses all 900 images from this sprite through
a deterministic, stratified split of 600 training, 150 validation and 150
held-out test observations. It is intentionally described as a curated official
subset and never as the complete 70,000-image Fashion-MNIST benchmark.

The upstream Fashion-MNIST repository publishes the dataset and utilities under
the MIT License. This file records provenance; it does not alter the upstream
license or ownership.
