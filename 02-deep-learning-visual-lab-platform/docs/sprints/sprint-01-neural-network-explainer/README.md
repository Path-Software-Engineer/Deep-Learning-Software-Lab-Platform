# Sprint 1 — Neural Network Explainer

## Goal

Allow a user to enter XOR values and observe how a small PyTorch MLP transforms
the input into a prediction, while keeping the scientific claims bounded.

## Scope

Days 190–210 cover the controlled data contract, 2–4–1 model, explainable
forward snapshot, activation lab, reproducible offline training, checkpoint
integrity, application service, FastAPI contract, Next.js experience and
cross-layer validation.

## Completed increment

- Week 1: data, model, internal state capture and activation lab;
- Week 2: training, artifacts, service, API and reports;
- Week 3: Next.js client, interactive network, learning evidence, failures,
  responsive design and release preparation.

## Official outputs

- checkpoint `xor-mlp-v1.pt`;
- manifest and training history;
- metrics report;
- generated OpenAPI schema;
- Axon Next.js module;
- unit, contract, integration and component tests;
- root quality gate.

## Decisions

- PyTorch is the sole neural engine.
- Training is offline; requests are read-only except for bounded forward
  inference.
- React receives and displays neural values but does not calculate them.
- A visible limitation boundary accompanies every trace.
- No database is required for immutable versioned Sprint 1 artifacts.

## Acceptance

The implementation satisfies the functional and technical criteria through Day
210. A formal Gitflow release remains a separate authorized action. Live
browser screenshots must be regenerated after the corrected architecture is
running; screenshots from the superseded incompatible implementation are not
accepted.

## Weekly records

- [Week 1 exploration](week-01/exploration.md)
- [Week 1 review](week-01/review.md)
- [Week 2 exploration](week-02/exploration.md)
- [Week 2 review](week-02/review.md)
- [Week 3 exploration](week-03/exploration.md)
- [Week 3 review](week-03/review.md)
