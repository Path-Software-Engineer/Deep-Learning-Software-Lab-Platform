"""Repository-level acceptance check for Sprint 2."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SOURCE_SHA256 = (
    "a7de0a151f8c68e6e96f157a018ac290d1f6b0e7845892c3d7d85cb64961c3cb"
)
REQUIRED_FILES = [
    "data/raw/fashion-mnist-official/fashion-mnist-sprite.png",
    "data/raw/fashion-mnist-official/SOURCE.md",
    "models/cnn/fashion-cnn-v1.pt",
    "models/cnn/manifest.json",
    "models/cnn/training-history.json",
    "models/cnn/sample-gallery.json",
    "reports/metrics/cnn/fashion-cnn-v1.json",
    "reports/summaries/cnn/fashion-cnn-v1.md",
    "frontend/lab-app/app/cnn/page.tsx",
    "frontend/lab-app/features/cnn/components/CnnFeatureMapViewer.tsx",
    "backend/api/app/cnn/interfaces/router.py",
    "docs/sprints/sprint-02-cnn-feature-map-viewer/README.md",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(65_536), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not (PROJECT_ROOT / path).is_file()]
    if missing:
        raise SystemExit(f"Missing Sprint 2 evidence: {', '.join(missing)}")

    if (PROJECT_ROOT / "ai-services" / "autoencoder-latent-space").exists():
        raise SystemExit("Sprint 3 implementation was opened before authorization.")

    source_path = (
        PROJECT_ROOT
        / "data"
        / "raw"
        / "fashion-mnist-official"
        / "fashion-mnist-sprite.png"
    )
    assert sha256(source_path) == EXPECTED_SOURCE_SHA256

    manifest = json.loads(
        (PROJECT_ROOT / "models" / "cnn" / "manifest.json").read_text(
            encoding="utf-8"
        )
    )
    assert manifest["model_version"] == "fashion-cnn-v1"
    assert manifest["dataset_source_sha256"] == EXPECTED_SOURCE_SHA256
    assert manifest["checkpoint_bytes"] > 0
    assert manifest["evaluation"]["samples"] == 150
    assert manifest["evaluation"]["correct"] == 122
    assert abs(manifest["evaluation"]["accuracy"] - 0.8133333325386047) < 1e-9

    router_source = (
        PROJECT_ROOT / "backend" / "api" / "app" / "cnn" / "interfaces" / "router.py"
    ).read_text(encoding="utf-8")
    for route in ('"/summary"', '"/samples"', '"/predict"', '"/feature-maps"'):
        assert route in router_source, f"missing Sprint 2 route: {route}"

    service_source = (
        PROJECT_ROOT
        / "ai-services"
        / "cnn-feature-map-viewer"
        / "src"
        / "cnn_feature_map_viewer"
        / "service.py"
    ).read_text(encoding="utf-8")
    assert "per-channel-min-max-for-display" in service_source
    assert "run_with_activations" in service_source

    frontend_source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (PROJECT_ROOT / "frontend" / "lab-app").rglob("*.tsx")
    )
    for forbidden in ("import torch", "torch.nn", "torch.tensor", "conv2d(", "convolve("):
        assert forbidden not in frontend_source.lower()
    assert "Activation is not explanation." in frontend_source

    print("OK - Sprint 2 CNN Feature Map Viewer check passed")
    print("Dataset: official 900-image Fashion-MNIST sprite with verified SHA-256")
    print("Evaluation: 122/150 correct | 81.33% held-out accuracy")
    print("Boundary: Next.js -> FastAPI -> controlled PyTorch hooks")


if __name__ == "__main__":
    main()
