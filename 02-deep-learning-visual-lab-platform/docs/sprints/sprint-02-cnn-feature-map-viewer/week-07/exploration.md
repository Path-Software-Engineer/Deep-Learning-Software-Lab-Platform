# Week 7 exploration — Release hardening

## Questions

- Which checks prove Sprint 2 without weakening Sprint 1?
- Which public claims can be supported by the registered evidence?
- What must remain explicitly outside the release?

## Decisions

- Run both Sprint checks through one root quality gate.
- Validate the official source and held-out metrics by checksum and values.
- Keep the autoencoder bounded context absent.
- Record visual validation at desktop, tablet and mobile widths.
- Release only after lint, types, tests, build, live HTTP flow and Git checks
  pass.
