# Week 11 Exploration

## Questions

- What is the smallest honest deployment boundary for the completed platform?
- Which generated artifacts must be excluded from Git?
- Which checks prove the three contexts still work together?

## Decision

Use a two-service Docker Compose topology: non-root FastAPI/PyTorch API and a
non-root standalone Next.js server. Keep immutable model evidence in the image,
validate all three sprints together and ignore TypeScript build metadata.
