# Technical Decisions

## ADR-001 — Self-contained PyTorch neural service

**Decision:** PyTorch is the sole neural engine in this repository.

**Reason:** The official map requires the Software project to implement its own
reproducible service boundary while sharing concepts—not runtime artifacts—with
the paired AI learning project.

## ADR-002 — Offline training and read-only HTTP inference

**Decision:** Training runs only through a local reproducible script. HTTP
exposes summary, forward trace and history.

**Reason:** Requests remain bounded, predictable and safe while evidence stays
versioned.

## ADR-003 — Artifact integrity is mandatory

**Decision:** The checkpoint is accepted only when its manifest, history,
configuration, size and SHA-256 agree.

**Reason:** Serving a stale or mismatched model would make the visual trace
misleading.

## ADR-004 — Dedicated frontend client

**Decision:** Components call a typed API client and never invoke HTTP directly
or reproduce neural formulas.

**Reason:** Presentation remains testable and contract drift is detectable.

## ADR-005 — SVG for the network

**Decision:** Use a semantic responsive SVG with keyboard-operable computed
nodes.

**Reason:** The topology is small and deterministic; SVG makes weights, node
selection and accessible labeling explicit without a visualization dependency.

## ADR-006 — No database in Sprint 1

**Decision:** Versioned files are sufficient for the immutable educational
checkpoint and history.

**Reason:** A database would add operations without solving a current product
requirement.

## ADR-007 — Same-origin local API proxy

**Decision:** Next.js rewrites `/api/*` to the configurable FastAPI
`API_PROXY_TARGET`. The browser uses relative API paths by default.

**Reason:** Local browser requests no longer depend on cross-port CORS behavior,
while FastAPI remains the only business API and production may still provide an
explicit `NEXT_PUBLIC_API_ROOT`.

## ADR-008 — Official sprite as a self-contained learning dataset

**Decision:** Sprint 2 versions the official 900-image Fashion-MNIST sprite and
records its SHA-256.

**Reason:** The release stays reproducible and honest about its limited evidence
without depending on a runtime download.

## ADR-009 — Controlled PyTorch hooks

**Decision:** Feature maps come from removable forward hooks on two allowlisted
ReLU layers.

**Reason:** The service observes the registered forward pass without modifying
the model or exposing arbitrary modules.

## ADR-010 — Raw image bodies instead of multipart

**Decision:** Prediction endpoints accept a registered sample ID or a bounded
raw PNG/JPEG body.

**Reason:** The contract remains small and requires no multipart dependency,
while preserving typed query controls and safe upload limits.

## ADR-011 — Per-channel display normalization

**Decision:** Every selected activation channel is mapped independently to
`[0, 1]` for display while raw statistics remain in the API.

**Reason:** Spatial patterns remain visible without falsely implying that color
intensity is comparable across channels.

## ADR-012 — No database in Sprint 2

**Decision:** Immutable dataset, model and report evidence remains file-based.

**Reason:** Sprint 2 has no mutable product state, user accounts or durable
runtime workflow that would justify persistence infrastructure.

## ADR-013 — Native two-dimensional bottleneck

**Decision:** The registered autoencoder learns exactly two latent values.

**Reason:** The product can display the actual representation without applying
a second projection. The accepted tradeoff is lower reconstruction capacity.

## ADR-014 — Server-owned latent operations

**Decision:** Reconstruction error, neighbor ranking and interpolation decoding
remain in the PyTorch bounded context.

**Reason:** Every visual result stays tied to the checksum-verified checkpoint;
React manages interaction without duplicating neural mathematics.

## ADR-015 — Reuse the verified official source

**Decision:** Sprint 3 reuses the Sprint 2 Fashion-MNIST sprite and split.

**Reason:** The complete project remains self-contained and its evidence stays
comparable. The limited 900-image scope remains explicit.

## ADR-016 — Two-container final local topology

**Decision:** Docker Compose runs a non-root standalone Next.js image and a
non-root FastAPI/PyTorch image with health checks.

**Reason:** The topology preserves frontend/backend separation and production
build behavior without adding a database or orchestrator unsupported by product
requirements.

## ADR-017 — No database in the final platform

**Decision:** Model and dataset evidence remains immutable and file-based.

**Reason:** Axon has no authentication, mutable experiment authoring, saved
workspace or durable user state. Persistence would add operational complexity
without serving a current use case.
