from __future__ import annotations

from fastapi.testclient import TestClient


def test_health_reports_loaded_registered_artifact(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "deep-learning-visual-lab-api",
        "version": "0.1.0",
        "artifact": "xor-mlp-v1",
    }


def test_platform_catalog_contains_only_the_implemented_sprint_module(
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
        }
    ]
