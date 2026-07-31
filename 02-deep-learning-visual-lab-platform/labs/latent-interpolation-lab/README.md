# Latent Interpolation Lab

## Question

What does the registered decoder produce along a straight segment between two
held-out 2D coordinates?

## Controlled procedure

1. Select two different IDs from the 100-point registered gallery.
2. Choose between three and twelve steps.
3. Linearly interpolate the two coordinates in the PyTorch service.
4. Decode every coordinate with `fashion-autoencoder-2d-v1`.
5. Return coordinates, alpha values and PNG evidence through FastAPI.

## Product decision

The browser sends only the point IDs and step count. It does not derive
coordinates or decode images. This keeps the visual result tied to the
registered checkpoint and makes invalid inputs fail through one contract.

## Interpretation boundary

A visually smooth sequence demonstrates local decoder continuity along one
chosen segment. It does not establish semantic control, disentanglement,
causality or model understanding.
