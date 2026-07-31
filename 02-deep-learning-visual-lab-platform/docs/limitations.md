# Limitations and Claims Boundary

- XOR contains four synthetic observations and has no external validation set.
- The MLP is deliberately small and does not represent a deep production model.
- Perfect XOR accuracy is not evidence of generalization beyond this contract.
- Weights, biases, preactivations and activations are internal computations.
- An internal computation is not a causal explanation of model behavior.
- Line color and width encode API values for inspection; they do not encode
  importance.
- Reproducibility is guaranteed within the recorded code, dependency and
  execution boundary; exact floating-point equality across all hardware is not
  claimed.
- The platform is an educational engineering product, not a production model
  serving system.
- Sprint 2 uses 900 official Fashion-MNIST sprite images, not the complete
  70,000-image benchmark.
- The held-out set contains 150 controlled observations.
- Held-out accuracy of 81.33% describes only the registered split and model.
- Feature-map color is normalized independently per channel and is not directly
  comparable between maps.
- Feature maps are intermediate activations, not causal explanations or feature
  importance.
- Confidence values are model outputs, not calibrated guarantees.
- Temporary uploaded images are processed in memory and are not persisted.
- The autoencoder compresses each image into only two values; this visibility
  deliberately sacrifices reconstruction capacity.
- Held-out autoencoder evidence covers 150 images from the controlled sprite,
  not the complete Fashion-MNIST benchmark or an external dataset.
- Euclidean distance describes proximity only inside this registered 2D
  representation and does not guarantee semantic similarity.
- Smooth interpolation shows continuity of the registered decoder along one
  segment; it does not demonstrate understanding, disentanglement or causality.
- Reconstruction MSE and MAE describe pixel differences on `[0, 1]`; neither
  metric measures perceptual quality by itself.
- No module is production ready, and no output should drive consequential
  decisions.
