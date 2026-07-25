# Week 3 Exploration — Days 204–210

## Primary flow

```text
open module
→ load summary, history and initial trace
→ choose x1/x2
→ request forward pass
→ inspect prediction and selectable nodes
→ review registered loss
→ read evidence boundaries
```

## UI states

- loading the artifact-backed workspace;
- connected with an initial trace;
- forward request in progress;
- typed backend error;
- API unavailable with Retry;
- no fabricated content when evidence is unavailable.

## Rendering decision

Use a responsive SVG for the network because its topology is small, semantic
and deterministic. Use HTML controls and panels around it. Weight sign changes
line color and magnitude changes width. A visible legend prevents ambiguous
encoding.

## Accessibility

- binary controls expose current state with `aria-pressed`;
- computed nodes support Enter and Space;
- SVG has an accessible label;
- errors use `role=alert`;
- loading uses `aria-live`;
- focus indicators and reduced motion are explicit.
