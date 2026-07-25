"""Repository-level evidence check for the completed Sprint 1 boundary."""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "README.md",
    "pyproject.toml",
    "frontend/lab-app/package.json",
    "frontend/lab-app/app/page.tsx",
    "backend/api/app/main.py",
    "ai-services/neural-network-explainer/src/neural_network_explainer/model.py",
    "ai-services/neural-network-explainer/src/neural_network_explainer/artifacts.py",
    "ai-services/neural-network-explainer/src/neural_network_explainer/service.py",
    "scripts/train_neural_network.py",
    "models/neural-network/xor-mlp-v1.pt",
    "models/neural-network/manifest.json",
    "models/neural-network/training-history.json",
    "reports/metrics/neural-network/xor-mlp-v1.json",
    "docs/api/openapi.json",
    "docs/sprints/sprint-01-neural-network-explainer/README.md",
]


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not (PROJECT_ROOT / path).is_file()]
    if missing:
        raise SystemExit(f"Missing Sprint 1 evidence: {', '.join(missing)}")

    future_contexts = [
        PROJECT_ROOT / "ai-services" / "cnn-feature-map-viewer",
        PROJECT_ROOT / "ai-services" / "autoencoder-latent-space",
    ]
    opened = [str(path.relative_to(PROJECT_ROOT)) for path in future_contexts if path.exists()]
    if opened:
        raise SystemExit(f"Future sprint implementation opened early: {', '.join(opened)}")

    manifest = json.loads(
        (PROJECT_ROOT / "models" / "neural-network" / "manifest.json").read_text(
            encoding="utf-8"
        )
    )
    assert manifest["model_version"] == "xor-mlp-v1"
    assert manifest["model_configuration"]["hidden_size"] == 4
    assert manifest["metrics"]["accuracy"] == 1.0

    router_source = (
        PROJECT_ROOT
        / "backend"
        / "api"
        / "app"
        / "neural_network"
        / "interfaces"
        / "router.py"
    ).read_text(encoding="utf-8")
    for route in ('"/summary"', '"/forward"', '"/training-history"'):
        assert route in router_source, f"missing Sprint 1 route: {route}"
    for route in ('"/catalog"', '"/experiment"', '"/experiment/reset"', '"/experiment/train"'):
        assert route not in router_source, f"route outside Sprint 1 contract: {route}"

    frontend_source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (PROJECT_ROOT / "frontend" / "lab-app").rglob("*.tsx")
    )
    for forbidden in ("torch.", "Math.tanh", "Math.exp"):
        assert forbidden not in frontend_source

    print("OK - Sprint 1 integrated repository check passed")
    print("Boundary: Next.js -> FastAPI -> registered PyTorch checkpoint")
    print("Training: deterministic offline script; HTTP inference is read-only")


if __name__ == "__main__":
    main()
