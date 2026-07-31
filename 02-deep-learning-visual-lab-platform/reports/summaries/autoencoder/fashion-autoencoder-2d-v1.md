# Autoencoder Latent Space Demo — registered model evidence

## Dataset

- Source: Zalando Research official Fashion-MNIST sprite.
- Source SHA-256: `a7de0a151f8c68e6e96f157a018ac290d1f6b0e7845892c3d7d85cb64961c3cb`.
- Controlled subset: 900 images, 90 per class.
- Split: 600 training, 150 validation and 150 held-out test images.

## Model

- Version: `fashion-autoencoder-2d-v1`.
- Architecture: convolutional encoder, 2D bottleneck and convolutional decoder.
- Checkpoint SHA-256: `77462547e9d0eb1e95df72b1419398cc2d0f970fd394c4aec79d725d855586d4`.
- Recorded CPU training duration: 39.90 seconds.

## Reconstruction evidence

- Validation MSE: 0.033606.
- Validation MAE: 0.108231.
- Held-out MSE: 0.033027.
- Held-out MAE: 0.106527.

## Evidence boundary

The two-dimensional bottleneck is intentionally restrictive and makes the
representation visible at the cost of reconstruction capacity. Distance and
interpolation belong only to this registered model; neither is a causal or
universal semantic explanation.
