# Week 4 exploration — Data and CNN foundation

## Questions

- How can the sprint remain reproducible without a runtime dataset download?
- Which source boundary is honest enough for a portfolio release?
- What architecture is small enough for CPU execution but rich enough to
  expose meaningful convolutional layers?

## Alternatives

- Full torchvision download: rejected because it adds network availability to
  reproduction.
- Synthetic geometric shapes: rejected because it would not satisfy the
  Fashion-MNIST product scope.
- Official Fashion-MNIST sprite: selected as a traceable 900-image source.

## Decisions

- Verify and version the sprite SHA-256.
- Use a deterministic 60/15/15 split per class.
- Register a two-block Conv-BN-ReLU-Pool model and preserve held-out evidence.
