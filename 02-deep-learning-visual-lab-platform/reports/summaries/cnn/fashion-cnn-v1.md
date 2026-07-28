# CNN Feature Map Viewer — registered model evidence

## Dataset

- Source: Zalando Research official Fashion-MNIST sprite.
- Source SHA-256: `a7de0a151f8c68e6e96f157a018ac290d1f6b0e7845892c3d7d85cb64961c3cb`.
- Controlled subset: 900 images, 90 per class.
- Split: 600 training, 150 validation, 150 held-out evaluation images.

## Model

- Version: `fashion-cnn-v1`.
- Architecture: two Conv-BatchNorm-ReLU-Pool blocks and a 128-unit classifier.
- Checkpoint SHA-256: `9f07a60d97ef03ecb5b80086ddc9cd48077db5be5a89cd4663e2ec916bc7639e`.
- Training duration on the recorded CPU run: 19.30 seconds.

## Held-out evidence

- Accuracy: 0.8133 (122/150).
- Cross-entropy loss: 0.669677.

## Evidence boundary

This registered model is an educational release built from a curated official sprite,
not the complete Fashion-MNIST benchmark. Feature maps are intermediate activations,
not causal explanations, saliency maps or production-readiness evidence.
