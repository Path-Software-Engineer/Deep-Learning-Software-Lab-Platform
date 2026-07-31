"""Repository-level acceptance check for Sprint 3 and the final platform."""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "models/autoencoder/fashion-autoencoder-2d-v1.pt",
    "models/autoencoder/manifest.json",
    "models/autoencoder/training-history.json",
    "models/autoencoder/latent-gallery.json",
    "reports/metrics/autoencoder/fashion-autoencoder-2d-v1.json",
    "reports/summaries/autoencoder/fashion-autoencoder-2d-v1.md",
    "frontend/lab-app/app/autoencoder/page.tsx",
    "frontend/lab-app/features/autoencoder/components/AutoencoderLatentSpaceDemo.tsx",
    "backend/api/app/autoencoder/interfaces/router.py",
    "docs/sprints/sprint-03-autoencoder-latent-space-demo/README.md",
    "docker-compose.yml",
    "backend/api/Dockerfile",
    "frontend/lab-app/Dockerfile",
    ".stitch/DESIGN.md",
    "scripts/start-local.ps1",
    "scripts/stop-local.ps1",
    "reports/visual-validation/sprint-03/README.md",
    "docs/releases/v1.0.0-deep-learning-visual-lab-platform.md",
]


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not (PROJECT_ROOT / path).is_file()]
    if missing:
        raise SystemExit(f"Missing Sprint 3 evidence: {', '.join(missing)}")

    manifest = json.loads(
        (PROJECT_ROOT / "models" / "autoencoder" / "manifest.json").read_text(
            encoding="utf-8"
        )
    )
    assert manifest["model_version"] == "fashion-autoencoder-2d-v1"
    assert manifest["checkpoint_bytes"] > 0
    assert manifest["evaluation"]["samples"] == 150
    assert manifest["evaluation"]["mean_squared_error"] < 0.05
    assert manifest["model_configuration"]["latent_dimensions"] == 2
    assert set(manifest["latent_bounds"]) == {"x", "y"}

    gallery = json.loads(
        (
            PROJECT_ROOT / "models" / "autoencoder" / "latent-gallery.json"
        ).read_text(encoding="utf-8")
    )
    assert len(gallery["points"]) == 100

    router_source = (
        PROJECT_ROOT
        / "backend"
        / "api"
        / "app"
        / "autoencoder"
        / "interfaces"
        / "router.py"
    ).read_text(encoding="utf-8")
    for route in (
        '"/summary"',
        '"/samples"',
        '"/latent-points"',
        '"/reconstruct"',
        '"/interpolate"',
    ):
        assert route in router_source, f"missing Sprint 3 route: {route}"

    frontend_source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (PROJECT_ROOT / "frontend" / "lab-app").rglob("*.tsx")
    ).lower()
    for forbidden in ("import torch", "torch.nn", "torch.tensor", "model.decode"):
        assert forbidden not in frontend_source
    assert "2d bottleneck" in frontend_source
    assert "summary.limitations.map" in frontend_source

    limitation_source = (
        PROJECT_ROOT
        / "ai-services"
        / "autoencoder-latent-space"
        / "src"
        / "autoencoder_latent_space"
        / "config.py"
    ).read_text(encoding="utf-8").lower()
    assert "latent proximity" in limitation_source
    assert "euclidean distance" in limitation_source

    platform_source = (
        PROJECT_ROOT
        / "backend"
        / "api"
        / "app"
        / "platform"
        / "interfaces"
        / "router.py"
    ).read_text(encoding="utf-8")
    for module in (
        "neural-network-explainer",
        "cnn-feature-map-viewer",
        "autoencoder-latent-space-demo",
    ):
        assert module in platform_source

    print("OK - Sprint 3 Autoencoder Latent Space Demo check passed")
    print(
        "Evidence: 150 held-out reconstructions | "
        f"MSE {manifest['evaluation']['mean_squared_error']:.6f}"
    )
    print("Platform: three bounded contexts | Next.js -> FastAPI -> PyTorch")


if __name__ == "__main__":
    main()
