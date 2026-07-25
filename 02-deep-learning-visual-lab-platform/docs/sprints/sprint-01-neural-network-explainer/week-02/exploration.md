# Week 2 Exploration — Days 197–203

## Questions

- Which artifact fields make an educational checkpoint reproducible?
- Where should checkpoint integrity be checked?
- How can the API prove that history is registered evidence and not request
  training?

## Decision

Register a checkpoint, training configuration, sampled loss history, metrics
and SHA-256 manifest as one bundle. Validate the checksum inside the artifact
repository before model construction. Expose read and inference endpoints only.

## Risks and controls

| Risk | Control |
|---|---|
| Silent checkpoint replacement | SHA-256 validation |
| Training during a request | No training use case or route |
| Contract drift | Pydantic resources, OpenAPI and contract tests |
| Stack trace or payload disclosure | Typed error envelope |
| Model/client identity mismatch | Version and checksum in responses |
