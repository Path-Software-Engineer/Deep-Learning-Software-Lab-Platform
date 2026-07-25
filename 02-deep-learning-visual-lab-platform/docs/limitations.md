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
