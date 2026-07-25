# Week 1 Exploration — Days 190–196

## Questions

- What is the smallest nonlinear model that makes internal transformations
  meaningful?
- Which values can be shown honestly without implying causal explanation?
- Should this repository own a framework model or consume another project's
  runtime?

## Alternatives

1. Implement a small self-contained PyTorch model.
2. Depend on an external educational engine through an adapter.
3. Serve static trace fixtures without a live model.

## Decision

Implement the official 2–4–1 MLP with PyTorch inside this repository. The
Software and AI paths may share concepts, but the deployed module must not
depend on an unrelated checkout or fabricate traces.

## Constraints

- exactly two binary features and one binary output;
- controlled XOR data and fixed seed;
- no client-side model mathematics;
- no runtime training endpoint;
- no future sprint scaffold;
- no causal explanation claims.
