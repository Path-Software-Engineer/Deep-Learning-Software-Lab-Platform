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

### Neural Network Explainer bounded context

- defines the controlled XOR contract and 2–4–1 MLP;
- loads one checksum-verified checkpoint at service construction;
- executes PyTorch forward inference;
- creates transport-safe layer snapshots;
- returns registered offline training history.

### CNN Feature Map Viewer bounded context

- owns the official Fashion-MNIST sprite contract and deterministic split;
- loads one checksum-verified CNN checkpoint and registered sample gallery;
- validates registered samples or bounded temporary PNG/JPEG inputs;
- runs inference and captures only allowlisted ReLU activations through
  removable PyTorch forward hooks;
- preserves raw channel statistics and produces display-only normalized
  matrices;
- has no knowledge of HTTP or React.

### Offline pipeline

Each bounded context has its own deterministic offline training script. Sprint
1 writes the XOR evidence set. Sprint 2 fixes seed `20260728`, trains the Fashion
CNN and writes its checkpoint, manifest, sample gallery, history and metrics.

## Dependency rule

Dependencies point inward from interfaces to application and neural services.
The neural package has no knowledge of HTTP or React. The frontend has no
PyTorch or activation mathematics.

## Growth rule

The Neural Network Explainer and CNN Feature Map Viewer contexts are active.
The autoencoder context remains absent until Sprint 3 is explicitly authorized.
