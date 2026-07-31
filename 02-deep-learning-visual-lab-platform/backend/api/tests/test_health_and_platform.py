from __future__ import annotations

from fastapi.testclient import TestClient


def test_health_reports_loaded_registered_artifact(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "deep-learning-visual-lab-api",
        "version": "1.0.0",
        "artifact": "xor-mlp-v1|fashion-cnn-v1|fashion-autoencoder-2d-v1",
    }


def test_platform_catalog_contains_all_implemented_sprint_modules(
    client: TestClient,
) -> None:
    response = client.get("/api/v1/platform/modules")
    assert response.status_code == 200
    assert response.json()["modules"] == [
        {
            "id": "neural-network-explainer",
            "name": "Neural Network Explainer",
            "description": "Inspect a registered PyTorch MLP and its forward trace.",
            "path": "/",
            "status": "available",
            "sprint": 1,
        },
        {
            "id": "cnn-feature-map-viewer",
            "name": "CNN Feature Map Viewer",
            "description": "Classify Fashion-MNIST images and inspect allowlisted feature maps.",
            "path": "/cnn",
            "status": "available",
            "sprint": 2,
        },
        {
            "id": "autoencoder-latent-space-demo",
            "name": "Autoencoder Latent Space Demo",
            "description": (
                "Compare reconstructions and inspect a registered "
                "two-dimensional latent representation."
            ),
            "path": "/autoencoder",
            "status": "available",
            "sprint": 3,
        },
    ]
