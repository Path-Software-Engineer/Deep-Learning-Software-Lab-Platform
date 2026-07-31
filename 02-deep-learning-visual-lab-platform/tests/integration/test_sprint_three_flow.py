from __future__ import annotations

from app.main import app
from fastapi.testclient import TestClient


def test_registered_artifact_drives_the_full_sprint_three_flow() -> None:
    with TestClient(app) as client:
        summary = client.get("/api/v1/autoencoder/summary").json()
        points = client.get("/api/v1/autoencoder/latent-points").json()
        reconstruction = client.post(
            "/api/v1/autoencoder/reconstruct",
            json={"point_id": "latent-08-00"},
        ).json()
        interpolation = client.post(
            "/api/v1/autoencoder/interpolate",
            json={
                "start_id": "latent-01-00",
                "end_id": "latent-09-00",
                "steps": 7,
            },
        ).json()

    assert summary["model"]["version"] == "fashion-autoencoder-2d-v1"
    assert summary["evaluation"]["samples"] == 150
    assert len(points["points"]) == 100
    assert reconstruction["model_version"] == summary["model"]["version"]
    assert reconstruction["sample"]["label"] == "Bag"
    assert len(reconstruction["neighbors"]) == 5
    assert interpolation["model_version"] == summary["model"]["version"]
    assert len(interpolation["steps"]) == 7
    assert interpolation["steps"][0]["alpha"] == 0.0
    assert interpolation["steps"][-1]["alpha"] == 1.0
