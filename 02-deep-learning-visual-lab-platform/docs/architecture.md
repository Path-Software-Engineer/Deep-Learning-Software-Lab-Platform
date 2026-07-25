# Architecture

## System boundary

```text
Next.js presentation
→ dedicated TypeScript API client
→ FastAPI interfaces and Pydantic resources
→ application service
→ PyTorch model and registered artifacts
```

## Responsibilities

### Next.js

- renders controls, traces, training evidence and limitations;
- owns loading, empty, success and failure states;
- keeps only selected binary inputs and selected visual node as local state;
- never trains the model or recomputes neural values.

### FastAPI

- exposes the versioned HTTP contract;
- validates binary input and rejects unknown fields;
- delegates to the application service;
- maps validation and artifact failures to safe error envelopes;
- never performs training during a request.

### Neural Network Explainer

- defines the controlled XOR contract and 2–4–1 MLP;
- loads one checksum-verified checkpoint at service construction;
- executes PyTorch forward inference;
- creates transport-safe layer snapshots;
- returns registered offline training history.

### Offline pipeline

`scripts/train_neural_network.py` fixes seed `190`, trains with Adam and
`BCELoss`, and writes the checkpoint, manifest, history and metrics. These
artifacts form one versioned evidence set.

## Dependency rule

Dependencies point inward from interfaces to application and neural services.
The neural package has no knowledge of HTTP or React. The frontend has no
PyTorch or activation mathematics.

## Growth rule

Only the Neural Network Explainer context exists in Sprint 1. CNN and
autoencoder directories will be created when their sprints begin, avoiding
empty speculative architecture.
