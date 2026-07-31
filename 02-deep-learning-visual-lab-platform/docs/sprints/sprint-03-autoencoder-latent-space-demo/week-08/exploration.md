# Week 8 Exploration

## Questions

- Can the existing official 900-image source support an honest autoencoder demo?
- Which bottleneck makes the representation directly inspectable?
- Which reconstruction metrics remain meaningful on the `[0, 1]` pixel scale?

## Alternatives

- A larger downloaded dataset would improve evidence but break the
  self-contained source boundary.
- A latent width above two would improve capacity but require a projection that
  could be mistaken for the model representation.
- A multilayer perceptron is simpler; a small convolutional encoder/decoder
  better preserves the image structure already used by Sprint 2.

## Decision

Reuse the verified official sprite and deterministic split. Train a compact
convolutional autoencoder with a native 2D bottleneck and evaluate MSE and MAE
on the held-out 150 images.
