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
CNN and writes its registered evidence. Sprint 3 fixes seed `20260729`, trains a
convolutional autoencoder and writes its checkpoint, manifest, history,
100-point gallery and reconstruction metrics.

### Autoencoder Latent Space Demo bounded context

- reuses the verified Fashion-MNIST sprite and deterministic split;
- loads one checksum-verified autoencoder and registered latent gallery;
- calculates reconstruction error and Euclidean neighbors in the service;
- decodes interpolation coordinates with the actual registered decoder;
- exposes no model objects, tensors or latent mathematics to React.

## Dependency rule

Dependencies point inward from interfaces to application and neural services.
The neural package has no knowledge of HTTP or React. The frontend has no
PyTorch or activation mathematics.

## Growth rule

The Neural Network Explainer, CNN Feature Map Viewer and Autoencoder Latent
Space Demo are active, independent bounded contexts behind one versioned API
and one shared Next.js navigation shell.

## Production-shaped local topology

```text
browser
→ Next.js standalone container :3000
→ same-origin /api rewrite
→ FastAPI + PyTorch container :8000
→ immutable integrity-checked model artifacts
```

Both images use non-root users and health checks. There is no database because
the final product has no mutable accounts, projects or durable user workflow;
all runtime evidence is immutable and versioned in the repository.
