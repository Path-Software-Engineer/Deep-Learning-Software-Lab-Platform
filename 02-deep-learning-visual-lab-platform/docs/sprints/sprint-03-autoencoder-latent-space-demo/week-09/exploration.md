# Week 9 Exploration

## Questions

- Which point set is small enough for an interactive client but broad enough to
  show every reference class?
- Should neighbors and interpolation be calculated in React or by the model
  service?
- How should invalid endpoints and step counts fail?

## Decision

Publish 100 registered held-out points, ten per class. FastAPI delegates
reconstruction, Euclidean-neighbor ranking and decoder interpolation to the
PyTorch service. Requests use typed resources and stable 422 error envelopes.
