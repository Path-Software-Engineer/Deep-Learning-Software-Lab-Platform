# Sprint 2 — CNN Feature Map Viewer

## Goal

Allow a student to classify a Fashion-MNIST image and inspect selected
convolutional activations with enough metadata and limitations to interpret the
representation responsibly.

## Scope

Days 232–259 cover dataset provenance, deterministic CNN training, registered
artifacts, controlled hooks, display normalization, typed FastAPI resources,
the responsive Next.js viewer and cross-context validation.

## Completed increment

- Week 4: official source contract, model architecture and reproducible
  checkpoint;
- Week 5: activation capture, normalization, application service and API;
- Week 6: typed frontend client, samples/uploads, layer/channel controls and
  feature-map presentation;
- Week 7: adversarial validation, responsive review, documentation and release
  gate.

## Official outputs

- official 900-image sprite and provenance record;
- `fashion-cnn-v1.pt`, manifest, history and sample gallery;
- held-out metrics and Markdown summary;
- four versioned CNN API resources;
- Axon `/cnn` module;
- Python, API, contract, component and live E2E tests;
- Sprint 1 regression and Sprint 2 repository checks.

## Verified evidence

| Evidence | Result |
|---|---:|
| Model parameters | 207,018 |
| Training / validation / test | 600 / 150 / 150 |
| Validation accuracy | 85.33% (128/150) |
| Held-out accuracy | 81.33% (122/150) |
| Held-out loss | 0.669677 |
| Observable layers | 2 |
| Maximum selected channels | 12 |

## Decisions and limits

- PyTorch remains the sole neural engine.
- Runtime requests never train or mutate a checkpoint.
- Only two published ReLU layers are observable.
- Uploads are bounded, processed in memory and never persisted.
- Each map uses an independent display scale; raw statistics remain available.
- Feature maps are activations, not causal explanations.
- The 900-image source is not the complete Fashion-MNIST benchmark.
- Sprint 3 remains unopened.

## Weekly records

- [Week 4 exploration](week-04/exploration.md)
- [Week 4 review](week-04/review.md)
- [Week 5 exploration](week-05/exploration.md)
- [Week 5 review](week-05/review.md)
- [Week 6 exploration](week-06/exploration.md)
- [Week 6 review](week-06/review.md)
- [Week 7 exploration](week-07/exploration.md)
- [Week 7 review](week-07/review.md)
