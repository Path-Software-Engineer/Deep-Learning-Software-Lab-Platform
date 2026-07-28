# Week 6 exploration — Viewer experience

## Questions

- How can a user move from image to representation without a dense ML console?
- Which metadata must remain next to each map?
- How should the new module coexist with Sprint 1?

## Decisions

- Use a three-step workspace: input, layer and channels.
- Present prediction, input tensor and activation tensor before the map matrix.
- Keep raw min, mean and max on every feature-map card.
- Preserve the Axon identity and add explicit navigation between modules.
- Implement upload, loading, empty and error states without fabricated values.
