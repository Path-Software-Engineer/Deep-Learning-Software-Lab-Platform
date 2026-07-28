# Week 5 exploration — Representation contract

## Questions

- Should activations be returned by modifying the model forward method or by
  hooks?
- How should maps be transported without hiding their raw magnitude?
- Which upload contract stays bounded without introducing multipart machinery?

## Alternatives

- Arbitrary module names: rejected because they expose internal implementation.
- Permanent hooks: rejected because lifecycle and memory ownership are unclear.
- Global normalization: rejected because outlier channels can hide spatial
  patterns.

## Decisions

- Use removable hooks on two published ReLU layers.
- Return bounded JSON matrices with raw statistics.
- Normalize each channel independently only for display.
- Accept either a registered sample ID or one raw PNG/JPEG body.
