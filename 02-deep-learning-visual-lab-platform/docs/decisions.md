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
